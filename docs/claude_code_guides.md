# Claude Code 拡張機能ガイド — 論文読解プロジェクト向け

本ドキュメントは Claude Code の各拡張機能の概要・設定方法・本プロジェクトへの適用方針をまとめたものである。

---

## 1. AGENT.md / CLAUDE.md

### 概要
- プロジェクトルートに配置するマークダウンファイル
- 毎セッション開始時に自動的に読み込まれる
- `CLAUDE.md` から `@AGENT.md` のようにインポート可能
- 推奨サイズ: ~500行以内（コンテキスト効率のため）

### 設定方法
- `CLAUDE.md`: エントリポイント。`@AGENT.md` でインポート指定
- `AGENT.md`: プロジェクト固有の指示を記述

### 本プロジェクトでの適用
- `CLAUDE.md` → `@AGENT.md` のみ（既存）
- `AGENT.md` → 研究ワークフロー指示（~350行）。認識論的スタンス、ファイル規約、ワークフローコマンド一覧等を記述

---

## 2. Skills

### 概要
- YAML frontmatter + markdown で定義するワークフロー
- `/slash-command` でユーザーが呼び出し可能
- `.claude/skills/<skill-name>/SKILL.md` に配置

### 主要設定項目
```yaml
---
name: skill-name
description: 説明文
context: fork          # fork=SubAgentに委譲, 省略=メインコンテキスト
agent: agent-name      # fork時に使用するSubAgent
allowed-tools:         # 使用可能なツール制限
  - Read
  - WebSearch
---
```

### 本プロジェクトでの適用
| Skill | 用途 | context |
|-------|------|---------|
| `/read-paper` | 論文の体系的読解 | メイン（対話的） |
| `/survey` | 文献サーベイ作成 | fork→literature-surveyor |
| `/trace-citations` | 引用チェーン調査 | fork→citation-tracer |
| `/reimplement` | Python再現実装 | メイン（対話的） |
| `/compare-papers` | 複数論文比較分析 | メイン |
| `/paper-status` | 進捗ダッシュボード | メイン |

---

## 3. SubAgents

### 概要
- 独立コンテキストで動作する専門エージェント
- `.claude/agents/<agent-name>.md` に配置
- メインコンテキストを消費せずにタスクを委譲可能

### 主要設定項目（YAML frontmatter）
```yaml
---
name: agent-name
model: opus             # opus / sonnet / haiku
allowed-tools:          # 使用可能ツールの制限
  - Read
  - Grep
memory: true            # 永続メモリの有効化
permissionMode: default # default / plan / bypassPermissions
---
```

### 本プロジェクトでの適用
| Agent | Model | 用途 |
|-------|-------|------|
| paper-reader | opus | 論文深読、認識論的スタンス厳密適用 |
| literature-surveyor | opus | Web検索+既存ノート横断でサーベイ生成 |
| citation-tracer | sonnet | 大量Web検索+短い要約（コスト効率） |
| reimplementer | opus | TDDでPython実装 |

---

## 4. Agent Teams（実験的機能）

### 概要
- 複数の独立セッション + 共有タスクリスト + peer-to-peer メッセージ
- 大規模タスクの並列処理に適する

### 本プロジェクトでの判断
**不使用**。理由:
- 実験的機能であり安定性に懸念
- SubAgent で十分な並列性を確保可能
- トークンコストが高い

---

## 5. MCP (Model Context Protocol)

### 概要
- 外部ツールとの連携プロトコル（HTTP/stdio）
- `claude mcp add` コマンドで追加
- `.claude/settings.local.json` で設定管理

### 設定方法
```bash
claude mcp add <server-name> -- <command> [args...]
```

### 本プロジェクトでの適用
- 現状は追加MCP不要
- 将来的に Semantic Scholar API の MCP サーバー等を検討可能

---

## 6. Hooks

### 概要
- ライフサイクルイベントでシェルコマンドを自動実行
- イベント種類: `SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`
- `.claude/settings.local.json` の `hooks` セクションで設定

### 設定例
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "command": "prettier --write $CLAUDE_FILE_PATH"
      }
    ]
  }
}
```

### 本プロジェクトでの判断
**最小限**。理由:
- 研究プロジェクトでは柔軟性を優先
- グローバル設定（`~/.claude/settings.json`）の Hooks で十分
- 必要に応じて段階的に追加

---

## 参考リンク

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [AGENT.md Specification](https://docs.anthropic.com/en/docs/claude-code/agent-md)
- [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Claude Code Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
