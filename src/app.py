from sitegen import Site, AnimationType, Alignment, Spacing, ButtonType, ObjectFit

def create_site():
    site = Site(
        source_dir="src", 
        content_dir="content", 
        output_dir="docs"
    )
    
    site.set_meta(
        site_title="Harry Yin's Portfolio",
        description="A showcase of my projects and thoughts :D",
        author="Harry Yin (Xild076)",
        keywords="portfolio, projects, blog, developer",
        base_url="https://xild076.github.io",
        main_nav_items=[
            {"text": "Home", "url": "/index.html"},
            {"text": "Projects", "url": "/projects.html"},
            {"text": "Blog", "url": "/blog.html"},
            {"text": "Cool Stuff", "url": "/cool_stuff.html"},
            {"text": "About", "url": "/about.html"},
        ]
    )
    
    return site

def build_index_page(site: Site):
    page = site.add_page("index", "Home")
    
    with page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg hero-section"):
        page.Write("Welcome to Harry Yin's Portfolio!", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--bs-body-color)")
        page.Write("A showcase of my projects and other random and cool stuff.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--bs-body-color)")
    
    with page.Container(css_class="my_lg"):
        page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2)
        
        with page.Container(css_class="text-center mb-4"):
            page.Write("Featured", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="40px")
        
        with page.Card(scroll_animation=True, scroll_animation_delay=0.2, css_class="hover-lift project-showcase"):
            with page.Columns(n=2, gap=Spacing.LG, spacing_before=Spacing.LG):
                with page.Container(css_class="project-card-media d-flex justify-content-center align-items-center"):
                    page.Image("/static/imgs/etsa_pipeline.png", alt="ETSA Pipeline", caption="ETSA Pipeline", width=None, height="240px", object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)

                with page.Container(css_class="d-flex flex-column justify-content-center"):
                    page.Markdown("### ETSA --- QC", align=Alignment.CENTER, spacing_after=Spacing.LG)
                    page.Markdown("Recently, I have been working on ETSA with Assistant Professor David Guy Brizan and Alex Pezcon (MAGICS Lab @ University of San Francisco). It is a unified, graph-centric pipeline for tracking how sentiment attaches to—and evolves around—entities and their aspects within any text. ETSA processes raw sentences one by one, builds a dynamic property graph of entities and descriptive phrases, scores sentiment at multiple levels, and propagates those scores through tunable, explainable message-passing. We are currently collecting data for the project: [You can participate in the survey here.](https://etsa---qc---survey.streamlit.app/) We would greatly appreciate your help in collecting data for this project. The survey is quick and easy, and it will help us a lot in our research. Thank you for your time and support!", align=Alignment.LEFT, spacing_after=Spacing.LG)
                    page.Button("View the project", link="projects/etsa_qc.html", style_type=ButtonType.PRIMARY)
        
        page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.LG, thickness=2)
        
        with page.Container(css_class="text-center"):
            page.Write("Explore More", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="28px", text_color="var(--heading-color)")
            with page.Columns(n=3, gap=Spacing.MD, spacing_before=Spacing.LG):
                with page.Card(css_class="text-center p-4"):
                    page.Write("Projects", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--accent-primary)")
                    page.Write("Research and development, from my older, more less developed projects to newer, SOTA projects.", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                    page.Button("View Projects", link="/projects.html", style_type=ButtonType.OUTLINE_PRIMARY)

                with page.Card(css_class="text-center p-4"):
                    page.Write("Blog", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--accent-primary)")
                    page.Write("Some thoughts by some guy on tech and philosophy", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                    page.Button("Read Blog", link="/blog.html", style_type=ButtonType.OUTLINE_PRIMARY)

                with page.Card(css_class="text-center p-4"):
                    page.Write("About", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--accent-primary)")
                    page.Write("Background, skills, and interests", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                    page.Button("About Me", link="/about.html", style_type=ButtonType.OUTLINE_PRIMARY)

def build_projects_page(site: Site):
    page = site.add_page("projects", "Projects")
    
    with page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.ZOOM_IN, css_class="rounded-lg hero-section"):
        page.Write("Projects", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="48px", text_color="var(--heading-color)")
        page.Write("AI research & development portfolio", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")
    
    with page.Container(css_class="my_lg"):
        page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2)
        page.Write("Research Projects", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size='32px', text_color="var(--accent-primary)")
        # ETSA
        with page.Card(spacing_after=Spacing.LG, css_class="project-showcase"):
            with page.Columns(n=2, gap=Spacing.LG):
                with page.Container(css_class="project-card-media d-flex justify-content-center align-items-center"):
                    page.Image("/static/imgs/etsa_pipeline.png", alt="ETSA Pipeline", height="220px", object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)
                with page.Container():
                    page.Write("Entity Targeted Sentiment Analysis", text_size="24px", text_color="var(--heading-color)", spacing_after=Spacing.SM)
                    page.Write("Advanced NLP pipeline combining graph-centric analysis with quantum-centric techniques for precise sentiment detection.", text_color="var(--text)", spacing_after=Spacing.MD)
                    page.Write("Technologies: Python, NetworkX, NLTK, Machine Learning", text_color="var(--text-secondary)", text_size="14px", spacing_after=Spacing.MD)
                    with page.Container(css_class="d-flex gap-2"):
                        page.Button("View Project", link="projects/etsa_qc.html", style_type=ButtonType.PRIMARY)
                        page.Button("GitHub", link="https://github.com/Xild076/ETSA--QC-", style_type=ButtonType.OUTLINE_PRIMARY)

        # LSD-AI
        with page.Card(spacing_after=Spacing.LG, css_class="project-showcase"):
            with page.Columns(n=2, gap=Spacing.LG):
                with page.Container(css_class="project-card-media d-flex justify-content-center align-items-center"):
                    page.Image("/static/imgs/lsd_ai.png", alt="LSD AI", height="220px", object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)
                with page.Container():
                    page.Write("LSD AI Framework", text_size="24px", text_color="var(--heading-color)", spacing_after=Spacing.SM)
                    page.Write("Experimental machine learning framework exploring novel approaches to artificial intelligence research and development.", text_color="var(--text)", spacing_after=Spacing.MD)
                    page.Write("Technologies: Python, TensorFlow, PyTorch, Research Methodologies", text_color="var(--text-secondary)", text_size="14px", spacing_after=Spacing.MD)
                    with page.Container(css_class="d-flex gap-2"):
                        page.Button("View Project", link="projects/lsdai.html", style_type=ButtonType.PRIMARY)
                        page.Button("GitHub", link="https://github.com/Xild076/LSD-AI", style_type=ButtonType.OUTLINE_PRIMARY)

        # Objective News
        with page.Card(spacing_after=Spacing.LG, css_class="project-showcase"):
            with page.Columns(n=2, gap=Spacing.LG):
                with page.Container(css_class="project-card-media d-flex justify-content-center align-items-center"):
                    page.Image("/static/imgs/objective_news.png", alt="Objective News", height="220px", object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)
                with page.Container():
                    page.Write("Alitheia AI (Objective News)", text_size="24px", text_color="var(--heading-color)", spacing_after=Spacing.SM)
                    page.Write("AI-powered news analysis system designed to identify and reduce bias in media reporting through advanced NLP techniques.", text_color="var(--text)", spacing_after=Spacing.MD)
                    page.Write("Technologies: Python, BERT, Transformers, News APIs", text_color="var(--text-secondary)", text_size="14px", spacing_after=Spacing.MD)
                    with page.Container(css_class="d-flex gap-2"):
                        page.Button("View Project", link="projects/objectivenews.html", style_type=ButtonType.PRIMARY)
                        page.Button("GitHub", link="https://github.com/Xild076/Objective-News", style_type=ButtonType.OUTLINE_PRIMARY)

        # Stock prediction
        with page.Card(spacing_after=Spacing.LG, css_class="project-showcase"):
            with page.Columns(n=2, gap=Spacing.LG):
                with page.Container(css_class="project-card-media d-flex justify-content-center align-items-center"):
                    page.Image("/static/imgs/stock_pred.png", alt="Stock Prediction", height="220px", object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)
                with page.Container():
                    page.Write("Stock Prediction with RL", text_size="24px", text_color="var(--heading-color)", spacing_after=Spacing.SM)
                    page.Write("Reinforcement learning approach to stock market prediction using deep Q-networks and market sentiment analysis.", text_color="var(--text)", spacing_after=Spacing.MD)
                    page.Write("Technologies: Python, PyTorch, RL Algorithms, Financial APIs", text_color="var(--text-secondary)", text_size="14px", spacing_after=Spacing.MD)
                    with page.Container(css_class="d-flex gap-2"):
                        page.Button("View Project", link="projects/stockpred.html", style_type=ButtonType.PRIMARY)
                        page.Button("GitHub", link="https://github.com/Xild076/StockPred", style_type=ButtonType.OUTLINE_PRIMARY)

def build_blog_page(site: Site):
    page = site.add_page("blog", "Blog")
    
    with page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg hero-section"):
        page.Write("Blog", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--heading-color)")
        page.Write("Thoughts and insights on technology, AI, and life", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")
    
    with page.Container(css_class="my_lg"):
        page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)
        page.Write("Latest Posts", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size='30px', text_color="var(--accent-primary)")
        page.BlockQuote("Some random words by some random guy.", author="Harry Yin", align=Alignment.CENTER, spacing_after=Spacing.LG, animation=AnimationType.FADE_IN)
        
        with page.Container(css_class="row"):
            all_blog_posts = [
                {"slug": "writing_fun", "title": "Misc - Short Story: The Frog Who Cried Rain", "file": "blogs/writing_fun.md", "author": "Harry Yin", "date": "2025-09-30"},
                {"slug": "ai_ethics", "title": "Programming - My thoughts on AI ethics and how that ties into Fatalism", "file": "blogs/ai_ethics.md", "author": "Harry Yin", "date": "2025-08-22"},
                {"slug": "local_minima", "title": "Programming - Funny ways to describe the local minima to an edgy teen", "file": "blogs/local_minima.md", "author": "Harry Yin", "date": "2025-08-10"},
                {"slug": "revisit", "title": "Programming - Revisiting old projects", "file": "blogs/revisiting_projects.md", "author": "Harry Yin", "date": "2025-07-25"},
                {"slug": "on_mortality", "title": "Misc - Scary Moment", "file": "blogs/on_mortality.md", "author": "Harry Yin", "date": "2025-06-20"},
                {"slug": "heuristic_eq", "title": "Programming - Finding Heuristic Equations", "file": "blogs/heuristic_eq.md", "author": "Harry Yin", "date": "2025-05-31"},
                {"slug": "sentiment_target", "title": "Programming - Entity Sentiment Targeting", "file": "blogs/sentiment_target.md", "author": "Harry Yin", "date": "2025-04-04"},
                {"slug": "question", "title": "Misc - The Question We Forget", "file": "blogs/question_forget.md", "author": "Harry Yin", "date": "2025-03-24"},
                {"slug": "polarization", "title": "Programming - Polarization in Modern Media", "file": "blogs/polarization.md", "author": "Harry Yin", "date": "2025-03-20"},
                {"slug": "ai_vs_algorithm", "title": "Programming - Stockfish vs AlphaZero, Algorithm vs AI", "file": "blogs/ai_algorithm.md", "author": "Harry Yin", "date": "2025-03-13"},
                {"slug": "bias_types", "title": "Programming - Types of Bias", "file": "blogs/modern_media.md", "author": "Harry Yin", "date": "2025-03-12"},
                {"slug": "fatalism", "title": "Misc - My Thoughts on Fatalism", "file": "blogs/fatalism.md", "author": "Harry Yin", "date": "2025-03-11"},
                {"slug": "debias", "title": "Programming - Removing Bias from Text", "file": "blogs/bias_removal.md", "author": "Harry Yin", "date": "2025-03-10"},
                {"slug": "fake_news", "title": "Programming - Methods to Detect Fake News", "file": "blogs/fake_news.md", "author": "Harry Yin", "date": "2025-03-09"},
                {"slug": "self_atten_blog", "title": "Programming - Self Attention in Textual Clustering", "file": "blogs/self_atten_blog.md", "author": "Harry Yin", "date": "2025-03-08"},
                {"slug": "likeable_character", "title": "Misc - What makes a likeable character?", "file": "blogs/likeable_character.md", "author": "Harry Yin", "date": "2025-03-08"},
                {"slug": "hello_blog", "title": "Hello Blog", "file": "blogs/hello_blog.md", "author": "Harry Yin", "date": "2025-03-07"},
            ]
            # Sort by date descending
            all_blog_posts.sort(key=lambda x: x["date"], reverse=True)
            for post in all_blog_posts:
                with page.Container(css_class="col-md-6 mb-4"):
                    with page.Card(css_class="h-100 hover-lift"):
                        page.Write(post["title"], text_size="20px", text_color="var(--heading-color)", spacing_after=Spacing.SM)
                        # Optionally show date and author
                        page.Write(f"{post['author']} — {post['date']}", text_color="var(--text-secondary)", text_size="13px", spacing_after=Spacing.SM)
                        # Short description: use first sentence of the markdown file if desired, or just the title
                        page.Button("Read More", link=f"blog/{post['slug']}.html", style_type=ButtonType.PRIMARY)

def build_cool_stuff_page(site: Site):
    page = site.add_page("cool_stuff", "Cool Stuff")
    
    with page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg hero-section"):
        page.Write("Cool Stuff", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--heading-color)")
        page.Write("Experimental projects and fun explorations", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")
    
    with page.Container(css_class="my_lg"):
        page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)
        
        page.Widget(
            "APUSH Timeline",
            "Timeline visualization from my AP US History course.",
            link="/apush_timeline.html",
            image_url="/static/imgs/placeholder.png",
            animation=AnimationType.FADE_IN_LEFT,
            scroll_animation=True,
            scroll_animation_delay=0.15
        )
        
        page.Widget(
            "CSP Project",
            "My Computer Science Principles final project showcase.",
            link="/csp.html",
            image_url="/static/imgs/placeholder.png",
            animation=AnimationType.FADE_IN_LEFT,
            scroll_animation=True,
            scroll_animation_delay=0.15
        )

def add_html_pages(site: Site):
    import os
    static_dir = "static"
    content_dir = "content"
    docs_dir = "docs"
    
    apush_rel = "cool_stuff/apush_timeline.html"
    if os.path.exists(os.path.join(content_dir, apush_rel)):
        site.add_html_file_page("apush_timeline", "APUSH Timeline", apush_rel)
    else:
        apush_page = site.add_page("apush_timeline", "APUSH Timeline")
        apush_page.Write("APUSH Timeline", align=Alignment.CENTER, text_size="40px", spacing_after=Spacing.LG)
        apush_page.Write("Timeline content coming soon!", align=Alignment.CENTER, spacing_after=Spacing.LG)

    graph_demo_rel = "projects/etsa/graph_sentiment_analysis.html"
    if os.path.exists(os.path.join(content_dir, graph_demo_rel)):
        site.add_html_file_page("graph_sentiment_analysis", "Graph Sentiment Analysis", graph_demo_rel)

    """csp_rel = "cool_stuff/csp.html"
    if os.path.exists(os.path.join(content_dir, csp_rel)):
        site.add_html_file_page("csp", "CSP Project", csp_rel)
    else:
        csp_page = site.add_page("csp", "CSP Project")
        csp_page.Write("CSP Project", align=Alignment.CENTER, text_size="40px", spacing_after=Spacing.LG)
        csp_page.Write("Computer Science Principles project details coming soon!", align=Alignment.CENTER, spacing_after=Spacing.LG)"""


def build_about_page(site:Site):
    page = site.add_page("about", "About Me")
    
    with page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg hero-section"):
        page.Write("About Me", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="42px", text_color="var(--heading-color)")
        page.Write("Getting to know the person behind the code", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")
    
    with page.Container(css_class="my_lg"):
        with page.Columns(n=2, gap=Spacing.XL, spacing_before=Spacing.LG):
            with page.Container(css_class="d-flex justify-content-center align-items-center"):
                page.Image("/static/imgs/placeholder.png", alt="Harry Yin", 
                         caption="Harry Yin - Developer & Researcher", 
                         width="350px", height="350px", object_fit=ObjectFit.COVER, 
                         align=Alignment.CENTER)
            
            with page.Container(css_class="d-flex flex-column justify-content-center"):
                page.Markdown("""Hello, I'm Harry, I'm gonna finish this bit soon!""", align=Alignment.LEFT)
                
                with page.Container(css_class="d-flex gap-2 mt-3"):
                    page.Button("EXEC PROJECTS", link="/projects.html", style_type=ButtonType.PRIMARY)
                    page.Button("READ BLOG", link="/blog.html", style_type=ButtonType.OUTLINE_PRIMARY)

def add_project_pages(site : Site):
    site.add_project_page(
        'etsa_qc',
        'ETSA --- QC',
        project_readme_file='projects/etsa/etsa_qc_intro.md',
        timeline_events=[
            {"time": "2025-03-17", "description": "Began project ETSA --- QC"},
            {"time": "2025-04-11", "description": "Joined the MAGICS Lab at USF"},
        ],
        technologies_used=[
            "Python 3.x for backend processing",
            "Streamlit for hosting",
            "SpaCy for NLP",
            "REBEL for entity resolution",
            "NetworkX for graph processing",
            "Hugging Face Transformers for state-of-the-art models",
            "Maverick for coreference resolution",
            "Github for development",
            "Pandas for data manipulation",
            "Numpy for numerical operations",
            "Matplotlib for plotting"
        ],
        project_documents=[
            {"title": "Summary of Novelty", "url": "projects/etsa/A Summary of Novelty.md"},
            {"title": "Survey Proposal", "url": "projects/etsa/ABSA Survey Proposal.md"},
            {"title": "ETSA --- QC Survey", "url": "https://etsa-survey.streamlit.app/"},
            {"title": "Graph Demo", "url": "projects/etsa/graph_sentiment_analysis.html"}
        ],
        meta_info={"author": "Xild076", "project_id": "ETSA-QC"}
    )
    
    site.add_project_page(
        'lsdai',
        'L&SD AI (Speech and Debate AI)',
        project_readme_file='projects/lsdai/lsd_ai_intro.md',
        timeline_events=[
            {"time": "2024-06-24", "description": "Began project L&SD AI"},
            {"time": "2024-08-11", "description": "Completed the first beta version of L&SD AI"},
            {"time": "2024-08-19", "description": "Began reworking and updating the project"},
            {"time": "2024-09-01", "description": "Completed the second beta of L&SD AI"},
            {"time": "2024-10-27", "description": "Migrated L&SD AI from an app to Streamlit"}
        ],
        technologies_used=[
            "Python 3.x for backend processing",
            "Streamlit for hosting",
            "OpenAI API keys for audio/content analysis",
            "Kaggle for training data",
            "Github for development"
        ],
        project_documents=[
            {"title": "LS&DAI README", "url": "projects/lsdai/lsd_ai_readme.md"}
        ],
        meta_info={"author": "Xild076", "project_id": "LS&DAI"}
    )
    
    site.add_project_page(
        'objectivenews',
        'Alitheia AI (Objective News)',
        project_readme_file='projects/objective_news/objective_news_intro.md',
        timeline_events=[
            {"time": "2024-10-01", "description": "Began project Objective News"},
            {"time": "2024-12-15", "description": "Completed the first beta version of Objective News"},
            {"time": "2025-01-02", "description": "Completed the second beta version of Objective News"},
            {"time": "2025-02-09", "description": "Completed official proposal paper for full version of Objective News"},
            {"time": "2025-03-06", "description": "Renamed project to Alitheia AI (Greek for 'truth')"},
            {"time": "2025-07-25", "description": "Massive rework including but not limited to: improved clustering algorithms, hyperparameter tuning, self-attention model trained with meta-learning, etc... (see project page for more details)"}
        ],
        technologies_used=[
            "Python 3.x for backend processing",
            "Streamlit for hosting",
            "Stanza for NLP",
            "Hugging Face Transformers for state-of-the-art models",
            "Scikit-learn for clustering",
            "BeautifulSoup for web scraping",
            "Requests for HTTP requests",
            "Github for development"
        ],
        project_documents=[
            {"title": "Beta Paper", "url": "projects/objective_news/paper_vbeta.md"},
            {"title": "Official Proposal", "url": "projects/objective_news/Proposal—Objective News.pdf"}
        ],
        meta_info={"author": "Xild076", "project_id": "ObjectiveNews"}
    )
    
    site.add_project_page(
        'stockpred',
        'Polystock AI (Stock Prediction)',
        project_readme_file='projects/stockpred/stock_pred_intro.md',
        timeline_events=[
            {"time": "2023-06-11", "description": "Began project Polystock AI"},
            {"time": "2023-10-15", "description": "Completed the first beta version of Polystock AI"},
            {"time": "2023-11-20", "description": "Wrote the first paper on Polystock AI"},
            {"time": "2024-09-03", "description": "Began to rework the project to use more advanced techniques"},
            {"time": "2024-11-10", "description": "Completed the second beta version of Polystock AI with full functionality and partially trained models"},
            {"time": "2025-07-06", "description": "Updated Polystock AI to use a different data source, better data storage, and a more advanced model architecture"}
        ],
        technologies_used=[
            "Python 3.x for backend processing",
            "FRED API for data",
            "Streamlit for hosting",
            "Requests for HTTP requests",
            "Yfinance for stock data",
            "Pandas for data manipulation",
            "Numpy for numerical operations",
            "Matplotlib for plotting",
            "PyTorch for ML development",
            "Github for development"
        ],
        project_documents=[
            {"title": "Beta Paper", "url": "projects/stockpred/RL_for_Stocks.pdf"}
        ],
        meta_info={"author": "Xild076", "project_id": "StockPred"}
    )

def add_blog_posts(site):
    blog_posts = [
        {"slug": "writing_fun", "title": "Misc - Short Story: The Frog Who Cried Rain", "file": "blogs/writing_fun.md", "author": "Harry Yin", "date": "2025-09-30"},
        {"slug": "ai_ethics", "title": "Programming - My thoughts on AI ethics and how that ties into Fatalism", "file": "blogs/ai_ethics.md", "author": "Harry Yin", "date": "2025-08-22"},
        {"slug": "local_minima", "title": "Programming - Funny ways to describe the local minima to an edgy teen", "file": "blogs/local_minima.md", "author": "Harry Yin", "date": "2025-08-10"},
        {"slug": "revisit", "title": "Programming - Revisiting old projects", "file": "blogs/revisiting_projects.md", "author": "Harry Yin", "date": "2025-07-25"},
        {"slug": "on_mortality", "title": "Misc - Scary Moment", "file": "blogs/on_mortality.md", "author": "Harry Yin", "date": "2025-06-20"},
        {"slug": "heuristic_eq", "title": "Programming - Finding Heuristic Equations", "file": "blogs/heuristic_eq.md", "author": "Harry Yin", "date": "2025-05-31"},
        {"slug": "sentiment_target", "title": "Programming - Entity Sentiment Targeting", "file": "blogs/sentiment_target.md", "author": "Harry Yin", "date": "2025-04-04"},
        {"slug": "question", "title": "Misc - The Question We Forget", "file": "blogs/question_forget.md", "author": "Harry Yin", "date": "2025-03-24"},
        {"slug": "polarization", "title": "Programming - Polarization in Modern Media", "file": "blogs/polarization.md", "author": "Harry Yin", "date": "2025-03-20"},
        {"slug": "ai_vs_algorithm", "title": "Programming - Stockfish vs AlphaZero, Algorithm vs AI", "file": "blogs/ai_algorithm.md", "author": "Harry Yin", "date": "2025-03-13"},
        {"slug": "bias_types", "title": "Programming - Types of Bias", "file": "blogs/modern_media.md", "author": "Harry Yin", "date": "2025-03-12"},
        {"slug": "fatalism", "title": "Misc - My Thoughts on Fatalism", "file": "blogs/fatalism.md", "author": "Harry Yin", "date": "2025-03-11"},
        {"slug": "debias", "title": "Programming - Removing Bias from Text", "file": "blogs/bias_removal.md", "author": "Harry Yin", "date": "2025-03-10"},
        {"slug": "fake_news", "title": "Programming - Methods to Detect Fake News", "file": "blogs/fake_news.md", "author": "Harry Yin", "date": "2025-03-09"},
        {"slug": "self_atten_blog", "title": "Programming - Self Attention in Textual Clustering", "file": "blogs/self_atten_blog.md", "author": "Harry Yin", "date": "2025-03-08"},
        {"slug": "likeable_character", "title": "Misc - What makes a likeable character?", "file": "blogs/likeable_character.md", "author": "Harry Yin", "date": "2025-03-08"},
        {"slug": "hello_blog", "title": "Hello Blog", "file": "blogs/hello_blog.md", "author": "Harry Yin", "date": "2025-03-07"},
    ]

    for post in blog_posts:
        site.add_blog_post(
            post['slug'],
            post['title'],
            post['file'],
            author=post.get('author'),
            date=post.get('date')
        )

def main():
    print("Building site...")
    
    site = create_site()
    
    build_index_page(site)
    build_projects_page(site)
    build_blog_page(site)
    build_cool_stuff_page(site)
    build_about_page(site)
    
    add_project_pages(site)
    add_blog_posts(site)
    add_html_pages(site)
    
    site.build()
    print("Site built successfully!")

if __name__ == "__main__":
    main()