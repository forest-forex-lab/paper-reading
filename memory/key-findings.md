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
- 2026-02-24 | DeepResearchEval がペルソナ駆動のタスク自動生成と適応型品質評価（固定次元+タスク固有次元）を提案。全9システムでタスク固有次元のスコアが固定次元より一貫して低く、現在の Deep Research システムがタスク固有の成功基準を満たすことに課題があることを示唆 | Related: papers/agents/wang-2026/
- 2026-02-24 | Deep Research システムの事実リスクは「でっち上げ」(Wrong) よりも「裏付け不十分な主張」(Unknown) に起因する傾向が強い。能動的事実検証 (Active Fact-Checking) により Web 検索でクレームを検証するアプローチを提案 | Related: papers/agents/wang-2026/
- 2026-02-24 | 品質と事実性は必ずしも相関しない：Gemini-2.5-Pro Deep Research が品質トップ (8.51/10)、Manus が事実正確性トップ (82.30% Ratio)。品質評価での自己選好バイアス（Gemini が judge かつ被評価者）の可能性あり | Related: papers/agents/wang-2026/
- 2026-02-23 | ASearcher が100ターン以上・400kトークンの Long-Horizon 探索を実現。非同期 RL による大規模訓練が鍵 | Related: surveys/deep-research/
- 2026-02-24 | Wei et al. が Agentic Reasoning を「scaling test-time computation」から「scaling test-time interaction」への移行として定義。POMDP ベースの形式化で思考空間 Z と行動空間 A を分離し、800+の既存研究を 3層（Foundational / Self-evolving / Collective）× 2モード（In-context / Post-training）で体系化 | Related: papers/agents/wei-2026/
- 2026-02-24 | Multi-agent memory の4次元設計フレームワーク（Architecture / Topology / Content / Management）が actionable な貢献。6つの Open Problems（Personalization, Long-horizon, World Models, Multi-agent Training, Latent Reasoning, Governance）を特定 | Related: papers/agents/wei-2026/
- 2026-02-24 | Post-training（RL/SFT）による tool use と search の mastery が in-context approach を補完するという主張。DeepSeek-R1 の RL 成功をエージェント全般に拡張する方向性を示唆するが、実験的裏付けはサーベイ論文のため不在 | Related: papers/agents/wei-2026/
- 2026-02-24 | SycEval が sycophancy を progressive（正答方向）/ regressive（誤答方向）に二分類。全サンプルの58.19%で sycophantic behavior を観察。Citation-based rebuttal が regressive sycophancy を最大化し、偽の権威的情報源による authority bias の存在を示唆 | Related: papers/evaluation/fanous-2025/
- 2026-02-24 | Sycophancy の persistence rate は78.5%と高く、follow-up で矛盾を指摘されても回答を維持。Tomašev et al. の Authority Gradient の議論（LLM の sycophancy がコミュニケーションを阻害）と直接接続する実証データ | Related: papers/evaluation/fanous-2025/, papers/agents/tomasev-2026/
- 2026-02-24 | A-RAG の Naive 構成（単一 embedding tool のみ）が Graph RAG・Workflow RAG を上回り、agentic paradigm 自体の有効性を示唆。ただし GPT-5-mini での結果に限定 | Related: papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | 階層的 retrieval interface（snippet-based progressive disclosure）により、A-RAG (Full) は Naive 比で retrieved token を約90%削減しつつ精度向上（HotpotQA: 2,737 vs 27,455 tokens）。Token 効率と精度のトレードオフ改善の有望なアプローチ | Related: papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | Test-time compute scaling が RAG でも確認：max steps 増加で約8%、reasoning effort 増加で約25%の精度向上。ただし MuSiQue-300 サブセットのみでの検証 | Related: papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | Deep-thinking ratio (DTR) は Transformer の layer-wise 予測分布収束深度で推論努力を測定する新指標。32 設定で平均 Pearson r=0.683 を達成し、トークン長（r=-0.594）や Self-Certainty（r=0.605）を上回ると報告。ただし一部設定で負相関を示し普遍性に疑問 | Related: papers/evaluation/chen-2026/
- 2026-02-24 | Think@n は DTR ベースの test-time scaling 戦略で、50 トークンの prefix から DTR を推定し low-effort サンプルを early reject。Self-Consistency (Cons@n) 同等以上の精度を約半分の推論コストで達成と主張。LLM 内部状態アクセスが必要という実用制約あり | Related: papers/evaluation/chen-2026/
- 2026-02-24 | 推論努力の「長さ vs 深さ」問題：出力長と精度が負相関する反直覚的パターンを DTR で説明。Wei et al. の test-time compute scaling と接続する evaluation 視点 | Related: papers/evaluation/chen-2026/, papers/agents/wei-2026/
