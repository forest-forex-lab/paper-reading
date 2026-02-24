![Image](paper_artifacts/image_000000_73ceca6f21f2685db190ec1d8849c1bbc340a27392bfca88d03fb7f3e6a453da.png)

## Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens

Wei-Lin Chen 1,2* , Liqian Peng 2 , Tian Tan 2 , Chao Zhao 2 , Blake JianHang Chen 2 , Ziqian Lin 2 , Alec Go 2 and Yu Meng 1

1 University of Virginia, 2 Google, * Work done as a student researcher at Google.

Large language models (LLMs) は、長い Chain-of-Thought (CoT) によってテスト時の計算量をスケーリングすることで、印象的な推論能力を示してきた。しかし、最近の知見では、トークン数の生の値は推論品質の信頼できる代理指標ではないことが示唆されており、生成長の増加は精度と一貫した相関を示さず、むしろ「過剰思考（overthinking）」を示すシグナルとなり、性能低下を招く可能性がある。本研究では、深層モデル層において内部予測が収束前に大幅に修正されるトークン——deep-thinking tokens——を特定することで、推論時の努力量を定量化する。4つの難解な数学・科学ベンチマーク（AIME 24/25、HMMT 25、GPQA-diamond）および推論特化型モデルの多様なセット（GPT-OSS、DeepSeek-R1、Qwen3）において、deep-thinking ratio（生成系列中の deep-thinking tokens の割合）が精度と頑健かつ一貫した正の相関を示し、長さベースおよび信頼度ベースのベースラインを大幅に上回ることを示す。この知見を活用し、high deep-thinking ratio を持つサンプルを優先する Test-time scaling 戦略 Think@$n$ を導入する。Think@$n$ は、短い接頭辞に基づいて有望でない生成を早期に棄却することで推論コストを大幅に削減しながら、標準的な self-consistency の性能と同等またはそれ以上を達成することを示す。

図1 | 精度と思考努力の代理指標との相関の比較。このプロットは、AIME 2024/2025、HMMT 2025、GPQA-Diamond における GPT-OSS-120Bmedium のモデル性能と2つの推論時思考努力指標との関係を示している。（左）出力トークン数は中程度の負の相関（平均 $r = -0.544$）を示しており、出力長が性能の信頼できる指標ではないことを示唆している。（右）これに対し、我々が提案する deep-thinking ratio は精度と強い正の相関（平均 $r = 0.828$）を示す。

![Image](paper_artifacts/image_000001_e28dc8bd826444a3a4595b5cfe630c9f4d49742327855ccd850cc75e7369d7d2.png)

## 1. Introduction

Large language models (LLMs) は、明示的な思考過程を生成することで、特に Chain-of-Thought (CoT) パラダイム（Wei et al., 2022）を通じて、顕著な推論能力を達成してきた。先行研究では、生成する推論トークン数を増やすことで一般にタスク性能が向上することが示されており（Anthropic, 2025a,b; Guo et al., 2025; Jaech et al., 2024; OpenAI, 2025; Team et al., 2025; Yang et al., 2025; Zhong et al., 2024）、より長く精緻な思考トレースを促す手法の研究が動機付けられてきた（Balachandran et al., 2025; Muennighoff et al., 2025; Yeo et al., 2025）。

しかし、増加する証拠は、トークン数が推論中のモデル性能の信頼できる指標ではないことを示唆しており、推論が長くなっても精度が一貫して向上するわけではない（Aggarwal et al., 2025; Su et al., 2025; Sui et al., 2025; Wu et al., 2025）。実証研究では、CoT 長と性能の間に逆U字型の関係が明らかになっており（Wu et al., 2025）、推論トレースが長くなるほど性能が系統的に低下するという逆スケーリング挙動も観察されている（Gema et al., 2025）。過度な推論は過剰思考（overthinking）を反映することがあり、モデルが欠陥のあるヒューリスティクスを増幅させたり無関係な詳細に固執したりする（Feng et al., 2025）。したがって、推論品質の指標として長さに依拠することは、明確さよりも冗長性を促すだけでなく、情報を持たないトークンに対して計算資源を無駄にする。最近の研究では CoT の意味的構造を評価しようとする試みもある（例えば、推論トレースをグラフとして表現する）が、そのようなアプローチはしばしばコストのかかる補助的な解析や外部アノテーションに依存する（Feng et al., 2025）。これらの限界に対処するには、効果的な推論を情報を持たない生成から区別できる、より原理的かつ効率的な思考努力測定手法が必要である。

本研究では、推論時の思考努力の直接的な指標として deep-thinking ratio (DTR) を導入する。出力長のような表面的な特徴に依存する代わりに、個々のトークンが内部でどのように生成されるかに注目する。あるトークンの予測が早い層で安定化する場合、その後の深さ方向の修正は相対的に低い計算的努力を伴い、より少ない思考に類似していると仮定する。対照的に、収束前に深い層まで持続的な修正を受けるトークン予測は、より大きな思考を反映する（Chuang et al., 2023）。この考えを、中間層の隠れ状態を語彙空間に射影し、各層の予測分布を最終層の分布と比較することで具体化する。分布が深い層まで収束しないトークンを deep-thinking tokens と特定する。生成系列中の deep-thinking tokens の割合を計算することで DTR を得る。これはタスク固有のヒューリスティクスも外部の構造的アノテーションも必要としない、シンプルで機構的に根拠のある思考努力の指標を提供する。

4つの難解な数学・科学推論ベンチマーク——AIME 2024、AIME 2025、HMMT 2025、GPQA（Art of Problem Solving, 2024a,b, 2025a,b; HMMT, 2025; Rein et al., 2024）——および GPT-OSS、DeepSeek-R1、Qwen3 ファミリー（Guo et al., 2025; OpenAI et al., 2025; Yang et al., 2025）を含む多様な推論特化型言語モデルにわたって、deep-thinking tokens の測定がタスク精度との強い相関をもたらすことを示す。達成された相関は、長さベースまたは信頼度ベースのベースラインを用いた場合よりも実質的に高い。さらに、deep-thinking tokens を並列推論スケーリングに活用できることを示す。より高い DTR を持つ応答を優先的に選択・集約することで、計算コストを半分に削減しながら、標準的なコンセンサスベースの手法と同等またはそれ以上の性能を達成できる。我々の貢献を以下にまとめる：

- deep-thinking ratio (DTR)——収束前に深い層まで持続的な修正を受けるトークンの割合を測定する指標——を、推論時の思考努力を特徴づける新たな視点として導入する。
- 複数の推論ベンチマークおよびモデルファミリーにわたって、生成系列の DTR がタスク精度と強い正の相関を示し、長さベースおよび信頼度ベースのベースラインを大幅に上回ることを実証的に示す。

- &amp;8

- 18

- 62

- L7

- 9Z

- 87

- 17.

- 61

- LI

- ST

- ST

- II

- 6

- L

- 9.

- 8

- 1|

pue і

8

all Et

S!

Et (

S!

0

'0 -

![Image](paper_artifacts/image_000002_449b10fb120542affe589ced057bff1e837bb2e8fa1c7b1c81acaef1259eb1e5.png)

0.0

図2 | 思考のヒートマップ：GPT-OSS-120Bhigh の回答系列において、最終層（第36層）と中間層の分布間の Jensen-Shannon divergence (JSD) 値をプロットしている。機能語・定型語（例：'and'、'is'、'boxed'、'`<| return |>`'）は比較的浅い層で収束することが多い。演算子の後に続く記号（例：'+'、'='）や回答トークン・記号（例：'13'、'(D)'）は深い層まで安定しない。興味深いことに、回答トークン '13' は最初に出現した後、より早い層で徐々に現れるようになる。

- Think@$n$——DTR が高いサンプルを優先的に選択・集約する Test-time scaling 戦略——を導入する。短い接頭辞から推定される DTR に基づいて有望でない生成を早期に停止することで、Think@$n$ は推論コストを約半分に削減しながら、標準的な self-consistency と同等またはそれ以上の性能を達成する。

## 2. Measuring Deep-Thinking Ratio

## 2.1. Preliminaries

$L$ 個の Transformer 層、隠れ次元 $d$、語彙 $V$ から構成される自己回帰言語モデル $f_\theta$ を考える。接頭辞系列 $y_{<t}$ が与えられると、生成ステップ $t$ における順伝播は残差ストリーム状態の系列 $\{h_{t,l}\}_{l=1}^L$ を生成し、$h_{t,l} \in \mathbb{R}^d$ は層 $l$ 後の隠れ状態を表す。最終層の出力 $h_{t,L}$ は言語モデリングヘッド（すなわち、unembedding 行列）$W_U \in \mathbb{R}^{|V| \times d}$ によって射影され、語彙上のロジットを生成する。

Early exiting に関する先行研究（Belrose et al., 2023; Din et al., 2024; Elbayad et al., 2019; Schuster et al., 2022; Teerapittayanon et al., 2016）は、専門的な補助訓練なしに言語モデリングヘッドを中間層の隠れ状態に直接適用することで効果的に意味のある予測分布が得られることを示してきた（Kao et al., 2020; Nostalgebraist, 2020）。この研究系統を踏まえ、同じ unembedding 行列 $W_U$ を用いて中間層の隠れ状態を語彙空間に射影する。各中間層 $l \in \{1, \ldots, L-1\}$ について、ロジットベクトル $z_{t,l}$ と確率分布 $p_{t,l}$ を以下のように計算する：

<!-- formula-not-decoded -->

モデルの最終層の分布を $p_{t,L}$ と表す。

図3 | deep-thinking tokens を特定する手法の図解。10層のモデルを想定し、depth fraction $\rho = 0.8$ を設定した場合、生成ステップ $t$ のトークンは、最終層の分布との JSD が閾値 $g$ を下回るのが late-settling regime に達するまでであるため、deep-thinking token として正常に分類される。

![Image](paper_artifacts/image_000003_2bd5a692dc805ff63288784785d1aad311543a651552a8d62dcb087026d09c52.png)

## 2.2. Deep-Thinking Tokens

推論時の思考努力がトークンにとって、LM 層をまたいで予測分布（すなわち $p_{t,l}$）が継続的に進化するという形で現れると仮定する。分布的安定化が早いトークンは追加思考が少ないことに対応し、安定化が遅いトークンはより拡張された内部思考を必要とすることに対応する。言い換えれば、単純なトークンは浅い計算で早期に安定し、より多くの思考を必要とする困難なトークンは深い層でより多くの計算で分布的シフトを示す。これを説明するために、Figure 2 に GPQA（Rein et al., 2024）の質問への回答についての動機付け例を示す。

この挙動を定量化するために、トークンの予測分布が安定する前にどのくらい変化し続けるかを測定する。これは、中間の分布が最終層の分布に十分近くなる層として具体化される。具体的に、各生成ステップ $t$ と層 $l$ について、中間層の分布 $p_{t,l}$ と最終層の分布 $p_{t,L}$ の間の Jensen-Shannon divergence (JSD) を計算する：

<!-- formula-not-decoded -->

ここで $H(\cdot)$ は Shannon entropy を表す。構成上、$D_{t,L} = 0$ である。ゼロに近づくのが遅い層においてのみとなる軌道 $l \mapsto D_{t,l}$ は、長引く分布的修正（より多く考える）を示し、一方で早期収束はモデルがより少ない後続の更新で最終予測に落ち着くことを示す（より少なく考える）。JSD はその対称性と有界性のため採用しており、(Chuang et al., 2023) に従っている。Section A において他の距離指標を探索する。

## Algorithm 1: Computing DeepThinking Ratio (DTR)

```
Input : Autoregressive LM 𝑓 𝜃 with 𝐿 layers and unembedding matrix 𝑊𝑈 ; Input prompt 𝑥 ; Threshold 𝑔 ; Depth fraction 𝜌 Output: DTR ( 𝑆 ) of the generated sequence 𝑆 𝐶 ← 0; // deep thinking token count 𝑆 ←∅ ; // generated sequence 𝑦 𝑡 ← [ BOS ] ; // initialize with start token while 𝑦 𝑡 ≠ [ EOS ] do Sample 𝑦 𝑡 ∼ 𝑝𝑡,𝐿 ( 𝑓 𝜃 (· | 𝑥, 𝑆 )) ; 𝑆 ←( 𝑆, 𝑦 𝑡 ) ; for 𝑙 ← 1 to 𝐿 do 𝑝𝑡,𝑙 ← softmax ( 𝑊𝑈ℎ𝑡,𝑙 ) ; 𝐷𝑡,𝑙 ← JSD ( 𝑝𝑡,𝐿 , 𝑝 𝑡,𝑙 ) ; end 𝑐 𝑡 ← min { 𝑙 : min 𝑗 ≤ 𝑙 𝐷𝑡,𝑗 ≤ 𝑔 } ; if 𝑐 𝑡 ≥ ⌈( 1 -𝜌 ) 𝐿 ⌉ then 𝐶 ← 𝐶 + 1; end end return 𝐶 /| 𝑆 | ;
```

安定化の厳密な概念を強制するために、以下を計算する：

<!-- formula-not-decoded -->

settling depth $c_t$ を、$\bar{D}_{t,l}$ が固定閾値 $g$ を下回る最初の層として定義する：

<!-- formula-not-decoded -->

次に、depth fraction $\rho \in (0, 1)$ を用いて deep-thinking regime を定義する：

<!-- formula-not-decoded -->

トークンが deep-thinking token（すなわち、最終層の分布に十分近くなるまでより多くの層計算とより多くの思考努力を必要とする）として分類されるのは、$c_t \in \mathcal{L}_{\text{deep-thinking}}$ の場合である。図3 に図解を示す。

最後に、長さ $T$ の生成系列 $S$ について、系列の deep-thinking ratio DTR$(S)$ を、late regime で安定するトークンの割合として定義する：

<!-- formula-not-decoded -->

より高い DTR は、安定化前により多くのトークンが分布的修正のために拡張された計算を行うことを示す。提案手法は、早期安定化トークンが最適でないことを意味するのではなく、むしろ推論時の思考努力の深さ方向の特性評価を提供し、表面的なトークン長の指標を補完するものである。DTR の全体的なアルゴリズムを Algorithm 1 に示す。また、Section E において定性的な例を提供する。

## 3. Deep-Thinking Ratio Reflects Task Accuracy More Reliably

著者らは、分布的距離に基づく測定が、表面的な長さベースの代理指標（すなわちトークン数）よりも、推論時の思考努力の忠実でより頑健な特性評価を提供するかどうかを実験的に評価する。

**Models.** 3つのモデルファミリーから8つの変種の推論 LLM を評価する：GPT-OSS-20B（low、medium、high の推論レベル）と GPT-OSS-120B（low、medium、high の推論レベル）（OpenAI et al., 2025）、DeepSeek-R1-70B（Guo et al., 2025）、1 および Qwen3-30B-Thinking（Yang et al., 2025）。これらのモデルは数学的・複雑な推論における強力な長い CoT 能力で知られており、包括的なカバレッジのために複数のパラメータスケールにまたがっている。

**Tasks.** CoT スタイルの推論時計算のスケーリングが中心的な役割を果たす推論集約型ベンチマークに焦点を当てる。最近の LLM 推論能力の評価で広く使用されている4つのベンチマーク（Balunović et al., 2025; OpenAI, 2025; xAI, 2025）を採用する。競技レベルの数学問題セット3種——AIME 2024（Art of Problem Solving, 2024a,b）、AIME 2025（Art of Problem Solving, 2025a,b）、HMMT 2025（HMMT, 2025）——および難解な大学院レベルの科学的問題から構成される GPQA（Rein et al., 2024）の diamond セットを含む。

1 簡潔のため、DeepSeek-R1-70B は DeepSeek-R1 が生成したサンプルで蒸留された Llama-3.3-70B-Instruct を指す（https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B）。

**Decoding settings.** （Gema et al., 2025）に従い、推論バジェットを指定したり明示的に長い熟慮を促したりすることなく、固定された中立的な指示を用いてモデルにステップごとの推論を行うよう促す。この設定により、各モデルはインスタンスごとに推論時計算を自然に割り当てることができ、外部から課されるトークンバジェットやバジェット条件付きプロンプトによる交絡を回避する。自然な過剰思考分析の標準的な慣行（Gema et al., 2025）に従い、各質問に対して複数の応答をサンプリングする（実験では質問ごとに25応答）。これらのサンプルにわたって、モデルは自然に推論長と内部計算パターンのバリエーションを示す。テスト済みの全モデルについて開発者推奨のサンプリングパラメータを使用する：GPT-OSS シリーズには temperature=1.0 および top p=1.0；DeepSeek-R1-70B および Qwen-3-30B-Thinking には temperature=0.6 および top p=0.95。

各サンプリング応答について、中間層の隠れ状態を記録し、射影された確率分布を取得し、Section 2 で述べた DTR を計算する。settling 閾値 $g = 0.5$ と depth fraction $\rho = 0.85$ を一様に設定して deep-thinking regime を定義する。異なる値での分析も行い、結果は Section 3.2 に提供する。報告される統計量は、デコーディング実行における30のランダムシードの平均値である。

## 3.1. Results

推論時の思考努力とタスク性能の関係を定量化するために、Pearson 相関係数を計算することで思考努力スコアと回答精度の関連を測定する。具体的に、（Gema et al., 2025）に従ったビン分析を実施し、DTR（式(6)）に基づいてサンプリングされた系列を分位数ビン（すなわち5ビン）に分割し、各ビン内の平均精度を計算する。

deep-thinking token の測定を、長さベースの代理指標や信頼度ベースのアプローチを含む以下のベースラインと比較する。これらも生成品質の評価によく採用されている。

**Token count.** モデルの出力推論トレースで生成されたトークンの総数。この指標はテスト時計算の直接的な代理指標として広く位置づけられており、推論時スケーリングの多くの実証研究の基礎となっている（Anthropic, 2025a,b; Guo et al., 2025; Jaech et al., 2024; OpenAI, 2025; Team et al., 2025; Yang et al., 2025; Zhong et al., 2024）。

**Reverse token count.** 補完的なベースラインとして、各応答の生成トークン総数の負の値として定義される reverse token count も考慮する。この変換は、LLM の過剰思考において推論長と精度の間に頻繁に観察される逆の関係を考慮するために含まれる（Gema et al., 2025; Wu et al., 2025）。

**Log probability.** Section 2 の表記に従い、生成系列 $S = (y_1, \ldots, y_T)$ とする。生成ステップ $t$ において、語彙 V 上のモデルの出力予測分布（最終層 $L$ における）を $p_{t,L}(\cdot)$ と表す。サンプリングされたトークンの平均対数確率を計算する：

<!-- formula-not-decoded -->

より高い値は、モデルが自身の生成に対してより高い尤度を割り当てることを示し、より高い信頼度として一般的に解釈される。

表1 | タスク精度と異なる推論時指標（長さベースおよび信頼度ベースのベースラインを含む）の Pearson 相関。8つのモデル変種と4つの推論ベンチマークにわたる相関値を色分けで示す：強い正の相関（$0.5 \sim 1$）は濃い緑、弱い正の相関（$0 \sim 0.5$）は薄い緑、弱い負の相関（$-0.5 \sim 0$）は薄いオレンジ、強い負の相関（$-1 \sim -0.5$）は濃いオレンジで示す。

|                    | Token Length   | Reverse To- ken Length   | Log Proba- bility   | Negative Perplexity   | Negative Entropy   | Self- Certainty   | DTR (Ours)   |
|--------------------|----------------|--------------------------|---------------------|-----------------------|--------------------|-------------------|--------------|
|                    | AIME 2025      | AIME 2025                | AIME 2025           | AIME 2025             | AIME 2025          | AIME 2025         | AIME 2025    |
| OSS-120B-low       | 0.504          | -0.504                   | 0.872               | 0.453                 | 0.863              | 0.803             | 0.930        |
| OSS-120B-medium    | -0.365         | 0.365                    | 0.817               | 0.246                 | 0.822              | 0.815             | 0.862        |
| OSS-120B-high      | -0.961         | 0.961                    | 0.705               | 0.552                 | 0.711              | 0.728             | 0.796        |
| OSS-20B-low        | -0.689         | 0.689                    | 0.579               | 0.849                 | 0.665              | 0.275             | 0.373        |
| OSS-20B-medium     | -0.757         | 0.757                    | 0.616               | -0.677                | 0.637              | 0.097             | 0.161        |
| OSS-20B-high       | -0.385         | 0.385                    | 0.455               | -0.795                | 0.550              | 0.489             | 0.610        |
| DeepSeek-R1-70B    | -0.973         | 0.973                    | 0.961               | 0.955                 | 0.946              | 0.899             | 0.974        |
| Qwen3-30B-Thinking | -0.663         | 0.663                    | -0.008              | -0.035                | 0.154              | 0.828             | 0.855        |
|                    | AIME 2024      | AIME 2024                | AIME 2024           | AIME 2024             | AIME 2024          | AIME 2024         | AIME 2024    |
| OSS-120B-low       | -0.166         | 0.166                    | 0.897               | 0.682                 | 0.869              | 0.741             | 0.840        |
| OSS-120B-medium    | -0.680         | 0.680                    | 0.795               | -0.293                | 0.908              | 0.924             | 0.533        |
| OSS-120B-high      | -0.755         | 0.755                    | 0.700               | -0.275                | 0.593              | 0.654             | 0.905        |
| OSS-20B-low        | -0.655         | 0.655                    | 0.548               | -0.342                | 0.667              | 0.584             | 0.730        |
| OSS-20B-medium     | -0.827         | 0.827                    | 0.195               | -0.150                | 0.440              | 0.252             | -0.192       |
| OSS-20B-high       | -0.989         | 0.989                    | 0.809               | 0.262                 | 0.921              | 0.855             | 0.824        |
| DeepSeek-R1-70B    | -0.987         | 0.987                    | -0.037              | 0.223                 | 0.067              | 0.287             | 0.430        |
| Qwen3-30B-Thinking | -0.869         | 0.869                    | -0.857              | -0.720                | -0.680             | -0.246            | -0.657       |
|                    | GPQA-Diamond   | GPQA-Diamond             | GPQA-Diamond        | GPQA-Diamond          | GPQA-Diamond       | GPQA-Diamond      | GPQA-Diamond |
| OSS-120B-low       | 0.682          | -0.682                   | 0.984               | 0.172                 | 0.995              | 0.996             | 0.976        |
| OSS-120B-medium    | -0.340         | 0.340                    | 0.973               | 0.316                 | 0.985              | 0.981             | 0.823        |
| OSS-120B-high      | -0.970         | 0.970                    | 0.854               | 0.501                 | 0.813              | 0.885             | 0.845        |
| OSS-20B-low        | -0.602         | 0.602                    | 0.984               | 0.235                 | 0.991              | 0.917             | 0.935        |
| OSS-20B-medium     | -0.847         | 0.847                    | 0.914               | 0.468                 | 0.911              | 0.889             | 0.718        |
| OSS-20B-high       | -0.794         | 0.794                    | 0.879               | 0.461                 | 0.902              | 0.915             | 0.992        |
| DeepSeek-R1-70B    | -0.930         | 0.930                    | 0.068               | -0.133                | -0.165             | -0.532            | 0.885        |
| Qwen3-30B-Thinking | -0.634         | 0.634                    | 0.589               | 0.865                 | 0.711              | 0.943             | 0.828        |
|                    | HMMT 2025      | HMMT 2025                | HMMT 2025           | HMMT 2025             | HMMT 2025          | HMMT 2025         | HMMT 2025    |
| OSS-120B-low       | 0.871          | -0.871                   | 0.761               | 0.629                 | 0.695              | 0.884             | 0.305        |
| OSS-120B-medium    | -0.793         | 0.793                    | 0.706               | 0.045                 | 0.618              | 0.631             | 0.926        |
| OSS-120B-high      | -0.967         | 0.967                    | 0.750               | 0.503                 | 0.728              | 0.754             | 0.972        |
| OSS-20B-low        | -0.634         | 0.634                    | -0.695              | 0.549                 | -0.359             | -0.489            | 0.689        |
| OSS-20B-medium     | -0.668         | 0.668                    | 0.447               | 0.336                 | 0.424              | 0.331             | 0.247        |
| OSS-20B-high       | -0.352         | 0.352                    | 0.537               | 0.994                 | 0.831              | 0.628             | 0.932        |
| DeepSeek-R1-70B    | -0.866         | 0.866                    | 0.879               | 0.889                 | 0.858              | 0.905             | 0.902        |
| Qwen3-30B-Thinking | -0.950         | 0.950                    | -0.803              | -0.762                | -0.801             | 0.745             | 0.911        |
| Average            | -0.594         | 0.594                    | 0.527               | 0.219                 | 0.571              | 0.605             | 0.683        |

**Negative perplexity.** Perplexity は指数化された負の平均対数確率として定義される：

<!-- formula-not-decoded -->

より大きな値がより高い信頼度に対応するように、negative perplexity $-\text{PPL}(S)$ を報告する。

**Negative entropy.** サンプリングされたトークンのみでなく V 上の完全な予測分布からの情報を組み込むために、平均 entropy を計算する：

<!-- formula-not-decoded -->

より大きな値がより尖った分布、したがってより高いモデル信頼度を示すように、negative entropy $-\text{Ent}(S)$ を報告する。

**Self-Certainty.** Self-Certainty（Kang et al., 2025）も含める。これは、より高い信頼度が最大不確実性を表す一様分布 $u$ から遠い予測分布に対応するという考えに基づく分布的信頼度指標である。形式的に、self-certainty は $u(v) = 1/|\mathcal{V}|$ と $p_{t,L}$ の間の平均 Kullback-Leibler (KL) divergence として定義される：

<!-- formula-not-decoded -->

全てのベースラインについて、相関はトークン数（またはその否定）や信頼度スコアによって系列をランク付けしてビン分けする同じプロトコルを用いて計算される。

表1 は、8つのモデル変種と4つのベンチマークにわたるタスク精度と異なる測定値の相関を報告する。観察されるように、トークン数による系列の測定は顕著なオレンジ色の値（$r < 0$）を示し、平均 $r = -0.59$ となる。これは、生成が長くなるほど性能が低くなる傾向があることを示しており、逆スケーリングと過剰思考に関する最近の報告と一致している。推論トレースの延長は、冗長で誤った方向に向かう、あるいはエラーを増幅させる熟慮の症状である可能性がある。結果は、効果的な問題解決の代理指標として表面的な長さの特徴を使用することの信頼性のなさを強調している。トークン数を反転させると同じ大きさの正の相関が得られる。しかし、この改善は純粋に事後的なものであり、より短い応答がより正確である体制での経験的規則性を反映している。したがって、reverse token count は統計的調整としてのみ機能し、計算や思考努力の原理的な概念を捉えるものではない。

トークン数の測定と比較して、信頼度ベースの指標（log probability、negative perplexity、negative entropy、self-certainty）は平均 $r = 0.219 \sim 0.605$ の適度に正の相関を示し、緑色の値が優勢であることで反映されている。これはモデルの信頼度が正確性に関する部分的な情報を捉えることを示している。しかし、それらの挙動はモデルやベンチマークによって比較的不均質である：特定の設定では強い正の相関が達成されるが、他では弱いまたは負の関連性にまで悪化する。この不一致は、信頼度シグナルが過信などの他の要因と混同されている可能性があり、したがって推論時計算の努力や問題解決の有効性を確実に反映するものではないことを示唆している。

対照的に、我々が提案する DTR の測定はタスク性能との最も強く安定した関係を示し、$r = 0.683$ の最高平均相関を達成し、信頼度ベースのアプローチの中で最もパフォーマンスの高いベースラインである reverse token count および Self-Certainty を上回る。全体として、DTR はモデルやベンチマークにわたって正を保ち、オレンジ色の値が最も少ない（テスト済みの32のモデル-ベンチマーク設定のうち2つ）。総じて、結果は出力系列に対して DTR を計算することが、トークン量のみや信頼度ベースの代替手段よりも、成功した推論結果のより忠実でより頑健な特性評価を提供することを示している。

## 3.2. Settling Threshold と Depth Fraction の影響

2つの主要なハイパーパラメータ、すなわち settling threshold $g$ と late-settling depth fraction $\rho$ が、測定される思考努力量およびタスク性能との相関にどのような影響を与えるかを分析する。図4は、様々な思考努力量（すなわち、平均

Accuracy (Pass@1)

0

0

0

0

0

.

.

.

.

.

700

675

650

625

600

r

= 0.820

0

.

24

r

= 0.962

0

.

32

0

.

40

Deep-Thinking Ratio

(a) settling threshold $g$ の異なる値による影響

![Image](paper_artifacts/image_000004_8f27ce42e9aaf57b346560b6c42537057134d8b0e557221bb3a837cfef4d145a.png)

(b) depth fraction $\rho$ の異なる値による影響

図4 | ハイパーパラメータが思考努力量の測定と精度プロファイルに与える影響。settling threshold $g$ と depth fraction $\rho$ をスイープすることでハイパーパラメータの影響を分析する。(a) $g$ の変動は相関により大きな影響を与える。permissive な threshold（$g = 0.25$）はよりフラットなトレンドをもたらすのに対し、$g = 0.5$ は最も頑健な正のシグナルを提供する。(b) $\rho$ の変動は思考努力スコアの範囲を変化させるが、全体的に一貫した正の傾きを維持する。全体として、より厳格な基準（高い $g$、低い $\rho$）は DTR の範囲を縮小させ、$( g, \rho ) = ( 0.5, 0.85 )$ が安定性と相関のバランスとして理想的である。

late-settling token ratio）に渡る精度プロファイルを示しており、$g \in \{ 0.25, 0.5, 0.75 \}$ および $\rho \in \{ 0.8, 0.85, 0.9, 0.95 \}$ から導出されている。$g$ をスイープする際は $\rho$ を 0.85 に固定し、$\rho$ をスイープする際は $g$ を 0.5 に固定する。結果は reasoning level high の GPT-OSS-20B を用いた GPQA-D で報告する。

以下の観察を結論とする：(1) 測定されるシーケンスレベルの思考努力量の大きさは、これらのパラメータの厳格さに直接影響される。具体的には、図4aと図4bの両方が示すように、より厳格な基準の適用、すなわち settling threshold $g$ を高く設定するか depth fraction $\rho$ を低く設定することで、平均 late-settling token ratio が低下することがわかる。これは機械論的に一貫している。高い $g$ は、中間状態が late regime の深いレイヤーに到達するまで最終出力と分布的に大きく乖離していることを要求する；一方、低い $\rho$ は late regime の定義をより深いレイヤーの狭い範囲に限定する。いずれの条件も自然と候補をより多く除外し、late-settling と分類されるトークンが少なくなり、結果として全体的な思考努力スコアの範囲が低下する。

- (2) settling threshold $g$ は、depth fraction $\rho$ よりも思考努力量と精度の相関に対してより顕著な影響を持つ。図4bに示すように、$\rho$ の変動は厳格さの違いにより late-settling ratio の範囲を変化させるが、全設定において一貫した正の傾きを維持しており、このメトリクスが late layer の具体的な定義に対して比較的頑健であることを示している。対照的に、図4aは $g$ の選択が測定結果に対してより大きな影響を持つことを示している：$g = 0.25$ のソフトな threshold はより低い相関値でフラットなトレンドをもたらし、これが過度に permissive であり、計算努力の少ないトークンを含めることで測定の高品質な軌道を識別する能力を低下させる可能性を示唆している。逆に、$g = 0.5$ および $g = 0.75$ の threshold は精度を反映するより頑健な正の相関を示す。
- (3) 全体として、基準が過度に制限的（$g = 0.75$ および $\rho \in \{ 0.9, 0.95 \}$）な場合、トレンドは正の相関を維持しているものの、情報量の多い高計算トークンの潜在的なフィルタリングにより若干不安定になる可能性がある。テストされた設定の中で、$( g, \rho ) = ( 0.5, 0.85 )$ は理想的なバランスを達成し、高い相関値を持つ信頼性の高いトレンドをもたらす。

threshold threshold

threshold

g

g

g

=2.5e-01

=5.0e-01

=7.5e-01

r

= 0.012

0

.

48

表2 | 4つの reasoning ベンチマークにおける異なる aggregation 手法での、タスク精度と平均推論コスト（k トークン）の比較。報告されるコスト削減（$\Delta$%）は Cons@$n$ に対する相対値で示す。Think@$n$ は最良の全体性能を達成しつつ、推論コストを約 50% 削減する。† のついた手法は early stopping の判断に prefix 長 50 を採用する。

| 手法                  | AIME 25           | AIME 25           | AIME 24           | AIME 24           | HMMT 25           | HMMT 25           | GPQA-D            | GPQA-D            |
|-----------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
|                       | Acc               | Cost ( $\Delta$ %) | Acc               | Cost ( $\Delta$ %) | Acc               | Cost ( $\Delta$ %) | Acc               | Cost ( $\Delta$ %) |
|                       | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   |
| Cons@$n$              | 92.7              | 307.6 (-)         | 92.7              | 235.1 (-)         | 80.0              | 355.6 (-)         | 73.8              | 93.5 (-)          |
| Mean@$n$              | 80.0              | 307.6 (-)         | 81.6              | 235.1 (-)         | 62.6              | 355.6 (-)         | 69.9              | 93.5 (-)          |
| Long@$n$              | 86.7              | 307.6 (-)         | 86.7              | 235.1 (-)         | 73.3              | 355.6 (-)         | 73.2              | 93.5 (-)          |
| Short@$n$             | 87.3              | 255.7 (-17%)      | 88.0              | 200.9 (-15%)      | 77.3              | 290.4 (-18%)      | 73.3              | 84.4 (-10%)       |
| Self-Certainty@$n$ †  | 87.3              | 150.6 (-51%)      | 91.3              | 119.3 (-49%)      | 78.0              | 177.0 (-50%)      | 76.0              | 47.9 (-49%)       |
| Think@$n$ †           | 94.7              | 155.4 (-49%)      | 93.3              | 121.3 (-48%)      | 80.0              | 181.9 (-49%)      | 74.7              | 48.8 (-48%)       |
|                       | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking |
| Cons@$n$              | 86.7              | 1073.1 (-)        | 93.3              | 950.1 (-)         | 63.3              | 1275.7 (-)        | 67.8              | 410.6 (-)         |
| Mean@$n$              | 81.2              | 1073.1 (-)        | 86.3              | 950.1 (-)         | 55.7              | 1275.7 (-)        | 66.9              | 410.6 (-)         |
| Long@$n$              | 85.3              | 1073.1 (-)        | 86.7              | 950.1 (-)         | 52.7              | 1275.7 (-)        | 66.7              | 410.6 (-)         |
| Short@$n$             | 90.0              | 983.6 (-8%)       | 90.0              | 871.0 (-8%)       | 63.3              | 1165.7 (-9%)      | 68.2              | 382.9 (-7%)       |
| Self-Certainty@$n$ †  | 86.7              | 548.9 (-49%)      | 90.0              | 480.9 (-49%)      | 63.3              | 641.4 (-50%)      | 68.2              | 206.6 (-50%)      |
| Think@$n$ †           | 90.0              | 537.5 (-50%)      | 93.3              | 482.2 (-49%)      | 66.7              | 641.4 (-50%)      | 69.7              | 206.8 (-50%)      |

## 4. Deep-Thinking Tokens による効率的な Test-Time Scaling の実現

反復サンプリング（repeated sampling）は、長い CoT の生成と並行して Test-Time Compute をスケールするための一般的な戦略である（Brown et al., 2024; Gupta and Srikumar, 2025; Saad-Falcon et al., 2024, 2025; Stroebl et al., 2024）。推論予算の増大を代償に、問題ごとに独立して生成された複数のサンプルを集約することで精度を向上させる。本セクションでは、提案する DTR 指標を活用して、より高品質なサンプルを優先的に選択・集約し、より良い性能を達成できるかどうかを検討する。

実験設定。本研究では、最近の Test-Time Scaling 研究で一般的に採用される best-of-n (BoN) 評価プロトコルに従う（Fu et al., 2025）。各問題に対して、同一のデコーディング設定で $n$ 個の応答をサンプリングし、以下の aggregation 手法を比較する：Cons@$n$：標準的な self-consistency（Wang et al., 2023）であり、$n$ 個のサンプリングされた応答全体に対して多数決を行う；Mean@$n$：$n$ 個のサンプル全体の平均精度であり、優先的な集約を行わないベースラインを反映する；Long@$n$ および Short@$n$：トークン数で順位付けされた $n$ 個のサンプルのうち、最長/最短の $\eta$ パーセントに対して多数決を行う（Agarwal et al., 2025; Hassid et al., 2025）。Self-Certainty@$n$：Self-Certainty スコアで順位付けされた $n$ 個のサンプルの上位 $\eta$ パーセントに対して多数決を行う（セクション3で最良のベースライン）；Think@$n$：DTR($\cdot$) で順位付けされた $n$ 個のサンプルの上位 $\eta$ パーセントに対して多数決を行う。全手法は同一の $n$ 個のサンプルプールを使用する。$n = 48$、$\eta = 50\%$ と設定する。さらなる分析はセクション C に提供する。結果は 10 試行の平均値である。

結果。結果を表2に報告する。効率性を比較するため、サブセットのサンプルのみを集約する Short@$n$、Self-Certainty@$n$、Think@$n$ については early stopping を明示的に考慮する。具体的には、以下のプロトコルで生成トークンの総数として測定した、問題ごとの平均推論コストを報告する。

Cons@$n$ および Mean@$n$ の場合、推論コストはサンプリングされた $n$ 個の全応答のトークン数の合計（すなわち、$\sum_{i=1}^{n} |S_i|$）として定義され、early stopping なしの完全デコーディングに対応する。Short@$n$ の場合、サンプルを長さで順位付けし、最短の $\eta \times n$ 個のサンプルを選択する。推論コストは

図5 | 異なる aggregation 手法でのタスク精度と推論コスト（トークン数）のトレードオフの比較。精度は4つのデータセット（AIME 24/25, HMMT 25, GPQA-D）全体で平均化される。提案手法 Think@$n$ は最良の全体的な Pareto 最適な性能を達成する。これは推論コストを約半分にしながら Cons@n の精度に匹敵または上回り、一方 Self-Certainty@$n$ は著しく効率が低い。

![Image](paper_artifacts/image_000005_7eaacc6327affc1c172f6b9d0301f08d868eb5be12dded2d6232ceff81f10506.png)

表3 | AIME 2025 における Think@$n$ 性能と推論コストに対する prefix 長（$\ell_{\text{prefix}}$）の影響。DTR の推定に 50 トークンの短い prefix を使用することは、より長いものを使用するよりも優れており、完全なシーケンス（all）と同等の性能を発揮しながら、大幅なコスト削減を実現する。参考のため Pass@1 および Cons@$n$ も報告する。添字は10試行の標準偏差を示す。

|                        | Accuracy           | Cost (k tokens)   |
|------------------------|--------------------|-------------------|
| Pass@1                 | 80.0$_{4.2}$       | 6.4               |
| Cons@$n$               | 90.0$_{2.5}$       | 307.6             |
| Think@$n$ Prefix length |                   |                   |
| 50                     | 94.7$_{1.6}$       | 155.4             |
| 100                    | 92.0$_{1.6}$       | 154.1             |
| 500                    | 92.7$_{1.3}$       | 153.2             |
| 1000                   | 92.7$_{1.3}$       | 177.4             |
| 2000                   | 92.0$_{1.3}$       | 198.8             |
| all                    | 94.0$_{0.3}$       | 307.6             |

選択されたサンプルのトークン数の合計に加え、$\ell_{\text{longest\_short}} \times \eta \times n$ に等しい early stopping オーバーヘッドとして計算される。ここで $\ell_{\text{short}}$ は選択された最短サブセットの中で最長のサンプルの長さを示す。この項は、サブセット生成が完了した時点で終了する（すなわち $\ell_{\text{longest\_short}}$ で制限される）部分的に生成されたサンプルのコストを考慮する。Long@$n$ の推論コストは、最長のサンプルを選択するために完全なデコーディングが必要なため、Cons@$n$ および Mean@$n$ と同じである。Think@$n$ の場合、サンプルは固定 prefix から計算された DTR で順位付けされる。$\ell_{\text{prefix}}$ を DTR（$S[:\ell_{\text{prefix}}]$）の推定に使用される prefix トークン数とする。推論コストは、上位 $\eta \times n$ 個の順位付けされたサンプルの合計トークン数に、$\ell_{\text{prefix}} \times \eta \times n$ の固定 prefix オーバーヘッドを加えたものとして定義される。これは early termination 前に全候補を生成するコストを反映する。Self-Certainty@$n$ は Think@$n$ と同じコスト計算に従うが、サンプルが DTR（$S[:\ell_{\text{prefix}}]$）ではなく Self-Certainty（$S[:\ell_{\text{prefix}}]$）で順位付けされる点のみが異なる。

表3は、AIME 25 において $\ell_{\text{prefix}}$ を変化させた予備的 ablation を報告する。$\ell_{\text{prefix}} = 50$ トークンのみを使用することで、より長い prefix よりも高い精度が達成され、完全なシーケンスを使用した場合と同等の性能が得られ、推論コストを大幅に削減できることがわかった。したがって、表2の全実験において $\ell_{\text{prefix}} = 50$ に固定する。

示されるように、Cons@$n$ は全候補の完全デコーディングにより最も高い推論コストを要するが、強力な精度ベースラインを提供する。Mean@$n$ は Cons@$n$ と同じコストを持つが、全手法の中で最も性能が低い。early stopping の下では、Short@$n$ は Cons@$n$ に対して控えめなコスト削減を達成するが、精度において一貫して Cons@$n$ を下回る。Long@$n$ は Short@$n$ よりもさらに低下した性能を示すが、コスト削減の恩恵をもたらさない。これは、長さベースのヒューリスティックが推論品質の粗いプロキシに留まり、高品質なサンプルを信頼性高く識別できないことが多く、最適でない集約につながることを示している。Self-Certainty@$n$ は短い prefix を用いた early stopping を可能にすることで推論コストを大幅に削減するが、それでも評価された4つのベンチマークのうち3つで Cons@$n$ と Think@$n$ の両方を下回る。対照的に、Think@$n$ は推論コストを約半分にしながら、一貫して Cons@$n$ の精度に匹敵または上回る。Pareto 最適な性能は図5に示された平均結果において最も顕著であり、Think@$n$ が最良の全体的な精度-コストのトレードオフを達成している。要約すると、これらの結果は DTR がより情報量の多い、信頼性の高い選択シグナルを提供し、推論 Compute の効率的な並列スケーリングを可能にすることを実証している。

## 5. 関連研究

## 5.1. CoT 長と性能の関係

Test-Time Scaling のパラダイムは、より多くの計算リソース、通常はより長い CoT シーケンスとして現れる、を割り当てることが推論性能を向上させるという主張に基づいて大きく発展してきた（Guo et al., 2025; Muennighoff et al., 2025; Wei et al., 2022）。最近の実証的研究は、この「長ければよい」ヒューリスティックの普遍性に対するニュアンスを強調している（Feng et al., 2025; Wu et al., 2025）。Gema et al. (2025) は、推論長の増加が特にモデルが気散りしやすい場合に、多様なタスクにわたって精度を系統的に低下させる逆スケーリング体制を特定している。同様に、Wu et al. (2025) は CoT 長と精度の関係を「逆U字」曲線として特徴付け、誤差の蓄積などの要因により、ある長さを超えると性能が低下する最適な長さが存在することを示唆している。

いくつかの研究は、簡潔さを好むことで対応する観察を活用する手法を提案している。Hassid et al. (2025) は、サンプリングされた候補の中で最短の推論チェーンがしばしば最も正確であることを実証し、効率的な生成のための推論時の長さベース投票を提案している。Agarwal et al. (2025) による近い研究も、並列デコーディングで最初に完成したトレースを選択するトレーニング不要の戦略を導入し、精度を維持しながらトークン使用量を削減している。トレーニング側では、Shrivastava et al. (2025) が RL における長さ膨張を明示的に抑制するために、より長い応答をフィルタリングする rejection sampling を用いた Group Filtered Policy Optimization (GFPO) を提案し、モデルが性能を犠牲にせずに思考量を減らせることを実証している。我々の研究は、生のトークン数が効果的な推論努力の信頼性の低いプロキシであることを確認するという点でこれらの観点と一致しているが、単に表面的な簡潔さのヒューリスティックに頼るのではなく、機械論的な内部シグナルを提案する点で異なる。

## 5.2. LLM における内部情報の活用

言語モデルが層を越えて情報を内部でどのように表現・操作するか、また内部状態をどのように活用できるかについて、豊富な研究が行われてきた。この方向性の中心となるのは、言語モデルの中間表現が最終層に到達する前に有意義なシグナルをエンコードすることが多いという観察である。この見解の初期の証拠は Nostalgebraist (2020) によって提供されており、モデルの unembedding matrix を使用して中間の hidden states を直接語彙空間に射影する手法（我々の研究でも採用する手法）を示した。結果は、自己回帰 Transformer が次のトークンについての粗い推測を形成し、それが層を越えて反復的に洗練されることを明らかにする。後続の分析（Belrose et al., 2023）はさらに、浅い層でより解釈可能なトークン予測を可能にし、中間

表現を最終予測空間に対してよりよく整合させる、層固有の学習済みアフィン変換を導入している。

モデルのプロービングを超えて、Chuang et al. (2023) は言語モデルの事実的知識が特定の層でしばしばより顕著であるという経験的発見を活用している。上位層と下位層のロジットを対比させることで、事実的シグナルを増幅して事実性を向上させるデコーディング手法を提案している。Vilas et al. (2025) による最近の研究は、生成された推論トレース全体の hidden states の時系列的な発展を特徴付ける潜在軌跡シグナルを導入して正確性を予測している。この研究が表現の逐次的な次元を調べるのに対し、我々の研究は個々のトークンに対する層を越えた予測の深さ方向の発展に焦点を当てている。

補完的な解釈可能性研究も、推論時に LLM が深さをどのように活用するかを再考している。Gupta et al. (2025) は、初期層が高頻度の汎用的なトークン推測を好む傾向があり、それが後続のより文脈に適切な予測へと洗練されることを示している。Csordás et al. (2025) は、後期層が根本的に新しい変換を導入するのではなく主に細粒度の分布的洗練を行うことを示唆し、現代の LLM における深さ利用の効率性について疑問を提起している。これらの発見は、内部予測が最終層の前に安定する可能性があるという見解を強化し、我々の動機と一致している。全体として、我々の目標は内部状態を修正または構築してモデル能力を向上させることを目的とした新しい手法を開発することではない。むしろ、LLM における思考努力を暗黙的に反映するモデルの計算努力を測定するためのプロキシとして、自然な、変更されていない内部表現を活用する。

## 6. 結論

我々は LLM における推論時の推論努力の新しい指標として deep-thinking ratio (DTR) を導入した。トークン予測の深さ方向の安定化を追跡することにより、DTR はトークン長や信頼度などの表面的なプロキシよりも効果的な推論の信頼性の高いシグナルを提供する。この洞察に基づいて、DTR を早期選択と集約に活用する Test-Time Scaling 戦略として Think@$n$ を提案し、推論コストを大幅に削減しながら標準的な self-consistency と同等またはそれ以上の性能を達成する。これらの結果は総じて、モデルがどれだけ長く思考するかではなく、どのように内部で思考するかを測定することが有望な方向性であることを示唆している。将来の研究は、この洞察を活用して効果的な推論がどのように特徴付けられるかを探求する可能性があり、より長い思考連鎖を生成することからより深くより計算集約的な推論を誘発することへと焦点を移し、より信頼性が高く効率的な推論モデルの実現を可能にすることができる。

## 謝辞

Google AIR の Congchao Wang および同僚の貴重なサポートに感謝する。また、Virginia Tech の Yu-Min Tseng および UVA の Meng-Lab メンバーの有益な議論にも感謝する。
## References

- A. Agarwal, A. Sengupta, and T. Chakraborty. First finish search: Efficient test-time scaling in large language models. arXiv preprint arXiv:2505.18149 , 2025.
- P. Aggarwal, S. Kim, J. Lanchantin, S. Welleck, J. Weston, I. Kulikov, and S. Saha. OptimalThinkingBench: Evaluating over and underthinking in LLMs. arXiv , 2025.
3. Anthropic. Claude 3.7 sonnet system card. https://assets.anthropic.com/m/ 785e231869ea8b3b/original/claude-3-7-sonnet-system-card.pdf , 2025a.

- Anthropic. System card: Claude opus 4 &amp; claude sonnet 4. https://www-cdn.anthropic.com/ 6d8a8055020700718b0c49369f60816ba2a7c285.pdf , 2025b.
- Art of Problem Solving. 2024 aime i. https://artofproblemsolving.com/wiki/index.php/ 2024\_AIME\_I , 2024a.
- Art of Problem Solving. 2024 aime ii. https://artofproblemsolving.com/wiki/index.php/ 2024\_AIME\_II , 2024b.
- Art of Problem Solving. 2025 aime i. https://artofproblemsolving.com/wiki/index.php/ 2025\_AIME\_I , 2025a.
- Art of Problem Solving. 2025 aime ii. https://artofproblemsolving.com/wiki/index.php/ 2025\_AIME\_II , 2025b.
- V. Balachandran, J. Chen, L. Chen, S. Garg, N. Joshi, Y. Lara, J. Langford, B. Nushi, V. Vineet, Y. Wu, and S. Yousefi. Inference-time scaling for complex tasks: Where we stand and what lies ahead. arXiv , 2025. doi: 10.48550/arxiv.2504.00294.
- M. Balunović, J. Dekoninck, I. Petrov, N. Jovanović, and M. Vechev. Matharena: Evaluating llms on uncontaminated math competitions. arXiv preprint arXiv:2505.23281 , 2025.
- N. Belrose, Z. Furman, L. Smith, D. Halawi, I. Ostrovsky, L. McKinney, S. Biderman, and J. Steinhardt. Eliciting latent predictions from transformers with the tuned lens. arXiv preprint arXiv:2303.08112 , 2023.
- B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and A. Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling. arXiv , 2024. doi: 10.48550/arxiv.2407.21787.
- Y.-S. Chuang, Y. Xie, H. Luo, Y. Kim, J. Glass, and P. He. DoLa: Decoding by contrasting layers improves factuality in large language models. arXiv , 2023.
- R. Csordás, C. D. Manning, and C. Potts. Do language models use their depth efficiently? arXiv , 2025. doi: 10.48550/arxiv.2505.13898.
- A. Y. Din, T. Karidi, L. Choshen, and M. Geva. Jump to conclusions: Short-cutting transformers with linear transformations. In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024) , pages 9615-9625, 2024.
- M. Elbayad, J. Gu, E. Grave, and M. Auli. Depth-adaptive transformer. arXiv preprint arXiv:1910.10073 , 2019.
- Y. Feng, J. Kempe, C. Zhang, P. Jain, and A. Hartshorn. What characterizes effective reasoning? revisiting length, review, and structure of CoT. arXiv , 2025.
- Y. Fu, X. Wang, Y. Tian, and J. Zhao. Deep think with confidence. arXiv preprint arXiv:2508.15260 , 2025.
- A. P. Gema, A. Hägele, R. Chen, A. Arditi, J. Goldman-Wetzler, K. Fraser-Taliente, H. Sleight, L. Petrini, J. Michael, B. Alex, P. Minervini, Y. Chen, J. Benton, and E. Perez. Inverse scaling in test-time compute. arXiv , 2025. doi: 10.48550/arxiv.2507.14417.
- D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948 , 2025.

- A. Gupta and V. Srikumar. Test-time scaling with repeated sampling improves multilingual text generation. arXiv , 2025. doi: 10.48550/arxiv.2505.21941.
- A. Gupta, J. Yeung, G. Anumanchipalli, and A. Ivanova. How do LLMs use their depth? arXiv , 2025.
- M. Hassid, G. Synnaeve, Y. Adi, and R. Schwartz. Don't overthink it. preferring shorter thinking chains for improved llm reasoning. arXiv preprint arXiv:2505.17813 , 2025.
4. HMMT. Hmmt 2025. https://www.hmmt.org/ , 2025.
- A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al. Openai o1 system card. arXiv preprint arXiv:2412.16720 , 2024.
- Z. Kang, X. Zhao, and D. Song. Scalable best-of-n selection for large language models via self-certainty. arXiv , 2025. doi: 10.48550/arxiv.2502.18581.
7. W.-T. Kao, T.-H. Wu, P.-H. Chi, C.-C. Hsieh, and H.-Y. Lee. Bert's output layer recognizes all hidden layers? some intriguing phenomena and a simple way to boost bert. arXiv preprint arXiv:2001.09309 , 2020.
- N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi, L. Zettlemoyer, P. Liang, E. Candès, and T. B. Hashimoto. s1: Simple test-time scaling. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing , pages 20286-20332, 2025.
9. Nostalgebraist. Interpreting gpt: The logit lens. https://www.lesswrong.com/posts/ AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens , 2020.
10. OpenAI. Openai o3-mini system card. https://openai.com/index/o3-mini-system-card/ , 2025.
11. OpenAI. Introducing gpt-5. https://openai.com/index/introducing-gpt-5/ , 2025.
12. OpenAI, :, S. Agarwal, L. Ahmad, J. Ai, S. Altman, A. Applebaum, E. Arbus, R. K. Arora, Y. Bai, B. Baker, H. Bao, B. Barak, A. Bennett, T. Bertao, N. Brett, E. Brevdo, G. Brockman, S. Bubeck, C. Chang, K. Chen, M. Chen, E. Cheung, A. Clark, D. Cook, M. Dukhan, C. Dvorak, K. Fives, V. Fomenko, T. Garipov, K. Georgiev, M. Glaese, T. Gogineni, A. Goucher, L. Gross, K. G. Guzman, J. Hallman, J. Hehir, J. Heidecke, A. Helyar, H. Hu, R. Huet, J. Huh, S. Jain, Z. Johnson, C. Koch, I. Kofman, D. Kundel, J. Kwon, V. Kyrylov, E. Y. Le, G. Leclerc, J. P. Lennon, S. Lessans, M. Lezcano-Casado, Y. Li, Z. Li, J. Lin, J. Liss, Lily , Liu, J. Liu, K. Lu, C. Lu, Z. Martinovic, L. McCallum, J. McGrath, S. McKinney, A. McLaughlin, S. Mei, S. Mostovoy, T. Mu, G. Myles, A. Neitz, A. Nichol, J. Pachocki, A. Paino, D. Palmie, A. Pantuliano, G. Parascandolo, J. Park, L. Pathak, C. Paz, L. Peran, D. Pimenov, M. Pokrass, E. Proehl, H. Qiu, G. Raila, F. Raso, H. Ren, K. Richardson, D. Robinson, B. Rotsted, H. Salman, S. Sanjeev, M. Schwarzer, D. Sculley, H. Sikchi, K. Simon, K. Singhal, Y. Song, D. Stuckey, Z. Sun, P. Tillet, S. Toizer, F. Tsimpourlas, N. Vyas, E. Wallace, X. Wang, M. Wang, O. Watkins, K. Weil, A. Wendling, K. Whinnery, C. Whitney, H. Wong, L. Yang, Y. Yang, M. Yasunaga, K. Ying, W. Zaremba, W. Zhan, C. Zhang, B. Zhang, E. Zhang, and S. Zhao. gpt-oss-120b &amp; gpt-oss-20b model card. arXiv , 2025. doi: 10.48550/arxiv.2508.10925.
- D. Rein, B. L. Hou, A. C. Stickland, J. Petty , R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman. Gpqa: A graduate-level google-proof q&amp;a benchmark. In First Conference on Language Modeling , 2024.
- J. Saad-Falcon, A. G. Lafuente, S. Natarajan, N. Maru, H. Todorov, E. Guha, E. K. Buchanan, M. Chen, N. Guha, C. Ré, and A. Mirhoseini. Archon: An architecture search framework for inference-time techniques. arXiv , 2024. doi: 10.48550/arxiv.2409.15254.

- J. Saad-Falcon, E. K. Buchanan, M. F. Chen, T.-H. Huang, B. McLaughlin, T. Bhathal, S. Zhu, B. Athiwaratkun, F. Sala, S. Linderman, A. Mirhoseini, and C. Ré. Shrinking the generation-verification gap with weak verifiers. arXiv , 2025. doi: 10.48550/arxiv.2506.18203.
- T. Schuster, A. Fisch, J. Gupta, M. Dehghani, D. Bahri, V. Tran, Y. Tay, and D. Metzler. Confident adaptive language modeling. Advances in Neural Information Processing Systems , 35:17456-17472, 2022.
- V. Shrivastava, A. Awadallah, V. Balachandran, S. Garg, H. Behl, and D. Papailiopoulos. Sample more to think less: Group filtered policy optimization for concise reasoning. arXiv preprint arXiv:2508.09726 , 2025.
- B. Stroebl, S. Kapoor, and A. Narayanan. Inference scaling fLaws: The limits of LLM resampling with imperfect verifiers. arXiv , 2024. doi: 10.48550/arxiv.2411.17501.
- J. Su, J. Healey, P. Nakov, and C. Cardie. Between underthinking and overthinking: An empirical study of reasoning length and correctness in LLMs. arXiv , 2025. doi: 10.48550/arxiv.2505.00127.
- Y. Sui, Y.-N. Chuang, G. Wang, J. Zhang, T. Zhang, J. Yuan, H. Liu, A. Wen, S. Zhong, H. Chen, and X. Hu. Stop overthinking: A survey on efficient reasoning for large language models. arXiv , 2025. doi: 10.48550/arxiv.2503.16419.
- K. Team, A. Du, B. Gao, B. Xing, C. Jiang, C. Chen, C. Li, C. Xiao, C. Du, C. Liao, et al. Kimi k1. 5: Scaling reinforcement learning with llms. arXiv preprint arXiv:2501.12599 , 2025.
- S. Teerapittayanon, B. McDanel, and H.-T. Kung. Branchynet: Fast inference via early exiting from deep neural networks. In 2016 23rd international conference on pattern recognition (ICPR) , pages 2464-2469. IEEE, 2016.
- M. G. Vilas, S. Yousefi, B. Nushi, E. Horvitz, and V. Balachandran. Tracing the traces: Latent temporal signals for efficient and accurate reasoning. arXiv , 2025.
- X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou. Selfconsistency improves chain of thought reasoning in language models. In The Eleventh International Conference on Learning Representations , 2023. URL https://openreview.net/forum?id= 1PL1NIMMrw .
- J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou. Chain of thought prompting elicits reasoning in large language models. arXiv , 2022. doi: 10.48550/arxiv. 2201.11903.
- Y. Wu, Y. Wang, T. Du, S. Jegelka, and Y. Wang. When more is less: Understanding chain-of-thought length in LLMs. arXiv , 2025.
13. xAI. Grok 4. https://x.ai/news/grok-4 , 2025.
- A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al. Qwen3 technical report. arXiv preprint arXiv:2505.09388 , 2025.
- E. Yeo, Y. Tong, M. Niu, G. Neubig, and X. Yue. Demystifying long chain-of-thought reasoning in LLMs. arXiv , 2025. doi: 10.48550/arxiv.2502.03373.
- T. Zhong, Z. Liu, Y. Pan, Y. Zhang, Y. Zhou, S. Liang, Z. Wu, Y. Lyu, P. Shu, X. Yu, et al. Evaluation of openai o1: Opportunities and challenges of agi. arXiv preprint arXiv:2409.18486 , 2024.


## A. DTRに対する異なる距離指標の比較

本手法（Section 2）は、Jensen-Shannon divergence（JSD）を採用して中間層と最終層の予測間の乖離を定量化し、DTRを算出する。他の距離の概念も考えられる。ここでは、Kullback-Leibler divergence（KLD）とcosine similarityという2つの追加指標を検討する。結果はFigure 6に示す。

Kullback-Leibler divergence。Equation (2)においてJSDをKLDに置き換えることで、最終層の分布 $p_{t,L}$ と中間層の分布 $p_{t,l}$ の間のdivergenceを以下のように計算する。

<!-- formula-not-decoded -->

Cosine similarity。Section 2.2で定義した分布比較を、cosine similarityを用いた表現空間の指標で置き換える。共有unembedding行列 $W_U$（Equation (1)）によって中間層のhidden stateを語彙空間に射影する代わりに、中間層のhidden state $h_{t,l}$ と最終層のhidden state $h_{t,L}$ の間のcosine similarityを直接計算する。距離は以下のように定義される。

<!-- formula-not-decoded -->

KLDとcosine similarityのいずれについても、Section 2.2と同じ設定を適用してdeep-thinkingトークンを特定し、KLDベースのDTRおよびcosineベースのDTRを計算する。

Results。AIME 25とHMMT 25において、$\text{OSS-120B}_{\text{medium}}$ を用いたKLDベースおよびcosineベースのDTRの相関結果を、本手法のJSDベースのDTRと比較して報告する。両データセットにわたって、JSDベースのDTRは精度との正の相関において一貫して最も強い結果を示す（AIME 25では $r = 0.869$、HMMT 25では $r = 0.895$）。これにより、Section 2のDTR定義においてJSDを採用することが正当化される。対照的に、cosineベースのDTRは大幅に弱く不安定な相関を示す（AIME 25では $r = 0.633$、HMMT 25では $r = 0.172$ にすぎない）。KLDベースのDTRも同様に一貫性のない挙動を示し、AIME 25では負の相関（$r = -0.698$）、HMMT 25では控えめな正の相関（$r = 0.409$）となった。この一貫性のなさは、KLDの非対称性と数値的不安定性に起因する可能性がある。すなわち、初期層の予測は高エントロピーで比較的フラットであり、後に近ゼロの値へと押し込まれる多くのトークンに確率質量を割り当てる。その結果、KLDは人為的に小さくなり得るため、この指標は感度が非常に高くなる。

## B. 異なるGPT-OSSの推論レベルにおけるDTR

Figure 7は、GPT-OSS-120Bモデルの異なる推論レベル設定（低・中・高）においてDTRがどのように変化するかを示している。AIME 25とGPQA-Dの両方において、興味深く一貫したトレンドが観察される。モデルの重みは同一のままで、システムプロンプトのみが異なるにもかかわらず、低い推論レベルの設定ではDTR値が高く、一方で高い推論レベルの設定では系統的にDTRが小さくなり、より良いタスク精度を達成する。

考えられる説明の一つは、高い推論レベルほど計算を深さから系列長へと再配分し、各トークンの層ごとの計算を実質的にフラット化するというものである。高い推論レベルのモデルは、個々のトークンごとの深い修正をあまり必要とせず、代わりにより多くのforward passを伴う長い推論チェーンを生成するため、合計の実効計算量が増大し、性能が向上する。

Accuracy (Pass@1)

0

0

0

0

Accuracy (Pass@1)

.

.

.

.

850

825

800

775

0

.

060

Cosine Similarity

r

= 0.633

0

.

066

.

072

0

0

.

078

DTR

(a) Cosine similarityを距離指標として用いた場合（AIME 25）。

Cosine Similarity

0

0

0

0

.

.

.

.

68

64

60

56

0

.

060

r

= 0.172

0

.

066

0

.

072

0

.

078

DTR

(d) Cosine similarityを距離指標として用いた場合（HMMT 25）。

r

= 0.409

0

.

375

0

.

390

0

.

405

DTR

(e) KL divergenceを距離指標として用いた場合（HMMT 25）。

(c) JS divergenceを距離指標として用いた場合（AIME 25）。

![Image](paper_artifacts/image_000006_6f449bc108af7d63c091a8433855d7d2403e5bac32a060573c6cf78b08437a20.png)

Jensen-Shannon Divergence

0

0

0

0

.

.

.

.

68

64

60

56

0

.

135

r

= 0.895

0

.

150

0

.

165

0

.

180

DTR

(f) JS divergenceを距離指標として用いた場合（HMMT 25）。

Figure 6 | AIME 25（上段）およびHMMT 25（下段）において、異なる距離指標（cosine similarity、KL divergence、JS divergence）を用いた場合の精度とdeep-thinking ratio（DTR）の相関の比較。

タスク性能。DTRはdeep-thinkingトークンの割合として定義されている（すなわち、生成されたトークンの総数で平均化される）ため、系列が長くなるとDTR計算の分母が増大し、より小さな値が得られる。これはまた、DTRが異なるモデルやモデルモード間で直接比較できない可能性があることも示唆している。

## C. Think@ $n$ の追加分析

ここでは、(i) サンプリングする応答数 $n$ および (ii) 投票に使用する上位 $\eta$ パーセンテージを変化させた場合に Think@ $n$ がどのように振る舞うかについて追加分析を行う。

**サンプル数 $n$ の影響。** 図8aは、$n$ を増加させた場合（$n \in \{16, 32, 48\}$）における Think@ $n$ と Cons@ $n$（すなわち self-consistency）との比較を示す。Think@ $n$ は $n$ が大きくなるにつれて単調に改善し、Cons@ $n$ に対する優位性はより顕著になる。より多くの応答をサンプリングすることで、正解の答えのクラスタがより大きくなり、出現しやすくなる。Think@ $n$ は、より良いサンプルを優先的に選択することでこの拡大された候補プールを活用することができ、Cons@ $n$ に対してより強力な性能向上をもたらす。

**上位 $\eta$ パーセンテージの影響。** 図8aは、異なる上位 $\eta$ パーセント（$\eta \in \{25\%, 50\%, 75\%\}$）における Think@ $n$ を評価する。性能は $\eta=50\%$ でピークに達し、小さい割合（$\eta=25\%$）では低下する。

Accuracy (Pass@1)

Accuracy (Pass@1)

0

0

0

0

.

.

.

.

84

80

76

72

0

.

345

Kullback-Leibler Divergence

r

= -0.698

0

.

360

.

375

0

0

.

390

DTR

(b) KL divergence as the distance metric on AIME 25.

Kullback-Leibler Divergence

0

0

0

0

.

.

.

.

675

650

625

600

Accuracy (Pass@1)

![Image](paper_artifacts/image_000007_7aea57f0f866bfe21982b97feb2f17a4e742491ee4bbf3a0cb9d44379afc04d3.png)

図7 | OSS-120B モデルの異なる推論レベル設定における Deep-thinking ratio（DTR）。

![Image](paper_artifacts/image_000008_dd1ead7c4a2e268138baa900ef80cac65734bc56d8eaa99bc84782923d59cd06.png)

- (a) 異なるサンプル数 $n$ の比較。
- (b) 異なる上位 $\eta$ パーセンテージの比較。

![Image](paper_artifacts/image_000009_25e10e26020f3719fffc0a8083dd471dc9951ac4829acf6832fbf5e6626892d5.png)

図8 | 異なるサンプル数 $n$ および上位 $\eta$ パーセントを用いた Think@ $n$ の分析。(a) $n$ が増加するにつれて、Think@ $n$ は一貫してより大きな候補プールから恩恵を受け、$n$ が高い場合に Cons@ $n$ に対する性能差が拡大する。(b) 性能は $\eta=50\%$ でピークに達し、過度に積極的なフィルタリングおよび過度に寛容な選択はいずれも精度の低下につながる可能性がある。

および大きい割合（$\eta=75\%$）でも低下する。これはトレードオフを示唆している：サンプルが少なすぎると投票の堅牢性が低下し、多数決を安定させるための強い候補が減少する可能性があるのに対し、サンプルが多すぎると品質の低いサンプルが混入し、Think@ $n$ の恩恵が希薄化する可能性がある。全体として、結果は安定した動作点として $\eta=50\%$ を選択したことを支持している。

## D. プロンプト

数学タスク（AIME 2024、AIME 2025、HMMT 2025）の実験で採用したプロンプトを表4に、GPQA のプロンプトを表5に示す。

## 表4 | 数学タスク（AIME 2024、AIME 2025、HMMT 2025）の推論プロンプト。

## AIME 2024、AIME 2025、HMMT 2025 のプロンプト

Please reason step by step, and put your final answer within \ boxed {} .

## 表5 | GPQA の推論プロンプト。

## GPQA のプロンプト

You will be given a multiple choice question with different choices such as (A), (B), (C), (D). Think step by step before giving a final answer to this question. Always finish your answer with 'The final answer is \ boxed { (X) } .', where X is the correct answer choice. If none of the options match, choose the closest option as the final answer.

## E. 定性的な例

AIME 2025 データセットの例題とその正解（表6）、および OSS-120B$^{\text{medium}}$ からの2つの出力——誤った出力（表7）と正しい出力（表8）——を示す。特筆すべきことに、誤った出力は大幅に冗長（27,724トークン）であり、DTR値が低い（13.9）のに対し、正しい出力はより簡潔（3,725トークン）であり、DTR値が高い（19.0）。

表6 | AIME 2025 からの例題とその正解。

## AIME 2025 からの例題。

点 $A$ を中心とし半径6の円 $\omega_1$ が、半径15の円 $\omega_2$ に点 $B$ で内接している。点 $C$ および $D$ は $\omega_2$ 上にあり、$BC$ が $\omega_2$ の直径であり、$BC \perp AD$ を満たす。長方形 $EFGH$ が $\omega_1$ に内接しており、$EF \perp BC$、$C$ は $EF$ より $GH$ に近く、$D$ は $EH$ より $FG$ に近い（図示の通り）。三角形 $\triangle DGF$ と $\triangle CHG$ は面積が等しい。長方形 $EFGH$ の面積は $\frac{m}{n}$ であり、$m$ と $n$ は互いに素な正の整数である。$m + n$ を求めよ。

## 正解。

293

## 表7 | 例題に対する OSS-120B$^{\text{medium}}$ の誤った出力。

## DTR = 13.9%、トークン数 = 27,724 の誤った出力。

幾何学を解釈する必要がある。設定：点 A を中心とし半径6の円 $\omega_1$ が、半径15の大きい円 $\omega_2$ に点 B で内接している。したがって B は $\omega_1$ が $\omega_2$ の内側で接する共通点である。内接接線より、距離 AB = 15-6 = 9 であり、B は直線 AB 上にある。

座標系を設定しよう。A を原点に置くか？より簡単かもしれない：$\omega_1$ を中心 (0,0)、半径6とする。すると B は円 $\omega_1$ 上にあり、かつ $\omega_2$ 上にもある。$\omega_2$ の半径は大きく15で、中心を O とする。O を $\omega_2$ の中心と表記しよう。距離 OA = 9（AB = 9 より）で、AB = 9？ 待って AB = 中心間距離 = 15-6 = 9、合っている。B は $\omega_1$ と $\omega_2$ の直線 OA 上にあり、A の外側にある？ 実は内接接線：小さい円が大きい円の内側にある；それらは、小さい円から大きい円への方向に中心を結ぶ直線上の点で接する。A を (0,0)、O を (9,0) に設定すると（O は右側）、B は A から O の方向に距離 6 の点、すなわち B は (6,0)。確かに O から B までの距離：O(9,0) から B(6,0) まで距離3であり、これが $\omega_2$ の半径？ 待って $\omega_2$ の半径は15、O から B は15のはず。しかし O(9,0) から B(6,0) の距離は3であり、15ではない。何かがおかしい。

O を (0,0) にした方が簡単かもしれない。$\omega_2$ を O (0,0) を中心、半径15とする。$\omega_1$ の半径6が B で内接している；その中心 A は O から距離 15-6 = 9 にあり、ある方向に沿っている。内接接線の B を円 $\omega_2$ 上の直線 OA 上の A から O の外側の点として選ぶか？ 実は内接接線：小さい円が大きい円の内側にあり、両円が交わる1点 B で接する。中心を結ぶ直線は B を通る。O から B までの距離は15（半径）。A から B までの距離は6。O から A は9。B は直線 OA 上の A の外側にある？ 待って O から A は9、小さい円の半径は6なので、O から A から B へ同じ直線に沿って進むと：O-A-B の方向？ B が両円の円周上にあるため。O から B までの距離 = 15 = OA + AB？ OA=9、AB=6 で OA+AB=15 なので、B は O から A を通ってさらに外側にある。O を原点、A を例えば正の x 方向に距離9の位置に置こう。O を (0,0)、A を (9,0) とする。すると B は O から B への距離が15の x 軸上のさらに遠い点なので、B は (15,0)。確認：A (9,0) から B (15,0) までの距離 = 6、正しい。

今、BC は $\omega_2$ の直径であり、B から C は中心 O（$\omega_2$ の中心）を通り、長さ30（直径）。B が (15,0) にあるため、直径の反対側の点は、O が中点となるように C が位置する：O = (0,0) は B と C の中点。したがって C = (-15,0)（直径は原点を通るため）。だから BC は水平線（x 軸）。

長方形 EFGH は $\omega_1$（中心 A (9,0)、半径6）に内接している。長方形は必ずしも軸に整列していないか？ EF は GH と平行、FG は EH と平行。EF ⊥ BC（BC は水平）が与えられているので、EF（と GH）は垂直か？ 待って EF が BC と垂直であり、BC は水平なので EF は垂直。したがって長方形の一辺は垂直。よって長方形の辺は垂直・水平に整列している：EF が垂直、FG が水平等。つまり長方形は（BC が水平の座標系で）軸に整列している。したがって長方形の辺は軸と平行（BC が水平なので EF が垂直）。

BC ⊥ AD が与えられているので、AD は x 軸に垂直、つまり A を通る垂直線を意味する？ 待って AD のセグメントは A (9,0) から $\omega_2$ 上の点 D を結んでいるが、AD が BC すなわち x 軸に垂直の垂直線（x=9）となる。AD は $\omega_2$ と点 D で交差しなければならない。したがって D は垂直線 x=9 が $\omega_2$（半径15）と交わる点。方程式 $x^2 + y^2 = 225$。x=9 を代入 $\Rightarrow 81 + y^2 = 225 \Rightarrow y^2 = 144 \Rightarrow y = \pm 12$。どちらか？ 方向によりおそらく D は上側？ 指定されていない。D を (9,12)（上側）と考えよう。下側でもよいが、長方形の方向が決めるかもしれない。

C は GH より EF に近い。GH は EF の反対側：EF（左）と GH（右）が垂直辺の長方形かもしれない？方向を確認しよう：通常長方形の頂点は E-F-G-H の順に配置され、おそらく時計回り；しかし本質的ではない。EF が垂直なら、FG は水平、GH は垂直、HE は水平。つまり EF が左側、GH が右側（EF の右に長方形がある場合）。不明。

同様に、D は EH より FG に近い。FG が上側（水平）、EH が下側（水平）。D は (9,12) の高い点；上側 FG への距離が下側 EH への距離より小さい（長方形が上部近くにある場合は理にかなっている）。したがって FG が上側、EH が下側。したがって長方形 EFGH はおそらく上側が D 近く、左側が C 近く。

C は (-15,0) の遠い左側。「C は EF より GH に近い」とは、C から直線 GH への距離が直線 EF への距離より小さいことを意味する。C は遠い左側なので、GH が左側の辺（より左側）、EF が右側の辺であることを意味する？ 待って C から垂直線までの距離は水平距離。GH が左側の辺（より左側）であれば、その C への距離は EF（右側の辺）への距離より小さい。それは C が GH に近いことに一致する。したがって GH が長方形の左側（より左側）、EF が右側。

## ... 説明のため省略 ...

整数の因数分解はないようである。非有理係数の2次式で因数分解できるかもしれないが、役に立たない。

複雑さを考えると、答えはおそらく m+n = 207 のようなものかもしれない？ 推測しよう？ 良くない。時間が限られているため、プレースホルダーを出力する。

したがって x は無理数かもしれない；つまり k は有理整数でない。したがって面積は無理数？ 問題文と矛盾する。時間が来たので、おそらく長方形が軸に整列しているという以前の仮定が間違っていたかもしれない；長方形が回転していれば、有理数の面積になるかもしれない。

assistant final 207

## 表8 | 例題に対する OSS-120B$^{\text{medium}}$ の正しい出力。

## DTR = 19.0%、トークン数 = 3,725 の正しい出力。

幾何学を解析する必要がある。座標を定義しよう。

座標系を設定しよう：AB を垂直にするか？B を原点に置いた方が簡単かもしれない。

2つの円がある：$\omega_2$ 半径15、$\omega_1$ は A を中心とし半径6で、点 B で内接している。したがって A は $\omega_2$ の内側にあり、距離 AB = 半径の差 = 15 - 6 = 9。B は接点であり、直線 AB 上にある。

$\omega_2$ の中心を O（O2 と呼ぼうか）と置こう。$\omega_1$ の中心 A は O から距離9にあり、B は両円の円周上にある点で直線 O-A 上にある。

点 C および D は $\omega_2$ 上にあり、BC が $\omega_2$ の直径となる。したがって BC は中心 O を通り、長さ30（直径）。B が (15,0) にあるため、直径の反対側の端は O が中点：O = (0,0) が B と C の中点。したがって C = (-15,0)（B(15,0) が原点を横切れば C(-15,0)）。だから BC は水平線（x 軸）。

O を (0,0) に置こう。AB を正の x 軸に沿って：B を (15,0) に置こうか？ $\omega_2$ は半径15で O (0,0) を中心とする。B が $\omega_1$ が $\omega_2$ に内接する接点であれば、B は $\omega_2$ 上の O から距離15の点にある。したがって B は (15,0)。すると A は直線 OB 上の O から距離9の内側の B から距離6の点（$\omega_1$ の半径が6）。したがって O を (0,0)、B を (15,0) とすると、A は同じ直線に沿って (9,0) に位置する（O から A は9）。A は (9,0)。すると $\omega_1$ は半径6で (9,0) を中心とする。

- ... 説明のため省略 ...
- *三角形 $DGF$：* 底辺 $GF$ の長さは $w$；$D(9, 12)$ から直線 $y = h/2$（$GF$ を含む直線）までの垂直距離は $12 - \frac{h}{2}$。したがって

<!-- formula-not-decoded -->

*三角形 $CHG$：* 辺 $HG$ は垂直で長さ $h$；$C(-15, 0)$ から直線 $x = 9 - \frac{w}{2}$（$HG$ を含む直線）までの水平距離は $24 - \frac{w}{2}$。したがって

<!-- formula-not-decoded -->

問題は $[\triangle DGF] = [\triangle CHG]$ と述べている。$\frac{1}{2}$ の因子を消去すると

<!-- formula-not-decoded -->

$-\frac{wh}{2}$ の項が両辺に現れ、消去すると

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

-

$w$ と $h$ を解く $(2)$ を $(1)$ に代入する：

したがって

長方形 $EFGH$ の面積は

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

したがって $m = 288$、$n = 5$（互いに素）、したがって

<!-- formula-not-decoded -->
