# Popular Papers on Foundational LLMs, RAG & AI Agents (Computer Science)

*Generated: 2026-10-27 01:23:11*
*Source: Semantic Scholar batch API refresh of existing paper IDs*
*Filtered for Computer Science papers only*
*Includes foundational LLM papers resolved by stable arXiv IDs.*

## Foundational LLMs & Transformers

*Retrieved: 2026-10-27 01:23:11*

### 1. Attention is All you Need

**Authors:** Ashish Vaswani, Noam Shazeer, N. Parmar, et al.  
**Year:** 2017 | **Citations:** 198,575 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Jun 2017]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776](https://www.semanticscholar.org/paper/204e3073870fae3d05bcbc2f6a8e263d9b72e776)  
**arXiv:** [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)  

**Abstract:** The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

---

### 2. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

**Authors:** J. Devlin, Ming-Wei Chang, Kenton Lee, et al.  
**Year:** 2019 | **Citations:** 123,375 | **Venue:** North American Chapter of the Association for Computational Linguistics  
**Year Month:** [Oct 2018]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/df2b0e26d0599ce3e70df8a9da02e51594e0e992](https://www.semanticscholar.org/paper/df2b0e26d0599ce3e70df8a9da02e51594e0e992)  
**arXiv:** [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)  

**Abstract:** We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models (Peters et al., 2018a; Radford et al., 2018), BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5 (7.7 point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

---

### 3. Language Models are Few-Shot Learners

**Authors:** Tom B. Brown, Benjamin Mann, Nick Ryder, et al.  
**Year:** 2020 | **Citations:** 65,197 | **Venue:** Neural Information Processing Systems  
**Year Month:** [May 2020]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/90abbc2cf38462b954ae1b772fac9532e2ccd8b0](https://www.semanticscholar.org/paper/90abbc2cf38462b954ae1b772fac9532e2ccd8b0)  
**arXiv:** [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)  

**Abstract:** Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something which current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art fine-tuning approaches. Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or fine-tuning, with tasks and few-shot demonstrations specified purely via text interaction with the model. GPT-3 achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly reasoning or domain adaptation, such as unscrambling words, using a novel word in a sentence, or performing 3-digit arithmetic. At the same time, we also identify some datasets where GPT-3's few-shot learning still struggles, as well as some datasets where GPT-3 faces methodological issues related to training on large web corpora. Finally, we find that GPT-3 can generate samples of news articles which human evaluators have difficulty distinguishing from articles written by humans. We discuss broader societal impacts of this finding and of GPT-3 in general.

---

### 4. Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer

**Authors:** Colin A. Raffel, Noam Shazeer, Adam Roberts, et al.  
**Year:** 2019 | **Citations:** 27,922 | **Venue:** Journal of machine learning research  
**Year Month:** [Oct 2019]  
**Fields:** Mathematics, Computer Science  
**URL:** [https://www.semanticscholar.org/paper/6c4b76232bb72897685d19b3d264c6ee3005bc2b](https://www.semanticscholar.org/paper/6c4b76232bb72897685d19b3d264c6ee3005bc2b)  
**arXiv:** [https://arxiv.org/abs/1910.10683](https://arxiv.org/abs/1910.10683)  

**Abstract:** Transfer learning, where a model is first pre-trained on a data-rich task before being fine-tuned on a downstream task, has emerged as a powerful technique in natural language processing (NLP). The effectiveness of transfer learning has given rise to a diversity of approaches, methodology, and practice. In this paper, we explore the landscape of transfer learning techniques for NLP by introducing a unified framework that converts every language problem into a text-to-text format. Our systematic study compares pre-training objectives, architectures, unlabeled datasets, transfer approaches, and other factors on dozens of language understanding tasks. By combining the insights from our exploration with scale and our new "Colossal Clean Crawled Corpus", we achieve state-of-the-art results on many benchmarks covering summarization, question answering, text classification, and more. To facilitate future work on transfer learning for NLP, we release our dataset, pre-trained models, and code.

---

### 5. Training language models to follow instructions with human feedback

**Authors:** Long Ouyang, Jeff Wu, Xu Jiang, et al.  
**Year:** 2022 | **Citations:** 25,305 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Mar 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/d766bffc357127e0dc86dd69561d5aeb520d6f4c](https://www.semanticscholar.org/paper/d766bffc357127e0dc86dd69561d5aeb520d6f4c)  
**arXiv:** [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)  

**Abstract:** Making language models bigger does not inherently make them better at following a user's intent. For example, large language models can generate outputs that are untruthful, toxic, or simply not helpful to the user. In other words, these models are not aligned with their users. In this paper, we show an avenue for aligning language models with user intent on a wide range of tasks by fine-tuning with human feedback. Starting with a set of labeler-written prompts and prompts submitted through the OpenAI API, we collect a dataset of labeler demonstrations of the desired model behavior, which we use to fine-tune GPT-3 using supervised learning. We then collect a dataset of rankings of model outputs, which we use to further fine-tune this supervised model using reinforcement learning from human feedback. We call the resulting models InstructGPT. In human evaluations on our prompt distribution, outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters. Moreover, InstructGPT models show improvements in truthfulness and reductions in toxic output generation while having minimal performance regressions on public NLP datasets. Even though InstructGPT still makes simple mistakes, our results show that fine-tuning with human feedback is a promising direction for aligning language models with human intent.

---

### 6. LLaMA: Open and Efficient Foundation Language Models

**Authors:** Hugo Touvron, Thibaut Lavril, Gautier Izacard, et al.  
**Year:** 2023 | **Citations:** 22,198 | **Venue:** arXiv.org  
**Year Month:** [Feb 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/57e849d0de13ed5f91d086936296721d4ff75a75](https://www.semanticscholar.org/paper/57e849d0de13ed5f91d086936296721d4ff75a75)  
**arXiv:** [https://arxiv.org/abs/2302.13971](https://arxiv.org/abs/2302.13971)  

**Abstract:** We introduce LLaMA, a collection of foundation language models ranging from 7B to 65B parameters. We train our models on trillions of tokens, and show that it is possible to train state-of-the-art models using publicly available datasets exclusively, without resorting to proprietary and inaccessible datasets. In particular, LLaMA-13B outperforms GPT-3 (175B) on most benchmarks, and LLaMA-65B is competitive with the best models, Chinchilla-70B and PaLM-540B. We release all our models to the research community.

---

### 7. Llama 2: Open Foundation and Fine-Tuned Chat Models

**Authors:** Hugo Touvron, Louis Martin, Kevin R. Stone, et al.  
**Year:** 2023 | **Citations:** 18,740 | **Venue:** arXiv.org  
**Year Month:** [Jul 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/104b0bb1da562d53cbda87aec79ef6a2827d191a](https://www.semanticscholar.org/paper/104b0bb1da562d53cbda87aec79ef6a2827d191a)  
**arXiv:** [https://arxiv.org/abs/2307.09288](https://arxiv.org/abs/2307.09288)  

**Abstract:** In this work, we develop and release Llama 2, a collection of pretrained and fine-tuned large language models (LLMs) ranging in scale from 7 billion to 70 billion parameters. Our fine-tuned LLMs, called Llama 2-Chat, are optimized for dialogue use cases. Our models outperform open-source chat models on most benchmarks we tested, and based on our human evaluations for helpfulness and safety, may be a suitable substitute for closed-source models. We provide a detailed description of our approach to fine-tuning and safety improvements of Llama 2-Chat in order to enable the community to build on our work and contribute to the responsible development of LLMs.

---


## RAG (Retrieval-Augmented Generation)

*Retrieved: 2026-10-27 01:23:11*

### 1. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Authors:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, et al.  
**Year:** 2020 | **Citations:** 20,054 | **Venue:** Neural Information Processing Systems  
**Year Month:** [May 2020]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/659bf9ce7175e1ec266ff54359e2bd76e0b7ff31](https://www.semanticscholar.org/paper/659bf9ce7175e1ec266ff54359e2bd76e0b7ff31)  
**arXiv:** [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)  

**Abstract:** Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

---

### 2. Retrieval-Augmented Generation for Large Language Models: A Survey

**Authors:** Yun-Fan Gao, Yun Xiong, Xin-Yu Gao, et al.  
**Year:** 2023 | **Citations:** 4,356 | **Venue:** arXiv.org  
**Year Month:** [Dec 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/46f9f7b8f88f72e12cbdb21e3311f995eb6e65c5](https://www.semanticscholar.org/paper/46f9f7b8f88f72e12cbdb21e3311f995eb6e65c5)  
**arXiv:** [https://arxiv.org/abs/2312.10997](https://arxiv.org/abs/2312.10997)  

**Abstract:** Large Language Models (LLMs) showcase impressive capabilities but encounter challenges like hallucination, outdated knowledge, and non-transparent, untraceable reasoning processes. Retrieval-Augmented Generation (RAG) has emerged as a promising solution by incorporating knowledge from external databases. This enhances the accuracy and credibility of the generation, particularly for knowledge-intensive tasks, and allows for continuous knowledge updates and integration of domain-specific information. RAG synergistically merges LLMs' intrinsic knowledge with the vast, dynamic repositories of external databases. This comprehensive review paper offers a detailed examination of the progression of RAG paradigms, encompassing the Naive RAG, the Advanced RAG, and the Modular RAG. It meticulously scrutinizes the tripartite foundation of RAG frameworks, which includes the retrieval, the generation and the augmentation techniques. The paper highlights the state-of-the-art technologies embedded in each of these critical components, providing a profound understanding of the advancements in RAG systems. Furthermore, this paper introduces up-to-date evaluation framework and benchmark. At the end, this article delineates the challenges currently faced and points out prospective avenues for research and development.

---

### 3. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

**Authors:** Lei Huang, Weijiang Yu, Wei-Tao Ma, et al.  
**Year:** 2023 | **Citations:** 4,093 | **Venue:** ACM Trans. Inf. Syst.  
**Year Month:** [Nov 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1e909e2a8cdacdcdff125ebcc566f37cb869a1c8](https://www.semanticscholar.org/paper/1e909e2a8cdacdcdff125ebcc566f37cb869a1c8)  
**arXiv:** [https://arxiv.org/abs/2311.05232](https://arxiv.org/abs/2311.05232)  

**Abstract:** The emergence of large language models (LLMs) has marked a significant breakthrough in natural language processing (NLP), fueling a paradigm shift in information acquisition. Nevertheless, LLMs are prone to hallucination, generating plausible yet nonfactual content. This phenomenon raises significant concerns over the reliability of LLMs in real-world information retrieval (IR) systems and has attracted intensive research to detect and mitigate such hallucinations. Given the open-ended general-purpose attributes inherent to LLMs, LLM hallucinations present distinct challenges that diverge from prior task-specific models. This divergence highlights the urgency for a nuanced understanding and comprehensive overview of recent advances in LLM hallucinations. In this survey, we begin with an innovative taxonomy of hallucination in the era of LLM and then delve into the factors contributing to hallucinations. Subsequently, we present a thorough overview of hallucination detection methods and benchmarks. Our discussion then transfers to representative methodologies for mitigating LLM hallucinations. Additionally, we delve into the current limitations faced by retrieval-augmented LLMs in combating hallucinations, offering insights for developing more robust IR systems. Finally, we highlight the promising research directions on LLM hallucinations, including hallucination in large vision-language models and understanding of knowledge boundaries in LLM hallucinations.

---

### 4. REALM: Retrieval-Augmented Language Model Pre-Training

**Authors:** Kelvin Guu, Kenton Lee, Zora Tung, et al.  
**Year:** 2020 | **Citations:** 3,555 | **Venue:** International Conference on Machine Learning  
**Year Month:** [Feb 2020]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/832fff14d2ed50eb7969c4c4b976c35776548f56](https://www.semanticscholar.org/paper/832fff14d2ed50eb7969c4c4b976c35776548f56)  
**arXiv:** [https://arxiv.org/abs/2002.08909](https://arxiv.org/abs/2002.08909)  

**Abstract:** Language model pre-training has been shown to capture a surprising amount of world knowledge, crucial for NLP tasks such as question answering. However, this knowledge is stored implicitly in the parameters of a neural network, requiring ever-larger networks to cover more facts. To capture knowledge in a more modular and interpretable way, we augment language model pre-training with a latent knowledge retriever, which allows the model to retrieve and attend over documents from a large corpus such as Wikipedia, used during pre-training, fine-tuning and inference. For the first time, we show how to pre-train such a knowledge retriever in an unsupervised manner, using masked language modeling as the learning signal and backpropagating through a retrieval step that considers millions of documents. We demonstrate the effectiveness of Retrieval-Augmented Language Model pre-training (REALM) by fine-tuning on the challenging task of Open-domain Question Answering (Open-QA). We compare against state-of-the-art models for both explicit and implicit knowledge storage on three popular Open-QA benchmarks, and find that we outperform all previous methods by a significant margin (4-16% absolute accuracy), while also providing qualitative benefits such as interpretability and modularity.

---

### 5. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

**Authors:** Akari Asai, Zeqiu Wu, Yizhong Wang, et al.  
**Year:** 2023 | **Citations:** 2,937 | **Venue:** International Conference on Learning Representations  
**Year Month:** [Oct 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/ddbd8fe782ac98e9c64dd98710687a962195dd9b](https://www.semanticscholar.org/paper/ddbd8fe782ac98e9c64dd98710687a962195dd9b)  
**arXiv:** [https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)  

**Abstract:** Despite their remarkable capabilities, large language models (LLMs) often produce responses containing factual inaccuracies due to their sole reliance on the parametric knowledge they encapsulate. Retrieval-Augmented Generation (RAG), an ad hoc approach that augments LMs with retrieval of relevant knowledge, decreases such issues. However, indiscriminately retrieving and incorporating a fixed number of retrieved passages, regardless of whether retrieval is necessary, or passages are relevant, diminishes LM versatility or can lead to unhelpful response generation. We introduce a new framework called Self-Reflective Retrieval-Augmented Generation (Self-RAG) that enhances an LM's quality and factuality through retrieval and self-reflection. Our framework trains a single arbitrary LM that adaptively retrieves passages on-demand, and generates and reflects on retrieved passages and its own generations using special tokens, called reflection tokens. Generating reflection tokens makes the LM controllable during the inference phase, enabling it to tailor its behavior to diverse task requirements. Experiments show that Self-RAG (7B and 13B parameters) significantly outperforms state-of-the-art LLMs and retrieval-augmented models on a diverse set of tasks. Specifically, Self-RAG outperforms ChatGPT and retrieval-augmented Llama2-chat on Open-domain QA, reasoning and fact verification tasks, and it shows significant gains in improving factuality and citation accuracy for long-form generations relative to these models.

---

### 6. From Local to Global: A Graph RAG Approach to Query-Focused Summarization

**Authors:** Darren Edge, Ha Trinh, Newman Cheng, et al.  
**Year:** 2024 | **Citations:** 2,429 | **Venue:** arXiv.org  
**Year Month:** [Apr 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/c1799bf28d1ae93e1631be5b59196ee1e568f538](https://www.semanticscholar.org/paper/c1799bf28d1ae93e1631be5b59196ee1e568f538)  
**arXiv:** [https://arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130)  

**Abstract:** The use of retrieval-augmented generation (RAG) to retrieve relevant information from an external knowledge source enables large language models (LLMs) to answer questions over private and/or previously unseen document collections. However, RAG fails on global questions directed at an entire text corpus, such as"What are the main themes in the dataset?", since this is inherently a query-focused summarization (QFS) task, rather than an explicit retrieval task. Prior QFS methods, meanwhile, do not scale to the quantities of text indexed by typical RAG systems. To combine the strengths of these contrasting methods, we propose GraphRAG, a graph-based approach to question answering over private text corpora that scales with both the generality of user questions and the quantity of source text. Our approach uses an LLM to build a graph index in two stages: first, to derive an entity knowledge graph from the source documents, then to pregenerate community summaries for all groups of closely related entities. Given a question, each community summary is used to generate a partial response, before all partial responses are again summarized in a final response to the user. For a class of global sensemaking questions over datasets in the 1 million token range, we show that GraphRAG leads to substantial improvements over a conventional RAG baseline for both the comprehensiveness and diversity of generated answers.

---

### 7. FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation

**Authors:** Sewon Min, Kalpesh Krishna, Xinxi Lyu, et al.  
**Year:** 2023 | **Citations:** 1,901 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [May 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/bd5deadc58ee45b5e004378ba1d54a96bc947b4a](https://www.semanticscholar.org/paper/bd5deadc58ee45b5e004378ba1d54a96bc947b4a)  
**arXiv:** [https://arxiv.org/abs/2305.14251](https://arxiv.org/abs/2305.14251)  

**Abstract:** Evaluating the factuality of long-form text generated by large language models (LMs) is non-trivial because (1) generations often contain a mixture of supported and unsupported pieces of information, making binary judgments of quality inadequate, and (2) human evaluation is time-consuming and costly. In this paper, we introduce FACTSCORE, a new evaluation that breaks a generation into a series of atomic facts and computes the percentage of atomic facts supported by a reliable knowledge source. We conduct an extensive human evaluation to obtain FACTSCOREs of people biographies generated by several state-of-the-art commercial LMs -- InstructGPT, ChatGPT, and the retrieval-augmented PerplexityAI -- and report new analysis demonstrating the need for such a fine-grained score (e.g., ChatGPT only achieves 58%). Since human evaluation is costly, we also introduce an automated model that estimates FACTSCORE using retrieval and a strong language model, with less than a 2% error rate. Finally, we use this automated metric to evaluate 6,500 generations from a new set of 13 recent LMs that would have cost $26K if evaluated by humans, with various findings: GPT-4 and ChatGPT are more factual than public models, and Vicuna and Alpaca are some of the best public models. FACTSCORE is available for public use via `pip install factscore`.

---

### 8. SGLang: Efficient Execution of Structured Language Model Programs

**Authors:** Lian-Min Zheng, Liangsheng Yin, Zhiqiang Xie, et al.  
**Year:** 2023 | **Citations:** 1,723 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Dec 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/eb95c327260725498404eb43ec370d419b8d92c7](https://www.semanticscholar.org/paper/eb95c327260725498404eb43ec370d419b8d92c7)  
**arXiv:** [https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)  

**Abstract:** Large language models (LLMs) are increasingly used for complex tasks that require multiple generation calls, advanced prompting techniques, control flow, and structured inputs/outputs. However, efficient systems are lacking for programming and executing these applications. We introduce SGLang, a system for efficient execution of complex language model programs. SGLang consists of a frontend language and a runtime. The frontend simplifies programming with primitives for generation and parallelism control. The runtime accelerates execution with novel optimizations like RadixAttention for KV cache reuse and compressed finite state machines for faster structured output decoding. Experiments show that SGLang achieves up to 6.4x higher throughput compared to state-of-the-art inference systems on various large language and multi-modal models on tasks including agent control, logical reasoning, few-shot learning benchmarks, JSON decoding, retrieval-augmented generation pipelines, and multi-turn chat. The code is publicly available at https://github.com/sgl-project/sglang

---

### 9. Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning

**Authors:** Bowen Jin, Hansi Zeng, Zhenrui Yue, et al.  
**Year:** 2025 | **Citations:** 1,696 | **Venue:** arXiv.org  
**Year Month:** [Mar 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1fcaafeb72142fe3d1a5d698a072d69778d244b0](https://www.semanticscholar.org/paper/1fcaafeb72142fe3d1a5d698a072d69778d244b0)  
**arXiv:** [https://arxiv.org/abs/2503.09516](https://arxiv.org/abs/2503.09516)  

**Abstract:** Efficiently acquiring external knowledge and up-to-date information is essential for effective reasoning and text generation in large language models (LLMs). Prompting advanced LLMs with reasoning capabilities to use search engines during inference is often suboptimal, as the LLM might not fully possess the capability on how to interact optimally with the search engine. This paper introduces Search-R1, an extension of reinforcement learning (RL) for reasoning frameworks where the LLM learns to autonomously generate (multiple) search queries during step-by-step reasoning with real-time retrieval. Search-R1 optimizes LLM reasoning trajectories with multi-turn search interactions, leveraging retrieved token masking for stable RL training and a simple outcome-based reward function. Experiments on seven question-answering datasets show that Search-R1 improves performance by 41% (Qwen2.5-7B) and 20% (Qwen2.5-3B) over various RAG baselines under the same setting. This paper further provides empirical insights into RL optimization methods, LLM choices, and response length dynamics in retrieval-augmented reasoning. The code and model checkpoints are available at https://github.com/PeterGriffinJin/Search-R1.

---

### 10. Few-shot Learning with Retrieval Augmented Language Models

**Authors:** Gautier Izacard, Patrick Lewis, M. Lomeli, et al.  
**Year:** 2022 | **Citations:** 1,453 | **Venue:** Journal of machine learning research  
**Year Month:** [Aug 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/916be31cbf847faa65cad0549e153f0c25b9f424](https://www.semanticscholar.org/paper/916be31cbf847faa65cad0549e153f0c25b9f424)  
**arXiv:** [https://arxiv.org/abs/2208.03299](https://arxiv.org/abs/2208.03299)  

**Abstract:** Large language models have shown impressive few-shot results on a wide range of tasks. However, when knowledge is key for such results, as is the case for tasks such as question answering and fact checking, massive parameter counts to store knowledge seem to be needed. Retrieval augmented models are known to excel at knowledge intensive tasks without the need for as many parameters, but it is unclear whether they work in few-shot settings. In this work we present Atlas, a carefully designed and pre-trained retrieval augmented language model able to learn knowledge intensive tasks with very few training examples. We perform evaluations on a wide range of tasks, including MMLU, KILT and NaturalQuestions, and study the impact of the content of the document index, showing that it can easily be updated. Notably, Atlas reaches over 42% accuracy on Natural Questions using only 64 examples, outperforming a 540B parameters model by 3% despite having 50x fewer parameters.

---

### 11. RAGAs: Automated Evaluation of Retrieval Augmented Generation

**Authors:** Shahul Es, J. James, Luis Espinosa-Anke, et al.  
**Year:** 2023 | **Citations:** 1,245 | **Venue:** Conference of the European Chapter of the Association for Computational Linguistics  
**Year Month:** [Sep 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/f5e9e5bbe22f0263be1f1ce88c66978a2b927772](https://www.semanticscholar.org/paper/f5e9e5bbe22f0263be1f1ce88c66978a2b927772)  
**arXiv:** [https://arxiv.org/abs/2309.15217](https://arxiv.org/abs/2309.15217)  

**Abstract:** We introduce RAGAs (Retrieval Augmented Generation Assessment), a framework for reference-free evaluation of Retrieval Augmented Generation (RAG) pipelines. RAGAs is available at [https://github.com/explodinggradients/ragas]. RAG systems are composed of a retrieval and an LLM based generation module. They provide LLMs with knowledge from a reference textual database, enabling them to act as a natural language layer between a user and textual databases, thus reducing the risk of hallucinations. Evaluating RAG architectures is challenging due to several dimensions to consider: the ability of the retrieval system to identify relevant and focused context passages, the ability of the LLM to exploit such passages faithfully, and the quality of the generation itself. With RAGAs, we introduce a suite of metrics that can evaluate these different dimensions without relying on ground truth human annotations. We posit that such a framework can contribute crucially to faster evaluation cycles of RAG architectures, which is especially important given the fast adoption of LLMs.

---

### 12. A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models

**Authors:** Wenqi Fan, Yujuan Ding, Liang-bo Ning, et al.  
**Year:** 2024 | **Citations:** 1,229 | **Venue:** Knowledge Discovery and Data Mining  
**Year Month:** [May 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/eb9c4a07a336e8deefe7b399c550d3af0241238e](https://www.semanticscholar.org/paper/eb9c4a07a336e8deefe7b399c550d3af0241238e)  
**arXiv:** [https://arxiv.org/abs/2405.06211](https://arxiv.org/abs/2405.06211)  

**Abstract:** As one of the most advanced techniques in AI, Retrieval-Augmented Generation (RAG) can offer reliable and up-to-date external knowledge, providing huge convenience for numerous tasks. Particularly in the era of AI-Generated Content (AIGC), the powerful capacity of retrieval in providing additional knowledge enables RAG to assist existing generative AI in producing high-quality outputs. Recently, Large Language Models (LLMs) have demonstrated revolutionary abilities in language understanding and generation, while still facing inherent limitations such as hallucinations and out-of-date internal knowledge. Given the powerful abilities of RAG in providing the latest and helpful auxiliary information, Retrieval-Augmented Large Language Models (RA-LLMs) have emerged to harness external and authoritative knowledge bases, rather than solely relying on the model's internal knowledge, to augment the quality of the generated content of LLMs. In this survey, we comprehensively review existing research studies in RA-LLMs, covering three primary technical perspectives: Furthermore, to deliver deeper insights, we discuss current limitations and several promising directions for future research. Updated information about this survey can be found at: https://advanced-recommender-systems.github.io/RAG-Meets-LLMs/

---

### 13. In-Context Retrieval-Augmented Language Models

**Authors:** Ori Ram, Yoav Levine, Itay Dalmedigos, et al.  
**Year:** 2023 | **Citations:** 1,180 | **Venue:** Transactions of the Association for Computational Linguistics  
**Year Month:** [Feb 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/465471bb5bf1a945549d6291c2d23367966b4957](https://www.semanticscholar.org/paper/465471bb5bf1a945549d6291c2d23367966b4957)  
**arXiv:** [https://arxiv.org/abs/2302.00083](https://arxiv.org/abs/2302.00083)  

**Abstract:** Abstract Retrieval-Augmented Language Modeling (RALM) methods, which condition a language model (LM) on relevant documents from a grounding corpus during generation, were shown to significantly improve language modeling performance. In addition, they can mitigate the problem of factually inaccurate text generation and provide natural source attribution mechanism. Existing RALM approaches focus on modifying the LM architecture in order to facilitate the incorporation of external information, significantly complicating deployment. This paper considers a simple alternative, which we dub In-Context RALM: leaving the LM architecture unchanged and prepending grounding documents to the input, without any further training of the LM. We show that In-Context RALM that builds on off-the-shelf general purpose retrievers provides surprisingly large LM gains across model sizes and diverse corpora. We also demonstrate that the document retrieval and ranking mechanism can be specialized to the RALM setting to further boost performance. We conclude that In-Context RALM has considerable potential to increase the prevalence of LM grounding, particularly in settings where a pretrained LM must be used without modification or even via API access.1

---

### 14. REPLUG: Retrieval-Augmented Black-Box Language Models

**Authors:** Weijia Shi, Sewon Min, Michihiro Yasunaga, et al.  
**Year:** 2023 | **Citations:** 1,154 | **Venue:** North American Chapter of the Association for Computational Linguistics  
**Year Month:** [Jan 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/07b14c24833400b79978b0a5f084803337e30a15](https://www.semanticscholar.org/paper/07b14c24833400b79978b0a5f084803337e30a15)  
**arXiv:** [https://arxiv.org/abs/2301.12652](https://arxiv.org/abs/2301.12652)  

**Abstract:** We introduce REPLUG, a retrieval-augmented language modeling framework that treats the language model (LM) as a black box and augments it with a tuneable retrieval model. Unlike prior retrieval-augmented LMs that train language models with special cross-attention mechanisms to encode the retrieved text, REPLUG simply prepends retrieved documents to the input for the frozen black-box LM. This simple design can be easily applied to any existing language models. Furthermore, we show that the LM can be used to supervise the retrieval model, which can then find documents that help the LM make better predictions. Our experiments demonstrate that REPLUG with the tuned retriever significantly improves the performance of GPT-3 (175B) on language modeling by 6.3%, as well as the performance of Codex on five-shot MMLU by 5.1%. Code is publicly released at github.com/swj0419/REPLUG.

---

### 15. Evaluating Very Long-Term Conversational Memory of LLM Agents

**Authors:** Adyasha Maharana, Dong-Ho Lee, S. Tulyakov, et al.  
**Year:** 2024 | **Citations:** 1,044 | **Venue:** Annual Meeting of the Association for Computational Linguistics  
**Year Month:** [Feb 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/0bf3a1867f7245b8a702093901c66b08b518eafc](https://www.semanticscholar.org/paper/0bf3a1867f7245b8a702093901c66b08b518eafc)  
**arXiv:** [https://arxiv.org/abs/2402.17753](https://arxiv.org/abs/2402.17753)  

**Abstract:** Existing works on long-term open-domain dialogues focus on evaluating model responses within contexts spanning no more than five chat sessions. Despite advancements in long-context large language models (LLMs) and retrieval augmented generation (RAG) techniques, their efficacy in very long-term dialogues remains unexplored. To address this research gap, we introduce a machine-human pipeline to generate high-quality, very long-term dialogues by leveraging LLM-based agent architectures and grounding their dialogues on personas and temporal event graphs. Moreover, we equip each agent with the capability of sharing and reacting to images. The generated conversations are verified and edited by human annotators for long-range consistency and grounding to the event graphs. Using this pipeline, we collect LoCoMo, a dataset of very long-term conversations, each encompassing 300 turns and 9K tokens on avg., over up to 35 sessions. Based on LoCoMo, we present a comprehensive evaluation benchmark to measure long-term memory in models, encompassing question answering, event summarization, and multi-modal dialogue generation tasks. Our experimental results indicate that LLMs exhibit challenges in understanding lengthy conversations and comprehending long-range temporal and causal dynamics within dialogues. Employing strategies like long-context LLMs or RAG can offer improvements but these models still substantially lag behind human performance.

---

### 16. Active Retrieval Augmented Generation

**Authors:** Zhengbao Jiang, Frank F. Xu, Luyu Gao, et al.  
**Year:** 2023 | **Citations:** 938 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [May 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/88884b8806262a4095036041e3567d450dba39f7](https://www.semanticscholar.org/paper/88884b8806262a4095036041e3567d450dba39f7)  
**arXiv:** [https://arxiv.org/abs/2305.06983](https://arxiv.org/abs/2305.06983)  

**Abstract:** Despite the remarkable ability of large language models (LMs) to comprehend and generate language, they have a tendency to hallucinate and create factually inaccurate output. Augmenting LMs by retrieving information from external knowledge resources is one promising solution. Most existing retrieval augmented LMs employ a retrieve-and-generate setup that only retrieves information once based on the input. This is limiting, however, in more general scenarios involving generation of long texts, where continually gathering information throughout generation is essential. In this work, we provide a generalized view of active retrieval augmented generation, methods that actively decide when and what to retrieve across the course of the generation. We propose Forward-Looking Active REtrieval augmented generation (FLARE), a generic method which iteratively uses a prediction of the upcoming sentence to anticipate future content, which is then utilized as a query to retrieve relevant documents to regenerate the sentence if it contains low-confidence tokens. We test FLARE along with baselines comprehensively over 4 long-form knowledge-intensive generation tasks/datasets. FLARE achieves superior or competitive performance on all tasks, demonstrating the effectiveness of our method. Code and datasets are available at https://github.com/jzbjyb/FLARE.

---

### 17. Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

**Authors:** Prateek Chhikara, Dev Khant, Saket Aryan, et al.  
**Year:** 2025 | **Citations:** 834 | **Venue:** European Conference on Artificial Intelligence  
**Year Month:** [Apr 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1d9c21a0fdb1cc16a32c5d490ebaf98436a23382](https://www.semanticscholar.org/paper/1d9c21a0fdb1cc16a32c5d490ebaf98436a23382)  
**arXiv:** [https://arxiv.org/abs/2504.19413](https://arxiv.org/abs/2504.19413)  

**Abstract:** Large Language Models (LLMs) have demonstrated remarkable prowess in generating contextually coherent responses, yet their fixed context windows pose fundamental challenges for maintaining consistency over prolonged multi-session dialogues. We introduce Mem0, a scalable memory-centric architecture that addresses this issue by dynamically extracting, consolidating, and retrieving salient information from ongoing conversations. Building on this foundation, we further propose an enhanced variant that leverages graph-based memory representations to capture complex relational structures among conversational elements. Through comprehensive evaluations on LOCOMO benchmark, we systematically compare our approaches against six baseline categories: (i) established memory-augmented systems, (ii) retrieval-augmented generation (RAG) with varying chunk sizes and k-values, (iii) a full-context approach that processes the entire conversation history, (iv) an open-source memory solution, (v) a proprietary model system, and (vi) a dedicated memory management platform. Empirical results show that our methods consistently outperform all existing memory systems across four question categories: single-hop, temporal, multi-hop, and open-domain. Notably, Mem0 achieves 26% relative improvements in the LLM-as-a-Judge metric over OpenAI, while Mem0 with graph memory achieves around 2% higher overall score than the base configuration. Beyond accuracy gains, we also markedly reduce computational overhead compared to full-context method. In particular, Mem0 attains a 91% lower p95 latency and saves more than 90% token cost, offering a compelling balance between advanced reasoning capabilities and practical deployment constraints. Our findings highlight critical role of structured, persistent memory mechanisms for long-term conversational coherence, paving the way for more reliable and efficient LLM-driven AI agents.

---

### 18. RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval

**Authors:** Parth Sarthi, Salman Abdullah, Aditi Tuli, et al.  
**Year:** 2024 | **Citations:** 819 | **Venue:** International Conference on Learning Representations  
**Year Month:** [Jan 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1d40f07569482d24e3335ffb31394d4bf1567e6f](https://www.semanticscholar.org/paper/1d40f07569482d24e3335ffb31394d4bf1567e6f)  
**arXiv:** [https://arxiv.org/abs/2401.18059](https://arxiv.org/abs/2401.18059)  

**Abstract:** Retrieval-augmented language models can better adapt to changes in world state and incorporate long-tail knowledge. However, most existing methods retrieve only short contiguous chunks from a retrieval corpus, limiting holistic understanding of the overall document context. We introduce the novel approach of recursively embedding, clustering, and summarizing chunks of text, constructing a tree with differing levels of summarization from the bottom up. At inference time, our RAPTOR model retrieves from this tree, integrating information across lengthy documents at different levels of abstraction. Controlled experiments show that retrieval with recursive summaries offers significant improvements over traditional retrieval-augmented LMs on several tasks. On question-answering tasks that involve complex, multi-step reasoning, we show state-of-the-art results; for example, by coupling RAPTOR retrieval with the use of GPT-4, we can improve the best performance on the QuALITY benchmark by 20% in absolute accuracy.

---

### 19. Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity

**Authors:** Soyeong Jeong, Jinheon Baek, Sukmin Cho, et al.  
**Year:** 2024 | **Citations:** 770 | **Venue:** North American Chapter of the Association for Computational Linguistics  
**Year Month:** [Mar 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/e5e8c6ac537e0f5b5db14170bc232d6f9e641bbc](https://www.semanticscholar.org/paper/e5e8c6ac537e0f5b5db14170bc232d6f9e641bbc)  
**arXiv:** [https://arxiv.org/abs/2403.14403](https://arxiv.org/abs/2403.14403)  

**Abstract:** Retrieval-Augmented Large Language Models (LLMs), which incorporate the non-parametric knowledge from external knowledge bases into LLMs, have emerged as a promising approach to enhancing response accuracy in several tasks, such as Question-Answering (QA). However, even though there are various approaches dealing with queries of different complexities, they either handle simple queries with unnecessary computational overhead or fail to adequately address complex multi-step queries; yet, not all user requests fall into only one of the simple or complex categories. In this work, we propose a novel adaptive QA framework that can dynamically select the most suitable strategy for (retrieval-augmented) LLMs from the simplest to the most sophisticated ones based on the query complexity. Also, this selection process is operationalized with a classifier, which is a smaller LM trained to predict the complexity level of incoming queries with automatically collected labels, obtained from actual predicted outcomes of models and inherent inductive biases in datasets. This approach offers a balanced strategy, seamlessly adapting between the iterative and single-step retrieval-augmented LLMs, as well as the no-retrieval methods, in response to a range of query complexities. We validate our model on a set of open-domain QA datasets, covering multiple query complexities, and show that ours enhances the overall efficiency and accuracy of QA systems, compared to relevant baselines including the adaptive retrieval approaches. Code is available at: https://github.com/starsuzi/Adaptive-RAG.

---

### 20. Retrieval-Augmented Generation for AI-Generated Content: A Survey

**Authors:** Penghao Zhao, Hailin Zhang, Qinhan Yu, et al.  
**Year:** 2024 | **Citations:** 764 | **Venue:** Data Science and Engineering  
**Year Month:** [Feb 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/ab15463babf98fffc6f683fe2026de0725b5e1a9](https://www.semanticscholar.org/paper/ab15463babf98fffc6f683fe2026de0725b5e1a9)  
**arXiv:** [https://arxiv.org/abs/2402.19473](https://arxiv.org/abs/2402.19473)  

**Abstract:** Advancements in model algorithms, the growth of foundational models, and access to high-quality datasets have propelled the evolution of Artificial Intelligence Generated Content (AIGC). Despite its notable successes, AIGC still faces hurdles such as updating knowledge, handling long-tail data, mitigating data leakage, and managing high training and inference costs. Retrieval-Augmented Generation (RAG) has recently emerged as a paradigm to address such challenges. In particular, RAG introduces the information retrieval process, which enhances the generation process by retrieving relevant objects from available data stores, leading to higher accuracy and better robustness. In this paper, we comprehensively review existing efforts that integrate RAG technique into AIGC scenarios. We first classify RAG foundations according to how the retriever augments the generator, distilling the fundamental abstractions of the augmentation methodologies for various retrievers and generators. This unified perspective encompasses all RAG scenarios, illuminating advancements and pivotal technologies that help with potential future progress. We also summarize additional enhancements methods for RAG, facilitating effective engineering and implementation of RAG systems. Then from another view, we survey on practical applications of RAG across different modalities and tasks, offering valuable references for researchers and practitioners. Furthermore, we introduce the benchmarks for RAG, discuss the limitations of current RAG systems, and suggest potential directions for future research. Github: https://github.com/PKU-DAIR/RAG-Survey.

---

### 21. Benchmarking Large Language Models in Retrieval-Augmented Generation

**Authors:** Jiawei Chen, Hong-Yu Lin, Xian-Pei Han, et al.  
**Year:** 2023 | **Citations:** 719 | **Venue:** AAAI Conference on Artificial Intelligence  
**Year Month:** [Sep 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/28e2ecb4183ebc0eec504b12dddc677f8aef8745](https://www.semanticscholar.org/paper/28e2ecb4183ebc0eec504b12dddc677f8aef8745)  
**arXiv:** [https://arxiv.org/abs/2309.01431](https://arxiv.org/abs/2309.01431)  

**Abstract:** Retrieval-Augmented Generation (RAG) is a promising approach for mitigating the hallucination of large language models (LLMs). However, existing research lacks rigorous evaluation of the impact of retrieval-augmented generation on different large language models, which make it challenging to identify the potential bottlenecks in the capabilities of RAG for different LLMs. In this paper, we systematically investigate the impact of Retrieval-Augmented Generation on large language models. We analyze the performance of different large language models in 4 fundamental abilities required for RAG, including noise robustness, negative rejection, information integration, and counterfactual robustness. To this end, we establish Retrieval-Augmented Generation Benchmark (RGB), a new corpus for RAG evaluation in both English and Chinese. RGB divides the instances within the benchmark into 4 separate testbeds based on the aforementioned fundamental abilities required to resolve the case. Then we evaluate 6 representative LLMs on RGB to diagnose the challenges of current LLMs when applying RAG. Evaluation reveals that while LLMs exhibit a certain degree of noise robustness, they still struggle significantly in terms of negative rejection, information integration, and dealing with false information. The aforementioned assessment outcomes indicate that there is still a considerable journey ahead to effectively apply RAG to LLMs.

---

### 22. Benchmarking Retrieval-Augmented Generation for Medicine

**Authors:** Guang-Zhi Xiong, Qiao Jin, Zhi-Yong Lu, et al.  
**Year:** 2024 | **Citations:** 679 | **Venue:** Annual Meeting of the Association for Computational Linguistics  
**Year Month:** [Feb 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/b798cf6af813638fab09a8af6ad0f3df6c241485](https://www.semanticscholar.org/paper/b798cf6af813638fab09a8af6ad0f3df6c241485)  
**arXiv:** [https://arxiv.org/abs/2402.13178](https://arxiv.org/abs/2402.13178)  

**Abstract:** While large language models (LLMs) have achieved state-of-the-art performance on a wide range of medical question answering (QA) tasks, they still face challenges with hallucinations and outdated knowledge. Retrieval-augmented generation (RAG) is a promising solution and has been widely adopted. However, a RAG system can involve multiple flexible components, and there is a lack of best practices regarding the optimal RAG setting for various medical purposes. To systematically evaluate such systems, we propose the Medical Information Retrieval-Augmented Generation Evaluation (MIRAGE), a first-of-its-kind benchmark including 7,663 questions from five medical QA datasets. Using MIRAGE, we conducted large-scale experiments with over 1.8 trillion prompt tokens on 41 combinations of different corpora, retrievers, and backbone LLMs through the MedRAG toolkit introduced in this work. Overall, MedRAG improves the accuracy of six different LLMs by up to 18% over chain-of-thought prompting, elevating the performance of GPT-3.5 and Mixtral to GPT-4-level. Our results show that the combination of various medical corpora and retrievers achieves the best performance. In addition, we discovered a log-linear scaling property and the"lost-in-the-middle"effects in medical RAG. We believe our comprehensive evaluations can serve as practical guidelines for implementing RAG systems for medicine.

---

### 23. Graph Retrieval-Augmented Generation: A Survey

**Authors:** Boci Peng, Yun Zhu, Yong-Chao Liu, et al.  
**Year:** 2024 | **Citations:** 673 | **Venue:** ACM Trans. Inf. Syst.  
**Year Month:** [Aug 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/9ab45aa875b56335303398e84a59a3756cd9d530](https://www.semanticscholar.org/paper/9ab45aa875b56335303398e84a59a3756cd9d530)  
**arXiv:** [https://arxiv.org/abs/2408.08921](https://arxiv.org/abs/2408.08921)  

**Abstract:** Recently, Retrieval-Augmented Generation (RAG) has achieved remarkable success in addressing the challenges of Large Language Models (LLMs) without necessitating retraining. By referencing an external knowledge base, RAG refines LLM outputs, effectively mitigating issues such as “hallucination,” lack of domain-specific knowledge, and outdated information. However, the complex structure of relationships among different entities in databases presents challenges for RAG systems. In response, GraphRAG leverages structural information across entities to enable more precise and comprehensive retrieval, capturing relational knowledge and facilitating more accurate, context-aware responses. Given the novelty and potential of GraphRAG, a systematic review of current technologies is imperative. This article provides the first comprehensive overview of GraphRAG methodologies. We formalize the GraphRAG workflow, encompassing Graph-Based Indexing, Graph-Guided Retrieval, and Graph-Enhanced Generation. We then outline the core technologies and training methods at each stage. Additionally, we examine downstream tasks, application domains, evaluation methodologies, and industrial use cases of GraphRAG. Finally, we explore future research directions to inspire further inquiries and advance progress in the field. In order to track recent progress, we set up a repository at https://github.com/pengboci/GraphRAG-Survey.

---

### 24. LeanDojo: Theorem Proving with Retrieval-Augmented Language Models

**Authors:** Kaiyu Yang, Aidan M. Swope, Alex Gu, et al.  
**Year:** 2023 | **Citations:** 637 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Jun 2023]  
**Fields:** Computer Science, Mathematics  
**URL:** [https://www.semanticscholar.org/paper/87875a07976c26f82705de1fc70041169e5d652b](https://www.semanticscholar.org/paper/87875a07976c26f82705de1fc70041169e5d652b)  
**arXiv:** [https://arxiv.org/abs/2306.15626](https://arxiv.org/abs/2306.15626)  

**Abstract:** Large language models (LLMs) have shown promise in proving formal theorems using proof assistants such as Lean. However, existing methods are difficult to reproduce or build on, due to private code, data, and large compute requirements. This has created substantial barriers to research on machine learning methods for theorem proving. This paper removes these barriers by introducing LeanDojo: an open-source Lean playground consisting of toolkits, data, models, and benchmarks. LeanDojo extracts data from Lean and enables interaction with the proof environment programmatically. It contains fine-grained annotations of premises in proofs, providing valuable data for premise selection: a key bottleneck in theorem proving. Using this data, we develop ReProver (Retrieval-Augmented Prover): an LLM-based prover augmented with retrieval for selecting premises from a vast math library. It is inexpensive and needs only one GPU week of training. Our retriever leverages LeanDojo's program analysis capability to identify accessible premises and hard negative examples, which makes retrieval much more effective. Furthermore, we construct a new benchmark consisting of 98,734 theorems and proofs extracted from Lean's math library. It features challenging data split requiring the prover to generalize to theorems relying on novel premises that are never used in training. We use this benchmark for training and evaluation, and experimental results demonstrate the effectiveness of ReProver over non-retrieval baselines and GPT-4. We thus provide the first set of open-source LLM-based theorem provers without any proprietary datasets and release it under a permissive MIT license to facilitate further research.

---

### 25. RepoCoder: Repository-Level Code Completion Through Iterative Retrieval and Generation

**Authors:** Fengji Zhang, B. Chen, Yue Zhang, et al.  
**Year:** 2023 | **Citations:** 635 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [Mar 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/af5c7848417882012203ac21399977ebda695a2b](https://www.semanticscholar.org/paper/af5c7848417882012203ac21399977ebda695a2b)  
**arXiv:** [https://arxiv.org/abs/2303.12570](https://arxiv.org/abs/2303.12570)  

**Abstract:** The task of repository-level code completion is to continue writing the unfinished code based on a broader context of the repository. While for automated code completion tools, it is difficult to utilize the useful information scattered in different files. We propose RepoCoder, a simple, generic, and effective framework to address the challenge. It streamlines the repository-level code completion process by incorporating a similarity-based retriever and a pre-trained code language model in an iterative retrieval-generation pipeline. RepoCoder makes effective utilization of repository-level information for code completion and has the ability to generate code at various levels of granularity. Moreover, we propose a new benchmark RepoEval, which consists of the latest and high-quality real-world repositories covering line, API invocation, and function body completion scenarios. Experimental results indicate that RepoCoder significantly improves the In-File completion baseline by over 10% in all settings and consistently outperforms the vanilla retrieval-augmented code completion approach. Furthermore, we validate the effectiveness of RepoCoder through comprehensive analysis, providing valuable insights for future research. Our source code and benchmark are publicly available: https://github.com/microsoft/CodeT/tree/main/RepoCoder

---

### 26. Memory-Based Model Editing at Scale

**Authors:** E. Mitchell, Charles Lin, Antoine Bosselut, et al.  
**Year:** 2022 | **Citations:** 623 | **Venue:** International Conference on Machine Learning  
**Year Month:** [Jun 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1d650f1afd45c59ff907396fe8b678595dcb85ea](https://www.semanticscholar.org/paper/1d650f1afd45c59ff907396fe8b678595dcb85ea)  
**arXiv:** [https://arxiv.org/abs/2206.06520](https://arxiv.org/abs/2206.06520)  

**Abstract:** Even the largest neural networks make errors, and once-correct predictions can become invalid as the world changes. Model editors make local updates to the behavior of base (pre-trained) models to inject updated knowledge or correct undesirable behaviors. Existing model editors have shown promise, but also suffer from insufficient expressiveness: they struggle to accurately model an edit's intended scope (examples affected by the edit), leading to inaccurate predictions for test inputs loosely related to the edit, and they often fail altogether after many edits. As a higher-capacity alternative, we propose Semi-Parametric Editing with a Retrieval-Augmented Counterfactual Model (SERAC), which stores edits in an explicit memory and learns to reason over them to modulate the base model's predictions as needed. To enable more rigorous evaluation of model editors, we introduce three challenging language model editing problems based on question answering, fact-checking, and dialogue generation. We find that only SERAC achieves high performance on all three problems, consistently outperforming existing approaches to model editing by a significant margin. Code, data, and additional project information will be made available at https://sites.google.com/view/serac-editing.

---

### 27. AI Agents vs. Agentic AI: A Conceptual Taxonomy, Applications and Challenges

**Authors:** Ranjan Sapkota, Konstantinos I. Roumeliotis, Manoj Karkee  
**Year:** 2025 | **Citations:** 615 | **Venue:** Information Fusion  
**Year Month:** [May 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/986e813f4c4f36786c3642cb9c8718586e47bdcf](https://www.semanticscholar.org/paper/986e813f4c4f36786c3642cb9c8718586e47bdcf)  
**arXiv:** [https://arxiv.org/abs/2505.10468](https://arxiv.org/abs/2505.10468)  

**Abstract:** This review critically distinguishes between AI Agents and Agentic AI, offering a structured, conceptual taxonomy, application mapping, and analysis of opportunities and challenges to clarify their divergent design philosophies and capabilities. We begin by outlining the search strategy and foundational definitions, characterizing AI Agents as modular systems driven and enabled by LLMs and LIMs for taskspecific automation. Generative AI is positioned as a precursor providing the foundation, with AI agents advancing through tool integration, prompt engineering, and reasoning enhancements. We then characterize Agentic AI systems, which, in contrast to AI Agents, represent a paradigm shift marked by multi-agent collaboration, dynamic task decomposition, persistent memory, and coordinated autonomy. Through a chronological evaluation of architectural evolution, operational mechanisms, interaction styles, and autonomy levels, we present a comparative analysis across both AI agents and agentic AI paradigms. Application domains enabled by AI Agents such as customer support, scheduling, and data summarization are then contrasted with Agentic AI deployments in research automation, robotic coordination, and medical decision support. We further examine unique challenges in each paradigm including hallucination, brittleness, emergent behavior, and coordination failure, and propose targeted solutions such as ReAct loops, retrieval-augmented generation (RAG), automation coordination layers, and causal modeling. This work aims to provide a roadmap for developing robust, scalable, and explainable AI-driven systems.

---

### 28. Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy

**Authors:** Zhihong Shao, Yeyun Gong, Ye-Long Shen, et al.  
**Year:** 2023 | **Citations:** 609 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [May 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/a1675f47125aa409525c5f759b5e6bcc1c8831aa](https://www.semanticscholar.org/paper/a1675f47125aa409525c5f759b5e6bcc1c8831aa)  
**arXiv:** [https://arxiv.org/abs/2305.15294](https://arxiv.org/abs/2305.15294)  

**Abstract:** Large language models are powerful text processors and reasoners, but are still subject to limitations including outdated knowledge and hallucinations, which necessitates connecting them to the world. Retrieval-augmented large language models have raised extensive attention for grounding model generation on external knowledge. However, retrievers struggle to capture relevance, especially for queries with complex information needs. Recent work has proposed to improve relevance modeling by having large language models actively involved in retrieval, i.e., to improve retrieval with generation. In this paper, we show that strong performance can be achieved by a method we call Iter-RetGen, which synergizes retrieval and generation in an iterative manner. A model output shows what might be needed to finish a task, and thus provides an informative context for retrieving more relevant knowledge which in turn helps generate a better output in the next iteration. Compared with recent work which interleaves retrieval with generation when producing an output, Iter-RetGen processes all retrieved knowledge as a whole and largely preserves the flexibility in generation without structural constraints. We evaluate Iter-RetGen on multi-hop question answering, fact verification, and commonsense reasoning, and show that it can flexibly leverage parametric knowledge and non-parametric knowledge, and is superior to or competitive with state-of-the-art retrieval-augmented baselines while causing fewer overheads of retrieval and generation. We can further improve performance via generation-augmented retrieval adaptation.

---

### 29. AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases

**Authors:** Zhaorun Chen, Zhen Xiang, Chao-Wei Xiao, et al.  
**Year:** 2024 | **Citations:** 579 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Jul 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/b6948a9e8b3eec5a56a80c69727154fcd7ececce](https://www.semanticscholar.org/paper/b6948a9e8b3eec5a56a80c69727154fcd7ececce)  
**arXiv:** [https://arxiv.org/abs/2407.12784](https://arxiv.org/abs/2407.12784)  

**Abstract:** LLM agents have demonstrated remarkable performance across various applications, primarily due to their advanced capabilities in reasoning, utilizing external knowledge and tools, calling APIs, and executing actions to interact with environments. Current agents typically utilize a memory module or a retrieval-augmented generation (RAG) mechanism, retrieving past knowledge and instances with similar embeddings from knowledge bases to inform task planning and execution. However, the reliance on unverified knowledge bases raises significant concerns about their safety and trustworthiness. To uncover such vulnerabilities, we propose a novel red teaming approach AgentPoison, the first backdoor attack targeting generic and RAG-based LLM agents by poisoning their long-term memory or RAG knowledge base. In particular, we form the trigger generation process as a constrained optimization to optimize backdoor triggers by mapping the triggered instances to a unique embedding space, so as to ensure that whenever a user instruction contains the optimized backdoor trigger, the malicious demonstrations are retrieved from the poisoned memory or knowledge base with high probability. In the meantime, benign instructions without the trigger will still maintain normal performance. Unlike conventional backdoor attacks, AgentPoison requires no additional model training or fine-tuning, and the optimized backdoor trigger exhibits superior transferability, in-context coherence, and stealthiness. Extensive experiments demonstrate AgentPoison's effectiveness in attacking three types of real-world LLM agents: RAG-based autonomous driving agent, knowledge-intensive QA agent, and healthcare EHRAgent. On each agent, AgentPoison achieves an average attack success rate higher than 80% with minimal impact on benign performance (less than 1%) with a poison rate less than 0.1%.

---

### 30. LightRAG: Simple and Fast Retrieval-Augmented Generation

**Authors:** Zirui Guo, Lianghao Xia, Yanhua Yu, et al.  
**Year:** 2024 | **Citations:** 562 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [Oct 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1ea143c34b9bc359780f79ba4d68dee68bcc1129](https://www.semanticscholar.org/paper/1ea143c34b9bc359780f79ba4d68dee68bcc1129)  
**arXiv:** [https://arxiv.org/abs/2410.05779](https://arxiv.org/abs/2410.05779)  

**Abstract:** Retrieval-Augmented Generation (RAG) systems enhance large language models (LLMs) by integrating external knowledge sources, enabling more accurate and contextually relevant responses tailored to user needs. However, existing RAG systems have significant limitations, including reliance on flat data representations and inadequate contextual awareness, which can lead to fragmented answers that fail to capture complex inter-dependencies. To address these challenges, we propose LightRAG, which incorporates graph structures into text indexing and retrieval processes. This innovative framework employs a dual-level retrieval system that enhances comprehensive information retrieval from both low-level and high-level knowledge discovery. Additionally, the integration of graph structures with vector representations facilitates efficient retrieval of related entities and their relationships, significantly improving response times while maintaining contextual relevance. This capability is further enhanced by an incremental update algorithm that ensures the timely integration of new data, allowing the system to remain effective and responsive in rapidly changing data environments. Extensive experimental validation demonstrates considerable improvements in retrieval accuracy and efficiency compared to existing approaches. We have made our LightRAG open-source and available at the link: https://github.com/HKUDS/LightRAG

---


## AI Agents

*Retrieved: 2026-10-27 01:23:11*

### 1. Qwen3 Technical Report

**Authors:** An Yang, An-Feng Li, Baosong Yang, et al.  
**Year:** 2025 | **Citations:** 9,640 | **Venue:**   
**Year Month:** [May 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/d2d84d56f730f81d276a02b48d5d44db5bde0b4a](https://www.semanticscholar.org/paper/d2d84d56f730f81d276a02b48d5d44db5bde0b4a)  
**arXiv:** [https://arxiv.org/abs/2505.09388](https://arxiv.org/abs/2505.09388)  

**Abstract:** In this work, we present Qwen3, the latest version of the Qwen model family. Qwen3 comprises a series of large language models (LLMs) designed to advance performance, efficiency, and multilingual capabilities. The Qwen3 series includes models of both dense and Mixture-of-Expert (MoE) architectures, with parameter scales ranging from 0.6 to 235 billion. A key innovation in Qwen3 is the integration of thinking mode (for complex, multi-step reasoning) and non-thinking mode (for rapid, context-driven responses) into a unified framework. This eliminates the need to switch between different models--such as chat-optimized models (e.g., GPT-4o) and dedicated reasoning models (e.g., QwQ-32B)--and enables dynamic mode switching based on user queries or chat templates. Meanwhile, Qwen3 introduces a thinking budget mechanism, allowing users to allocate computational resources adaptively during inference, thereby balancing latency and performance based on task complexity. Moreover, by leveraging the knowledge from the flagship models, we significantly reduce the computational resources required to build smaller-scale models, while ensuring their highly competitive performance. Empirical evaluations demonstrate that Qwen3 achieves state-of-the-art results across diverse benchmarks, including tasks in code generation, mathematical reasoning, agent tasks, etc., competitive against larger MoE models and proprietary models. Compared to its predecessor Qwen2.5, Qwen3 expands multilingual support from 29 to 119 languages and dialects, enhancing global accessibility through improved cross-lingual understanding and generation capabilities. To facilitate reproducibility and community-driven research and development, all Qwen3 models are publicly accessible under Apache 2.0.

---

### 2. Reflexion: language agents with verbal reinforcement learning

**Authors:** Noah Shinn, Federico Cassano, Edward Berman, et al.  
**Year:** 2023 | **Citations:** 6,312 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Mar 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/0671fd553dd670a4e820553a974bc48040ba0819](https://www.semanticscholar.org/paper/0671fd553dd670a4e820553a974bc48040ba0819)  
**arXiv:** [https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)  

**Abstract:** Large language models (LLMs) have been increasingly used to interact with external environments (e.g., games, compilers, APIs) as goal-driven agents. However, it remains challenging for these language agents to quickly and efficiently learn from trial-and-error as traditional reinforcement learning methods require extensive training samples and expensive model fine-tuning. We propose Reflexion, a novel framework to reinforce language agents not by updating weights, but instead through linguistic feedback. Concretely, Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials. Reflexion is flexible enough to incorporate various types (scalar values or free-form language) and sources (external or internally simulated) of feedback signals, and obtains significant improvements over a baseline agent across diverse tasks (sequential decision-making, coding, language reasoning). For example, Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%. We also conduct ablation and analysis studies using different feedback signals, feedback incorporation methods, and agent types, and provide insights into how they affect performance.

---

### 3. Generative Agents: Interactive Simulacra of Human Behavior

**Authors:** J. Park, Joseph O'Brien, C. Cai, et al.  
**Year:** 2023 | **Citations:** 6,146 | **Venue:** ACM Symposium on User Interface Software and Technology  
**Year Month:** [Apr 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/5278a8eb2ba2429d4029745caf4e661080073c81](https://www.semanticscholar.org/paper/5278a8eb2ba2429d4029745caf4e661080073c81)  
**arXiv:** [https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)  

**Abstract:** Believable proxies of human behavior can empower interactive applications ranging from immersive environments to rehearsal spaces for interpersonal communication to prototyping tools. In this paper, we introduce generative agents: computational software agents that simulate believable human behavior. Generative agents wake up, cook breakfast, and head to work; artists paint, while authors write; they form opinions, notice each other, and initiate conversations; they remember and reflect on days past as they plan the next day. To enable generative agents, we describe an architecture that extends a large language model to store a complete record of the agent’s experiences using natural language, synthesize those memories over time into higher-level reflections, and retrieve them dynamically to plan behavior. We instantiate generative agents to populate an interactive sandbox environment inspired by The Sims, where end users can interact with a small town of twenty-five agents using natural language. In an evaluation, these generative agents produce believable individual and emergent social behaviors. For example, starting with only a single user-specified notion that one agent wants to throw a Valentine’s Day party, the agents autonomously spread invitations to the party over the next two days, make new acquaintances, ask each other out on dates to the party, and coordinate to show up for the party together at the right time. We demonstrate through ablation that the components of our agent architecture—observation, planning, and reflection—each contribute critically to the believability of agent behavior. By fusing large language models with computational interactive agents, this work introduces architectural and interaction patterns for enabling believable simulations of human behavior.

---

### 4. A Survey of Large Language Models

**Authors:** W. Zhao, Kun Zhou, Junyi Li, et al.  
**Year:** 2023 | **Citations:** 5,173 | **Venue:** Frontiers Comput. Sci.  
**Year Month:** [Mar 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/36709000a9272e941338244ef80ff5ab1dd2bba1](https://www.semanticscholar.org/paper/36709000a9272e941338244ef80ff5ab1dd2bba1)  
**arXiv:** [https://arxiv.org/abs/2303.18223](https://arxiv.org/abs/2303.18223)  

**Abstract:** The rapid evolution of large language models (LLMs) has driven a transformative shift in artificial intelligence (AI), reshaping both research paradigms and practical applications. Distinguished from their predecessors by unprecedented scale and advanced capabilities, LLMs necessitate new frameworks for understanding their development, behavior, and societal impact. This survey systematically reviews recent advancements in LLM techniques across four key dimensions: (1) pre-training methodologies, which establish core model capabilities through large-scale self-supervised training, architectural innovations, and data curation strategies; (2) post-training techniques, including supervised fine-tuning and reinforcement learning, which adapt foundational models to downstream tasks and enhance their alignment and safety; (3) utilization strategies, such as in-context learning, prompt engineering, and agentic reasoning, that optimize real-world deployment and enable effective interaction with external environments; and (4) evaluation methods, encompassing benchmarks for key ability dimensions such as core language capabilities, reasoning, and safety, which support comprehensive and reliable assessment of model performance. Additionally, we identify critical research issues, including those concerning theoretical foundations, efficient scaling, alignment, and agentic capability, and highlight the open challenges they present. By synthesizing state-of-the-art insights and emerging trends, this survey aims to provide a systematic and comprehensive framework for understanding the trajectory, current limitations, and future directions of LLM progress.

---

### 5. Qwen Technical Report

**Authors:** Jinze Bai, Shuai Bai, Yun-Fei Chu, et al.  
**Year:** 2023 | **Citations:** 4,498 | **Venue:** arXiv.org  
**Year Month:** [Sep 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/5fc1a3a49e8f1d106118b69d1d6be3b6caa23da0](https://www.semanticscholar.org/paper/5fc1a3a49e8f1d106118b69d1d6be3b6caa23da0)  
**arXiv:** [https://arxiv.org/abs/2309.16609](https://arxiv.org/abs/2309.16609)  

**Abstract:** Large language models (LLMs) have revolutionized the field of artificial intelligence, enabling natural language processing tasks that were previously thought to be exclusive to humans. In this work, we introduce Qwen, the first installment of our large language model series. Qwen is a comprehensive language model series that encompasses distinct models with varying parameter counts. It includes Qwen, the base pretrained language models, and Qwen-Chat, the chat models finetuned with human alignment techniques. The base language models consistently demonstrate superior performance across a multitude of downstream tasks, and the chat models, particularly those trained using Reinforcement Learning from Human Feedback (RLHF), are highly competitive. The chat models possess advanced tool-use and planning capabilities for creating agent applications, showcasing impressive performance even when compared to bigger models on complex tasks like utilizing a code interpreter. Furthermore, we have developed coding-specialized models, Code-Qwen and Code-Qwen-Chat, as well as mathematics-focused models, Math-Qwen-Chat, which are built upon base language models. These models demonstrate significantly improved performance in comparison with open-source models, and slightly fall behind the proprietary models.

---

### 6. A survey on large language model based autonomous agents

**Authors:** Lei Wang, Chengbang Ma, Xue-Yang Feng, et al.  
**Year:** 2023 | **Citations:** 4,239 | **Venue:** Frontiers of Computer Science  
**Year Month:** [Aug 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/28c6ac721f54544162865f41c5692e70d61bccab](https://www.semanticscholar.org/paper/28c6ac721f54544162865f41c5692e70d61bccab)  
**arXiv:** [https://arxiv.org/abs/2308.11432](https://arxiv.org/abs/2308.11432)  

**Abstract:** Autonomous agents have long been a research focus in academic and industry communities. Previous research often focuses on training agents with limited knowledge within isolated environments, which diverges significantly from human learning processes, and makes the agents hard to achieve human-like decisions. Recently, through the acquisition of vast amounts of Web knowledge, large language models (LLMs) have shown potential in human-level intelligence, leading to a surge in research on LLM-based autonomous agents. In this paper, we present a comprehensive survey of these studies, delivering a systematic review of LLM-based autonomous agents from a holistic perspective. We first discuss the construction of LLM-based autonomous agents, proposing a unified framework that encompasses much of previous work. Then, we present a overview of the diverse applications of LLM-based autonomous agents in social science, natural science, and engineering. Finally, we delve into the evaluation strategies commonly used for LLM-based autonomous agents. Based on the previous studies, we also present several challenges and future directions in this field.

---

### 7. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

**Authors:** Brian Ichter, Anthony Brohan, Yevgen Chebotar, et al.  
**Year:** 2022 | **Citations:** 4,043 | **Venue:** Conference on Robot Learning  
**Year Month:** [Apr 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/cb5e3f085caefd1f3d5e08637ab55d39e61234fc](https://www.semanticscholar.org/paper/cb5e3f085caefd1f3d5e08637ab55d39e61234fc)  
**arXiv:** [https://arxiv.org/abs/2204.01691](https://arxiv.org/abs/2204.01691)  

**Abstract:** Large language models can encode a wealth of semantic knowledge about the world. Such knowledge could be extremely useful to robots aiming to act upon high-level, temporally extended instructions expressed in natural language. However, a significant weakness of language models is that they lack real-world experience, which makes it difficult to leverage them for decision making within a given embodiment. For example, asking a language model to describe how to clean a spill might result in a reasonable narrative, but it may not be applicable to a particular agent, such as a robot, that needs to perform this task in a particular environment. We propose to provide real-world grounding by means of pretrained skills, which are used to constrain the model to propose natural language actions that are both feasible and contextually appropriate. The robot can act as the language model's"hands and eyes,"while the language model supplies high-level semantic knowledge about the task. We show how low-level skills can be combined with large language models so that the language model provides high-level knowledge about the procedures for performing complex and temporally-extended instructions, while value functions associated with these skills provide the grounding necessary to connect this knowledge to a particular physical environment. We evaluate our method on a number of real-world robotic tasks, where we show the need for real-world grounding and that this approach is capable of completing long-horizon, abstract, natural language instructions on a mobile manipulator. The project's website and the video can be found at https://say-can.github.io/.

---

### 8. A Survey on Evaluation of Large Language Models

**Authors:** Yu-Peng Chang, Xu Wang, Jin-Dong Wang, et al.  
**Year:** 2023 | **Citations:** 3,955 | **Venue:** ACM Transactions on Intelligent Systems and Technology  
**Year Month:** [Jul 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/888728745dbb769e29ed475d4f7661eebe1a71cf](https://www.semanticscholar.org/paper/888728745dbb769e29ed475d4f7661eebe1a71cf)  
**arXiv:** [https://arxiv.org/abs/2307.03109](https://arxiv.org/abs/2307.03109)  

**Abstract:** Large language models (LLMs) are gaining increasing popularity in both academia and industry, owing to their unprecedented performance in various applications. As LLMs continue to play a vital role in both research and daily use, their evaluation becomes increasingly critical, not only at the task level, but also at the society level for better understanding of their potential risks. Over the past years, significant efforts have been made to examine LLMs from various perspectives. This paper presents a comprehensive review of these evaluation methods for LLMs, focusing on three key dimensions: what to evaluate, where to evaluate, and how to evaluate. Firstly, we provide an overview from the perspective of evaluation tasks, encompassing general natural language processing tasks, reasoning, medical usage, ethics, education, natural and social sciences, agent applications, and other areas. Secondly, we answer the ‘where’ and ‘how’ questions by diving into the evaluation methods and benchmarks, which serve as crucial components in assessing the performance of LLMs. Then, we summarize the success and failure cases of LLMs in different tasks. Finally, we shed light on several future challenges that lie ahead in LLMs evaluation. Our aim is to offer invaluable insights to researchers in the realm of LLMs evaluation, thereby aiding the development of more proficient LLMs. Our key point is that evaluation should be treated as an essential discipline to better assist the development of LLMs. We consistently maintain the related open-source materials at: https://github.com/MLGroupJLU/LLM-eval-survey

---

### 9. Qwen3-VL Technical Report

**Authors:** Shuai Bai, Yuxuan Cai, Rui-Zhe Chen, et al.  
**Year:** 2025 | **Citations:** 2,966 | **Venue:** arXiv.org  
**Year Month:** [Nov 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/15538df854dd33351dfb5cefd7e8f3340c8936c3](https://www.semanticscholar.org/paper/15538df854dd33351dfb5cefd7e8f3340c8936c3)  
**arXiv:** [https://arxiv.org/abs/2511.21631](https://arxiv.org/abs/2511.21631)  

**Abstract:** We introduce Qwen3-VL, the most capable vision-language model in the Qwen series to date, achieving superior performance across a broad range of multimodal benchmarks. It natively supports interleaved contexts of up to 256K tokens, seamlessly integrating text, images, and video. The model family includes both dense (2B/4B/8B/32B) and mixture-of-experts (30B-A3B/235B-A22B) variants to accommodate diverse latency-quality trade-offs. Qwen3-VL delivers three core pillars: (i) markedly stronger pure-text understanding, surpassing comparable text-only backbones in several cases; (ii) robust long-context comprehension with a native 256K-token window for both text and interleaved multimodal inputs, enabling faithful retention, retrieval, and cross-referencing across long documents and videos; and (iii) advanced multimodal reasoning across single-image, multi-image, and video tasks, demonstrating leading performance on comprehensive evaluations such as MMMU and visual-math benchmarks (e.g., MathVista and MathVision). Architecturally, we introduce three key upgrades: (i) an enhanced interleaved-MRoPE for stronger spatial-temporal modeling across images and video; (ii) DeepStack integration, which effectively leverages multi-level ViT features to tighten vision-language alignment; and (iii) text-based time alignment for video, evolving from T-RoPE to explicit textual timestamp alignment for more precise temporal grounding. Under comparable token budgets and latency constraints, Qwen3-VL achieves superior performance in both dense and Mixture-of-Experts (MoE) architectures. We envision Qwen3-VL serving as a foundational engine for image-grounded reasoning, agentic decision-making, and multimodal code intelligence in real-world workflows.

---

### 10. Voyager: An Open-Ended Embodied Agent with Large Language Models

**Authors:** Guanzhi Wang, Yuqi Xie, Yunfan Jiang, et al.  
**Year:** 2023 | **Citations:** 2,714 | **Venue:** Trans. Mach. Learn. Res.  
**Year Month:** [May 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/f197bf0fc2f228483f6af3285000d54d8d97f9eb](https://www.semanticscholar.org/paper/f197bf0fc2f228483f6af3285000d54d8d97f9eb)  
**arXiv:** [https://arxiv.org/abs/2305.16291](https://arxiv.org/abs/2305.16291)  

**Abstract:** We introduce Voyager, the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention. Voyager consists of three key components: 1) an automatic curriculum that maximizes exploration, 2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and 3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification for program improvement. Voyager interacts with GPT-4 via blackbox queries, which bypasses the need for model parameter fine-tuning. The skills developed by Voyager are temporally extended, interpretable, and compositional, which compounds the agent's abilities rapidly and alleviates catastrophic forgetting. Empirically, Voyager shows strong in-context lifelong learning capability and exhibits exceptional proficiency in playing Minecraft. It obtains 3.3x more unique items, travels 2.3x longer distances, and unlocks key tech tree milestones up to 15.3x faster than prior SOTA. Voyager is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other techniques struggle to generalize. We open-source our full codebase and prompts at https://voyager.minedojo.org/.

---

### 11. MetaGPT: Meta Programming for Multi-Agent Collaborative Framework

**Authors:** Si-Rui Hong, Xia-Wu Zheng, Jonathan P. Chen, et al.  
**Year:** 2023 | **Citations:** 2,691 | **Venue:** arXiv.org  
**Year Month:** [Aug 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/703035b483c181953de1b55b5fd59cd4cd4cf211](https://www.semanticscholar.org/paper/703035b483c181953de1b55b5fd59cd4cd4cf211)  
**arXiv:** [https://arxiv.org/abs/2308.00352](https://arxiv.org/abs/2308.00352)  

**Abstract:** Recently, remarkable progress has been made in automated task-solving through the use of multi-agent driven by large language models (LLMs). However, existing LLM-based multi-agent works primarily focus on solving simple dialogue tasks, and complex tasks are rarely studied, mainly due to the LLM hallucination problem. This type of hallucination becomes cascading when naively chaining multiple intelligent agents, resulting in a failure to effectively address complex problems. Therefore, we introduce MetaGPT, an innovative framework that incorporates efficient human workflows as a meta programming approach into LLM-based multi-agent collaboration. Specifically, MetaGPT encodes Standardized Operating Procedures (SOPs) into prompts to enhance structured coordination. Subsequently, it mandates modular outputs, empowering agents with domain expertise comparable to human professionals, to validate outputs and minimize compounded errors. In this way, MetaGPT leverages the assembly line paradigm to assign diverse roles to various agents, thereby establishing a framework that can effectively and cohesively deconstruct complex multi-agent collaborative problems. Our experiments on collaborative software engineering benchmarks demonstrate that MetaGPT generates more coherent and correct solutions compared to existing chat-based multi-agent systems. This highlights the potential of integrating human domain knowledge into multi-agent systems, thereby creating new opportunities to tackle complex real-world challenges. The GitHub repository of this project is publicly available on:https://github.com/geekan/MetaGPT.

---

### 12. WebArena: A Realistic Web Environment for Building Autonomous Agents

**Authors:** Shuyan Zhou, Frank F. Xu, Hao Zhu, et al.  
**Year:** 2023 | **Citations:** 2,368 | **Venue:** International Conference on Learning Representations  
**Year Month:** [Jul 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/e41482f4ee984f17382f6cdd900df094d928be06](https://www.semanticscholar.org/paper/e41482f4ee984f17382f6cdd900df094d928be06)  
**arXiv:** [https://arxiv.org/abs/2307.13854](https://arxiv.org/abs/2307.13854)  

**Abstract:** With advances in generative AI, there is now potential for autonomous agents to manage daily tasks via natural language commands. However, current agents are primarily created and tested in simplified synthetic environments, leading to a disconnect with real-world scenarios. In this paper, we build an environment for language-guided agents that is highly realistic and reproducible. Specifically, we focus on agents that perform tasks on the web, and create an environment with fully functional websites from four common domains: e-commerce, social forum discussions, collaborative software development, and content management. Our environment is enriched with tools (e.g., a map) and external knowledge bases (e.g., user manuals) to encourage human-like task-solving. Building upon our environment, we release a set of benchmark tasks focusing on evaluating the functional correctness of task completions. The tasks in our benchmark are diverse, long-horizon, and designed to emulate tasks that humans routinely perform on the internet. We experiment with several baseline agents, integrating recent techniques such as reasoning before acting. The results demonstrate that solving complex tasks is challenging: our best GPT-4-based agent only achieves an end-to-end task success rate of 14.41%, significantly lower than the human performance of 78.24%. These results highlight the need for further development of robust agents, that current state-of-the-art large language models are far from perfect performance in these real-life tasks, and that WebArena can be used to measure such progress.

---

### 13. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

**Authors:** John Yang, Carlos E. Jimenez, Alexander Wettig, et al.  
**Year:** 2024 | **Citations:** 2,275 | **Venue:** Neural Information Processing Systems  
**Year Month:** [May 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/1c3c531fc0fbe79f97f367ed3648de8467caeeaa](https://www.semanticscholar.org/paper/1c3c531fc0fbe79f97f367ed3648de8467caeeaa)  
**arXiv:** [https://arxiv.org/abs/2405.15793](https://arxiv.org/abs/2405.15793)  

**Abstract:** Language model (LM) agents are increasingly being used to automate complicated tasks in digital environments. Just as humans benefit from powerful software applications, such as integrated development environments, for complex tasks like software engineering, we posit that LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces to the software they use. We investigate how interface design affects the performance of language model agents. As a result of this exploration, we introduce SWE-agent: a system that facilitates LM agents to autonomously use computers to solve software engineering tasks. SWE-agent's custom agent-computer interface (ACI) significantly enhances an agent's ability to create and edit code files, navigate entire repositories, and execute tests and other programs. We evaluate SWE-agent on SWE-bench and HumanEvalFix, achieving state-of-the-art performance on both with a pass@1 rate of 12.5% and 87.7%, respectively, far exceeding the previous state-of-the-art achieved with non-interactive LMs. Finally, we provide insight on how the design of the ACI can impact agents' behavior and performance.

---

### 14. The Rise and Potential of Large Language Model Based Agents: A Survey

**Authors:** Zhiheng Xi, Wen-Xiang Chen, Xin Guo, et al.  
**Year:** 2023 | **Citations:** 2,164 | **Venue:** arXiv.org  
**Year Month:** [Sep 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/0c72450890a54b68d63baa99376131fda8f06cf9](https://www.semanticscholar.org/paper/0c72450890a54b68d63baa99376131fda8f06cf9)  
**arXiv:** [https://arxiv.org/abs/2309.07864](https://arxiv.org/abs/2309.07864)  

**Abstract:** For a long time, humanity has pursued artificial intelligence (AI) equivalent to or surpassing the human level, with AI agents considered a promising vehicle for this pursuit. AI agents are artificial entities that sense their environment, make decisions, and take actions. Many efforts have been made to develop intelligent agents, but they mainly focus on advancement in algorithms or training strategies to enhance specific capabilities or performance on particular tasks. Actually, what the community lacks is a general and powerful model to serve as a starting point for designing AI agents that can adapt to diverse scenarios. Due to the versatile capabilities they demonstrate, large language models (LLMs) are regarded as potential sparks for Artificial General Intelligence (AGI), offering hope for building general AI agents. Many researchers have leveraged LLMs as the foundation to build AI agents and have achieved significant progress. In this paper, we perform a comprehensive survey on LLM-based agents. We start by tracing the concept of agents from its philosophical origins to its development in AI, and explain why LLMs are suitable foundations for agents. Building upon this, we present a general framework for LLM-based agents, comprising three main components: brain, perception, and action, and the framework can be tailored for different applications. Subsequently, we explore the extensive applications of LLM-based agents in three aspects: single-agent scenarios, multi-agent scenarios, and human-agent cooperation. Following this, we delve into agent societies, exploring the behavior and personality of LLM-based agents, the social phenomena that emerge from an agent society, and the insights they offer for human society. Finally, we discuss several key topics and open problems within the field. A repository for the related papers at https://github.com/WooooDyy/LLM-Agent-Paper-List.

---

### 15. CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society

**Authors:** G. Li, Hasan Hammoud, Hani Itani, et al.  
**Year:** 2023 | **Citations:** 2,082 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Mar 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/7bf72a3b5fbac8bc0f461780810fbc781c28ef53](https://www.semanticscholar.org/paper/7bf72a3b5fbac8bc0f461780810fbc781c28ef53)  
**arXiv:** [https://arxiv.org/abs/2303.17760](https://arxiv.org/abs/2303.17760)  

**Abstract:** The rapid advancement of chat-based language models has led to remarkable progress in complex task-solving. However, their success heavily relies on human input to guide the conversation, which can be challenging and time-consuming. This paper explores the potential of building scalable techniques to facilitate autonomous cooperation among communicative agents, and provides insight into their"cognitive"processes. To address the challenges of achieving autonomous cooperation, we propose a novel communicative agent framework named role-playing. Our approach involves using inception prompting to guide chat agents toward task completion while maintaining consistency with human intentions. We showcase how role-playing can be used to generate conversational data for studying the behaviors and capabilities of a society of agents, providing a valuable resource for investigating conversational language models. In particular, we conduct comprehensive studies on instruction-following cooperation in multi-agent settings. Our contributions include introducing a novel communicative agent framework, offering a scalable approach for studying the cooperative behaviors and capabilities of multi-agent systems, and open-sourcing our library to support research on communicative agents and beyond: https://github.com/camel-ai/camel.

---

### 16. MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts

**Authors:** Pan Lu, Hritik Bansal, Tony Xia, et al.  
**Year:** 2023 | **Citations:** 2,028 | **Venue:** International Conference on Learning Representations  
**Year Month:** [Oct 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/8946891e94831adc8cddb0d32311cce2445c96d2](https://www.semanticscholar.org/paper/8946891e94831adc8cddb0d32311cce2445c96d2)  
**arXiv:** [https://arxiv.org/abs/2310.02255](https://arxiv.org/abs/2310.02255)  

**Abstract:** Large Language Models (LLMs) and Large Multimodal Models (LMMs) exhibit impressive problem-solving skills in many tasks and domains, but their ability in mathematical reasoning in visual contexts has not been systematically studied. To bridge this gap, we present MathVista, a benchmark designed to combine challenges from diverse mathematical and visual tasks. It consists of 6,141 examples, derived from 28 existing multimodal datasets involving mathematics and 3 newly created datasets (i.e., IQTest, FunctionQA, and PaperQA). Completing these tasks requires fine-grained, deep visual understanding and compositional reasoning, which all state-of-the-art foundation models find challenging. With MathVista, we have conducted a comprehensive, quantitative evaluation of 12 prominent foundation models. The best-performing GPT-4V model achieves an overall accuracy of 49.9%, substantially outperforming Bard, the second-best performer, by 15.1%. Our in-depth analysis reveals that the superiority of GPT-4V is mainly attributed to its enhanced visual perception and mathematical reasoning. However, GPT-4V still falls short of human performance by 10.4%, as it often struggles to understand complex figures and perform rigorous reasoning. This significant gap underscores the critical role that MathVista will play in the development of general-purpose AI agents capable of tackling mathematically intensive and visually rich real-world tasks. We further explore the new ability of self-verification, the application of self-consistency, and the interactive chatbot capabilities of GPT-4V, highlighting its promising potential for future research. The project is available at https://mathvista.github.io/.

---

### 17. HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face

**Authors:** Yongliang Shen, Kai-Tao Song, Xu Tan, et al.  
**Year:** 2023 | **Citations:** 1,835 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Mar 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/d1120d67b700e4dfe8b39eb1e48fbdea4e1a0c43](https://www.semanticscholar.org/paper/d1120d67b700e4dfe8b39eb1e48fbdea4e1a0c43)  
**arXiv:** [https://arxiv.org/abs/2303.17580](https://arxiv.org/abs/2303.17580)  

**Abstract:** Solving complicated AI tasks with different domains and modalities is a key step toward artificial general intelligence. While there are numerous AI models available for various domains and modalities, they cannot handle complicated AI tasks autonomously. Considering large language models (LLMs) have exhibited exceptional abilities in language understanding, generation, interaction, and reasoning, we advocate that LLMs could act as a controller to manage existing AI models to solve complicated AI tasks, with language serving as a generic interface to empower this. Based on this philosophy, we present HuggingGPT, an LLM-powered agent that leverages LLMs (e.g., ChatGPT) to connect various AI models in machine learning communities (e.g., Hugging Face) to solve AI tasks. Specifically, we use ChatGPT to conduct task planning when receiving a user request, select models according to their function descriptions available in Hugging Face, execute each subtask with the selected AI model, and summarize the response according to the execution results. By leveraging the strong language capability of ChatGPT and abundant AI models in Hugging Face, HuggingGPT can tackle a wide range of sophisticated AI tasks spanning different modalities and domains and achieve impressive results in language, vision, speech, and other challenging tasks, which paves a new way towards the realization of artificial general intelligence.

---

### 18. Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents

**Authors:** Wen-Long Huang, P. Abbeel, Deepak Pathak, et al.  
**Year:** 2022 | **Citations:** 1,774 | **Venue:** International Conference on Machine Learning  
**Year Month:** [Jan 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/92a8f7f09f3705cb5a6009a42220a6f01ea084e8](https://www.semanticscholar.org/paper/92a8f7f09f3705cb5a6009a42220a6f01ea084e8)  
**arXiv:** [https://arxiv.org/abs/2201.07207](https://arxiv.org/abs/2201.07207)  

**Abstract:** Can world knowledge learned by large language models (LLMs) be used to act in interactive environments? In this paper, we investigate the possibility of grounding high-level tasks, expressed in natural language (e.g."make breakfast"), to a chosen set of actionable steps (e.g."open fridge"). While prior work focused on learning from explicit step-by-step examples of how to act, we surprisingly find that if pre-trained LMs are large enough and prompted appropriately, they can effectively decompose high-level tasks into mid-level plans without any further training. However, the plans produced naively by LLMs often cannot map precisely to admissible actions. We propose a procedure that conditions on existing demonstrations and semantically translates the plans to admissible actions. Our evaluation in the recent VirtualHome environment shows that the resulting method substantially improves executability over the LLM baseline. The conducted human evaluation reveals a trade-off between executability and correctness but shows a promising sign towards extracting actionable knowledge from language models. Website at https://huangwl18.github.io/language-planner

---

### 19. Inner Monologue: Embodied Reasoning through Planning with Language Models

**Authors:** Wen-Long Huang, F. Xia, Ted Xiao, et al.  
**Year:** 2022 | **Citations:** 1,764 | **Venue:** Conference on Robot Learning  
**Year Month:** [Jul 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/f3cf71c51b882fe3111d71c4bf104297d38197f8](https://www.semanticscholar.org/paper/f3cf71c51b882fe3111d71c4bf104297d38197f8)  
**arXiv:** [https://arxiv.org/abs/2207.05608](https://arxiv.org/abs/2207.05608)  

**Abstract:** Recent works have shown how the reasoning capabilities of Large Language Models (LLMs) can be applied to domains beyond natural language processing, such as planning and interaction for robots. These embodied problems require an agent to understand many semantic aspects of the world: the repertoire of skills available, how these skills influence the world, and how changes to the world map back to the language. LLMs planning in embodied environments need to consider not just what skills to do, but also how and when to do them - answers that change over time in response to the agent's own choices. In this work, we investigate to what extent LLMs used in such embodied contexts can reason over sources of feedback provided through natural language, without any additional training. We propose that by leveraging environment feedback, LLMs are able to form an inner monologue that allows them to more richly process and plan in robotic control scenarios. We investigate a variety of sources of feedback, such as success detection, scene description, and human interaction. We find that closed-loop language feedback significantly improves high-level instruction completion on three domains, including simulated and real table top rearrangement tasks and long-horizon mobile manipulation tasks in a kitchen environment in the real world.

---

### 20. SGLang: Efficient Execution of Structured Language Model Programs

**Authors:** Lian-Min Zheng, Liangsheng Yin, Zhiqiang Xie, et al.  
**Year:** 2023 | **Citations:** 1,723 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Dec 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/eb95c327260725498404eb43ec370d419b8d92c7](https://www.semanticscholar.org/paper/eb95c327260725498404eb43ec370d419b8d92c7)  
**arXiv:** [https://arxiv.org/abs/2312.07104](https://arxiv.org/abs/2312.07104)  

**Abstract:** Large language models (LLMs) are increasingly used for complex tasks that require multiple generation calls, advanced prompting techniques, control flow, and structured inputs/outputs. However, efficient systems are lacking for programming and executing these applications. We introduce SGLang, a system for efficient execution of complex language model programs. SGLang consists of a frontend language and a runtime. The frontend simplifies programming with primitives for generation and parallelism control. The runtime accelerates execution with novel optimizations like RadixAttention for KV cache reuse and compressed finite state machines for faster structured output decoding. Experiments show that SGLang achieves up to 6.4x higher throughput compared to state-of-the-art inference systems on various large language and multi-modal models on tasks including agent control, logical reasoning, few-shot learning benchmarks, JSON decoding, retrieval-augmented generation pipelines, and multi-turn chat. The code is publicly available at https://github.com/sgl-project/sglang

---

### 21. MemGPT: Towards LLMs as Operating Systems

**Authors:** Charles Packer, Sarah Wooders, Kevin Lin, et al.  
**Year:** 2023 | **Citations:** 1,705 | **Venue:** arXiv.org  
**Year Month:** [Oct 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/908dad62c0e43d80e3e3cb3c0402f7c71c70499c](https://www.semanticscholar.org/paper/908dad62c0e43d80e3e3cb3c0402f7c71c70499c)  
**arXiv:** [https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)  

**Abstract:** Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis. To enable using context beyond limited context windows, we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory. Using this technique, we introduce MemGPT (Memory-GPT), a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window, and utilizes interrupts to manage control flow between itself and the user. We evaluate our OS-inspired design in two domains where the limited context windows of modern LLMs severely handicaps their performance: document analysis, where MemGPT is able to analyze large documents that far exceed the underlying LLM's context window, and multi-session chat, where MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users. We release MemGPT code and data for our experiments at https://memgpt.ai.

---

### 22. Ethical and social risks of harm from Language Models

**Authors:** Laura Weidinger, John F. J. Mellor, Maribeth Rauh, et al.  
**Year:** 2021 | **Citations:** 1,704 | **Venue:** arXiv.org  
**Year Month:** [Dec 2021]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/fd1b829261ba04bb92e0ab60c4f6e7cea0d99fbf](https://www.semanticscholar.org/paper/fd1b829261ba04bb92e0ab60c4f6e7cea0d99fbf)  
**arXiv:** [https://arxiv.org/abs/2112.04359](https://arxiv.org/abs/2112.04359)  

**Abstract:** This paper aims to help structure the risk landscape associated with large-scale Language Models (LMs). In order to foster advances in responsible innovation, an in-depth understanding of the potential risks posed by these models is needed. A wide range of established and anticipated risks are analysed in detail, drawing on multidisciplinary expertise and literature from computer science, linguistics, and social sciences. We outline six specific risk areas: I. Discrimination, Exclusion and Toxicity, II. Information Hazards, III. Misinformation Harms, V. Malicious Uses, V. Human-Computer Interaction Harms, VI. Automation, Access, and Environmental Harms. The first area concerns the perpetuation of stereotypes, unfair discrimination, exclusionary norms, toxic language, and lower performance by social group for LMs. The second focuses on risks from private data leaks or LMs correctly inferring sensitive information. The third addresses risks arising from poor, false or misleading information including in sensitive domains, and knock-on risks such as the erosion of trust in shared information. The fourth considers risks from actors who try to use LMs to cause harm. The fifth focuses on risks specific to LLMs used to underpin conversational agents that interact with human users, including unsafe use, manipulation or deception. The sixth discusses the risk of environmental harm, job automation, and other challenges that may have a disparate effect on different social groups or communities. In total, we review 21 risks in-depth. We discuss the points of origin of different risks and point to potential mitigation approaches. Lastly, we discuss organisational responsibilities in implementing mitigations, and the role of collaboration and participation. We highlight directions for further research, particularly on expanding the toolkit for assessing and evaluating the outlined risks in LMs.

---

### 23. InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency

**Authors:** Wei-Yun Wang, Zhangwei Gao, Li-Xin Gu, et al.  
**Year:** 2025 | **Citations:** 1,614 | **Venue:** arXiv.org  
**Year Month:** [Aug 2025]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/18d83103fb98905ccbce420987470eb2ea021187](https://www.semanticscholar.org/paper/18d83103fb98905ccbce420987470eb2ea021187)  
**arXiv:** [https://arxiv.org/abs/2508.18265](https://arxiv.org/abs/2508.18265)  

**Abstract:** We introduce InternVL 3.5, a new family of open-source multimodal models that significantly advances versatility, reasoning capability, and inference efficiency along the InternVL series. A key innovation is the Cascade Reinforcement Learning (Cascade RL) framework, which enhances reasoning through a two-stage process: offline RL for stable convergence and online RL for refined alignment. This coarse-to-fine training strategy leads to substantial improvements on downstream reasoning tasks, e.g., MMMU and MathVista. To optimize efficiency, we propose a Visual Resolution Router (ViR) that dynamically adjusts the resolution of visual tokens without compromising performance. Coupled with ViR, our Decoupled Vision-Language Deployment (DvD) strategy separates the vision encoder and language model across different GPUs, effectively balancing computational load. These contributions collectively enable InternVL3.5 to achieve up to a +16.0\% gain in overall reasoning performance and a 4.05$\times$ inference speedup compared to its predecessor, i.e., InternVL3. In addition, InternVL3.5 supports novel capabilities such as GUI interaction and embodied agency. Notably, our largest model, i.e., InternVL3.5-241B-A28B, attains state-of-the-art results among open-source MLLMs across general multimodal, reasoning, text, and agentic tasks -- narrowing the performance gap with leading commercial models like GPT-5. All models and code are publicly released.

---

### 24. τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

**Authors:** Shun-Yu Yao, Noah Shinn, Pedram Razavi, et al.  
**Year:** 2024 | **Citations:** 1,597 | **Venue:** arXiv.org  
**Year Month:** [Jun 2024]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/70aa016c1f68fd5c0261f26ad20017b8307650af](https://www.semanticscholar.org/paper/70aa016c1f68fd5c0261f26ad20017b8307650af)  
**arXiv:** [https://arxiv.org/abs/2406.12045](https://arxiv.org/abs/2406.12045)  

**Abstract:** Existing benchmarks do not test language agents on their interaction with human users or ability to follow domain-specific rules, both of which are vital for deploying them in real world applications. We propose $\tau$-bench, a benchmark emulating dynamic conversations between a user (simulated by language models) and a language agent provided with domain-specific API tools and policy guidelines. We employ an efficient and faithful evaluation process that compares the database state at the end of a conversation with the annotated goal state. We also propose a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials. Our experiments show that even state-of-the-art function calling agents (like gpt-4o) succeed on<50% of the tasks, and are quite inconsistent (pass^8<25% in retail). Our findings point to the need for methods that can improve the ability of agents to act consistently and follow rules reliably.

---

### 25. WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents

**Authors:** Shunyu Yao, Howard Chen, John Yang, et al.  
**Year:** 2022 | **Citations:** 1,587 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Jul 2022]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/23525374cfd3af714f3ffb7a203b1ef3253333fe](https://www.semanticscholar.org/paper/23525374cfd3af714f3ffb7a203b1ef3253333fe)  
**arXiv:** [https://arxiv.org/abs/2207.01206](https://arxiv.org/abs/2207.01206)  

**Abstract:** Existing benchmarks for grounding language in interactive environments either lack real-world linguistic elements, or prove difficult to scale up due to substantial human involvement in the collection of data or feedback signals. To bridge this gap, we develop WebShop -- a simulated e-commerce website environment with $1.18$ million real-world products and $12,087$ crowd-sourced text instructions. Given a text instruction specifying a product requirement, an agent needs to navigate multiple types of webpages and issue diverse actions to find, customize, and purchase an item. WebShop provides several challenges for language grounding including understanding compositional instructions, query (re-)formulation, comprehending and acting on noisy text in webpages, and performing strategic exploration. We collect over $1,600$ human demonstrations for the task, and train and evaluate a diverse range of agents using reinforcement learning, imitation learning, and pre-trained image and language models. Our best model achieves a task success rate of $29\%$, which outperforms rule-based heuristics ($9.6\%$) but is far lower than human expert performance ($59\%$). We also analyze agent and human trajectories and ablate various model components to provide insights for developing future agents with stronger language understanding and decision making abilities. Finally, we show that agents trained on WebShop exhibit non-trivial sim-to-real transfer when evaluated on amazon.com and ebay.com, indicating the potential value of WebShop in developing practical web-based agents that can operate in the wild.

---

### 26. Mind2Web: Towards a Generalist Agent for the Web

**Authors:** Xiang Deng, Yu Gu, Boyuan Zheng, et al.  
**Year:** 2023 | **Citations:** 1,585 | **Venue:** Neural Information Processing Systems  
**Year Month:** [Jun 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/58f8925a8b87054ad0635a6398a7fe24935b1604](https://www.semanticscholar.org/paper/58f8925a8b87054ad0635a6398a7fe24935b1604)  
**arXiv:** [https://arxiv.org/abs/2306.06070](https://arxiv.org/abs/2306.06070)  

**Abstract:** We introduce Mind2Web, the first dataset for developing and evaluating generalist agents for the web that can follow language instructions to complete complex tasks on any website. Existing datasets for web agents either use simulated websites or only cover a limited set of websites and tasks, thus not suitable for generalist web agents. With over 2,000 open-ended tasks collected from 137 websites spanning 31 domains and crowdsourced action sequences for the tasks, Mind2Web provides three necessary ingredients for building generalist web agents: 1) diverse domains, websites, and tasks, 2) use of real-world websites instead of simulated and simplified ones, and 3) a broad spectrum of user interaction patterns. Based on Mind2Web, we conduct an initial exploration of using large language models (LLMs) for building generalist web agents. While the raw HTML of real-world websites are often too large to be fed to LLMs, we show that first filtering it with a small LM significantly improves the effectiveness and efficiency of LLMs. Our solution demonstrates a decent level of performance, even on websites or entire domains the model has never seen before, but there is still a substantial room to improve towards truly generalizable agents. We open-source our dataset, model implementation, and trained models (https://osu-nlp-group.github.io/Mind2Web) to facilitate further research on building a generalist agent for the web.

---

### 27. AgentBench: Evaluating LLMs as Agents

**Authors:** Xiao Liu, Hao Yu, Hanchen Zhang, et al.  
**Year:** 2023 | **Citations:** 1,544 | **Venue:** International Conference on Learning Representations  
**Year Month:** [Aug 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/5dbf93a68b7fda600521f046dea35ea8ba9e884f](https://www.semanticscholar.org/paper/5dbf93a68b7fda600521f046dea35ea8ba9e884f)  
**arXiv:** [https://arxiv.org/abs/2308.03688](https://arxiv.org/abs/2308.03688)  

**Abstract:** The potential of Large Language Model (LLM) as agents has been widely acknowledged recently. Thus, there is an urgent need to quantitatively \textit{evaluate LLMs as agents} on challenging tasks in interactive environments. We present AgentBench, a multi-dimensional benchmark that consists of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities. Our extensive test over \num API-based and open-sourced (OSS) LLMs shows that, while top commercial LLMs present a strong ability of acting as agents in complex environments, there is a significant disparity in performance between them and many OSS competitors that are no larger than 70B. We identify the typical reasons of failures in environments and LLMs, showing that poor long-term reasoning, decision-making, and instruction following abilities are the main obstacles for developing usable LLM agents. Improving instruction following and training on high quality multi-round alignment data could improve agent performance. And different from existing assumptions, training on code present ambivalent impacts on different agent tasks. Datasets, environments, and an integrated evaluation package for AgentBench are released at https://github.com/THUDM/AgentBench.

---

### 28. Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate

**Authors:** Tian Liang, Zhiwei He, Wenxiang Jiao, et al.  
**Year:** 2023 | **Citations:** 1,494 | **Venue:** Conference on Empirical Methods in Natural Language Processing  
**Year Month:** [May 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/385c74957858e7d6856d48e72b5a902b4c1aa28c](https://www.semanticscholar.org/paper/385c74957858e7d6856d48e72b5a902b4c1aa28c)  
**arXiv:** [https://arxiv.org/abs/2305.19118](https://arxiv.org/abs/2305.19118)  

**Abstract:** Modern large language models (LLMs) like ChatGPT have shown remarkable performance on general language tasks but still struggle on complex reasoning tasks, which drives the research on cognitive behaviors of LLMs to explore human-like problem-solving strategies. Along this direction, one representative strategy is self-reflection, which asks an LLM to refine the solution with the feedback generated by itself iteratively. However, our study shows that such reflection-style methods suffer from the Degeneration-of-Thought (DoT) problem: once the LLM has established confidence in its solutions, it is unable to generate novel thoughts later through reflection even if its initial stance is incorrect. To address the DoT problem, we propose a Multi-Agent Debate (MAD) framework, in which multiple agents express their arguments in the state of “tit for tat” and a judge manages the debate process to obtain a final solution. Clearly, our MAD framework encourages divergent thinking in LLMs which would be helpful for tasks that require deep levels of contemplation. Experiment results on two challenging datasets, commonsense machine translation and counter-intuitive arithmetic reasoning, demonstrate the effectiveness of our MAD framework. Extensive analyses suggest that the adaptive break of debate and the modest level of “tit for tat” state are required for MAD to obtain good performance. Moreover, we find that LLMs might not be a fair judge if different LLMs are used for agents.

---

### 29. Augmenting large language models with chemistry tools

**Authors:** Andrés M Bran, Sam Cox, Oliver Schilter, et al.  
**Year:** 2023 | **Citations:** 1,397 | **Venue:** Nature Machine Intelligence  
**Year Month:** [Apr 2023]  
**Fields:** Physics, Mathematics, Medicine, Computer Science  
**URL:** [https://www.semanticscholar.org/paper/354dcdebf3f8b5feeed5c62090e0bc1f0c28db06](https://www.semanticscholar.org/paper/354dcdebf3f8b5feeed5c62090e0bc1f0c28db06)  
**arXiv:** [https://arxiv.org/abs/2304.05376](https://arxiv.org/abs/2304.05376)  

**Abstract:** Large language models (LLMs) have shown strong performance in tasks across domains but struggle with chemistry-related problems. These models also lack access to external knowledge sources, limiting their usefulness in scientific applications. We introduce ChemCrow, an LLM chemistry agent designed to accomplish tasks across organic synthesis, drug discovery and materials design. By integrating 18 expert-designed tools and using GPT-4 as the LLM, ChemCrow augments the LLM performance in chemistry, and new capabilities emerge. Our agent autonomously planned and executed the syntheses of an insect repellent and three organocatalysts and guided the discovery of a novel chromophore. Our evaluation, including both LLM and expert assessments, demonstrates ChemCrow’s effectiveness in automating a diverse set of chemical tasks. Our work not only aids expert chemists and lowers barriers for non-experts but also fosters scientific advancement by bridging the gap between experimental and computational chemistry. Large language models can be queried to perform chain-of-thought reasoning on text descriptions of data or computational tools, which can enable flexible and autonomous workflows. Bran et al. developed ChemCrow, a GPT-4-based agent that has access to computational chemistry tools and a robotic chemistry platform, which can autonomously solve tasks for designing or synthesizing chemicals such as drugs or materials.

---

### 30. ChatDev: Communicative Agents for Software Development

**Authors:** Cheng Qian, Wei Liu, Hongzhang Liu, et al.  
**Year:** 2023 | **Citations:** 1,379 | **Venue:** Annual Meeting of the Association for Computational Linguistics  
**Year Month:** [Jul 2023]  
**Fields:** Computer Science  
**URL:** [https://www.semanticscholar.org/paper/9474b463654fd92a62c103b21f95aed94b087907](https://www.semanticscholar.org/paper/9474b463654fd92a62c103b21f95aed94b087907)  
**arXiv:** [https://arxiv.org/abs/2307.07924](https://arxiv.org/abs/2307.07924)  

**Abstract:** Software development is a complex task that necessitates cooperation among multiple members with diverse skills. Numerous studies used deep learning to improve specific phases in a waterfall model, such as design, coding, and testing. However, the deep learning model in each phase requires unique designs, leading to technical inconsistencies across various phases, which results in a fragmented and ineffective development process. In this paper, we introduce ChatDev, a chat-powered software development framework in which specialized agents driven by large language models (LLMs) are guided in what to communicate (via chat chain) and how to communicate (via communicative dehallucination). These agents actively contribute to the design, coding, and testing phases through unified language-based communication, with solutions derived from their multi-turn dialogues. We found their utilization of natural language is advantageous for system design, and communicating in programming language proves helpful in debugging. This paradigm demonstrates how linguistic communication facilitates multi-agent collaboration, establishing language as a unifying bridge for autonomous task-solving among LLM agents. The code and data are available at https://github.com/OpenBMB/ChatDev.

---

