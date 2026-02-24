# Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens

**Authors:** Wei-Lin Chen, Liqian Peng, Tian Tan, Chao Zhao, Blake JianHang Chen, Ziqian Lin, Alec Go, Yu Meng
**Venue:** Google / University of Virginia, 2026 (preprint)
**PDF:** `paper.pdf`
**Date Read:** 2026-02-24

---

## One-Sentence Summary

LLM の推論努力を測定するために、出力トークン数ではなく、モデル内部の layer-wise な予測分布の収束深度に基づく deep-thinking ratio (DTR) を提案し、DTR が精度とより強い正の相関を示すことを実証した上で、DTR を活用した test-time scaling 戦略 Think@n を導入している。

## Problem Statement

LLM の Chain-of-Thought (CoT) による推論において、生成トークン数（出力の長さ）が推論品質の信頼できる指標であるという仮定が広く採用されている。しかし、近年の研究は、トークン数と精度の間に逆U字型の関係や逆スケーリング現象を報告しており、長い推論が必ずしも良い結果をもたらさないことを示している。著者らはこの問題に対し、推論努力を測定するためのより原理的で機構的に根拠のある指標が必要であると主張している。

## Core Thesis & Design Philosophy

- **Core thesis:** LLM の推論努力の本質は「どれだけ長く考えるか」ではなく「どれだけ深く考えるか」にあり、個々のトークン生成時に深い layer まで予測分布が改訂され続ける度合いが、有効な推論の質を反映するという洞察。
- **What they reject:** トークン数（出力長）が test-time compute や推論品質の適切な代理指標であるという従来の仮定を否定する。Overthinking（冗長で誤りを増幅する推論）の存在がこの仮定を覆すと主張している。
- **What they bet on:** Transformer の各 layer における中間予測分布の深さ方向の進化（depth-wise evolution）が、トークンレベルでの計算努力を自然に反映しており、これを集約することで sequence レベルの推論品質を測定できるという原理。

## Intellectual Lineage

| Source | Original Concept | How This Paper Adapts It |
|--------|-----------------|-------------------------|
| Nostalgebraist (2020) — Logit Lens | 中間 layer の hidden state を unembedding matrix で vocabulary space に射影し、各 layer での next-token 予測を可視化する手法 | この射影手法をそのまま採用し、各 layer の予測分布と最終 layer の分布間の Jensen-Shannon divergence を計算することで、トークンごとの「settling depth」を定量化する基盤技術として使用 |
| Chuang et al. (2023) — DoLa | LLM の factual knowledge が特定の layer でより顕著であるという観察に基づき、高い layer と低い layer の logit を対比させて factuality を改善する decoding 手法 | DoLa が layer 間の対比を decoding 改善に活用したのに対し、本研究は layer 間の分布差を推論努力の測定指標として再解釈。JSD の使用も DoLa に倣っているが、目的は生成改善ではなく推論品質の事後評価 |
| Belrose et al. (2023) — Tuned Lens | 中間 layer の hidden state に学習済みの affine 変換を適用し、より正確な layer-wise 予測を得る手法（Logit Lens の改良版） | Tuned Lens のような学習済み変換は使わず、生の unembedding matrix による射影のみを使用。これにより追加学習なしで任意のモデルに適用可能な手法を実現 |
| Wang et al. (2023) — Self-Consistency | 複数サンプリングされた回答に対して majority voting を行い、最も一致する回答を選択する test-time scaling 手法 | Self-Consistency の majority voting フレームワークを基盤としつつ、全サンプルではなく DTR スコアの高い上位サンプルのみを選択的に集約する Think@n として拡張。これにより約半分の推論コストで同等以上の精度を実現 |
| Early Exiting 研究 (Elbayad 2019, Schuster 2022, Teerapittayanon 2016) | 計算コスト削減のため、中間 layer で予測が十分に安定した場合に残りの layer をスキップする手法群 | Early exiting が「早く安定するトークンの計算を省略する」のに対し、本研究は「遅くまで安定しないトークンの割合」を推論品質の指標として測定。方向性は逆だが、layer-wise stabilization という共通の概念を活用 |

## Proposed Method

### Overview

著者らは deep-thinking ratio (DTR) を提案している。これは、生成されたシーケンス中で、中間 layer の予測分布が最終 layer の分布に収束するまでに深い layer を必要としたトークン（deep-thinking tokens）の割合である。DTR は各トークンの hidden state を unembedding matrix で vocabulary space に射影し、各 layer の分布と最終 layer の分布間の Jensen-Shannon divergence (JSD) を計算することで算出される（Algorithm 1）。さらに、DTR を活用した test-time scaling 戦略 Think@n を導入し、複数サンプル中から DTR の高いサンプルを優先的に選択・集約する。

### Key Design Decisions

1. **距離指標として JSD を採用** — 中間 layer と最終 layer の予測分布間の距離を JSD で測定。*Rationale:* JSD は対称性と有界性（0から1の範囲）を持ち、数値的に安定している。*Alternatives:* KL divergence（非対称で数値的に不安定、AIME 25 で r=-0.698 と負の相関を示した）、Cosine similarity（hidden state 空間での類似度、HMMT 25 で r=0.172 と弱い相関）。Figure 6 で JSD が最も安定して強い正の相関を示すことが検証されている。

2. **Cumulative minimum による settling depth の定義** — 単一 layer での JSD 値ではなく、cumulative minimum $\bar{D}_{t,l}$ を用いて settling を判定。*Rationale:* 単一 layer の JSD は非単調な振る舞いを示す可能性があり、一時的に閾値を下回っても再び上昇するケースを排除するため。Cumulative minimum を取ることで「一度収束したら安定的に閾値以下に留まる」という厳密な settling の定義を保証する。*Alternatives:* 単一 layer の JSD がそのまま閾値を下回る最初の layer を使用（偽陽性のリスク）、moving average による平滑化。

3. **Depth fraction $\rho$ による deep-thinking regime の定義** — 全 layer のうち上位 $(1-\rho)$ の割合に位置する layer を "late regime" と定義し、そこで初めて settle するトークンを deep-thinking token と分類。*Rationale:* 絶対的な layer 番号ではなく相対的な深さ割合を使うことで、異なる layer 数のモデルに汎用的に適用可能。*Alternatives:* 固定 layer 番号での閾値設定（モデル依存）、連続値としての settling depth をそのまま使用（離散分類しない方法）。

4. **Think@n における短い prefix での DTR 推定** — 完全なシーケンスを生成せず、最初の $\ell_{\text{prefix}}=50$ トークンのみで DTR を推定し、低 DTR サンプルを早期棄却。*Rationale:* Table 3 で prefix 50 トークンが完全シーケンスと同等の精度を達成しつつ推論コストを約半分に削減することが示されている。短い prefix でもシーケンス全体の DTR 傾向を十分に捉えられるという実験的知見に基づく。*Alternatives:* 完全シーケンスでの DTR 計算（コスト削減なし）、より長い prefix（100, 500, 1000 トークン — Table 3 で精度がやや低下）。

### Technical Details

**モデルの定式化:** Autoregressive LM $f_\theta$ は $L$ 個の Transformer layer、hidden dimension $d$、vocabulary $V$ を持つ。Generation step $t$ において、各 layer $l$ の hidden state $h_{t,l} \in \mathbb{R}^d$ が得られる。

**中間 layer 予測分布の計算:** Unembedding matrix $W_U \in \mathbb{R}^{|V| \times d}$ を用いて、中間 layer $l$ の logit vector $z_{t,l}$ と確率分布 $p_{t,l}$ を算出:
$$z_{t,l} = W_U h_{t,l}, \quad p_{t,l} = \text{softmax}(z_{t,l})$$

**JSD の計算:** 各 layer $l$ の分布と最終 layer $L$ の分布間の JSD:
$$D_{t,l} = \text{JSD}(p_{t,L}, p_{t,l})$$

**Settling depth:** Cumulative minimum $\bar{D}_{t,l} = \min_{j \leq l} D_{t,j}$ を計算し、settling depth $c_t$ を次のように定義:
$$c_t = \min\{l : \bar{D}_{t,l} \leq g\}$$
ここで $g$ は settling threshold（実験では $g=0.5$）。

**Deep-thinking token の分類:** Depth fraction $\rho$ を用いて late regime $\mathcal{L}_{\text{deep-thinking}}$ を定義し、$c_t \in \mathcal{L}_{\text{deep-thinking}}$（すなわち $c_t \geq \lceil(1-\rho)L\rceil$）ならば deep-thinking token と分類（実験では $\rho=0.85$）。

**DTR の計算:** シーケンス $S$ の DTR は deep-thinking tokens の割合:
$$\text{DTR}(S) = \frac{|\{t : c_t \in \mathcal{L}_{\text{deep-thinking}}\}|}{|S|}$$

**Think@n:** $n$ 個のサンプルを生成し、各サンプルの DTR を prefix $\ell_{\text{prefix}}$ トークンから推定。DTR 上位 $\eta\%$ のサンプルに対して majority voting を実行。

![Figure 1](paper_artifacts/image_000001_e28dc8bd826444a3a4595b5cfe630c9f4d49742327855ccd850cc75e7369d7d2.png)

Figure 1 は Token Count と DTR の accuracy との相関の比較を示す。Token Count は平均 r=-0.544 の負の相関、DTR は平均 r=0.828 の正の相関を示している。

![Figure 2](paper_artifacts/image_000002_449b10fb120542affe589ced057bff1e837bb2e8fa1c7b1c81acaef1259eb1e5.png)

Figure 2 は GPT-OSS-120B-high の回答シーケンスにおける layer ごとの JSD heatmap。機能語（'and', 'is' 等）は浅い layer で収束し、演算子の後の補完（'+', '=' 等）や回答トークン（'13', '(D)' 等）は深い layer まで収束しない。

![Figure 3](paper_artifacts/image_000003_2bd5a692dc805ff63288784785d1aad311543a651552a8d62dcb087026d09c52.png)

Figure 3 は deep-thinking token の判定プロセスの図解。10 layer のモデル、$\rho=0.8$ の例で、各 layer の JSD 値と閾値 $g$ の比較を示す。

## Key Claims

1. **DTR は task accuracy と強い正の相関を示し、トークン長ベースおよび confidence ベースの baseline を大幅に上回る** — Evidence: Table 1 で 8 モデル x 4 ベンチマーク（32 設定）にわたり DTR の平均相関 r=0.683 を達成（Reverse Token Count r=0.594、Self-Certainty r=0.605 に対して最高）。
2. **トークン数は推論品質の信頼できない代理指標であり、長い推論は精度低下と関連する** — Evidence: Table 1 で Token Length の平均相関 r=-0.594。Figure 1 左パネルで負の相関を視覚的に確認。
3. **Think@n は Self-Consistency (Cons@n) と同等以上の精度を約半分の推論コストで達成する** — Evidence: Table 2 で OSS-120B-medium において Think@n が 4 ベンチマーク中 3 つで Cons@n を上回り（AIME 25: 94.7 vs 92.7、AIME 24: 93.3 vs 92.7、HMMT 25: 80.0 vs 80.0）、コスト削減は約 48-49%。
4. **DTR は 50 トークンの短い prefix から推定可能であり、完全シーケンスと同等の性能を維持する** — Evidence: Table 3 で prefix 50 の Think@n が accuracy 94.7 を達成し、全シーケンス使用時の 94.0 を上回る。

## Methodology Assessment

- **Datasets:** AIME 2024、AIME 2025、HMMT 2025（competition-level 数学問題）、GPQA-Diamond（大学院レベル科学問題）の 4 ベンチマーク。いずれも推論集約型の challenging なタスクとして広く使用されている。問題数は限られており（AIME は各年 30 問、HMMT や GPQA-D もおそらく数百問規模）、統計的検出力に懸念がある。
- **Baselines:** Token Count、Reverse Token Count、Log Probability、Negative Perplexity、Negative Entropy、Self-Certainty の 6 種類。包括的だが、Vilas et al. (2025) の latent-trajectory signal のような他の内部表現ベースの手法との比較が欠けている。
- **Metrics:** Pearson 相関係数（binned analysis、5 bins）。Binning は分散を減らすが、非線形関係を隠す可能性がある。精度は Pass@1 および majority voting accuracy。
- **Statistical rigor:** 30 random seeds で平均化（相関分析）、10 trials で平均化（Think@n 実験）。標準偏差は Table 3 でのみ報告されており、Table 1 の相関値には信頼区間が提示されていない。
- **Reproducibility:** GPT-OSS モデルは OpenAI の非公開モデルであり、中間 layer の hidden state へのアクセスが必要。DeepSeek-R1-70B と Qwen3 はオープンソースだが、GPT-OSS での再現は困難。ハイパーパラメータ（$g=0.5$、$\rho=0.85$）は明示されている。コード公開の有無は本文で言及されていない。

## Results Summary

**相関分析（Table 1）:** DTR は 32 のモデル-ベンチマーク設定中 30 で正の相関を示し（負の相関は 2 件のみ）、平均 r=0.683 を達成。これは全 baseline を上回る。ただし、一部の設定（OSS-20B-medium/AIME 2024: r=-0.192、Qwen3-30B/AIME 2024: r=-0.657）では DTR が失敗しており、普遍的ではない。

**Think@n（Table 2、Figure 5）:** OSS-120B-medium では Think@n が 4 ベンチマーク中 3 つで Cons@n を上回り、コストを約 49% 削減。Qwen3-4B-Thinking でも同様の傾向が確認されている。

**ハイパーパラメータ感度（Figure 4）:** Settling threshold $g$ は相関に大きな影響を与え、$g=0.5$ が最適。Depth fraction $\rho$ は相関に対する影響が小さく、ロバスト。

**Reasoning level との関係（Figure 7、Appendix B）:** GPT-OSS-120B の reasoning level が高いほど DTR は低下するが精度は向上するという興味深い傾向が報告されている。著者らは、高い reasoning level が depth-wise computation を sequence length に再分配している可能性を示唆している。

## Limitations & Open Questions

- **モデル内部へのアクセスが必要:** DTR の計算には全 layer の hidden state が必要であり、API 経由のみでアクセス可能なモデル（GPT-4o, Claude 等）には直接適用できない。この制約は実用性を大幅に制限する。
- **一部の設定で DTR が失敗する:** Table 1 で OSS-20B-medium/AIME 2024 (r=-0.192) や Qwen3-30B/AIME 2024 (r=-0.657) で負の相関が観測されており、DTR の有効性が普遍的でない可能性がある。著者らはこれらの失敗ケースについて詳細な分析を提供していない。
- **DTR のモデル間・モード間比較不可能性:** Appendix B で著者ら自身が認めているように、DTR は生成長（分母）に依存するため、異なるモデルや reasoning level 間での直接比較には適さない。
- **因果関係の不在:** DTR と精度の正の相関は示されているが、「深い思考がより良い推論を引き起こす」という因果的主張は検証されていない。単に「正しい回答を生成するときにモデルの内部処理がより深くなる」という相関的観察に過ぎない可能性がある。
- **ベンチマークの限定性:** 数学・科学の 4 ベンチマークのみで評価されており、自然言語推論、コード生成、常識推論など他の推論タスクへの汎化は未検証。
- **Binned analysis の影響:** 5 bins での Pearson 相関はデータの平滑化効果があり、個々のサンプルレベルでの相関はかなり弱い可能性がある。
- **Prefix DTR の理論的根拠の欠如:** 50 トークンの prefix で全シーケンスの DTR を推定できるという知見は経験的であり、なぜ短い prefix が有効なのかについての理論的説明は提供されていない。

## Connections to Other Work

- **Builds on:** Logit Lens (Nostalgebraist 2020)、DoLa (Chuang et al. 2023)、Self-Consistency (Wang et al. 2023)、inverse scaling の観察 (Gema et al. 2025; Wu et al. 2025)
- **Compared with:** Token count proxies、confidence-based measures (Log Probability, Perplexity, Entropy, Self-Certainty)、length-based voting (Hassid et al. 2025; Agarwal et al. 2025)
- **Enables:** DTR を test-time compute の配分に活用する adaptive reasoning、early exiting と DTR の組み合わせ、DTR を reward signal とした RL-based training、モデル内部の depth utilization の理解深化

## Personal Notes

- DTR の概念自体は直感的に魅力的であり、「長く考える」と「深く考える」の区別は重要な洞察である。しかし、因果関係が確立されていないため、DTR が高いトークンが「より良い推論をしている」のか、単に「難しい予測を行っている」のかは区別できない。
- Table 1 の結果を注意深く見ると、DTR が他の baseline を劇的に上回るわけではない。平均相関 r=0.683 は Self-Certainty の r=0.605 や Negative Entropy の r=0.571 と比較して modest な改善にとどまる。特に GPQA-Diamond では Negative Entropy (平均 ~0.77) や Self-Certainty (平均 ~0.87) が DTR と同等以上の性能を示すケースが多い。
- Think@n の実用的価値は高い。50 トークンの prefix で早期棄却できるという知見は、推論コスト削減に直結する。ただし、この手法が効果的であるためには中間 layer の hidden state へのアクセスが必要であり、実際の deployment では制約となる。
- Appendix B の reasoning level と DTR の関係は論文の主張と緊張関係にある。高い reasoning level（より良い推論能力）が低い DTR をもたらすのであれば、「深い思考 = 良い推論」という単純な解釈は成立しない。著者らは depth から length への計算再分配として説明しているが、これは DTR の解釈をより複雑にする。
