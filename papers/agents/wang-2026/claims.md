# Claims Analysis: DeepResearchEval

**Paper:** `papers/agents/wang-2026/`
**Date:** 2026-02-24

---

## Claim 1: ペルソナ駆動パイプラインは高品質な deep research タスクを自動生成できる

| Aspect | Assessment |
|--------|-----------|
| **Type** | Methodological / Empirical |
| **Evidence** | 7名の博士号保持専門家が155タスクを独立評価し、80%が4名以上の承認を獲得（Table 2）。最終的に人間ランキングに基づき100タスクを選定。 |
| **Methodology** | 専門家による独立評価（criteria: multi-round search, multi-source evidence integration, substantial analytical depth）。二段階フィルタリング（Task Qualification Filter + Search Necessity Filter）の有効性を人間検証で確認。 |
| **Potential Issues** | 「高品質」の定義が deep research に適しているかは、評価者の主観に依存する。7名の専門家の選定基準・ドメイン分布が不明確。また、自動生成タスクと人手作成タスクの直接比較は行われていない。承認基準の閾値（4名以上）の根拠が示されていない。 |
| **Reproducibility** | プロンプトが Appendix E に全掲載されており、パイプラインの再現は可能。ただし LLM のバージョン依存性（GPT-5-mini）がある。 |
| **Status** | **Partially Supported** -- 人間検証は肯定的だが、既存手動ベンチマークとの比較検証がなく、「自動生成が手動と同等以上」とまでは言えない。 |

**Notes:** パイプラインの段階的フィルタリングは合理的だが、Search Necessity Filter で除外されたタスクの具体例や、フィルタリングの偽陽性・偽陰性率の分析がない。

---

## Claim 2: タスク固有の評価次元は固定次元より一貫して低スコアを示し、タスク適応型評価の必要性を示す

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 3 において、9システム全てで Task-Specific（Task.）列のスコアが Coverage, Insight, Instruction-following, Clarity の全ての固定次元スコアより低い。Table 5（GPT-5 judge）でも同様の傾向。 |
| **Methodology** | 100タスク x 9システム = 900レポートに対して、Gemini-2.5-Pro と GPT-5 の2つの judge モデルで評価。 |
| **Potential Issues** | タスク固有次元が「より厳しい」のは、次元の性質（具体的・特化的であるほど減点されやすい）に起因する可能性があり、Deep research システムの「弱点」とは限らない。また、タスク固有次元の生成品質そのものの検証（人間による妥当性評価）が不足している。生成された次元が本当に重要な品質側面を捕捉しているかは未確認。 |
| **Reproducibility** | 評価プロンプトが全て公開されており、同一モデルアクセスがあれば再現可能。 |
| **Status** | **Supported** -- 数値的傾向は明確であり、2つの judge モデルで一貫。ただし因果的解釈（「システムがタスク固有要件に弱い」vs「タスク固有次元が本質的に厳しい」）は区別できていない。 |

**Notes:** この発見は実用的に重要だが、「タスク固有次元のスコアが低い = タスク適応型評価が必要」という論理的飛躍がある。固定次元を細分化しても同様のスコア低下が起きる可能性がある。

---

## Claim 3: Gemini-2.5-Pro Deep Research がレポート品質で最高、Manus が事実正確性で最高

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Table 3: Gemini-2.5-Pro が Avg 8.51 で全次元トップ。Table 4: Manus が Ratio 82.30% でトップ。Figure 1 で視覚的にも確認。 |
| **Methodology** | 品質評価は Gemini-2.5-Pro judge（100タスク x 9システム）。事実検証は GPT-5-mini agent（MiroFlow + Google Serper API）。 |
| **Potential Issues** | **品質評価における自己選好バイアス**: Gemini-2.5-Pro が judge を務めており、自システムのレポートに有利なバイアスが存在する可能性。GPT-5 judge でも Gemini が1位だが、スコアの絶対値は大きく異なる（8.51 vs 5.29）。**データ収集期間の不統一**: Table 7 によると、DeepSeek は2025年11月10日に収集されており他システム（8-9月）と2ヶ月以上のタイムラグがある。システムのアップデートが結果に影響しうる。**レポート長の差異**: Gemini-2.5-Pro のレポートは平均51.8K文字で、DeepSeek は5.5Kと10倍の差がある。長いレポートが品質評価で有利になる可能性。 |
| **Reproducibility** | システムの API アクセスとプロンプトが公開されており、原理的に再現可能。ただし商用システムの出力は時間とともに変わりうる。 |
| **Status** | **Partially Supported** -- 数値は明確だが、自己選好バイアス、データ収集期間の不統一、レポート長の差異など、結果の解釈に影響する交絡因子が存在する。 |

**Notes:** GPT-5 judge でも順位はほぼ同じだが、絶対スコアの乖離（Gemini の品質が 8.51 vs 5.29）は、judge モデルによってスコアのキャリブレーションが大きく異なることを示唆し、スコアの絶対値の信頼性に疑問を投げかける。

---

## Claim 4: 能動的事実検証は人間専門家と73%一致し、不一致の70%でモデルが正しい

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | 4名の専門家が80文にアノテーション → 73% agreement (Figure 5)。不一致20文を人間+GPT-5.2で再検証 → 70%でモデル判定が正しいと判断（Section 5.3）。 |
| **Methodology** | Wrong と Unknown を negative として二値化した上で一致率を計算。不一致ケースは別の人間専門家が GPT-5.2 の補助を受けて再判定。 |
| **Potential Issues** | **サンプルサイズが極小**: 80文のみであり、統計的有意性の議論がない。信頼区間が示されていない。**再判定の循環性**: 不一致ケースの再判定に GPT-5.2 が介入しており、「モデルが70%正しい」という判定自体がモデルに有利にバイアスされている可能性。**二値化の妥当性**: Wrong と Unknown を同一カテゴリにまとめることの妥当性が未検討。Wrong（明確な誤り）と Unknown（証拠不十分）は本質的に異なる。**比較基準の欠如**: 他の事実検証手法（引用ベース等）との直接比較がない。 |
| **Reproducibility** | 具体的な80文の選定方法が不明。プロンプトは公開されているが、同一の80文セットでの再現は困難。 |
| **Status** | **Partially Supported** -- 方向性は肯定的だが、サンプルサイズの小ささと再判定プロセスの循環性が大きな懸念。73%という数値自体も、タスクの性質を考慮すると高いのか低いのか判断が難しい。 |

**Notes:** Appendix F に正例・誤例が詳細に示されており透明性は高いが、規模の小さい検証で「人間を超える」と示唆する解釈には慎重であるべき。

---

## Claim 5: 品質評価は judge モデルや確率的変動に対してロバストである

| Aspect | Assessment |
|--------|-----------|
| **Type** | Empirical |
| **Evidence** | Cross-judge: GPT-5 judge で9モデル中7モデルが同一順位、残り2モデルも |ΔRank|=1（Table 5）。Stochastic stability: 3回独立実行で全モデルの順位不変、σ ≤ 0.08（Table 6）。 |
| **Methodology** | Cross-judge: Gemini-2.5-Pro と GPT-5 の2つの judge モデルで同一900レポートを評価。Stochastic stability: Gemini-2.5-Pro で3回実行（temperature=0.1, seed=42）。 |
| **Potential Issues** | **Judge モデルの多様性不足**: 2つの frontier モデル間の一致は、両モデルが類似した学習データ・バイアスを共有している可能性がある。より多様なモデル（オープンソースモデルを含む）での検証が望ましい。**温度設定が低い**: temperature=0.1 での3回実行は確率的安定性の強い証拠とは言えない（元々変動が少ない設定）。**順位のみの比較**: 絶対スコアは judge 間で大きく異なる（e.g., Gemini: 8.51 vs 5.29）ため、「ロバスト」の定義が順位の一致に限定されている。 |
| **Reproducibility** | 同一モデルアクセスと設定で再現可能。 |
| **Status** | **Supported** -- 順位のロバスト性は説得力がある。ただし、「ロバスト」を順位安定性に限定した主張であり、絶対スコアのキャリブレーションについては保証されていない。 |

**Notes:** Table 6 の標準偏差の小ささ（0.01-0.08）は印象的だが、低温度設定下での安定性は本質的なロバスト性というよりは設計上の帰結である可能性がある。

---

## Overall Assessment

- **Strongest claims:** Claim 2（タスク固有次元のスコア低下）と Claim 5（評価のロバスト性）は、数値的証拠が明確で2つの judge モデルで一貫している。
- **Weakest claims:** Claim 4（人間との一致率）は、サンプルサイズの小ささと再判定の循環性により、主張の強さに対して証拠が不十分。Claim 3 は自己選好バイアスと交絡因子の影響を受けている可能性がある。
- **Missing experiments:**
  - タスク固有次元の品質に関する人間評価（生成された次元が本当に重要な品質側面を捉えているか）
  - オープンソース Deep research システムの評価
  - 既存手動ベンチマーク（DeepResearch Bench 等）との直接比較
  - 能動的事実検証 vs 引用ベース事実検証の直接比較
  - より大規模な人間一致率検証（80文ではなく数百文規模）
  - レポート長を統制した品質評価（長いレポートが有利になるバイアスの検証）
