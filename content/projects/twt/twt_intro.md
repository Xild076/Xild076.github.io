<center>

### **Thinking Without Thinking: An Explainable Agentic AI Pipeline**

</center>

**Project Summary:** "Thinking Without Thinking" started as a fun personal project to see if I could create a more structured and transparent "thought process" for an AI using just prompt engineering. It's an agentic reasoning pipeline that deconstructs user query into steps that integrate custom tools to generate the best possible answer.

**My Role:** I was the sole developer and designed and built the entire system.

---

### The Problem: Costly LLMs

While modern LLMs are powerful, they are extremely massive and costly. I decided to take a shot to see if I could use a cheap and free model (Gemma 27B) to match the quality of a model 25x its size (something like Deepseek v3.1, the high quality model of which I knew the parameter size).

### The Solution: Multistage prompting

Instead of one big "thinking" step, this project breaks down reasoning into a predictable, four-phase process inspired by how a person might tackle a problem: plan, gather information, synthesize, and refine. Each phase is handled by specialized prompts, creating an pseudo "chain of reasoning" that is both easy to follow and robust. 
---

### Technical Details: System Architecture & Skills

The pipeline is orchestrated by a central `ThinkingPipeline` class that dynamically routes a user's query through a sequence of "blocks."

#### 1. Phase 1: Meta-Reasoning (Planning & Routing)
-   **Purpose:** Before doing any work, the system first creates a strategy to answer the prompt. Then, another prompt has the model create a machine-readable tool usage plan to integrate the necessary context into the system.
-   **Technology:** This is powered entirely by a series of chained prompts sent to the **Google Gemma 27B** model.
-   **Skills Demonstrated:**
    -   **AI & LLM Engineering:** Advanced prompt engineering, designing self-correction loops, and structured data extraction from model outputs.
    -   **System Design:** Architecting a meta-reasoning layer that improves the reliability of downstream tasks.

#### 2. Phase 2: Tool Execution
-   **Purpose:** The pipeline executes the planned blocks in sequence, using the output of one block as potential input for the next. This allows the system to gather and process information from multiple sources.
-   **Technology:**
    -   **Code Tool:** Executes Python code in a sandboxed environment using the `subprocess` module. It automatically captures stdout, handles errors, and uses a custom `matplotlib` hook to save any generated plots to temporary files.
    -   **Internet Tool:** Performs live web searches through HTML scraping with `requests` and `BeautifulSoup` if the feed fails. Article content is then extracted using `trafilatura` and `newspaper3k`.
    -   **Creative Tool:** Uses a high-temperature LLM call to brainstorm a diverse set of ideas and then uses a separate, low-temperature evaluation prompt to select the most promising one.
-   **Skills Demonstrated:**
    -   **Software Engineering:** Building sandboxed execution environments and creating robust, fault-tolerant tool integrations.
    -   **Web Scraping & Data Extraction:** Combining multiple libraries to build a resilient web scraping tool that handles failures gracefully.
    -   **API Integration:** Interfacing with external services and handling their outputs within a unified pipeline.

#### 3. Phase 3: Synthesis & Self-Correction
-   **Purpose:** This module gathers all the collected information (code outputs, web summaries, brainstormed ideas) and synthesizes a comprehensive, human-readable answer. This initial draft is then "scored" by another LLM call, which provides feedback, and a final "improver" prompt refines the answer based on this feedback.
-   **Technology:** This phase relies on prompt engineering that instruct the LLM to consolidate context, generate a draft, critique it based on a rubric (clarity, logic, actionability), and then produce a final, polished version.
-   **Skills Demonstrated:**
    -   **Prompt Engineering:** Designing a multi-step editorial review process using LLMs.
    -   **Content Synthesis:** Building prompts that can effectively synthesize information from disparate sources into a coherent narrative.

#### 4. Phase 4: Transparent User Interface
-   **Purpose:** The entire process is demonstrated through an interactive web application, allowing a user to see the final answer and inspect every step the agent took to get there.
-   **Technology:** I built the UI using Streamlit.
-   **Skills Demonstrated:**
    -   **Web Development:** Creating a full-stack, interactive web application with `Streamlit`.
    -   **UI/UX Design:** Designing an intuitive interface for visualizing complex, multi-step processes.
    -   **Data Visualization:** Presenting logs, code, and structured JSON in an easily digestible format.

---

### Results & Impact

The result is an AI that does what every math teacher wants you to do: show its work. 

-   **Reliable Tool Use:** The system can successfully perform complex tasks like searching for recent news, writing Python code to analyze it, generating a plot, and embedding that plot into a final summary, all within a single query.
-   **Full Transparency:** The Streamlit UI provides complete insight into the agent's reasoning, making it a powerful tool for understanding how these models "think."

---

### Skills Showcase

-   **Programming & Core Tech:**
    -   **Python:** Advanced proficiency, including object-oriented design, `subprocess` management, and package development.
    -   **Git & GitHub:** Version control and project management.
-   **AI & Large Language Models (LLMs):**
    -   **Prompt Engineering:** Designing complex, chained prompts for planning, execution, self-critique, and synthesis with Google Gemma.
    -   **Agentic AI Design:** Architecting a multi-step reasoning pipeline with tool-use and self-correction loops.
-   **Web Scraping & Data Extraction:**
    -   **Libraries:** `requests`, `BeautifulSoup`, `trafilatura`, `newspaper3k`.
    -   **Strategy:** Implemented a robust dual-strategy (RSS + HTML) approach for data retrieval.
-   **Web & Visualization:**
    -   **Streamlit:** Developed a full-stack, interactive web application for demonstrating the pipeline.
    -   **PDF Generation:** `ReportLab` and `PyPDF2` for creating and reading PDF documents.
    -   **Data Visualization:** `Matplotlib` for generating plots within the sandboxed code environment.
-   **Software Engineering:**
    -   **System Design:** Architecting a modular, block-based system for easy extension.
    -   **API Integration:** Building resilient modules with caching, error handling, and rate limiting.