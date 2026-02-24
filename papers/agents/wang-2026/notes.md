# DeepResearchEval: An Automated Framework for Deep Research Task Construction and Agentic Evaluation

**Authors:** Yibo Wang, Lei Wang, Yue Deng, Keming Wu, Yao Xiao, Huanjin Yao, Liwei Kang, Hai Ye, Yongcheng Jing, Lidong Bing
**Venue:** Preprint (arXiv), 2026
**PDF:** `paper.pdf`
**Date Read:** 2026-02-24

---

## One-Sentence Summary

Deep research システムの評価における3つの根本的課題（タスク構築のコスト、固定的な評価軸、引用なし主張の検証不能）を解決するため、persona 駆動のタスク自動生成とタスク適応型品質評価・能動的事実検証を組み合わせた自動評価フレームワーク DeepResearchEval を提案する論文。

## Problem Statement

Deep research システム（OpenAI Deep Research, Gemini Deep Research 等）は、複雑なマルチステップ Web 調査・分析・レポート生成を自律的に行うが、その評価には以下の3つの課題が存在すると著者らは主張する:
1. **タスク構築のコスト**: 既存ベンチマークの多くは専門家による手動アノテーションに依存しており、高コストかつスケーラブルでない
2. **固定的な評価次元**: 全タスクに同一の評価軸を適用するため、タスク固有の品質要素を捉えられない
3. **引用依存の事実検証**: 引用付き主張のみを検証し、引用なしの事実主張を見逃す

## Core Thesis & Design Philosophy

- **Core thesis:** Deep research レポートの評価は「タスクごとに異なる成功基準」を持つべきであり、固定的な rubric では不十分である。タスク構築も人手ではなくペルソナ駆動で自動化すべきである。
- **What they reject:** 従来の「固定評価次元 + 引用ベース事実検証」パラダイム。すべてのタスクを同じ物差しで測ることの限界、および引用リンクの有無に依存した事実確認の不完全性を否定する。
- **What they bet on:** LLM を evaluator として活用する「agentic evaluation」パラダイム。タスクごとに評価次元・基準・重みを動的に生成し、MCP ツールを用いた能動的 Web 検索で引用の有無にかかわらず事実を検証できるという賭け。

## Intellectual Lineage

| Source | Original Concept | How This Paper Adapts It |
|--------|-----------------|-------------------------|
| Wettig et al. (2025) "Organize the Web" | Web データのドメイン分類タクソノミー。Web コーパスのキュレーションに使用。 | 10カテゴリのドメインセットとして借用し、ペルソナ生成の種（seed）として利用。ドメイン多様性を確保するための構造的基盤とする。 |
| Wei et al. (2024) "Long-form Factuality" | LLM の長文生成における事実性を文レベルで検証する手法。Search-Augmented Factual Evaluation を提案。 | Active Fact-Checking の基本設計に影響。文レベルの事実抽出と外部証拠による検証というパターンを踏襲しつつ、引用なし主張への拡張と Right/Wrong/Unknown の3値ラベル体系を導入。 |
| MiroFlow (MiroMind, 2025) | MCP ベースのオープンソース agentic フレームワーク。Deep research のためのツール呼び出しアーキテクチャ。 | Fact-checking agent の実行基盤として採用。MCP サーバーの google_search(), scrape_website(), wiki_get_page_content() を活用し、エージェントが自律的に証拠を収集する仕組みを構築。 |
| Du et al. (2025) "DeepResearch Bench", Fan et al. (2025) | 固定評価次元（Coverage, Coherence 等）による Deep research レポート評価。 | 4つの固定次元（Coverage, Insight, Instruction-following, Clarity）を保持しつつ、タスク固有次元を LLM で自動生成する「適応型」設計に拡張。固定と動的のハイブリッド構成。 |
| Phan et al. (2025) "Humanity's Last Exam", Mialon et al. (2024) "GAIA" | エージェントの汎用推論・ツール使用能力を測るベンチマーク。手動でタスク構築。 | タスク構築の自動化という対比軸として位置づけ。人手アノテーションの限界を動機とし、ペルソナ駆動パイプラインによる自動生成を提案。 |

## Proposed Method

### Overview

DeepResearchEval は大きく2つのコンポーネントから構成される:
1. **タスク構築パイプライン** (Section 3): ペルソナ駆動でリアルな deep research タスクを自動生成
2. **Agentic 評価パイプライン** (Section 4): 適応型品質評価 + 能動的事実検証

全体のワークフローは Figure 2 と Figure 4 に示されている。

![Figure 2: Task Construction Pipeline](paper_artifacts/image_000001_7c9f4d8a6586c756bc2ec5e3856056041da60746395374d3cbb27f302517d2fc.png)

![Figure 4: Agentic Evaluation Pipeline](paper_artifacts/image_000003_d7c444fe980852cfc342c45d7e3317f77f3b649c7d1590b0d84e9dc402964b3b.png)

### Key Design Decisions

1. **ペルソナ駆動タスク生成**: ドメインごとにペルソナを生成し、そのペルソナの背景に基づいてタスクを構築する方式を採用。
   - *Rationale:* 現実世界の多様な情報ニーズを反映し、タスクの複雑性とリアリティを確保するため。専門家アノテーションのコストとドメインバイアスを回避。
   - *Alternatives:* 専門家による手動タスク設計（Du et al., 2025; Abaskohi et al., 2025）、既存データセットからのタスク抽出（Li et al., 2025a）。

2. **二段階フィルタリング（Task Qualification + Search Necessity）**: 生成タスクを「Deep research として適格か」と「LLM の内部知識だけでは解けないか」の2段階で選別。
   - *Rationale:* 単純な QA やパラメトリック知識で解ける問題を排除し、真に外部検索と多ソース統合が必要なタスクのみを残すため。
   - *Alternatives:* 人間によるフィルタリングのみ（コスト高）、単一基準のフィルタリング（品質不十分）。

3. **固定次元 + タスク固有次元のハイブリッド評価**: 4つの一般評価次元（Coverage, Insight, Instruction-following, Clarity）を全タスク共通とし、加えて1-3個のタスク固有次元を LLM で動的生成。
   - *Rationale:* タスク間の比較可能性（固定次元）と、タスク固有の成功基準の捕捉（動的次元）を両立させるため。
   - *Alternatives:* 完全固定次元（Du et al., 2025; Fan et al., 2025）、完全動的次元（解釈性・比較性の低下リスク）。

4. **能動的事実検証（Active Fact-Checking）**: 引用の有無に関係なく、レポートから検証可能な主張を抽出し、MCP ツール経由で Web 検索して外部証拠と照合。
   - *Rationale:* 引用ベースの検証では、引用なし主張や引用先が主張を支持しないケースを見逃す。能動的検索により網羅的な事実検証を実現。
   - *Alternatives:* 引用ベース検証のみ（Du et al., 2025; Fan et al., 2025）、LLM の内部知識による検証（最新情報に弱い）。

5. **Right / Wrong / Unknown の3値ラベル**: 事実検証の結果を「正しい」「誤り」「証拠不十分」の3値で分類。
   - *Rationale:* 検証不能な主張と明確な誤りを区別することで、より精密な事実性評価を可能にする。
   - *Alternatives:* 二値分類（Correct/Incorrect）、連続スコア。

### Technical Details

**タスク構築パイプライン:**
- 10ドメイン x 5ペルソナ = 50ペルソナを生成
- 各ペルソナから4タスク生成 → 200候補タスク
- Task Qualification Filter（信頼スコア > 0.7）→ 候補を絞り込み
- Search Necessity Filter（LLM の内部知識による no-search baseline を生成・評価し、高スコアのものを除外）→ 155タスク保持
- 7名の博士号保持専門家による検証（80%が4名以上の承認）→ 最終的に100タスクを選定

**適応型品質評価:**
- $D = D_{\text{general}} \cup D_{\text{task}}$ として評価次元を構成
- 各次元 $d$ に正規化重み $W_d$ を割り当て（$\sum_{d \in D} W_d = 1$）
- 各次元内で基準 $\{c\}$ に重み $w_{d,c}$ を割り当て（$\sum_c w_{d,c} = 1$）
- 各基準を [1, 10] でスコアリング
- 最終スコア: $S_{\text{quality}} = \sum_{d \in D} W_d \cdot \sum_c w_{d,c} \cdot s_{d,c}$
- 評価 LLM: Gemini-2.5-Pro（temperature=0.1, seed=42, max 8192 tokens）

**能動的事実検証:**
- レポートをセグメント $P = \{p_1, p_2, \ldots, p_N\}$ に分割
- 各セグメントから検証可能な主張 $S_i = \{s_{i1}, s_{i2}, \ldots\}$ を抽出
- MCP ツール（google_search, scrape_website, wiki_get_page_content）で外部証拠 $E(s)$ を収集
- $y(s) \in \{\text{Right}, \text{Wrong}, \text{Unknown}\}$ を判定
- Ratio = $N_{\text{Right}} / N_{\text{Statements}}$
- Fact-checking LLM: GPT-5-mini（MiroFlow フレームワーク上、最大30ターン、ターンあたり最大10ツール呼び出し）

## Key Claims

1. **ペルソナ駆動パイプラインは高品質な deep research タスクを自動生成できる** -- Evidence: 7名の博士号保持専門家による検証で155タスク中80%が4名以上の承認を獲得（Table 2）
2. **タスク固有の評価次元は固定次元より一貫して低スコアを示す** -- Evidence: 9システム全てで Task-Specific スコアが一般次元より低い（Table 3, Table 5）
3. **Gemini-2.5-Pro Deep Research がレポート品質で最高性能、Manus が事実正確性で最高** -- Evidence: 品質評価で Gemini が8.51/10、事実検証で Manus が82.30% Ratio（Table 3, Table 4, Figure 1）
4. **能動的事実検証は人間の専門家と73%の一致率を達成し、不一致ケースの70%でモデルが正しい** -- Evidence: 4名の専門家が80文を検証し73%一致、不一致20文の再検証で70%がモデル正答（Section 5.3, Figure 5）
5. **品質評価は judge モデルや確率的変動に対してロバスト** -- Evidence: GPT-5 judge で9モデル中7モデルが同一順位（Table 5）、3回独立実行でランキング不変・標準偏差が微小（Table 6）

## Methodology Assessment

- **Datasets:** 自動生成の100タスク x 9システム = 900レポート。10ドメインをカバー。タスク分布は Figure 3 に示す（各ドメイン9-12%でほぼ均等）。ただし英語中心であり、多言語評価は未実施。
- **Baselines:** 9つの商用 deep research システムを比較。オープンソースシステム（WebThinker, DeepResearcher 等）は含まれていない。
- **Metrics:** 品質評価は [1,10] スケールの加重平均スコア、事実検証は Right Ratio。品質と事実性を分離して評価する設計。
- **Statistical rigor:** 品質評価の3回独立実行で安定性を確認（Table 6, 標準偏差 0.01-0.08）。ただし事実検証の再現性は明示的に検証されていない。人間との一致率検証は80文のみで規模が小さい。
- **Reproducibility:** コードは GitHub で公開（https://github.com/Infinity-AILab/DeepResearchEval）。ただし評価に Gemini-2.5-Pro と GPT-5-mini という商用モデルを使用しており、完全な再現にはこれらへのアクセスが必要。プロンプトは Appendix に全て掲載。

## Results Summary

**品質評価 (Table 3):**
- Gemini-2.5-Pro Deep Research が全次元でトップ（Avg 8.51）、Claude-Sonnet-4.5 が2位（7.53）
- DeepSeek（5.25）と Manus（5.95）が最下位グループ
- 全システムで Task-Specific スコアが最も低く、固定次元との一貫したギャップを確認

**事実検証 (Table 4):**
- Manus が最高 Ratio（82.30%）、Gemini-2.5-Pro（76.62%）、DeepSeek（76.44%）が続く
- Perplexity（58.94%）と Claude-Sonnet-4.5（60.72%）が最低
- Wrong よりも Unknown が多く、事実リスクは「明白な誤り」より「根拠不十分な主張」に起因すると示唆

**品質 vs 事実性のトレードオフ:**
- 品質トップの Gemini は事実性でも上位だが、品質2位の Claude-Sonnet-4.5 は事実性で最下位グループ
- DeepSeek は品質最下位だが事実性は上位（保守的な出力戦略の結果と著者らは示唆）

**検証の信頼性 (Section 5.3):**
- Cross-judge: GPT-5 judge で7/9モデルが同一順位
- Stochastic stability: 3回実行で順位不変、σ ≤ 0.08
- Human alignment: 73%一致、不一致の70%でモデルが正解

## Limitations & Open Questions

- **英語中心**: タスク構築・評価パイプラインとも英語情報エコシステムに依存。多言語設定での性能は未検証
- **計算コスト**: Gemini-2.5-Pro と GPT-5-mini への大量API呼び出しが必要であり、リアルタイムや大規模デプロイには制約がある
- **LLM-as-Judge の循環性**: 評価対象（Deep research システム = LLM）を LLM で評価するという循環構造。自己選好バイアスの完全な排除は保証されていない（cross-judge で部分的に緩和を試みている）
- **事実検証の限界**: 80文の人間検証は規模が限定的。Unknown ラベルの扱い（Ratio 計算で「正しくない」側にカウント）が妥当かどうかは議論の余地がある
- **タスク固有次元の品質保証**: LLM が生成するタスク固有次元の妥当性・網羅性について系統的な検証がない
- **オープンソースシステムの欠如**: 評価対象が商用システムのみであり、オープンソース Deep research 実装の比較がない
- **時間的安定性**: データ収集期間（2025年8-11月）が限定的であり、システムのアップデートによる性能変動は考慮されていない

## Connections to Other Work

- **Builds on:** Wei et al. (2024) の長文事実性評価、Wettig et al. (2025) のドメイン分類、MiroFlow (MiroMind, 2025) の agentic フレームワーク
- **Compared with:** DeepResearch Bench (Du et al., 2025), LiveResearchBench (Wang et al., 2025), DRBench (Abaskohi et al., 2025), BrowseComp-Plus (Chen et al., 2025), ReportBench (Li et al., 2025a) 等。Table 1 で包括的に比較し、5つの機能軸全てを満たす唯一のベンチマークと位置づけ
- **Enables:** 動的に更新可能な「ライブベンチマーク」としての運用、タスク適応型評価の標準化、Deep research システムの弱点（タスク固有要件への対応力）の定量化

## Personal Notes

- タスク固有次元でのスコア低下は全システムで一貫しており、現在の Deep research システムが「一般的に良いレポート」は書けるが「タスクの具体的要求」に応えるのが苦手であるという示唆は興味深い。これは prompt engineering やタスク分解の改善余地を示唆している。
- 事実検証の「Wrong よりも Unknown が多い」という発見は、Deep research システムの hallucination が「でっち上げ」よりも「裏付け不十分な推測」の形態をとる傾向を示唆しており、従来の hallucination 研究とは異なる視点を提供する。
- 評価パイプライン自体の計算コスト（frontier モデルへの大量API呼び出し）が、ベンチマークの広範な採用にとってボトルネックになる可能性がある。よりコスト効率の良い評価モデルへの蒸留が今後の課題となりうる。
- Ratio メトリクスにおいて Unknown を「正しくない」側に暗黙的にカウントする設計は、保守的な出力（主張数が少ない）に有利に働く可能性がある。DeepSeek の高 Ratio・低 Statements 数がその例。
