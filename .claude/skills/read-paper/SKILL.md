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
   - Run: `uv run python scripts/pdf_to_markdown.py <pdf_path>`
   - This generates `paper.md` (Markdown text with image references) and `paper_artifacts/` (extracted images as PNG)
   - If `docling` is not installed, prompt the user to run `uv sync`
4. **Verify conversion**: Confirm `paper.md` exists and `paper_artifacts/` contains extracted images.

### Step 0.5: Japanese Translation Check

- If `paper-ja.md` already exists in the paper directory, use it for subsequent reading passes (preferred over `paper.md`).
- If it does not exist, proceed with `paper.md`. Do not ask whether to translate — the user can invoke `/translate-paper` separately if desired.

### Step 1: First Pass — Scope

- Read the beginning of `paper.md` (Abstract, Introduction)
- Read images in `paper_artifacts/` referenced in the text to understand key diagrams
- Identify the core problem, proposed solution, and claimed contributions
- Report a one-sentence summary to the user and proceed to the next step

### Step 2: Second Pass — Method, Design Philosophy, & Intellectual Lineage

This pass extracts not just WHAT the method is, but WHY it was designed this way and WHERE its ideas come from.

#### 2a: Core Thesis & Design Philosophy

Before diving into technical details, identify the paper's intellectual stance:

- **Core thesis**: What is the fundamental insight or bet? (e.g., "in-context learning can replace explicit meta-learning")
- **What they reject**: What conventional assumptions do they challenge?
- **What they bet on**: What principle or mechanism do they trust instead?

Report these to the user before proceeding to technical details.

#### 2b: Intellectual Lineage

For each significant prior work referenced in the Method section, identify:

1. **Source concept**: What specific idea, mechanism, or framework is borrowed?
2. **Original context**: How was this concept used in the original work?
3. **Transformation**: How does this paper adapt, extend, or combine it?

This is NOT a bibliography — it's a map of "which ideas flowed from where into this design."

Examples of what to capture:
- "Borrowed the contract-first principle from formal verification, adapted it as a decomposition stopping criterion"
- "Extended FeUdal Networks' Manager-Worker hierarchy from single-agent HRL to multi-agent delegation"
- "Combined Press & Dyson's extortion strategies with sequence model in-context learning"

#### 2c: Method & Key Design Decisions

- Read the Method/Approach section from `paper.md`
- View figures referenced in this section using Read tool
- For each significant design choice, identify:
  - **What** was chosen
  - **Why** (the rationale — look for justification in the text)
  - **Alternatives** (what else could have been done, whether discussed by authors or not)
- Note key equations, referencing by paper numbering (Eq. 1, etc.)
- Note architectural choices and technical details

Proceed to the next step. (The user can interrupt at any point if they want deeper exploration.)

### Step 3: Third Pass — Evidence

- Read Experiments and Results sections from `paper.md`
- View result figures and tables (extracted as images in `paper_artifacts/`)
- Catalog each claim with its supporting evidence
- Note datasets, baselines, metrics, and statistical rigor
- Flag any methodological concerns

### Step 4: Generate Notes

- Create `notes.md` following `docs/templates/paper-notes.md`
  - Embed key figure references: `![Figure 1](paper_artifacts/image_xxxx.png)`
  - **CRITICAL**: Ensure the following sections are substantive (not placeholders):
    - **Core Thesis & Design Philosophy**: Must articulate WHY, not just WHAT
    - **Intellectual Lineage**: Must have at least 3 entries with Source → Original → Adaptation
    - **Key Design Decisions**: Must list at least 3 decisions with rationale and alternatives
    - **Technical Details**: Must include specific equations, architecture, algorithms
- Create `claims.md` following `docs/templates/claims-analysis.md`
- Create `README.md` with a one-paragraph summary and metadata

### Step 5: Update Memory

- Append entry to `memory/reading-log.md`
- Add any significant findings to `memory/key-findings.md`
- Add any open questions to `memory/open-questions.md`

## Important

- **Always convert PDF to Markdown first** — do not read PDF directly
- Figures extracted from the PDF are viewable with the Read tool (`paper_artifacts/*.png`)
- Embed important figure references in `notes.md` for later review
- Maintain epistemic stance: distinguish claims from evidence
- Use the paper's original notation for equations and terminology
- Run all passes (Steps 1 through 5) continuously without pausing for confirmation between steps. Only stop to ask the user if: (a) a step fails and requires a decision, or (b) the user explicitly asked to run in interactive mode (`--interactive` flag).
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless of output language.
