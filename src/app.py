import os
from urllib.parse import urljoin
from sitegen import Site, Page, Alignment, Spacing, ButtonType, AnimationType, ColorTheme, ObjectFit, InputType, FlexDirection, FlexWrap, build_tab_content

main_nav_items = [
    {"text":"Home", "url": "/index.html"},
    {"text":"Projects", "url": "/projects.html"},
    {"text":"Blog", "url": "/blog.html"},
    {"text":"Cool Stuff", "url": "/cool_stuff.html"},
    {"text":"About", "url": "/about.html"},
]

site = Site(source_dir="src", output_dir="docs")
site.set_meta(
    site_title="Harry Yin's Portfolio",
    description="A showcase of my projects and thoughts :D",
    author="Harry Yin (Xild076)",
    keywords="portfolio, projects, blog, developer",
    base_url="https://xild076.github.io",
    main_nav_items=main_nav_items
)

index_page = site.add_page("index", "Home")

with index_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg"):
        index_page.Write("Welcome to Harry Yin's Portfolio!", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--bs-body-color)")
        index_page.Write("A showcase of my projects and other random and cool stuff.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--bs-body-color)")

with index_page.Container(css_class="my_lg"):
    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    index_page.Write("Featured", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="40px")
    with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
        with index_page.Columns(n=2, gap=Spacing.LG, spacing_before=Spacing.LG):
            with index_page.Container(css_class="rounded-lg"):
                index_page.Image("/static/imgs/placeholder.png", alt="ETSA Pipeline", caption="ETSA Pipeline", width="300px", height="300px", object_fit=ObjectFit.COVER, align=Alignment.CENTER)

            with index_page.Container(css_class="rounded-lg"):
                index_page.Markdown("### ETSA --- QC", align=Alignment.CENTER, spacing_after=Spacing.LG)
                index_page.Markdown("Recently, I have been working on ETSA with Assistant Professor David Guy Brizan and Alex Pezcon (MAGICS Lab @ University of San Francisco). It is a unified, graph-centric pipeline for tracking how sentiment attaches to—and evolves around—entities and their aspects within any text. ETSA processes raw sentences one by one, builds a dynamic property graph of entities and descriptive phrases, scores sentiment at multiple levels, and propagates those scores through tunable, explainable message-passing. We are currently collecting data for the project: [You can participate in the survey here.](https://etsa---qc---survey.streamlit.app/) We would greatly appreciate your help in collecting data for this project. The survey is quick and easy, and it will help us a lot in our research. Thank you for your time and support!", align=Alignment.LEFT, spacing_after=Spacing.LG)
                index_page.Button("View the project", link="projects/etsa_qc.html", style_type=ButtonType.PRIMARY, animation=AnimationType.PULSE, scroll_animation=True, scroll_animation_delay=0.15)

    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    with index_page.Columns(2):
        with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
            index_page.Markdown("### Latest Project:", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Widget("Alitheia AI (Objective News)", "A project aimed towards locating and presenting the most objective news possible.", link="projects/objectivenews.html", image_url="/static/imgs/objective_news.png", scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Button("View all projects", link="/projects.html", style_type=ButtonType.PRIMARY, animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15)

        with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
            index_page.Markdown("### Latest Blog Post:", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Widget("Revisiting Projects", "Explaining revisiting some projects.", link="blog/revisit.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Button("View all blog posts", link="/blog.html", style_type=ButtonType.PRIMARY, animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15)

projects_page = site.add_page("projects", "Projects")

site.add_project_page(
    "etsa_qc",
    "ETSA --- QC",
    project_readme_file="projects/etsa/etsa_qc_intro.md",
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
    "objectivenews",
    "Alitheia AI (Objective News)",
    project_readme_file="projects/objective_news/objective_news_intro.md",
    timeline_events=[
        {"time": "2024-10-01", "description": "Began project Objective News"},
        {"time": "2024-12-15", "description": "Completed the first beta version of Objective News"},
        {"time": "2025-01-02", "description": "Completed the second beta version of Objective News"},
        {"time": "2025-02-09", "description": "Completed official proposal paper for full version of Objective News"},
        {"time": "2025-03-06", "description": "Renamed project to Alitheia AI (Greek for 'truth')"},
        {"time": "2025-07-25", "description": "Massive rework including but not limited to: improved clustering algorithms, hyperparameter tuning, self-attention model trained with meta-learning, etc... (see project page for more details)"},
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
    "stockpred",
    "Polystock AI (Stock Prediction)",
    project_readme_file="projects/stockpred/stock_pred_intro.md",
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

site.add_project_page(
    "lsdai",
    "L&SD AI (Speech and Debate AI)",
    project_readme_file="projects/lsdai/lsd_ai_intro.md",
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
    "aicat",
    "AI Catalog (Basic PyTorch recreation)",
    project_readme_file="projects/catalog/ai_catalog_intro.md",
    timeline_events=[
        {"time": "2024-02-09", "description": "Began project AI Catalog"},
        {"time": "2024-04-05", "description": "Finalized first version of VPG with only numpy"},
        {"time": "2024-05-03", "description": "Began creation of PyTorch structure with Karpathy's Micrograd as reference"},
        {"time": "2024-07-10", "description": "Completed first basic version of Micrograd"}
    ],
    technologies_used=[
        "Python 3.x for backend processing",
        "Numpy for numerical processing",
        "Github for development"
    ],
    project_documents=[],
    meta_info={"author": "Xild076", "project_id": "AICatalogue"}
)

with projects_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.ZOOM_IN, css_class="rounded-lg"):
    projects_page.Write("Projects", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--bs-body-color)")
    projects_page.Write("A showcase of my projects.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--bs-body-color)")

with projects_page.Container(css_class="my_lg"):
    projects_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    projects_page.Write("Latest Projects:", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size='30px')
    projects_page.Widget("ETSA --- QC", "A unified, graph-centric pipeline for tracking how sentiment attaches to and evolves around entities and their aspects within any text.", link="projects/etsa_qc.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    projects_page.Widget("Alitheia AI (Objective News)", "A project aimed towards locating and presenting the most objective news possible.", link="projects/objectivenews.html", image_url="/static/imgs/objective_news.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    projects_page.Widget("Polystock AI", "A deep learning system for forecasting stock market behavior using real-time financial data.", link="projects/stockpred.html", image_url="/static/imgs/stock_pred.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    projects_page.Widget("LSD AI", "An AI system for analyzing speech and debate content using NLP, audio analysis, and content tracking.", link="projects/lsdai.html", image_url="/static/imgs/lsd_ai.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    projects_page.Widget("ML Catalog", "A project that aims to look into the basic of ML", link="projects/aicat.html", image_url="/static/imgs/ai_cat.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)

blog_page = site.add_page("blog", "Blog")

site.add_blog_post("revisit", "Programming - Revisiting old projects", "blogs/revisiting_projects.md", author="Harry Yin", date="2025-07-25")
site.add_blog_post("on_mortality", "Misc - Scary Moment", "blogs/on_mortality.md", author="Harry Yin", date="2025-06-20")
site.add_blog_post("heuristic_eq", "Programming - Finding Heuristic Equations", "blogs/heuristic_eq.md", author="Harry Yin", date="2025-05-31")
site.add_blog_post("sentiment_target", "Programming - Entity Sentiment Targeting", "blogs/sentiment_target.md", author="Harry Yin", date="2025-04-04")
site.add_blog_post("question", "Misc - The Question We Forget", "blogs/question_forget.md", author="Harry Yin", date="2025-03-24")
site.add_blog_post("polarization", "Programming - Polarization in Modern Media", "blogs/polarization.md", author="Harry Yin", date="2025-03-20")
site.add_blog_post("ai_vs_algorithm", "Programming - Stockfish vs AlphaZero, Algorithm vs AI", "blogs/ai_algorithm.md", author="Harry Yin", date="2025-03-13")
site.add_blog_post("bias_types", "Programming - Types of Bias", "blogs/bias_types.md", author="Harry Yin", date="2025-03-12")
site.add_blog_post("fatalism", "Misc - My Thoughts on Fatalism", "blogs/fatalism.md", author="Harry Yin", date="2025-03-11")
site.add_blog_post("debias", "Programming - Removing Bias from Text", "blogs/debias.md", author="Harry Yin", date="2025-03-10")
site.add_blog_post("fake_news", "Programming - Methods to Detect Fake News", "blogs/fake_news.md", author="Harry Yin", date="2025-03-09")
site.add_blog_post("self_atten_blog", "Programming - Self Attention in Textual Clustering", "blogs/self_atten_blog.md", author="Harry Yin", date="2025-03-08")
site.add_blog_post("likeable_character", "Misc - What makes a likeable character?", "blogs/likeable_character.md", author="Harry Yin", date="2025-03-08")
site.add_blog_post("hello_blog", "Hello Blog", "blogs/hello_blog.md", author="Harry Yin", date="2025-03-07")

with blog_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg"):
    blog_page.Write("Blogs", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--bs-body-color)")
    blog_page.Write("Random thoughts of mine on a couple of different things.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--bs-body-color)")

with blog_page.Container(css_class="my_lg"):
    blog_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    blog_page.Write("Latest Blog Posts:", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size='30px')
    blog_page.BlockQuote("Some random words by some random guy.", author="me, 2025", align=Alignment.CENTER, spacing_after=Spacing.LG, animation=AnimationType.FADE_IN)
    blog_page.Widget("Revisiting Old Projects", "A blog post about revisiting old projects and the importance of doing so.", link="blog/revisit.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Scary Moment", "Describing a scary moment in my life.", link="blog/on_mortality.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Finding Heuristic Equations", "This is a blog post on finding heuristic equations.", link="blog/heuristic_eq.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Entity Sentiment Targetting", "This is a blog post on entity sentiment targetting.", link="blog/sentiment_target.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("The Question We Forget", "This is a blog post on the question we forget.", link="blog/question.html", image_url="/static/imgs/question.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Polarization in Modern Media", "This is a blog post on my thoughts on the polarization of modern media.", link="blog/polarization.html", image_url="/static/imgs/polarization.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Stockfish vs AlphaZero, Algorithm vs AI", "This is a blog post on the differences between algorithms and AI.", link="blog/ai_vs_algorithm.html", image_url="/static/imgs/ai_vs_algorithm.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Types of Bias", "This is a blog post on my thoughts on the types of biases.", link="blog/bias_types.html", image_url="/static/imgs/bias_types.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("My Thoughts on Fatalism", "This is a blog post on my thoughts about fatalism.", link="blog/fatalism.html", image_url="/static/imgs/fatalism.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Removing Bias from Text", "This is a blog post about methods to algorithmically remove bias from text.", link="blog/debias.html", image_url="/static/imgs/bias_removal.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Methods to Detect Fake News", "This is a blog post about methods to detect fake news.", link="blog/fake_news.html", image_url="/static/imgs/fake_news.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Self Attention in Textual Clustering", "This is a blog post about self attention in textual clustering.", link="blog/self_atten_blog.html", image_url="/static/imgs/self_atten.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("What makes a likeable character?", "This is a blog post about my thoughs on what makes a likeable character.", link="blog/likeable_character.html", image_url="/static/imgs/likeable_character.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    blog_page.Widget("Test Blog", "This is a test blog post with a bunch of internal markdown tests", link="blog/first_blog.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)

cool_stuff_page = site.add_page("cool_stuff", "Cool Stuff")

site.add_html_file_page("apush_timeline", "APUSH Timeline", "apush_timeline.html")

with cool_stuff_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.FADE_IN, css_class="rounded-lg"):
    cool_stuff_page.Write("Cool Stuff", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--bs-body-color)")
    cool_stuff_page.Write("Random cool stuff.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--bs-body-color)")

with cool_stuff_page.Container(css_class="my_lg"):
    cool_stuff_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    cool_stuff_page.Widget("APUSH Timeline", "Just finished the APUSH test, wanted to post this thing here.", link="/apush_timeline.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    cool_stuff_page.Widget("CSP Study Guide", "A study guide for the CSP test.", link="csp.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)
    cool_stuff_page.Widget("Graph Demo", "A demo showcasing the ETSA graph capabilities.", link="/projects/etsa_qc/graph_sentiment_analysis.html", image_url="/static/imgs/placeholder.png", animation=AnimationType.FADE_IN_LEFT, scroll_animation=True, scroll_animation_delay=0.15)

about_page = site.add_page("about", "About Me")

with about_page.Container(css_class="my_lg"):
    with about_page.Columns(n=2, gap=Spacing.LG, spacing_before=Spacing.LG):
        with about_page.Container(css_class="rounded-lg"):
            about_page.Image("/static/imgs/placeholder.png", alt="Placeholder 1", caption="A placeholder image, no image of me yet :D.", width="300px", height="300px", object_fit=ObjectFit.COVER, align=Alignment.CENTER)
        with about_page.Container(css_class="rounded-lg"):
            about_page.Markdown("""Hi, I'm **Harry**, an **aspiring data scientist** and **AI** *(the behind the scenes type of AI)* **enthusiast**! I'm very interested implementing unique applications of AI in many different types of projects.

I'm currently a **junior at Leland High School** and have done a couple of research and development projects using AI, some of which include Stock Prediction, an AI Speech and Debate Coach, and a news objectifier. I have worked with **python for over 8 years** and have worked in **AI development for over 3 years**. I am good working with torch, sklearn, and numpy, the three big packages of AI development in python.

The two main reasons I develop AI systems are for **1.** a possible future employment prospect and **2.** for fun! I find the problem-solving aspect of AI development and programming overall fascinating, and it's always satisfying to come up with cool solutions to unique problems. 

I believe, on a more philosophical level, that AI systems and technology in general should, ideally, be used as **tools for the benefit of everyone**. While that is impossible, I aim to make my projects accessible and useful for everyone across the globe.

Outside of all this, I love reading! I especially love reading fantasy/scifi novels. While I haven't picked up any fun books recently due to a variety of reasons, some titles I would highly recommend are: 

- The Three Body Problem *(the second book in particular)*

- Artemis Fowl *(more of a childhood classic, up to the fifth book)*

I also enjoy playing Hollow Knight, swimming, and last but not least: sleeping! My favorite drink is apple juice, my favorite color oscillates between green and black, and my favorite animal are cats!""")

with about_page.Container(css_class="my_lg"):
    pass

site.build()