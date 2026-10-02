# Azure OpenAI + LLM

![GitHub last commit](https://img.shields.io/github/last-commit/kimtth/awesome-azure-openai-llm?label=commit&color=hotpink&style=flat-square)
![Azure OpenAI](https://img.shields.io/badge/llm-azure_openai-blue?style=flat-square)
![GitHub Created At](https://img.shields.io/github/created-at/kimtth/awesome-azure-openai-llm?style=flat-square)

A comprehensive, curated collection of resources for Azure OpenAI, Large Language Models (LLMs), and their applications.

🔹Concise Summaries: Each resource is briefly described for quick understanding  
🔹Chronological Organization: Resources appended with date (first commit, publication, or paper release)  
🔹Monthly Updates: The list is updated monthly; candidate entries before the update are tracked in the issue.  

<!-- > [!TIP]
> A refined list focusing on Azure and Microsoft products.  
> Check [**_Awesome Azure OpenAI & Copilot_**](https://github.com/kimtth/awesome-azure-openai-copilot).   --> 

## 🧭 Quick Navigation (Propedia-style)

| Layer / Era | What it controls | Jump to sections |
|-------------|----------------------------------------|-------------|
| **Weights** <br/> 2022-2023 | Capabilities encoded in model parameters. <br/> `Themes: Pretraining, scaling, fine-tuning, alignment` | [Model landscape](section/models_research.md#large-language-model-landscape) · [Model collection](section/models_research.md#large-language-model-collection) · [Training & optimization](section/models_research.md#large-language-model-training-and-optimization) · [Model training](section/azure.md#model-training--inference) |
| **Context** <br/> 2023-2024 | Instructions and knowledge supplied at inference. <br/> `Themes: Prompting, RAG, memory, long context` | [Prompting](section/models_research.md#prompt-engineering-and-visual-prompts) · [RAG](section/applications.md#rag-retrieval-augmented-generation) · [Azure AI Search](section/azure.md#azure-ai-search) · [Memory](section/applications.md#memory) · [Long-context limits](section/models_research.md#context-and-long-context-limits) |
| **Agentic Engineering** <br/> 2025-2026 | How applications use models and tools to act. <br/> `Themes: Agents, MCP, skills, orchestration, evaluation` | [Agent frameworks](section/azure.md#agent-frameworks) · [Agent protocols](section/applications.md#agent-protocol) · [Agentic engineering](section/applications.md#agentic-engineering) · [Agent best practices](section/best_practices.md#agent-best-practices) · [Evaluation](section/tools_extra.md#evaluating-large-language-models) |

Refereces: [DailyDoseOfDS - *Evolution of the Agent Landscape*](https://blog.dailydoseofds.com/p/evolution-of-agent-landscape-from)

## 1. App & Agent
🚀 [RAG Systems, LLM Applications, Agents, Frameworks & Orchestration](section/applications.md)

- **RAG**
  - [RAG](section/applications.md#rag-retrieval-augmented-generation)
  - [GraphRAG](section/applications.md#graphrag)
  - [RAG Application](section/applications.md#rag-application)
  - [Vector Database & Embedding](section/applications.md#vector-database--embedding)
- **Application**
  - [Top Agent Frameworks](section/applications.md#top-agent-frameworks)
  - [Additional Agent Framework](section/applications.md#additional-agent-framework)
  - [Cache](section/applications.md#cache)
  - [Data & Analytics Agents](section/applications.md#data--analytics-agents)
  - [Data Processing & OCR](section/applications.md#data-processing--ocr)
  - [Desktop AI Assistant](section/applications.md#desktop-ai-assistant)
  - [Memory](section/applications.md#memory)
  - [Model Gateway](section/applications.md#model-gateway)
  - [Model Serving & Local Runtimes](section/applications.md#model-serving--local-runtimes)
  - [Observability & LLMOps](section/applications.md#observability--llmops)
  - [**Popular LLM Applications** (GitHub Stars >= 1000)](section/x_llm_apps.md)
  - [SDKs, Integration & ML Libraries](section/applications.md#sdks-integration--ml-libraries)
  - [Training & Fine-tuning](section/applications.md#training--fine-tuning)
  - [UI & No-Code Tool](section/applications.md#ui--no-code-tool)
- **Agent Protocols**
  - [A2A](section/applications.md#a2a)
  - [Computer use](section/applications.md#computer-use)
  - [Model Context Protocol (MCP)](section/applications.md#model-context-protocol-mcp)
- **Coding & Research**
  - [Coding](section/applications.md#coding)
  - [Deep Research](section/applications.md#deep-research)
  - [Domain-Specific Agents](section/applications.md#domain-specific-agents)
  - [Skills](section/applications.md#skills)
  - [Agentic Engineering](section/applications.md#agentic-engineering): Harness Engineering → Loop Engineering → Graph Engineering

**[⬆ back to top](#azure-openai--llm-wiki)**

## 2. Azure OpenAI & Copilot
🌌 [Microsoft's Cloud-Based AI Platform and Services](section/azure.md)

- **Overview**
  - [Azure OpenAI & Foundry Overview](section/azure.md#azure-openai--foundry-overview)
- **Frameworks**
  - [Orchestration Frameworks](section/azure.md#orchestration-frameworks)
  - [Agent Frameworks](section/azure.md#agent-frameworks)
- **Tooling**
  - [Prompt Engineering & Tooling](section/azure.md#prompt-engineering--tooling)
  - [Dev Tools, MCP & Extensions](section/azure.md#dev-tools-mcp--extensions)
- **Products**
  - [Copilot Product Catalog](section/azure.md#copilot-product-catalog)
  - [Agent Development](section/azure.md#agent-development)
  - [Microsoft 365 Agent Development](section/azure.md#microsoft-365-agent-development)
- **Services**
  - [Azure AI Search](section/azure.md#azure-ai-search)
  - [Microsoft Foundry & AI Services](section/azure.md#microsoft-foundry--ai-services)
- **Research**
  - [Microsoft Research](section/azure.md#microsoft-research)
- **Applications**
  - [Sample Applications](section/azure.md#sample-applications)
  - [Solution Accelerators](section/azure.md#solution-accelerators)
  - [Architecture Patterns & Use Cases](section/azure.md#architecture-patterns--use-cases)

**[⬆ back to top](#azure-openai--llm-wiki)**

## 3. Research & Survey
🧠 [LLM Landscape, Prompt Engineering, Finetuning, Challenges & Surveys](section/models_research.md)

- **Landscape**
  - [Large Language Model Landscape](section/models_research.md#large-language-model-landscape)
  - [Large Language Model Collection](section/models_research.md#large-language-model-collection)
  - [Foundation Model Providers](section/models_research.md#foundation-model-providers)
  - [Domain-Specific and Specialized LLMs](section/models_research.md#domain-specific-and-specialized-llms)
- **Prompting**
  - [Prompt Engineering and Visual Prompts](section/models_research.md#prompt-engineering-and-visual-prompts)
- **Training & Optimization**
  - [Large Language Model Training and Optimization](section/models_research.md#large-language-model-training-and-optimization)
  - [Pre-training and Data Preparation](section/models_research.md#pre-training-and-data-preparation)
  - [Architecture and Inference Patterns](section/models_research.md#architecture-and-inference-patterns)
  - [Post-training and Fine-Tuning](section/models_research.md#post-training-and-fine-tuning)
- **Impact & Products**
  - [AI Adoption, Impact, and Society](section/models_research.md#ai-adoption-impact-and-society)
  - [OpenAI Products](section/models_research.md#openai-products)
  - [Anthropic AI Products](section/models_research.md#anthropic-ai-products)
  - [Google AI Products](section/models_research.md#google-ai-products)
- **Survey & Reference**
  - [Survey and Reference](section/models_research.md#survey-and-reference)
  - [Additional Topics: A Survey of LLMs](section/models_research.md#additional-topics-a-survey-of-llms)
  - [**LLM Research** (Ranked by cite count ≥150)](section/x_llm_papers.md)
  - [Learning Resources, Implementations, and Regional Materials](section/models_research.md#learning-resources-implementations-and-regional-materials)

**[⬆ back to top](#azure-openai--llm-wiki)**

## 4. Datasets, Evaluation, and Extras
🛠️ [Training Data, Datasets & Evaluation Methods](section/tools_extra.md)

- **Data**
  - [Datasets for LLM Training](section/tools_extra.md#datasets-for-llm-training)
- **Evaluation**
  - [Evaluating Large Language Models](section/tools_extra.md#evaluating-large-language-models)
  - [LLM Evaluation Benchmarks](section/tools_extra.md#llm-evaluation-benchmarks)
  - [LLMOps: Large Language Model Operations](section/tools_extra.md#llmops-large-language-model-operations)
- **Extras**
  - [LLM for Robotics](section/tools_extra.md#llm-for-robotics)
  - [Awesome Demo](section/tools_extra.md#awesome-demo)

**[⬆ back to top](#azure-openai--llm-wiki)**

## 5. Best Practices
📋 [Curated Blogs, Patterns, and Implementation Guidelines](section/best_practices.md)

- **RAG**
  - [The Problem with RAG](section/best_practices.md#the-problem-with-rag)
  - [RAG Solution Design](section/best_practices.md#rag-solution-design)
  - [RAG Research](section/best_practices.md#rag-research)
  - [**RAG Research** (Ranked by cite count >=100)](section/best_practices.md#rag-research-ranked-by-cite-count-100)
- **Agent**
  - [Agent Design Patterns](section/best_practices.md#agent-design-patterns)
  - [Agent Research](section/best_practices.md#agent-research)
  - [**Agent Research** (Ranked by cite count >=100)](section/best_practices.md#agent-research-ranked-by-cite-count-100)
  - [Tool Use: LLM to Master APIs](section/best_practices.md#tool-use)
- **Security**
  - [Security and Governance](section/best_practices.md#security-and-governance)
- **Reference**
  - [Proposals & Glossary](section/best_practices.md#proposals--glossary)

**[⬆ back to top](#azure-openai--llm-wiki)**

## 🧭 Start Here: Choose a Goal

Pick the outcome closest to your task and follow the links in order. Each path is a short starting point, not a required sequence.

| Goal | Suggested path |
|------|----------------|
| **Build a RAG application** | [RAG](section/applications.md#rag-retrieval-augmented-generation) → [Azure AI Search](section/azure.md#azure-ai-search) → [RAG Solution Design](section/best_practices.md#rag-solution-design) → [RAG Application](section/applications.md#rag-application) |
| **Design an AI agent** | [Top Agent Frameworks](section/applications.md#top-agent-frameworks) → [Agent Design Patterns](section/best_practices.md#agent-design-patterns) → [Agent Development](section/azure.md#agent-development) → [Memory](section/applications.md#memory) |
| **Connect tools with MCP** | [Model Context Protocol](section/applications.md#model-context-protocol-mcp) → [Dev Tools, MCP & Extensions](section/azure.md#dev-tools-mcp--extensions) → [Tool Use](section/best_practices.md#tool-use) |
| **Build a Microsoft 365 agent** | [Microsoft 365 Agent Development](section/azure.md#microsoft-365-agent-development) → [Copilot Product Catalog](section/azure.md#copilot-product-catalog) → [Agent Development](section/azure.md#agent-development) |
| **Build a coding or research agent** | [Coding](section/applications.md#coding) → [Skills](section/applications.md#skills) → [Agentic Engineering](section/applications.md#agentic-engineering) → [Deep Research](section/applications.md#deep-research) |
| **Run a local model application** | [Model Collection](section/models_research.md#large-language-model-collection) → [Model Serving & Local Runtimes](section/applications.md#model-serving--local-runtimes) → [Model Gateway](section/applications.md#model-gateway) → [Observability & LLMOps](section/applications.md#observability--llmops) |
| **Train or evaluate a model** | [Datasets for LLM Training](section/tools_extra.md#datasets-for-llm-training) → [Training & Fine-tuning](section/applications.md#training--fine-tuning) → [Evaluating Large Language Models](section/tools_extra.md#evaluating-large-language-models) → [Evaluation Metrics](section/tools_extra.md#evaluation-metrics) |
| **Operate an application in production** | [Architecture Patterns & Use Cases](section/azure.md#architecture-patterns--use-cases) → [Safety, Security & LLMOps](section/azure.md#safety-security--llmops) → [LLMOps](section/tools_extra.md#llmops-large-language-model-operations) → [Evaluation](section/tools_extra.md#evaluating-large-language-models) |
| **Explore LLM research** | [Model Landscape](section/models_research.md#large-language-model-landscape) → [Survey and Reference](section/models_research.md#survey-and-reference) → [LLM Research](section/models_research.md#llm-research-ranked-by-cite-count-150) |

## 📖 Legend & Notation

| Symbol | Meaning | Symbol | Meaning |
|--------|---------|--------|---------|
| ![**github**](https://img.shields.io/github/stars/kimtth/awesome-azure-openai-llm?style=flat&label=%20&color=f0f1f2&cacheSeconds=360000) | GitHub repository | 🗄️ | Archived files |
| 💡🏆 | Recommend | 📺 | Video content |
| 📑 |  Academic paper | 🤗 | Huggingface |

> **Info:** Applications that have been archived or have had no commits for more than 12 months are listed in [applications.old.md](section/applications.old.md). Archived Azure-related repositories are listed in [azure.old.md](section/azure.old.md).

<!-- 
All rights reserved © `kimtth` 
-->
<!-- 
https://shields.io/badges/git-hub-created-at
-->

**[`^        back to top        ^`](#azure-openai--llm-wiki)**
