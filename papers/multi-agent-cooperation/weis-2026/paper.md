![Image](paper_artifacts/image_000000_73ceca6f21f2685db190ec1d8849c1bbc340a27392bfca88d03fb7f3e6a453da.png)

## Multi-agent cooperation through in-context co-player inference

Marissa A. Weis ★ ,1 , Maciej Wołczyk ★ ,1 , Rajai Nasser 1 , Rif A. Saurous 1 , Blaise Agüera y Arcas 1,2

João Sacramento and Alexander Meulemans

, 1 1

1 Google, Paradigms of Intelligence Team, 2 Santa Fe Institute, ★ Equal contribution

Achieving cooperation among self-interested agents remains a fundamental challenge in multi-agent reinforcement learning. Recent work showed that mutual cooperation can be induced between 'learningaware' agents that account for and shape the learning dynamics of their co-players. However, existing approaches typically rely on hardcoded, often inconsistent, assumptions about co-player learning rules or enforce a strict separation between 'naive learners' updating on fast timescales and 'meta-learners' observing these updates. Here, we demonstrate that the in-context learning capabilities of sequence models allow for co-player learning awareness without requiring hardcoded assumptions or explicit timescale separation. We show that training sequence model agents against a diverse distribution of co-players naturally induces in-context best-response strategies, effectively functioning as learning algorithms on the fast intra-episode timescale. We find that the cooperative mechanism identified in prior work-where vulnerability to extortion drives mutual shaping-emerges naturally in this setting: in-context adaptation renders agents vulnerable to extortion, and the resulting mutual pressure to shape the opponent's in-context learning dynamics resolves into the learning of cooperative behavior. Our results suggest that standard decentralized reinforcement learning on sequence models combined with co-player diversity provides a scalable path to learning cooperative behaviors.

## 1. Introduction

The development of foundation model agents is rapidly shifting the landscape of artificial intelligence from isolated systems to interacting autonomous agents (Aguera Y Arcas et al., 2026; Park et al., 2023; Xi et al., 2023). As these sequence-model-based agents are deployed in increasingly complex environments, they inevitably face multi-agent interactions where outcomes depend on interactions of multiple entities. Because these interactions frequently involve competing goals, ensuring that selfinterested agents robustly cooperate in mixed-motive settings remains an important open challenge, even as individual agent capabilities have grown significantly.

Decentralized Multi-Agent Reinforcement Learning (MARL) addresses the problem of learning to interact with other agents while only having access to local observations. However, decentralized MARL is challenging due to two primary factors: equilibrium selection and non-stationarity of the environment (Hernandez-Leal et al., 2017; Shoham &amp; Leyton-Brown, 2008). In general-sum games, many Nash equilibria may exist, and agents independently optimizing their own rewards frequently converge to suboptimal outcomes, such as mutual defection in social dilemmas (Claus &amp; Boutilier, 1998; Foerster et al., 2018). Furthermore, from the perspective of a single agent, the environment is non-stationary because other agents are simultaneously learning and adapting their policies (Hernandez-Leal et al., 2017). Since standard single-agent reinforcement learning (RL) algorithms assume stationarity, they often fail to learn effective policies in these decentralized settings (Claus &amp; Boutilier, 1998; Foerster et al., 2018).

To address this non-stationarity, co-player learning awareness enables agents to anticipate the learning dynamics of other agents and shape their co-players' learning toward more beneficial equilibria (Agha-

johari et al., 2024a,b; Balaguer et al., 2022; Cooijmans et al., 2023; Duque et al., 2024; Foerster et al., 2018; Khan et al., 2024; Lu et al., 2022; Meulemans et al., 2025a; Piche et al., 2025; Segura et al., 2025; Willi et al., 2022; Xie et al., 2021). These approaches generally fall into two categories. The first explicitly models the co-player's learning update, estimating a shaping gradient by differentiating through the opponent's update step (Aghajohari et al., 2024a,b; Cooijmans et al., 2023; Duque et al., 2024; Foerster et al., 2018; Piche et al., 2025; Willi et al., 2022). However, this requires rigid assumptions about the opponent's learning rule and creates inconsistencies if the opponent is also learning-aware. The second category implicitly learns to shape opponents by extending the RL time horizon to encompass multiple update steps of the co-player (Khan et al., 2024; Lu et al., 2022; Meulemans et al., 2025a; Segura et al., 2025). While effective, this requires a separation of agents into 'naive learners' (who update parameters frequently) and 'meta-learners' (who update slowly), effectively treating the interaction as a meta-learning problem (Bengio et al., 1990; Hochreiter et al., 2001; Schmidhuber, 1987).

Meulemans et al. (2025a) describe a three-step mechanism explaining why co-player learning awareness leads to the learning of cooperative behaviors among self-interested agents:

1. Extortion of naive learners: The optimal strategy against a naive learner (an agent updating its policy to maximize rewards on a fast timescale) is extortion (Press &amp; Dyson, 2012). A learningaware meta-agent shapes the interaction so the naive learner updates its policy towards more cooperation, allowing the meta-agent to exploit the resulting behavior.
2. Mutual extortion leads to cooperation: When two agents with such extortionate capabilities face each other, their attempts to shape the learning of one another result in both agents learning more cooperative strategies.
3. Heterogeneity is key: Consequently, cooperation emerges when agents are trained in a mixed population of naive learners and learning-aware agents. Interactions with naive learners provide the gradient pressure to learn extortion (avoiding mutual defection), while interactions with learning-aware agents refine this into mutual cooperation.

We argue that the complex mechanisms employed by current co-player learning-aware methods, such as explicit naive learners and meta learners, or differentiating through co-players' learning updates, are unnecessary for learning cooperative behaviors. We hypothesize that training sequence model agents via decentralized MARL against a diverse distribution of co-players naturally yields in-context best-response policies. These policies exhibit goal-directed adaptation through in-context learning within a single episode. Crucially, we show that this acts as a functional drop-in replacement for the 'naive learner' parameter updates of prior work. Because in-context learning occurs on a fast timescale within the episode, agents become susceptible to extortion by other learning agents using in-weight updates. Consequently, the cooperative gradient dynamics identified by Meulemans et al. (2025a) emerge: gradients incentivizing the extortion of in-context learners pull agents away from pure defection, while mutual extortion gradients drive them toward cooperation.

Our contributions are as follows. We introduce a decentralized MARL setup where sequence model agents are trained against a mixed pool of diverse co-players and demonstrate that this training distribution induces strong in-context co-player inference capabilities and thereby the mutual extortion pressures leading to cooperation. We show that this setup leads to robust cooperation in the Iterated Prisoner's Dilemma without the distinction between meta and inner trajectories, or assumptions about opponent learning rules. By bridging in-context learning and co-player learning-awareness, we provide a scalable path toward cooperative multi-agent systems using standard sequence modeling and RL. We introduce a new RL method that leverages self-supervised learning of predictive sequence models, which is well-suited to learn the in-context best-response policies required for the mixed pool

training. We provide a theoretical characterization of the training equilibrium of this method, and relate it to Nash equilibria and subjective embedded equilibria (Meulemans et al., 2025b).

## 2. Problem setup and methods

Partially observable stochastic games . We formalize the multi-agent interaction as a partially observable stochastic game (POSG; Kuhn, 1953) of 𝑁 agents. Each agent 𝑖 receives at each timestep an observation 𝑜 𝑖 𝑡 ∈ O 𝑖 and reward 𝑟 𝑖 𝑡 ∈ R 𝑖 , and executes an action 𝑎 𝑖 𝑡 ∈ A 𝑖 , with O 𝑖 , R 𝑖 and A 𝑖 being finite sets. Policies are conditioned on the interaction history 𝑥 𝑖 ≤ 𝑡 = {( 𝑜 𝑖 𝑘 , 𝑎 𝑖 𝑘 -1 , 𝑟 𝑖 𝑘 -1 )} 𝑡 𝑘 = 1 . We denote the policy of agent 𝑖 as 𝜋 𝑖 ( 𝑎 𝑖 𝑡 | 𝑥 𝑖 ≤ 𝑡 ; 𝜙 𝑖 ) , parameterized by 𝜙 𝑖 .

The iterated prisoner's dilemma . We focus on the Iterated Prisoner's Dilemma (IPD), a canonical model for studying cooperation among self-interested agents (Axelrod &amp; Hamilton, 1981; Rapoport, 1974). In each round 𝑡 , two agents choose simultaneously to cooperate (C) or defect (D), i.e., 𝑎 𝑖 𝑡 ∈ { C , D } , receiving payoffs as detailed in Tab. 1. This structure creates a social dilemma: in a single-shot game, mutual defection is the unique Nash equilibrium, even though mutual cooperation yields higher global and individual returns. While the infinitely iterated game allows for cooperative Nash equilibria, converging to these equilibria via decentralized reinforcement learning remains challenging (Claus &amp; Boutilier, 1998; Foerster et al., 2018). For computational tractability, we approximate the infinite horizon with a fixed horizon of 𝑇 = 100 steps, which is sufficient for the small-scale policy networks used in this work to approximate infinite-horizon behavior.

Mixed pool training . To induce robust in-context inference capabilities, we train agents within a mixed population rather than against a single fixed opponent. The training pool consists of (i) Learning Agents which use a sequence model policy that processes the full episode history 𝑥 𝑖 ≤ 𝑡 and whose parameters are learned during training, and (ii) static Tabular Agents parameterized by a 5-dimensional vector, defining the probability of cooperating in the initial state and in response to the four possible joint action outcomes of the previous turn ( 𝑎 𝑖 𝑡 -1 , 𝑎 -𝑖 𝑡 -1 ) . During training, a learning agent plays 50% of its episodes against another learning agent and 50% against a tabular agent sampled uniformly from the parameter space. Crucially, agents do not receive agent identifiers; they must infer the nature and strategy of their opponent solely from the interaction history 𝑥 𝑖 ≤ 𝑡 .

We investigate two learning algorithms for the learning agents in our pool:

Independent A2C. We employ Advantage Actor-Critic (A2C) (Mnih et al., 2016) as a standard decentralized model-free RL method. Each agent independently optimizes its policy parameters 𝜙 𝑖 to maximize its own expected return, treating the other agents as part of the environment.

Predictive Policy Improvement (PPI). We introduce a model-based algorithm that leverages a sequence model predicting the joint sequence of actions, observations, and rewards, serving simultaneously as a world model and a policy prior. This method is a variation of Maximum A-Posteriori Policy Optimization (Abdolmaleki et al., 2018, MPO), inspired by the MUPI framework for multi-agent learning (Meulemans et al., 2025b), and enables efficient learning of in-context inference mechanisms through self-supervised training. Each iteration consists of (i) gathering data with the improved policy and (ii) retraining the sequence model on the newly gathered data, similar to classical policy iteration. We define the improved policy 𝜋 𝑖 ( 𝑎 𝑖 | 𝑥 𝑖 ≤ 𝑡 ) as follows:

<!-- formula-not-decoded -->

where 𝛽 is an inverse temperature hyperparameter. The action value ˆ 𝑄𝑝 ( ℎ, 𝑎 ) is estimated via Monte Carlo rollouts performed within the sequence model 𝑝𝜙 . We deploy this improved policy 𝜋 𝑖 ( 𝑎 𝑖 | 𝑥 𝑖 ≤ 𝑡 ) in the games interacting with other agents, collecting a new batch of trajectories. We end the iteration by

Figure 1 | Mixed training leads to robust cooperation. RL agents trained against a mix of tabular policies and learning agents converge to cooperation (solid lines). Ablations: Agents trained purely against other learning agents (dotted lines) or with access to explicit co-player identifications (dashed lines) converge to defection, highlighting that in-context inference is a critical factor for the learning of cooperative behaviors with standard decentralized MARL. Error bars indicate standard deviation across 10 random seeds.

![Image](paper_artifacts/image_000001_82bd5cb673b727506892227b1a8ed992e8abc3975478e4566277a9628508eb50.png)

retraining the sequence model 𝑝 𝑖 𝜙 𝑖 on all accumulated trajectory batches of the current and previous iterations, distilling the improved behavior of 𝜋 𝑖 into the parameters 𝜙 𝑖 . We initialize the sequence model 𝑝𝜙 by pretraining on interactions between randomly sampled tabular agents. Refer to App. A for the implementation details, App. C for a theoretical derivation and motivation of PPI, and App. D for a theoretical analysis of the equilibrium behavior of PPI agents.

## 3. Results

Our central hypothesis is that training the learning agents against a diverse distribution of co-players necessitates the development of two distinct capabilities: (i) inferring the co-player's policy from interaction history, and (ii) adapting to a best response within a single episode. We posit that this in-context best-response policy makes the agent vulnerable to extortion, reproducing the 'naive learner' dynamics described by Meulemans et al. (2025a). This leads to learning pressures towards extortion policies, and subsequently, the mutual extortion between learning agents drives the agents toward cooperative policies. Interestingly, in this setup, the learning agents simultaneously occupy two roles traditionally separated in the literature: they are 'naive learners' on the fast timescale (via in-context learning) and 'learning-aware agents' on the slow timescale (via weight updates).

In this section, we first demonstrate that mixed-pool training indeed leads to robust cooperation without explicit time-scale separations or meta-gradient machinery. We then dissect the underlying mechanism, showing that (1) mixed pool training induces in-context best-response policies, (2) these policies are vulnerable to extortion, and (3) mutual extortion pressures resolve into learning cooperative behaviors.

## 3.1. Mixed training induces robust cooperation

As shown in Figure 1, both PPI and A2C agents trained in the mixed pool setup converge to cooperation in IPD. To verify this stems from the dynamics of in-context opponent inference, we perform two ablations: (1) Explicit Identification: We condition the policy on the opponent's policy parameters (for tabular opponents) or identity flag (for other learning agents) at the start of the episode, removing the need for in-context opponent inference. (2) No mixed pool training: We train agents solely against a single other learning agent (without the tabular agent pool or structured pretraining).

Figure 2 | A-B: Emergence of in-context best response. Performance of PPI agents (trained against random tabular opponents) when evaluated against specific fixed strategies. The agents demonstrate in-context learning, identifying the opponent and converging to the best response within the episode. C-D: Learning to extort in-context learners. Agents trained against a 'Fixed In-Context Learner' (an agent pre-trained in Step 1 to best-respond to tabular policies) learn to extort it. The RL agent achieves a higher share of the reward by exploiting the in-context adaptation of its opponent. E-F: From mutual extortion to cooperation. When two agents initialized with extortion policies (from Step 2) play against each other, their mutual attempts to extort their co-player result in the shaping of each other's policy towards more cooperative behavior, both within episodes through in-context learning ( F ) and across episodes through in-weight learning ( E ). Error bars indicate standard deviation across 10 random seeds.

![Image](paper_artifacts/image_000002_ef90b34409d5120145ef6e409642ff4219618bc2bdcb48f03755adccb9b30dcf.png)

Without diverse opponents, agents have no incentive to develop general-purpose in-context learning mechanisms. In both ablations, agents collapse to mutual defection (c.f. Fig. 1; dashed and dotted curves). This confirms that in-context learning mechanisms-induced by the necessity to identify diverse opponents-are a critical factor enabling cooperative outcomes. Refer to App. A.4 for the ablation details.

## 3.2. Mechanism analysis: From in-context learning to cooperation

We now deconstruct the learning of cooperative behavior into three distinct steps, validating the causal chain from diversity to in-context learning, to extortability, and finally to cooperation.

Step 1: Diversity induces in-context best-response mechanisms. First, we verify that training against the tabular pool cultivates in-context learning. We evaluate a PPI agent trained solely against the tabular agents pool. Figure 2 B plots the agent's performance against specific tabular policies over

the course of an episode. The agent rapidly adapts to the best response for the specific opponent. This confirms the emergence of in-context best-response mechanisms that perform goal-directed adaptation on the fast timescale of the episode.

Step 2: In-context learners are vulnerable to extortion. Next, we establish that such in-context best-response policies are susceptible to shaping by other co-players. We freeze the agent from Step 1, termed the "Fixed In-Context Learner" (Fixed-ICL), and train a new PPI agent solely against it. The new agent learns to extort the Fixed-ICL policy (Fig. 2 C &amp; D ) (Press &amp; Dyson, 2012). By exploiting the Fixed-ICL's tendency to adapt, the new agent forces it into unfair cooperation, maximizing the new agent's own reward at the expense of the Fixed-ICL. This confirms that goal-directed adaptation within the episode provides the necessary gradient signal for opponents to learn extortionate behaviors via weight updates.

Step 3: Mutual extortion drives cooperation. We initialize two agents with the extortion policies learned in Step 2 and train them against each other. Within an episode, both extortion policies shape each others in-context learning dynamics into more cooperative behavior (Fig. 2 F ). This push towards more cooperation is then picked up by the parameter updates, further driving both policies towards cooperative behavior (Fig. 2 E ), mirroring the "mutual shaping" effect observed in explicit learning-aware methods (Lu et al., 2022; Meulemans et al., 2025a).

Step 4: Synthesis in mixed populations. Mixed-pool training combines these dynamics by forcing agents to maintain in-context adaptation for tabular opponents, which renders them vulnerable to mutual extortion by other learners, ultimately driving the learning agents toward cooperation through mutual extortion (Sec. 3.1; Fig. 1 &amp; Fig. 3). Figure 4 in Appendix B.2 shows similar results for A2C learning agents.

## 4. Conclusion

In this work, we have demonstrated that the complex machinery of explicit co-player learningawareness-such as meta gradients or rigid timescale separation-is not required to learn cooperative behaviors in general-sum games. Instead, we found that simply training agents against a diverse distribution of co-players suffices to induce in-context best-response strategies. This in-context learning renders agents susceptible to shaping and consequently driving them toward cooperative behaviors through mutual extortion dynamics. Crucially, this result bridges the gap between multi-agent reinforcement learning and the training paradigms of modern foundation models. Since foundation models naturally exhibit in-context learning and are trained on diverse tasks and behaviors, our findings suggest a scalable and computationally efficient path for the emergence of cooperative social behaviors using standard decentralized learning techniques.

## Acknowledgments

We would like to thank Guillaume Lajoie, Angelika Steger and the Google Paradigms of Intelligence team for feedback and insightful discussions.

## References

Abbas Abdolmaleki, Jost Tobias Springenberg, Yuval Tassa, Remi Munos, Nicolas Heess, and Martin Riedmiller. Maximum a posteriori policy optimisation. arXiv preprint arXiv:1806.06920 , 2018.

- Milad Aghajohari, Tim Cooijmans, Juan Agustin Duque, Shunichi Akatsuka, and Aaron Courville. Best response shaping. arXiv preprint arXiv:2404.06519 , 2024a.
- Milad Aghajohari, Juan Agustin Duque, Tim Cooijmans, and Aaron Courville. Loqa: Learning with opponent q-learning awareness. arXiv preprint arXiv:2405.01035 , 2024b.
- Blaise Aguera Y Arcas, Benjamin Bratton, and James Evans. The silicon interior, feb 2026. URL https://antikythera.substack.com/p/the-silicon-interior . Accessed: 2026-2-12.
- Robert Axelrod and William D. Hamilton. The evolution of cooperation. Science , 211(4489):13901396, March 1981.
- Jan Balaguer, Raphael Koster, Christopher Summerfield, and Andrea Tacchetti. The good shepherd: An oracle agent for mechanism design. arXiv preprint arXiv:2202.10135 , 2022.
- Yoshua Bengio, Samy Bengio, and Jocelyn Cloutier. Learning a synaptic learning rule. Technical report, Université de Montréal, Département d'Informatique et de Recherche opérationnelle, 1990.
- James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. JAX: composable transformations of Python+NumPy programs, 2018.
- Caroline Claus and Craig Boutilier. The dynamics of reinforcement learning in cooperative multiagent systems. AAAI/IAAI , 1998(746-752):2, 1998.
- Tim Cooijmans, Milad Aghajohari, and Aaron Courville. Meta-value learning: a general framework for learning with learning awareness. arXiv preprint arXiv:2307.08863 , 2023.
- DeepMind, Igor Babuschkin, Kate Baumli, Alison Bell, Surya Bhupatiraju, Jake Bruce, Peter Buchlovsky, David Budden, Trevor Cai, Aidan Clark, Ivo Danihelka, Antoine Dedieu, Claudio Fantacci, Jonathan Godwin, Chris Jones, Ross Hemsley, Tom Hennigan, Matteo Hessel, Shaobo Hou, Steven Kapturowski, Thomas Keck, Iurii Kemaev, Michael King, Markus Kunesch, Lena Martens, Hamza Merzic, Vladimir Mikulik, Tamara Norman, George Papamakarios, John Quan, Roman Ring, Francisco Ruiz, Alvaro Sanchez, Laurent Sartran, Rosalia Schneider, Eren Sezener, Stephen Spencer, Srivatsan Srinivasan, Miloš Stanojević, Wojciech Stokowiec, Luyu Wang, Guangyao Zhou, and Fabio Viola. The DeepMind JAX Ecosystem, 2020. URL http://github.com/google-deepmind .
- Juan Agustin Duque, Milad Aghajohari, Tim Cooijmans, Razvan Ciuca, Tianyu Zhang, Gauthier Gidel, and Aaron Courville. Advantage alignment algorithms. arXiv preprint arXiv:2406.14662 , 2024.
- Jakob Foerster, Richard Y. Chen, Maruan Al-Shedivat, Shimon Whiteson, Pieter Abbeel, and Igor Mordatch. Learning with opponent-learning awareness. In International Conference on Autonomous Agents and Multiagent Systems , 2018.
- Charles R. Harris, K. Jarrod Millman, Stéfan J. van der Walt, Ralf Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, Julian Taylor, Sebastian Berg, Nathaniel J. Smith, Robert Kern, Matti Picus, Stephan Hoyer, Marten H. van Kerkwijk, Matthew Brett, Allan Haldane, Jaime Fernández del Río, Mark Wiebe, Pearu Peterson, Pierre Gérard-Marchant, Kevin Sheppard, Tyler Reddy, Warren Weckesser, Hameer Abbasi, Christoph Gohlke, and Travis E. Oliphant. Array programming with NumPy. Nature , 585(7825):357-362, 2020.
- Jonathan Heek, Anselm Levskaya, Avital Oliver, Marvin Ritter, Bertrand Rondepierre, Andreas Steiner, and Marc van Zee. Flax: A neural network library and ecosystem for JAX, 2024. URL http: //github.com/google/flax .

- Pablo Hernandez-Leal, Michael Kaisers, Tim Baarslag, and Enrique Munoz De Cote. A survey of learning in multiagent environments: Dealing with non-stationarity. arXiv preprint arXiv:1707.09183 , 2017.
- Sepp Hochreiter, A. Steven Younger, and Peter R. Conwell. Learning to learn using gradient descent. In International Conference on Artificial Neural Networks , Lecture Notes in Computer Science. Springer, 2001.
- J. D. Hunter. Matplotlib: A 2D graphics environment. Computing in Science &amp; Engineering , 9(3): 90-95, 2007.
- Sham Kakade and John Langford. Approximately optimal approximate reinforcement learning. In Proceedings of the nineteenth international conference on machine learning , pp. 267-274, 2002.
- Akbir Khan, Timon Willi, Newton Kwan, Andrea Tacchetti, Chris Lu, Edward Grefenstette, Tim Rocktäschel, and Jakob N. Foerster. Scaling opponent shaping to high dimensional games. In International Conference on Autonomous Agents and Multiagent Systems , 2024.
- H. W. Kuhn. Extensive games and the problem of information . Princeton University Press, 1953.
- Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101 , 2017.
- Christopher Lu, Timon Willi, Christian A Schroeder De Witt, and Jakob Foerster. Model-free opponent shaping. In International Conference on Machine Learning , 2022.
- Alexander Meulemans, Seijin Kobayashi, Johannes von Oswald, Nino Scherrer, Eric Elmoznino, Blake Richards, Guillaume Lajoie, João Sacramento, et al. Multi-agent cooperation through learningaware policy gradients. ICLR , 2025a.
- Alexander Meulemans, Rajai Nasser, Maciej Wołczyk, Marissa A. Weis, Seijin Kobayashi, Blake Richards, Guillaume Lajoie, Angelika Steger, Marcus Hutter, James Manyika, Rif A. Saurous, João Sacramento, and Blaise Agüera y Arcas. Embedded universal predictive intelligence: a coherent framework for multi-agent learning, 2025b.
- Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu. Asynchronous methods for deep reinforcement learning. In International Conference on Machine Learning , 2016.
- Joon Sung Park, Joseph O'Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology , 2023.
- Juan Perdomo, Tijana Zrnic, Celestine Mendler-Dünner, and Moritz Hardt. Performative prediction. In International Conference on Machine Learning , pp. 7599-7609. PMLR, 2020.
- Dereck Piche, Mohammed Muqeeth, Milad Aghajohari, Juan Duque, Michael Noukhovitch, and Aaron Courville. Learning robust social strategies with large language models. arXiv preprint arXiv:2511.19405 , 2025.
- William H. Press and Freeman J. Dyson. Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent. Proceedings of the National Academy of Sciences , 109(26):10409-10413, 2012.

- Prajit Ramachandran, Barret Zoph, and Quoc V. Le. Searching for activation functions. arXiv preprint arXiv:1710.05941 , 2017.
- Anatol Rapoport. Prisoner's dilemma-recollections and observations. In Game Theory as a Theory of a Conflict Resolution , pp. 17-34. Springer, 1974.
- Jürgen Schmidhuber. Evolutionary principles in self-referential learning, or on learning how to learn: the meta-meta-... hook . Diploma thesis, Institut für Informatik, Technische Universität München, 1987.
- John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation. arXiv preprint arXiv:1506.02438 , 2015.
- Marta Emili Garcia Segura, Stephen Hailes, and Mirco Musolesi. Opponent shaping in llm agents. arXiv preprint arXiv:2510.08255 , 2025.
- Yoav Shoham and Kevin Leyton-Brown. Multiagent systems: Algorithmic, game-theoretic, and logical foundations . Cambridge University Press, 2008.
- Michael L. Waskom. seaborn: statistical data visualization. Journal of Open Source Software , 6(60): 3021, 2021. doi: 10.21105/joss.03021. URL https://doi.org/10.21105/joss.03021 .
- Wes McKinney. Data Structures for Statistical Computing in Python. In Stéfan van der Walt and Jarrod Millman (eds.), Proceedings of the 9th Python in Science Conference , pp. 56 - 61, 2010. doi: 10.25080/Majora-92bf1922-00a.
- Timon Willi, Alistair Hp Letcher, Johannes Treutlein, and Jakob Foerster. COLA: consistent learning with opponent-learning awareness. In International Conference on Machine Learning , 2022.
- Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, Rui Zheng, Xiaoran Fan, Xiao Wang, Limao Xiong, Yuhao Zhou, Weiran Wang, Changhao Jiang, Yicheng Zou, Xiangyang Liu, Zhangyue Yin, Shihan Dou, Rongxiang Weng, Wensen Cheng, Qi Zhang, Wenjuan Qin, Yongyan Zheng, Xipeng Qiu, Xuanjing Huang, and Tao Gui. The rise and potential of large language model based agents: a survey. arXiv preprint arXiv:2309.07864 , 2023.
- Annie Xie, Dylan Losey, Ryan Tolsma, Chelsea Finn, and Dorsa Sadigh. Learning latent representations to influence multi-agent interaction. In Conference on Robot Learning , 2021.

## A. Additional details on methods

## A.1. Partially observable stochastic games

We formalize the multi-agent interaction as a partially observable stochastic game (POSG; Kuhn, 1953) defined by the tuple (I , S , A , 𝑃 𝑡 , 𝑃 𝑟 , 𝑃 𝑖 , O , 𝑃 𝑜 , 𝛾, 𝑇 ) . Here, I = { 1 , . . . , 𝑛 } is the set of 𝑛 agents. At each time step 𝑡 , the environment is in state 𝑠 𝑡 ∈ S . Agents simultaneously select actions from the joint action space A = × 𝑖 ∈I A 𝑖 , transitioning the environment according to 𝑃𝑡 ( 𝑆𝑡 + 1 | 𝑆𝑡 , 𝐴 𝑡 ) . The initial state is sampled from 𝑃𝑖 ( 𝑠 0 ) . Each agent 𝑖 receives a reward 𝑟 𝑖 𝑡 from the joint factorized distribution 𝑃𝑟 = × 𝑖 ∈I 𝑃 𝑖 𝑟 ( 𝑟 𝑖 | 𝑠, 𝑎 ) , and an observation 𝑜 𝑖 𝑡 from the observation space O = × 𝑖 ∈I O 𝑖 via the distribution 𝑃𝑜 ( 𝑜𝑡 | 𝑠 𝑡 , 𝑎 𝑡 -1 ) . We denote the discount factor by 𝛾 and the horizon by 𝑇 . We use the superscript 𝑖 to denote variables specific to agent 𝑖 , and -𝑖 for the remaining agents. Policies are conditioned on the interaction history 𝑥 𝑖 ≤ 𝑡 = {( 𝑜 𝑖 𝑘 , 𝑎 𝑖 𝑘 -1 , 𝑟 𝑖 𝑘 -1 )} 𝑡 𝑘 = 1 . We denote the policy of agent 𝑖 as 𝜋 𝑖 ( 𝑎 𝑖 𝑡 | 𝑥 𝑖 ≤ 𝑡 ; 𝜙 𝑖 ) , parameterized by 𝜙 𝑖 .

## A.2. Environment

Iterated Prisoners Dilemma (IPD) In each round both agents can output two possible actions: cooperate ( 𝐶 ) and defect ( 𝐷 ). As such, the environment emits five possible observations: the initial observation 𝑠 0 and four observations based on the actions the two players took in the previous round: ( 𝐶, 𝐶 ) , ( 𝐶, 𝐷 ) , ( 𝐷, 𝐶 ) , ( 𝐷, 𝐷 ) . The state 𝑠 𝑡 is then comprised of all past observations 𝑜 ≤ 𝑡 . While the tabular agents are only conditioned on the latest observation 𝑜𝑡 , the PPI and A2C agents leverage the full history 𝑥 ≤ 𝑡 . Each game consists of 100 rounds. Each agent observes the state of the previous round

Table 1 | Single-round IPD payoff matrix

![Image](paper_artifacts/image_000003_762e84cf8534444e5376d7626a971611db4e2c8f7aa35b19f7d39e5b3f656aae.png)

from a first person view, i.e., its own action is enumerated first. In every round, each agent receives a reward following the payoff matrix in Tab. 1.

## A.3. Agent implementations

## A.3.1. PPI agents

Predictive Policy Improvement (PPI) agents, our practical approximation of embedded Bayesian agents (Meulemans et al., 2025b), combine a learned sequence model with a planning-based policy improvement mechanism.

Sequence Model Architecture. The sequence model is a Gated Recurrent Unit (GRU) with a 128dimensional hidden state. Inputs-comprising observations, actions, and rewards-are processed via modality-specific linear layers to project them into a shared 32-dimensional embedding space; observations and actions are one-hot encoded prior to projection. These embeddings serve as inputs to the GRU, and we apply the Swish activation function (Ramachandran et al., 2017) on the output. Distinct linear output heads decode the hidden states to predict future tokens for each modality.

Training Objectives. We train the sequence model iteratively for 30 phases. In each phase, the model parameters 𝜙 are re-initialized and trained on a dataset of interaction histories D = { 𝑥 ( 𝑛 ) } 𝑁 𝑛 = 1 to minimize the next-token prediction loss:

## Algorithm 1 Predictive Policy Improvement

Require: Initial sequence model 𝑝𝜙 0 , reinforcement learning environment E , number of iterations 𝑁 𝑁 𝑁 D

```
iter, number of training epochs epochs, number of samples samples , initial dataset 0 1: for 𝑘 = 1 to 𝑁 iter do 2: Initialize weights 𝜙𝑘 of 𝑝𝜙𝑘 randomly 3: for 𝑒 = 1 to 𝑁 epochs do ⊲ Step 1: Train sequence model 4: Update parameters of 𝑝𝜙𝑘 using D 𝑘 -1 to minimize loss function 𝐿𝑡𝑟𝑎𝑖𝑛 in Eq. 2 5: end for 6: Initialize empty dataset R 𝑘 . 7: for 𝑟 = 1 to 𝑁 samples do ⊲ Step 2: Collect game trajectories 8: Reset environment E . 9: Generate a sequence of actions/observations using 𝑝𝜙𝑘 within E . 10: Collect trajectory 𝜏𝑟 = ( 𝑜 0 , 𝑟 0 , 𝑎 0 , 𝑜 1 , 𝑟 1 , 𝑎 1 , . . . ) from E . 11: Add 𝜏𝑟 to R 𝑘 . 12: end for 13: Set D 𝑘 ←D 𝑘 -1 ∪ R 𝑘 for the next iteration's training. 14: end for
```

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

D comprises of the interaction histories from all previous and current phases. This is a common strategy in performative prediction (Perdomo et al., 2020) to ensure more stable training of the prediction model.

We model 𝑝𝜙 ( 𝑎𝑡 | 𝑥 ≤ 𝑡 ) and 𝑝𝜙 ( 𝑜𝑡 | 𝑥 &lt;𝑡 , 𝑎 𝑡 -1 ) using a categorical distribution, yielding a standard categorical cross-entropy loss and we model 𝑝𝜙 ( 𝑟 𝑡 | 𝑥 &lt;𝑡 , 𝑎 𝑡 -1 , 𝑜 𝑡 ) with a normal distribution with fixed variance, yielding the mean-square error loss ( 𝑟 -ˆ 𝑟 ) 2 . In each phase, we sample 20 000 trajectories, which are concatenated with samples from previous phases for joint training of the sequence model. Optimization is performed using AdamW (Loshchilov &amp; Hutter, 2017) (learning rate 10 -4 , weight decay 10 -2 , 𝛽 1 = 0 . 9, 𝛽 2 = 0 . 98) for 10 epochs with a batch size of 256. Gradients are clipped at a norm of 1.0.

Pre-training The sequence model is pretrained on an initial dataset D 0 of 200 000 sample trajectories of two random tabular agents playing IPD against each other for 100 rounds using the same training hyperparameters as outlined above.

Inference During deployment, the agent estimates Q values by performing Monte Carlo roll-outs for 15 rounds into the future using the learned sequence model as a simulator. The final action selection

follows a policy 𝜋 ( 𝑎 | 𝑥 ≤ 𝑡 ) that re-weights the model's prior probability 𝑝 ( 𝑎 | 𝑥 ≤ 𝑡 ; 𝜙 ) by the estimated value ˆ 𝑄 𝑝 ( 𝑥 ≤ 𝑡 , 𝑎 ) derived from the roll-outs:

<!-- formula-not-decoded -->

We use 𝛽 = 0 . 01 for all experiments.

## A.3.2. Model-free agent

Architecture We implement an Advantage Actor-Critic (A2C) agent (Mnih et al., 2016) using a GRU-based sequence model with the same configuration as for the PPI agents. The GRU takes as input the history of observations of previous rounds and outputs the next action. The GRU is further augmented with a linear output head to estimate the value function 𝑉 ( 𝑥 ) . During training, we estimate the advantage 𝐴 ( 𝑥 ≤ 𝑡 , 𝑎 𝑡 ) using bootstrapped temporal-difference errors:

<!-- formula-not-decoded -->

The model parameters are updated to minimize the combined policy gradient and value estimation loss:

<!-- formula-not-decoded -->

where 𝑐 𝑣 , 𝑐 𝑒 are hyperparameters representing, correspondingly, the value function and entropy training coefficients.

Training To get comparable results, we follow the A2C training protocol from Meulemans et al. (2025a) including the value function estimation, Generalized Advantage Estimation (Schulman et al., 2015), advantage normalization and reward scaling. See Appendix A of Meulemans et al. (2025a) for details.

For each experiment, we perform a hyperparameter search over the learning rate, GAE lambda, advantage normalization, reward scaling and entropy regularization. We report the hyperparameters corresponding to the best-performing setting in Table 2.

## A.3.3. Tabular agents

Tabular agents employ a memory-1 policy defined by five parameters: the cooperation probabilities conditional on the previous outcome ( 𝑐𝑐, 𝑐𝑑, 𝑑𝑐, 𝑑𝑑 ) and the initial state ( 𝑠 0). Each parameter is initialized from a uniform distribution U( 0 , 1 ) .

## A.4. Ablations

## A.4.1. Policy conditioning

For the 'Opponent ID' ablation (Fig. 1), we prepend the observation sequence x ≤ 𝑡 with a conditioning vector z representing the opponent's identity. For tabular agents, z is defined as the flattened vector

Table 2 | A2C hyperparameters

| RL Hyperparameter        | Step 1    | Step 2    | Step 3    | Step 4    |
|--------------------------|-----------|-----------|-----------|-----------|
| advantages_normalization | True      | False     | True      | True      |
| batch size               | 2048      | 2048      | 4096      | 4096      |
| reward_rescaling         | 0 . 2     | 0 . 05    | 0 . 02    | 0 . 02    |
| value_discount ( 𝛾 )     | 0 . 99    | 0 . 99    | 0 . 99    | 0 . 99    |
| td_lambda ( 𝜆 td )       | 0 . 99    | 1 . 0     | 0 . 95    | 1 . 0     |
| gae_lambda ( 𝜆 gae )     | 0 . 99    | 1 . 0     | 0 . 95    | 1 . 0     |
| value_coefficient        | 0 . 5     | 0 . 5     | 0 . 5     | 0 . 5     |
| entropy_reg              | 0 . 001   | 0 . 001   | 0 . 001   | 0 . 01    |
| optimizer                | Adam      | Adam      | Adam      | Adam      |
| adam_epsilon             | 0 . 00001 | 0 . 00001 | 0 . 00001 | 0 . 00001 |
| learning_rate            | 0 . 005   | 0 . 005   | 0 . 0005  | 0 . 001   |
| max_grad_norm            | 1 . 0     | 1 . 0     | 1 . 0     | 1 . 0     |

of log-probabilities across all possible observations 𝑜 ∈ O :

<!-- formula-not-decoded -->

where O = {( 𝐶, 𝐶 ) , ( 𝐶, 𝐷 ) , ( 𝐷, 𝐶 ) , ( 𝐷, 𝐷 ) , Start } . For A2C and PPI agents, z = 0 .

## A.4.2. No mixed pool training

For the 'No Tabular Opponents' ablation (Fig. 1), we remove the tabular opponents from the mixed agent pool for both PPI and A2C experiments. For PPI, we additionally change the pretraining data distribution 𝐷 0 to not include tabular agents but instead consist of purely random action sequences with the corresponding rewards.

## B. Additional results

## B.1. In-episode trajectories for mixed pool training

Figure 3 shows the performance of PPI and A2C within a single episode during early training in the mixed pool setting (c.f. Sec. 3.1), i.e., for phase = 8 for PPI and training iteration = 70 𝑘 for A2C, showing the emergence of in-context opponent inference and an initial gradient towards cooperation against other learning agents.

## B.2. Additional results on A2C

Figure 4 shows A2C-based results, corresponding to the PPI results presented in Figure 2 in the main text. In Step 1, we observe that an A2C agent learns to implement best response against a variety of tabular agents, same as for PPI. In Step 2, however, we observe that the newly trained A2C agent manages to get a higher reward playing against the Fixed-ICL baseline than the PPI agent (correspondingly, ∼ 1 . 25 vs. ∼ 0 . 9). This can either be caused by (i) the PPI Fixed-ICL policy being harder to exploit or (ii) A2C finding a better exploiter policy. The irregular shape of the exploitation dynamics in Figure 4D suggests that the A2C exploiter agent learned a complex adversarial strategy against the A2C Fixed-ICL policy. In contrast, the PPI extortion policy of Figure 2D seems to be a more regular extortion policy. Finally, in Step 3, the A2C agents initially move towards cooperation but due to training instability they might still turn back to defection depending on the seed.

Figure 3 | Emergence of best-response in mixed training. We plot within-episode performance of models trained in Figure 1 before convergence. We observe that both A2C and PPI try to extort their counterpart at the beginning of the episode which subsequently leads to increased levels of cooperation. At the same time, identifying the opponent as a non-tit-for-tat-like tabular policy leads to high defection ratio. Error bars indicate standard deviation across 10 random seeds.

![Image](paper_artifacts/image_000004_875f83c347f39ce048f118a40e58f6b17a23e48a92073c861d2e92dcc9508849.png)

Step 1) A.Training Progress

![Image](paper_artifacts/image_000005_7422058008f3fce00afe151e1c1a8893dbe5e31abd23f3923d604c4ffe002c80.png)

Figure 4 | A-B: Emergence of in-context best response Performance of A2C trained against random tabular opponents and evaluated after convergence on a set of specific static policies. We denote the final agent as 'Fixed In-Context Learner'. C-D: Learning to extort in-context learners. Performance of a randomly initialized A2C agent against the Fixed In-Context Learner. E-F: From mutual extortion to cooperation. Two A2C extortion agents initially converge to cooperation when playing against each other, but with time they might collapse to mutual defection depending on the random seed. Error bars correspond to standard deviation over 5 random initializations.

## C. Derivation of Predictive Policy Improvement (PPI)

In this section, we provide a formal derivation of the Predictive Policy Improvement (PPI) algorithm. PPI is inspired by the theoretically grounded MUPI framework (Meulemans et al., 2025b), and is closely related to Maximum a Posteriori Policy Optimization (MPO; Abdolmaleki et al., 2018). PPI departs from standard MPO by replacing the separate value function and self-model of MPO with a single sequence model trained in a self-supervised fashion to predict actions, observations and rewards. This model serves simultaneously as a world model and a policy prior, leveraging the generative capabilities of sequence models for value estimation and policy representation.

## C.1. Objective: The Variational Lower Bound

We consider an agent optimizing its policy 𝜋 to maximize the expected return 𝑉 ( 𝜋 ) = 𝔼 𝜏 ∼ ℙ 𝜋 GLYPH&lt;2&gt;˝ 𝑇 𝑡 = 0 𝛾 𝑡 𝑟 𝑡 GLYPH&lt;3&gt; . To avoid notational clutter, we omit the agent-specific superscripts, as this derivation applies equally to the single-agent setting. We introduce a parameterized sequence model 𝑝𝜙 ( 𝑎 | 𝑥 ≤ 𝑡 ) which acts as a behavioral prior or self-model over the interaction history 𝑥 ≤ 𝑡 . We define a surrogate objective 𝐽 by penalizing the KL-divergence between the behavioral policy 𝜋 and the prior 𝑝𝜙 :

<!-- formula-not-decoded -->

Since KL (·||·) ≥ 0, 𝐽 ( 𝜋, 𝜙 ) is a strict lower bound on 𝑉 ( 𝜋 ) , with equality at 𝜋 = 𝑝𝜙 . We optimize this bound via coordinate ascent on 𝜋 (the non-parametric policy) and 𝜙 (the parametric sequence model).

## C.2. Step 1: Non-parametric Policy Improvement w.r.t. 𝜋

Optimizing 𝐽 ( 𝜋, 𝜙 ) w.r.t. 𝜋 for a fixed 𝜙 is a full-fledged optimal control problem, which generally lacks an analytical solution and is therefore ill-suited for direct non-parametric policy improvement. Instead, we use a first-order approximation of 𝐽 ( 𝜋, 𝜙 𝑘 ) around 𝜋 = 𝑝𝜙𝑘 , where 𝑝𝜙𝑘 is the self-model trained on the dataset gathered by deploying the previous policy 𝜋𝑘 -1:

<!-- formula-not-decoded -->

Note that here, the Q-value is equal to the unregularized value 𝑄 𝑝𝜙 𝑘 ( 𝑥 ≤ 𝑡 , 𝑎 ) = 𝔼 𝜏&gt;𝑡 ∼ ℙ 𝑝 𝜙 𝑘 (·| 𝑥 ≤ 𝑡 ,𝑎 ) GLYPH&lt;2&gt;˝ 𝑇 𝑡 ′ = 𝑡 𝛾 𝑡 ′ -𝑡 𝑟 𝑡 ′ GLYPH&lt;3&gt; , as all KL terms evaluate to zero under the prior. The crucial difference between 𝐽 and ¯ 𝐽 is that the expectation over histories in ¯ 𝐽 does not depend on the policy 𝜋 being optimized, which permits a closed-form solution for arg max 𝜋 ¯ 𝐽 .

We proceed to show that ¯ 𝐽 is indeed a first-order approximation to 𝐽 around 𝑝𝜙𝑘 via the following two lemmas.

<!-- formula-not-decoded -->

Proof. It is easy to see that the terms of equation 8 inside the expectation cancel out when 𝜋 = 𝑝𝜙𝑘 , leaving only 𝐽 ( 𝑝𝜙𝑘 , 𝜙 𝑘 ) . □

<!-- formula-not-decoded -->

Proof. We analyze the functional derivatives of both objectives with respect to the policy distribution 𝜋 ( 𝑎 | 𝑥 ≤ 𝑡 ) evaluated at a specific history 𝑥 ≤ 𝑡 and action 𝑎 .

First, consider the surrogate objective ¯ 𝐽 ( 𝜋, 𝜙 𝑘 ) . Because the expectation over histories is fixed to the prior distribution ℙ 𝑝 𝜙 𝑘 and thus does not depend on the optimization variable 𝜋 , the functional derivative is straightforward. Applying the product rule to the logarithmic term, the functional derivative with respect to the local action probability 𝜋 ( 𝑎 | 𝑥 ≤ 𝑡 ) is:

<!-- formula-not-decoded -->

Evaluating this derivative at the prior 𝜋 = 𝑝𝜙𝑘 , the logarithmic term vanishes (since log 1 = 0), yielding:

<!-- formula-not-decoded -->

Next, differentiating the true objective 𝐽 ( 𝜋, 𝜙 𝑘 ) is more involved because 𝜋 dictates the history visitation distribution ℙ 𝜋 ( 𝑥 ≤ 𝑡 ) . We define the regularized Q-function, 𝑄 𝜋 reg ( 𝑥 ≤ 𝑡 , 𝑎 ) , which captures the expected return including all future KL penalties, but excluding the immediate penalty at time 𝑡 :

<!-- formula-not-decoded -->

Using this, the value of a specific history is:

<!-- formula-not-decoded -->

To find the functional derivative of the global objective 𝐽 with respect to the local policy 𝜋 ( 𝑎 | 𝑥 ≤ 𝑡 ) , we apply the continuous extension of the Performance Difference Lemma (Kakade &amp; Langford, 2002). This theorem establishes that the indirect effect of the policy on the visitation distribution ℙ 𝜋 ( 𝑥 ≤ 𝑡 ) yields a net zero contribution to the gradient. Consequently, the derivative isolates the state visitation probability multiplied by the local derivative of the value function:

<!-- formula-not-decoded -->

Taking the partial derivative of 𝑉 𝜋 ( 𝑥 ≤ 𝑡 ) yields:

<!-- formula-not-decoded -->

Finally, we evaluate this true derivative at the prior policy 𝜋 = 𝑝𝜙𝑘 . Three simplifications occur:

- The history visitation distribution matches the prior: ℙ 𝜋 ( 𝑥 ≤ 𝑡 ) = ℙ 𝑝 𝜙 𝑘 ( 𝑥 ≤ 𝑡 ) .
- The immediate KL penalty evaluates to zero: log 1 = 0.
- Because the policy perfectly matches the prior at all future timesteps, all future KL penalties evaluate to zero. Consequently, the regularized Q-function smoothly collapses to the unregularized Q-function of the prior: 𝑄 𝜋 reg ( 𝑥 ≤ 𝑡 , 𝑎 ) = 𝑄 𝑝𝜙 𝑘 ( 𝑥 ≤ 𝑡 , 𝑎 ) .

Applying these simplifications yields:

<!-- formula-not-decoded -->

Since the functional derivatives of both 𝐽 and ¯ 𝐽 evaluated at 𝜋 = 𝑝𝜙𝑘 perfectly coincide, it follows that ∇ 𝜋 ¯ 𝐽 ( 𝜋, 𝜙 𝑘 )| 𝜋 = 𝑝 𝜙 𝑘 = ∇ 𝜋 𝐽 ( 𝜋, 𝜙 𝑘 )| 𝜋 = 𝑝 𝜙 𝑘 , concluding the proof. □

Optimizing ¯ 𝐽 . Optimizing ¯ 𝐽 ( 𝜋, 𝜙 𝑘 ) w.r.t. 𝜋 for fixed 𝜙𝑘 has the well-known Boltzmann policy as solution:

<!-- formula-not-decoded -->

with the inverse temperature 𝛽 = 1 𝛼 . We treat 𝛽 as a fixed hyperparameter defining a trust region around 𝑝𝜙𝑘 where ¯ 𝐽 is a sufficiently accurate approximation of 𝐽 .

## C.3. Comparison with MPO and Sequence-Model Value Estimation

While PPI shares the coordinate-ascent structure of MPO, it differs in how Q-values are obtained and whether 𝜋 or 𝑝𝜙𝑘 is deployed as behavioral policy to gather trajectories. In standard MPO, 𝑄 ( 𝑠, 𝑎 ) is typically represented by a separate neural network (a critic) trained via temporal difference (TD) learning on the agent's own experience, relying on the Markov property to condition on a single state 𝑠 instead of the full history.

In contrast, PPI leverages the sequence model as a world model. The value ˆ 𝑄𝑝 ( 𝑥 ≤ 𝑡 , 𝑎 ) is estimated via Monte Carlo rollouts performed within the sequence model itself. By sampling future trajectories 𝜏&gt;𝑡 from 𝑝𝜙 (· | 𝑥 ≤ 𝑡 , 𝑎 ) , the agent evaluates the expected return of an action based on its internal representation of both the environment dynamics and the co-player's predicted responses. This allows PPI to benefit from the high-capacity temporal dependencies captured by the sequence model. Note that PPI is easily extendable toward learning an explicit Q-value function conditioned on full histories to amortize the cost of the MC rollouts and reduce variance.

## D. Theoretical Analysis of the Equilibrium Behavior of PPI Agents

In this section, we analyze the theoretical properties of the Predictive Policy Improvement (PPI) algorithm. Unlike standard reinforcement learning, where agents optimize a policy against a fixed (or stationarily adapting) environment, PPI agents operate in a performative loop: the agent's predictive model determines its policy, which determines the data distribution, which in turn is used to update the predictive model. This is closely related to the concept of 'performative prediction' (Perdomo et al., 2020), where the predictions of a model can affect the distribution of the very data it is trying to predict (with traffic prediction models being a prominent example).

We formalize this interaction and define the concept of a Predictive Equilibrium (PE). We show that while a global pure-strategy equilibrium is not guaranteed to exist due to the non-convex nature of deep neural networks, a local predictive equilibrium (consistent with gradient-based optimization) and a mixed predictive equilibrium (randomized strategies) are guaranteed to exist under standard assumptions. Finally, we show that in the limit of a perfect world model, a predictive equilibrium corresponds to a subjective embedded equilibrium (Meulemans et al., 2025b).

## D.1. Formal Setup

Consider a game with 𝑛 agents. Each agent 𝑖 maintains a predictive sequence model 𝑝𝜃𝑖 ( ℎ 𝑖 ) parameterized by 𝜃𝑖 ∈ Θ 𝑖 , where ℎ 𝑖 is a history 𝑥 𝑖 ≤ 𝑡 of arbitrary length 𝑡 , and Θ 𝑖 is a compact metric space (e.g., a bounded subset of ℝ 𝑑 ).

The Performative Loop. The PPI algorithm (Algorithm 1) induces a closed-loop dependency between parameters and data:

1. Model induces Policy: The agent derives a policy 𝜋𝜃𝑖 from its model 𝑝𝜃𝑖 via the policy improvement operator, defined in Eq. 6 (the Boltzmann policy over Q-values estimated via rollout).
2. Policy induces Data: When all agents interact using policies 𝝅𝜽 = { 𝜋𝜃 1 , . . . , 𝜋 𝜃𝑁 } , they induce a joint distribution over interaction histories ℎ . We denote the true probability distribution of histories generated by the current joint configuration 𝜽 as ℙ (· ; 𝜽 ) .
3. Data induces Model: The agent updates 𝜃𝑖 to minimize the Kullback-Leibler (KL) divergence between the observed distribution ℙ (· ; 𝜽 ) and its model 𝑝𝜃𝑖 .

## D.2. Predictive Equilibria

A stable point of this training loop is a configuration where the model optimally predicts the data generated by the policy derived from that very model.

Definition D.1 (Global Predictive Equilibrium) . A joint configuration 𝜽 ∗ = ( 𝜃 ∗ 1 , . . . , 𝜃 ∗ 𝑛 ) is a Global Predictive Equilibrium if, for all agents 𝑖 :

<!-- formula-not-decoded -->

Intuitively , at equilibrium, no agent can improve their world model given the behavior induced by the current joint models.

Challenges. Proving the existence of a global PE is difficult because the map 𝜃 ↦→ 𝜋𝜃 is complex and the resulting objective is generally non-convex. The 'argmin' set may change discontinuously (mode hopping), preventing the application of standard fixed-point theorems. To address this, we define two relaxed solution concepts: Local PE (relevant to gradient descent) and Mixed PE.

## D.2.1. Local Predictive Equilibrium

In practice, PPI agents update parameters via gradient descent. They do not find global minima but rather stationary points. Crucially, the update assumes that the data distribution is fixed (which can be interpreted as a 'stop-gradient' on the environment dynamics).

Definition D.2 (Local Predictive Equilibrium) . Let Θ 𝑖 ⊂ ℝ 𝑑𝑖 be a compact, convex parameter space for each agent 𝑖 ∈ I . A joint configuration 𝜽 ∗ = ( 𝜃 ∗ 1 , . . . , 𝜃 ∗ 𝑛 ) ∈ ˛ 𝑖 ∈I Θ 𝑖 is a Local Predictive Equilibrium if, for all agents 𝑖 ∈ I , the configuration satisfies the first-order stationarity condition with respect to their local loss, assuming the data generating process is fixed. Formally:

<!-- formula-not-decoded -->

where ⟨· , ·⟩ denotes the standard inner product.

This variational inequality definition corresponds precisely to the convergence criteria of projected gradient descent in the PPI algorithm. If 𝜃 ∗ 𝑖 lies in the interior of Θ 𝑖 , Eq. 18 implies the standard condition

<!-- formula-not-decoded -->

Theorem D.3 (Existence of Local Predictive Equilibrium) . Assume Θ 𝑖 is a compact, convex subset of ℝ 𝑑𝑖 . Assume the mapping from parameters 𝜽 to the local gradient of the loss 𝐺𝑖 ( 𝜽 ) = ∇ 𝜗 KL ( ℙ (· ; 𝜽 ) | | 𝑝𝜗 ) GLYPH&lt;12&gt; GLYPH&lt;12&gt; 𝜗 = 𝜃𝑖 is continuous. Then, there exists at least one Local Predictive Equilibrium.

Proof. Weanalyze the existence of a Local Predictive Equilibrium by framing it as a fixed-point problem. Let L 𝑖 ( 𝜽 , 𝜓 ) = KL GLYPH&lt;0&gt; ℙ ( ℎ𝑖 ; 𝜽 ) | | 𝑝𝜓 ( ℎ𝑖 ) GLYPH&lt;1&gt; denote the loss function for agent 𝑖 , where the first argument 𝜽 determines the data distribution (fixed locally) and the second argument 𝜓 is the parameter being optimized. Define the local gradient field 𝐺 : Θ → ℝ 𝐷 (where 𝐷 = ˝ 𝑖 ∈I 𝑑𝑖 ) as the concatenation of the individual gradients:

<!-- formula-not-decoded -->

A Local Predictive Equilibrium is characterized by the variational inequality ⟨ 𝐺 ( 𝜽 ∗ ) , 𝜙 -𝜽 ∗ ⟩ ≥ 0 for all 𝜙 ∈ Θ , where Θ = ˛ 𝑖 ∈I Θ 𝑖 .

Weassume the parameter space Θ is a compact, convex subset of Euclidean space, and that the gradient field 𝐺 ( 𝜽 ) is continuous. The continuity of 𝐺 follows naturally from the smoothness assumptions on the predictive models 𝑝𝜃 and the induced policy distributions.

Consider the map 𝑇 : Θ → Θ defined by a projected gradient step:

<!-- formula-not-decoded -->

where 𝜂 &gt; 0 is a scalar step size and Proj Θ is the Euclidean projection onto the set Θ .

1. Compactness and Convexity: By assumption, Θ is a compact and convex set.
2. Continuity: The map 𝐺 is continuous by assumption. The projection operator Proj Θ is nonexpansive and thus continuous. Therefore, the composition 𝑇 is a continuous map from Θ to itself.

By Brouwer's Fixed Point Theorem, there exists a point 𝜽 ∗ ∈ Θ such that 𝑇 ( 𝜽 ∗ ) = 𝜽 ∗ . This fixed point condition implies:

<!-- formula-not-decoded -->

By the standard property of the Euclidean projection onto a closed convex set, this equation holds if and only if:

<!-- formula-not-decoded -->

Simplifying the terms inside the inner product, we obtain:

<!-- formula-not-decoded -->

This inequality is precisely the first-order stationarity condition defined in Eq. 18, generalized to the joint parameter space Θ . Therefore, the fixed point 𝜽 ∗ constitutes a Local Predictive Equilibrium, rigorously accommodating both interior stationary points and boundary solutions. □

## D.2.2. Mixed Predictive Equilibrium

To guarantee the existence of an equilibrium without relying on local approximations, we can allow agents to randomize over model parameters. This is analogous to mixed strategies in game theory.

Definition D.4 (Mixed Predictive Equilibrium) . Let ΔΘ 𝑖 be the set of probability distributions over parameters Θ 𝑖 . A Mixed Predictive Equilibrium is a tuple of distributions 𝝁 ∗ = ( 𝜇 ∗ 1 , . . . , 𝜇 ∗ 𝑛 ) such that for all 𝑖 ∈ I :

<!-- formula-not-decoded -->

where 𝑝𝜇𝑖 ( ℎ𝑖 ) = 𝔼 𝜃𝑖 ∼ 𝜇𝑖 GLYPH&lt;2&gt; 𝑝𝜃𝑖 ( ℎ𝑖 ) GLYPH&lt;3&gt; , and ℙ ( ℎ𝑖 ; 𝝁 ∗ ) is the distribution of histories generated when each agent 𝑖 follows the policy 𝜋𝜇𝑖 obtained by applying the policy improvement operator equation 6 on 𝑝𝜇𝑖 .

Theorem D.5 (Existence of Mixed Predictive Equilibrium) . Assume Θ 𝑖 is a compact metric space 1 and the map ( 𝜽 , 𝜃 ′ 𝑖 ) ↦→ KL GLYPH&lt;16&gt; ℙ (· ; 𝜽 ) | | 𝑝 𝜃 ′ 𝑖 GLYPH&lt;17&gt; is continuous for every 𝑖 ∈ I . Furthermore, assume that KL GLYPH&lt;0&gt; ℙ ( ℎ𝑖 ; 𝝁 ) | | 𝑝𝜇𝑖 ( ℎ𝑖 ) GLYPH&lt;1&gt; &lt; ∞ for all 𝝁 ∈ Δ = ˛ 𝑖 ∈I ΔΘ 𝑖 . Then a Mixed Predictive Equilibrium exists.

Proof. We prove existence by constructing a continuous map on the space of mixed strategies and applying a fixed-point theorem. Let ΔΘ 𝑖 be the space of Borel probability measures on the compact metric space Θ 𝑖 . Endowed with the Wasserstein metric, ΔΘ 𝑖 is a compact, convex metric space. Let Δ = ˛ 𝑖 ∈I ΔΘ 𝑖 be the joint strategy space.

Since ΔΘ 𝑖 is a compact metric space, it is separable. We can fix a countable dense subset 𝐷𝑖 = { ˜ 𝜇𝑖,𝑘 } ∞ 𝑘 = 1 ⊂ ΔΘ 𝑖 .

We define the continuous advantage function 𝑎𝑖 : Δ × ΔΘ 𝑖 → ℝ ≥ 0 as:

<!-- formula-not-decoded -->

Since KL GLYPH&lt;0&gt; ℙ ( ℎ𝑖 ; 𝝁 ) | | 𝑝𝜇𝑖 ( ℎ𝑖 ) GLYPH&lt;1&gt; &lt; ∞ , the advantage function is well-defined and evaluates to a finite real number.

We now construct a transition map 𝑇𝑖 : Δ → ΔΘ 𝑖 . Define a finite measure 𝐴𝑖 ( 𝝁 ) on Θ 𝑖 that places weights on the dense subset 𝐷𝑖 proportional to the advantage:

<!-- formula-not-decoded -->

Let 𝐴𝑖 ( 𝝁 )( Θ 𝑖 ) = ˝ ∞ 𝑘 = 1 2 -𝑘 𝑎𝑖 ( 𝝁 , ˜ 𝜇𝑖,𝑘 ) denote its total mass. We define 𝑇𝑖 ( 𝝁 ) by mixing the current strategy 𝜇𝑖 with the improvement measure 𝐴𝑖 ( 𝝁 ) :

<!-- formula-not-decoded -->

Since the mappings 𝜽 ↦→ KL GLYPH&lt;16&gt; ℙ (· ; 𝜽 ) | | 𝑝 𝜇 ′ 𝑖 GLYPH&lt;17&gt; are continuous and the spaces are compact, 𝑎𝑖 is uniformly bounded and continuous in 𝝁 with respect to the weak-* topology. Consequently, the joint map 𝑇 ( 𝝁 ) = ( 𝑇 1 ( 𝝁 ) , . . . , 𝑇 𝑛 ( 𝝁 )) is a continuous function from the compact convex set Δ to itself. By Schauder's fixed-point theorem, there exists a fixed point 𝝁 ∗ ∈ Δ such that 𝑇 ( 𝝁 ∗ ) = 𝝁 ∗ .

1 It is worth noting that we do not require the convexity of Θ 𝑖 in Theorem D.5, we only need compactness.

We now prove by contradiction that 𝝁 ∗ is a Mixed Predictive Equilibrium. Let

<!-- formula-not-decoded -->

From the fixed point condition 𝜇 ∗ 𝑖 = 𝑇𝑖 ( 𝝁 ∗ ) , we obtain:

<!-- formula-not-decoded -->

Assume 𝝁 ∗ is not a Mixed Predictive Equilibrium. Then, for some agent 𝑖 ∈ I , there exists a distribution ˆ 𝜇𝑖 ∈ ΔΘ 𝑖 such that

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Let

By definition, the advantage of ˆ 𝜇𝑖 is strictly positive: 𝑎𝑖 ( 𝝁 ∗ , ˆ 𝜇𝑖 ) = 𝜖 &gt; 0.

Now since the mapping ( 𝜽 , 𝜃 ′ 𝑖 ) ↦→ KL GLYPH&lt;16&gt; ℙ (· ; 𝜽 ) | | 𝑝 𝜃 ′ 𝑖 GLYPH&lt;17&gt; is continuous, it follows that the functional 𝜇 ′ 𝑖 ↦→ KL GLYPH&lt;16&gt; ℙ ( ℎ𝑖 ; 𝝁 ∗ ) | | 𝑝 𝜇 ′ 𝑖 ( ℎ𝑖 ) GLYPH&lt;17&gt; is continuous on the compact metric space ΔΘ 𝑖 , and hence the advantage function 𝑎𝑖 ( 𝝁 ∗ , ·) is uniformly continuous. Therefore, there exists an open neighborhood 𝑈 ⊂ ΔΘ 𝑖 containing ˆ 𝜇𝑖 such that 𝑎𝑖 ( 𝝁 ∗ , 𝜇 ′ 𝑖 ) &gt; 𝜖 / 2 for all 𝜇 ′ 𝑖 ∈ 𝑈 .

Since the set 𝐷𝑖 = { ˜ 𝜇𝑖,𝑘 } ∞ 𝑘 = 1 is dense in ΔΘ 𝑖 , there exists an integer 𝐾 such that ˜ 𝜇𝑖,𝐾 ∈ 𝑈 . Consequently, 𝑎𝑖 ( 𝝁 ∗ , ˜ 𝜇𝑖,𝐾 ) &gt; 𝜖 / 2 &gt; 0. This strictly positive advantage guarantees that the total mass of the improvement measure is strictly positive:

<!-- formula-not-decoded -->

From the fixed-point condition 𝐶𝑖 𝜇 ∗ 𝑖 = 𝐴𝑖 ( 𝝁 ∗ ) , and knowing 𝐶𝑖 &gt; 0, we can express 𝜇 ∗ 𝑖 as an infinite convex combination of the basis measures in 𝐷𝑖 :

<!-- formula-not-decoded -->

where the weights 𝑤𝑘 = 2 -𝑘 𝑎𝑖 ( 𝝁 ∗ , ˜ 𝜇𝑖,𝑘 ) 𝐶𝑖 ≥ 0 sum to exactly 1.

Now, consider the expected predictive model under the mixed strategy 𝜇 ∗ 𝑖 . By linearity of the expectation, we have:

<!-- formula-not-decoded -->

Because the Kullback-Leibler divergence is strictly convex with respect to its second argument, we can apply Jensen's inequality to the infinite convex combination:

<!-- formula-not-decoded -->

Crucially, by the definition of the advantage function and the construction of the weights 𝑤𝑘 , any weight 𝑤𝑘 is strictly positive if and only if the corresponding advantage 𝑎𝑖 ( 𝝁 ∗ , ˜ 𝜇𝑖,𝑘 ) &gt; 0. A strictly positive advantage exactly means that the evaluated measure achieves a strictly lower loss than the current state 𝜇 ∗ 𝑖 :

<!-- formula-not-decoded -->

Since there is at least one weight 𝑤𝐾 &gt; 0 with an advantage bounded away from zero by 𝜖 / 2, substituting this strict upper bound into the sum over 𝑘 yields:

<!-- formula-not-decoded -->

Combining the inequalities together, we arrive at the following absolute contradiction:

<!-- formula-not-decoded -->

Therefore, our initial assumption must be false. No such superior distribution ˆ 𝜇𝑖 can exist, and the fixed point 𝝁 ∗ is indeed a Mixed Predictive Equilibrium. □

An interesting corollary of the above theorem, is that if our model is convex in functional space, then there exists a pure global predictive equilibrium.

Corollary D.6 (Existence of Pure Predictive Equilibrium under Model Functional Convexity) . Consider the same assumptions as in Theorem D.5. Assume furthermore that for every agent 𝑖 ∈ I , the space of representable predictive models { 𝑝𝜃𝑖 | 𝜃𝑖 ∈ Θ 𝑖 } is convex. That is, for every 𝜃 ′ 𝑖 , 𝜃 ′′ 𝑖 ∈ Θ 𝑖 and every 𝛼𝑖 ∈ [ 0 , 1 ] , there exists a pure parameter 𝜃𝑖 ∈ Θ 𝑖 satisfying 𝑝𝜃𝑖 = 𝛼𝑖 𝑝 𝜃 ′ 𝑖 + ( 1 -𝛼𝑖 ) 𝑝 𝜃 ′′ 𝑖 . 2 Under these conditions, a Global Predictive Equilibrium (in pure strategies) always exists.

Proof. From Theorem D.5, there exists a Mixed Predictive Equilibrium 𝝁 ∗ = ( 𝜇 ∗ 1 , . . . , 𝜇 ∗ 𝑛 ) ∈ ˛ 𝑖 ∈I ΔΘ 𝑖 . To establish the existence of a pure Global Predictive Equilibrium, we will demonstrate that for any probability distribution 𝜇𝑖 ∈ ΔΘ 𝑖 , the model functional convexity assumption guarantees the existence of a pure parameter 𝜃 ∗ 𝑖 ∈ Θ 𝑖 such that 𝑝 𝜃 ∗ 𝑖 = 𝑝𝜇𝑖 = 𝔼 𝜃𝑖 ∼ 𝜇𝑖 GLYPH&lt;2&gt; 𝑝𝜃𝑖 GLYPH&lt;3&gt; .

We first prove this claim for finitely supported measures. Let 𝜇𝑖 = ˝ 𝑚 𝑘 = 1 𝑤𝑘𝛿𝜃𝑖,𝑘 be a finitely supported probability measure on Θ 𝑖 , where 𝑤𝑘 ≥ 0 and ˝ 𝑚 𝑘 = 1 𝑤𝑘 = 1. We proceed by induction on the support size 𝑚 . The base case 𝑚 = 1 is trivial, as 𝑝𝜇𝑖 = 𝑝𝜃𝑖, 1 . Assuming the claim holds for 𝑚 -1, we can express 𝜇𝑖 (provided 𝑤𝑚 &lt; 1) as:

<!-- formula-not-decoded -->

By the inductive hypothesis, there exists a pure parameter ˜ 𝜃𝑖 ∈ Θ 𝑖 such that 𝑝 ˜ 𝜃𝑖 = ˝ 𝑚 -1 𝑘 = 1 𝑤𝑘 1 -𝑤𝑚 𝑝𝜃𝑖,𝑘 . Applying the convexity assumption with 𝛼𝑖 = 𝑤𝑚 , 𝜃 ′ 𝑖 = 𝜃𝑖,𝑚 , and 𝜃 ′′ 𝑖 = ˜ 𝜃𝑖 , there exists 𝜃𝑖 ∈ Θ 𝑖 such that 𝑝𝜃𝑖 = 𝑤𝑚𝑝𝜃𝑖,𝑚 + ( 1 -𝑤𝑚 ) 𝑝 ˜ 𝜃𝑖 = 𝑝𝜇𝑖 . Thus, the claim holds for all finitely supported measures.

2 We emphasize that we do not require convexity in the parameters, i.e., we do not require that 𝑝 𝛼 𝑖 𝜃 ′ 𝑖 +( 1 -𝛼 𝑖 ) 𝜃 ′′ 𝑖 = 𝛼𝑖 𝑝 𝜃 ′ 𝑖 + ( 1 -𝛼𝑖 ) 𝑝 𝜃 ′′ 𝑖 .

Now, consider an arbitrary measure 𝜇𝑖 ∈ ΔΘ 𝑖 . Since the set of finitely supported measures is dense in ΔΘ 𝑖 under the weak-* topology, there exists a sequence of finitely supported measures ( 𝜇 ( 𝑚 ) 𝑖 ) ∞ 𝑚 = 1 converging weakly to 𝜇𝑖 .

Because the mapping 𝜃𝑖 ↦→ 𝑝𝜃𝑖 ( ℎ𝑖 ) is continuous and bounded for any given ℎ𝑖 , the functional 𝜈 ↦→ 𝑝𝜈 ( ℎ𝑖 ) = ∫ 𝑝𝜃𝑖 ( ℎ𝑖 ) 𝑑𝜈 ( 𝜃𝑖 ) is continuous with respect to the weak-* topology. Consequently, the sequence of expected models converges pointwise: 𝑝 𝜇 ( 𝑚 ) 𝑖 → 𝑝𝜇𝑖 as 𝑚 →∞ .

From the inductive step, for each finitely supported measure 𝜇 ( 𝑚 ) 𝑖 , there exists a corresponding pure parameter 𝜃 ( 𝑚 ) 𝑖 ∈ Θ 𝑖 such that 𝑝 𝜃 ( 𝑚 ) 𝑖 = 𝑝 𝜇 ( 𝑚 ) 𝑖 . This constructs a sequence of pure parameters ( 𝜃 ( 𝑚 ) 𝑖 ) ∞ 𝑚 = 1 in Θ 𝑖 . Since Θ 𝑖 is a compact metric space, this sequence admits a convergent subsequence ( 𝜃 ( 𝑚𝑘 ) 𝑖 ) ∞ 𝑘 = 1 that converges to some limit point 𝜃 ∗ 𝑖 ∈ Θ 𝑖 .

By the continuity of the map 𝜃𝑖 ↦→ 𝑝𝜃𝑖 , we find:

<!-- formula-not-decoded -->

Thus, for the Mixed Predictive Equilibrium 𝝁 ∗ , there exists a joint configuration of pure parameters 𝜽 ∗ = ( 𝜃 ∗ 1 , . . . , 𝜃 ∗ 𝑛 ) ∈ ˛ 𝑖 ∈I Θ 𝑖 such that 𝑝 𝜃 ∗ 𝑖 = 𝑝 𝜇 ∗ 𝑖 for all 𝑖 ∈ I .

It then follows that

<!-- formula-not-decoded -->

This precisely satisfies the definition of a Global Predictive Equilibrium, proving its existence in pure strategies under these conditions. □

We remark that while the assumption of functional convexity is an idealization for finite-capacity networks, deep neural networks are universal function approximators; consequently, as model capacity increases, the space of representable distributions approximates the full convex set of valid probability measures, rendering the existence of a pure equilibrium an increasingly accurate approximation.

## D.3. Relationship to Nash Equilibria and Subjective Embedded Equilibria

Finally, we connect the fixed points of the PPI algorithm to the standard solution concepts of game theory. In standard game theory, a Nash Equilibrium assumes that agents act optimally given a fixed environment, where the policies of co-players are independent of the focal agent's current action selection. In contrast, agents in the PPI framework act optimally with respect to an internal world model 𝑝𝜃𝑖 that estimates the joint distribution of future trajectories, thereby capturing potential reactive dependencies between the focal agent's actions and the co-players' responses.

This is closely related to the concept of 'Embedded Equilibria', which characterizes the equilibrium behavior that emerges from such self-predictive dynamics:

Definition D.7 (Subjective Embedded Equilibrium) . (Meulemans et al., 2025b) A joint policy profile 𝝅 ∗ and a set of internal sequence models { 𝑝 ∗ 1 , . . . , 𝑝 ∗ 𝑛 } constitute a Subjective Embedded Equilibrium if:

1. Subjective Optimality: Each agent's policy 𝜋 ∗ 𝑖 is a strict best-response to its internal world model 𝑝 ∗ 𝑖 .

2. On-Path Consistency: Each agent's world model perfectly matches the true environment dynamics exclusively on the equilibrium path (the distribution of histories ℙ ∗ genuinely generated by the joint policy 𝝅 ∗ ).

Crucially, a Subjective Embedded Equilibrium places no constraints on the accuracy of the agents' models regarding off-path counterfactuals (actions that are assigned zero probability under 𝝅 ∗ ). Nevertheless, 𝜋 ∗ 𝑖 must be a best response with respect to 𝑝 ∗ 𝑖 , and this takes into account counterfactual off-policy paths. In other words, according to the predictive model 𝑝 ∗ 𝑖 , the agent 𝑖 will not get higher expected returns by deviating from 𝜋 ∗ 𝑖 .

We refer the reader to Meulemans et al. (2025b) for further details about subjective embedded equilibria and their properties.

It turns out that if PPI agents converge to a fixed point for which their (predictive) world models are perfect, then the predictive equilibrium corresponds to a subjective embedded equilibrium. Let us first formalize the predictive equilibrium with perfect world models:

Definition D.8 (Perfect Predictive Equilibrium) . A Perfect Predictive Equilibrium is a configuration 𝜽 ∗ where the agents perfectly model the induced data distribution:

<!-- formula-not-decoded -->

Theorem D.9 (Perfect Predictive Equilibrium = ⇒ Subjective Embedded Equilibrium) . Consider predictive agents using the policy improvement operator defined in Eq. 6, where 𝜋𝜃𝑖 ( 𝑎𝑖 | ℎ𝑖 ) ∝ 𝑝𝜃𝑖 ( 𝑎𝑖 | ℎ𝑖 ) exp ( 𝛽𝑄 𝑝𝜃 𝑖 ( ℎ𝑖 , 𝑎 𝑖 )) . If 𝜽 ∗ is a Perfect Predictive Equilibrium, then the resulting configuration is consistent with a Subjective Embedded Equilibrium.

Proof. At a Perfect Predictive Equilibrium, the condition KL GLYPH&lt;16&gt; ℙ (· ; 𝜽 ∗ ) | | 𝑝 𝜃 ∗ 𝑖 (·) GLYPH&lt;17&gt; = 0 implies that the sequence model matches the true data distribution almost everywhere. Thus, on the equilibrium path, the prior action probability generated by the sequence model exactly matches the true behavioral policy: 𝑝 𝜃 ∗ 𝑖 ( 𝑎𝑖 | ℎ𝑖 ) = 𝜋𝜃 ∗ 𝑖 ( 𝑎𝑖 | ℎ𝑖 ) . This immediately satisfies the On-Path Consistency condition.

Substituting 𝑝 𝜃 ∗ 𝑖 = 𝜋𝜃 ∗ 𝑖 into the policy improvement operator yields:

<!-- formula-not-decoded -->

For any action 𝑎𝑖 in the support of the policy (where 𝜋𝜃 ∗ 𝑖 ( 𝑎𝑖 | ℎ𝑖 ) &gt; 0), we divide both sides by 𝜋𝜃 ∗ 𝑖 ( 𝑎𝑖 | ℎ𝑖 ) to obtain:

<!-- formula-not-decoded -->

Since 𝑍 ( ℎ𝑖 ) is a normalizing constant independent of 𝑎𝑖 , the expected return evaluated under the model must be identical for all actions played with positive probability.

Nowconsider any off-path action 𝑎 ′ 𝑖 not in the support of the policy (where 𝜋𝜃 ∗ 𝑖 ( 𝑎 ′ 𝑖 | ℎ𝑖 ) = 0). Because this action is never taken under the joint policy, the marginal probability ℙ ( ℎ𝑖 , 𝑎 ′ 𝑖 ; 𝜽 ∗ ) = 0. Consequently, the KL divergence places absolutely no constraints on the model's conditional predictions following 𝑎 ′ 𝑖 .

To formally verify Subjective Optimality, we demonstrate that there exists a valid completion of the sequence model's off-path conditional probabilities that justifies 𝜋𝜃 ∗ 𝑖 ( 𝑎 ′ 𝑖 | ℎ𝑖 ) = 0. Let 𝑒 𝑚𝑖𝑛 = ( 𝑜, 𝑟 𝑚𝑖𝑛 ) be

an environment percept containing the minimal possible reward 𝑟 𝑚𝑖𝑛 . We define the model's off-path counterfactual completion as 𝑝 𝜃 ∗ 𝑖 ( 𝑒 𝑚𝑖𝑛 | ℎ𝑖 , 𝑎 ′ 𝑖 ) = 1, assuming absorbing minimal rewards thereafter.

Evaluating the expected return under this completed subjective model yields 𝑄 𝑝 𝜃 ∗ 𝑖 ( ℎ𝑖 , 𝑎 ′ 𝑖 ) = 𝑉𝑚𝑖𝑛 , which is not larger than the on-path return ln 𝑍 ( ℎ𝑖 ) 𝛽 . Because the policy operator is restricted by the prior 𝑝 𝜃 ∗ 𝑖 ( 𝑎 ′ 𝑖 | ℎ𝑖 ) , which must evaluate to 0 to satisfy the fixed point, the agent assigns exactly 0 probability to the suboptimal deviation 𝑎 ′ 𝑖 . Therefore, the agent is playing an exact, best-response to its subjective world model, fully satisfying the definition of a Subjective Embedded Equilibrium. □

## E. Software

Experiments were implemented in Python together with the Google JAX (Bradbury et al., 2018) framework, and the NumPy (Harris et al., 2020), pandas (Wes McKinney, 2010), Matplotlib (Hunter, 2007), seaborn (Waskom, 2021), Flax (Heek et al., 2024) and Optax (DeepMind et al., 2020) packages.

## E.1. LLM usage

We used Gemini 3 Pro for language editing and readability improvements during the preparation of this manuscript. We also used Gemini 3 Pro for providing additional details in the proof of Lemma C.2, which were afterwards checked by the authors.