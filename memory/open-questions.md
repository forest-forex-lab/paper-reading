# Open Questions

<!-- Format: - YYYY-MM-DD | [OPEN/RESOLVED] | Question | Context/Related papers -->

- 2026-02-23 | [OPEN] | Weis et al. の mixed pool メカニズムは IPD 以外の Social Dilemma（Stag Hunt, Chicken, Public Goods Game）でも協調を誘導するか？ | papers/multi-agent-cooperation/weis-2026/
- 2026-02-23 | [OPEN] | LLM ベースのエージェント（Transformer）で in-context co-player inference による協調は出現するか？GRU から Transformer へのスケーリングの効果は？ | papers/multi-agent-cooperation/weis-2026/
- 2026-02-23 | [OPEN] | A2C の Step 3 不安定性の原因は何か？PPI の安定性は Self-Supervised 訓練・累積データ・パラメータ再初期化のどれに起因するか？ | papers/multi-agent-cooperation/weis-2026/
- 2026-02-23 | [OPEN] | TTD-DR の Diffusion ベース反復改善は、計算コストに見合う品質向上をもたらすか？Denoising 回数と品質のトレードオフの最適点は？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | RL で獲得される Deep Research エージェントの創発的行動（自己反省、クロスバリデーション）は、RLVR の限界（NeurIPS 2025: 推論能力拡張ではなくサンプリング効率向上に留まる）と矛盾しないか？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | Long-Horizon 探索（ASearcher: 100+ターン、400k+トークン）の終了条件をどう設計すべきか？不要な探索を回避しつつ網羅性を確保する制御手法は？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | Deep Research エージェントのレポート品質の統一的評価基準は確立可能か？事実性・引用正確性・構造の論理性・情報網羅性をどう統合するか？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | Tongyi DeepResearch の 3段階訓練（Agentic CPT → SFT → RL）のうち、性能向上への寄与が最も大きいステージはどれか？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | マルチモーダル Deep Research（WebWatcher 的アプローチ）は、テキスト中心のアプローチと比較してどの程度実用的な優位性を持つか？ | surveys/deep-research/
- 2026-02-23 | [OPEN] | Contract-first decomposition は主観的・創造的タスク（デザイン、文章作成等）でも収束するか？「検証可能な粒度」まで分解すると意味のある単位でなくなる可能性の検証が必要 | papers/agents/tomasev-2026/
- 2026-02-23 | [OPEN] | zk-SNARKs + Smart Contract + TEE を統合した delegation システムの計算オーバーヘッドはリアルタイム delegation に許容可能か？proof-of-concept による定量評価が必要 | papers/agents/tomasev-2026/
- 2026-02-23 | [OPEN] | Weis et al. の in-context co-player inference は、Tomašev et al. の Trust Calibration メカニズムの実装として機能しうるか？エージェント間の信頼を interaction history から in-context で推定する可能性 | papers/agents/tomasev-2026/, papers/multi-agent-cooperation/weis-2026/
- 2026-02-24 | [OPEN] | タスク固有評価次元のスコア低下は、システムの弱点を反映しているのか、それとも具体的な次元が本質的に厳しいことの帰結なのか？ | papers/agents/wang-2026/
- 2026-02-24 | [OPEN] | DeepResearchEval の品質評価における自己選好バイアス（Gemini-2.5-Pro が judge かつ被評価者）はどの程度結果に影響しているのか？独立した judge モデルでの再評価が必要 | papers/agents/wang-2026/
- 2026-02-24 | [OPEN] | In-context reasoning と post-training reasoning の最適な組み合わせ方とそのコスト対効果を定量的に評価するベンチマークが存在しない。Wei et al. の taxonomy が実証的に検証可能な形でベンチマーク化できるか？ | papers/agents/wei-2026/
- 2026-02-24 | [OPEN] | Multi-agent collaboration が single-agent を真に超えるのはどのような条件下か？通信コスト・latency 増加とのトレードオフの体系的分析が Wei et al. サーベイでも不足 | papers/agents/wei-2026/
- 2026-02-24 | [OPEN] | Progressive sycophancy と genuine self-correction をどう区別するか？モデルが正しく evidence を評価して回答を修正する行為と、単なる追従を分離する方法論が未確立 | papers/evaluation/fanous-2025/
- 2026-02-24 | [OPEN] | Citation-based rebuttal による regressive sycophancy の最大化は、adversarial attack ベクトルとして悪用可能か？偽の権威的情報源を用いた LLM 操作の実世界リスク評価が必要 | papers/evaluation/fanous-2025/
- 2026-02-24 | [OPEN] | A-RAG の SFT/RL によるツール使用最適化でどの程度の追加改善が得られるか？現状は zero-shot prompting のみで学習ベースの最適化は未実施 | papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | [OPEN] | A-RAG のマルチホップ QA 以外のタスク（fact verification, dialogue, long-form generation）への汎化性は？現状の評価は HotpotQA, 2WikiMHQA, MuSiQue, Bamboogle の4データセットに限定 | papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | [OPEN] | A-RAG の inference token（reasoning token）を含む total token consumption での効率性比較はどうなるか？retrieved token のみの比較では真のコスト優位性は不明 | papers/retrieval-augmented-generation/du-2026/
- 2026-02-24 | [OPEN] | DTR と精度の相関は因果関係を反映しているのか、それとも「難しい予測をするトークンの割合」が問題の難易度と相関しているだけなのか？因果的な介入実験が不在 | papers/evaluation/chen-2026/
- 2026-02-24 | [OPEN] | DTR は数学・科学以外の推論タスク（コード生成、自然言語推論、常識推論）でも有効か？現状は AIME24, MATH500, GPQA 等の STEM タスクに限定 | papers/evaluation/chen-2026/
- 2026-02-24 | [OPEN] | 高い reasoning level で DTR が低下するという観察（Appendix B）の解釈：depth から length への計算再分配は何を意味するのか？ | papers/evaluation/chen-2026/
