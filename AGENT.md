# Paper Reading & Reimplementation Agent

This project supports systematic reading, surveying, and reimplementing ML/AI research papers.

---

## Epistemic Stance

When discussing papers, maintain intellectual neutrality:

- **Hedge claims**: Use "the authors claim...", "results suggest...", "the paper proposes..."
- **Distinguish clearly**:
  - **Claims** — what authors assert
  - **Evidence** — empirical results, proofs, ablations supporting claims
  - **Unverified** — claims lacking sufficient evidence or independent replication
- **Never present a paper's claims as established fact** unless independently verified
- **Note methodological limitations** (dataset size, evaluation metrics, missing baselines, compute assumptions)
- **Flag potential confounds** and alternative explanations

---

## Technical Communication

- Use technical terms precisely; do not paraphrase standard terminology
- Preserve original terms: Attention, Transformer, Embedding, Softmax, Cross-Entropy, Gradient, Backpropagation, etc.
- Reproduce mathematical notation as written in the paper (e.g., $\mathcal{L}$, $\theta$, $\nabla$)
- When a paper introduces novel terminology, quote it on first use and provide a brief gloss
- Reference equations, figures, and tables by their paper-internal numbering (e.g., "Eq. 3", "Figure 2a", "Table 1")

---

## Language Policy

- **デフォルト出力言語: 日本語**
- `--en` フラグが指定された場合は英語で出力する
- Technical terms（専門用語）は原語（英語）のまま維持する
  - 例: Attention, Transformer, Embedding, Loss, Gradient 等は訳さない
- 論文タイトルは原語で引用する
- 数式の説明文は出力言語に従うが、変数名・記号は論文のまま

---

## File Conventions

### Paper Directory Structure

Each paper lives under `papers/<topic>/<first-author>-<year>/`:

```
papers/
  inbox/                   # PDF投入口（/organize-inbox で自動分配）
    new-paper.pdf
  transformers/
    vaswani-2017/
      paper.pdf            # Original PDF (Git LFS)
      paper.md             # PDF→Markdown変換結果（自動生成）
      figures/             # PDFから抽出した画像（自動生成）
        img_0001.png
      notes.md             # Reading notes (from template)
      claims.md            # Claim-by-claim analysis (from template)
      README.md            # One-paragraph summary + metadata
```

### notes.md Structure

Follow `docs/templates/paper-notes.md`:
- One-Sentence Summary
- Problem Statement
- Proposed Method
- Key Claims (numbered)
- Methodology Assessment
- Results Summary
- Limitations & Open Questions
- Connections to Other Work
- Personal Notes / Questions

### claims.md Structure

Follow `docs/templates/claims-analysis.md`:
- Each claim analyzed for: Type, Evidence, Methodology, Potential Issues, Reproducibility, Status

### Survey Structure

Surveys live under `surveys/<topic>/`:
```
surveys/
  vision-transformers/
    survey.md              # Main survey document
    papers.bib             # Bibliography (optional)
    comparison-table.md    # Structured comparison
```

---

## Workflow Commands

The following `/slash-commands` are available:

| Command | Description | Mode |
|---------|-------------|------|
| `/organize-inbox` | inbox内のPDFを自動分類・配置 | Interactive |
| `/read-paper <path>` | Systematically read and annotate a paper | Interactive |
| `/survey <topic>` | Create a literature survey on a topic | SubAgent (literature-surveyor) |
| `/trace-citations <path>` | Trace citation chains for a paper | SubAgent (citation-tracer) |
| `/reimplement <path>` | Reimplement a paper's method in Python | Interactive |
| `/translate-paper <path>` | paper.md を日本語に翻訳（paper-ja.md 生成） | Interactive |
| `/compare-papers <paths...>` | Compare multiple papers side by side | Interactive |
| `/paper-status` | Show project-wide progress dashboard | Read-only |

---

## PDF Handling

### PDF → Markdown 変換（読解の前提）

論文の読解は必ず **PDF→Markdown変換→Markdown読解** の順で実施する:

1. **変換**: `uv run python scripts/pdf_to_markdown.py <paper.pdf>` を実行
   - `paper.md` が生成される（Markdown形式の論文本文）
   - `figures/` に画像が抽出される（PNG）
   - Markdown内で `![](figures/img_xxxx.png)` として画像が参照される
2. **読解**: 生成された `paper.md` を Read ツールで読み、分析を行う
   - 画像は Read ツールで直接表示可能
   - PDF を直接読む必要はない

### 変換ツールのセットアップ

```bash
uv sync
uv run python scripts/pdf_to_markdown.py <paper.pdf>
```

### 読解の順序

- **First pass**: Abstract → Introduction → Conclusion で全体像を把握
- **Second pass**: Method セクションを精読、数式・図を参照
- **Third pass**: Experiments, ablations, supplementary material

### Git LFS

- PDFは Git LFS で管理（`*.pdf` は `.gitattributes` で追跡）
- 変換後の `paper.md` と `figures/` はgit通常管理

---

## Implementation Standards

### Language & Environment
- **Python 3.10+** as default language
- **Virtual environment**: `venv` in each implementation directory
- **Package management**: `uv` with `pyproject.toml`

### Code Quality
- **Type hints** on all function signatures
- **Immutable patterns**: Prefer creating new objects over mutation
- **Docstrings**: Google-style for public functions
- **Testing**: `pytest` with 80%+ coverage target
- **Linting**: Follow project `.flake8` / `ruff` config if present

### Implementation Directory Structure
```
implementations/
  <paper-name>/
    README.md              # Implementation plan + deviations from paper
    requirements.txt
    src/
      __init__.py
      model.py
      train.py
      data.py
      utils.py
    tests/
      test_model.py
      test_data.py
    configs/
      default.yaml
    results/
      figures/
```

### TDD Workflow
1. Write test describing expected behavior
2. Run test — confirm it FAILS
3. Implement minimal code to pass
4. Run test — confirm it PASSES
5. Refactor while keeping tests green
6. Check coverage (target: 80%+)

---

## Memory System

The `memory/` directory maintains cross-session state:

| File | Purpose | Update Frequency |
|------|---------|-----------------|
| `memory/reading-log.md` | Chronological log of papers read with dates and status | After each paper reading session |
| `memory/key-findings.md` | Important insights, patterns, and connections across papers | When significant findings emerge |
| `memory/open-questions.md` | Unresolved questions and research threads to follow | As questions arise or get resolved |

### Update Rules
- **Append** new entries; do not delete resolved items (mark as `[RESOLVED]` instead)
- **Keep entries concise**: 1-3 lines per item
- **Cross-reference**: Link to specific paper directories when relevant
- **Date all entries**: Use ISO 8601 format (YYYY-MM-DD)

---

## SubAgents

Four specialized SubAgents are available in `.claude/agents/`:

| Agent | Model | Specialty |
|-------|-------|-----------|
| `paper-reader` | opus | Deep paper analysis with strict epistemic stance |
| `literature-surveyor` | opus | Web search + existing notes for survey generation |
| `citation-tracer` | sonnet | High-volume citation chain investigation |
| `reimplementer` | opus | TDD-based Python reimplementation |

---

## Quality Checklist

Before finalizing any paper notes or analysis:
- [ ] All claims are labeled with evidence status
- [ ] Methodology limitations are noted
- [ ] Connections to related work are identified
- [ ] Mathematical notation matches the paper
- [ ] Templates are followed consistently
- [ ] Memory files are updated if warranted
