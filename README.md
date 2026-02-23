# Paper Reading & Reimplementation

ML/AI論文の体系的な読解・サーベイ・再現実装を支援するClaude Codeプロジェクト。

## ディレクトリ構成

```
papers/            論文（topic/author-year/ ごとに整理）
surveys/           文献サーベイ
implementations/   Python再現実装
docs/templates/    ノート・分析用テンプレート
memory/            セッション横断の記録（読書ログ、発見、未解決質問）
```

## ワークフロー

| コマンド | 説明 |
|---------|------|
| `/read-paper <path>` | 論文を体系的に読解し、構造化ノートを作成 |
| `/survey <topic>` | トピックの文献サーベイを生成 |
| `/trace-citations <path>` | 引用チェーンを調査 |
| `/reimplement <path>` | 論文手法をPythonでTDD再現実装 |
| `/compare-papers <paths...>` | 複数論文の比較分析 |
| `/paper-status` | プロジェクト全体の進捗ダッシュボード |

## 論文の追加方法

```bash
mkdir -p papers/<topic>/<first-author>-<year>
cp /path/to/downloaded.pdf papers/<topic>/<first-author>-<year>/paper.pdf
```

その後 `/read-paper papers/<topic>/<first-author>-<year>/` で読解を開始。

## セットアップ

```bash
# Git LFS（PDF管理用）
brew install git-lfs
git lfs install
```

## 技術スタック

- **Claude Code** — Skills, SubAgents, Memory による研究ワークフロー自動化
- **Python 3.10+** — 再現実装（pytest, type hints, immutable patterns）
- **Git LFS** — 論文PDFのバージョン管理
