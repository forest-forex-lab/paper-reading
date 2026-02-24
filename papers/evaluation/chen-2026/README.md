# Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens

**Authors:** Wei-Lin Chen, Liqian Peng, Tian Tan, Chao Zhao, Blake JianHang Chen, Ziqian Lin, Alec Go, Yu Meng
**Affiliations:** University of Virginia, Google
**Year:** 2026 (preprint)
**Topics:** LLM Evaluation, Reasoning, Test-Time Compute, Mechanistic Interpretability

## Summary

本論文は、LLM の推論努力（inference-time thinking effort）を測定するための新しい指標として deep-thinking ratio (DTR) を提案している。従来、Chain-of-Thought における出力トークン数が推論品質の代理指標として広く使用されてきたが、著者らは長い推論が必ずしも高い精度に結びつかない（overthinking 問題）ことを指摘する。DTR は、各トークン生成時における Transformer の中間 layer の予測分布が最終 layer の分布に収束するまでの深さ（settling depth）を Jensen-Shannon divergence で測定し、深い layer まで予測が改訂され続けるトークン（deep-thinking tokens）の割合として定義される。4 つの数学・科学ベンチマーク（AIME 24/25, HMMT 25, GPQA-Diamond）と 3 つのモデルファミリー（GPT-OSS, DeepSeek-R1, Qwen3）にわたる実験で、DTR がトークン長および confidence ベースの baseline よりもタスク精度と強い正の相関を示すことが報告されている。さらに、DTR を活用した test-time scaling 戦略 Think@n を導入し、DTR が高いサンプルを優先的に選択・集約することで、標準的な Self-Consistency と同等以上の精度を約半分の推論コストで達成すると主張している。

## Files

- [notes.md](notes.md) — 詳細な読解ノート（Core Thesis, Intellectual Lineage, Key Design Decisions, Technical Details を含む）
- [claims.md](claims.md) — Claim-by-claim の分析（6 claims, evidence assessment, status 判定）
- [paper.pdf](paper.pdf) — 原論文 PDF
- [paper.md](paper.md) — PDF から変換された Markdown
