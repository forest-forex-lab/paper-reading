---
name: survey
description: Create a comprehensive literature survey on a given topic using web search and existing notes.
context: fork
agent: literature-surveyor
---

# /survey

Create a literature survey on the specified topic.

## Arguments

- `$ARGUMENTS` — Topic to survey (e.g., "vision transformers", "diffusion models for text generation")
- Optional flag: `--en` — Output survey in English (default: Japanese)

## Instructions for the literature-surveyor agent

1. **Scope Definition**:
   - Define the survey scope based on the topic: `$ARGUMENTS`
   - Determine time range (default: last 5 years unless specified)
   - Identify key subtopics and categories

2. **Gather Sources**:
   - Search the web (Semantic Scholar, arXiv, Google Scholar, Papers With Code, OpenReview) for relevant papers
   - Check existing `papers/` and `surveys/` directories for already-read papers
   - Read any existing `notes.md` files for papers related to this topic

3. **Build Survey**:
   - Create survey directory: `surveys/{topic-slug}/`
   - Generate `survey.md` following `docs/templates/survey-template.md`:
     - Timeline of key papers
     - Taxonomy of approaches (with mermaid diagram)
     - Comparison table (approach, dataset, metrics, results, code availability)
     - Key themes and trends
     - Relationship diagram between papers (mermaid)
     - Open problems and future directions
   - Generate `comparison-table.md` with detailed structured comparison

4. **Update Memory**:
   - Add key findings to `memory/key-findings.md`
   - Add open questions to `memory/open-questions.md`

## Output

The survey document at `surveys/{topic-slug}/survey.md` with all sections completed.

## Language

Default output is Japanese. If `--en` is in `$ARGUMENTS`, output all documents and conversation in English. Technical terms (Attention, Transformer, etc.) remain in English regardless.
