# Key Findings

<!-- Format: - YYYY-MM-DD | Finding summary | Related: papers/<topic>/<author-year>/ -->

- 2026-02-23 | Mixed pool training（多様な co-player）が Sequence Model の in-context best-response を誘導し、明示的な meta-learning なしに IPD で協調が出現。In-context learning が "naive learner" の機能的代替として働く | Related: papers/multi-agent-cooperation/weis-2026/
- 2026-02-23 | 同一エージェントがエピソード内（in-context = fast timescale）と エピソード間（in-weight = slow timescale）で異なる役割を自然に担う二重性。Foundation Model エージェントの multi-agent 展開に重要な含意 | Related: papers/multi-agent-cooperation/weis-2026/
- 2026-02-23 | Deep Research 分野は2025年に急速に成熟。80以上の商用/OSS実装が登場（Xu & Peng 2025 サーベイ）| Related: surveys/deep-research/
- 2026-02-23 | TTD-DR (Google, 2025-07) がレポート生成を Diffusion プロセスとして定式化。Denoising + Retrieval による反復的改善で SOTA 達成と報告 | Related: surveys/deep-research/
- 2026-02-23 | RL による Deep Research エージェントの end-to-end 訓練が主要トレンド。DeepResearcher → ASearcher → DeepDive → O-Researcher と急速に発展 | Related: surveys/deep-research/
- 2026-02-23 | Multi-Agent 構成の Claude Research が単一エージェント比 90.2% 性能向上。性能差の80%はトークン使用量で説明可能（Anthropic 報告）| Related: surveys/deep-research/
- 2026-02-23 | Tomašev et al. が AI delegation の包括的フレームワークを提案。Contract-first decomposition（Verifiability を分解の停止条件とする）と Privilege Attenuation（委任チェーンで権限が単調減少）が設計上の核心原理 | Related: papers/agents/tomasev-2026/
- 2026-02-23 | 組織論の概念（Principal-Agent Problem, Span of Control, Authority Gradient, Zone of Indifference）が AI multi-agent delegation の設計に直接応用可能。特に Authority Gradient（能力格差がコミュニケーションを阻害）は LLM の sycophancy 問題との接続が示唆的 | Related: papers/agents/tomasev-2026/
- 2026-02-23 | 既存 agentic プロトコル（MCP, A2A, AP2, UCP）はいずれも intelligent delegation の要件を部分的にしか満たさない。特に MCP は semantic attenuation（権限の細粒度制御）を欠き、A2A は cryptographic verification を欠く | Related: papers/agents/tomasev-2026/
- 2026-02-23 | Tongyi DeepResearch (Alibaba, 30.5B MoE) が OSS で商用級性能を達成。「Deep Research 版 DeepSeek moment」と評される | Related: surveys/deep-research/
- 2026-02-23 | DeepResearcher の RL 訓練で創発的認知行動（計画立案、クロスバリデーション、自己反省、正直な不確実性の表明）が獲得された | Related: surveys/deep-research/
- 2026-02-23 | ASearcher が100ターン以上・400kトークンの Long-Horizon 探索を実現。非同期 RL による大規模訓練が鍵 | Related: surveys/deep-research/
