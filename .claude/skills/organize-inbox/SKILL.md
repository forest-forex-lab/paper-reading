---
name: organize-inbox
description: Scan papers/inbox/ for PDFs, extract metadata, and organize them into the proper directory structure.
---

# /organize-inbox

Scan `papers/inbox/` for PDF files and organize them into `papers/<topic>/<author-year>/`.

## Arguments

- `$ARGUMENTS` — (optional) Specific PDF filename in inbox to process. If omitted, process all PDFs in inbox.

## Workflow

### Step 1: Scan Inbox

- List all `.pdf` files in `papers/inbox/`
- If `$ARGUMENTS` specifies a filename, process only that file
- If no PDFs found, report "inbox is empty" and exit
- Report the list of PDFs found to the user

### Step 2: For Each PDF — Extract Metadata

For each PDF file:

1. **Convert to Markdown** (temporary, for metadata extraction):
   - Run: `uv run python scripts/pdf_to_markdown.py <pdf_path> --output-dir papers/inbox/_tmp_<filename>`
   - This generates a temporary markdown + images for reading

2. **Read first ~100 lines** of the generated markdown to extract:
   - **Title** — the paper title
   - **Authors** — list of authors (identify first author's last name)
   - **Year** — publication year
   - **Venue** — conference or journal (if identifiable)
   - **Topic** — classify into a topic category

3. **Determine topic**:
   - Check existing `papers/` subdirectories for matching topics
   - Suggest the most appropriate existing topic, or propose a new topic slug
   - Topic should be lowercase, hyphenated (e.g., `retrieval-augmented-generation`, `vision-transformers`, `diffusion-models`)

4. **Construct destination path**:
   - Format: `papers/<topic>/<first-author-lastname>-<year>/`
   - Author name: lowercase ASCII (e.g., `vaswani-2017`, `brown-2020`)
   - If directory already exists, warn and ask user

### Step 3: Confirm with User

Present a summary table for all PDFs to be organized:

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

### Step 4: Move and Convert

For each approved PDF:

1. **Create destination directory**: `mkdir -p papers/<topic>/<author-year>/`
2. **Move PDF**: `mv papers/inbox/<file>.pdf papers/<topic>/<author-year>/paper.pdf`
3. **Run full conversion**: `uv run python scripts/pdf_to_markdown.py papers/<topic>/<author-year>/paper.pdf`
   - This generates `paper.md` and `paper_artifacts/` in the proper location
4. **Clean up**: Remove temporary conversion files from inbox (`papers/inbox/_tmp_*`)

### Step 5: Report Results

```
=== Organization Complete ===

Moved 2 papers:
  papers/transformers/vaswani-2017/   — "Attention Is All You Need"
  papers/language-models/devlin-2019/ — "BERT: Pre-training of Deep..."

Remaining in inbox: 0 PDFs
```

### Step 6: Update Memory (optional)

- If papers were successfully organized, optionally append to `memory/reading-log.md` with status `[INBOX]`

## Topic Classification Guidelines

Use these topic categories as reference (create new ones as needed):

- `transformers` — Transformer architecture and variants
- `language-models` — LLMs, pretraining, fine-tuning
- `retrieval-augmented-generation` — RAG, retrieval-based methods
- `vision` — Computer vision, image classification, detection
- `vision-transformers` — ViT and variants
- `diffusion-models` — Diffusion-based generative models
- `reinforcement-learning` — RL, RLHF, reward models
- `optimization` — Training methods, optimizers, learning rate
- `agents` — LLM agents, tool use, planning
- `multimodal` — Vision-language, audio-text models
- `evaluation` — Benchmarks, metrics, evaluation methods
- `interpretability` — Explainability, mechanistic interpretability
- `efficiency` — Pruning, quantization, distillation, efficient inference

## Error Handling

- If `docling` is not installed, prompt: `uv sync`
- If metadata extraction fails, fall back to asking user for title/author/year manually
- If destination directory already exists, ask user whether to overwrite or choose a different name

## Important

- **Always confirm with user before moving files**
- Clean up all temporary files (`_tmp_*`) after processing
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English.
