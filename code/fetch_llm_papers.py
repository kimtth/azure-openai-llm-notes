"""Fetch high-citation papers covering the LLM landscape and derived technologies from Semantic Scholar.

Captures survey, research, and position papers across all major LLM topic areas derived
from the curated hint list in the awesome-azure-openai-llm knowledge base.
Only Computer Science papers with >= --min-citations citations are included.
Discovery for LLM Architecture Innovations also resolves the original
Transformer paper by its stable arXiv ID, even if a keyword search misses it.

Usage:
    python code/fetch_llm_papers.py
    python code/fetch_llm_papers.py --min-citations 200 --top-n 20
    python code/fetch_llm_papers.py --output files/llm_papers.md
    python code/fetch_llm_papers.py --topics "Reasoning" "Agents"
    python code/fetch_llm_papers.py --discover-popular

Monthly updates cache successful API responses in .cache/semantic-scholar.
Use --refresh-existing for citation-only updates; repeat the same command to
resume outstanding IDs, even if citation changes reorder the Markdown entries.
The cache expires each UTC calendar month. Run the two paper scripts sequentially;
their shared cache also coordinates request pacing and rate-limit cooldowns.
--discover-popular merges the existing popular-paper list and citation-ranked
searches into the landscape without removing existing papers. It saves progress
after each query; rerun it to resume cached successes if an API request fails.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import random
import re
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

import requests
from utils.http_utils import create_session
from utils.path_utils import get_repo_root
from utils.semantic_scholar import SemanticScholarSession

# ---------------------------------------------------------------------------
# Topic → query mapping
# Each entry maps a section name to a list of Semantic Scholar search queries.
# Queries intentionally omit "survey" to capture ALL high-citation papers
# (research contributions, position papers, benchmarks, overviews) in each area.
# ---------------------------------------------------------------------------
TOPICS: dict[str, list[str]] = {
    "Reasoning in LLMs": [
        "advancing reasoning large language models methods approaches",
        "chain-of-thought reasoning LLM prompting",
        "agentic reasoning large language models",
        "thinking machines LLM reasoning strategies",
        "efficient reasoning large language models",
        "stop overthinking efficient reasoning LLM",
        "harnessing reasoning economy efficient LLM",
        "mathematical reasoning large language models benchmark",
        "tree of thoughts deliberate problem solving LLM",
        "reinforcement learning verifiable rewards reasoning LLM",
        "DeepSeek-R1 incentivizing reasoning reinforcement learning",
        "process reward model mathematical reasoning step-by-step",
        "test-time compute scaling reasoning language model",
        "logical reasoning commonsense large language models",
    ],
    "LLM Agents": [
        "LLM-based autonomous agents",
        "large language model based agents",
        "AI agents large language models",
        "agent AI towards holistic intelligence position paper",
        "evaluation LLM-based agents benchmark",
        "AI agent protocols communication",
        "LLM agent communication protocols security countermeasures",
        "rise potential large language model based agents",
        "autonomous agents language model planning tool use",
    ],
    "Retrieval-Augmented Generation (RAG)": [
        "retrieval-augmented generation large language models",
        "agentic retrieval-augmented generation RAG",
        "retrieval augmented text generation LLM",
        "retrieval structuring augmented generation LLM",
        "dense passage retrieval open-domain question answering",
        "self-RAG retrieval augmented generation reflection",
        "corrective retrieval augmented generation CRAG",
        "hypothetical document embeddings HyDE retrieval",
    ],
    "GUI Agents": [
        "GUI agents large language models",
        "large language model brained GUI agents",
        "web agent GUI automation LLM",
    ],
    "Hallucination in LLMs": [
        "hallucination large language models taxonomy",
        "mitigating hallucination large language models techniques",
        "hallucination natural language generation",
        "factuality large language models overview",
        "sycophancy LLM faithfulness factual accuracy",
    ],
    "Prompt Engineering & In-Context Learning": [
        "prompt engineering large language models NLP tasks",
        "automatic prompt optimization techniques LLM",
        "in-context learning large language models",
        "few-shot prompting large language models",
        "chain-of-thought prompting elicits reasoning",
    ],
    "Context Engineering": [
        "context engineering large language models",
        "long context large language models",
        "retrieval augmented generation context window",
        "long context language models benchmark retrieval",
        "context compression large language models",
        "needle in a haystack long context language models",
    ],
    "LLM Memory & Personalization": [
        "memory mechanism large language model agents",
        "long-term memory LLM agents",
        "personalized large language models memory",
        "conversation memory large language models agents",
        "agent memory large language models",
    ],
    "Efficient LLMs: Training & Inference": [
        "efficient training transformers",
        "model compression large language models",
        "compression algorithms language models quantization pruning",
        "efficient guided generation large language models",
        "transformer inference optimization techniques",
        "efficient generative large language model serving systems",
        "efficient architectures large language models speed",
        "speculative decoding language model inference",
        "knowledge distillation language models",
        "flash attention fast memory efficient exact attention IO-awareness",
        "quantization INT4 INT8 LLM weight-only",
        "AWQ activation-aware weight quantization LLM",
    ],
    "Alignment & RLHF": [
        "aligned large language models human feedback",
        "reinforcement learning from human feedback open problems limitations",
        "post-training large language models alignment",
        "direct preference optimization language models",
        "constitutional AI harmless helpful language model",
        "PPO proximal policy optimization language model fine-tuning",
        "GRPO group relative policy optimization language model",
        "reward hacking alignment language models",
        "scalable oversight alignment language models",
        "value alignment large language models safety",
    ],
    "Evaluation of LLMs & Agents": [
        "evaluation large language models comprehensive",
        "evaluating large language models benchmark",
        "LLM-as-a-Judge evaluation framework",
        "SEED-Bench benchmarking multimodal LLMs comprehension",
        "evaluation LLM-based agents benchmark",
        "LLM benchmark leaderboard evaluation methodology",
    ],
    "Multimodal LLMs": [
        "multimodal large language models",
        "foundation models vision language",
        "multimodal deep learning vision language",
        "mathematical reasoning multimodal large language models challenges",
        "vision language model image understanding",
    ],
    "Multilingual & Low-Resource LLMs": [
        "multilingual large language models cross-lingual evaluation",
        "low-resource language large language models",
        "multilingual instruction tuning language models",
        "machine translation large language models multilingual",
        "culturally aware multilingual language models benchmark",
    ],
    "Speech & Audio Language Models": [
        "speech language models audio understanding",
        "audio large language models multimodal",
        "speech instruction tuning language model",
        "spoken dialogue large language models",
    ],
    "Small Language Models": [
        "small language models measurements insights",
        "small language models era large language models",
        "role small models LLM era",
        "phi language model small efficient",
    ],
    "Mixture of Experts": [
        "mixture of experts large language models",
        "sparse mixture of experts transformer",
        "MoE language model routing",
    ],
    "LLMs for Healthcare & Science": [
        "large language models healthcare clinical NLP",
        "medical reasoning large language models",
        "autonomous scientific discovery AI agentic science",
        "large language models biology chemistry science",
    ],
    "LLMs for Code": [
        "code foundation models agents applications",
        "code intelligence large language models",
        "code generation large language models",
        "LLM program synthesis code completion",
    ],
    "Tabular Data & NL2SQL": [
        "NL2SQL large language models text-to-SQL",
        "tabular data understanding large language models",
        "table question answering language model",
    ],
    "Data for LLMs": [
        "data management large language models",
        "data synthesis augmentation large language models",
        "pretraining data curation large language models",
        "synthetic data large language models instruction tuning",
        "data contamination large language model benchmarks",
        "web-scale dataset curation language model pretraining",
    ],
    "Trustworthy & Secure LLMs": [
        "trustworthy large language models safety",
        "adversarial attacks aligned language models universal",
        "jailbreak attacks large language models",
        "red-teaming large language models safety",
    ],
    "LLM Governance, Privacy & Copyright": [
        "large language model governance responsible AI",
        "privacy preserving large language models",
        "copyright training data large language models",
        "machine unlearning large language models",
        "AI regulation foundation models risk management",
    ],
    "Interpretability & Mechanistic Understanding": [
        "mechanistic interpretability transformer language models",
        "interpretability large language models circuits",
        "understanding language model representations probing",
        "explainable AI large language models",
        "sparse autoencoders language model features",
    ],
    "LLM Overview & History": [
        "AI-generated content AIGC history generative AI GAN ChatGPT",
        "large language models ChatGPT GPT-4 research perspective",
        "open-source large language models ChatGPT benchmarks performance",
        "language models recent developments outlook",
        "challenges applications large language models NLP",
        "harnessing power LLMs in practice ChatGPT beyond",
        "Google Gemini OpenAI GPT reshaping generative AI research",
        "foundation models opportunities risks",
    ],
    "AIOps & Observability": [
        "AIOps large language models era",
        "LLM operations observability monitoring",
        "log anomaly detection large language model",
    ],
    "Federated & Personalized AI": [
        "personalized federated intelligence foundation model",
        "federated learning large language models",
        "towards artificial general personalized intelligence",
    ],
    "Self-Supervised & Representation Learning": [
        "self-supervised learning cookbook methods",
        "self-supervised representation learning transformers",
        "contrastive learning language model pretraining",
    ],
    "GraphRAG & Knowledge Graphs": [
        "graph retrieval-augmented generation knowledge graph LLM",
        "GraphRAG knowledge graph large language models",
        "knowledge graph question answering large language models",
        "graph neural networks language models",
        "knowledge-enhanced large language models",
    ],
    "Embeddings & Vector Search": [
        "text embeddings large language models dense retrieval",
        "sentence embeddings semantic similarity",
        "vector databases approximate nearest neighbor search",
        "dense retrieval neural information retrieval",
        "embedding models language representation MTEB",
    ],
    "Function Calling & Tool Use": [
        "tool learning large language models API",
        "function calling language models external tools",
        "LLM tool augmented generation external knowledge",
        "language models API calling tool use",
        "plan and execute LLM tools agents",
    ],
    "Structured Generation & Constrained Decoding": [
        "constrained decoding large language models structured output",
        "grammar constrained generation language models",
        "JSON schema guided generation large language models",
        "formal language constrained decoding LLM",
    ],
    "LLM for Robotics & Embodied AI": [
        "large language models robotics embodied AI",
        "foundation models for robotic manipulation",
        "LLM robot planning grounding",
        "vision language models robotics",
        "embodied intelligence large language models",
    ],
    "LLMOps & Model Serving": [
        "LLMOps large language model operations deployment",
        "efficient serving large language models inference",
        "continuous batching language model serving",
        "AI model deployment monitoring production",
        "vLLM PagedAttention efficient LLM serving",
    ],
    "PEFT & LoRA": [
        "LoRA low-rank adaptation large language models",
        "parameter-efficient fine-tuning methods survey",
        "QLoRA efficient finetuning quantized LLMs",
        "adapter methods parameter-efficient transfer learning",
        "prefix tuning prompt tuning parameter efficient",
        "AdaLoRA adaptive budget allocation parameter efficient fine-tuning",
        "LoftQ LoRA fine-tuning quantization initializing language models",
        "DoRA weight-decomposed low-rank adaptation",
    ],
    "Instruction Tuning & SFT": [
        "instruction tuning large language models",
        "supervised fine-tuning language models instruction following",
        "self-instruct aligning language models instruction self-generated",
        "finetuned language models zero-shot learners",
        "LIMA less is more alignment data instruction tuning",
        "open instruction following evaluation benchmark",
        "alpaca instruction-following fine-tuning language model",
        "distilabel synthetic data instruction tuning pipeline",
    ],
    "RLAIF & Constitutional AI": [
        "reinforcement learning AI feedback RLAIF",
        "constitutional AI training harmless assistant AI feedback",
        "AI feedback preference learning language models",
        "self-rewarding language models AI feedback alignment",
        "scalable AI feedback language model alignment",
        "weak-to-strong generalization superalignment",
        "reward model AI preference language model",
    ],
    "RLVR & Process Reward Models": [
        "reinforcement learning verifiable rewards language model RLVR",
        "process reward model step-level feedback math reasoning",
        "outcome reward model ORM process reward PRM comparison",
        "DeepSeek GRPO reinforcement learning reasoning",
        "let's verify step by step process reward model",
        "math olympiad problem solving reinforcement learning LLM",
        "reward shaping language model reasoning verifiable",
        "STILL thinking slower language model reinforcement learning",
    ],
    "Inference-Time Scaling & Test-Time Compute": [
        "inference time scaling test-time compute language model",
        "scaling LLM test-time compute verifier reranking",
        "o1 OpenAI reasoning model thinking tokens",
        "chain-of-thought test time reasoning scaling",
        "best-of-n sampling language model inference compute",
        "self-consistency chain of thought reasoning LLM decoding",
        "compute-optimal inference language models",
        "thinking longer test-time reasoning scaling laws",
    ],
    "Scaling Laws": [
        "scaling laws neural language models",
        "Chinchilla training compute optimal large language models",
        "emergent abilities large language models scaling",
        "scaling data model size language model performance",
        "neural scaling laws data model compute",
        "grokking generalization beyond overfitting neural networks",
        "scaling language models methods analysis insights",
    ],
    "LLM Architecture Innovations": [
        "attention is all you need",
        "flash attention efficient exact attention IO-awareness",
        "Mamba linear time sequence modeling selective state spaces",
        "RWKV parallelizable RNN language models transformer",
        "rotary position embedding RoPE transformer",
        "grouped query attention GQA multi-query attention inference",
        "RetNet retentive network successor transformer",
        "state space model SSM sequence modeling language",
        "transformer architecture improvements efficiency",
        "sparse attention transformer long sequences",
        "multi-head latent attention KV cache compression",
    ],
    "Continual Learning & Model Merging": [
        "continual learning large language models catastrophic forgetting",
        "model merging task vectors weight interpolation language models",
        "model soup averaging weights fine-tuning",
        "ties-merging resolving interference model merging",
        "knowledge editing large language models",
        "lifelong learning language models forgetting",
        "catastrophic forgetting neural networks continual learning",
        "parameter merging multi-task language models",
    ],
}

FOUNDATIONAL_ARCHITECTURE_IDS = ("ARXIV:1706.03762",)

POPULAR_DISCOVERY_QUERIES: dict[str, list[str]] = {
    "LLM Overview & History": ['"language model"', '"foundation model"'],
    "LLM Architecture Innovations": ['"transformer" +"language"', '"transformer" +"attention" +"language"'],
    "Retrieval-Augmented Generation (RAG)": ['"retrieval augmented generation"', '"retrieval augmented language"'],
    "LLM Agents": ['"language model" +"agent"', '"language agent"'],
}

POPULAR_SOURCE_TOPICS = {
    "Foundational LLMs & Transformers": ("LLM Architecture Innovations", "LLM Overview & History"),
    "RAG (Retrieval-Augmented Generation)": ("Retrieval-Augmented Generation (RAG)",),
    "AI Agents": ("LLM Agents",),
}


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "based", "by", "for", "from", "in", "is", "it", "model",
    "models", "large", "language", "llm", "llms", "of", "on", "or", "the", "to", "towards", "using",
    "via", "with",
}

CORE_RELEVANCE_TERMS = (
    "large language model", "large language models", "llm", "llms", "language model", "language models",
    "chatgpt", "gpt-4", "gpt4", "foundation model", "foundation models", "transformer",
    "transformers", "pretrained language", "pre-trained language", "instruction tuning", "prompt tuning",
    "retrieval-augmented", "retrieval augmented", "vision-language", "multimodal", "tool use",
    "agent", "agents", "text-to-sql", "code generation", "mixture-of-experts", "mixture of experts",
    "lora", "quantization", "embedding", "state space model", "mamba", "rlhf", "alignment",
)

TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Reasoning in LLMs": (
        "reasoning", "chain-of-thought", "chain of thought", "tree of thoughts", "math reasoning",
        "logical reasoning", "test-time compute", "process reward", "verifiable reward",
    ),
    "LLM Agents": ("agent", "agents", "autonomous", "planning", "multi-agent", "agentic"),
    "Retrieval-Augmented Generation (RAG)": ("retrieval-augmented", "retrieval augmented", "rag", "dense retrieval"),
    "GUI Agents": ("gui", "computer use", "web agent", "screen", "ui agent"),
    "Hallucination in LLMs": ("hallucination", "hallucinations", "factuality", "faithfulness", "sycophancy"),
    "Prompt Engineering & In-Context Learning": (
        "prompt", "prompting", "in-context", "few-shot", "demonstrations", "prompt engineering",
    ),
    "Context Engineering": ("long context", "context window", "context engineering", "prompt compression"),
    "LLM Memory & Personalization": (
        "memory", "long-term memory", "conversation memory", "personalized", "personalization",
        "user preference", "agent memory",
    ),
    "Efficient LLMs: Training & Inference": (
        "efficient", "inference", "serving", "compression", "quantization", "pruning", "distillation",
        "speculative decoding", "flashattention", "pagedattention",
    ),
    "Alignment & RLHF": ("alignment", "rlhf", "human feedback", "preference", "reward model", "dpo"),
    "Evaluation of LLMs & Agents": ("evaluation", "benchmark", "bench", "leaderboard", "judge"),
    "Multimodal LLMs": ("multimodal", "vision-language", "vision language", "video", "image", "audio"),
    "Multilingual & Low-Resource LLMs": (
        "multilingual", "cross-lingual", "low-resource", "machine translation", "cultural",
    ),
    "Speech & Audio Language Models": (
        "speech", "audio", "spoken dialogue", "speech recognition", "text-to-speech",
    ),
    "Small Language Models": ("small language", "slm", "mobilellm", "phi", "on-device"),
    "Mixture of Experts": ("mixture of experts", "mixture-of-experts", "moe", "routing"),
    "LLMs for Healthcare & Science": ("healthcare", "clinical", "medical", "medicine", "science", "chemistry", "biology"),
    "LLMs for Code": ("code", "program synthesis", "code generation", "software engineering", "verilog"),
    "Tabular Data & NL2SQL": ("tabular", "table", "text-to-sql", "nl2sql", "sql"),
    "Data for LLMs": ("data", "dataset", "pretraining data", "synthetic data", "data curation"),
    "Trustworthy & Secure LLMs": (
        "trustworthy", "security", "safety", "jailbreak", "red-teaming", "adversarial", "privacy",
    ),
    "LLM Governance, Privacy & Copyright": (
        "governance", "responsible ai", "privacy", "copyright", "regulation", "machine unlearning",
    ),
    "Interpretability & Mechanistic Understanding": (
        "interpretability", "mechanistic", "circuits", "probing", "explainable", "sparse autoencoder",
    ),
    "LLM Overview & History": ("survey", "overview", "history", "foundation models", "aigc", "chatgpt"),
    "AIOps & Observability": ("aiops", "observability", "monitoring", "logs", "anomaly"),
    "Federated & Personalized AI": ("federated", "personalized", "personalization", "private data"),
    "Self-Supervised & Representation Learning": (
        "self-supervised", "self supervised", "representation learning", "contrastive", "masked language",
    ),
    "GraphRAG & Knowledge Graphs": ("graphrag", "knowledge graph", "graph rag", "graph retrieval"),
    "Embeddings & Vector Search": ("embedding", "embeddings", "vector", "semantic similarity", "dense retrieval"),
    "Function Calling & Tool Use": ("tool", "tools", "function calling", "api", "tool learning"),
    "Structured Generation & Constrained Decoding": (
        "constrained decoding", "structured output", "grammar", "json schema", "guided generation",
    ),
    "LLM for Robotics & Embodied AI": ("robot", "robotics", "embodied", "vision-language-action", "vla"),
    "LLMOps & Model Serving": ("llmops", "serving", "deployment", "continuous batching", "pagedattention"),
    "PEFT & LoRA": ("lora", "qlora", "adapter", "parameter-efficient", "peft", "prefix tuning"),
    "Instruction Tuning & SFT": ("instruction tuning", "instruction following", "sft", "self-instruct", "alpaca"),
    "RLAIF & Constitutional AI": ("rlaif", "constitutional ai", "ai feedback", "harmless"),
    "RLVR & Process Reward Models": ("rlvr", "process reward", "verifiable reward", "grpo", "reward shaping"),
    "Inference-Time Scaling & Test-Time Compute": (
        "test-time", "inference-time", "thinking", "best-of-n", "self-consistency", "verifier",
    ),
    "Scaling Laws": ("scaling law", "scaling laws", "compute-optimal", "chinchilla", "emergent abilities"),
    "LLM Architecture Innovations": (
        "architecture", "attention", "transformer", "mamba", "rwkv", "rope", "gqa", "state space",
        "retnet", "kv cache",
    ),
    "Continual Learning & Model Merging": (
        "continual", "catastrophic forgetting", "model merging", "model soup", "knowledge editing", "lifelong",
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def infer_arxiv_date(arxiv_id: str) -> tuple[int, int] | None:
    """Infer (year, month) from arXiv ID (YYMM.NNNNN format)."""
    match = re.match(r"(\d{2})(\d{2})\.(\d{4,5})", arxiv_id)
    if not match:
        return None
    yy, mm = int(match.group(1)), int(match.group(2))
    year = 2000 + yy
    if not (1 <= mm <= 12 and 2000 <= year <= datetime.datetime.now(datetime.UTC).year + 1):
        return None
    return year, mm


def format_month_year(year: int, month: int) -> str:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"[{months[month - 1]} {year}]"


def _paper_text(paper: dict) -> str:
    return " ".join(
        str(paper.get(key) or "") for key in ("title", "abstract", "venue")
    ).lower()


def _contains_term(text: str, term: str) -> bool:
    term = term.lower()
    if len(term) <= 4 and term.isalnum():
        return bool(re.search(rf"\b{re.escape(term)}\b", text))
    return term in text


def _has_core_relevance(paper: dict) -> bool:
    text = _paper_text(paper)
    return any(_contains_term(text, term) for term in CORE_RELEVANCE_TERMS)


def _topic_score(paper: dict, topic: str) -> float:
    text = _paper_text(paper)
    score = 0.0

    for keyword in TOPIC_KEYWORDS.get(topic, ()):
        if _contains_term(text, keyword):
            score += 3.0 if " " in keyword or "-" in keyword else 1.5

    for query in TOPICS.get(topic, []):
        tokens = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if t not in STOPWORDS and len(t) > 2]
        if not tokens:
            continue
        hits = sum(1 for token in tokens if _contains_term(text, token))
        if hits >= min(2, len(tokens)):
            score += hits / len(tokens)

    return score


def infer_paper_topics(paper: dict, max_topics: int = 3) -> list[str]:
    """Infer likely topic tags from title/abstract text for compact output."""
    existing = paper.get("topics") or []
    if existing:
        return list(dict.fromkeys(existing))[:max_topics]

    scored = [
        (topic, _topic_score(paper, topic))
        for topic in TOPICS
    ]
    topics = [topic for topic, score in sorted(scored, key=lambda item: item[1], reverse=True) if score > 0]
    if not topics and _has_core_relevance(paper):
        topics = ["LLM Overview & History"]
    return topics[:max_topics]


def _is_relevant_paper(paper: dict, topic: str) -> bool:
    """Keep broad Semantic Scholar searches from drifting away from the LLM landscape."""
    fields = paper.get("fieldsOfStudy") or []
    if "Computer Science" not in fields:
        return False
    if not _has_core_relevance(paper):
        return False
    return _topic_score(paper, topic) > 0


_DISCOVERY_TITLE_LANGUAGE = re.compile(
    r"\b(?:languages?|texts?|linguistic|nlp|llms?|gpt(?:-?\d+)?|chatgpt|bert|roberta|"
    r"llama|qwen|deepseek|t5|tokenization|retrieval[- ]augmented|rag|"
    r"translation|question answering|prompting|in-context learning)\b",
    re.IGNORECASE,
)
_DISCOVERY_ABSTRACT_LANGUAGE = re.compile(
    r"\b(?:language model(?:s|ing|ling)?|language agents?|large language|llms?|"
    r"gpt(?:-?\d+)?|chatgpt|bert|roberta|llama|qwen|deepseek|"
    r"natural language processing|machine translation|vision[- ]language|"
    r"retrieval[- ]augmented generation|text generation|question answering)\b",
    re.IGNORECASE,
)
_DISCOVERY_OTHER_DOMAIN = re.compile(
    r"\b(?:images?|vision|visual|video|segmentation|object detection|"
    r"time[- ]series|forecasting|gan|gans|generative adversarial|graph|"
    r"recommendation|robot|tracking|medical)\b",
    re.IGNORECASE,
)
_DISCOVERY_GENERAL_ARCHITECTURE = re.compile(
    r"\b(?:transformers?|attention)\b",
    re.IGNORECASE,
)


def _is_language_discovery(paper: dict) -> bool:
    """Require language relevance, not just background mentions in unrelated work."""
    title = str(paper.get("title") or "")
    abstract = str(paper.get("abstract") or "")
    if _DISCOVERY_TITLE_LANGUAGE.search(title):
        return True
    if _DISCOVERY_OTHER_DOMAIN.search(title):
        return False
    if abstract and _DISCOVERY_GENERAL_ARCHITECTURE.search(title):
        return True
    return bool(_DISCOVERY_ABSTRACT_LANGUAGE.search(abstract))


class QueryFetchError(RuntimeError):
    """Raised when a Semantic Scholar query cannot be fetched after retries."""


class TopicFetchIncomplete(RuntimeError):
    """Raised when a topic has partial results but one or more queries failed."""

    def __init__(self, topic: str, papers: list[dict], failed_queries: list[str]) -> None:
        super().__init__(f"{topic}: {len(failed_queries)} query/query(s) failed")
        self.topic = topic
        self.papers = papers
        self.failed_queries = failed_queries


# ---------------------------------------------------------------------------
# Fetcher
# ---------------------------------------------------------------------------

class SemanticScholarFetcher:
    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    _FIELDS: ClassVar[list[str]] = [
        "paperId",
        "title",
        "authors",
        "year",
        "citationCount",
        "abstract",
        "venue",
        "url",
        "externalIds",
        "fieldsOfStudy",
    ]

    def __init__(
        self,
        *,
        user_agent: str | None,
        api_key: str | None,
        timeout: int,
        max_retries: int,
        backoff: float,
        request_delay: float,
        jitter: float,
        cache_dir: Path | None = None,
    ) -> None:
        self.session = (
            SemanticScholarSession(cache_dir, request_delay=request_delay, jitter=jitter, user_agent=user_agent)
            if cache_dir is not None else create_session(user_agent)
        )
        if api_key:
            self.session.headers.update({"x-api-key": api_key})
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.request_delay = request_delay
        self.jitter = jitter
        # Public Semantic Scholar access is heavily rate-limited. Reserve the
        # next request slot before every call, including the first one.
        self._next_request_at = 0.0

    def _wait_for_request_slot(self) -> None:
        if isinstance(self.session, SemanticScholarSession):
            return
        wait = self._next_request_at - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_request_at = (
            time.monotonic()
            + max(self.request_delay, 1.0)
            + random.uniform(0, max(self.jitter, 0))
        )

    def _defer_after_rate_limit(self, backoff: float) -> None:
        self._next_request_at = max(
            self._next_request_at,
            time.monotonic() + backoff + random.uniform(0, max(self.jitter, 0)),
        )

    def search_papers(self, query: str, limit: int = 100, *, citation_ranked: bool = False) -> list[dict]:
        params: dict[str, str | int] = {
            "query": query,
            "fields": ",".join(self._FIELDS),
        }
        if citation_ranked:
            params.update({"sort": "citationCount:desc", "fieldsOfStudy": "Computer Science"})
        else:
            params["limit"] = min(limit, 100)
        url = f"{self.BASE_URL}/paper/search" + ("/bulk" if citation_ranked else "")
        backoff = self.backoff
        last_error = "no response"

        for attempt in range(self.max_retries):
            try:
                self._wait_for_request_slot()
                response = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if response.status_code == 200:
                    return response.json().get("data", [])[:limit]

                message = ""
                try:
                    payload = response.json()
                    message = str(payload.get("message") or payload.get("error") or "").strip()
                except ValueError:
                    message = response.text[:200].strip()
                last_error = f"HTTP {response.status_code}"
                if message:
                    last_error += f": {message}"

                if response.status_code not in {429, 500, 502, 503, 504}:
                    break

                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        backoff = max(backoff, float(retry_after))
                    except ValueError:
                        pass
                elif response.status_code == 429:
                    backoff = max(backoff, 120.0)
                    self._defer_after_rate_limit(backoff)

            if attempt < self.max_retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 300.0)

        raise QueryFetchError(f"Semantic Scholar query failed after retries ({last_error}): {query}")

    def batch_papers(self, ids: list[str], *, fields: list[str] | None = None) -> list[dict | None]:
        """Fetch papers by stable IDs in one low-volume API request."""
        if not ids:
            return []

        url = f"{self.BASE_URL}/paper/batch"
        params = {"fields": ",".join(self._FIELDS if fields is None else fields)}
        backoff = self.backoff
        last_error = "no response"

        for attempt in range(self.max_retries):
            try:
                self._wait_for_request_slot()
                response = self.session.post(url, params=params, json={"ids": ids}, timeout=self.timeout)
            except requests.RequestException as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                if response.status_code == 200:
                    return response.json()

                message = ""
                try:
                    payload = response.json()
                    message = str(payload.get("message") or payload.get("error") or "").strip()
                except ValueError:
                    message = response.text[:200].strip()
                last_error = f"HTTP {response.status_code}"
                if message:
                    last_error += f": {message}"

                if response.status_code not in {429, 500, 502, 503, 504}:
                    break

                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        backoff = max(backoff, float(retry_after))
                    except ValueError:
                        pass
                elif response.status_code == 429:
                    backoff = max(backoff, 120.0)
                    self._defer_after_rate_limit(backoff)

            if attempt < self.max_retries - 1:
                time.sleep(backoff)
                backoff = min(backoff * 2, 300.0)

        raise QueryFetchError(f"Semantic Scholar batch fetch failed after retries ({last_error})")

    def fetch_topic(
        self,
        topic: str,
        queries: list[str],
        top_n: int,
        min_citations: int,
        query_cache: dict[str, list[dict]],
        cache_updated: Callable[[], None] | None = None,
    ) -> list[dict]:
        """Aggregate results for multiple queries, deduplicate, filter, sort."""
        seen: set = set()
        papers: list[dict] = []
        failed_queries: list[str] = []

        for query in queries:
            cache_key = query.strip().lower()
            if cache_key in query_cache:
                search_results = query_cache[cache_key]
                print(f"  [cache] {query}")
            else:
                try:
                    search_results = self.search_papers(query)
                except QueryFetchError as exc:
                    print(f"  [WARN] {exc}")
                    failed_queries.append(query)
                    break
                query_cache[cache_key] = search_results
                if cache_updated:
                    cache_updated()

            for paper in search_results:
                pid = paper.get("paperId")
                if pid and pid not in seen:
                    seen.add(pid)
                    papers.append(paper)

        filtered = [
            p for p in papers
            if p.get("citationCount", 0) >= min_citations
            and _is_relevant_paper(p, topic)
        ]
        filtered.sort(key=lambda p: p.get("citationCount", 0), reverse=True)

        for paper in filtered:
            paper["topics"] = list(dict.fromkeys([*(paper.get("topics") or []), topic]))

        selected = filtered[:top_n] if top_n else filtered

        if failed_queries:
            raise TopicFetchIncomplete(topic, selected, failed_queries)

        return selected


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _paper_arxiv_url(paper: dict) -> str | None:
    ext = paper.get("externalIds") or {}
    arxiv_id = ext.get("ArXiv")
    return f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None


def _paper_link(paper: dict) -> str:
    return _paper_arxiv_url(paper) or paper.get("link") or paper.get("url") or "#"


def _paper_lookup_id(paper: dict) -> str | None:
    ext = paper.get("externalIds") or {}
    arxiv_id = ext.get("ArXiv")
    if arxiv_id:
        return f"ARXIV:{arxiv_id}"

    link = paper.get("link") or paper.get("url") or ""
    if "arxiv.org/abs/" in link:
        return "ARXIV:" + link.rsplit("/abs/", 1)[1].strip()
    if "semanticscholar.org/paper/" in link:
        return link.rsplit("/paper/", 1)[1].split("/", 1)[0].strip()
    return None


def _paper_date_str(paper: dict) -> str:
    if paper.get("date_str"):
        return paper["date_str"]
    ext = paper.get("externalIds") or {}
    arxiv_id = ext.get("ArXiv")
    if arxiv_id:
        ym = infer_arxiv_date(arxiv_id)
        if ym:
            return format_month_year(ym[0], ym[1])
    return ""


def _author_str(paper: dict) -> str:
    authors = paper.get("authors", [])
    names = [a.get("name", "") for a in authors[:3]]
    suffix = ", et al." if len(authors) > 3 else ""
    return ", ".join(names) + suffix


def format_paper_console(paper: dict, rank: int) -> str:
    lines = [
        f"\n{rank}. {paper.get('title', 'No title')}",
        f"   Authors: {_author_str(paper)}",
        (
            f"   Year: {paper.get('year', 'N/A')} | Citations: {paper.get('citationCount', 0):,}"
            f" | Venue: {paper.get('venue', 'N/A')}"
        ),
    ]
    date_str = _paper_date_str(paper)
    if date_str:
        lines.append(f"   Date: {date_str}")
    arxiv_url = _paper_arxiv_url(paper)
    if arxiv_url:
        lines.append(f"   arXiv: {arxiv_url}")
    else:
        lines.append(f"   URL: {paper.get('url', 'N/A')}")
    return "\n".join(lines) + "\n"


def _short_description(paper: dict) -> str:
    """Return a short description from the abstract (first sentence, max 200 chars)."""
    if paper.get("description"):
        return paper["description"].strip()
    abstract = (paper.get("abstract") or "").strip()
    if not abstract:
        return ""
    # Take up to the first sentence-ending punctuation
    for end in (".", "!", "?"):
        idx = abstract.find(end)
        if 30 < idx < 200:
            return abstract[: idx + 1]
    # Fallback: truncate at 200 chars on a word boundary
    if len(abstract) > 200:
        cut = abstract[:200].rsplit(" ", 1)[0]
        return cut.rstrip(",;:") + " ..."
    return abstract


def format_compact_entry(paper: dict, rank: int = 0) -> str:
    """Format: N. [Title📑](url): description. [Mon YYYY] (Citations: NNN)"""
    title = paper.get("title", "No title")
    link = _paper_link(paper)
    desc = _short_description(paper)
    date_str = _paper_date_str(paper)
    citations = paper.get("citationCount", 0)
    topics = infer_paper_topics(paper)

    prefix = f"{rank}." if rank > 0 else "1."
    entry = f"{prefix} [{title}📑]({link})"
    if desc:
        entry += f": {desc}"
    if date_str:
        entry += f" {date_str}"
    topic_str = f"; Topics: {', '.join(topics)}" if topics else ""
    entry += f" (Citations: {citations:,}{topic_str})"
    return entry


def _parse_compact_entry(line: str) -> dict | None:
    if not re.match(r"^\d+\. ", line):
        return None

    citation_match = re.search(r" \(Citations: ([\d,]+)(?:; Topics: (.*))?\)$", line)
    if not citation_match:
        return None

    body = line[: citation_match.start()]
    link_match = re.match(r"^\d+\. \[(.+?)\]\(([^)]+)\)(.*)$", body)
    if not link_match:
        return None

    title, link, remainder = link_match.groups()
    title = re.sub(r"(?:📑|≡ƒôæ)$", "", title).strip()
    date_str = ""
    date_match = re.search(r" (\[[A-Z][a-z]{2} \d{4}\])$", remainder)
    if date_match:
        date_str = date_match.group(1)
        remainder = remainder[: date_match.start()]

    abstract = remainder[2:].strip() if remainder.startswith(": ") else ""
    topics = []
    if citation_match.group(2):
        topics = [topic.strip() for topic in citation_match.group(2).split(",") if topic.strip()]

    paper = {
        "paperId": link,
        "title": title,
        "link": link,
        "url": link,
        "abstract": abstract,
        "description": abstract,
        "date_str": date_str,
        "citationCount": int(citation_match.group(1).replace(",", "")),
        "topics": topics,
    }
    if not topics:
        paper["topics"] = infer_paper_topics(paper)
    return paper


def _compact_entry_blocks(markdown_text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []

    for line in markdown_text.splitlines():
        if re.match(r"^\d+\. ", line):
            if current:
                blocks.append(" ".join(part.strip() for part in current if part.strip()))
            current = [line]
        elif current and not line.startswith("#") and line.strip():
            current.append(line)

    if current:
        blocks.append(" ".join(part.strip() for part in current if part.strip()))
    return blocks


def refresh_existing_papers(
    fetcher: SemanticScholarFetcher,
    output_file: str,
    min_citations: int,
    batch_size: int,
) -> None:
    existing_papers = _load_existing_markdown(output_file)
    if not existing_papers:
        print(f"No compact paper entries found in: {output_file}")
        return

    output_path = Path(output_file)
    discovery_note = None
    if output_path.exists():
        match = re.search(
            r"^\*(Popular-paper discovery[^\n]*)\* *$",
            output_path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if match:
            discovery_note = match.group(1)

    lookup_ids = [_paper_lookup_id(paper) for paper in existing_papers]
    refreshed_by_id: dict[str, dict | None] = {}
    if isinstance(fetcher.session, SemanticScholarSession):
        cached = fetcher.session.cached_papers(
            [paper_id for paper_id in lookup_ids if paper_id], ["citationCount"],
        )
        refreshed_by_id.update(cached)
        print(f"[cache] Found citation data for {len(cached)} existing paper IDs.")
    pending = list(dict.fromkeys(
        paper_id for paper_id in lookup_ids if paper_id and paper_id not in refreshed_by_id
    ))
    failure: QueryFetchError | None = None
    for start in range(0, len(pending), batch_size):
        chunk = pending[start:start + batch_size]
        print(f"[batch] Fetching {len(chunk)} papers ({start + 1}-{start + len(chunk)})")
        try:
            results = fetcher.batch_papers(chunk, fields=["citationCount"])
        except QueryFetchError as exc:
            if not any(refreshed_by_id.values()):
                raise
            print(f"  [WARN] {exc}; saving successful updates and retaining unavailable counts.")
            failure = exc
            break
        refreshed_by_id.update(zip(chunk, results))

    refreshed: list[dict] = []
    updated = 0
    missing = 0
    for original, lookup_id in zip(existing_papers, lookup_ids):
        live = refreshed_by_id.get(lookup_id or "")
        if live:
            live = {**original, **live}
            topics = original.get("topics") or infer_paper_topics(original)
            live["topics"] = topics
            refreshed.append(live)
            if live.get("citationCount") != original.get("citationCount"):
                updated += 1
        else:
            refreshed.append(original)
            missing += 1

    refreshed = [paper for paper in refreshed if paper.get("citationCount", 0) >= min_citations]
    refresh_note = f"Citation data refreshed for {len(existing_papers) - missing} existing entries."
    if missing:
        refresh_note += f" Warning: {missing} unavailable entries retain previously recorded citation counts."
    _flush_output(
        output_file, refreshed, min_citations,
        refresh_note=refresh_note, discovery_note=discovery_note,
    )
    print(
        f"Refreshed {len(refreshed)} existing papers from Semantic Scholar batch API: "
        f"{updated} citation count(s) changed, {missing} missing response(s)."
    )
    if failure:
        raise QueryFetchError(f"Partial citation refresh saved to {output_file}: {failure}") from failure


def _load_existing_markdown(output_file: str, source_file: str | None = None) -> list[dict]:
    if source_file == "-":
        markdown_text = sys.stdin.read()
    elif source_file and source_file.startswith("git:"):
        repo_root = get_repo_root(__file__)
        markdown_bytes = subprocess.check_output(
            ["git", "show", source_file.removeprefix("git:")],
            cwd=repo_root,
        )
        markdown_text = markdown_bytes.decode("utf-8")
    else:
        path = Path(source_file or output_file)
        if not path.exists():
            return []
        markdown_text = path.read_text(encoding="utf-8")

    papers = []
    for line in _compact_entry_blocks(markdown_text):
        paper = _parse_compact_entry(line)
        if paper:
            papers.append(paper)
    return papers


def merge_discovered_papers(
    existing: list[dict],
    candidates: list[dict],
    topics: tuple[str, ...],
    min_citations: int,
) -> int:
    """Append relevant, previously unseen candidates without changing existing records."""
    identifiers = {_paper_lookup_id(paper) for paper in existing if _paper_lookup_id(paper)}
    paper_ids = {paper.get("paperId") for paper in existing if paper.get("paperId")}
    titles = {(paper.get("title") or "").strip().casefold() for paper in existing}
    added = 0
    for candidate in candidates:
        citations = candidate.get("citationCount")
        title = (candidate.get("title") or "").strip()
        identifier = _paper_lookup_id(candidate)
        paper_id = candidate.get("paperId") or identifier
        matching_topics = [topic for topic in topics if _is_relevant_paper(candidate, topic)]
        if (
            not isinstance(citations, int) or citations < min_citations or not title or not paper_id
            or not matching_topics or identifier in identifiers or paper_id in paper_ids
            or title.casefold() in titles
        ):
            continue
        paper = {**candidate, "paperId": paper_id, "topics": matching_topics}
        existing.append(paper)
        if identifier:
            identifiers.add(identifier)
        paper_ids.add(paper_id)
        titles.add(title.casefold())
        added += 1
    return added


def discover_popular_papers(
    fetcher: SemanticScholarFetcher,
    output_file: str,
    popular_source: str,
    min_citations: int,
) -> None:
    """Merge prior popular papers and citation-ranked discoveries into existing output."""
    from fetch_popular_papers import parse_existing_markdown

    existing = _load_existing_markdown(output_file)
    if not existing:
        raise ValueError(f"No landscape papers found in {output_file}; leaving output unchanged.")
    source_sections = parse_existing_markdown(popular_source)
    if not source_sections or not any(entries for _, entries in source_sections):
        raise ValueError(f"No popular papers found in {popular_source}; leaving output unchanged.")
    current_text = Path(output_file).read_text(encoding="utf-8")
    previous_note = re.search(r"^\*(Citation data refreshed[^\n]*)\* *$", current_text, re.MULTILINE)
    refresh_note = previous_note.group(1) if previous_note else None
    imported = 0
    for section, candidates in source_sections:
        topics = POPULAR_SOURCE_TOPICS.get(section)
        if topics:
            imported += merge_discovered_papers(existing, candidates, topics, min_citations)
    print(f"[popular source] Added {imported} previously omitted papers from {popular_source}")

    total_queries = sum(len(queries) for queries in POPULAR_DISCOVERY_QUERIES.values())
    completed = 0
    discovered = 0

    def save_progress(status: str) -> None:
        note = (
            f"Popular-paper discovery {status}; {completed}/{total_queries} citation-ranked queries completed. "
            "Searches examine up to the first 1,000 results per query and include qualifying "
            "records from the existing popular-paper list."
        )
        _flush_output(output_file, existing, min_citations, refresh_note=refresh_note, discovery_note=note)

    save_progress("in progress")
    for topic, queries in POPULAR_DISCOVERY_QUERIES.items():
        for query in queries:
            print(f"[citation-ranked search] {topic}: {query}")
            try:
                results = fetcher.search_papers(query, limit=1000, citation_ranked=True)
            except QueryFetchError as exc:
                save_progress("incomplete")
                raise QueryFetchError(
                    f"Popular-paper discovery paused at {query!r}; {completed}/{total_queries} queries "
                    "completed. Existing and discovered records were saved; rerun --discover-popular to resume."
                ) from exc
            candidates = [paper for paper in results if _is_language_discovery(paper)]
            added = merge_discovered_papers(existing, candidates, (topic,), min_citations)
            discovered += added
            completed += 1
            print(f"  -> {added} new eligible papers")
            save_progress("in progress")

    save_progress("complete")
    print(f"Popular discovery complete: {imported} imported, {discovered} found via citation-ranked search.")


def _topic_counts(papers: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for paper in papers:
        for topic in infer_paper_topics(paper):
            counts[topic] = counts.get(topic, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _load_checkpoint(checkpoint_file: str) -> tuple[list[dict], set[str], list[str], dict[str, list[dict]], list[str]]:
    """Load discovery progress only for the current UTC month."""
    path = Path(checkpoint_file)
    if not path.exists():
        return [], set(), [], {}, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        period = datetime.datetime.now(datetime.UTC).strftime("%Y-%m")
        if data.get("period") != period:
            print("  [resume] Checkpoint is from an earlier or unknown month; starting current-month discovery.")
            return [], set(), [], {}, []
        papers = data.get("papers", [])
        completed = data.get("completed_topics", [])
        query_cache = data.get("query_cache", {})
        failed_queries = data.get("failed_queries", [])
        seen = {p["paperId"] for p in papers if p.get("paperId")}
        print(
            f"  [resume] Loaded {len(papers)} papers, {len(completed)} completed topics, "
            f"{len(query_cache)} cached queries from checkpoint."
        )
        return papers, seen, completed, query_cache, failed_queries
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        print(f"  [WARN] Could not read checkpoint ({exc}); starting fresh.")
        return [], set(), [], {}, []


def _save_checkpoint(
    checkpoint_file: str,
    papers: list[dict],
    completed_topics: list[str],
    query_cache: dict[str, list[dict]],
    failed_queries: list[str],
) -> None:
    """Persist current state to checkpoint JSON."""
    data = {
        "period": datetime.datetime.now(datetime.UTC).strftime("%Y-%m"),
        "completed_topics": completed_topics,
        "failed_queries": failed_queries,
        "query_cache": query_cache,
        "papers": papers,
    }
    Path(checkpoint_file).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _flush_output(
    output_file: str,
    papers: list[dict],
    min_citations: int,
    *,
    refresh_note: str | None = None,
    discovery_note: str | None = None,
) -> list[str]:
    """Sort papers by citation count and rewrite the output markdown. Returns compact lines."""
    sorted_papers = sorted(papers, key=lambda p: p.get("citationCount", 0), reverse=True)
    compact_lines = [format_compact_entry(p, rank=i + 1) for i, p in enumerate(sorted_papers)]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# LLM Landscape Papers (Citation \u2265 {min_citations})\n\n")
        f.write(f"*Generated: {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}*  \n")
        f.write("*Source: Semantic Scholar API and local topic inference \u2014 Computer Science papers only*  \n")
        if refresh_note:
            f.write(f"*{refresh_note}*  \n")
        if discovery_note:
            f.write(f"*{discovery_note}*  \n")
        f.write(f"*Total papers: {len(sorted_papers)}*\n\n")
        counts = _topic_counts(sorted_papers)
        if counts:
            f.write("## Topic Coverage\n\n")
            f.writelines(f"- {topic}: {count}\n" for topic, count in counts.items())
            f.write("\n## Papers\n\n")
        f.write("\n".join(compact_lines) + "\n")
    return compact_lines


def write_markdown_section(f, topic: str, papers: list[dict]) -> None:
    f.write(f"\n## {topic}\n\n")
    f.write(f"*Retrieved: {datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}*  \n")
    f.write(f"*Papers shown: {len(papers)}*\n\n")

    if not papers:
        f.write("*No papers found meeting the criteria.*\n\n")
        return

    for idx, paper in enumerate(papers, 1):
        title = paper.get("title", "No title")
        url = paper.get("url", "")
        arxiv_url = _paper_arxiv_url(paper)
        link = arxiv_url or url

        f.write(f"### {idx}. [{title}]({link})\n\n")
        f.write(f"**Authors:** {_author_str(paper)}  \n")
        f.write(
            f"**Year:** {paper.get('year', 'N/A')} | "
            f"**Citations:** {paper.get('citationCount', 0):,} | "
            f"**Venue:** {paper.get('venue', 'N/A')}  \n"
        )
        date_str = _paper_date_str(paper)
        if date_str:
            f.write(f"**Month:** {date_str}  \n")
        fields = paper.get("fieldsOfStudy") or []
        if fields:
            f.write(f"**Fields:** {', '.join(fields)}  \n")
        if arxiv_url:
            f.write(f"**arXiv:** [{arxiv_url}]({arxiv_url})  \n")

        abstract = paper.get("abstract", "")
        if abstract:
            # Truncate very long abstracts for readability
            if len(abstract) > 600:
                abstract = abstract[:600].rstrip() + " ..."
            f.write(f"\n> {abstract}\n")
        f.write("\n---\n\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch high-citation LLM landscape papers (research, surveys, benchmarks) from Semantic Scholar."
    )
    parser.add_argument("--output", help="Output markdown file path.")
    parser.add_argument(
        "--min-citations", type=int, default=150,
        help="Minimum citation count (default: 150)."
    )
    parser.add_argument(
        "--top-n", type=int, default=0,
        help="Maximum papers per topic; 0 keeps all eligible search results (default: 0)."
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--backoff", type=float, default=1.0)
    parser.add_argument(
        "--request-delay", type=float, default=5.0,
        help="Delay between Semantic Scholar requests in seconds (default: 5.0)."
    )
    parser.add_argument(
        "--jitter", type=float, default=0.5,
        help="Random extra delay between requests in seconds (default: 0.5)."
    )
    parser.add_argument(
        "--api-key-env", default="S2_API_KEY",
        help="Environment variable containing a Semantic Scholar API key, if available."
    )
    parser.add_argument(
        "--user-agent", default="Academic-Research-Tool/1.0",
        help="HTTP User-Agent header."
    )
    parser.add_argument(
        "--topics", nargs="*",
        help="Limit to specific topic names (substring match, case-insensitive)."
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Ignore any existing checkpoint and start from scratch."
    )
    parser.add_argument(
        "--annotate-existing", action="store_true",
        help="Rewrite the existing output with inferred topic tags and coverage without calling the API."
    )
    parser.add_argument(
        "--refresh-existing", action="store_true",
        help="Refresh citation counts of existing entries using lightweight Semantic Scholar batches, preserving metadata."
    )
    parser.add_argument(
        "--discover-popular", action="store_true",
        help="Merge the popular-paper list and citation-ranked searches into existing landscape output.",
    )
    parser.add_argument(
        "--popular-source",
        help="Popular-paper Markdown source for --discover-popular (default: section/x_popular_papers.md).",
    )
    parser.add_argument(
        "--batch-size", type=int, default=20,
        help="Number of papers per refresh request (default: 20)."
    )
    parser.add_argument("--cache-dir", type=Path, help="Shared monthly API cache (default: .cache/semantic-scholar).")
    parser.add_argument(
        "--annotate-source",
        help="Optional markdown source for --annotate-existing; use '-' for stdin or 'git:<rev>:<path>'."
    )
    args = parser.parse_args()
    if args.batch_size < 1 or args.top_n < 0 or args.min_citations < 0:
        parser.error("--batch-size must be positive; --top-n and --min-citations must be non-negative.")
    if args.discover_popular and (args.refresh_existing or args.annotate_existing or args.topics):
        parser.error("--discover-popular cannot be combined with --refresh-existing, --annotate-existing, or --topics.")
    if args.max_retries < 1 or args.request_delay < 1 or args.jitter < 0 or args.backoff < 0:
        parser.error("--max-retries and --request-delay must be at least 1; --jitter and --backoff must be non-negative.")

    root_dir = get_repo_root(__file__)
    output_file = args.output or str(root_dir / "section" / "x_llm_papers.md")

    if args.annotate_existing:
        existing_papers = _load_existing_markdown(output_file, args.annotate_source)
        if not existing_papers:
            print(f"No compact paper entries found in: {output_file}")
            return
        _flush_output(output_file, existing_papers, args.min_citations)
        print(f"Annotated {len(existing_papers)} existing papers with inferred topics: {output_file}")
        return

    fetcher = SemanticScholarFetcher(
        user_agent=args.user_agent,
        api_key=os.environ.get(args.api_key_env),
        timeout=args.timeout,
        max_retries=args.max_retries,
        backoff=args.backoff,
        request_delay=args.request_delay,
        jitter=args.jitter,
        cache_dir=args.cache_dir or root_dir / ".cache" / "semantic-scholar",
    )

    if args.refresh_existing:
        refresh_existing_papers(fetcher, output_file, args.min_citations, args.batch_size)
        return

    if args.discover_popular:
        popular_source = args.popular_source or str(root_dir / "section" / "x_popular_papers.md")
        discover_popular_papers(fetcher, output_file, popular_source, args.min_citations)
        return

    # Optionally filter topics
    topics_to_run = TOPICS
    if args.topics:
        filters = [t.lower() for t in args.topics]
        topics_to_run = {
            k: v for k, v in TOPICS.items()
            if any(f in k.lower() for f in filters)
        }
        if not topics_to_run:
            print("No matching topics found. Available topics:")
            for t in TOPICS:
                print(f"  {t}")
            return

    checkpoint_file = str(Path(output_file).with_suffix(".checkpoint.json"))

    # Load or reset checkpoint
    if args.reset and Path(checkpoint_file).exists():
        Path(checkpoint_file).unlink()
        print("  [reset] Checkpoint deleted.")

    global_papers, global_seen, completed_topics, query_cache, failed_queries = _load_checkpoint(checkpoint_file)

    def persist_progress() -> None:
        _save_checkpoint(checkpoint_file, global_papers, completed_topics, query_cache, failed_queries)

    def merge_papers(papers: list[dict], topic_name: str) -> int:
        added = 0
        by_id = {paper.get("paperId"): paper for paper in global_papers if paper.get("paperId")}
        by_lookup_id = {
            lookup_id: paper for paper in global_papers
            if (lookup_id := _paper_lookup_id(paper))
        }
        for paper in papers:
            pid = paper.get("paperId")
            if not pid:
                continue
            existing = by_id.get(pid) or by_lookup_id.get(_paper_lookup_id(paper) or "")
            if existing is not None:
                existing_topics = existing.get("topics") or []
                existing["topics"] = list(dict.fromkeys([*existing_topics, topic_name]))
            elif pid not in global_seen:
                paper["topics"] = list(dict.fromkeys([*(paper.get("topics") or []), topic_name]))
                global_seen.add(pid)
                global_papers.append(paper)
                by_id[pid] = paper
                lookup_id = _paper_lookup_id(paper)
                if lookup_id:
                    by_lookup_id[lookup_id] = paper
                added += 1
        return added

    if "LLM Architecture Innovations" in topics_to_run:
        known_ids = {_paper_lookup_id(paper) for paper in global_papers}
        missing_ids = [identifier for identifier in FOUNDATIONAL_ARCHITECTURE_IDS if identifier not in known_ids]
        if missing_ids:
            foundations = fetcher.batch_papers(missing_ids)
            if len(foundations) != len(missing_ids):
                raise QueryFetchError("Incomplete foundational architecture paper response; output unchanged.")
            for identifier, paper in zip(missing_ids, foundations):
                if (
                    not paper or not paper.get("paperId") or _paper_lookup_id(paper) != identifier
                    or "Computer Science" not in (paper.get("fieldsOfStudy") or [])
                    or not isinstance(paper.get("citationCount"), int)
                ):
                    raise QueryFetchError(
                        f"Invalid or missing foundational architecture paper {identifier}; output unchanged."
                    )
                if paper["citationCount"] >= args.min_citations:
                    merge_papers([paper], "LLM Architecture Innovations")
            persist_progress()

    # Collect all papers across every topic into a single deduplicated pool
    for topic_name, queries in topics_to_run.items():
        if topic_name in completed_topics:
            print(f"\n[{topic_name}] Already done (skipping).")
            continue

        print(f"\n[{topic_name}] Querying {len(queries)} search term(s)...")
        try:
            papers = fetcher.fetch_topic(
                topic_name,
                queries,
                top_n=args.top_n,
                min_citations=args.min_citations,
                query_cache=query_cache,
                cache_updated=persist_progress,
            )
        except TopicFetchIncomplete as exc:
            added = merge_papers(exc.papers, topic_name)
            failed_queries.extend(exc.failed_queries)
            persist_progress()
            print(
                f"  [pause] {topic_name} incomplete: {len(exc.failed_queries)} failed query/query(s), "
                f"{added} partial paper(s) saved to checkpoint. Re-run without --reset to resume."
            )
            return

        added = merge_papers(papers, topic_name)
        completed_topics.append(topic_name)
        failed_queries = []
        print(f"  -> {len(papers)} papers, {added} new (pool size: {len(global_papers)})")

        # Persist progress after every topic so we can resume on interruption
        persist_progress()

    # Final flush (updates timestamp)
    _flush_output(output_file, global_papers, args.min_citations)

    # Print to console
    sorted_papers = sorted(global_papers, key=lambda p: p.get("citationCount", 0), reverse=True)
    for idx, paper in enumerate(sorted_papers, 1):
        print(format_paper_console(paper, idx))

    print(f"\nDone. {len(global_papers)} unique papers saved to: {output_file}")

    # Remove checkpoint on successful completion
    if Path(checkpoint_file).exists():
        Path(checkpoint_file).unlink()
        print("  [done] Checkpoint removed.")


if __name__ == "__main__":
    main()
