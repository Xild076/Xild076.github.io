<center>

### Alitheia AI - An Engine for Objectifying News

</center>

**Project Summary:** Alitheia AI was my attempt to build a tool to help navigate the complex and often biased world of online news. It's a multi-stage pipeline that automatically gathers news articles on a given topic, identifies the core underlying narratives, rewrites them to be more objective, and assigns a transparent reliability score. The goal is to move beyond simple "fact-checking" and instead provide users with a clear, neutralized view of what different sources are actually saying.

**My Role:** As the sole developer, I designed and built this project from the ground up. My work involved everything from architecting the data pipeline and implementing the web scraping tools to designing the clustering algorithms, building the language objectification engine, and creating the final interactive Streamlit application.

---

### The Problem: Navigating the Maze of Misinformation

Misinformation isn't new, but the scale and speed at which it spreads today is. With endless news sources, echo chambers, and emotionally charged language, it's incredibly difficult to get a clear, unbiased picture of any given topic. A single event can be framed in dozens of different ways, leaving you to wonder what the core facts really are.

This project was born out of that frustration. I wanted to create a system that could automatically cut through the noise, strip away the spin, and present the fundamental narratives in a way that was easy to understand and trust.

### The Solution: A Pipeline for Clarity

Alitheia AI tackles this problem with a structured, multi-stage pipeline. Instead of relying on a single, opaque model to declare what's "true," it deconstructs the problem into a series of transparent, logical steps: gather, group, objectify, score, and present.

<center>

<img src="static/imgs/objective_news_pipeline.png" alt="Pipeline for Alitheia AI." width="600">

</center>

This modular approach makes the entire process explainable. You can see which sources were used, how narratives were grouped, and what language was changed, giving you full transparency into the final output.

---

### Technical Deep Dive: System Architecture & Skills

The Alitheia AI pipeline is composed of several core modules, each designed to handle a specific part of the analysis process.

#### 1. Intelligence Gathering & Web Scraping
-   **Purpose:** To start, the I needed to gather a wide and diverse range of articles on a topic.
-   **Technology:** I built a resilient web scraper using `requests` and `BeautifulSoup`. It employs a dual-strategy approach: it first tries the more structured **Google News RSS feed** and falls back to **HTML scraping** if that fails. To extract clean article text from messy web pages, I integrated `trafilatura` and `newspaper3k`.
-   **Skills Demonstrated:**
    -   **Web Scraping & Data Extraction:** Building a robust tool that can handle different web formats and gracefully manage failures.
    -   **System Design:** Implementing a multi-strategy, fault-tolerant data retrieval system.

#### 2. Narrative Clustering with Unsupervised Learning
-   **Purpose:** I grouped sentences and articles by their core argument, to locate key narratives.
-   **Technology:** I used a sentence-embedding approach with `Sentence-Transformers` (`all-MiniLM-L6-v2`) to convert text into numerical vectors. To handle the unknown number of narratives, I used `HDBSCAN`, a density-based clustering algorithm. For performance, I used `UMAP` for dimensionality reduction before clustering. A significant part of this work involved hyperparameter tuning with **Optuna** to find the optimal settings for the clustering pipeline, which I logged and tracked.
-   **Skills Demonstrated:**
    -   **Unsupervised Machine Learning:** Applying density-based clustering (HDBSCAN) to a real-world NLP task.
    -   **NLP & Embeddings:** Using sentence embeddings to capture semantic meaning for clustering.
    -   **Hyperparameter Optimization:** Using `Optuna` to systematically find the best parameters for the clustering algorithm.

#### 3. Language Objectification & Bias Removal
-   **Purpose:** To get to the factual heart of a narrative, I create a system to identify and neutralize subjective, emotionally charged language.
-   **Technology:** I built a custom, rule-based objectification engine. It uses an ensemble of lexicon-based tools (`TextBlob`, `VaderSentiment`, `NLTK SentiWordNet`, and the MPQA subjectivity lexicon) to calculate an "objectivity score" for each word. For subjective words, it uses `WordNet` and other APIs to find more neutral synonyms and intelligently replaces them while trying to preserve grammatical correctness.
-   **Skills Demonstrated:**
    -   **Computational Linguistics:** Designing and implementing a rule-based system for language transformation.
    -   **Algorithm Design:** Creating a novel algorithm for scoring word objectivity and finding neutral alternatives.

#### 4. Dynamic Reliability Scoring
-   **Purpose:** I create a system to provide a transparent score for how trustworthy each narrative is.
-   **Technology:** I developed a multi-factor reliability score calculated from:
    1.  **Source Reputation:** Pulled from a pre-compiled dataset of source bias ratings.
    2.  **Source Diversity:** Narratives supported by more sources are scored higher.
    3.  **Objectivity:** The calculated objectivity score from the previous module.
    4.  **Recency & Temporal Cohesion:** How recent and chronologically consistent the reporting is.
-   **Skills Demonstrated:**
    -   **Data Analysis:** Combining multiple features into a single, meaningful score.
    -   **Feature Engineering:** Designing and implementing metrics for source diversity and temporal consistency.

#### 5. Summarization & User Interface
-   **Purpose:** The final step was to present all this complex information in a simple, intuitive way.
-   **Technology:** I built a multi-page web application using **Streamlit**. The app provides different views for analyzing articles, exploring the objectification engine, and more. For summaries, the pipeline can use fast extractive methods or a more powerful abstractive model (**Gemma**) for higher quality.
-   **Skills Demonstrated:**
    -   **Web Development:** Building a full-stack, interactive web application with `Streamlit`.
    -   **UI/UX Design:** Designing a user-friendly interface to present complex analytical results.

---

### Conclusion

Alitheia AI was a challenging but incredibly rewarding project. It was a deep dive into the practical application of NLP and ML to a real-world problem that I'm passionate about. By building this tool, I not only honed my technical skills but also developed a deeper appreciation for the complexities of language and information. My hope is that this project demonstrates a viable path toward creating AI tools that don't just give answers, but promote clarity and critical thinking. Cheers!

You can try out the live application here: **[https://objectivenews.streamlit.app/](https://objectivenews.streamlit.app/)**

---

### Skills Showcase
-   **Programming & Core Tech:**
    -   **Python:** Advanced proficiency in building multi-module applications, including OOP and data processing.
    -   **Git & GitHub:** Version control for project management.
-   **NLP & Machine Learning:**
    -   **Core NLP:** Text preprocessing, sentence splitting, POS tagging, lemmatization.
    -   **Libraries:** `spaCy`, `NLTK`, `Sentence-Transformers`, `scikit-learn`, `PyTorch`.
    -   **Unsupervised Learning:** HDBSCAN, UMAP, KMeans for narrative clustering.
    -   **Hyperparameter Tuning:** `Optuna` for optimizing the clustering pipeline.
-   **Data Science & Scientific Computing:**
    -   **Libraries:** `NumPy`, `Pandas`, `SciPy`.
    -   **Algorithm Design:** Developed custom algorithms for objectivity and reliability scoring.
-   **Web Scraping & Development:**
    -   **Scraping:** `requests`, `BeautifulSoup`, `trafilatura`, `newspaper3k`.
    -   **Web App:** `Streamlit` for building and deploying the interactive UI.