---
name: survey
description: Create a comprehensive literature survey on a given topic using web search and existing notes.
---

# /survey

Create a literature survey on the specified topic by delegating to the `literature-surveyor` sub-agent.

## Arguments

- `$ARGUMENTS` — Topic to survey (e.g., "vision transformers", "diffusion models for text generation")
- Optional flag: `--en` — Output survey in English (default: Japanese)

## Workflow

### Step 1: Delegate to literature-surveyor sub-agent (main agent)

Determine language:
- If `--en` is in `$ARGUMENTS` → `lang = en`
- Otherwise → `lang = ja`

1. **Read the agent instructions**: Read the file `.claude/agents/literature-surveyor.md` to get the full agent instructions.
2. **Launch a single sub-agent**: Use the Task tool with `subagent_type: "general-purpose"` and include the agent instructions in the prompt.

The prompt should be structured as:

```
You are the literature-surveyor agent. Follow these instructions:

<paste full content of .claude/agents/literature-surveyor.md here>

---

Now perform the following task:

topic: <extracted topic from $ARGUMENTS>
lang: <ja or en>

1. Define the survey scope based on the topic.
2. Determine time range (default: last 5 years unless specified).
3. Search the web (Semantic Scholar, arXiv, Google Scholar, Papers With Code, OpenReview) for relevant papers.
4. Check existing `papers/` and `surveys/` directories for already-read papers.
5. Read any existing `notes.md` files for papers related to this topic.
6. Create survey directory: `surveys/{topic-slug}/`.
7. Generate `survey.md` following `docs/templates/survey-template.md`.
8. Generate `comparison-table.md` with detailed structured comparison.
9. Update `memory/key-findings.md` and `memory/open-questions.md`.
```

### Step 2: Report to user (main agent)

After the sub-agent completes, report:
- The survey output path (`surveys/{topic-slug}/survey.md`)
- Key themes and number of papers covered

## Important

- **Do NOT perform the survey in the main context.** All research and writing is done by the sub-agent.
- The main agent only handles: sub-agent delegation (Step 1) and reporting (Step 2).
- **Language**: Default output is Japanese. If `--en` is in `$ARGUMENTS`, output all documents and conversation in English. Technical terms (Attention, Transformer, etc.) remain in English regardless.
