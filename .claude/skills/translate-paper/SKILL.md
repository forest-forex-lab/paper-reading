---
name: translate-paper
description: Translate a paper's Markdown (paper.md) into Japanese (paper-ja.md), preserving technical terms, equations, and formatting.
---

# /translate-paper

Translate a paper's Markdown into Japanese.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/agents/tomasev-2026/`) or to `paper.md` directly

## Workflow

### Step 1: Locate paper.md

1. If a directory path is given, look for `paper.md` inside it.
2. If a file path is given, use it directly.
3. If `paper.md` does not exist, inform the user and suggest running `/read-paper` first to convert the PDF.
4. Check if `paper-ja.md` already exists. If so, ask the user whether to overwrite.

### Step 2: Translate

Read `paper.md` and translate its content into Japanese **section by section**.

For long papers, process in chunks of ~300 lines to stay within context limits:
1. Read a chunk with the Read tool (using `offset` and `limit`).
2. Translate the chunk following the rules below.
3. Append the translated text to an accumulator.
4. Repeat until the entire file is processed.

### Step 3: Write output

Write the complete translated text to `paper-ja.md` in the same directory as `paper.md`.

## Translation Rules

1. **Technical terms**: Keep in English as-is. Do NOT translate:
   - Model/method names (Transformer, Attention, Embedding, Softmax, RAG, etc.)
   - Proper nouns (dataset names, benchmark names, tool names)
   - Abbreviations (LLM, RL, MARL, QA, etc.)
2. **Mathematical notation**: Preserve exactly as written (`$...$`, `$$...$$`, LaTeX commands).
3. **Markdown formatting**: Preserve all formatting:
   - Headings (`#`, `##`, etc.)
   - Lists (`-`, `*`, `1.`)
   - Bold/italic (`**...**`, `_..._`)
   - Code blocks (`` ``` ``)
   - Image references (`![...](figures/...)`)
   - Table structure (`|...|`)
4. **Citations**: Keep author names and years as-is (e.g., "Vaswani et al., 2017").
5. **Figure/Table/Equation references**: Keep numbering as-is (e.g., "Figure 1", "Table 2", "Eq. 3"). Translate only the label word if natural (e.g., "Figure 1" can remain or become "図1").
6. **Section headings**: Translate heading text but keep numbering (e.g., "## 3. Method" -> "## 3. 手法").
7. **Abstract**: Translate fully.
8. **Tone**: Use academic Japanese (である調). Maintain the paper's register.
9. **Page artifacts**: Remove page numbers, headers/footers, and other conversion artifacts if present.

## Important

- Always read `paper.md` first — never read the PDF directly.
- Process section by section to maintain translation quality and context.
- If a section is too domain-specific and you are uncertain about terminology, flag it and proceed with your best translation.
- Output language is always Japanese. The `--en` flag is NOT applicable to this skill.
