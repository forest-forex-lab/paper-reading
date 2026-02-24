# Paper Reading & Reimplementation

ML/AI 論文の体系的な読解・サーベイ・再現実装を支援する Claude Code プロジェクト。

---

## セットアップ

```bash
# 1. Git LFS（PDF管理用）
brew install git-lfs
git lfs install

# 2. Python 依存関係のインストール
uv sync
```

> **注意**: パッケージ管理は `uv` を使用。`pip` は使わない。

---

## ディレクトリ構成

```
paper-reading/
├── papers/                        # 論文ディレクトリ（トピック別）
│   ├── inbox/                     #   PDF投入口（未分類）
│   ├── agents/                    #   LLM Agent 関連論文
│   ├── multi-agent-cooperation/   #   マルチエージェント協調
│   └── retrieval-augmented-generation/  # RAG 関連論文
│
├── surveys/                       # 文献サーベイ
│   └── deep-research/             #   Deep Research agents サーベイ
│
├── implementations/               # Python 再現実装
│
├── scripts/                       # ユーティリティスクリプト
│   ├── pdf_to_markdown.py         #   PDF → Markdown 変換（Docling）
│   └── compare_pdf_converters.py  #   PDF 変換エンジンの比較
│
├── docs/templates/                # テンプレート
│   ├── paper-notes.md             #   読解ノート用
│   ├── claims-analysis.md         #   Claim 分析用
│   ├── survey-template.md         #   サーベイ用
│   └── reimplementation-plan.md   #   再現実装計画用
│
├── memory/                        # セッション横断の記録
│   ├── reading-log.md             #   読書ログ（日付・ステータス付き）
│   ├── key-findings.md            #   重要な知見・パターン
│   └── open-questions.md          #   未解決の問い
│
├── .claude/
│   ├── agents/                    # SubAgent 定義（6種）
│   └── skills/                    # Slash Command 定義（8種）
│
├── AGENT.md                       # プロジェクト仕様書（Claude Code 用）
└── pyproject.toml                 # Python プロジェクト設定
```

### 論文ディレクトリの構造

各論文は `papers/<topic>/<first-author>-<year>/` に格納：

```
papers/agents/tomasev-2026/
├── paper.pdf              # 原本 PDF（Git LFS 管理）
├── paper.md               # PDF → Markdown 変換結果（自動生成）
├── paper_artifacts/       # 抽出された画像（自動生成）
│   └── image_000000_*.png
├── notes.md               # 構造化された読解ノート
├── claims.md              # Claim 単位の分析
└── README.md              # 1パラグラフ要約 + メタデータ
```

---

## ワークフローコマンド

### 基本ワークフロー

```
PDF 入手 → /organize-inbox → /read-paper → /translate-paper → /trace-citations
                                              ↓
                                         /survey（複数論文を横断）
                                              ↓
                                         /reimplement（必要に応じて）
```

### コマンド一覧

| コマンド | 説明 | SubAgent | Model |
|---------|------|----------|-------|
| `/organize-inbox` | inbox 内の PDF を自動分類・ディレクトリ配置 | inbox-classifier | Sonnet |
| `/read-paper <path>` | 論文の3パス読解 → notes.md, claims.md, README.md 生成 | paper-reader | Opus |
| `/translate-paper <path>` | paper.md を日本語に翻訳 → paper-ja.md 生成 | paper-translator | Sonnet |
| `/trace-citations <path>` | Semantic Scholar で引用チェーンを調査 | citation-tracer | Sonnet |
| `/survey <topic>` | Web 検索 + 既存ノートからサーベイ文書を生成 | literature-surveyor | Opus |
| `/reimplement <path>` | 論文手法を TDD で Python 再現実装 | reimplementer | Opus |
| `/compare-papers <paths...>` | 複数論文の比較分析 | — | — |
| `/paper-status` | 全論文・サーベイ・実装の進捗ダッシュボード | — | — |

---

## 各コマンドの詳細

### `/organize-inbox`

`papers/inbox/` に置いた PDF を自動的にトピック分類し、適切なディレクトリに配置する。

```bash
# 1. PDF を inbox に置く
cp ~/Downloads/new-paper.pdf papers/inbox/

# 2. コマンドを実行
/organize-inbox
```

処理内容:
1. PDF → Markdown 変換でメタデータ（タイトル、著者、年）を抽出
2. トピックを自動分類（agents, transformers, RL, etc.）
3. `papers/<topic>/<first-author>-<year>/` ディレクトリを作成し移動

### `/read-paper <path>`

論文を体系的に読解し、構造化されたノートを生成する。

```bash
/read-paper papers/agents/tomasev-2026/
```

処理内容:
1. **PDF → Markdown 変換**: `scripts/pdf_to_markdown.py` で `paper.md` を生成
2. **3パス読解プロトコル**:
   - **1st pass**: Abstract → Introduction → Conclusion で全体像を把握
   - **2nd pass**: Method セクション精読、数式・図を詳細に分析
   - **3rd pass**: Experiments, ablations, supplementary material
3. **成果物生成**: `notes.md`, `claims.md`, `README.md` をテンプレートに従い作成
4. **Memory 更新**: `reading-log.md`, `key-findings.md`, `open-questions.md` に追記

### `/translate-paper <path>`

`paper.md`（英語）を日本語に翻訳し、`paper-ja.md` を生成する。

```bash
/translate-paper papers/agents/wei-2026/
```

処理内容:
- セクション境界で Chunk 分割し、並列翻訳
- 技術用語（Attention, Transformer 等）は英語のまま維持
- 数式・図表参照・引用番号はそのまま保持

### `/survey <topic>`

指定トピックの文献サーベイを Web 検索と既存ノートから生成する。

```bash
/survey "deep research agents"
```

成果物:
- `surveys/<topic>/survey.md` — タイムライン、分類体系、比較表、トレンド分析
- Mermaid 図（関係図、分類フローチャート）を含む

### `/trace-citations <path>`

Semantic Scholar API を使い、論文の引用チェーン（被引用・参照文献）を調査する。

```bash
/trace-citations papers/agents/tomasev-2026/
```

成果物:
- `citations.md` — 被引用論文・参照文献のリストと要約

### `/reimplement <path>`

論文のコア手法を Python で TDD 再現実装する。

```bash
/reimplement papers/agents/tomasev-2026/
```

ワークフロー: RED → GREEN → REFACTOR サイクルで、pytest 80%+ coverage を目標に実装。

---

## PDF → Markdown 変換

論文の読解は必ず PDF → Markdown 変換を経由する。

```bash
# 基本的な使い方
uv run python scripts/pdf_to_markdown.py papers/agents/tomasev-2026/paper.pdf

# 出力先とファイル名を指定
uv run python scripts/pdf_to_markdown.py paper.pdf --output-dir ./output --output-name result.md
```

- **変換エンジン**: [Docling](https://github.com/docling-project/docling)
- **出力**: `paper.md`（Markdown 本文）+ `paper_artifacts/`（抽出画像）
- Markdown 内で `![Image](paper_artifacts/image_xxxx.png)` として画像を参照

---

## SubAgent アーキテクチャ

各コマンドは専用の SubAgent に処理を委譲する。SubAgent 定義は `.claude/agents/` に配置。

```
┌─────────────────────────────────┐
│  Claude Code (Main Session)     │
│  - コマンド受付・ファイル管理     │
│  - Memory 更新                   │
└─────────┬───────────────────────┘
          │ Task tool (subagent_type: "general-purpose")
          │
    ┌─────┴──────────────────────────────────────────┐
    │                                                  │
    ▼              ▼              ▼              ▼     │
┌────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐ │
│ paper- │  │ paper-    │  │literature│  │citation-│ │
│ reader │  │translator │  │-surveyor │  │ tracer  │ ...
│(Opus)  │  │(Sonnet)   │  │(Opus)    │  │(Sonnet) │
└────────┘  └───────────┘  └──────────┘  └─────────┘
```

### SubAgent 一覧

| Agent | Model | 主な役割 |
|-------|-------|---------|
| `paper-reader` | Opus | 3パス読解、notes.md / claims.md / README.md 生成 |
| `paper-translator` | Sonnet | Chunk ベースの英日翻訳（技術用語保持） |
| `inbox-classifier` | Sonnet | PDF メタデータ抽出、トピック分類 |
| `literature-surveyor` | Opus | Web 検索 + 既存ノート統合によるサーベイ生成 |
| `citation-tracer` | Sonnet | Semantic Scholar 経由の引用チェーン調査 |
| `reimplementer` | Opus | TDD ベースの Python 再現実装 |

---

## Memory システム

`memory/` ディレクトリでセッション間の状態を永続管理する。

| ファイル | 内容 | 更新タイミング |
|---------|------|--------------|
| `reading-log.md` | 読書ログ（日付・ステータス・論文パス） | 論文読解後 |
| `key-findings.md` | 重要な知見・論文間の関連パターン | 重要な発見時 |
| `open-questions.md` | 未解決の問い・追跡すべき研究テーマ | 問いの発生・解決時 |

ステータス: `[INBOX]` → `[READING]` → `[DONE]`（または `[SKIMMED]`）

---

## 認識論的スタンス

論文を扱う際の基本姿勢:

- **Claims（主張）** と **Evidence（証拠）** を厳密に区別する
- 「著者は〜と主張している」「結果は〜を示唆する」のように Hedge する
- 独立検証されていない主張を確定事実として扱わない
- 方法論的限界（データセット規模、評価指標、ベースライン不足等）を明記する

---

## 技術スタック

| 技術 | 用途 |
|------|------|
| **Claude Code** | Skills, SubAgents, Memory による研究ワークフロー自動化 |
| **Python 3.13+** | 再現実装（pytest, type hints, immutable patterns） |
| **uv** | Python パッケージ管理 |
| **Docling** | PDF → Markdown 変換エンジン |
| **Git LFS** | 論文 PDF のバージョン管理 |
| **Semantic Scholar API** | 引用チェーン調査 |
