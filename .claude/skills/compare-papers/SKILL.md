---
name: compare-papers
description: Compare multiple papers side by side, analyzing their approaches, results, and trade-offs.
---

# /compare-papers

Compare multiple papers and produce a structured analysis.

## Arguments

- `$ARGUMENTS` — Space-separated paths to paper directories (e.g., `papers/topic/paper1 papers/topic/paper2`)
- Optional flag: `--en` — Output in English (default: Japanese)

## Workflow

1. **Read Existing Notes**:
   - For each paper path, read `notes.md` and `claims.md`
   - If notes don't exist for a paper, notify the user and suggest running `/read-paper` first

2. **Build Comparison**:
   - **Problem framing**: How does each paper define the problem?
   - **Method**: Key differences in approach, architecture, training procedure
   - **Evaluation**: Datasets, metrics, baselines used by each paper
   - **Results**: Direct comparison where papers report on the same benchmarks
   - **Trade-offs**: Compute cost, complexity, generalizability, assumptions

3. **Generate Comparison Table**:

   | Dimension | Paper A | Paper B | ... |
   |-----------|---------|---------|-----|
   | Problem | ... | ... | |
   | Core idea | ... | ... | |
   | Architecture | ... | ... | |
   | Key metric | ... | ... | |
   | Strengths | ... | ... | |
   | Weaknesses | ... | ... | |

4. **Analysis**:
   - Which paper makes stronger empirical claims?
   - Where do the papers agree/disagree?
   - What would a synthesis of these approaches look like?
   - Which approach is more promising for future work and why?

5. **Output**:
   - Present the comparison directly to the user
   - Optionally save to a file if the user requests it

## Important

- Maintain epistemic stance: clearly attribute claims to specific papers
- Note when comparisons are not apples-to-apples (different datasets, metrics, etc.)
- Highlight complementary strengths that could be combined
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless.
