---
name: trace-citations
description: Trace the citation chain of a paper — both papers it cites and papers that cite it.
context: fork
agent: citation-tracer
---

# /trace-citations

Trace citation chains for a given paper.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`) or paper title/identifier
- Optional flag: `--en` — Output in English (default: Japanese)

## Instructions for the citation-tracer agent

1. **Identify the Paper**:
   - If a path is given, read `notes.md` or `README.md` to get the paper title and authors
   - If a title is given, search for the paper on Semantic Scholar or Google Scholar

2. **Backward Citations (References)**:
   - Identify the key references cited by this paper
   - For each reference, provide: title, authors, year, venue, one-sentence contribution
   - Classify references by role: foundational, methodological, baseline/comparison, dataset, tangential
   - Highlight the most influential references (those central to the paper's method)

3. **Forward Citations (Cited By)**:
   - Search for papers that cite this work
   - For the top cited-by papers, provide: title, authors, year, venue, how they build on this work
   - Classify: extends, applies, improves upon, competes with, surveys

4. **Citation Graph**:
   - Create a summary showing the paper's position in the citation network
   - Identify citation clusters and research threads

5. **Output**:
   - Write results to `{paper-directory}/citations.md` (or `citations-{paper-slug}.md` in current directory if no paper directory)
   - Format with clear sections for backward and forward citations

## Notes

- Use Semantic Scholar API when possible for structured citation data
- Fall back to Google Scholar and arXiv for additional coverage
- Keep individual paper summaries to 1-2 sentences for efficiency
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless.
