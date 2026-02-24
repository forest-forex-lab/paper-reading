# Deep Research Systems — 詳細比較表

**Date:** 2026-02-23

---

## 1. 商用システム比較

| 項目 | OpenAI Deep Research | Gemini Deep Research | Perplexity Deep Research | Claude Research |
|------|---------------------|---------------------|-------------------------|----------------|
| **リリース日** | 2025-02 | 2025 | 2025-02 | 2025 |
| **ベースモデル** | o3 (dense transformer) | Gemini 2.5 Pro (sparse MoE) | 非公開 | Opus 4 + Sonnet 4 |
| **アーキテクチャ** | RL-trained reasoning model | 非同期タスク管理 + Search | 反復的検索ループ | Multi-Agent Orchestrator-Worker |
| **Planning** | RL による動的計画 | 反復的計画 + Gap識別 | クエリ調整型 | Lead Agent 戦略策定 |
| **Retrieval** | Web ブラウジング + Data分析 | Google Search + URL context | 反復的検索 + Pivot | 並列 Subagent 探索 |
| **Reasoning** | 内部 Chain-of-Thought | マルチモーダル統合推論 | 検索結果ベース推論 | トークン量ベーススケーリング |
| **入力** | テキスト + ファイル | テキスト + 画像 + PDF + 音声 + 動画 | テキスト | テキスト + ファイル |
| **DeepResearch Bench** | 46.98 | 48.88 (1位) | - | - |
| **特徴的な強み** | Instruction-Following (49.27) | 総合性能リーダー | 速度 + 引用の明確さ | Multi-Agent で 90.2% 向上 |
| **コスト** | ChatGPT Pro ($200/月) | Gemini Advanced | Perplexity Pro | Claude Pro |
| **コード公開** | No | No | No | No |

---

## 2. RL ベース学術研究システム比較

| 項目 | DeepResearcher | ASearcher | DeepDive | O-Researcher | Step-DeepResearch |
|------|---------------|-----------|---------|-------------|-------------------|
| **arXiv ID** | 2504.03160 | 2508.07976 | 2509.10446 | 2601.03743 | 2512.20491 |
| **公開日** | 2025-04 | 2025-08 | 2025-09 | 2026-01 | 2025-12 |
| **ベースモデル** | Qwen2.5-7B/32B 等 | QwQ-32B | 32B | Multiple scales | 32B |
| **RL 手法** | End-to-end RL (Real Web) | 大規模非同期 RL | Multi-Turn RL | Agentic RL | RL (Progressive) |
| **訓練環境** | 実世界 Web | 実世界 Web | Knowledge Graph + Web | Multi-Agent Distillation | Atomic Capability 合成 |
| **主要な革新** | 初の Real-Web RL | 100+ ターン Long-Horizon | KG ベース訓練データ合成 | Multi-Agent Distillation | Progressive Training Path |
| **創発的行動** | 計画、クロスバリデーション、自己反省 | 超長時間探索 | 冗長性ペナルティ | - | Atomic Capability |
| **主要ベンチマーク** | Prompt ENG +28.9pt, RAG RL +7.2pt | xBench 51.1, GAIA 58.7 | BrowseComp OSS SOTA | DR Bench 新SOTA | Scale AI Rubrics 61.4% |
| **最大ターン数** | ~数十 | 100+ | ~数十 | - | - |
| **最大出力トークン** | - | 400k+ | - | - | - |
| **コード公開** | [GitHub](https://github.com/GAIR-NLP/DeepResearcher) | arXiv | [GitHub](https://github.com/THUDM/DeepDive) | arXiv | arXiv |

---

## 3. 特殊アプローチ比較

| 項目 | TTD-DR | DRE (Reflect Evolve) | WebWatcher | Search-o1 | AI Scientist v2 |
|------|--------|---------------------|-----------|-----------|----------------|
| **arXiv ID** | 2507.16075 | 2601.20843 | 2508.05748 | 2501.05366 | 2504.08066 |
| **公開日** | 2025-07 | 2026-01 | 2025-08 | 2025-01 | 2025-04 |
| **組織** | Google | 個人研究者 | Alibaba | RUC-NLPIR | Sakana AI |
| **主要手法** | Test-Time Diffusion | Sequential Reflection + Crossover | Multi-modal Agent + RL | Agentic RAG + Reason-in-Documents | Agentic Tree Search |
| **Diffusion** | Denoising + Retrieval | - | - | - | - |
| **Self-Evolution** | コンポーネント単位最適化 | - | - | - | VLM Feedback Loop |
| **マルチモーダル** | - | - | テキスト + 画像検索 | - | テキスト + 図表生成 |
| **適用ドメイン** | 汎用 Deep Research | 汎用 Deep Research | マルチモーダル情報検索 | Multi-hop QA | 科学研究の自動化 |
| **DeepResearch Bench** | SOTA (報告値) | 46.21 | - | - | - |
| **特筆すべき成果** | SOTA on multi-hop benchmarks | Claude/Perplexity/Grok 超え | BrowseComp-VL SOTA | EMNLP 2025 採択 | ICLR Workshop ピアレビュー通過 |
| **コード公開** | No | [GitHub](https://github.com/SauravP97/deep-researcher-reflect-evolve) | arXiv | [GitHub](https://github.com/RUC-NLPIR/Search-o1) | [GitHub](https://github.com/SakanaAI/AI-Scientist-v2) |

---

## 4. オープンソースシステム比較

| 項目 | Tongyi DeepResearch | Open Deep Search | node-DeepResearch | STORM/Co-STORM | HF open-deep-research | LangChain open_deep_research |
|------|--------------------|-----------------|--------------------|---------------|----------------------|----------------------------|
| **組織** | Alibaba | Sentient AGI | Jina AI | Stanford OVAL | Hugging Face | LangChain |
| **モデル** | 30.5B MoE (3.3B active) | DeepSeek-R1 等 | Gemini/OpenAI/Local | 任意 LLM | 任意 LLM (smolagents) | 任意 LLM |
| **パラメータ** | 30.5B total, 3.3B active | ユーザー選択 | ユーザー選択 | ユーザー選択 | ユーザー選択 | ユーザー選択 |
| **Context Length** | 128K | モデル依存 | モデル依存 | モデル依存 | モデル依存 | モデル依存 |
| **訓練パイプライン** | Agentic CPT → SFT → RL | なし（推論のみ） | なし（推論のみ） | なし（推論のみ） | なし（推論のみ） | なし（推論のみ） |
| **ライセンス** | Apache 2.0 | MIT | MIT | MIT | Apache 2.0 | MIT |
| **主要ベンチマーク** | HLE 32.9, BrowseComp 43.4 | FRAMES +9.7% over GPT-4o | - | - | - | DR Bench 0.4344 |
| **特徴** | 初の OSS で商用級性能 | OSS推論LLMと組合せ可能 | OpenAI DR の即時再現 | Multi-Perspective QA | smolagents ベース | GPT-5 対応, DR Bench #6 |

---

## 5. 評価ベンチマーク比較

| ベンチマーク | 公開日 | 問題数 | 分野数 | 評価観点 | 特徴 |
|------------|--------|--------|--------|---------|------|
| DeepResearch Bench | 2025-06 | 100 (50中+50英) | 22 | RACE (レポート品質) + FACT (事実性+引用) | PhD レベル、多次元評価 |
| DeepResearch Arena | 2025-09 | 10,000+ | 12 | 汎用研究能力 | 学術セミナーから導出 |
| BrowseComp | - | - | - | 複雑情報検索 | テキストベース |
| BrowseComp-VL | 2025-08 | - | - | マルチモーダル情報検索 | WebWatcher が提案 |
| xBench | - | - | - | エージェント能力汎用 | 多言語対応 |
| GAIA | - | - | - | 汎用 AI アシスタント能力 | 多段階タスク |
| FRAMES | - | - | - | Factuality + Reasoning | RAG 評価向け |
| SimpleQA | - | - | - | 単純事実QA | ベースライン評価 |
| Scale AI Research Rubrics | - | - | - | 専門家作成基準 | レポート品質の詳細評価 |
| ADR-Bench | - | - | - | Advanced Deep Research | Step-DeepResearch で使用 |
| HLE (Humanity's Last Exam) | - | - | - | 最高難度学術推論 | 人類最後の試験 |
| Wiki Live Challenge | 2026-02 | - | - | 知識の新鮮さ | 動的更新への対応 |

---

## 6. 技術コンポーネント対応表

各システムが採用するコア技術コンポーネントの有無:

| システム | Dynamic Planning | Iterative Retrieval | Multi-hop Reasoning | RL Training | Diffusion | Multi-Agent | Self-Reflection | Multimodal |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| OpenAI DR | o | o | o | o | - | - | o | - |
| Gemini DR | o | o | o | - | - | - | o | o |
| Perplexity DR | - | o | o | - | - | - | - | - |
| Claude Research | o | o | o | - | - | o | - | - |
| TTD-DR | o | o | o | - | o | - | o | - |
| DeepResearcher | o | o | o | o | - | - | o | - |
| ASearcher | o | o | o | o | - | - | o | - |
| DeepDive | o | o | o | o | - | - | - | - |
| O-Researcher | o | o | o | o | - | o | - | - |
| Step-DeepResearch | o | o | o | o | - | - | - | - |
| DRE | o | o | o | - | - | - | o | - |
| WebWatcher | o | o | o | o | - | - | - | o |
| Search-o1 | - | o | o | - | - | - | - | - |
| Tongyi DR | o | o | o | o | - | - | o | - |
| Open Deep Search | o | o | o | - | - | - | - | - |
| STORM/Co-STORM | o | o | - | - | - | o | - | - |
| AI Scientist v2 | o | - | o | - | - | o | o | o |

凡例: o = 対応, - = 非対応/不明
