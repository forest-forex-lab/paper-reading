---
name: read-paper
description: Systematically read and annotate an academic paper, producing structured notes following the project template.
---

# /read-paper

Systematically read an academic paper and create structured notes.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`) or PDF file

## Workflow

1. **Locate the PDF**: Find `paper.pdf` in the given path. If a PDF path is given directly, use that.

2. **First Pass — Scope** (pages 1-3 typically):
   - Read Abstract, Introduction, and Conclusion
   - Identify the core problem, proposed solution, and claimed contributions
   - Report a one-sentence summary to the user and ask if they want to continue

3. **Second Pass — Method**:
   - Read the Method/Approach section in detail
   - Note key equations, referencing by paper numbering (Eq. 1, etc.)
   - Note architectural choices and design decisions
   - Ask the user if any section needs deeper exploration

4. **Third Pass — Evidence**:
   - Read Experiments and Results sections
   - Catalog each claim with its supporting evidence
   - Note datasets, baselines, metrics, and statistical rigor
   - Flag any methodological concerns

5. **Generate Notes**:
   - Create `notes.md` following `docs/templates/paper-notes.md`
   - Create `claims.md` following `docs/templates/claims-analysis.md`
   - Create `README.md` with a one-paragraph summary and metadata

6. **Update Memory**:
   - Append entry to `memory/reading-log.md`
   - Add any significant findings to `memory/key-findings.md`
   - Add any open questions to `memory/open-questions.md`

## Important

- Use `pages` parameter when reading PDFs (max 20 pages per request)
- Maintain epistemic stance: distinguish claims from evidence
- Use the paper's original notation for equations and terminology
- Ask the user for input between passes — this is an interactive process
