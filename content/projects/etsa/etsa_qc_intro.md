<center>

### **AeVAA: An Explainable AI Framework for Aspect-Based Sentiment Analysis**

</center>

**Project Summary:** AeVAA is a modular, psychologically-grounded framework designed to provide an explainable and debuggable framework for Aspect-Based Sentiment Analysis (ABSA). It constructs a dynamic knowledge graph of entities and their interactions/relations, moving beyond "black-box" models to deliver nuanced, valence-aware sentiment scores with a clear, traceable reasoning process.

**My Role:** I performed as the first author on the paper, leading the conception and development of the project. My contributions included: 1. designing the system architecture, developing the LLM-powered relation and modifier extraction modules, implementing the survey-based data collection pipeline, and building the benchmarking and ablation study framework.

**Co-authors:** 
- Associate Professor David-Guy Brizan (Associate professor of CS at USFCA, project supervisor)
- Alex Peczon (Undergraduate student in CS at USFCA, co-author)
- Assistant Professor Sarah Hillenbrand (Assistant professor of neuroscience at USFCA, co-author and advisor)

---

### The Problem: The "Black Box" of Modern Sentiment Analysis

Most sentiment analysis tools produce a single, document-wide score, which fails to capture the complex sentiments directed at different subjects within a text. While Aspect-Based Sentiment Analysis (ABSA) addresses this by targeting specific entities, state-of-the-art, or SOTA, models (typically based on transformers like BERT, RoBERTa, etc) have three limitations:

1.  **Lack of Explainability:** These systems are "black boxes." It is almost impossible to understand why a model makes particular decision, making it difficult to debug.
2.  **Poor Long-Context Handling:** Most ABSA datasets are sentence-level, meaning the models trained on these datasets struggle to track document-wide sentiment analysis.
3.  **Limited Granularity:** Many models frame the task as a discrete classification problem (Positive, Negative, Neutral), losing the nuance of sentiment intensity, or valence (e.g., -0.2 for "problematic" vs. -0.7 "disastrous").

### The Solution: AeVAA's Modular, Graph-Centric Approach

AeVAA aims to solve these challenges by deconstructing the ABSA task into a multi-stage pipeline that models human cognitive processes. Instead of a single opaque model, AeVAA uses a series of modules that build upon each other to achieve a final sentiment score with an explanatory trace.

This modularity makes the system highly interpretable, debuggable, and changable, meaning any component to be swapped out for a more advanced or explainable alternative.

---

### Technical Details: System Architecture & Skills

The AeVAA pipeline is composed of five core modules, each demonstrating a distinct set of technical and analytical skills.

<center>

![Etsa Pipeline](/static/imgs/etsa_pipeline.png)

</center>

#### 1. Constituency Clause Extraction
-   **Purpose:** The system first breaks down raw text into grammatically coherent constituency clauses. This mirrors the hierarchical way humans parse information and ensures that entity interactions are analyzed within their correct local context.
-   **Technology:** We leveraged the **Berkeley Neural Parser (Benepar)**, integrated with a **spaCy** NLP pipeline, for its state-of-the-art accuracy in dependency and constituency parsing.
-   **Skills Demonstrated:**
    -   **NLP Fundamentals:** Deep understanding of syntax, dependency parsing, and constituency grammars.
    -   **Python & Library Integration:** Implementing and configuring advanced NLP libraries like `spaCy` and `Benepar`.

#### 2. Entity and Coreference Resolution
-   **Purpose:** This module identifies all unique entities (aspects) in the text and resolves coreferences (e.g., linking "the laptop," "my computer," and "it" to the same underlying entity).
-   **Technology:** I implemented a hybrid approach combining a custom rule-based aspect extractor (trained on SemEval data) with **Maverick**, a state-of-the-art coreference resolution model. The spaCy `en_core_web_trf` model provided the foundational token-level features (NER, POS tags).
-   **Skills Demonstrated:**
    -   **Machine Learning:** Training and applying rule-based models for Information Extraction.
    -   **NLP Pipelines:** Named Entity Recognition (NER), Noun Chunking, and Coreference Resolution.
    -   **System Design:** Engineering a hybrid system that combines the strengths of multiple models.

#### 3. Relation and Modifier Extraction
-   **Purpose:** The module identifies three crucial types of relationships between entities (**Action**, **Association**, **Ownership**) and extracts descriptive modifiers that carry sentiment (e.g., "incredibly fast," "terrible battery life").
-   **Technology:** As no off-the-shelf tools existed for this nuanced task, I developed a solution using the **Google Gemma 27B** Large Language Model. This involved designing a sophisticated few-shot prompting strategy with a strict output schema to ensure consistent, machine-readable JSON. The module also includes robust error handling, JSON parsing, and an intelligent caching layer to manage API costs and latency.
-   **Skills Demonstrated:**
    -   **AI & LLM Engineering:** Advanced prompt engineering, few-shot learning, and output structuring for generative models.
    -   **API Integration & Management:** Building resilient modules with rate limiting, backoff-retries, and file-based caching.
    -   **Data Structuring:** Designing and validating complex JSON schemas for reliable data exchange.

#### 4. Graph Construction and Layering
-   **Purpose:** The extracted entities, modifiers, and relations are synthesized into a layered, directed multi-graph. Each clause represents a 2D layer where nodes are entity mentions and edges are relations. These layers are stacked chronologically along a Z-axis, with temporal edges connecting mentions of the same entity across clauses.
-   **Technology:** The entire graph structure was implemented using the **NetworkX** library. I also developed a custom visualization module using **Plotly** to generate interactive 3D renderings of the graph for debugging and analysis.
-   **Skills Demonstrated:**
    -   **Data Structures & Algorithms:** Applied graph theory concepts to model complex linguistic phenomena.
    -   **Software Engineering:** Designing a robust and extensible `RelationGraph` class with a clear API.
    -   **Data Visualization:** Creating informative and interactive visualizations with `Plotly` and `Matplotlib`.

#### 5. Sentiment Calculation and Aggregation
-   **Purpose:** This final module calculates the sentiment. An initial valence score is assigned to each entity mention (based on its modifiers) and relation. These scores are then propagated through the graph using a suite of psychologically-grounded formulas. Finally, the clause-level scores for each entity are aggregated into a single, final sentiment value.
-   **Technology:** Initial sentiment is derived from a weighted ensemble of models, including a valence-mapped **DistilBERT** and **VADER**. The propagation and aggregation steps use custom formulas derived from human survey data (see below), implemented with **NumPy** and **SciPy**.
-   **Skills Demonstrated:**
    -   **Sentiment Analysis:** Implementing and ensembling multiple sentiment analysis models.
    -   **Algorithm Design:** Developing a novel graph-based algorithm for sentiment propagation and aggregation.
    -   **Scientific Computing:** Using `NumPy` for efficient numerical operations on sentiment scores.

---

### Innovation: Psychologically-Grounded Sentiment Models

To move beyond simple heuristics, we needed to model how humans *actually* process and update their impressions. Since no existing dataset captured these dynamics, we aimed to create one.

1.  **Lexicon Generation:** We built a lexicon optimizer that scored candidate words and phrases using a 9-model ensemble, perplexity scores (from GPT-2), and semantic cohesion to generate a high-quality lexicon for the survey.
2.  **Survey-Based Data Collection:** We designed and implemented a survey using **Streamlit** to collect human sentiment judgments. The survey generated randomized, templated scenarios modeling different entity interactions (e.g., a positive entity performing a negative action on another positive entity) and aggregation effects (primacy vs. recency bias).
3.  **Formula Derivation:** Using the collected pilot data (N=36), I fit parameters for a suite of candidate formulas using **SciPy's** optimization functions. These formulas, inspired by psychological concepts like negativity bias and the serial position effect, now power the AeVAA sentiment calculation module.

#### Explainable Trace Example

Below, I've included an example of the explanatory trace of the model.

<center>

![Etsa Pipeline](/static/imgs/pipeline_trace.png)

</center>

This data-driven approach allows the model's reasoning to be grounded in observable human behavior, making its outputs not only explainable but also more intuitively aligned with how people perceive sentiment.

---

### Results & Impact

We evaluated the end-to-end AeVAA framework on the SemEval 2014 ABSA benchmark. While it did not achieve state-of-the-art accuracy (achieving **78.58% accuracy** on the Restaurant dataset), this was not the primary goal. The true impact of AeVAA lies in its **explainability and debuggability**.

-   **Transparent Reasoning:** The modular architecture and graph output provide a complete trace, allowing us to see exactly how a final score was derived—from the initial modifiers to the effect of each relational interaction.
-   **Rapid Debugging:** During evaluation, we quickly identified performance bottlenecks. For example, the explanatory traces revealed that the modifier extraction module was a primary source of error. By refining the LLM prompt, we significantly improved performance, a task that would be impossible with a black-box model.
-   **Quantified Contributions:** An ablation study confirmed that the modifier extraction module was the most critical component for accuracy, demonstrating the framework's utility for analytical research.

AeVAA serves as a robust proof-of-concept, demonstrating that a modular, psychologically-grounded approach can create a powerful, trustworthy, and continuously improvable system for sentiment analysis.

##### Publication

We anticipate a submission to ARR in Jan 2026. This page may be taken down to abide with ARR double blind policy.

---

### Skills Showcase

-   **Programming & Core Tech:**
    -   **Python:** Advanced python including object-oriented design and package development.
    -   **Git & GitHub:** Version control, branching, and collaborative development.
    -   **Virtual Environments:** `venv` for dependency management.
-   **NLP & Machine Learning:**
    -   **Core NLP:** Dependency/Constituency Parsing, NER, POS Tagging, Coreference Resolution.
    -   **Libraries:** `spaCy`, `NLTK`, `Transformers`, `PyTorch`, `Maverick`.
    -   **Sentiment Analysis:** VADER, TextBlob, Flair, and various transformer-based models.
-   **AI & Large Language Models (LLMs):**
    -   **Prompt Engineering:** Designing complex few-shot prompts with structured JSON output for Google Gemma.
    -   **API Integration:** Building resilient services with caching, rate limiting, and error handling.
-   **Data Science & Scientific Computing:**
    -   **Libraries:** `NumPy`, `Pandas`, `SciPy` (for optimization), `scikit-learn`.
    -   **Experimental Design:** Designing and implementing a human-in-the-loop data collection survey.
    -   **Statistics:** Model evaluation (MSE, R²), cross-validation, and statistical analysis.
-   **Web & Visualization:**
    -   **Streamlit:** Developed a full-stack web application for data collection.
    -   **Data Visualization:** `Plotly` and `Matplotlib` for creating interactive 3D graphs and static report figures.