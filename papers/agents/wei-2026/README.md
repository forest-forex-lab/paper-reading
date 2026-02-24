# Agentic Reasoning for Large Language Models

**Authors:** Tianxin Wei, Ting-Wei Li, Zhining Liu, Xuying Ning, Ze Yang, Jiaru Zou, Zhichen Zeng, Ruizhong Qiu, Xiao Lin, Dongqi Fu, Zihao Li, Mengting Ai, Duo Zhou, Wenxuan Bao, Yunzhe Li, Gaotang Li, Cheng Qian, Yu Wang, Xiangru Tang, Yin Xiao, Liri Fang, Hui Liu, Xianfeng Tang, Yuji Zhang, Chi Wang, Jiaxuan You, Heng Ji, Hanghang Tong, Jingrui He

**Venue:** arXiv preprint, 2026

**Affiliations:** University of Illinois Urbana-Champaign, Meta, Amazon, Google DeepMind, UCSD, Yale

**GitHub:** https://github.com/weitianxin/Awesome-Agentic-Reasoning

---

## Summary

本論文は、LLMを受動的な sequence predictor から能動的な autonomous reasoning agent へと再定義する「Agentic Reasoning」パラダイムの包括的サーベイである。著者らは、このパラダイムを3つの環境ダイナミクス層（Foundational: 計画・ツール使用・探索、Self-evolving: フィードバック・記憶・適応、Collective: マルチエージェント協調）と2つの最適化モード（In-context Reasoning: 推論時の orchestration、Post-training Reasoning: RL/SFTによるパラメータ最適化）の直交する分類軸で体系化している。800以上の文献を網羅し、POMDP ベースの形式化の下で既存手法を統一的に位置づけるとともに、5つの応用ドメイン（Math/Code, Science, Robotics, Healthcare, Web）と能力別・応用別のベンチマーク群を整理している。最後に、personalization、long-horizon credit assignment、world models、multi-agent training、latent reasoning、governance の6つの open problem を特定し、今後の研究方向を示している。

---

## Files

- [`notes.md`](notes.md) — 詳細な読解ノート（Core Thesis, Intellectual Lineage, Key Design Decisions, Technical Details 含む）
- [`claims.md`](claims.md) — 主要な主張の claim-by-claim 分析（6 claims, evidence status 付き）
- [`paper.pdf`](paper.pdf) — 原論文 PDF
- [`paper.md`](paper.md) — PDF から変換された Markdown
