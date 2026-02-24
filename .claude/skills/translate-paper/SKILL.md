---
name: translate-paper
description: Translate a paper's Markdown (paper.md) into Japanese (paper-ja.md), preserving technical terms, equations, and formatting.
---

# /translate-paper

Translate a paper's Markdown into Japanese using parallel chunk translation via sub-agents.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/agents/tomasev-2026/`) or to `paper.md` directly

## Workflow

### Step 1: Locate paper.md and validate

1. If a directory path is given, look for `paper.md` inside it.
2. If a file path is given, use it directly.
3. If `paper.md` does not exist, inform the user and suggest running `/read-paper` first to convert the PDF.
4. Check if `paper-ja.md` already exists. If so, ask the user whether to overwrite.

### Step 2: Analyze structure and plan chunks

Do NOT read the full paper.md content. Instead:

1. Run `wc -l <paper.md>` to get total line count.
2. Run `grep -n '^#' <paper.md>` to find section heading positions.
3. **Identify the References section boundaries**:
   - Find the heading for References (e.g., `# References`, `## References`, `# Bibliography`). Record its line number as `references_start_line`.
   - Find the next heading **at the same or higher level** after References (e.g., Appendix). Record its line number as `references_end_line`. If there is no subsequent heading, `references_end_line` = total line count + 1.
   - The References section spans `[references_start_line, references_end_line - 1]`.
4. Plan chunk boundaries at section headings, targeting **200-300 lines per chunk** (hard maximum: 350 lines).
   - **Skip the References section**: create chunks for lines before it and lines after it (e.g., Appendix), but not for the References section itself.
   - Never split in the middle of a section — always split at a heading boundary.
   - If a section exceeds 300 lines even at finest sub-heading granularity, split at the **nearest blank line** after ~250 lines.
   - **Rationale**: Dense survey prose (274 lines) hit the 32K output token limit at the previous 500-line cap. 200-300 lines provides a 2x safety margin.
5. Record chunk plan as a list of `(start_line, end_line, chunk_index)`.
6. Record the references range: `(references_start_line, references_end_line - 1)` — this will be copied as-is (untranslated) in Step 4.

### Step 2.5: Clean stale chunk files

Before launching sub-agents, remove any chunk files from previous runs:
```bash
rm -f <paper_dir>/paper-ja-chunk-*.md <paper_dir>/paper-ja-references.md
```

### Step 3: Parallel chunk translation

1. **Read the agent instructions**: Read the file `.claude/agents/paper-translator.md` to get the full agent instructions.
2. **Launch chunk agents**: For each chunk, launch a sub-agent using the Task tool with `subagent_type: "general-purpose"` and `model: "sonnet"`.

Each sub-agent prompt should be structured as:

```
You are the paper-translator agent. Follow these instructions:

<paste full content of .claude/agents/paper-translator.md here>

---

Now perform the following task:

Source file: <paper.md path>
Output file: <paper_dir>/paper-ja-chunk-<N>.md
Read lines: offset=<start_line - 1>, limit=<end_line - start_line + 1>

Read the specified lines from the source file, translate following all translation rules above, and write the result to the output file.
```

**Launch ALL chunk agents in parallel** (multiple Task tool calls in a single response).

### Step 3.5: Verify chunk outputs

1. **File existence**: `test -f` each chunk file. Missing = CHUNK_FAILED.

2. **Line count ratio**: `wc -l` each chunk. If output < 70% of input lines → CONTENT_LOSS.

3. **Section coverage**: `grep -n '^#' <chunk_file>` and compare against the headings expected from Step 2. Missing heading → SECTION_MISSING.

4. **Handle failures**:
   - CHUNK_FAILED → Re-launch that sub-agent. Two failures → report to user.
   - CONTENT_LOSS → Split chunk in half, re-launch as two chunks. Both fail → report to user.
   - SECTION_MISSING → Report missing sections with line numbers, ask user.

### Step 4: Assemble and clean up

After all sub-agents complete:

1. **Extract the References section** (untranslated) from the original `paper.md`:
   ```bash
   sed -n '<references_start_line>,<references_end_line>p' <paper.md> > <paper_dir>/paper-ja-references.md
   ```
2. Concatenate all translated chunk files and the untranslated References section **in document order**:
   - Chunks before References → `paper-ja-references.md` → Chunks after References (e.g., Appendix)
   ```bash
   cat <paper_dir>/paper-ja-chunk-0.md ... <paper_dir>/paper-ja-references.md <paper_dir>/paper-ja-chunk-N.md ... > <paper_dir>/paper-ja.md
   ```
3. Remove temporary chunk files:
   ```bash
   rm <paper_dir>/paper-ja-chunk-*.md <paper_dir>/paper-ja-references.md
   ```
4. Report completion to the user with the output path.
5. **Post-assembly verification**:
   ```bash
   wc -l <paper_dir>/paper-ja.md
   wc -l <paper_dir>/paper.md
   grep -c '^#' <paper_dir>/paper-ja.md
   grep -c '^#' <paper_dir>/paper.md
   ```
   Report to user:
   ```
   Original: <N> lines (<H> headings) | Translated: <M> lines (<J> headings)
   Body coverage: <body_ja / body_orig * 100>% (excluding References)
   ```
   If body coverage < 90%, warn the user before reporting completion.

## Important

- **Do NOT read the full paper.md into the main context.** Only use `wc -l` and `grep -n` for structure analysis.
- Each sub-agent handles its own chunk independently — no context sharing between chunks.
- The chunking in Step 2 is an internal processing strategy. Do not ask the user for confirmation on chunk boundaries.
- Output language is always Japanese. The `--en` flag is NOT applicable to this skill.
- If the paper is short (< 300 lines), use a single sub-agent instead of splitting.
