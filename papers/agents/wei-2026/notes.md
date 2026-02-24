# Agentic Reasoning for Large Language Models

**Authors:** Tianxin Wei, Ting-Wei Li, Zhining Liu, Xuying Ning, Ze Yang, Jiaru Zou, Zhichen Zeng, Ruizhong Qiu, Xiao Lin, Dongqi Fu, Zihao Li, Mengting Ai, Duo Zhou, Wenxuan Bao, Yunzhe Li, Gaotang Li, Cheng Qian, Yu Wang, Xiangru Tang, Yin Xiao, Liri Fang, Hui Liu, Xianfeng Tang, Yuji Zhang, Chi Wang, Jiaxuan You, Heng Ji, Hanghang Tong, Jingrui He
**Venue:** arXiv preprint, 2026 (University of Illinois Urbana-Champaign, Meta, Amazon, Google DeepMind, UCSD, Yale)
**PDF:** `paper.pdf`
**Date Read:** 2026-02-24

---

## One-Sentence Summary

LLMベースの Agentic Reasoning を、Foundational（計画・ツール使用・探索）、Self-evolving（フィードバック・記憶・適応）、Collective（マルチエージェント協調）の3層に体系化し、in-context reasoning と post-training reasoning の2つの最適化モードを横断的に分析する包括的サーベイ論文。

## Problem Statement

LLMは数学やコードなどの closed-world ベンチマークでは強力な推論能力を示すが、動的で open-ended な環境では苦戦する。従来の LLM reasoning は静的な入力に対する single-pass の推論に留まり、環境との相互作用、記憶の永続化、フィードバックによる適応といった能力を欠いている。本サーベイの著者らは、この限界を克服する統一的なパラダイムとして「Agentic Reasoning」を提唱し、既存研究を体系的に整理する必要性を主張している。

## Core Thesis & Design Philosophy

- **Core thesis:** 推論は静的な internal computation としてスケールするのではなく、structured interaction（計画・行動・フィードバック・協調）を通じてスケールすべきであり、LLMを受動的な sequence predictor から能動的な autonomous reasoning agent へと再定義することが次世代 AI の鍵である。
- **What they reject:** LLM reasoning を model-internal な計算能力の向上（モデルサイズ拡大、プロンプトエンジニアリング、CoT等）としてのみ捉える従来の見方。つまり「scaling test-time computation」だけでは不十分であるという立場。
- **What they bet on:** 「scaling test-time interaction」—すなわち、推論プロセスそのものを環境との動的な相互作用ループとして再設計すること。ツール呼び出し、記憶更新、フィードバック統合、マルチエージェント協調を通じた iterative な推論が、静的推論の限界を超えるという信念。

## Intellectual Lineage

| Source | Original Concept | How This Paper Adapts It |
|--------|-----------------|-------------------------|
| Yao et al. (2023) — ReAct | 推論（Reasoning）と行動（Acting）を交互に実行する synergy。LLM が「思考→行動→観察」のループで外部環境と対話する | Agentic Reasoning の foundational paradigm として位置づけ、planning・tool use・search の全てに通底する基本原理として一般化。POMDP 上の policy factorization $\pi_\theta(z_t, a_t | h_t) = \pi_\theta(z_t | h_t) \cdot \pi_\theta(a_t | h_t, z_t)$ として形式化 |
| Yao et al. (2023) — Tree of Thoughts | 推論を木構造として展開し、BFS/DFS で探索する deliberate problem solving | Agentic Search の中核パラダイムとして採用。MCTS 含むツリー探索手法群を in-context planning の一類型として体系化し、heuristic evaluator $\hat{v}_\phi$ による最適パス探索として定式化 |
| Shinn et al. (2023) — Reflexion | verbal reinforcement learning: エージェントが自己批評を蓄積し次の試行で活用する | Self-evolving Agentic Reasoning の Reflective Feedback の原型として位置づけ。generate-critique-revise ループの一般化として、parametric adaptation・validator-driven feedback と並ぶ3つのフィードバック機構の1つに分類 |
| Wang et al. (2023) — Voyager | Minecraft 上の open-ended embodied agent。スキルライブラリの蓄積・コード生成による自律的な能力拡張 | Self-evolving の具体例として参照。experience memory の典型として、環境フィードバック＋記憶による推論の iterative improvement を実証する事例 |
| Hong et al. (2024) — MetaGPT | ソフトウェア開発ライフサイクルを模したマルチエージェント協調フレームワーク（Product Manager, Architect, Engineer 等の役割分担） | Collective Multi-agent Reasoning における domain-specific role taxonomy の典型例として採用。manually crafted hierarchical pipeline の代表として位置づけ |
| DeepSeek (2025) — DeepSeek-R1 | RL による reasoning model の post-training。長い chain-of-thought を RL で最適化 | Post-training reasoning の代表として参照。GRPO ベースの policy optimization が agentic reasoning の学習にも適用可能であることを示す基盤技術 |
| Schulman et al. (2017) — PPO / Shao et al. (2024) — GRPO | PPO: proximal policy optimization。GRPO: group-relative advantage で value network を不要にした RL 手法 | Post-training reasoning の数学的基盤として、agentic policy の最適化目標 $J(\theta) = \mathbb{E}_\tau[\sum_{t \geq 0} \gamma^t r_t]$ を GRPO で近似する枠組みを提示 |

## Proposed Method

### Overview

本論文は特定の手法を提案するのではなく、Agentic Reasoning という統一パラダイムの下に既存研究を体系化するサーベイである。著者らは以下の3層 × 2モードの分類体系（taxonomy）を構築している。

**3層の環境ダイナミクス:**
1. **Foundational Agentic Reasoning** (Sec. 3): Planning, Tool Use, Search
2. **Self-evolving Agentic Reasoning** (Sec. 4): Feedback, Memory, Evolving Capabilities
3. **Collective Multi-agent Reasoning** (Sec. 5): Role Taxonomy, Collaboration, Multi-agent Evolution

**2つの最適化モード（全層を横断）:**
- **In-context Reasoning**: パラメータ固定のまま、推論時の構造的 orchestration・探索・ワークフロー設計で scaling
- **Post-training Reasoning**: RL や SFT でモデルパラメータに推論戦略を内在化

![Figure 1](paper_artifacts/image_000004_39476f8f45bfec87ea9a8e9b149ebb304c2debfe08983ece934a95349910c8bb.png)

### Key Design Decisions

1. **3層構造による環境ダイナミクスの分類**: Foundational → Self-evolving → Collective という段階的複雑化で整理 — *Rationale:* 単一エージェントの基礎能力から適応、そして協調へと自然に複雑さが増す構造を反映。各層が前の層の能力を前提とする包含関係を明示 — *Alternatives:* 能力タイプ別（planning / memory / tool use 等）のフラットな分類、あるいはアプリケーションドメイン別の分類。著者らは環境のダイナミクスに着目した階層構造が、静的推論から動的推論への移行を最もよく捉えると主張

2. **In-context vs Post-training の直交軸**: 3層全てにおいて、推論時の orchestration と学習時のパラメータ最適化を区別 — *Rationale:* 同じ能力（例: tool use）でも、プロンプト設計による inference-time アプローチと RL/SFT による training-time アプローチでは設計空間が根本的に異なる。この区別により、各手法の実用上のトレードオフ（柔軟性 vs 耐久性）が明確になる — *Alternatives:* 学習パラダイム別（RL vs SFT vs prompting）のみで分類する方法。著者らの2軸分類はより抽象度が高く、手法横断的な比較を可能にする

3. **POMDP ベースの形式化**: Agentic Reasoning を $\langle \mathcal{X}, \mathcal{O}, \mathcal{A}, \mathcal{Z}, \mathcal{M}, T, \Omega, R, \gamma \rangle$ として定式化し、policy を $\pi_\theta(z_t, a_t | h_t) = \pi_\theta(z_t | h_t) \cdot \pi_\theta(a_t | h_t, z_t)$ と分解 — *Rationale:* 「思考 (Z)」と「行動 (A)」の分離を明示的に定式化することで、ReAct 等の think-act パラダイムを統一的に記述。latent reasoning space Z の導入により、CoT や tree search を同一フレームワーク内で扱える — *Alternatives:* MDP（完全観測仮定）、あるいは形式化なしの定性的分類。POMDP は partial observability を自然に扱えるため、real-world agentic setting に適切

4. **Applications と Benchmarks の体系的整理**: 5つの応用ドメイン（Math/Code, Science, Robotics, Healthcare, Web）と、能力別・応用別のベンチマーク群を包括的にカバー — *Rationale:* taxonomy の有用性を具体的なドメインへの適用で実証し、実務者向けの actionable guidance を提供 — *Alternatives:* 手法のみに焦点を絞り応用を省略するアプローチ。著者らはドメイン固有の制約（データモダリティ、環境特性、フィードバックループ）が agentic reasoning の設計に重要な影響を与えると主張

### Technical Details

**形式化（Sec. 2.2）:**

環境を POMDP としてモデル化:
- $\mathcal{X}$: latent environment state space（エージェントからは観測不能）
- $\mathcal{O}$: observation space（ユーザクエリ、API返答等）
- $\mathcal{A}$: external action space（ツール呼び出し、最終回答等）
- $\mathcal{Z}$: reasoning trace space（latent plan、CoT等）
- $\mathcal{M}$: internal memory/context space

Policy の分解: $\pi_\theta(z_t, a_t | h_t) = \pi_\theta(z_t | h_t) \cdot \pi_\theta(a_t | h_t, z_t)$

In-context reasoning は $\theta$ を固定し、heuristic value function $\hat{v}(\cdot)$ を用いた trajectory 探索として定式化。Post-training は GRPO 等で $J(\theta) = \mathbb{E}_\tau[\sum_{t \geq 0} \gamma^t r_t]$ を最適化。

**Foundational Agentic Reasoning の分類（Sec. 3）:**

![Figure 2: Planning Reasoning](paper_artifacts/image_000006_3a7de123080353c9a766cf654e75b6d6265d1015c389dc727136c4732bb6b869.png)

- **Planning**: Workflow Design, Tree Search (BFS/DFS/MCTS/A*/Beam), Process Formalization (Code-like/PDDL), Decomposition, Tool Use (RAG/KG/World Model), Reward Design
- **Tool Use**: In-context integration (interleaved reasoning + tool call), Post-training integration (SFT bootstrapping → RL mastery), Orchestration-based integration
- **Agentic Search**: In-context search (interleaved reasoning + retrieval), Post-training search (SFT/RL based), Structure-enhanced search (KG traversal等)

**Self-evolving Agentic Reasoning の分類（Sec. 4）:**

- **Feedback**: Reflective (inference-time self-critique), Parametric Adaptation (training-time), Validator-Driven (binary success/failure signal)
- **Memory**: Flat memory (factual/experience), Structured memory (graph/multimodal), Post-training memory control (RL-based)
- **Evolving Capabilities**: Self-evolving planning (task self-generation), Self-evolving tool-use (tool creation/synthesis), Self-evolving search (co-evolutionary memory-search loop)

**Collective Multi-agent Reasoning の分類（Sec. 5）:**

- **Role Taxonomy**: Generic roles (Leader, Worker, Critic, Memory Keeper, Communication Facilitator) + Domain-specific roles (SE, Finance, Legal, Education, Healthcare, Biomedicine, Music)
- **Collaboration**: In-context (manually crafted / LLM-driven pipelines / agent routing / ToM-augmented) vs Post-training (prompt optimization / graph-based topology / policy-based topology)
- **Multi-agent Evolution**: Intra-test-time vs inter-test-time evolution, multi-agent memory management (architecture/topology/content/management), training multi-agent to evolve (co-evolution via RL, MARL, preference alignment)

## Key Claims

1. Agentic Reasoning は LLM reasoning の自然な拡張であり、「scaling test-time computation」から「scaling test-time interaction」へのパラダイムシフトを表す — Evidence: Table 1 での5次元比較（Paradigm, Computation, Statefulness, Learning, Goal Orientation）
2. 3層（Foundational / Self-evolving / Collective）× 2モード（In-context / Post-training）の taxonomy が、既存の agentic reasoning 研究を包括的かつ体系的に整理できる — Evidence: 800以上の参考文献のカバレッジ、各カテゴリに対応する代表的手法の網羅的な表（Tables 2-9）
3. Post-training reasoning（特に RL ベース）が in-context reasoning を補完し、tool use や search の mastery に不可欠である — Evidence: ToolRL, Search-R1, SWE-RL 等の事例報告（ただしサーベイ論文のため独自実験なし）
4. Self-evolving 能力（feedback + memory）が foundational capabilities を持続的に改善するための鍵である — Evidence: Reflexion, Memory-R1, Dynamic Cheatsheet 等の既存研究の分析
5. Multi-agent collaboration は single-agent の限界を超えるが、credit assignment・topology optimization・governance に未解決の課題が多い — Evidence: 各ドメインでの MAS 適用事例と Open Problems (Sec. 8) での分析

## Methodology Assessment

- **Datasets:** サーベイ論文のため独自のデータセット・実験は含まない。既存ベンチマーク（WebArena, ALFWorld, SWE-bench, AgentBench 等）の包括的レビューを Sec. 7 で提供
- **Baselines:** 比較実験は実施されていない。taxonomy の妥当性は既存研究のカバレッジと分類の一貫性により間接的に主張
- **Metrics:** 該当なし（サーベイ論文）
- **Statistical rigor:** 独自実験を含まないため該当なし。各カテゴリの代表手法は網羅的にリストされているが、定量的な比較分析（例: 各カテゴリの性能比較メタ分析）は行われていない
- **Reproducibility:** GitHub リポジトリ (https://github.com/weitianxin/Awesome-Agentic-Reasoning) が提供されており、参考文献リストとしての再現性は高い

## Results Summary

サーベイ論文のため定量的結果はないが、以下の構造的知見が提示されている:

- 800以上の論文を体系的に分類し、3層 × 2モードの taxonomy に整理
- 5つの応用ドメイン（Math/Code, Science, Robotics, Healthcare, Web）にわたる agentic reasoning の実態を分析
- 能力別（Tool Use, Search, Memory/Planning, Multi-Agent）と応用別（Embodied, Science, Research, Medical, Web, Tool-Use）のベンチマークを網羅的にレビュー
- 6つの Open Problems（Personalization, Long-horizon, World Models, Multi-agent Training, Latent Reasoning, Governance）を特定

## Limitations & Open Questions

- **サーベイ固有の限界:** 独自実験による taxonomy の検証が欠如。分類の妥当性は定性的な議論に依存しており、異なる分類体系との定量的比較は行われていない
- **カバレッジの偏り:** 2025年までの文献を対象としているが、急速に進展する分野のため、出版時点で既に重要な新手法が欠落している可能性がある
- **定量的メタ分析の欠如:** 各カテゴリの手法間の性能比較や、taxonomy の各次元がタスク性能に与える影響の定量的分析が含まれていない
- **Latent Agentic Reasoning の扱いの薄さ:** Open Problem として挙げているものの、本文中での既存研究の分析が限定的
- **Governance/Safety の議論が表面的:** Sec. 8.6 で open problem として提起しているが、具体的なフレームワークや既存のアプローチの深い分析は不足
- **Open Question:** In-context reasoning と post-training reasoning の最適な組み合わせ方は？ 両者のトレードオフを定量的に評価するベンチマークは存在しない

## Connections to Other Work

- **Builds on:** Huang & Chang (2022) の LLM reasoning サーベイ、Wang et al. (2024) の LLM-based autonomous agents サーベイ、Zhang et al. (2025) の agentic RL サーベイ、Fang et al. (2025) の self-evolving agents サーベイ。これらの個別視点を「reasoning」を中心概念として統合
- **Compared with:** Ke et al. (2025) の LLM reasoning frontiers サーベイ（inference scaling + learning to reason + agentic systems）。本論文はより agent-centric で、environment dynamics に基づく3層構造と in-context/post-training の直交軸が差別化ポイント
- **Enables:** Agentic Reasoning の統一的理解に基づく次世代システム設計。特に latent agentic reasoning、user-centric personalization、long-horizon credit assignment、world model integration の研究方向を示唆

## Personal Notes

- 800以上の参考文献を持つ非常に包括的なサーベイであり、agentic AI の現状を把握するための「地図」として極めて有用。ただし、包括性と引き換えに個々の手法の深い分析は犠牲になっている
- POMDP ベースの形式化は理論的にはエレガントだが、実際のシステム設計にどこまで actionable な指針を与えるかは不明確。多くの実システムはこの形式化を意識せずに構築されている
- In-context vs Post-training の二分法は有用だが、実際には両者のハイブリッド（例: post-training で基礎能力を獲得し、in-context で task-specific に適応）が主流であり、この点の議論がもう少し深いと良かった
- Multi-agent memory の4次元分類（Architecture / Topology / Content / Management）は新規性が高く、実システム設計に直接活用できそうな貢献
- Open Problems の中で「Latent Agentic Reasoning」と「Governance」は今後最も重要になる可能性が高いが、現時点では具体的な方向性が不明確
