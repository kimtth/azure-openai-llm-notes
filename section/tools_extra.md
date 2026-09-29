# Tools, Datasets, and Evaluation

**Navigation Guide:** Choose the evaluation or operations resources that match the system under study; arrows show a suggested progression.

| Goal | Start with |
|---|---|
| Compare base-model capabilities | [LLM Evaluation Benchmarks](#llm-evaluation-benchmarks) |
| Assess RAG quality | [RAG Solution Design](best_practices.md#rag-solution-design) → [RAG Research](best_practices.md#rag-research) |
| Evaluate agent and tool-use behavior | [Tool Calling & Agentic](#tool-calling--agentic) benchmarks |
| Evaluate and operate a deployed application | [Evaluation Metrics](#evaluation-metrics) → [LLMOps](#llmops-large-language-model-operations) |

### **Contents**

- [Datasets for LLM Training](#datasets-for-llm-training)
- [Evaluating Large Language Models](#evaluating-large-language-models)
  - [LLM Evaluation Benchmarks](#llm-evaluation-benchmarks)
    - [Tool Calling & Agentic](#tool-calling--agentic)
  - [Evaluation Metrics](#evaluation-metrics)
- [LLMOps: Large Language Model Operations](#llmops-large-language-model-operations)
- [LLM for Robotics](#llm-for-robotics)
- [Awesome Demo](#awesome-demo)

## **Datasets for LLM Training**

##### Dataset Catalogs and Collections

- [LLMDataHub: Awesome Datasets for LLM Training](https://github.com/Zjh-819/LLMDataHub): A quick guide (especially) for trending instruction finetuning datasets
 ![**github stars**](https://img.shields.io/github/stars/Zjh-819/LLMDataHub?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Open LLMs and Datasets](https://github.com/eugeneyan/open-llms): A list of open LLMs available for commercial use.
 ![**github stars**](https://img.shields.io/github/stars/eugeneyan/open-llms?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

##### Synthetic / LLM-Generated Datasets

- [Nemotron-Personas-Japan: Synthesized Data for Sovereign AI🤗](https://huggingface.co/blog/nvidia/nemotron-personas-japan): The first open synthetic dataset that captures Japan's demographic, geographic, and cultural spectrum.  [23 Sep 2025]
- [Self-Alignment with Instruction Backtranslation📑](https://arxiv.org/abs/2308.06259): Without human seeding, use LLM to produce instruction-response pairs. The process involves two steps: self-augmentation and self-curation. [11 Aug 2023]
- [Self-Instruct📑](https://arxiv.org/abs/2212.10560): Seed task pool with a set of human-written instructions. [20 Dec 2022]
- [Synthetic Data of LLMs](https://github.com/wasiahmad/Awesome-LLM-Synthetic-Data): A reading list on LLM based Synthetic Data Generation [Oct 2024]
 ![**github stars**](https://img.shields.io/github/stars/wasiahmad/Awesome-LLM-Synthetic-Data?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Synthetic Data Vault (SDV) ](https://github.com/sdv-dev/SDV): Synthetic data generation for tabular data [May 2018] ![**github stars**](https://img.shields.io/github/stars/sdv-dev/SDV?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

##### QA and Search Datasets

- [MS MARCO Web Search](https://github.com/microsoft/MS-MARCO-Web-Search): A large-scale information-rich web dataset, featuring millions of real clicked query-document labels [Apr 2024]
 ![**github stars**](https://img.shields.io/github/stars/microsoft/MS-MARCO-Web-Search?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/): The Stanford Question Answering Dataset (SQuAD), a set of Wikipedia articles, 100,000+ question-answer pairs on 500+ articles. [16 Jun 2016]

##### Pretraining

- [arXiv Bulk Data Access](https://info.arxiv.org/help/bulk_data_s3.html) - Bulk scientific and technical paper corpus.
- [C4🤗](https://huggingface.co/datasets/allenai/c4) - Cleaned web corpus introduced for T5 pretraining.
- [Common Crawl](https://commoncrawl.org) - Raw web-scale corpus used for many LLM training datasets.
- [Dolma🤗](https://huggingface.co/datasets/allenai/dolma) - Multi-trillion-token open corpus from AI2.
- [FineWeb🤗](https://huggingface.co/datasets/HuggingFaceFW/fineweb):Crawled 15 trillion tokens of high-quality web data from the summer of 2013 to March 2024. [Apr 2024]
- [GitHub Archive Program](https://archiveprogram.github.com) - Public source-code archive used for programming corpora.
- [RedPajama](https://together.ai/blog/redpajama): LLaMA training dataset of over 1.2 trillion tokens / [git](https://github.com/togethercomputer/RedPajama-Data) [17 Apr 2023]
 ![**github stars**](https://img.shields.io/github/stars/togethercomputer/RedPajama-Data?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [RefinedWeb🤗](https://huggingface.co/datasets/tiiuae/falcon-refinedweb) - Filtered Common Crawl derivative used in Falcon models.
- [The Pile](https://pile.eleuther.ai) - Curated mixture of 22 diverse text sources.
- [The Stack📑](https://arxiv.org/abs/2211.15533):💡Large, license-aware source-code corpus for training code LLMs, with provenance metadata, near-deduplication, and an opt-out process. [🤗](https://huggingface.co/datasets/bigcode/the-stack) [20 Nov 2022]
- [Wikipedia Dumps](https://dumps.wikimedia.org) - Encyclopedic source commonly included in pretraining mixtures.

##### Mid-Training

- [Dolmino Mix🤗](https://huggingface.co/datasets/allenai/dolmino-mix-1124) - Capability-improvement dataset mixture after pretraining.
- [Longmino Mix🤗](https://huggingface.co/datasets/allenai/dolma3_longmino_mix-100B-1125) - Long-context and advanced reasoning dataset mixture.
- [MegaMath-Web-Pro-Max🤗](https://huggingface.co/datasets/OctoThinker/MegaMath-Web-Pro-Max) - Mathematics and reasoning-focused training dataset.

##### Supervised Fine-Tuning (SFT)

- [Alpaca🤗](https://huggingface.co/datasets/tatsu-lab/alpaca) - 🏆Instruction-following prompt-response dataset from self-instruct methods.
- [Dolci-Think-SFT🤗](https://huggingface.co/datasets/allenai/Dolci-Think-SFT-32B) - Reasoning-oriented supervised fine-tuning dataset.
- [MathInstruct🤗](https://huggingface.co/datasets/TIGER-Lab/MathInstruct) - Mathematical instruction-following dataset for SFT.
- [Open Thoughts](https://github.com/open-thoughts/open-thoughts): Fully Open Data Curation for Thinking Models [28 Jan 2025] ![**github stars**](https://img.shields.io/github/stars/open-thoughts/open-thoughts?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

##### Preference Optimization / Alignment

- [Dolci-Think-DPO-7B🤗](https://huggingface.co/datasets/allenai/Dolci-Think-DPO-7B) - Reasoning-focused preference optimization dataset.
- [UltraFeedback🤗](https://huggingface.co/datasets/openbmb/UltraFeedback) - 💡Large-scale preference ranking dataset for DPO and RLHF.

##### Pretrain for a base model

```json
{
    "text": ...,
    "meta": {"url": "...", "timestamp": "...", "source": "...", "language": "...", ...},
    "red_pajama_subset": "common_crawl" | "c4" | "github" | "books" | "arxiv" | "wikipedia" | "stackexchange"
}
```

databricks-dolly-15k: Instruction-Tuned [🤗](https://huggingface.co/datasets/databricks/databricks-dolly-15k): SFT training - QA pairs or Dialog

```json
{
  "prompt": "What is the capital of France?",
  "response": "The capital of France is Paris."
},
{
    "prompt": "Can you give me a recipe for chocolate chip cookies?",
    "response": "Sure! ..."
}
```

[Anthropic human-feedback🤗](https://huggingface.co/datasets/Anthropic/hh-rlhf): RLHF training - Chosen and Rejected pairs

```json
{
  "chosen": "I'm sorry to hear that. Is there anything I can do to help?",
  "rejected": "That's too bad. You should just get over it."
}
```

<!-- - [大規模言語モデルのデータセットまとめ](https://note.com/npaka/n/n686d987adfb1): 大規模言語モデルのデータセットまとめ [Apr 2023] -->
<!-- - [Dataset example](https://docs.argilla.io/) -->

##### SFT Dataset

| Category | Instruction | Context | Response |
| --- | --- | --- | --- |
| 0 | Open QA | How do I get rid of mosquitos in my house? | You can get rid of mosquitos in your house by ... |
| 1 | Classification | Classify each country as "African" or "European" | Nigeria: African<br>Rwanda: African<br>Portugal: European |
| 2 | Information Extraction | Extract the unique names of composers from the text. | To some extent, European and the US traditions... Pierre Boulez, Luigi Nono, Karlheinz Stockhausen |
| 3 | General QA | Should investors time the market? | Timing the market is based on predictions of t... |

##### RLHF Dataset

| Instruction | Chosen Response | Rejected Response |
| --- | --- | --- |
| What is Depreciation | Depreciation is the drop in value of an asset ... | What is Depreciation – 10 Important Facts to K... |
| What do you know about the city of Aberdeen in Scotland? | Aberdeen is a city located in the North East of Scotland. It is known for its granite architecture and its offshore oil industry. | As an AI language model, I don't have personal knowledge or experiences about Aberdeen. |
| Describe thunderstorm season in the United States and Canada. | Thunderstorm season in the United States and Canada typically occurs during the spring and summer months, when warm, moist air collides with cooler, drier air, creating the conditions for thunderstorms to form. | Describe thunderstorm season in the United States and Canada. |

## **Evaluating Large Language Models**

- [Artificial Analysis LLM Performance Leaderboard🤗](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard): Performance benchmarks & pricing across API providers of LLMs
- Awesome LLMs Evaluation Papers: Evaluating Large Language Models: A Comprehensive Survey / [git](https://github.com/tjunlp-lab/Awesome-LLMs-Evaluation-Papers) [Oct 2023] ![**github stars**](https://img.shields.io/github/stars/tjunlp-lab/Awesome-LLMs-Evaluation-Papers?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Can Large Language Models Be an Alternative to Human Evaluations?📑](https://arxiv.org/abs/2305.01937) [3 May 2023]
- [ChatGPT’s One-year Anniversary: Are Open-Source Large Language Models Catching up?📑](https://arxiv.org/abs/2311.16989): Open-Source LLMs vs. ChatGPT; Benchmarks and Performance of LLMs [28 Nov 2023]
- [Docker cagent](https://github.com/docker/cagent): Deterministic, replayable flows: the vcr (vcr.py) pattern records/replays http calls, making LLM and agent tests fast, reliable, and CI-friendly. [Sep 2025] ![**github stars**](https://img.shields.io/github/stars/docker/cagent?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- Evaluation of Large Language Models: [A Survey on Evaluation of Large Language Models📑](https://arxiv.org/abs/2307.03109): [6 Jul 2023]
- [Evaluation Papers for ChatGPT](https://github.com/THU-KEG/EvaluationPapers4ChatGPT) [28 Feb 2023]
 ![**github stars**](https://img.shields.io/github/stars/THU-KEG/EvaluationPapers4ChatGPT?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)](https://eugeneyan.com/writing/llm-evaluators/):💡Key considerations and Use cases when using LLM-evaluators [Aug 2024]
- [LightEval](https://github.com/huggingface/lighteval):🤗 a lightweight LLM evaluation suite that Hugging Face has been using internally [Jan 2024]
 ![**github stars**](https://img.shields.io/github/stars/huggingface/lighteval?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [LLM Model Evals vs LLM Task Evals](https://x.com/aparnadhinak/status/1752763354320404488)
: `Model Evals` are really for people who are building or fine-tuning an LLM. vs The best LLM application builders are using `Task evals`. It's a tool to help builders build. [Feb 2024]
- [LLMPerf Leaderboard](https://github.com/ray-project/llmperf-leaderboard): Evaulation the performance of LLM APIs. [Dec 2023]
 ![**github stars**](https://img.shields.io/github/stars/ray-project/llmperf-leaderboard?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [LLM-as-a-Judge](https://cameronrwolfe.substack.com/i/141159804/practical-takeaways):💡LLM-as-a-Judge offers a quick, cost-effective way to develop models aligned with human preferences and is easy to implement with just a prompt, but should be complemented by human evaluation to address biases.  [Jul 2024]
- [MTEB: Massive Text Embedding Benchmark📑](https://arxiv.org/abs/2210.07316):💡A multilingual, multimodal benchmark and leaderboard for comparing embedding and retrieval models across tasks such as retrieval, reranking, clustering, classification, and semantic textual similarity. / [git](https://github.com/embeddings-benchmark/mteb) [13 Oct 2022]
 ![**github stars**](https://img.shields.io/github/stars/embeddings-benchmark/mteb?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [OCR Arena](https://www.ocrarena.ai/battle): a free playground for testing and evaluating leading foundation VLMs and open source OCR models side-by-side. [Nov 2025]
- [Prometheus: Inducing Fine-grained Evaluation Capability in Language Models📑](https://arxiv.org/abs/2310.08491): We utilize the FEEDBACK COLLECTION, a novel dataset, to train PROMETHEUS, an open-source large language model with 13 billion parameters, designed specifically for evaluation tasks. [12 Oct 2023]
- [The Leaderboard Illusion📑](https://arxiv.org/abs/2504.20879):💡Chatbot Arena's benchmarking is skewed by selective disclosures, private testing advantages, and data access asymmetries, leading to overfitting and unfair model rankings. [29 Apr 2025]
- [Verifiers](https://github.com/PrimeIntellect-ai/verifiers) - Library of reinforcement-learning environments and evaluators. [Jan 2025] ![**github stars**](https://img.shields.io/github/stars/PrimeIntellect-ai/verifiers?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

### **LLM Evaluation Benchmarks**

#### Language Understanding and QA

- [BIG-bench📑](https://arxiv.org/abs/2206.04615): Consists of 204 evaluations, contributed by over 450 authors, that span a range of topics from science to social reasoning. The bottom-up approach; anyone can submit an evaluation task. / [git](https://github.com/google/BIG-bench) [9 Jun 2022]
![**github stars**](https://img.shields.io/github/stars/google/BIG-bench?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [BigBench](https://github.com/google/BIG-bench): 204 tasks. Predicting future potential [Published in 2023]
![**github stars**](https://img.shields.io/github/stars/google/BIG-bench?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [GLUE](https://gluebenchmark.com/leaderboard) & [SuperGLUE](https://super.gluebenchmark.com/leaderboard/):🏆GLUE (General Language Understanding Evaluation)
- [HELM📑](https://arxiv.org/abs/2211.09110):💡Evaluation scenarios like reasoning and disinformation using standardized metrics like accuracy, calibration, robustness, and fairness. The top-down approach; experts curate and decide what tasks to evaluate models on. / [git](https://github.com/stanford-crfm/helm) [16 Nov 2022] ![**github stars**](https://img.shields.io/github/stars/stanford-crfm/helm?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [IFEval: Instruction-Following Evaluation📑](https://arxiv.org/abs/2311.07911): Evaluates instruction adherence with around 500 prompts containing verifiable constraints such as word count, formatting, and required keywords, avoiding LLM-as-judge scoring. / [git](https://github.com/google-research/google-research/tree/master/instruction_following_eval) [14 Nov 2023]
- [MMLU (Massive Multitask Language Understanding)](https://github.com/hendrycks/test):🏆Over 15,000 questions across 57 diverse tasks. [Published in 2021]
![**github stars**](https://img.shields.io/github/stars/hendrycks/test?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [MMLU (Massive Multi-task Language Understanding)📑](https://arxiv.org/abs/2009.03300): LLM performance across 57 tasks including elementary mathematics, US history, computer science, law, and more. [7 Sep 2020]
- [TruthfulQA🤗](https://huggingface.co/datasets/truthful_qa): Truthfulness. [Published in 2022]

#### Coding

- [CodeXGLUE](https://github.com/microsoft/CodeXGLUE): Programming tasks.
![**github stars**](https://img.shields.io/github/stars/microsoft/CodeXGLUE?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [HumanEval](https://github.com/openai/human-eval):🏆Challenges coding skills. [Published in 2021]
![**github stars**](https://img.shields.io/github/stars/openai/human-eval?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [MBPP](https://github.com/google-research/google-research/tree/master/mbpp): Mostly Basic Python Programming. [Published in 2021]
- [SWE-bench](https://www.swebench.com/):🏆Software Engineering Benchmark. Real-world software issues sourced from GitHub. (GPT-5.2: 55.6% Pro, 80% Verified; Gemini 3: 76.2%)
- [SWE-Lancer](https://openai.com/index/swe-lancer/): OpenAI. full engineering stack, from UI/UX to systems design, and include a range of task types, from $50 bug fixes to $32,000 feature implementations. [18 Feb 2025] (GPT-5.2: 74.6% IC Diamond)
- [Vibe Code Bench](https://www.vals.ai/benchmarks/vibe-code): Claude Sonnet 4.5 (Thinking)and GPT 5.1 are head and shoulders above the competition. GPT 5.1 stands out especially for its low cost and high performance.
- [LiveCodeBench Pro](https://huggingface.co/spaces/LiveCodeBench/leaderboard): Algorithmic coding problems. (Gemini 3: Elo 2,439)

#### Chatbot Assistance

- [Chatbot Arena🤗](https://huggingface.co/datasets/lmsys/chatbot_arena_conversations): Human-ranked ELO ranking.
- [MT Bench](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge): Multi-turn open-ended questions
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena📑](https://arxiv.org/abs/2306.05685) [9 Jun 2023]

#### Vision & Multimodal

- [CharXiv Reasoning](https://arxiv.org/abs/2406.18521): Scientific chart reasoning. (GPT-5.2: 88.7% with Python, 82.1% without tools)
- [ScreenSpot-Pro](https://arxiv.org/abs/2504.07981): UI screenshot understanding. (GPT-5.2: 86.3% with Python, 64.2% without tools; Gemini 3: high performance)
- [MMMU-Pro](https://mmmu-benchmark.github.io/): Multimodal reasoning. (GPT-5.2: 80.4% with Python, 79.5% without tools; Gemini 3: 81.0%)
- [Video-MMMU](https://mmmu-benchmark.github.io/): Video understanding. (GPT-5.2: 85.9%; Gemini 3: 87.6%)

#### Long Context

- [BrowseComp](https://openai.com/index/browsecomp/): Long context web browsing (128k, 256k). (GPT-5.2: 92.0% at 128k, 89.8% at 256k; Gemini 3: reference available)
- [OpenAI MRCRv2📑](https://huggingface.co/datasets/openai/mrcr): Multi-round co-reference resolution. (GPT-5.2: 77.0% at 128k-256k tokens; Gemini 3: 77.0% at 128k)
- [RULER📑](https://arxiv.org/abs/2404.06654): Evaluates long-context models beyond simple needle-in-a-haystack recall, covering multi-needle retrieval, multi-hop tracing, aggregation, and question answering at configurable sequence lengths. / [git](https://github.com/NVIDIA/RULER) [9 Apr 2024]
 ![**github stars**](https://img.shields.io/github/stars/NVIDIA/RULER?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

#### Tool Calling & Agentic

- [AgentDojo📑](https://arxiv.org/abs/2406.13352): Extensible environment for measuring prompt-injection attacks and defenses in tool-using agents across realistic workspace, travel, and banking tasks. / [git](https://github.com/ethz-spylab/agentdojo) [19 Jun 2024]
 ![**github stars**](https://img.shields.io/github/stars/ethz-spylab/agentdojo?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [GAIA: A Benchmark for General AI Assistants📑](https://arxiv.org/abs/2311.12983): 466 real-world questions requiring reasoning, multimodality, web browsing, and tool use; designed to be simple for people but challenging for AI assistants. [21 Nov 2023]
- [LiveCodeBench Pro](https://huggingface.co/spaces/LiveCodeBench/leaderboard): Algorithmic coding problems. (Gemini 3: Elo 2,439)
- [OSWorld📑](https://arxiv.org/abs/2404.07972):💡Benchmark for multimodal agents completing open-ended tasks in real Ubuntu, Windows, and macOS environments, with execution-based evaluation. / [git](https://github.com/xlang-ai/OSWorld) [11 Apr 2024]
 ![**github stars**](https://img.shields.io/github/stars/xlang-ai/OSWorld?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Tau2-bench📑](https://arxiv.org/pdf/2506.07982): Multi-turn tool usage in customer support. (GPT-5.2: 98.7% Telecom, 82.0% Retail)
- [Vending-Bench 2](https://www.vellum.ai/blog/google-gemini-3-benchmarks): Year-long business simulation. (Gemini 3: $5,478.16 mean net worth, 272% higher than GPT-5.1)
- [WebArena📑](https://arxiv.org/abs/2307.13854):💡A self-hostable, realistic web environment with long-horizon tasks across e-commerce, social discussion, software development, and content management sites. / [git](https://github.com/web-arena-x/webarena) [25 Jul 2023]
 ![**github stars**](https://img.shields.io/github/stars/web-arena-x/webarena?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

#### Reasoning

- [ARC (AI2 Reasoning Challenge)](https://github.com/fchollet/ARC): Measures general fluid intelligence. (GPT-5.2: 86.2% ARC-AGI-1, 52.9% ARC-AGI-2; Gemini 3: 31.1% ARC-AGI-2, 45.1% with Deep Think)
![**github stars**](https://img.shields.io/github/stars/fchollet/ARC?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [DROP🤗](https://huggingface.co/datasets/drop): Evaluates discrete reasoning.
- [HellaSwag](https://github.com/rowanz/hellaswag): Commonsense reasoning. [Published in 2019]
![**github stars**](https://img.shields.io/github/stars/rowanz/hellaswag?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [LogicQA](https://github.com/lgw863/LogiQA-dataset): Evaluates logical reasoning skills.
![**github stars**](https://img.shields.io/github/stars/lgw863/LogiQA-dataset?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [GPQA Diamond](https://arxiv.org/abs/2311.12022): PhD-level scientific knowledge. (GPT-5.2: 92.4%; Gemini 3: 91.9%, 93.8% with Deep Think)
- [Humanity's Last Exam](https://huggingface.co/spaces/allenai/WildBench): Hardest reasoning benchmark. (GPT-5.2: 45.5% with search/Python; Gemini 3: 37.5%, 40%+ with Deep Think)

#### Translation

- [WMT🤗](https://huggingface.co/wmt): Evaluates translation skills.

#### Math

- [GSM8K](https://github.com/openai/grade-school-math): Arithmetic Reasoning. [Published in 2021]
![**github stars**](https://img.shields.io/github/stars/openai/grade-school-math?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [MATH](https://github.com/hendrycks/math): Tests ability to solve math problems. [Published in 2021]
![**github stars**](https://img.shields.io/github/stars/hendrycks/math?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [AIME 2025](https://www.maa.org/): Competition math benchmark. (GPT-5.2: 100%; Gemini 3: 100% with code, 95% without tools)
- [FrontierMath](https://epoch.ai/frontiermath): Expert-level mathematics. (GPT-5.2: 40.3% Tier 1-3, 14.6% Tier 4; Gemini 3: >20x improvement on MathArena Apex)
- [HMMT](https://www.hmmt.org/): High school math tournament. (GPT-5.2: 99.4% Feb 2025)

 #### Other Benchmarks

- [Alpha Arena](https://nof1.ai/): a benchmark designed to measure AI's investing abilities. [Oct 2025]
- [Comprehensive and Practical Evaluation of Retrieval-Augmented Generation Systems for Medical Question Answering📑](https://arxiv.org/abs/2411.09213) [14 Nov 2024]
- [Korean SAT LLM Leaderboard](https://github.com/Marker-Inc-Korea/Korean-SAT-LLM-Leaderboard): Benchmarking 10 years of Korean CSAT (College Scholastic Ability Test) exams [Oct 2024]
![**github stars**](https://img.shields.io/github/stars/Marker-Inc-Korea/Korean-SAT-LLM-Leaderboard?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [OpenAI BrowseComp](https://openai.com/index/browsecomp/): A benchmark assessing AI agents’ ability to use web browsing tools to complete tasks requiring up-to-date information, reasoning, and navigation skills. Boost from tools + reasoning. Human trainer success ratio = 29.2% × 86.4% ≈ 25.2% [10 Apr 2025]
- [OpenAI GDPval](https://openai.com/index/gdpval/): OpenAI's benchmark evaluating AI performance on real-world tasks across 44 occupations [25 Sep 2025]
- [OpenAI MLE-bench📑](https://arxiv.org/abs/2410.07095): A benchmark for measuring the performance of AI agents on ML tasks using Kaggle. / [git](https://github.com/openai/mle-bench) [9 Oct 2024] > Agent Framework used in MLE-bench, `GPT-4o (AIDE) achieves more medals on average than both MLAB and OpenHands (8.7% vs. 0.8% and 4.4% respectively)` 
![**github stars**](https://img.shields.io/github/stars/openai/mle-bench?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [OpenAI Paper Bench](https://openai.com/index/paperbench/): a benchmark evaluating the ability of AI agents to replicate state-of-the-art AI research. / [git](https://github.com/openai/preparedness/tree/main/project/paperbench) [2 Apr 2025]
- [OpenAI SimpleQA Benchmark](https://openai.com/index/introducing-simpleqa/): SimpleQA, a factuality benchmark for short fact-seeking queries, narrows its scope to simplify factuality measurement. / [git](https://github.com/openai/simple-evals) [30 Oct 2024] ![**github stars**](https://img.shields.io/github/stars/openai/simple-evals?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Social Sycophancy: A Broader Understanding of LLM Sycophancy📑](https://arxiv.org/abs/2505.13995): ELEPHANT; LLM Benchmark to assess LLM Sycophancy. Dataset (query): OEQ (Open-Ended Questions) and Reddit. LLMs (prompted as judges) to assess the presence of sycophancy in outputs with prompt [20 May 2025]

### **Evaluation Metrics**

- [Evaluating LLMs and RAG Systems](https://dzone.com/articles/evaluating-llms-and-rag-systems) (Jan 2025)
- Automated evaluation
  > - **n-gram metrics**: ROUGE, BLEU, METEOR → compare overlap with reference text.
  > - *ROUGE*: multiple variants (N, L, W, S, SU) based on n-gram, LCS, skip-bigrams.
  > - *BLEU*: 0–1 score for translation quality.
  > - *METEOR*: precision + recall + semantic similarity.
  > - **Probabilistic metrics**: *Perplexity* → lower is better predictive performance.
  > - **Embedding metrics**: Ada Similarity, BERTScore → semantic similarity using embeddings.
- Human evaluation
  > - Measures **relevance, fluency, coherence, groundedness**.
  > - Automated with LLM-based evaluators.
- Built-in methods
  > - Prompt flow evaluation methods: [Prompt Flow Evaluation Metrics](https://qiita.com/nohanaga/items/b68bf5a65142c5af7969) [Aug 2023] / [Submit a Batch Run to Evaluate a Prompt Flow](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/how-to-bulk-test-evaluate-flow)

## **LLMOps: Large Language Model Operations**

- [Agent QA](https://github.com/vostride/agent-qa): The self-improving QA agent for software teams, with natural-language web/mobile regression tests and persistent test memory. [May 2026] ![**github stars**](https://img.shields.io/github/stars/vostride/agent-qa?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Agent Trace](https://agent-trace.dev/): Data spec for recording AI agent attribution, reasoning steps, and tool calls.
- [agenta](https://github.com/Agenta-AI/agenta): OSS LLMOps workflow: building (LLM playground, evaluation), deploying (prompt and configuration management), and monitoring (LLM observability and tracing). [Jun 2023] ![**github stars**](https://img.shields.io/github/stars/Agenta-AI/agenta?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Azure ML Prompt flow](https://microsoft.github.io/promptflow/index.html): A set of LLMOps tools designed to facilitate the creation of LLM-based AI applications [Sep 2023] > [How to Evaluate & Upgrade Model Versions in the Azure OpenAI Service](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/how-to-evaluate-amp-upgrade-model-versions-in-the-azure-openai/ba-p/4218880) [14 Aug 2024]
- Azure Machine Learning studio Model Data Collector: Collect production data, analyze key safety and quality evaluation metrics on a recurring basis, receive timely alerts about critical issues, and visualize the results. [How to collect production data](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-collect-production-data?view=azureml-api-2&tabs=azure-cli) [Apr 2024]
- [circuit‑tracer](https://github.com/safety-research/circuit-tracer): Anthrophic. Tool for finding and visualizing circuits within large language models. a circuit is a minimal, causal computation pathway inside a transformer model that shows how internal features lead to a specific output. [May 2025] ![**github stars**](https://img.shields.io/github/stars/safety-research/circuit-tracer?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [DeepEval](https://github.com/confident-ai/deepeval): LLM evaluation framework. similar to Pytest but specialized for unit testing LLM outputs. [Aug 2023]
 ![**github stars**](https://img.shields.io/github/stars/confident-ai/deepeval?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [DeepTeam](https://github.com/confident-ai/deepteam): A LLM Red Teaming Framework. [Mar 2025] ![**github stars**](https://img.shields.io/github/stars/confident-ai/deepteam?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Giskard](https://github.com/Giskard-AI/giskard): The testing framework for ML models, from tabular to LLMs [Mar 2022] ![**github stars**](https://img.shields.io/github/stars/Giskard-AI/giskard?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [GenOps Framework](https://github.com/neerazz/genops-framework): MIT-licensed generative-operations framework for governing GenAI deployments across lifecycle, risk controls, and operating model; published in JISEM 2026 (DOI: 10.52783/jisem.v11i1s.14322). [2026] ![**github stars**](https://img.shields.io/github/stars/neerazz/genops-framework?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai):💡The UK AI Security Institute's framework for evaluating LLMs, with support for tool use, multi-turn dialogue, model-graded scoring, and reusable evaluation components. [2024] ![**github stars**](https://img.shields.io/github/stars/UKGovernmentBEIS/inspect_ai?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals): Community-maintained catalog of evaluations runnable with Inspect AI, spanning coding, agents, safeguards, cybersecurity, reasoning, and multimodal tasks. [2024] ![**github stars**](https://img.shields.io/github/stars/UKGovernmentBEIS/inspect_evals?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Langfuse](https://langfuse.com):🏆/ [git](https://github.com/langfuse/langfuse) LLMOps platform that helps teams to collaboratively monitor, evaluate and debug AI applications. [May 2023] 
 ![**github stars**](https://img.shields.io/github/stars/langfuse/langfuse?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness):💡Over 60 standard academic benchmarks for LLMs. A framework for few-shot evaluation. Hugginface uses this for [Open LLM Leaderboard🤗](https://huggingface.co/open-llm-leaderboard) [Aug 2020]
 ![**github stars**](https://img.shields.io/github/stars/EleutherAI/lm-evaluation-harness?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [LangWatch scenario](https://github.com/langwatch/scenario):💡LangWatch Agentic testing for agentic codebases. Simulating agentic communication using autopilot [Apr 2025] ![**github stars**](https://img.shields.io/github/stars/langwatch/scenario?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [LLMOps Database](https://www.zenml.io/llmops-database): A curated knowledge base of real-world LLMOps implementations.
- [Maxim AI](https://getmaxim.ai): / [git](https://github.com/maximhq) End-to-end simulation, evaluation, and observability plaform, helping teams ship their AI agents reliably and >5x faster. [Dec 2023]
- [Machine Learning Operations (MLOps) For Beginners](https://towardsdatascience.com/machine-learning-operations-mlops-for-beginners-a5686bfe02b2): DVC (Data Version Control), MLflow, Evidently AI (Monitor a model). Insurance Cross Sell Prediction / [git](https://github.com/prsdm/mlops-project) [29 Aug 2024]
 ![**github stars**](https://img.shields.io/github/stars/prsdm/mlops-project?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Netdata](https://github.com/netdata/netdata): AI-powered real-time infrastructure monitoring platform [Jun 2013] ![**github stars**](https://img.shields.io/github/stars/netdata/netdata?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [OpenAI Evals](https://github.com/openai/evals):💡A framework for evaluating large language models (LLMs) [Mar 2023]
 ![**github stars**](https://img.shields.io/github/stars/openai/evals?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Opik](https://github.com/comet-ml/opik): an open-source platform for evaluating, testing and monitoring LLM applications. Built by Comet. [2 Sep 2024] ![**github stars**](https://img.shields.io/github/stars/comet-ml/opik?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Pezzo](https://github.com/pezzolabs/pezzo): Open-source, developer-first LLMOps platform [May 2023]
 ![**github stars**](https://img.shields.io/github/stars/pezzolabs/pezzo?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [phoenix](https://github.com/Arize-ai/phoenix): AI Observability & Evaluation [Nov 2022] ![**github stars**](https://img.shields.io/github/stars/Arize-ai/phoenix?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [promptfoo](https://github.com/promptfoo/promptfoo):💡Test your prompts. Evaluate and compare LLM outputs, catch regressions, and improve prompt quality. [Apr 2023]
 ![**github stars**](https://img.shields.io/github/stars/promptfoo/promptfoo?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [PromptTools](https://github.com/hegelai/prompttools/): Open-source tools for prompt testing [Jun 2023] ![**github stars**](https://img.shields.io/github/stars/hegelai/prompttools?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Ragas](https://github.com/explodinggradients/ragas):🏆Evaluation framework for your Retrieval Augmented Generation (RAG) [May 2023]
 ![**github stars**](https://img.shields.io/github/stars/explodinggradients/ragas?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [traceloop openllmetry](https://github.com/traceloop/openllmetry): Quality monitoring for your LLM applications. [Sep 2023]
 ![**github stars**](https://img.shields.io/github/stars/traceloop/openllmetry?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [TruLens](https://github.com/truera/trulens): Instrumentation and evaluation tools for large language model (LLM) based applications. [Nov 2020]
 ![**github stars**](https://img.shields.io/github/stars/truera/trulens?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

### **Challenges in evaluating AI systems**

- [30 requirements for an MLOps environment](https://x.com/KirkDBorne/status/1679952405805555713): Kirk Borne twitter [15 Jul 2023]
- [Challenges in evaluating AI systems](https://www.anthropic.com/index/evaluating-ai-systems): The challenges and limitations of various methods for evaluating AI systems, such as multiple-choice tests, human evaluations, red teaming, model-generated evaluations, and third-party audits. [4 Oct 2023]
- [Economics of Hosting Open Source LLMs](https://towardsdatascience.com/economics-of-hosting-open-source-llms-17b4ec4e7691): Comparison of cloud vendors such as AWS, Modal, BentoML, Replicate, Hugging Face Endpoints, and Beam, using metrics like processing time, cold start latency, and costs associated with CPU, memory, and GPU usage. / [git](https://github.com/ilsilfverskiold/Awesome-LLM-Resources-List) [13 Nov 2024]
- [Pretraining on the Test Set Is All You Need📑](https://arxiv.org/abs/2309.08632): On that note, in the satirical Pretraining on the Test Set Is All You Need paper, the author trains a small 1M parameter LLM that outperforms all other models, including the 1.3B phi-1.5 model. This is achieved by training the model on all downstream academic benchmarks. It appears to be a subtle criticism underlining how easily benchmarks can be "cheated" intentionally or unintentionally (due to data contamination). [13 Sep 2023]
- [Sakana AI claimed 100x faster AI training, but a bug caused a 3x slowdown](https://techcrunch.com/2025/02/21/sakana-walks-back-claims-that-its-ai-can-dramatically-speed-up-model-training/): Sakana’s AI resulted in a 3x slowdown — not a speedup. [21 Feb 2025]
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) [29 Mar 2024] / [How to Evaluate LLM Applications: The Complete Guide](https://www.confident-ai.com/blog/how-to-evaluate-llm-applications) [7 Nov 2023]

## **LLM for Robotics**

- PromptCraft-Robotics: Robotics and a robot simulator with ChatGPT integration / [git](https://github.com/microsoft/PromptCraft-Robotics) [Feb 2023]
 ![**github stars**](https://img.shields.io/github/stars/microsoft/PromptCraft-Robotics?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- ChatGPT-Robot-Manipulation-Prompts: A set of prompts for Communication between humans and robots for executing tasks. / [git](https://github.com/microsoft/ChatGPT-Robot-Manipulation-Prompts) [Apr 2023]
 ![**github stars**](https://img.shields.io/github/stars/microsoft/ChatGPT-Robot-Manipulation-Prompts?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Siemens Industrial Copilot](https://news.microsoft.com/2023/10/31/siemens-and-microsoft-partner-to-drive-cross-industry-ai-adoption/)  [31 Oct 2023]
- [LeRobot🤗](https://huggingface.co/lerobot): Hugging Face. LeRobot aims to provide models, datasets, and tools for real-world robotics in PyTorch. / [git](https://github.com/huggingface/lerobot) [Jan 2024]
 ![**github stars**](https://img.shields.io/github/stars/huggingface/lerobot?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
- [Mobile ALOHA](https://mobile-aloha.github.io/): Stanford’s mobile ALOHA robot learns from humans to cook, clean, do laundry. Mobile ALOHA extends the original ALOHA system by mounting it on a wheeled base [4 Jan 2024] / [ALOHA](https://www.trossenrobotics.com/aloha.aspx): A Low-cost Open-source Hardware System for Bimanual Teleoperation.
- [Figure 01 + OpenAI](https://www.figure.ai/): Humanoid Robots Powered by OpenAI ChatGPT [📺](https://youtu.be/Sq1QZB5baNw?si=wyufZA1xtTYRfLf3) [Mar 2024]
- [Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/): Robotics built on the foundation of Gemini 2.0 [12 Mar 2025]
- [Gemini Robotics 2](https://deepmind.google/models/gemini-robotics/): Vision-language-action model for controlling robot embodiments, with companion embodied-reasoning and on-device models. [2026]
- [WorldClaw](https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw): Agentic 3D open-world generation system. [Aug 2026] ![**github stars**](https://img.shields.io/github/stars/Tencent-Hunyuan/Hunyuan3D-WorldClaw?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)

## **Awesome demo**

- [FRVR Official Teaser📺](https://youtu.be/Yjjpr-eAkqw): Prompt to Game: AI-powered end-to-end game creation [16 Jun 2023]
- [rewind.ai](https://www.rewind.ai/): Rewind captures everything you’ve seen on your Mac and iPhone [Nov 2023]
- [Vercel announced V0.dev](https://v0.dev/chat/AjJVzgx): Make a snake game with chat [Oct 2023]
- [Mobile ALOHA📺](https://youtu.be/HaaZ8ss-HP4?si=iMYKzvx8wQhf39yU): A day of Mobile ALOHA [4 Jan 2024]
- [groq](https://github.com/groq): An LPU Inference Engine, the LPU is reported to be 10 times faster than NVIDIA’s GPU performance [500 Tokens Per Second Shatters Record, Self-Developed LPU Outperforms NVIDIA GPU by 10 Times](https://www.gamingdeputy.com/groq-unveils-worlds-fastest-large-model-500-tokens-per-second-shatters-record-self-developed-lpu-outperforms-nvidia-gpu-by-10-times/) [Jan 2024]
- [Sora📺](https://youtu.be/HK6y8DAPN_0?si=FPZaGk4fP2d456QP): Introducing Sora — OpenAI’s text-to-video model [Feb 2024]
- [Oasis](https://www.etched.com/blog-posts/oasis): Minecraft clone. Generated by AI in Real-Time. The first playable AI model that generates open-world games. [Oasis model.github.io](https://oasis-model.github.io/) / [git](https://github.com/etched-ai/open-oasis) [31 Oct 2024] ![**github stars**](https://img.shields.io/github/stars/etched-ai/open-oasis?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000)
