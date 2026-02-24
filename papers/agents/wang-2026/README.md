# DeepResearchEval: An Automated Framework for Deep Research Task Construction and Agentic Evaluation

**Authors:** Yibo Wang, Lei Wang, Yue Deng, Keming Wu, Yao Xiao, Huanjin Yao, Liwei Kang, Hai Ye, Yongcheng Jing, Lidong Bing
**Affiliations:** Infinity Lab (Shanda Group), Nanyang Technological University
**Venue:** Preprint (arXiv), 2026
**Code:** https://github.com/Infinity-AILab/DeepResearchEval

## Summary

本論文は、Deep research システム（OpenAI Deep Research, Gemini Deep Research, Manus 等）の体系的評価のための自動フレームワーク DeepResearchEval を提案する。フレームワークは2つの主要コンポーネントからなる: (1) ペルソナ駆動のタスク自動生成パイプライン（10ドメイン x 50ペルソナから200候補を生成し、二段階フィルタリングと専門家検証を経て100タスクを選定）、(2) agentic 評価パイプライン（固定4次元 + LLM 生成のタスク固有次元による適応型品質評価、および MCP ツールを用いた能動的事実検証）。9つの商用 Deep research システムの900レポートを評価した結果、Gemini-2.5-Pro Deep Research が品質評価でトップ（8.51/10）、Manus が事実正確性でトップ（82.30%）であることを報告している。全システムでタスク固有次元のスコアが固定次元より一貫して低いという発見は、タスク適応型評価の必要性を示唆する。

## Files

- [`notes.md`](notes.md) -- 読解ノート（Core Thesis, Intellectual Lineage, Key Design Decisions, Technical Details 等）
- [`claims.md`](claims.md) -- 主張ごとの詳細分析（証拠の種類・強さ、方法論的懸念、再現性）
- [`paper.pdf`](paper.pdf) -- 原論文 PDF
- [`paper.md`](paper.md) -- PDF から変換した Markdown
