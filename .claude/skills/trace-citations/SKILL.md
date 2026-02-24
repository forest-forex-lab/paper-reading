---
name: trace-citations
description: Trace the citation chain of a paper — both papers it cites and papers that cite it.
---

# /trace-citations

Trace citation chains for a given paper by delegating to the `citation-tracer` sub-agent.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`) or paper title/identifier
- Optional flag: `--en` — Output in English (default: Japanese)

## Workflow

### Step 1: Delegate to citation-tracer sub-agent (main agent)

Determine language:
- If `--en` is in `$ARGUMENTS` → `lang = en`
- Otherwise → `lang = ja`

1. **Read the agent instructions**: Read the file `.claude/agents/citation-tracer.md` to get the full agent instructions.
2. **Launch a single sub-agent**: Use the Task tool with `subagent_type: "general-purpose"` and `model: "sonnet"` and include the agent instructions in the prompt.

The prompt should be structured as:

```
You are the citation-tracer agent. Follow these instructions:

<paste full content of .claude/agents/citation-tracer.md here>

---

Now perform the following task:

target: <paper path or title from $ARGUMENTS>
lang: <ja or en>

1. If a path is given, read `notes.md` or `README.md` to get the paper title and authors.
2. If a title is given, search for the paper on Semantic Scholar or Google Scholar.
3. Trace backward citations (references) — classify each as foundational, methodological, baseline, dataset, or tangential.
4. Trace forward citations (cited by) — classify each as extends, applies, improves, competes, or surveys.
5. Write results to `{paper-directory}/citations.md`.
```

### Step 2: Report to user (main agent)

After the sub-agent completes, report:
- The output file path
- Summary of citation statistics (total references, total citations)

## Important

- **Do NOT perform the citation tracing in the main context.** All search and analysis is done by the sub-agent.
- The main agent only handles: sub-agent delegation (Step 1) and reporting (Step 2).
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output in English. Technical terms remain in English regardless.
