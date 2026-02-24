---
name: read-paper
description: Systematically read and annotate an academic paper, producing structured notes following the project template.
---

# /read-paper

Systematically read an academic paper and create structured notes by delegating to the `paper-reader` sub-agent.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`) or PDF file
- Optional flag: `--en` — Output notes and conversation in English (default: Japanese)

## Workflow

### Step 0: PDF → Markdown Conversion (main agent)

1. **Locate the PDF**: Find `paper.pdf` in the given path. If a PDF path is given directly, use that.
2. **Check for existing conversion**: If `paper.md` already exists in the paper directory, skip conversion and ask the user if they want to re-convert.
3. **Convert PDF to Markdown**:
   - Run: `uv run python scripts/pdf_to_markdown.py <pdf_path>`
   - This generates `paper.md` (Markdown text with image references) and `paper_artifacts/` (extracted images as PNG)
   - If `docling` is not installed, prompt the user to run `uv sync`
4. **Verify conversion**: Confirm `paper.md` exists and `paper_artifacts/` contains extracted images.

### Step 0.5: Japanese Translation Check (main agent)

- If `paper-ja.md` already exists in the paper directory, the sub-agent will use it for reading (preferred over `paper.md`).
- If it does not exist, proceed with `paper.md`. Do not ask whether to translate.

### Step 1: Delegate to paper-reader sub-agent

Determine which source file to use:
- If `paper-ja.md` exists → `source_file = paper-ja.md`
- Otherwise → `source_file = paper.md`

Determine language:
- If `--en` is in `$ARGUMENTS` → `lang = en`
- Otherwise → `lang = ja`

1. **Read the agent instructions**: Read the file `.claude/agents/paper-reader.md` to get the full agent instructions.
2. **Launch a single sub-agent**: Use the Task tool with `subagent_type: "general-purpose"` and include the agent instructions in the prompt.

The prompt should be structured as:

```
You are the paper-reader agent. Follow these instructions:

<paste full content of .claude/agents/paper-reader.md here>

---

Now perform the following task:

paper_dir: <paper_directory_path>
source_file: <source_file name>
lang: <ja or en>

1. Read `<paper_dir>/<source_file>` following the 3-pass reading protocol above.
2. View figures in `<paper_dir>/paper_artifacts/` using the Read tool.
3. Read the templates at `docs/templates/paper-notes.md` and `docs/templates/claims-analysis.md`.
4. Generate `notes.md`, `claims.md`, and `README.md` in `<paper_dir>/` following the templates.
5. End your response with the SUMMARY_START/SUMMARY_END block as specified above.

Important:
- Maintain strict epistemic stance — distinguish claims from evidence.
- Use the paper's original notation for equations and terminology.
- Ensure Core Thesis, Intellectual Lineage, and Key Design Decisions sections are substantive.
```

### Step 2: Update Memory (main agent)

After the sub-agent completes, parse the `SUMMARY_START/SUMMARY_END` block from its response and:

1. **Append to `memory/reading-log.md`**:
   ```
   - YYYY-MM-DD: **<paper_title>** (<venue>) — <one_sentence_summary> → `<paper_dir>/`
   ```

2. **Append to `memory/key-findings.md`** (if significant findings):
   ```
   ### <paper_title> (YYYY-MM-DD)
   - <key_finding_1>
   - <key_finding_2>
   ```

3. **Append to `memory/open-questions.md`** (if open questions):
   ```
   ### <paper_title> (YYYY-MM-DD)
   - <open_question_1>
   - <open_question_2>
   ```

4. **Report to user**: Display the one-sentence summary, key findings, and note that `notes.md`, `claims.md`, and `README.md` have been generated.

## Important

- **Do NOT read the full paper.md in the main context.** All reading is done by the sub-agent.
- The main agent only handles: PDF conversion (Step 0), sub-agent delegation (Step 1), and memory updates (Step 2).
- The sub-agent writes `notes.md`, `claims.md`, and `README.md` directly.
- Run Steps 0 through 2 continuously without pausing for confirmation between steps. Only stop to ask the user if: (a) a step fails and requires a decision, or (b) the user explicitly asked to run in interactive mode (`--interactive` flag).
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless of output language.
