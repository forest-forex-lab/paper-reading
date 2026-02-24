# Intelligent AI Delegation

**Authors:** Nenad Tomašev, Matija Franklin, Simon Osindero
**Venue:** Google DeepMind Technical Report, 2026
**PDF:** `paper.pdf`
**Date Read:** 2026-02-23

---

## One-Sentence Summary

既存のヒューリスティックベースな AI タスク委任手法の限界を指摘し、動的評価・適応的実行・構造的透明性・スケーラブルな市場メカニズム・システム的回復力の5つの柱に基づく **intelligent delegation** フレームワークを提案する position paper。

## Problem Statement

AI エージェントが複雑なタスクを分解・委任する能力が求められる中、既存の multi-agent delegation 手法は静的なヒューリスティックに依存しており、動的環境への適応、障害からの回復、説明責任の確保が不十分である。特に、agentic web のスケールでは、責任の所在・信頼の構築・安全な権限委譲のための体系的フレームワークが欠如している。

## Core Thesis & Design Philosophy

- **Core thesis:** AI delegation は単なるタスク分解ではなく、権限・責任・信頼の移転を伴う意思決定プロセスであり、人間組織で発達した delegation の原理が AI にも適用可能である
- **What they reject:** 既存の multi-agent フレームワークの「タスク分解 = サブタスクの静的割当」という暗黙の前提。ヒューリスティックなルーティングや固定的なオーケストレーションで十分とする考え方
- **What they bet on:** 人間組織論（Principal-Agent Theory, Span of Control, Authority Gradient, Contingency Theory）の概念が、動的かつ安全な AI delegation の設計原理として機能する。特に、**検証可能性（Verifiability）を設計の中心制約**に据えることで、安全性とスケーラビリティを同時に確保できるという信念

## Intellectual Lineage

| Source | Original Concept | How This Paper Adapts It |
|--------|-----------------|-------------------------|
| Cvitanić et al. (2018) / Grossman & Hart (1992) — Principal-Agent Theory | エージェントが本人と異なる動機を持つ場合の委任リスクと契約設計 | AI delegation における reward misspecification / specification gaming を Principal-Agent 問題の変形として位置づけ。AI 特有の問題（deceptive alignment, sycophancy）を加味して拡張 |
| Ouchi & Dowling (1974) — Span of Control | 一人のマネージャーが効果的に管理できる部下の数の上限 | AI orchestrator が並列管理できる sub-agent 数、および人間 overseer が監督できる AI エージェント数の設計指針として転用。認知負荷とエラー率のトレードオフを AI 文脈に再定式化 |
| Alkov et al. (1992) — Authority Gradient (航空分野) | 能力・経験・権威の格差がコミュニケーションを阻害し、エラーを誘発 | LLM の sycophancy（権威への追従）を Authority Gradient の AI 版として捉え直す。Delegatee が delegator の誤った指示に挑戦できないリスクとして再解釈 |
| Finkelman (1993) / Isomura (2021) — Zone of Indifference | 権威が受容されると、一定範囲の指示が批判的検討なく実行される | AI の safety filter を「静的な Zone of Indifference」と見なし、**dynamic cognitive friction** の必要性を導出。文脈に応じて zone の境界を動的に調整する設計原理 |
| Williamson (1979) — Transaction Cost Economics | 企業の存在理由を内部委任 vs. 外部契約のコスト比較で説明 | AI delegation の4つの選択肢（自力実行 / 既知 sub-agent / 信頼済み外部 agent / 未知 agent）のコスト構造を transaction cost で定式化。**Complexity floor**（委任オーバーヘッド > タスク価値なら直接実行）の導出 |
| Donaldson (2001) — Contingency Theory | 普遍的に最適な組織構造は存在せず、環境条件に応じて動的に適合させるべき | フレームワーク全体の「静的設計の否定」の理論的根拠。Oversight の強度、delegatee の能力要件、人間の関与度をタスク特性に応じて動的に調整する設計思想の基盤 |
| Smith (1980) — Contract Net Protocol | エージェントがタスクを公告し、他のエージェントが入札するオークション型の分散タスク割当 | 基本的な入札メカニズムを継承しつつ、smart contract による形式化、reputation bond、multi-round negotiation、pre-commitment verification で大幅に拡張 |
| Teutsch & Reitwießner (2018) — TrueBit | 計算の正当性を検証する game-theoretic protocol。検証者が Schelling point に収束するインセンティブ設計 | Verifiable Task Completion (§4.8) の game-theoretic consensus メカニズムとして採用。LLM ベースの検証を多数決で robust 化するアイデアに転用 |
| Bainbridge (1983) — Paradox of Automation | 自動化が進むほど、人間が残された例外処理を行う能力が劣化する | De-skilling リスク (§5.6) の理論的基盤。**Curriculum-aware task routing**（人間のスキル維持のために意図的にタスクを割り当てる）という対策を導出 |

## Proposed Method

### Overview

著者らは **intelligent delegation** を「タスク割当に関する一連の決定であり、権限・責任・説明責任の移転、役割と境界の明確な仕様、意図の明確性、および当事者間の信頼構築メカニズムを組み込んだもの」と定義する。

フレームワークは **5つの Pillar** と **9つの Technical Protocol** から構成される:

| Pillar | Protocol |
|--------|----------|
| Dynamic Assessment | Task Decomposition (§4.1), Task Assignment (§4.2) |
| Adaptive Execution | Adaptive Coordination (§4.4) |
| Structural Transparency | Monitoring (§4.5), Verifiable Task Completion (§4.8) |
| Scalable Market | Multi-objective Optimization (§4.3), Trust & Reputation (§4.6) |
| Systemic Resilience | Permission Handling (§4.7), Security (§4.9) |

### Key Design Decisions

1. **Verifiability を分解の停止条件とする (Contract-first decomposition)**: サブタスクの検証可能性が確保されるまで再帰的に分解を継続する — *Rationale:* 検証不能なサブタスクを委任すると、障害検出も品質保証もできず、信頼チェーン全体が破綻する。形式検証の「仕様先行」原理を delegation に転用 — *Alternatives:* (a) 固定粒度での分解（多くの既存フレームワーク）、(b) delegatee の自己申告に依存（信頼前提が必要）、(c) 事後検証のみ（品質保証が遅延）
2. **分散型市場メカニズムを中心に据える**: 集中型レジストリではなく、入札・smart contract・エスクローによる分散型 delegation — *Rationale:* Web-scale では単一の orchestrator がボトルネックかつ単一障害点。市場メカニズムは price signal を通じて delegatee の能力と需要を自然にマッチングする — *Alternatives:* (a) 集中型レジストリ（Option A として言及、スケーラビリティに限界）、(b) 固定的なエージェント階層（柔軟性に欠ける）
3. **Privilege Attenuation（権限の単調減少）**: 委任チェーンの各段階で権限が厳密に縮小される capability-based security — *Rationale:* 末端エージェントの侵害がシステム全体に波及することを構造的に防止。Macaroons/Biscuits の暗号的 caveat チェーンにより技術的に実装可能 — *Alternatives:* (a) 全権限の転送（セキュリティリスク大）、(b) 中央集権的な権限管理サーバー（単一障害点）
4. **Transitive Accountability via Attestation**: 直接監視ではなく、署名付きアテステーションの連鎖で多段階の説明責任を実現 — *Rationale:* 委任チェーン A→B→C で A が C を直接監視するのは技術的にもプライバシー上も非現実的。B の「C を検証する能力」を A が検証する間接的モデルにより、プライバシーとスケーラビリティを両立 — *Alternatives:* (a) 全段階の直接監視（スケールしない）、(b) 信頼前提（セキュリティリスク）
5. **Dynamic Cognitive Friction の導入**: Zone of Indifference を静的にせず、タスクの criticality / uncertainty に応じて認知負荷を動的に調整 — *Rationale:* 人間の overseer は一律に高負荷だと alarm fatigue を起こし、一律に低負荷だと moral crumple zone が生じる。Contingency Theory の「状況適合」原理を oversight に適用 — *Alternatives:* (a) 一律の承認フロー（alarm fatigue リスク）、(b) 完全自動化（人間の meaningful control 喪失）

### Technical Details

**タスク属性の分類体系 (§2)**: 各タスクを以下の11属性で特徴づけ、delegation 判断の入力とする:
Complexity, Criticality, Uncertainty, Duration, Cost, Resource Requirements, Constraints, Verifiability, Reversibility, Contextuality, Subjectivity

**Monitoring の5軸分類 (Table 2)**:
- Target: Outcome-Level ↔ Process-Level
- Observability: Indirect ↔ Direct
- Transparency: Black-Box ↔ White-Box
- Privacy: Full Transparency ↔ Cryptographic (zk-SNARKs, MPC)
- Topology: Direct (1-to-1) ↔ Transitive (attestation chain)

**Reputation の3層モデル (Table 3)**:
- Immutable Ledger: ブロックチェーン上の改竄不能な実績記録
- Web of Trust: DID + Verifiable Credentials によるドメイン別ポートフォリオ
- Behavioral Metrics: プロセスの透明性スコア + 安全性スコア

**プロトコル拡張例 (§6.1)**:
- `verification_policy`: A2A Task object に検証基準（unit test log, zk-SNARK trace）を埋め込む
- `bid_object`: RFQ プロトコルで delegatee が signed bid を提出（cost, duration, privacy guarantee, reputation bond）
- DCT (Delegation Capability Tokens): Macaroons/Biscuits ベースの減衰可能トークン。委任チェーンに沿って制限を累積的に追加
- Monitoring stream: MCP 拡張。SSE による4段階粒度（L0_IS_OPERATIONAL → L3_FULL_STATE）

### 重要な図

- ![Figure 1: Task Decomposition & Assignment flowchart](figures/paper.pdf-10-0.png)
- ![Figure 2: Adaptive Coordination Cycle](figures/paper.pdf-12-0.png)

## Key Claims

1. **既存の delegation 手法はヒューリスティック依存で不十分** — Evidence: 先行研究サーベイ（§3）による定性的議論。定量的比較なし
2. **5 Pillar + 9 Protocol が intelligent delegation に必要** — Evidence: 組織論（Principal-Agent Problem, Span of Control, Authority Gradient 等）からの類推。必要十分性の論証なし
3. **Contract-first decomposition が安全な delegation の前提条件** — Evidence: 理論的議論。auto-verifiable domains（コード生成等）への適用は具体的だが、主観的タスクへの一般化は未解決
4. **分散型市場メカニズム（入札・Smart Contract・エスクロー）がスケーラブルな delegation を実現** — Evidence: 個別技術（zk-SNARKs, TrueBit 等）は実在するが統合システムの実現可能性は未検証
5. **既存プロトコル（MCP, A2A, AP2, UCP）は要件を部分的にしか満たさない** — Evidence: 各プロトコル仕様の gap analysis + 具体的 JSON 拡張例（§6）
6. **De-skilling リスクに対して意図的な非効率性の導入が必要** — Evidence: Paradox of Automation（Bainbridge, 1983）、Zone of Proximal Development からの類推
7. **Monitoring の5軸分類（Target, Observability, Transparency, Privacy, Topology）が設計空間を網羅** — Evidence: Table 2 の体系的整理。先行研究に基づく各軸の定義
8. **Trust と Reputation の3層モデル（Ledger, Web of Trust, Behavioral Metrics）がスケーラブルな信頼構築を支える** — Evidence: Table 3 の分類。DID + Verifiable Credentials 等の既存技術を引用

## Methodology Assessment

- **Datasets:** N/A（概念的フレームワーク、実験なし）
- **Baselines:** N/A（既存手法との定量比較なし）
- **Metrics:** N/A
- **Statistical rigor:** N/A
- **Reproducibility:** フレームワーク自体は再現不要だが、§6 のプロトコル拡張例（JSON スキーマ）は具体的で再現可能な出発点を提供

## Results Summary

実験的結果は含まれない。主な成果物は:
- 9コンポーネントからなる conceptual framework（Table 1）
- Monitoring の5軸分類（Table 2）
- Reputation 実装の3アプローチ（Table 3）
- 既存プロトコル（MCP, A2A, AP2, UCP）の gap analysis
- 具体的なプロトコル拡張例（verification_policy, bid_object, DCT, monitoring stream）

## Limitations & Open Questions

- **実装・評価の完全な欠如**: 9コンポーネントのいずれもプロトタイプ実装・シミュレーション・ユーザー実験で検証されていない
- **統合コストの未分析**: zk-SNARKs + Smart Contract + TEE + DID の組合せによる計算オーバーヘッド・レイテンシの定量的評価がない
- **循環的依存**: Trust → Monitoring → Trust の循環構造。新規エージェントの cold start problem への対応が不十分
- **主観的タスクへの適用限界**: contract-first decomposition は高 Verifiability タスクには有効だが、創造的・主観的タスクでの収束性が保証されない
- **経済的インセンティブの不整合**: De-skilling 対策としての「意図的非効率性」は競争的市場と矛盾。規制的枠組みの議論が不足
- **人間-AI 類推の限界**: 組織論の概念（Span of Control 等）をAIに適用する際の disanalogy（AI の hallucination、動機構造の欠如等）が十分に議論されていない

## Connections to Other Work

- **Builds on:** Principal-Agent Theory (Cvitanić et al., 2018), Contract Net Protocol (Smith, 1980), FeUdal Networks (Vezhnevets et al., 2017b), Scalable Oversight (Bowman et al., 2022), TrueBit (Teutsch & Reitwießner, 2018)
- **Compared with:** MCP (Anthropic, 2024), A2A (Google, 2025b), AP2 (Parikh & Surapaneni, 2025), UCP (Handa & Google Developers, 2026)
- **Enables:** Delegation-aware protocol extensions, agentic market infrastructure, curriculum-aware task routing for human skill preservation
- **Related (in this project):** Weis et al. (2026) の multi-agent cooperation — in-context co-player inference は本論文の Trust Calibration の実装候補となりうる

## Personal Notes

- 本論文の最大の価値は、散在する概念（信頼、権限、監視、検証）を delegation という統一的視座から体系化した点にある。個々のアイデアは新規ではないが、統合的なフレームワークとしての整理は有用
- Section 6 のプロトコル拡張提案（特に DCT と monitoring stream の段階的粒度）は、現在の MCP/A2A エコシステムの実装者にとって具体的な参考になる
- 「Cognitive Monoculture」（少数の foundation model への過度な依存）のリスク指摘は、現在の AI エコシステムの構造的脆弱性を的確に捉えている
- De-skilling と Paradox of Automation の議論（§5.6）は、AI エージェントの社会実装における最も重要な倫理的課題の一つを提起している
- 全体として、「実装論文」ではなく「設計思想の提示」として読むべき。今後の実装研究のための conceptual map として位置づけるのが適切
