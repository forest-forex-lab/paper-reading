---
name: read-paper
description: Systematically read and annotate an academic paper, producing structured notes following the project template.
---

# /read-paper

Systematically read an academic paper and create structured notes.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`) or PDF file
- Optional flag: `--en` — Output notes and conversation in English (default: Japanese)

## Workflow

### Step 0: PDF → Markdown 変換

1. **Locate the PDF**: Find `paper.pdf` in the given path. If a PDF path is given directly, use that.
2. **Check for existing conversion**: If `paper.md` already exists in the paper directory, skip conversion and ask the user if they want to re-convert.
3. **Convert PDF to Markdown**:
   - Run: `python scripts/pdf_to_markdown.py <pdf_path>`
   - This generates `paper.md` (Markdown text with image references) and `figures/` (extracted images as PNG)
   - If `pymupdf4llm` is not installed, prompt the user to run `pip install -r scripts/requirements.txt`
4. **Verify conversion**: Confirm `paper.md` exists and `figures/` contains extracted images.

### Step 0.5: Japanese Translation (Optional)

- After conversion, ask the user if they want a Japanese translation (`paper-ja.md`).
- If yes, invoke `/translate-paper` on the paper directory.
- If `paper-ja.md` already exists, skip and notify the user.
- Subsequent reading passes use `paper-ja.md` if it exists, falling back to `paper.md`.

### Step 1: First Pass — Scope

- Read the beginning of `paper.md` (Abstract, Introduction)
- Read images in `figures/` referenced in the text to understand key diagrams
- Identify the core problem, proposed solution, and claimed contributions
- Report a one-sentence summary to the user and ask if they want to continue

### Step 2: Second Pass — Method

- Read the Method/Approach section from `paper.md`
- View figures referenced in this section using Read tool (e.g., `figures/img_0005.png`)
- Note key equations, referencing by paper numbering (Eq. 1, etc.)
- Note architectural choices and design decisions
- Ask the user if any section needs deeper exploration

### Step 3: Third Pass — Evidence

- Read Experiments and Results sections from `paper.md`
- View result figures and tables (extracted as images in `figures/`)
- Catalog each claim with its supporting evidence
- Note datasets, baselines, metrics, and statistical rigor
- Flag any methodological concerns

### Step 4: Generate Notes

- Create `notes.md` following `docs/templates/paper-notes.md`
  - Embed key figure references: `![Figure 1](figures/img_xxxx.png)`
- Create `claims.md` following `docs/templates/claims-analysis.md`
- Create `README.md` with a one-paragraph summary and metadata

### Step 5: Update Memory

- Append entry to `memory/reading-log.md`
- Add any significant findings to `memory/key-findings.md`
- Add any open questions to `memory/open-questions.md`

## Important

- **Always convert PDF to Markdown first** — do not read PDF directly
- Figures extracted from the PDF are viewable with the Read tool (`figures/*.png`)
- Embed important figure references in `notes.md` for later review
- Maintain epistemic stance: distinguish claims from evidence
- Use the paper's original notation for equations and terminology
- Ask the user for input between passes — this is an interactive process
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless of output language.
