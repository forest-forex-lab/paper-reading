---
name: paper-status
description: Display a dashboard showing the status of all papers, surveys, and implementations in the project.
---

# /paper-status

Show the current status of all papers, surveys, and implementations.

## Workflow

1. **Scan Papers**:
   - List all directories under `papers/`
   - For each paper directory, check for: `paper.pdf`, `notes.md`, `claims.md`, `README.md`
   - Determine status: No Notes / Notes Only / Fully Analyzed

2. **Scan Surveys**:
   - List all directories under `surveys/`
   - For each survey, check for: `survey.md`, `comparison-table.md`
   - Show topic and completeness

3. **Scan Implementations**:
   - List all directories under `implementations/`
   - For each implementation, check for: `README.md`, `src/`, `tests/`
   - If tests exist, report test status (run `pytest --co -q` to count tests without executing)

4. **Read Memory**:
   - Show recent entries from `memory/reading-log.md`
   - Show count of open questions from `memory/open-questions.md`

5. **Display Dashboard**:

   ```
   === Paper Reading Project Status ===

   Papers (N total):
     [ANALYZED] topic/author-year — Paper Title
     [NOTES]    topic/author-year — Paper Title
     [PDF ONLY] topic/author-year

   Surveys (N total):
     [COMPLETE] topic — N papers covered
     [DRAFT]    topic

   Implementations (N total):
     [TESTED]  paper-name — N tests passing
     [WIP]     paper-name
     [PLANNED] paper-name

   Recent Activity:
     - YYYY-MM-DD: Read "Paper Title"

   Open Questions: N
   ```

## Important

- This is a **read-only** operation — do not modify any files
- Keep the output concise and scannable
- Use consistent status labels
