# Meta-Refactor History

Optimization decisions log — committable to version control.

---

### 2026-02-24 — Anti-rationalization rule
- **Change**: Added Error Handling rule 5 to AGENT.md: prohibit rationalizing output discrepancies; require reporting raw numbers and investigating instead
- **Friction addressed**: Communication Inefficiency / User Corrections — fabricated explanation for 203-line output gap, user forced to challenge (2 events)
- **Status**: applied

### 2026-02-24 — Read tool large-file guidance
- **Change**: Added "Tool Usage Constraints" section to AGENT.md with Read tool token limits (25K), mandatory `wc -l` check, offset/limit for large files
- **Friction addressed**: Tool Misuse — Read on 75K-token file without offset/limit (1 event)
- **Status**: applied

### 2026-02-24 — Edit tool staleness warning
- **Change**: Added Edit tool subsection to "Tool Usage Constraints" in AGENT.md: re-read before editing modified files, prefer Write/cat for assembled output
- **Friction addressed**: Failed Approaches — Edit "String not found" on concurrently modified file (1 event)
- **Status**: applied

### 2026-02-24 — Communication style preferences
- **Change**: Added "Communication Style" section to AGENT.md: execute operational tasks directly with minimal preamble, reserve verbose planning for analytical tasks
- **Friction addressed**: Communication Inefficiency — verbose plan mode interrupted by user for routine task (1 event)
- **Status**: applied

### 2026-02-24 — Sub-agent progress reporting
- **Change**: Added launch status + incremental completion reporting to translate-paper SKILL.md Step 3
- **Friction addressed**: Missing Automation — user manually polled sub-agent progress (1 event)
- **Status**: applied
