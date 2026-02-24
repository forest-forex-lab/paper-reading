# Multi-agent cooperation through in-context co-player inference

**Weis*, Wołczyk* et al. (2026)** — Google, Paradigms of Intelligence Team / Santa Fe Institute

Sequence Model エージェントを Tabular Agent と他の Learning Agent の混合プール（50/50）で Decentralized MARL 訓練すると、明示的な meta-learning やタイムスケール分離なしに Iterated Prisoner's Dilemma で頑健な協調が出現することを示した論文。多様な相手との対戦が in-context best-response 能力を自然に誘導し、この in-context 適応が従来の "naive learner" の役割を代替する。Extortion への脆弱性 → 相互 extortion → 協調という3段階メカニズムが標準的な RL 訓練から自然に出現する。新手法 Predictive Policy Improvement (PPI) を導入し、その均衡の理論的特性評価も提供。

## Key Details

| Item | Value |
|------|-------|
| **Environment** | Iterated Prisoner's Dilemma (T=100, 2 agents) |
| **Methods** | PPI (new), A2C (baseline) |
| **Architecture** | GRU (128-dim hidden, 32-dim embedding) |
| **Training** | 30 phases (PPI), mixed pool (50% learning + 50% tabular) |
| **Key Result** | Cooperation Rate ~0.85 (PPI), ~0.8 (A2C) in mixed pool |

## Files

- `paper.pdf` — Original PDF
- `paper.md` — Markdown conversion
- `paper-ja.md` — Japanese translation
- `notes.md` — Reading notes
- `claims.md` — Claim-by-claim analysis
- `figures/` — Extracted figures
