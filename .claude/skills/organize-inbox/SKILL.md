---
name: organize-inbox
description: Scan papers/inbox/ for PDFs, extract metadata, and organize them into the proper directory structure.
---

# /organize-inbox

Scan `papers/inbox/` for PDF files and organize them into `papers/<topic>/<author-year>/` using parallel classification via sub-agents.

## Arguments

- `$ARGUMENTS` — (optional) Specific PDF filename in inbox to process. If omitted, process all PDFs in inbox.

## Workflow

### Step 1: Scan Inbox (main agent)

- List all `.pdf` files in `papers/inbox/` using `ls papers/inbox/*.pdf`
- If `$ARGUMENTS` specifies a filename, process only that file
- If no PDFs found, report "inbox is empty" and exit
- Get the list of existing topic directories: `ls papers/` (to pass to sub-agents)

### Step 2: Parallel Classification (sub-agents)

1. **Read the agent instructions**: Read the file `.claude/agents/inbox-classifier.md` to get the full agent instructions.
2. **Launch classifier agents**: For each PDF, launch a sub-agent using the Task tool with `subagent_type: "general-purpose"` and `model: "sonnet"`.

Each sub-agent prompt should be structured as:

```
You are the inbox-classifier agent. Follow these instructions:

<paste full content of .claude/agents/inbox-classifier.md here>

---

Now perform the following task:

pdf_path: papers/inbox/<filename>.pdf
existing_topics: <comma-separated list of existing topic directories>

Follow the instructions above to:
1. Convert the PDF temporarily for metadata extraction
2. Extract title, authors, year, venue
3. Classify into an appropriate topic
4. Clean up temporary files
5. Return the METADATA_START/METADATA_END block
```

**Launch ALL classifier agents in parallel** (multiple Task tool calls in a single response).

### Step 3: Confirm with User (main agent)

Parse each sub-agent's `METADATA_START/METADATA_END` block and present a summary table:

```
=== Inbox Organization Plan ===

| # | PDF Filename           | Title                          | Destination                              |
|---|------------------------|--------------------------------|------------------------------------------|
| 1 | attention_is_all.pdf   | Attention Is All You Need      | papers/transformers/vaswani-2017/        |
| 2 | bert_pretraining.pdf   | BERT: Pre-training of Deep...  | papers/language-models/devlin-2019/      |
```

Ask the user to:
- **Approve all** — proceed with all proposed destinations
- **Edit** — modify specific topic or author-year for individual papers
- **Skip** — skip specific PDFs

### Step 4: Move and Convert (main agent)

For each approved PDF:

1. **Create destination directory**: `mkdir -p papers/<topic>/<author-year>/`
2. **Move PDF**: `mv papers/inbox/<file>.pdf papers/<topic>/<author-year>/paper.pdf`
3. **Run full conversion**: `uv run python scripts/pdf_to_markdown.py papers/<topic>/<author-year>/paper.pdf`
   - This generates `paper.md` and `paper_artifacts/` in the proper location
4. **Clean up**: Remove any remaining temporary files from inbox (`rm -rf papers/inbox/_tmp_*`)

### Step 5: Report Results (main agent)

```
=== Organization Complete ===

Moved N papers:
  papers/<topic>/<author-year>/ — "<title>"
  ...

Remaining in inbox: M PDFs
```

### Step 6: Update Memory (optional)

- If papers were successfully organized, optionally append to `memory/reading-log.md` with status `[INBOX]`

## Error Handling

- If `docling` is not installed, prompt: `uv sync`
- If a sub-agent fails to extract metadata (returns `CONVERSION_FAILED` or `unknown` fields), fall back to asking the user for title/author/year manually
- If destination directory already exists, ask user whether to overwrite or choose a different name

## Important

- **Do NOT read PDF content in the main context.** All metadata extraction is done by sub-agents.
- **Always confirm with user before moving files** (Step 3)
- Clean up all temporary files (`_tmp_*`) after processing
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English.
