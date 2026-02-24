# SycEval: Evaluating LLM Sycophancy

**Authors:** Aaron Fanous, Jacob Goldberg, Ank Agarwal, Joanna Lin, Anson Zhou, Sonnet Xu, Vasiliki Bikia, Roxana Daneshjou, Sanmi Koyejo
**Venue:** AAAI 2025
**Institution:** Stanford University

## Summary

本論文は、LLM の sycophancy（追従性）を体系的に評価するフレームワーク SycEval を提案する。ChatGPT-4o、Claude-Sonnet、Gemini-1.5-Pro の3モデルを対象に、数学（AMPS）と医療（MedQuad）の2ドメインで評価を実施した。著者らは sycophancy を progressive（正答方向への同調）と regressive（誤答方向への同調）に二分類し、rebuttal の修辞的強度（simple / ethos / justification / citation）と文脈（in-context / preemptive）が sycophancy の方向性に与える影響を分析した。主要な結果として、全体の58.19%で sycophantic behavior が観察され、simple rebuttal が progressive sycophancy を、citation rebuttal が regressive sycophancy を最大化することが示された。また、sycophancy の persistence rate は78.5%と高く、モデル・ドメイン・文脈に依存しないことが報告されている。

## Files

- [`notes.md`](notes.md) — 詳細な読解ノート（手法・設計哲学・知的系譜・結果・限界の分析）
- [`claims.md`](claims.md) — 主要 claim の個別評価（evidence、methodology、potential issues、status）
- [`paper.pdf`](paper.pdf) — 原論文 PDF
- [`paper.md`](paper.md) — Markdown 変換版
