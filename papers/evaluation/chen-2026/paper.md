![Image](paper_artifacts/image_000000_73ceca6f21f2685db190ec1d8849c1bbc340a27392bfca88d03fb7f3e6a453da.png)

## Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens

Wei-Lin Chen 1,2* , Liqian Peng 2 , Tian Tan 2 , Chao Zhao 2 , Blake JianHang Chen 2 , Ziqian Lin 2 , Alec Go 2 and Yu Meng 1

1 University of Virginia, 2 Google, * Work done as a student researcher at Google.

Large language models (LLMs) have demonstrated impressive reasoning capabilities by scaling test-time compute via long Chain-of-Thought (CoT). However, recent findings suggest that raw token counts are unreliable proxies for reasoning quality: increased generation length does not consistently correlate with accuracy and may instead signal 'overthinking,' leading to performance degradation. In this work, we quantify inference-time effort by identifying deep-thinking tokens -tokens where internal predictions undergo significant revisions in deeper model layers prior to convergence. Across four challenging mathematical and scientific benchmarks (AIME 24/25, HMMT 25, and GPQA-diamond) and a diverse set of reasoning-focused models (GPT-OSS, DeepSeek-R1, and Qwen3), we show that deep-thinking ratio (the proportion of deep-thinking tokens in a generated sequence) exhibits a robust and consistently positive correlation with accuracy, substantially outperforming both length-based and confidence-based baselines. Leveraging this insight, we introduce Think@ 𝑛 , a test-time scaling strategy that prioritizes samples with high deep-thinking ratios. We demonstrate that Think@ 𝑛 matches or exceeds standard self-consistency performance while significantly reducing inference costs by enabling the early rejection of unpromising generations based on short prefixes.

Figure 1 | Comparison of correlations between accuracy and proxies for thinking effort. The plots illustrate the relationship between model performance and two inference-time measures of thinking effort on GPT-OSS-120Bmedium across AIME 2024/2025, HMMT 2025, and GPQA-Diamond. (Left) Output token count exhibits a moderate negative correlation (average 𝑟 = -0 . 544), suggesting that output length is an unreliable indicator of performance. (Right) In contrast, our proposed deepthinking ratio demonstrates a strong positive correlation with accuracy (average 𝑟 = 0 . 828).

![Image](paper_artifacts/image_000001_e28dc8bd826444a3a4595b5cfe630c9f4d49742327855ccd850cc75e7369d7d2.png)

## 1. Introduction

Large language models (LLMs) have achieved remarkable reasoning capabilities by generating explicit thought traces, most notably through the Chain-of-Thought (CoT) paradigm (Wei et al., 2022). Prior works have shown that increasing the number of reasoning tokens generated can generally boost task performance (Anthropic, 2025a,b; Guo et al., 2025; Jaech et al., 2024; OpenAI, 2025; Team et al., 2025; Yang et al., 2025; Zhong et al., 2024), motivating methods that encourage longer and more elaborate thinking traces (Balachandran et al., 2025; Muennighoff et al., 2025; Yeo et al., 2025).

However, a growing body of evidence suggests that token counts are unreliable indicators of model performance during inference, as longer reasoning does not consistently translate into higher accuracy (Aggarwal et al., 2025; Su et al., 2025; Sui et al., 2025; Wu et al., 2025). Empirical studies reveal inverted-U relationships between CoT length and performance (Wu et al., 2025), as well as inverse-scaling behaviors in which longer reasoning traces systematically degrade performance (Gema et al., 2025). Excessive reasoning may reflect overthinking, wherein models amplify flawed heuristics or fixate on irrelevant details (Feng et al., 2025). Consequently, relying on length as a metric for reasoning quality not only encourages verbosity over clarity but also wastes computational resources on uninformative tokens. Though recent work has attempted to assess the semantic structure of CoTs ( e.g. , by representing reasoning traces as graphs), such approaches often rely on costly auxiliary parsing or external annotations (Feng et al., 2025). Addressing these limitations requires more principled and efficient methods for measuring thinking effort that can distinguish effective reasoning from uninformative generation.

In this work, we introduce deep-thinking ratio (DTR) as a direct measure of inference-time thinking effort. Instead of relying on surface-level features like output length, we focus on how individual tokens are produced internally. We posit that when a token prediction stabilizes in early layers, subsequent depth-wise modifications entail relatively low computational effort, resembling less thinking . In contrast, token predictions that undergo sustained revision in deeper layers before converging reflect greater thinking (Chuang et al., 2023). We operationalize this idea by projecting intermediate-layer hidden states into the vocabulary space and comparing each layer's prediction distribution to the finallayer distribution. Tokens whose distributions do not converge until deeper layers are identified as deep-thinking tokens . By counting the proportion of deep-thinking tokens in a generated sequence, we obtain DTR, which provides a simple, mechanistically grounded measure of thinking effort, requiring neither task-specific heuristics nor external structural annotations.

Across four challenging mathematical and scientific reasoning benchmarks-AIME 2024, AIME 2025, HMMT 2025, and GPQA (Art of Problem Solving, 2024a,b, 2025a,b; HMMT, 2025; Rein et al., 2024)-and a range of reasoning-focused language models, including GPT-OSS, DeepSeek-R1, and Qwen3 families (Guo et al., 2025; OpenAI et al., 2025; Yang et al., 2025), we demonstrate that measuring deep-thinking tokens yields strong correlations with task accuracy. The achieved correlation is substantially higher than those obtained using length-based or confidence-based baselines. Furthermore, we show that deep-thinking tokens can be leveraged for parallel inference scaling, where preferentially selecting and aggregating responses with higher DTR achieves performance comparable or better than standard consensus-based methods, while requiring only half the compute cost. Our contributions are summarized as follows:

- We introduce deep-thinking ratio (DTR)-a measure that counts the ratio of deep-thinking tokens in a sequence whose predictions undergo sustained revision in deeper layers before converging-as a new lens for characterizing inference-time thinking effort.
- We empirically show that, across multiple reasoning benchmarks and model families, DTR of a generated sequence exhibits strong positive correlations with task accuracy, outperforming length-based and confidence-based baselines significantly.

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

Figure 2 | Heatmap of thought: We plot the Jensen-Shannon divergence (JSD) values between the distributions of the last (36th) layer and intermediate layers for an answer sequence from GPT-OSS120Bhigh . Functional and templated words ( e.g. , 'and', 'is', 'boxed', ' &lt;| return |&gt; ') often converge at relatively shallow layers; Completions after operators ( e.g. , '+', '=') and answer tokens/symbols ( e.g. , '13', '(D)') do not settle until deeper layers. Interestingly, the answer token '13' gradually surfaces in earlier layers after its first appearance.

- We introduce Think@ 𝑛 , a test-time scaling strategy that preferentially selects and aggregates samples with higher DTR. By early halting unpromising generations based on DTR estimated from short prefixes, Think@ 𝑛 matches or surpasses standard self-consistency with approximately half the inference cost.

## 2. Measuring Deep-Thinking Ratio

## 2.1. Preliminaries

We consider an autoregressive language model 𝑓 𝜃 composed of 𝐿 transformer layers, hidden dimension 𝑑 , and vocabulary 𝑉 . Given a prefix sequence 𝑦 &lt;𝑡 , the forward pass at generation step 𝑡 produces a sequence of residual stream states { ℎ𝑡,𝑙 } 𝐿 𝑙 = 1 , where ℎ𝑡,𝑙 ∈ ℝ 𝑑 denotes the hidden state after layer 𝑙 . The final-layer output ℎ𝑡,𝐿 is projected by the language modeling head ( i.e. , the unembedding matrix) 𝑊𝑈 ∈ ℝ | 𝑉 | × 𝑑 to produce logits over the vocabulary.

Prior research on early exiting (Belrose et al., 2023; Din et al., 2024; Elbayad et al., 2019; Schuster et al., 2022; Teerapittayanon et al., 2016) has demonstrated that, without specialized auxiliary training, applying the language modeling head directly to intermediate-layer hidden states effectively yields meaningful predictive distributions (Kao et al., 2020; Nostalgebraist, 2020). Building on this line of works, we project intermediate-layer hidden states into the vocabulary space using the same unembedding matrix 𝑊𝑈 . For each intermediate layer 𝑙 ∈ { 1 , . . . , 𝐿 -1 } , we compute the logit vector 𝑧 𝑡,𝑙 and probability distribution 𝑝𝑡,𝑙 as

<!-- formula-not-decoded -->

The model's final-layer distribution is denoted by 𝑝𝑡,𝐿 .

Figure 3 | Illustration of our method of identifying deepthinking tokens. Suppose a model with 10 layers, by setting the depth fraction 𝜌 = 0 . 8, the token is successfully classified as a deep-thinking token at generation step 𝑡 since its JSD with the final-layer distribution first fall below the threshold 𝑔 only until it reaches the latesettling regime.

![Image](paper_artifacts/image_000003_2bd5a692dc805ff63288784785d1aad311543a651552a8d62dcb087026d09c52.png)

## 2.2. Deep-Thinking Tokens

We posit that inference-time thinking effort for a token manifests as the continued evolution of predictive distributions ( i.e. , 𝑝𝑡,𝑙 ) across LM layers. Tokens with earlier distributional stabilization correspond to less additional thinking, while those having later stabilization correspond to needing more extended internal thinking. In other words, simple tokens stabilize early with shallow computation, whereas difficult tokens requiring more thinking exhibit distributional shifts in deeper layers with more computation. To illustrate this, we show a motivation example on answering a GQPA (Rein et al., 2024) question in Figure 2.

To quantify this behavior, we measure how long a token's predictive distribution continues to change before settling , operationalized as the layer at which the intermediate distribution becomes sufficiently close to the final-layer distribution. Specifically , for each generation step 𝑡 and layer 𝑙 , we compute the Jensen-Shannon divergence (JSD) between the intermediate-layer distribution 𝑝𝑡,𝑙 and the final-layer distribution 𝑝𝑡,𝐿 :

<!-- formula-not-decoded -->

where 𝐻 (·) denotes Shannon entropy. By construction, 𝐷𝑡,𝐿 = 0. A trajectory 𝑙 ↦→ 𝐷𝑡,𝑙 that approaches zero only at later layers indicates prolonged distributional revision (think more), whereas early convergence indicates that the model settles on its final prediction with fewer subsequent updates (think less). We employ JSD due to its symmetry and boundedness, following (Chuang et al., 2023). We explore other distance metrics in Section A.

## Algorithm 1: Computing DeepThinking Ratio (DTR)

```
Input : Autoregressive LM 𝑓 𝜃 with 𝐿 layers and unembedding matrix 𝑊𝑈 ; Input prompt 𝑥 ; Threshold 𝑔 ; Depth fraction 𝜌 Output: DTR ( 𝑆 ) of the generated sequence 𝑆 𝐶 ← 0; // deep thinking token count 𝑆 ←∅ ; // generated sequence 𝑦 𝑡 ← [ BOS ] ; // initialize with start token while 𝑦 𝑡 ≠ [ EOS ] do Sample 𝑦 𝑡 ∼ 𝑝𝑡,𝐿 ( 𝑓 𝜃 (· | 𝑥, 𝑆 )) ; 𝑆 ←( 𝑆, 𝑦 𝑡 ) ; for 𝑙 ← 1 to 𝐿 do 𝑝𝑡,𝑙 ← softmax ( 𝑊𝑈ℎ𝑡,𝑙 ) ; 𝐷𝑡,𝑙 ← JSD ( 𝑝𝑡,𝐿 , 𝑝 𝑡,𝑙 ) ; end 𝑐 𝑡 ← min { 𝑙 : min 𝑗 ≤ 𝑙 𝐷𝑡,𝑗 ≤ 𝑔 } ; if 𝑐 𝑡 ≥ ⌈( 1 -𝜌 ) 𝐿 ⌉ then 𝐶 ← 𝐶 + 1; end end return 𝐶 /| 𝑆 | ;
```

To enforce a strict notion of settling, we compute:

<!-- formula-not-decoded -->

We define the settling depth 𝑐 𝑡 as the first layer at which ¯ 𝐷𝑡,𝑙 falls below a fixed threshold 𝑔 :

<!-- formula-not-decoded -->

We then define a deep-thinking regime using a depth fraction 𝜌 ∈ ( 0 , 1 ) , with

<!-- formula-not-decoded -->

A token is classified as a deep-thinking token ( i.e. , requiring more layer computations and more thinking effort to become sufficiently close to the final-layer distribution) if 𝑐 𝑡 ∈ L deep-thinking . An illustration is shown in Figure 3.

Finally, for a generated sequence 𝑆 of length 𝑇 , we define the deep-thinking ratio, DTR ( 𝑆 ) , for the sequence as the proportion of tokens that settle in the late regime:

<!-- formula-not-decoded -->

Ahigher DTR indicates that a larger fraction of tokens undergo extended computation for distributional revision before stabilizing. We note that our proposed method does not imply that early-settling tokens are suboptimal; rather, it provides a depth-wise characterization of inference-time thinking effort that complements the surface-level token length measure. We show the overall algorithm of DTR in Algorithm 1. We also provide qualitative examples in Section E.

## 3. Deep-Thinking Ratio Reflects Task Accuracy More Reliably

We empirically evaluate whether our distributional distance-based measurement provides a more faithful and robust characterization of inference-time thinking effort than surface-level, length-based proxies ( i.e. , token counts).

Models. We evaluate eight variants of reasoning LLMs from three model families: GPT-OSS-20B (with low, medium, and high reasoning levels) and GPT-OSS-120B (with low, medium, and high reasoning levels) (OpenAI et al., 2025), DeepSeek-R1-70B (Guo et al., 2025), 1 and Qwen3-30BThinking (Yang et al., 2025). These models are known for their strong, long CoT capability in mathematical and complex reasoning, and span multiple parametric scales for comprehensive coverage.

Tasks. We focus on reasoning-intensive benchmarks where scaling CoT-style computation at inference time plays a central role. We adopt four benchmarks widely used in recent evaluations of LLM reasoning capabilities (Balunović et al., 2025; OpenAI, 2025; xAI, 2025), including three competition-level mathematical problem sets, AIME 2024 (Art of Problem Solving, 2024a,b), AIME 2025 (Art of Problem Solving, 2025a,b), and HMMT 2025 (HMMT, 2025), as well as the diamond set of GPQA (Rein et al., 2024), which consists of challenging graduate-level scientific questions.

1 For brevity, we refer DeepSeek-R1-70B to Llama-3.3-70B-Instruct distilled with DeepSeek-R1 generated samples ( https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B ).

Decoding settings. Following (Gema et al., 2025), we prompt models to reason step by step using a fixed, neutral instruction, without specifying a reasoning budget or explicitly encouraging longer deliberation. This setup allows each model to naturally allocate inference-time computation on a per-instance basis, avoiding confounds introduced by externally imposed token budgets or budget-conditioning prompts. Following standard practice in natural overthinking analyses (Gema et al., 2025), we sample multiple responses for each question (25 responses per question in our experiments). Across these samples, models naturally exhibit variation in reasoning length and internal computation patterns. We use the developer recommended sampling parameters for all tested models: temperature=1.0 and top p =1.0 for GPT-OSS series; temperature=0.6 and top p = 0.95 for DeepSeek-R1-70B and Qwen-3-30B-Thinking.

For each sampled response, we record intermediate-layer hidden states, obtain their projected probability distribution, and compute DTR as described in Section 2. We uniformly set the settling threshold 𝑔 = 0 . 5 and the depth fraction 𝜌 = 0 . 85 to define the deep-thinking regime. We also analyze with different values and the results are provided in Section 3.2. The reported statistics are averaged over 30 random seeds across decoding runs.

## 3.1. Results

To quantify the relationship between inference-time thinking effort and task performance, we measure the association between thinking effort scores and answer accuracy by computing Pearson correlation coefficient. Specifically , we conduct a binned analysis following (Gema et al., 2025) by partitioning sampled sequences into quantile bins ( i.e. , 5 bins) based on their DTR (Equation (6)) and computing the average accuracy within each bin.

We compare deep-thinking token measurement against the following baselines, including lengthbased proxies and confidence-based approaches, which are also commonly adopted to assess generation quality.

Token count. The total number of tokens generated in the model's output reasoning traces. This measure is widely framed as a direct proxy for test-time compute, and underlies many empirical studies of inference-time scaling (Anthropic, 2025a,b; Guo et al., 2025; Jaech et al., 2024; OpenAI, 2025; Team et al., 2025; Yang et al., 2025; Zhong et al., 2024).

Reverse token count. As a complementary baseline, we additionally consider reverse token count, defined as the negative of the total number of generated tokens for each response. This transformation is included to account for the frequently observed inverse relationship between reasoning length and accuracy in LLM overthinking (Gema et al., 2025; Wu et al., 2025).

Log probability. Following the notation in Section 2, let a generated sequence 𝑆 = ( 𝑦 1 , . . . , 𝑦 𝑇 ) . At generation step 𝑡 , the model's output prediction distribution (at final-layer 𝐿 ) over the vocabulary V is denoted by 𝑝𝑡,𝐿 (·) . We compute the average log-probability of the sampled tokens:

<!-- formula-not-decoded -->

Higher values indicate that the model assigns higher likelihood to its own generation and are commonly interpreted as higher confidence.

Table 1 | Pearson correlations between task accuracy and different inference-time measures, including length-based and confidence-based baselines, across eight model variants and four reasoning benchmarks. Correlation values are color-coded: strong positive correlations (0 . 5 ∼ 1) are shown in dark green, weak positive correlations (0 ∼ 0 . 5) in light green, weak negative correlations ( -0 . 5 ∼ 0) in light orange, and strong negative correlations ( -1 ∼ -0 . 5) in dark orange.

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

Negative perplexity. Perplexity is defined as the exponentiated negative average log-probability:

<!-- formula-not-decoded -->

We report negative perplexity -PPL ( 𝑆 ) so that larger values correspond to higher confidence.

Negative entropy. To incorporate information from the full prediction distribution over V rather than only the sampled token, we compute the average entropy:

<!-- formula-not-decoded -->

We report negative entropy -Ent ( 𝑆 ) , where larger values indicate more peaked distributions and thus greater model confidence.

Self-Certainty. We also include Self-Certainty (Kang et al., 2025), a distributional confidence metric based on the idea that higher confidence corresponds to prediction distributions that are further from the uniform distribution 𝑢 , which represents maximum uncertainty. Formally, self-certainty is defined as the average Kullback-Leibler (KL) divergence between 𝑢 ( 𝑣 ) = 1 /|V| and 𝑝𝑡,𝐿 :

<!-- formula-not-decoded -->

For all baselines, correlations are computed using the same protocol, where sequences are ranked and binned by token count (or its negation) or confidence scores.

Table 1 reports the correlation between task accuracy and different measurments, across eight model variants and four benchmarks. As observed, measuring sequences with token count exhibits notable oranged-colored values ( 𝑟 &lt; 0), with mean 𝑟 = -0 . 59. This indicates that longer generations are more associated with lower performance, aligning with recent reports of inverse scaling and overthinking. Extended reasoning traces could be symptomatic of redundant, misguided, or erroramplifying deliberation. The results underscore the unreliability of using surface-level length feature as proxy for effective problem solving. Reversing token count yields a positive correlation of identical magnitude. However, the improvement is purely post hoc, reflecting the empirical regularity in regimes where shorter responses are more accurate. As such, reverse token count only serve as a statistical adjustment, rather than capture principled notion of computation or thinking effort.

Compared to token count measure, confidence-based measures (log probability, negative perplexity, negative entropy, and self-certainty) exhibit moderately positive correlations with mean 𝑟 = 0 . 219 ∼ 0 . 605, as reflected by the predominance of green-colored values. This indicates that model confidence captures partial information about correctness. However, their behavior is relatively heterogeneous across models and benchmarks: while certain configurations achieve strong positive correlations, others deteriorate to weak or even negative associations. This inconsistency suggests that confidence signals might conflate other factors like overconfidence, and therefore do not reliably reflect inferencetime compute effort or problem solving effectiveness.

In contrast, our proposed measurement of DTR demonstrates the strongest and most stable relationship with task performance, achieving the highest average correlation of 𝑟 = 0 . 683, outperforming both reverse token count and Self-Certainty, the best-performing baselines among confidence-based approaches. Overall, DTR remains positive across models and benchmarks, exhibiting the fewest orange-colored values (2 out of the 32 model-benchmark settings tested). Collectively, the results show that computing DTR over output sequences provides a more faithful and robust characterization of successful reasoning outcomes than token volume alone or confidence-based alternatives.

## 3.2. Effect of Settling Thresholds and Depth Fractions

We conduct an analysis to understand how our two key hyper-parameters-the settling threshold 𝑔 and the late-settling depth fraction 𝜌 -affect the measured thinking effort and its correlation with task performance. Figure 4 illustrates the accuracy profiles across varying thinking efforts ( i.e. , average

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

(a) Effect of different settling threshold 𝑔 .

![Image](paper_artifacts/image_000004_8f27ce42e9aaf57b346560b6c42537057134d8b0e557221bb3a837cfef4d145a.png)

(b) Effect of different depth fraction 𝜌 .

Figure 4 | Effect of hyper-parameters on thinking effort measurement and accuracy profiles. We analyze the impact of hyper-parameters by sweeping different settling threshold 𝑔 and depth fraction 𝜌 . (a) Varying 𝑔 has more impacts the correlation; a permissive threshold ( 𝑔 = 0 . 25) yields flatter trends, whereas 𝑔 = 0 . 5 provides the most robust positive signal. (b) Varying 𝜌 shifts the range of thinking effort scores but maintains overall consistent positive slopes. Overall, stricter criteria (higher 𝑔 , lower 𝜌 ) reduce the range of DTR, with ( 𝑔, 𝜌 ) = ( 0 . 5 , 0 . 85 ) offering an ideal balance between stability and correlation.

late-settling token ratios), derived by 𝑔 ∈ { 0 . 25 , 0 . 5 , 0 . 75 } and 𝜌 ∈ { 0 . 8 , 0 . 85 , 0 . 9 , 0 . 95 } . We set 𝜌 fixed to 0 . 85, when sweeping 𝑔 , and 𝑔 fixed to 0 . 5 when sweeping 𝜌 . We report results on GPQA-D using GPT-OSS-20B with reasoning level high.

We conclude the following observations: (1) the magnitude of the measured sequence-level thinking effort is directly influenced by the strictness of these parameters. Specifically , both Figures 4a and 4b show that imposing stricter criteria-a higher settling threshold 𝑔 or a lower depth fraction 𝜌 -results in a reduction of the average late-settling token ratio. This is mechanistically consistent: a higher 𝑔 requires the intermediate states to be distributionally far to the final output until reaching deeper layers in the late regime to be considered settle; while a lower 𝜌 restricts the definition of the late regime to a narrower band of deeper layers. Both conditions naturally filter out more candidates, resulting in fewer tokens being classified as late-settling and consequently a lower range of overall thinking effort scores.

- (2) The settling threshold 𝑔 has a more pronounced impact on the correlation between thinking effort and accuracy than the depth fraction 𝜌 . As shown in Figure 4b, varying 𝜌 shifts the range of late-settling ratios due to varying strictness but maintains a consistent, positive slope across all settings, indicating that the metric is relatively robust to the specific definition of the late layers. In contrast, Figure 4a reveals that the choice of 𝑔 has more impact on measured results: a softer threshold of 𝑔 = 0 . 25 yields a flatter trend with lower correlation value, suggesting that it may be overly permissive, including tokens with less computational efforts and diminishing the measurement's ability to distinguish high-quality trajectory. Conversely, thresholds of 𝑔 = 0 . 5 and 𝑔 = 0 . 75 exhibit more robust positive correlations reflecting the accuracy.
- (3) Overall, we can see that when the criteria are overly restrictive ( 𝑔 = 0 . 75 and 𝜌 ∈ { 0 . 9 , 0 . 95 } ), the trends, while still maintaining positive correlations, appears to be slightly more unstable due to the potential filtering of informative high computational tokens. Among the tested configurations, ( 𝑔, 𝜌 ) = ( 0 . 5 , 0 . 85 ) strikes an ideal balance, yielding a reliable trend with high correlation values.

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

Table 2 | Comparison of task accuracy and average inference cost (k tokens) under different aggregation methods, across four reasoning benchmarks. The reported cost reductions ( Δ %) are shown relative to Cons@ 𝑛 . Think@ 𝑛 achieves the best overall performance while reducing inference cost by approximately 50%. Methods with † adopt a prefix length of 50 to determine early stopping.

| Method              | AIME 25           | AIME 25           | AIME 24           | AIME 24           | HMMT 25           | HMMT 25           | GPQA-D            | GPQA-D            |
|---------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|
|                     | Acc               | Cost ( Δ %)       | Acc               | Cost ( Δ %)       | Acc               | Cost ( Δ %)       | Acc               | Cost ( Δ %)       |
|                     | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   | OSS-120B-medium   |
| Cons@ 𝑛             | 92.7              | 307.6 (-)         | 92.7              | 235.1 (-)         | 80.0              | 355.6 (-)         | 73.8              | 93.5 (-)          |
| Mean@ 𝑛             | 80.0              | 307.6 (-)         | 81.6              | 235.1 (-)         | 62.6              | 355.6 (-)         | 69.9              | 93.5 (-)          |
| Long@ 𝑛             | 86.7              | 307.6 (-)         | 86.7              | 235.1 (-)         | 73.3              | 355.6 (-)         | 73.2              | 93.5 (-)          |
| Short@ 𝑛            | 87.3              | 255.7 (-17%)      | 88.0              | 200.9 (-15%)      | 77.3              | 290.4 (-18%)      | 73.3              | 84.4 (-10%)       |
| Self-Certainty@ 𝑛 † | 87.3              | 150.6 (-51%)      | 91.3              | 119.3 (-49%)      | 78.0              | 177.0 (-50%)      | 76.0              | 47.9 (-49%)       |
| Think@ 𝑛 †          | 94.7              | 155.4 (-49%)      | 93.3              | 121.3 (-48%)      | 80.0              | 181.9 (-49%)      | 74.7              | 48.8 (-48%)       |
|                     | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking | Qwen3-4B-Thinking |
| Cons@ 𝑛             | 86.7              | 1073.1 (-)        | 93.3              | 950.1 (-)         | 63.3              | 1275.7 (-)        | 67.8              | 410.6 (-)         |
| Mean@ 𝑛             | 81.2              | 1073.1 (-)        | 86.3              | 950.1 (-)         | 55.7              | 1275.7 (-)        | 66.9              | 410.6 (-)         |
| Long@ 𝑛             | 85.3              | 1073.1 (-)        | 86.7              | 950.1 (-)         | 52.7              | 1275.7 (-)        | 66.7              | 410.6 (-)         |
| Short@ 𝑛            | 90.0              | 983.6 (-8%)       | 90.0              | 871.0 (-8%)       | 63.3              | 1165.7 (-9%)      | 68.2              | 382.9 (-7%)       |
| Self-Certainty@ 𝑛 † | 86.7              | 548.9 (-49%)      | 90.0              | 480.9 (-49%)      | 63.3              | 641.4 (-50%)      | 68.2              | 206.6 (-50%)      |
| Think@ 𝑛 †          | 90.0              | 537.5 (-50%)      | 93.3              | 482.2 (-49%)      | 66.7              | 641.4 (-50%)      | 69.7              | 206.8 (-50%)      |

## 4. Deep-Thinking Tokens Enable Efficient Test-Time Scaling

Repeated sampling is a popular strategy for scaling test-time compute, in parallel to generating long CoT (Brown et al., 2024; Gupta and Srikumar, 2025; Saad-Falcon et al., 2024, 2025; Stroebl et al., 2024). It improves accuracy by aggregating multiple independently generated samples per problem at the cost of increased inference budget. In this section, we explore whether our proposed DTR measure can be leveraged to preferentially select and aggregate higher-quality samples towards better performance.

Experimental setups. We follow the best-of-n (BoN) evaluation protocol commonly adopted in recent test-time scaling studies (Fu et al., 2025). For each problem, we sample 𝑛 responses using identical decoding settings, and compare the following aggregation methods: Cons@ 𝑛 : Standard self-consistency (Wang et al., 2023), which performs majority voting over all 𝑛 sampled responses; Mean@ 𝑛 : The average accuracy of all the 𝑛 samples, reflecting a baseline of no preferential aggregation; Long@ 𝑛 and Short@ 𝑛 : Majority voting over the longest/shortest 𝜂 percent of the 𝑛 samples, ranked by token count (Agarwal et al., 2025; Hassid et al., 2025). Self-Certainty@ 𝑛 : Majority voting over the highest-scoring 𝜂 percent of the 𝑛 samples, ranked by Self-Certainty score (the bestperforming baseline in Section 3); Think@ 𝑛 : Majority voting over the highest-scoring 𝜂 percent of the 𝑛 samples, ranked by DTR (·) . All methods operate on the same pool of 𝑛 samples. We set 𝑛 = 48 and 𝜂 = 50%. More analysis are provided in Section C. The results are averaged across 10 trials.

Results. We report the results in Table 2. To compare efficiency, we explicitly account for early stopping for Short@ 𝑛 , Self-Certainty@ 𝑛 , and Think@ 𝑛 , which aggregate only a subset of samples. Specifically, we report the average per-problem inference cost, measured as the total number of generated tokens, under the following protocols.

For Cons@ 𝑛 and Mean@ 𝑛 , the inference cost is defined as the sum of token counts across all 𝑛 sampled responses= ( i.e. , ˝ 𝑛 𝑖 = 1 | 𝑆𝑖 | ) corresponding to full decoding without early stopping. For Short@ 𝑛 , we rank samples by their length and select the shortest 𝜂 × 𝑛 samples. The inference cost is

Figure 5 | Comparison of the trade-off between task accuracy and inference cost (tokens) with different aggregation methods. Accuracy is averaged across all four datasets (AIME 24/25, HMMT 25, GPQA-D). Our Think@ 𝑛 method achieves the best overall Pareto-optimal performance. It matches or exceeds the accuracy of Cons@n with approximately half the inference cost, while Self-Certainty@ 𝑛 is notably less efficient.

![Image](paper_artifacts/image_000005_7eaacc6327affc1c172f6b9d0301f08d868eb5be12dded2d6232ceff81f10506.png)

Table 3 | Impact of prefix length ( ℓ prefix ) on Think@ 𝑛 performance and inference cost for AIME 2025. Using a short prefix of 50 tokens to estimate DTR outperforms using longer ones, and is comparable to full sequence (all) while providing significant cost savings. We also report Pass@1 and Cons@ 𝑛 for reference. Subscripts denote the standard deviation across 10 trials.

|                        | Accuracy   | Cost (k tokens)   |
|------------------------|------------|-------------------|
| Pass@1                 | 80.0 4 . 2 | 6.4               |
| Cons@ 𝑛                | 90.0 2 . 5 | 307.6             |
| Think@ 𝑛 Prefix length |            |                   |
| 50                     | 94.7 1 . 6 | 155.4             |
| 100                    | 92.0 1 . 6 | 154.1             |
| 500                    | 92.7 1 . 3 | 153.2             |
| 1000                   | 92.7 1 . 3 | 177.4             |
| 2000                   | 92.0 1 . 3 | 198.8             |
| all                    | 94.0 0 . 3 | 307.6             |

computed as the sum of the token count of the selected samples, plus an early-stopping overhead equal to ℓ longest\_short × 𝜂 × 𝑛 , where ℓ short denotes the length of the longest sample among the selected shortest subset. This term accounts for partially generated samples that are terminated once subset generation completes ( i.e. , bounded by ℓ longest\_short ). The inference cost for Long@ 𝑛 is the same as Cons@ 𝑛 and Mean@ 𝑛 as it requires full decoding to select longest samples. For Think@ 𝑛 , samples are ranked by DTR, computed from a fixed prefix. Let ℓ prefix denote the number of prefix tokens used to estimate DTR ( 𝑆 [ : ℓ prefix ]) . The inference cost is defined as the total token count of the top 𝜂 × 𝑛 ranked samples, plus a fixed prefix overhead of ℓ prefix × 𝜂 × 𝑛 , which reflects the cost of generating all candidates prior to early termination. Self-Certainty@ 𝑛 follows the same cost computation as Think@ 𝑛 , differing only in that samples are ranked by Self-Certainty ( 𝑆 [ : ℓ prefix ]) rather than DTR ( 𝑆 [ : ℓ prefix ]) .

Table 3 reports a preliminary ablation on AIME 25 that varies ℓ prefix . We find that using only ℓ prefix = 50 tokens achieves higher accuracy than longer prefixes and matches the performance obtained using the full sequence, while significantly reducing inference cost. Accordingly, we fix ℓ prefix = 50 for all experiments in Table 2.

As shown, Cons@ 𝑛 incurs the highest inference cost due to full decoding of every candidate, while providing a strong accuracy baseline. Mean@ 𝑛 has the same cost as Cons@ 𝑛 but is the worstperforming one among all methods. Under early stopping, Short@ 𝑛 achieves modest cost savings relative to Cons@ 𝑛 , yet consistently underperforms it in accuracy. Long@ 𝑛 exhibits further degraded performance compared to Short@ 𝑛 without offering any cost-saving benefits. This indicates that length-based heuristics remain a coarse proxy for reasoning quality and often fail to reliably identify high-quality samples, leading to suboptimal aggregations. Self-Certainty@ 𝑛 substantially reduces inference cost by enabling early stopping using short prefixes, but nonetheless underperforms both Cons@ 𝑛 and Think@ 𝑛 on three of the four evaluated benchmarks. In contrast, Think@ 𝑛 consistently matches or exceeds the accuracy of Cons@ 𝑛 while requiring approximately half the inference cost. The Pareto-optimal performance is most evident in the averaged results shown in Figure 5, where Think@ 𝑛 achieves the best overall accuracy-cost trade-off. In sum, these results demonstrate that DTR provides a more informative and reliable selection signal, enabling efficient parallel scaling of inference compute.

## 5. Related Work

## 5.1. Relationship between CoT Length and Performance

The paradigm of test-time scaling has largely operated on the assertion that allocating more computation, typically manifested as longer CoT sequences, boosts reasoning performance Guo et al. (2025); Muennighoff et al. (2025); Wei et al. (2022). Recent empirical studies have highlighted nuances to the universality of this 'longer is better' heuristic (Feng et al., 2025; Wu et al., 2025). Gema et al. (2025) identify inverse scaling regimes where increased reasoning length systematically degrades accuracy across diverse tasks, particularly when models are prone to distraction. Similarly, Wu et al. (2025) characterize the relationship between CoT length and accuracy as an 'inverted-U' curve, suggesting an optimal length exists beyond which performance deteriorates due to factors like error accumulation.

Several works have proposed methods to exploit corresponding observations by favoring conciseness. Hassid et al. (2025) demonstrated that the shortest reasoning chains among sampled candidates are often the most accurate, proposing inference-time length-based voting for efficient generations. A close work by Agarwal et al. (2025) also introduced a training-free strategy that selects the first completed trace in parallel decoding, reducing token usage while maintaining accuracy. On the training side, Shrivastava et al. (2025) proposed Group Filtered Policy Optimization (GFPO) to explicitly curb length inflation in RL by rejection sampling that filters longer responses, demonstrating that models can think less without sacrificing performance. Our work aligns with these perspectives by confirming that raw token count is an unreliable proxy for effective reasoning effort, but we diverge by proposing a mechanistic internal signal rather than simply relying on surface-level brevity heuristics.

## 5.2. Leveraging Internal Information in LLMs

A rich line of work has investigated how LMs internally represent and manipulate information across layers, and how internal states can be exploited. Central to this direction is the observation that intermediate representations in LMs often encode meaningful signals before reaching the final layer. Early evidence for this view was provided by Nostalgebraist (2020), which projects intermediate hidden states directly into the vocabulary space using the model's unembedding matrix-a technique we adopt in our work. The results reveal that autoregressive transformers form coarse guesses about the next token that are iteratively refined across layers. Subsequent analyses (Belrose et al., 2023) further introduce learned, layer-specific affine transformations that better align intermediate

representations with the final prediction space, enabling more interpretable token predictions in shallower layers.

Beyond model probing, Chuang et al. (2023) exploits the empirical finding that factual knowledge in LMs is often more salient in particular layers. By contrasting logits from higher and lower layers, they propose a decoding method that amplifies factual signals and improves factuality. A recent work by Vilas et al. (2025) introduces latent-trajectory signals characterizing the temporal evolution of hidden states across generated reasoning traces to predict correctness. While the work examines the sequential dimension of representations, our work focuses on the depth-wise evolution of predictions across layers for individual tokens.

Complementary interpretability works also revisit how LLMs utilize depth at inference. Gupta et al. (2025) shows that early layers tend to favor high-frequency, generic token guesses, which are subsequently refined into contextually appropriate predictions. Csordás et al. (2025) suggest that later layers primarily perform fine-grained distributional refinement rather than introducing fundamentally new transformations, raising questions about the efficiency of depth utilization in modern LLMs. These findings reinforce the view that internal predictions may stabilize before the final layer, aligning with our motivations. Overall, our goal is not to modify or construct internal states to develop new methods aimed at improving model capabilities. Instead, we leverage natural, unaltered internal representations as a proxy for measuring model computational effort, which implicitly reflects thinking effort in LLMs.

## 6. Conclusion

We introduced deep-thinking ratio (DTR) as a novel measure of inference-time reasoning effort in LLMs. By tracking depth-wise stabilization of token predictions, DTR provides a more reliable signal of effective reasoning than surface-level proxies such as token length or confidence. Building on this insight, we proposed Think@ 𝑛 , a test-time scaling strategy that leverages DTR for early selection and aggregation, achieving comparable or better performance than standard self-consistency while substantially reducing inference cost. Together, our results suggest that measuring how models think internally, rather than how long they think, is a promising direction. Future work may leverage this insight to explore how effective reasoning is characterized-shifting the focus from generating longer chains of thought to inducing deeper, more computationally intensive reasoning, and potentially enabling more reliable and efficient reasoning models.

## Acknowledgements

We thank Congchao Wang and colleagues from Google AIR for their valuable support. We also thank Yu-Min Tseng from Virginia Tech and members of Meng-Lab at UVA for their helpful discussion.

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

## A. Comparison of Different Distance Metrics for DTR

Our method (Section 2) adopts Jensen-Shannon divergence (JSD) to quantify the discrepancy between intermediate-layer and final-layer predictions and compute DTR. Alternative notions of distance are possible. Here we explore two additional metrics: Kullback-Leibler divergence (KLD) and cosine similarity. The results are presented in Figure 6.

Kullback-Leibler divergence. By replacing JSD with KLD in Equation (2), we compute the divergence between the final-layer distribution 𝑝𝑡,𝐿 and the intermediate-layer distribution 𝑝𝑡,𝑙 as

<!-- formula-not-decoded -->

Cosine similarity. Wereplace the distributional comparison defined in Section 2.2 with a representationspace measure using cosine similarity. Instead of projecting intermediate-layer hidden states into the vocabulary space via the shared unembedding matrix 𝑊𝑈 (Equation (1)), we directly compute the cosine similarity between the intermediate-layer hidden state ℎ𝑡,𝑙 and the final-layer hidden state ℎ𝑡,𝐿 . The distance is defined as

<!-- formula-not-decoded -->

For both KLD and cosine similarity, we then apply the same configurations in Section 2.2 to identify deep-thinking tokens and compute KLD-based DTR and cosine-based DTR.

Results. We report the correlation results of KLD-based and cosine-based DTR, compared with our main JSD-based DTR method, on AIME 25 and HMMT 25 using OSS-120Bmedium . Across both datasets, JSD-based DTR consistently achieves the strongest positive correlation with accuracy ( 𝑟 = 0.869 on AIME 25; 𝑟 = 0.895 on HMMT 25), justifying its use in our definition of DTR in Section 2. In contrast, cosine-based DTR exhibits substantially weaker and unstable correlations ( 𝑟 = 0.633 on AIME 25 and only 𝑟 = 0.172 on HMMT 25). KLD-based DTR shows similarly inconsistent behavior, with a negative correlation on AIME 25 ( 𝑟 = -0.698) and a modest positive correlation on HMMT 25 ( 𝑟 = 0.409). This inconsistency may stem from the asymmetric and numerically unstable nature of KLD: early-layer predictions tend to be high-entropy and relatively flat, assigning probability mass to many tokens that are later driven to near-zero values. Consequently, KLD can become artificially small, making the measure highly sensitive.

## B. DTR Under Different GPT-OSS Reasoning Levels

Figure 7 illustrates how DTR varies in different reasoning-level configurations (i.e., low, medium, and high) of the GPT-OSS-120B model. We observe an interesting and consistent trend on both AIME 25 and GPQA-D: although the underlying model weights remain identical and only the system prompt differs, lower reasoning-level configurations exhibit higher DTR values, whereas higher reasoning-level configurations yield systematically smaller DTR while achieving better task accuracy.

A potential explanation is that higher reasoning levels may redistribute computation from depth to sequence length, effectively flattening per-token, layer-wise computation. Models with higher reasoning levels require less deep revision for each individual token but instead generate longer reasoning chains with more forward passes, resulting in greater total effective compute and improved

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

(a) Cosine similarity as the distance metric on AIME 25.

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

(d) Cosine similarity as the distance metric on HMMT 25.

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

(e) KL divergence as the distance metric on HMMT 25.

(c) JS divergence as the distance metric on AIME 25.

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

(f) JS divergence as the distance metric on HMMT 25.

Figure 6 | Comparison of correlation between accuracy and deep-thinking ratio (DTR) using different distance metrics (cosine similarity, KL divergence, and JS divergence) on AIME 25 ( top row ) and HMMT 25 ( bottom row ).

task performance. Since DTR is defined as the proportion of deep-thinking tokens ( i.e. , averaged over the total number of generated tokens), longer sequences increase the denominator in the DTR calculation and thus produce smaller values. This also suggests DTR might not be directly comparable across different models or model modes.

## C. Additional Analysis of Think@ 𝒏

Here we provide additional analysis on how Think@ 𝑛 behaves when varying (i) the number of sampled responses 𝑛 and (ii) the retained top𝜂 percentage used for voting.

Effect of the number of samples n . Figure 8a compares Think@ 𝑛 against Cons@ 𝑛 ( i.e. , selfconsistency) as 𝑛 increases ( 𝑛 ∈ { 16 , 32 , 48 }) . Think@ 𝑛 improves monotonically with larger 𝑛 , where the advantage over Cons@ 𝑛 becomes more pronounced. Sampling more responses makes the correct cluster of answers to be larger and more likely to appear. Think@ 𝑛 is able to exploit this enlarged candidate pool by preferentially selecting better samples, leading to stronger performance gains over Cons@ 𝑛 .

Effect of top𝜼 percentage. Figure 8a evaluates Think@ 𝑛 under different top𝜂 percent ( 𝜂 ∈ { 25% , 50% , 75% } ). Performance peaks at 𝜂 =50%, while decrease for a smaller fraction ( 𝜂 =25%)

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

Figure 7 | Deep-thinking ratio (DTR) under different reasoning level configurations of OSS-120B models.

![Image](paper_artifacts/image_000008_dd1ead7c4a2e268138baa900ef80cac65734bc56d8eaa99bc84782927d59cd06.png)

- (a) Comparison of different number of samples 𝑛 .
- (b) Comparison of different top𝜂 percentage.

![Image](paper_artifacts/image_000009_25e10e26020f3719fffc0a8083dd471dc9951ac4829acf6832fbf5e6626892d5.png)

Figure 8 | Analysis of Think@ 𝑛 with different number of samples 𝑛 and top𝜂 percent. (a) As 𝑛 increases, Think@ 𝑛 consistently benefits from larger candidate pools and exhibits a widening performance gap over Cons@ 𝑛 at higher 𝑛 . (b) Performance peaks at 𝜂 =50%, while overly aggressive filtering and overly permissive selection could lead to degraded accuracy.

and a larger fraction ( 𝜂 =75%). This suggests a trade-off: selecting too few samples reduces voting robustness, potentially with fewer strong candidates to stabilize majority vote, whereas selecting too many might admit lower-quality samples that dilute the benefit of Think@ 𝑛 . Overall, the results support our choice of 𝜂 =50% as a stable operating point.

## D. Prompts

We provide the prompts adopted in our experiments for math tasks (AIME 2024, AIME 2025, HMMT 2025) in Table 4 and for GPQA in Table 5.

## Table 4 | Inference prompt for math tasks (AIME 2024, AIME 2025, HMMT 2025).

## Prompt for AIME 2024, AIME 2025, HMMT 2025

Please reason step by step, and put your final answer within \ boxed {} .

## Table 5 | Inference prompt for GPQA.

## Prompt for GPQA

You will be given a multiple choice question with different choices such as (A), (B), (C), (D). Think step by step before giving a final answer to this question. Always finish your answer with 'The final answer is \ boxed { (X) } .', where X is the correct answer choice. If none of the options match, choose the closest option as the final answer.

## E. Qualitative Examples

We present an example question from the AIME 2025 dataset along with its ground-truth answer (Table 6), and two outputs from OSS-120medium : one incorrect (Table 7) and one correct (Table 8). Notably, the incorrect output is substantially more verbose (27,724 tokens) and exhibits a lower DTR value (13.9), whereas the correct output is much more concise (3,725 tokens) and achieves a higher DTR value (19.0).

Table 6 | An example question and its ground-truth answer from AIME 2025.

## Example question from AIME 2025.

Circle 𝜔 1 with radius 6 centered at point 𝐴 is internally tangent at point 𝐵 to circle 𝜔 2 with radius 15. Points 𝐶 and 𝐷 lie on 𝜔 2 such that 𝐵𝐶 is a diameter of 𝜔 2 and 𝐵𝐶 ⊥ 𝐴𝐷 . The rectangle 𝐸𝐹𝐺𝐻 is inscribed in 𝜔 1 such that 𝐸𝐹 ⊥ 𝐵𝐶 , 𝐶 is closer to 𝐺𝐻 than to 𝐸𝐹 , and 𝐷 is closer to 𝐹𝐺 than to 𝐸𝐻 , as shown. Triangles △ 𝐷𝐺𝐹 and △ 𝐶𝐻𝐺 have equal areas. The area of rectangle 𝐸𝐹𝐺𝐻 is 𝑚 𝑛 , where 𝑚 and 𝑛 are relatively prime positive integers. Find 𝑚 + 𝑛 .

## Ground truth answer.

293

## Table 7 | An incorrect output of OSS-120Bmedium to the example question.

## Incorrect output with DTR = 13.9% and token count = 27,724.

We need to interpret geometry. Setup: Circle 𝜔 1 radius 6 centered at A, internally tangent to larger circle 𝜔 2 radius 15 at point B. So B is common point where 𝜔 1 touches inside 𝜔 2 . Since internal tangency, distance AB = 15-6 = 9, with B on line AB.

Let's set coordinate system. Place A at origin? maybe easier: Let 𝜔 1 centered at (0,0) radius 6. Then B is on circle 𝜔 1 and also on 𝜔 2 . Since 𝜔 2 larger radius 15 and centered at O? Let's denote O is center of 𝜔 2 . Distance OA = 9 (since AB = 9) and AB =9? Wait AB = distance between centers = 15-6 = 9 yes. B lies on line OA, outside? Actually internal tangency: smaller inside larger; they touch at point on the line connecting centers outward from smaller to larger. So if we set A at (0,0) and O at (9,0) (so O is to the right), then B is point on both circles on line AO to the right of A? The point outward from A towards O at distance 6 from A, i.e., B is at (6,0). Indeed distance from O to B: O(9,0) to B(6,0) distance 3 which is radius 15? Wait radius of 𝜔 2 is 15, O to B should be 15. But O(9,0) to B(6,0) distance 3, not 15. Something wrong.

Let's set O to be (0,0) maybe easier. Place 𝜔 2 centered at O (0,0), radius 15. 𝜔 1 radius 6 internally tangent at B; its center A is distance 15-6 = 9 from O, along some direction. Choose B as point of tangency on line OA outward from A to O? Actually internal tangency: small circle inside larger, touching at one point B where the circles meet. The line of centers passes through B. The distance from O to B is 15 (radius). The distance from A to B is 6. Since O to A is 9. B is on the line OA beyond A? Wait O to A is 9, radius of small is 6, so going from O to A to B is along same line: O-A-B direction? Since B is on circumference of both circles. The distance from O to B = 15 = OA + AB? OA=9, AB=6 gives OA+AB=15 so yes B is outward from O through A. So O at origin, A at distance 9 from O in direction e.g., positive x. Let O at (0,0), A at (9,0). Then B is further along x axis at O to B distance 15, so B at (15,0). Check: distance from A (9,0) to B (15,0) =6 correct. Good.

Now BC is a diameter of 𝜔 2 , meaning B to C passes through O (center of 𝜔 2 ). Since B is at (15,0), the opposite point on 𝜔 2 is at C at (-15,0) (diameter through O). So C is at (-15,0). So line BC is along x-axis.

Now rectangle EFGH is inscribed in 𝜔 1 (center A (9,0) radius 6). The rectangle is oriented not necessarily axis-aligned? We have EF parallel to GH, FG parallel to EH. Given EF ⊥ BC (BC horizontal), so EF (and GH) are vertical? Wait EF is perpendicular to BC, which is horizontal, so EF is vertical. So one side of rectangle is vertical. Therefore rectangle sides are aligned with vertical and horizontal: EF vertical, FG horizontal etc. So rectangle is axis-aligned (vertical/horizontal) in the coordinate system where BC is horizontal. Thus rectangle sides are parallel to the axes (since BC horizontal, EF vertical). Good.

Given BC ⊥ AD, so AD is perpendicular to x-axis, meaning AD is vertical line through A? Wait AD segment connects A (9,0) to D point on 𝜔 2 , such that AD is perpendicular to BC i.e., vertical line through A (x=9). Since AD must intersect 𝜔 2 at point D. So D is point where vertical line x=9 meets 𝜔 2 (radius 15). Equation x 2 + y 2 = 225. Substituting x=9 =&gt;81 + y 2 =225 =&gt; y 2 =144 =&gt; y= ±12. Which one? Since orientation maybe D is above? Not specified. We'll consider D at (9,12) (upper) maybe. Could also be lower but rectangle orientation may pick one.

Now C is closer to GH than to EF. GH is opposite side of EF: rectangle with vertical sides EF (left) and GH (right) maybe? Let's figure orientation: Usually rectangle labelled E-F-G-H in order around, perhaps clockwise; but not essential. If EF is vertical, then FG is horizontal, GH vertical, HE horizontal. So EF left side, GH right side (if rectangle sits to the right of EF). Not sure.

Similarly, D is closer to FG than to EH. Since FG is top side (horizontal), EH bottom side (horizontal). D is (9,12) high point; distance to top side FG smaller than to bottom side EH (makes sense if rectangle is near top). So FG is top side, EH bottom side. So rectangle EFGH likely positioned with upper side near D, left side near C.

C is at (-15,0) far left of both. "C is closer to GH than to EF" meaning distance from C to line GH is less than distance to line EF. Since C is far left, that would mean GH is left side, EF right side? Wait distance from C to a vertical line is horizontal distance. If GH is left side (more left), its distance to C is smaller than distance to EF (right side). That matches C being closer to GH. So GH is left side of rectangle (more left), EF right side. Good.

## ... Omitted for illustrative purposes ...

Seems no integer factorization. Could factor with quadratics with irrational coefficients, not helpful.

Given complexity, I think answer maybe m+n = something like 207? Let's guess? Not good. Given limited time, I will output placeholder.

Thus x may be irrational; thus k not integer rational. Therefore area is irrational? Conflict with problem statement. Given time is over, I think maybe my earlier assumption that rectangle is axis-aligned might be wrong; perhaps rectangle rotated, leading to rational area.

assistantfinal 207

## Table 8 | A correct output of OSS-120Bmedium to the example question.

## Correct output with DTR = 19.0% and token count = 3,725.

We need to parse geometry. Let's define coordinates.

Let's set coordinate system: Let AB be vertical? Choose B at origin maybe easier.

We have two circles: 𝜔 2 radius 15, 𝜔 1 radius 6 centered at A, internally tangent at point B. So A is inside 𝜔 2 , distance AB = radius difference = 15 - 6 = 9. B is the point of tangency, along line AB.

Let's position 𝜔 2 centered at O (call it O2) maybe O? Actually 𝜔 2 's center is some point O (call it O). 𝜔 1 's center A is at distance 9 from O, with B being point on both circles along line O-A.

Now Points C and D lie on 𝜔 2 such that BC is a diameter of 𝜔 2 . So BC passes through center O and length 30 (diameter). Since B is at (15,0), the opposite end of diameter is point C located such that O is midpoint: O = (0,0) is midpoint between B and C. So C = (-15,0). Indeed because B (15,0) opposite across origin yields C (-15,0). So BC is horizontal line (x-axis). Good.

Let's place O at (0,0). Let AB be along positive x-axis: place B at (15,0) maybe? Then 𝜔 2 radius 15 centered at O (0,0). If B is point of tangency where 𝜔 1 touches 𝜔 2 internally, then B lies on 𝜔 2 at distance 15 from O. So B at (15,0). Then A is located on line OB, inside, distance 6 from B (since radius of 𝜔 1 is 6). And O to A distance is 9 (since OA = 15-6 = 9). So O (0,0), B (15,0). Then A is at (9,0) (since O to A is 9 along same line). Yes A at (9,0). Then 𝜔 1 radius 6 centered at (9,0). Good.

- ... Omitted for illustrative purposes ...
- *Triangle 𝐷𝐺𝐹 :* Its base 𝐺𝐹 has length 𝑤 ; the vertical distance from 𝐷 ( 9 , 12 ) to the line 𝑦 = ℎ / 2 (the line containing 𝐺𝐹 ) is 12 -ℎ 2 . Hence

<!-- formula-not-decoded -->

*Triangle 𝐶𝐻𝐺 :* Side 𝐻𝐺 is vertical with length ℎ ; the horizontal distance from 𝐶 (-15 , 0 ) to the line 𝑥 = 9 -𝑤 2 (the line containing 𝐻𝐺 ) is 24 -𝑤 2 . Hence

<!-- formula-not-decoded -->

The problem states [ 𝐷𝐺𝐹 ] = [ 𝐶𝐻𝐺 ] . Cancelling the factor 1 2 gives

<!-- formula-not-decoded -->

The terms -𝑤ℎ 2 appear on both sides and cancel, leaving

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

-

Solving for 𝑤 and ℎ Substituting (2) into (1):

Hence

The area of rectangle 𝐸𝐹𝐺𝐻 is

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Thus 𝑚 = 288 , 𝑛 = 5 (relatively prime), and

<!-- formula-not-decoded -->

293