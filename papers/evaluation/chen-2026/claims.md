# Claims Analysis: Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens

**Paper:** `papers/evaluation/chen-2026/`
**Date:** 2026-02-24

---

## Claim 1: DTR はタスク精度と強い正の相関を示し、長さベースおよび confidence ベースの全 baseline を上回る

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 1: 8 モデル x 4 ベンチマーク（32 設定）で DTR の平均 Pearson 相関 r=0.683 を報告。Reverse Token Count (r=0.594)、Self-Certainty (r=0.605)、Negative Entropy (r=0.571) を上回る。Figure 1 で GPT-OSS-120B-medium における DTR の平均相関 r=0.828（vs Token Count r=-0.544）を視覚的に示す。 |
| **Methodology** | Binned analysis（5 bins の quantile 分割）で Pearson 相関を計算。30 random seeds で平均化。4 ベンチマーク（AIME 24/25, HMMT 25, GPQA-D）、3 モデルファミリー（GPT-OSS, DeepSeek-R1, Qwen3）で評価。 |
| **Potential Issues** | (1) Binned analysis は平滑化効果があり、個々のサンプルレベルでの相関は弱い可能性がある。5 bins の Pearson 相関は自由度 3 であり、統計的有意性の検定が提示されていない。(2) 平均 r=0.683 は modest な値であり、32 設定中 2 設定で負の相関（OSS-20B-medium/AIME24: r=-0.192、Qwen3-30B/AIME24: r=-0.657）を示す。(3) Figure 1 の r=0.828 は GPT-OSS-120B-medium のみの結果であり、Table 1 の平均 r=0.683 とは異なる。 |
| **Reproducibility** | GPT-OSS モデルは非公開であり、中間 layer の hidden state アクセスが必要。DeepSeek-R1-70B と Qwen3-30B-Thinking はオープンソースで再現可能。ハイパーパラメータ（g=0.5, ρ=0.85）は明示。 |
| **Status** | Partially Supported |

**Notes:** DTR が正の相関を示す傾向は全体的に確認されるが、「全 baseline を上回る」という主張は平均値での比較であり、個別設定では Self-Certainty や Negative Entropy が DTR を上回るケースが多数存在する（例: GPQA-Diamond の多くの設定）。また、OSS-20B シリーズでは DTR の相関が全体的に弱い傾向がある。

---

## Claim 2: トークン数は推論品質の信頼できない代理指標であり、長い推論は精度低下と関連する

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 1: Token Length の平均 Pearson 相関 r=-0.594。32 設定中、大多数で負の相関を示す。Figure 1 左パネルで 4 ベンチマークすべてにおいて Token Count と accuracy の負の相関を視覚的に確認。 |
| **Methodology** | 同上の binned analysis。中立的なプロンプト（reasoning budget を指定しない）を使用し、モデルが自然に推論長を決定する設定。 |
| **Potential Issues** | (1) これは本論文の独自の知見ではなく、先行研究（Gema et al. 2025; Wu et al. 2025）で既に報告されている現象の確認。(2) 因果関係ではなく相関であり、「長い推論が精度を低下させる」ではなく「難しい問題で長い推論が生成されやすい」という confound が考えられる。(3) OSS-120B-low/AIME25 (r=0.504) や OSS-120B-low/HMMT25 (r=0.871) では正の相関を示すケースもあり、普遍的ではない。 |
| **Reproducibility** | 先行研究でも類似の結果が報告されており、再現性は高いと考えられる。 |
| **Status** | Supported |

**Notes:** トークン長と精度の負の相関は先行研究と整合的であり、十分に支持されている。ただし、一部モデル・ベンチマーク設定（特に low reasoning level）では正の相関を示すため、「信頼できない」という表現はやや強すぎる可能性がある。正確には「一貫しない」と表現する方が適切。

---

## Claim 3: Think@n は Self-Consistency (Cons@n) と同等以上の精度を約半分の推論コストで達成する

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 2: OSS-120B-medium で Think@n は AIME 25 (94.7 vs 92.7, -49%), AIME 24 (93.3 vs 92.7, -48%), HMMT 25 (80.0 vs 80.0, -49%), GPQA-D (74.7 vs 73.8, -48%) と報告。Qwen3-4B-Thinking でも同様の傾向。Figure 5 で Pareto 最適性を視覚的に確認。 |
| **Methodology** | Best-of-n 評価プロトコル。n=48 サンプル、上位 η=50% を選択。prefix 長 50 トークンで DTR を推定。10 trials で平均化。Self-Certainty@n を含む複数の aggregation method と比較。 |
| **Potential Issues** | (1) 評価は OSS-120B-medium と Qwen3-4B-Thinking の 2 モデルのみ。Table 1 で DTR の相関が弱かったモデル（OSS-20B-medium 等）での Think@n 評価が欠けている。(2) GPQA-D では Cons@n (73.8) と Think@n (74.7) の差は小さく、Self-Certainty@n (76.0) が Think@n を上回っている。(3) n=48 は大量のサンプリングであり、実用的なコスト面での利点は限定的な可能性がある。(4) 標準偏差は Table 3 でのみ報告され、Table 2 では報告されていない。 |
| **Reproducibility** | OSS-120B-medium は非公開モデル。Qwen3-4B-Thinking はオープンソースだが中間 layer へのアクセスが必要。 |
| **Status** | Partially Supported |

**Notes:** 全体的な傾向として Think@n のコスト効率は確認されるが、「同等以上」という主張は一部設定（GPQA-D）では Self-Certainty@n に劣る。また、DTR の相関が弱いモデルでの検証が不足しており、汎化性に疑問が残る。

---

## Claim 4: DTR は 50 トークンの短い prefix から推定可能であり、完全シーケンスと同等の性能を維持する

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 3: AIME 2025 / OSS-120B-medium で prefix 50 の Think@n accuracy 94.7（cost 155.4k）vs 全シーケンス使用時 94.0（cost 307.6k）。Prefix 50 が最高精度を達成し、prefix 長を増やすと精度がやや低下（100: 92.0, 500: 92.7, 1000: 92.7, 2000: 92.0）。 |
| **Methodology** | AIME 2025、OSS-120B-medium のみで prefix 長を変化させた ablation。10 trials、標準偏差を報告。 |
| **Potential Issues** | (1) 単一ベンチマーク・単一モデルでの ablation のみ。他のモデルやベンチマークでの検証が欠けている。(2) Prefix 50 が全シーケンスより精度が高い（94.7 vs 94.0）のは直感に反し、分散の範囲内の変動である可能性（標準偏差 1.6 vs 0.3）。(3) なぜ短い prefix が有効かについての理論的説明がない。 |
| **Reproducibility** | OSS-120B-medium は非公開モデル。 |
| **Status** | Insufficient Evidence |

**Notes:** 結果は示唆的だが、単一設定での ablation のみでは「50 トークンで十分」という一般的主張を支持するには証拠が不十分。特に、prefix 50 が全シーケンスを上回るという結果は分散の影響である可能性が高く、より広範な検証が必要。

---

## Claim 5: Deep-thinking tokens は機能語と内容語で異なる settling パターンを示す

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical / Qualitative |
| **Evidence** | Figure 2: GPT-OSS-120B-high の回答シーケンスにおける JSD heatmap。機能語（'and', 'is', 'boxed' 等）は浅い layer で収束、演算子後の補完（'+', '=' 等）や回答トークン（'13', '(D)' 等）は深い layer まで収束しない。Appendix E の定性的例（Table 7/8）で、不正解（DTR=13.9%, 27,724 tokens）vs 正解（DTR=19.0%, 3,725 tokens）の対比。 |
| **Methodology** | 単一モデル（GPT-OSS-120B-high）の単一回答シーケンスの可視化。Appendix E も単一問題の 2 つの回答の比較。 |
| **Potential Issues** | (1) 極めて限られた定性的証拠。体系的な分析（トークンカテゴリ別の settling depth の統計的比較）が欠けている。(2) Cherry-picked な例である可能性を排除できない。(3) Appendix E の例は DTR と正解率の相関を示す anecdote であり、因果的証拠ではない。 |
| **Reproducibility** | GPT-OSS-120B-high は非公開モデル。 |
| **Status** | Insufficient Evidence |

**Notes:** 直感的には魅力的な観察だが、体系的な証拠が不足している。大規模なトークンカテゴリ別分析が必要。

---

## Claim 6: ハイパーパラメータ (g, ρ) = (0.5, 0.85) が最適なバランスを提供する

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Figure 4: GPQA-D / GPT-OSS-20B-high での g ∈ {0.25, 0.5, 0.75} および ρ ∈ {0.8, 0.85, 0.9, 0.95} のスイープ。g=0.5 で最も安定した正の相関、ρ の変化は DTR の range を shift するが傾きは維持。 |
| **Methodology** | 単一モデル（GPT-OSS-20B-high）、単一ベンチマーク（GPQA-D）での grid search。 |
| **Potential Issues** | (1) 単一モデル・単一ベンチマークでの結果を一般化している。他の設定での最適ハイパーパラメータが異なる可能性。(2) g=0.75 も良好な相関を示しており、g=0.5 が明確に最適とは言えない。(3) ρ と g の interaction effect は検証されていない。 |
| **Reproducibility** | GPT-OSS-20B-high は非公開。 |
| **Status** | Partially Supported |

**Notes:** 提示された設定では妥当な選択だが、単一設定での最適化を一般的推奨としている点は留保が必要。

---

## Overall Assessment

- **Strongest claims:** Claim 2（トークン長の不信頼性）は先行研究とも整合的で最も堅固。Claim 1（DTR と精度の正の相関）も全体的傾向として支持されるが、普遍性には疑問が残る。
- **Weakest claims:** Claim 4（50 トークン prefix の十分性）は単一設定での検証のみで証拠不十分。Claim 5（トークンカテゴリ別パターン）は定性的観察にとどまる。
- **Missing experiments:** (1) DTR の相関が弱いモデル（OSS-20B-medium、Qwen3-30B/AIME24）に対する詳細な failure analysis。(2) 個々のサンプルレベル（binning なし）での相関分析。(3) 数学・科学以外の推論タスク（コード生成、自然言語推論等）での評価。(4) Vilas et al. (2025) の latent-trajectory signal との直接比較。(5) DTR と精度の因果関係の検証（例: 介入実験）。(6) 複数モデル・ベンチマークでの prefix 長 ablation。
