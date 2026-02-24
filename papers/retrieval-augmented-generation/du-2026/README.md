# A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces

**Authors:** Mingxuan Du, Benfeng Xu, Chiwei Zhu, Shaohan Wang, Pengyu Wang, Xiaorui Wang, Zhendong Mao
**Affiliations:** University of Science and Technology of China; Metastone Technology
**Venue:** Preprint (arXiv), February 2026
**Code:** [https://github.com/Ayanami0730/arag](https://github.com/Ayanami0730/arag)

## Summary

本論文は、LLM に階層的な retrieval interface（keyword_search, semantic_search, chunk_read）をツールとして直接公開する Agentic RAG フレームワーク「A-RAG」を提案している。著者らは、既存の RAG 手法が (1) 一括 retrieval + context 結合（Graph RAG）か (2) 事前定義ワークフローの逐次実行（Workflow RAG）のいずれかに依存しており、モデルの推論能力を活用できていないと主張する。A-RAG は3粒度（keyword / sentence / chunk）の retrieval ツールを備え、ReAct ベースの agent loop でモデルが自律的に検索戦略を決定する。著者らの実験では、GPT-5-mini バックボーンで HotpotQA, MuSiQue, 2WikiMultiHopQA, GraphRAG-Bench の全4ベンチマーク（5データセット）で既存手法を上回ったとされる。さらに、単一 embedding ツールのみの Naive variant でも既存手法を上回る結果が報告されており、agentic paradigm 自体の有効性が示唆されている。Test-time compute のスケーリング（ステップ数・推論 effort の増加）により精度が向上することも報告されているが、検証は限定的なサブセットに留まる。

## Files

- [`notes.md`](notes.md) — 読解ノート（Core Thesis, Intellectual Lineage, Key Design Decisions, Methodology Assessment 等）
- [`claims.md`](claims.md) — 主要 claim の詳細分析（6 claims, evidence/methodology/issues/status）
- [`paper.pdf`](paper.pdf) — 論文原本
- [`paper.md`](paper.md) — PDF → Markdown 変換版
