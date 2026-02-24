# Multi-agent cooperation through in-context co-player inference

**Authors:** Marissa A. Weis*, Maciej Wołczyk*, Rajai Nasser, Rif A. Saurous, Blaise Agüera y Arcas, João Sacramento, Alexander Meulemans
**Venue:** Google, Paradigms of Intelligence Team / Santa Fe Institute, 2026 (preprint)
**PDF:** `paper.pdf`
**Date Read:** 2026-02-23

---

## One-Sentence Summary

Sequence Model エージェントを多様な co-player の混合プールで訓練するだけで、明示的な meta-learning 機構やタイムスケール分離なしに、Iterated Prisoner's Dilemma で in-context best-response が自然に誘導され、extortion → mutual extortion → 協調の段階的メカニズムを通じて頑健な協調行動が出現する。

## Problem Statement

Decentralized MARL において自己利益的なエージェント間で協調を達成すること。従来の co-player learning-aware 手法は (1) 相手の学習規則に関するハードコードされた仮定、(2) naive learner / meta-learner の明示的なタイムスケール分離、という制約があった。著者らはこれらの複雑な機構が不要であり、Sequence Model の in-context learning 能力と co-player の多様性だけで十分であると主張する。

## Core Thesis & Design Philosophy

- **Core thesis:** 多様な co-player の混合プールで訓練するだけで、Sequence Model の in-context learning 能力が自然に「相手推論 → 適応 → 協調」を誘導する。明示的な meta-learning 機構やタイムスケール分離は不要である
- **What they reject:** 従来の learning-aware 手法（LOLA, M-FOS, COLA）が前提とする「相手の学習規則に関するハードコードされた仮定」と「naive learner / meta-learner の明示的タイムスケール分離」。これらは人工的な構造であり、汎用的な Foundation Model には不要だとする立場
- **What they bet on:** (1) Sequence Model の in-context learning が、環境からの暗黙的な co-player 推論を自然に実現する。(2) Co-player の**多様性**（mixed pool）が、この推論能力を誘導する十分条件となる。(3) Extortion → Mutual Extortion → Cooperation という段階的ダイナミクスが、設計なしに創発する

## Intellectual Lineage

| Source | Original Concept | How This Paper Adapts It |
|--------|-----------------|-------------------------|
| Meulemans et al. (2025a) — Learning-aware policy gradients | 「多様性 → in-context best-response → extortion 脆弱性 → 相互 extortion → 協調」の3段階メカニズム。明示的な learning-aware 勾配計算を使用 | 3段階メカニズムの概念的枠組みをそのまま採用するが、**明示的勾配計算を in-context learning で代替**できることを実証。メカニズムの普遍性を主張する根拠として使用 |
| Meulemans et al. (2025b) — MUPI framework / Subjective Embedded Equilibrium (SEE) | Model-based policy improvement の一般的フレームワーク。Bayesian world model + policy improvement operator による均衡概念 | PPI アルゴリズムの理論的基盤。Sequence Model の next-token prediction を world model として、Monte Carlo rollout + softmax policy improvement を operator として、MUPI の具体的インスタンス化。Theorem D.9 で PPI → SEE の対応を証明 |
| Press & Dyson (2012) — Extortion strategies in IPD | Memory-1 戦略の線形不等式構造により、一方のプレイヤーが相手の報酬を支配（extort）できることの発見 | 協調出現の中間段階（Step 2-3）の説明に使用。In-context learner が extortion のターゲットとなる理由の直観的根拠。ただし形式的な対応は厳密に定義されていない |
| Brown et al. (2020) / 他 — Sequence Model as world model | GPT 型モデルが行動・観測系列の next-token prediction により暗黙的な世界モデルを獲得 | PPI の中核: Sequence Model が同時系列 $(a_t^1, a_t^2, r_t^1, r_t^2)$ を next-token prediction で学習し、MC rollout により $\hat{Q}$ を推定。In-context learning = 暗黙的 Bayesian inference という解釈 |
| Foerster et al. (2018) — LOLA | 相手の学習ステップを微分可能に仮定し、自身の方策勾配に織り込む learning-aware 手法 | **反面教師**として位置づけ。LOLA が必要とする「相手の学習規則の知識」を、mixed pool + in-context learning で不要にすることが本研究の主張の核心 |

## Proposed Method

### 環境と設定
- **Iterated Prisoner's Dilemma (IPD)**: T=100ステップ、2エージェント、行動 {C, D}
- **利得行列**: CC→(1,1), CD→(-1,2), DC→(2,-1), DD→(0,0)

### Mixed Pool Training
- **Learning Agents**: GRU ベース Sequence Model（128次元 hidden state, 32次元 embedding）
- **Tabular Agents**: Memory-1 方策、5パラメータ、U(0,1) からサンプル
- **訓練比率**: 50% vs Learning Agent, 50% vs Tabular Agent
- エージェント識別子は付与されない → 履歴からの推論が必須

### 2つの学習アルゴリズム
1. **Independent A2C**: 標準的な Model-Free RL（ベースライン）
2. **Predictive Policy Improvement (PPI)** — 本研究の新手法:
   - Sequence Model が行動・観測・報酬の同時系列を Next-Token Prediction で学習（式2）
   - Policy Improvement: π(a|x≤t) ∝ p_φ(a|x≤t) · exp(β Q̂(x≤t, a))（式1）
   - Q̂ は Sequence Model 内の 15ステップ Monte Carlo Rollout で推定
   - 30フェーズの反復訓練（各フェーズでパラメータ再初期化 + 全蓄積データで再訓練）
   - 事前訓練: ランダム Tabular Agent 間の 200,000 軌道

### Key Design Decisions

1. **Mixed Pool Training（50% Learning Agent, 50% Tabular Agent）**: 学習エージェントを多様な固定方策の Tabular Agent と混合して訓練する — *Rationale:* 同種エージェント同士のみの Self-Play では co-player の多様性が不足し、in-context adaptation が誘導されない。Tabular Agent プールが「多様な相手」を安価に提供する — *Alternatives:* (a) Pure Self-Play（ablation で裏切りに収束と確認）、(b) Population-based training（より計算コストが高い）、(c) 明示的な opponent modeling モジュールの追加（本研究が「不要」と主張する立場）
2. **エージェント識別子を付与しない**: 各エピソードで co-player が誰かの情報を与えず、行動履歴からの推論を強制する — *Rationale:* 識別子があると相手ごとに固定方策を暗記できるため、in-context 推論が不要になる。ablation (Explicit ID) で裏切りに収束することを確認 — *Alternatives:* (a) エージェント ID の提供（ablation で失敗を確認）、(b) 相手のタイプ情報の部分的提供
3. **PPI: Next-Token Prediction + MC Rollout による Policy Improvement**: Sequence Model が $(a_t^1, a_t^2, r_t^1, r_t^2)$ の同時系列を学習し、15ステップ MC Rollout で $\hat{Q}$ を推定、softmax policy improvement を適用 — *Rationale:* World model の明示的な学習を避け、next-token prediction の自然な帰結として世界モデルを獲得。MC Rollout は model-based planning の最もシンプルな形 — *Alternatives:* (a) 明示的な world model + planning（より複雑）、(b) Model-Free RL のみ（A2C として比較、Step 3 で不安定）
4. **30フェーズの反復訓練（各フェーズでパラメータ再初期化）**: データを蓄積しつつ、各フェーズで Sequence Model を再初期化して全データで再訓練 — *Rationale:* Self-Supervised 学習の安定性を確保。累積的なデータ蓄積により co-player 分布の変化を自然に反映 — *Alternatives:* (a) オンライン学習（分布シフトに脆弱）、(b) Replay buffer + 継続学習（catastrophic forgetting リスク）
5. **Memory-1 Tabular Agent のみを co-player プールに使用**: 5パラメータの最小メモリ方策 — *Rationale:* 最小限の設定で十分な多様性が得られるかの検証（原理の最小実証）。計算コストも低い — *Alternatives:* (a) より長いメモリの方策、(b) 学習済みエージェントのプール、(c) LLM ベースの co-player

### 協調出現の3段階メカニズム（Meulemans et al. 2025a に基づく）
1. **多様性 → In-context best-response**: Tabular プールの多様性がエピソード内での相手推論・適応能力を誘導
2. **In-context learning → Extortion への脆弱性**: エピソード内の高速適応が、他のエージェントの weight 更新による extortion のターゲットになる
3. **相互 Extortion → 協調**: Extortion 方策を持つエージェント同士が対戦すると、互いの in-context learning を形成し合い協調に収束

![Figure 1 - Mixed training leads to cooperation](figures/paper.pdf-3-7.png)

## Key Claims

1. **Mixed pool training が頑健な協調を誘導する** — Evidence: Figure 1, 10 seeds, 2つの ablation（Explicit ID / No mixed pool → 裏切りに収束）
2. **多様な co-player が in-context best-response を誘導する** — Evidence: Figure 2A-B, Tabular プール訓練後のエピソード内適応
3. **In-context learners は extortion に脆弱である** — Evidence: Figure 2C-D, Fixed-ICL に対する報酬の非対称的獲得
4. **相互 extortion が協調を駆動する** — Evidence: Figure 2E-F, extortion 方策の相互訓練による協調への収束
5. **PPI の訓練均衡は Subjective Embedded Equilibrium に対応する** — Evidence: Theorem D.9（Perfect PE → SEE）、理論的

## Methodology Assessment

- **Datasets:** IPD（2プレイヤー・2行動の最小環境）のみ。他の Social Dilemma は未検証
- **Baselines:** A2C（Model-Free）が唯一の学習アルゴリズム比較。LOLA, M-FOS, COLA 等の先行 learning-aware 手法との直接比較なし
- **Metrics:** Cooperation Rate, Average Reward（適切）
- **Statistical rigor:** 10 random seeds（PPI）/ 5 seeds（A2C の一部）。有意差検定は報告されていない。標準偏差のみ
- **Reproducibility:** ハイパーパラメータは詳細に報告（Table 2, Appendix A）。コード公開の記載なし。JAX/Flax 実装

## Results Summary

- **Figure 1**: PPI/A2C 共に mixed pool で協調に収束（PPI: Phase ~15, A2C: ~100k iteration）。Ablation（Explicit ID, No mixed pool）は裏切りに収束
- **Figure 2**: 3段階メカニズムの段階的検証。PPI で全ステップが成功
- **Figure 3**: 早期訓練時のエピソード内行動 — learning agent 同士ではエピソード前半で extortion を試み後半で協調
- **Figure 4**: A2C でも Step 1-2 は成功するが、**Step 3 で訓練不安定** — シードによっては裏切りに回帰

## Limitations & Open Questions

- **環境の限定性**: IPD のみ。2×2 の最小ゲームでの結果がより複雑な環境（連続行動、N>2 エージェント、部分観測が重い環境）に一般化するかは未検証
- **A2C の不安定性**: Step 3（mutual extortion → cooperation）で A2C は不安定。PPI の安定性が Sequence Model の Self-Supervised 訓練に起因するのか、他の要因によるのかの分析が不十分
- **先行手法との直接比較なし**: LOLA, M-FOS, COLA 等の learning-aware 手法との定量的比較がない（本研究はこれらが「不要」と主張するが、性能や効率の比較は有用）
- **計算コスト未報告**: PPI の MC Rollout は計算的に重いはずだが、壁時間・FLOPs の報告なし
- **Tabular Agent の設計選択**: Memory-1 のみ。より複雑な相手分布の効果は未調査
- **ハイパーパラメータ感度**: β=0.01, 50/50 比率, T=100 等の感度分析なし
- **Extortion の形式的定義**: Press & Dyson (2012) の extortion 戦略との厳密な対応関係が曖昧
- **理論と実験のギャップ**: Perfect PE → SEE の対応は完全な世界モデルを前提とし、有限容量ネットワークでの保証ではない

## Connections to Other Work

- **Builds on:** Meulemans et al. (2025a) — learning-aware policy gradients による協調の3段階メカニズム; Meulemans et al. (2025b) — MUPI フレームワーク、Subjective Embedded Equilibrium; Press & Dyson (2012) — IPD における extortion 戦略
- **Compared with:** LOLA (Foerster et al., 2018), M-FOS (Lu et al., 2022), COLA (Willi et al., 2022) — これらは明示的 learning-awareness を使用（本研究はこれらが不要と主張）
- **Enables:** Foundation Model エージェントの協調行動 — in-context learning は LLM の自然な能力であり、本研究の知見は LLM エージェント間の協調への道筋を示唆; スケーラブルな分散協調システム

## Personal Notes

- **最も説得力のある点**: 3段階メカニズムの段階的分解（Figure 2）が因果関係を明確に示している。各ステップを独立に検証しているのは方法論的に優れている
- **最も弱い点**: IPD のみという環境の限定性。Social Dilemma の他の変種（Stag Hunt では協調が Nash 均衡、Chicken ではゲームの構造が異なる）で同じメカニズムが作用するかは不明
- **興味深い洞察**: 同一エージェントが in-context learning（fast timescale）と weight update（slow timescale）で異なる役割を担うという二重性は、Foundation Model の multi-agent 展開において重要な含意を持つ
- **再現実装の候補**: GRU + IPD は比較的シンプルな設定。JAX/Flax で再現可能と思われる。PPI アルゴリズム（Algorithm 1）は十分詳細に記述されている
- **気になる拡張**: (1) LLM ベースのエージェントでの検証、(2) N>2 エージェント設定、(3) Communication ありの Social Dilemma
