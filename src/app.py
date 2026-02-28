from sitegen import Site, AnimationType, Alignment, Spacing, ButtonType, ObjectFit

# ============================================================
# Data — single source of truth for Blog & Project metadata
# ============================================================

BLOG_POSTS = [
    {"slug": "food",               "title": "Misc - Short Story: Food",                                       "file": "blogs/food.md",               "author": "Harry Yin", "date": "2026-02-28"},
    {"slug": "writing_lessons",    "title": "Misc - What I learned about writing",                             "file": "blogs/writing_lessons.md",    "author": "Harry Yin", "date": "2026-02-05"},
    {"slug": "research_reflection","title": "Programming - Research Reflection on ETSA (AeVAA)",               "file": "blogs/researching.md",        "author": "Harry Yin", "date": "2025-11-04"},
    {"slug": "writing_fun",        "title": "Misc - Short Story: The Frog Who Cried Rain",                     "file": "blogs/writing_fun.md",        "author": "Harry Yin", "date": "2025-09-30"},
    {"slug": "ai_ethics",          "title": "Programming - My thoughts on AI ethics and how that ties into Fatalism", "file": "blogs/ai_ethics.md",   "author": "Harry Yin", "date": "2025-08-22"},
    {"slug": "local_minima",       "title": "Programming - Funny ways to describe the local minima to an edgy teen","file": "blogs/local_minima.md",  "author": "Harry Yin", "date": "2025-08-10"},
    {"slug": "revisit",            "title": "Programming - Revisiting old projects",                           "file": "blogs/revisiting_projects.md","author": "Harry Yin", "date": "2025-07-25"},
    {"slug": "on_mortality",       "title": "Misc - Scary Moment",                                             "file": "blogs/on_mortality.md",       "author": "Harry Yin", "date": "2025-06-20"},
    {"slug": "heuristic_eq",       "title": "Programming - Finding Heuristic Equations",                       "file": "blogs/heuristic_eq.md",       "author": "Harry Yin", "date": "2025-05-31"},
    {"slug": "sentiment_target",   "title": "Programming - Entity Sentiment Targeting",                        "file": "blogs/sentiment_target.md",   "author": "Harry Yin", "date": "2025-04-04"},
    {"slug": "question",           "title": "Misc - The Question We Forget",                                   "file": "blogs/question_forget.md",    "author": "Harry Yin", "date": "2025-03-24"},
    {"slug": "polarization",       "title": "Programming - Polarization in Modern Media",                      "file": "blogs/polarization.md",       "author": "Harry Yin", "date": "2025-03-20"},
    {"slug": "ai_vs_algorithm",    "title": "Programming - Stockfish vs AlphaZero, Algorithm vs AI",           "file": "blogs/ai_algorithm.md",       "author": "Harry Yin", "date": "2025-03-13"},
    {"slug": "bias_types",         "title": "Programming - Types of Bias",                                     "file": "blogs/modern_media.md",       "author": "Harry Yin", "date": "2025-03-12"},
    {"slug": "fatalism",           "title": "Misc - My Thoughts on Fatalism",                                  "file": "blogs/fatalism.md",           "author": "Harry Yin", "date": "2025-03-11"},
    {"slug": "debias",             "title": "Programming - Removing Bias from Text",                           "file": "blogs/bias_removal.md",       "author": "Harry Yin", "date": "2025-03-10"},
    {"slug": "fake_news",          "title": "Programming - Methods to Detect Fake News",                       "file": "blogs/fake_news.md",          "author": "Harry Yin", "date": "2025-03-09"},
    {"slug": "self_atten_blog",    "title": "Programming - Self Attention in Textual Clustering",              "file": "blogs/self_atten_blog.md",    "author": "Harry Yin", "date": "2025-03-08"},
    {"slug": "likeable_character", "title": "Misc - What makes a likeable character?",                         "file": "blogs/likeable_character.md", "author": "Harry Yin", "date": "2025-03-08"},
    {"slug": "hello_blog",         "title": "Hello Blog",                                                      "file": "blogs/hello_blog.md",         "author": "Harry Yin", "date": "2025-03-07"},
]

PROJECTS = [
    {
        "slug": "etsa_qc",
        "title": "ETSA --- QC (AeVAA)",
        "description": "Advanced NLP pipeline combining graph-centric analysis with quantum-centric techniques for precise sentiment detection.",
        "image": "/static/imgs/etsa_pipeline.png",
        "techs": ["Python", "SpaCy", "NetworkX", "HuggingFace Transformers", "Streamlit", "Maverick", "Pandas", "Matplotlib"],
        "buttons": [
            {"text": "View Project", "link": "projects/etsa_qc.html", "style": "primary"},
            {"text": "GitHub", "link": "https://github.com/Xild076/ETSA--QC-", "style": "outline-primary"},
        ],
        "readme": "projects/etsa/etsa_qc_intro.md",
        "timeline": [
            {"time": "2025-03-17", "description": "Began project ETSA --- QC"},
            {"time": "2025-04-11", "description": "Joined the MAGICS Lab at USF"},
            {"time": "2025-10-05", "description": "Finished the AeVAA paper"},
        ],
        "documents": [
            {"title": "Summary of Novelty", "url": "projects/etsa/A Summary of Novelty.md"},
            {"title": "Survey Proposal", "url": "projects/etsa/ABSA Survey Proposal.md"},
            {"title": "ETSA --- QC Survey", "url": "https://etsa-survey.streamlit.app/"},
            {"title": "Graph Demo", "url": "projects/etsa/graph_sentiment_analysis.html"},
        ],
    },
    {
        "slug": "twt",
        "title": "Thinking Without Thinking",
        "description": "A free, open source agentic AI tool based fully on text systems.",
        "image": "/static/imgs/twt.png",
        "techs": ["Python", "Streamlit", "Google API"],
        "buttons": [
            {"text": "View Project", "link": "projects/twt.html", "style": "primary"},
            {"text": "GitHub", "link": "https://github.com/Xild076/ThinkingWithoutThinking", "style": "outline-primary"},
        ],
        "readme": "projects/twt/twt_intro.md",
        "timeline": [
            {"time": "2024-08-29", "description": "Begin development of Thinking Without Thinking"},
            {"time": "2024-08-30", "description": "Implemented the first system of self-criticism began hosting on Streamlit"},
            {"time": "2024-10-15", "description": "Began reworking TWT to include pipeline blocks system"},
        ],
        "documents": [],
    },
    {
        "slug": "lsdai",
        "title": "L&SD AI (Speech and Debate AI)",
        "description": "Experimental ML system to analyze and give feedback to speeches.",
        "image": "/static/imgs/lsd_ai.png",
        "techs": ["Python", "Streamlit", "OpenAI API", "Kaggle"],
        "buttons": [
            {"text": "View Project", "link": "projects/lsdai.html", "style": "primary"},
            {"text": "GitHub", "link": "https://github.com/Xild076/LSDAI", "style": "outline-primary"},
        ],
        "readme": "projects/lsdai/lsd_ai_intro.md",
        "timeline": [
            {"time": "2024-06-24", "description": "Began project L&SD AI"},
            {"time": "2024-08-11", "description": "Completed the first beta version of L&SD AI"},
            {"time": "2024-08-19", "description": "Began reworking and updating the project"},
            {"time": "2024-09-01", "description": "Completed the second beta of L&SD AI"},
            {"time": "2024-10-27", "description": "Migrated L&SD AI from an app to Streamlit"},
        ],
        "documents": [
            {"title": "LS&DAI README", "url": "projects/lsdai/lsd_ai_readme.md"},
        ],
    },
    {
        "slug": "objectivenews",
        "title": "Alitheia AI (Objective News)",
        "description": "AI-powered news analysis system designed to identify and reduce bias in media reporting through advanced NLP techniques.",
        "image": "/static/imgs/objective_news.png",
        "techs": ["Python", "Streamlit", "Stanza", "HuggingFace Transformers", "Scikit-learn", "BeautifulSoup"],
        "buttons": [
            {"text": "View Project", "link": "projects/objectivenews.html", "style": "primary"},
            {"text": "GitHub", "link": "https://github.com/Xild076/ObjectiveNews", "style": "outline-primary"},
        ],
        "readme": "projects/objective_news/objective_news_intro.md",
        "timeline": [
            {"time": "2024-10-01", "description": "Began project Objective News"},
            {"time": "2024-12-15", "description": "Completed the first beta version of Objective News"},
            {"time": "2025-01-02", "description": "Completed the second beta version of Objective News"},
            {"time": "2025-02-09", "description": "Completed official proposal paper for full version of Objective News"},
            {"time": "2025-03-06", "description": "Renamed project to Alitheia AI (Greek for 'truth')"},
            {"time": "2025-07-25", "description": "Massive rework including improved clustering algorithms, hyperparameter tuning, self-attention model"},
        ],
        "documents": [
            {"title": "Beta Paper", "url": "projects/objective_news/paper_vbeta.md"},
            {"title": "Official Proposal", "url": "projects/objective_news/Proposal—Objective News.pdf"},
        ],
    },
    {
        "slug": "stockpred",
        "title": "Polystock AI (Stock Prediction)",
        "description": "Reinforcement learning approach to stock market prediction using deep Q-networks and market sentiment analysis.",
        "image": "/static/imgs/stock_pred.png",
        "techs": ["Python", "PyTorch", "FRED API", "Streamlit", "Yfinance", "Pandas", "Matplotlib"],
        "buttons": [
            {"text": "View Project", "link": "projects/stockpred.html", "style": "primary"},
            {"text": "GitHub", "link": "https://github.com/Xild076/StockPred", "style": "outline-primary"},
        ],
        "readme": "projects/stockpred/stock_pred_intro.md",
        "timeline": [
            {"time": "2023-06-11", "description": "Began project Polystock AI"},
            {"time": "2023-10-15", "description": "Completed the first beta version of Polystock AI"},
            {"time": "2023-11-20", "description": "Wrote the first paper on Polystock AI"},
            {"time": "2024-09-03", "description": "Began to rework the project to use more advanced techniques"},
            {"time": "2024-11-10", "description": "Completed the second beta version of Polystock AI"},
            {"time": "2025-07-06", "description": "Updated to use different data source, better storage, and more advanced model"},
        ],
        "documents": [
            {"title": "Beta Paper", "url": "projects/stockpred/RL_for_Stocks.pdf"},
        ],
    },
]

# ============================================================
# Site setup
# ============================================================

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
        keywords="portfolio, projects, blog, developer, AI, NLP",
        base_url="https://xild076.github.io",
        main_nav_items=[
            {"text": "Home",       "url": "/index.html"},
            {"text": "Projects",   "url": "/projects.html"},
            {"text": "Blog",       "url": "/blog.html"},
            {"text": "Cool Stuff", "url": "/cool_stuff.html"},
            {"text": "CV/Resume",  "url": "/cv.html"},
            {"text": "About",      "url": "/about.html"},
        ]
    )
    return site

# ============================================================
# Page Builders
# ============================================================

def build_index_page(site: Site):
    page = site.add_page("index", "Home")

    # Hero
    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("Welcome to Harry Yin's Portfolio!", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--text-heading)")
        page.Write("A showcase of my projects and other random and cool stuff.", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL)

    # Featured project
    with page.Section(title="Featured Project"):
        page.ProjectCard(
            title="ETSA --- QC (AeVAA)",
            description="I've been working on AeVAA with Professor David-Guy Brizan and Alex Peczon from USFCA. It is a project to create an explainable ABSA system, and we are anticipating a paper submission at the start of next year.",
            image="/static/imgs/etsa_pipeline.png",
            techs=["Python", "SpaCy", "NetworkX", "HuggingFace Transformers"],
            buttons=[{"text": "View Project", "link": "projects/etsa_qc.html"}],
        )

    page.Divider(spacing_before=Spacing.LG, spacing_after=Spacing.LG)

    # Explore More
    with page.Section(title="Explore More"):
        with page.Columns(n=3, gap=Spacing.MD):
            with page.Card(css_class="text-center p-4"):
                page.Write("🚀", text_size="2rem", align=Alignment.CENTER, spacing_after=Spacing.SM)
                page.Write("Projects", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--primary)")
                page.Write("Research and development, from older to SOTA projects.", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                page.Button("View Projects", link="/projects.html", style_type=ButtonType.OUTLINE_PRIMARY)

            with page.Card(css_class="text-center p-4"):
                page.Write("✍️", text_size="2rem", align=Alignment.CENTER, spacing_after=Spacing.SM)
                page.Write("Blog", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--primary)")
                page.Write("Some thoughts by some guy on tech and philosophy.", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                page.Button("Read Blog", link="/blog.html", style_type=ButtonType.OUTLINE_PRIMARY)

            with page.Card(css_class="text-center p-4"):
                page.Write("👤", text_size="2rem", align=Alignment.CENTER, spacing_after=Spacing.SM)
                page.Write("About", align=Alignment.CENTER, text_size="18px", spacing_after=Spacing.SM, text_color="var(--primary)")
                page.Write("Background, skills, and interests.", align=Alignment.CENTER, text_size="14px", spacing_after=Spacing.MD)
                page.Button("About Me", link="/about.html", style_type=ButtonType.OUTLINE_PRIMARY)


def build_projects_page(site: Site):
    page = site.add_page("projects", "Projects")

    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("Projects", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="48px", text_color="var(--text-heading)")
        page.Write("AI research & development portfolio", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    with page.Section(title="Research Projects"):
        for i, proj in enumerate(PROJECTS):
            page.ProjectCard(
                title=proj["title"],
                description=proj["description"],
                image=proj.get("image"),
                techs=proj.get("techs", []),
                buttons=proj.get("buttons", []),
            )


def build_blog_page(site: Site):
    page = site.add_page("blog", "Blog")

    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("Blog", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--text-heading)")
        page.Write("Random thoughts and insights on technology, AI, and life", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    with page.Section(title="Latest Posts", subtitle="Some random words by some random guy."):
        sorted_posts = sorted(BLOG_POSTS, key=lambda x: x["date"], reverse=True)
        with page.Container(css_class="row"):
            for i, post in enumerate(sorted_posts):
                with page.Container(css_class="col-md-6 mb-4"):
                    page.BlogCard(
                        title=post["title"],
                        author=post.get("author"),
                        date=post.get("date"),
                        slug=post["slug"],
                    )


def build_cool_stuff_page(site: Site):
    page = site.add_page("cool_stuff", "Cool Stuff")

    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("Cool Stuff", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--text-heading)")
        page.Write("Experimental projects and fun explorations", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    with page.Section():
        page.Widget(
            "APUSH Timeline",
            "Timeline visualization from my AP US History course.",
            link="/apush_timeline.html",
            image_url="/static/imgs/placeholder.png",
        )
        page.Widget(
            "CSP Project",
            "My Computer Science Principles final project showcase.",
            link="/csp.html",
            image_url="/static/imgs/placeholder.png",
        )


def build_cv_page(site: Site):
    page = site.add_page("cv", "CV/Resume")

    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("CV/Resume", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px", text_color="var(--text-heading)")
        page.Write("My professional experience and skills", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    with page.Section():
        page.Callout("You can download my CV/Resume below.", callout_type="info", title="Download")
        page.Markdown("You can download my CV/Resume [here](static/docs/harry_yin_cv.pdf).", align=Alignment.CENTER, spacing_after=Spacing.LG)




def build_about_page(site: Site):
    page = site.add_page("about", "About Me")

    with page.Background(color="var(--light)", padding=Spacing.XL, css_class="rounded-lg hero-section"):
        page.Write("About Me", align=Alignment.CENTER, spacing_after=Spacing.MD, text_size="42px", text_color="var(--text-heading)")
        page.Write("(About me!!!)", align=Alignment.CENTER, spacing_after=Spacing.LG, text_color="var(--text-secondary)")

    with page.Container(css_class="my_lg"):
        with page.Columns(n=2, gap=Spacing.XL, spacing_before=Spacing.LG):
            with page.Container(css_class="d-flex justify-content-center align-items-center"):
                page.Image("/static/imgs/profileimage.jpg", alt="Harry Yin",
                           caption="Harry Yin - Developer & Researcher",
                           width="350px", height="350px", object_fit=ObjectFit.COVER,
                           align=Alignment.CENTER)

            with page.Container(css_class="d-flex flex-column justify-content-center"):
                page.Markdown("""Hi, I'm Harry!

I'm an aspiring data scientist and researcher! I love working on projects that involve the analysis of complex data like text and human emotions, using tools to analyze and model such processes.

My main interests lie in natural language processing, machine learning, and AI ethics. I've worked extensively with Python, scikit learn, spacy, and various other machine learning libraries to build projects. Currently, I'm exploring symbolic systems and their application to creating interpretable models.

In my free time, I enjoy reading a lot of novels, writing my own short stories, and sleeping. I also like swimming and playing some video games when I have the time.

Feel free to explore my projects and blog, and I'm always open to collaboration or discussion on interesting topics!
""", align=Alignment.LEFT)

                page.TagList(["Python", "NLP", "Machine Learning", "AI Ethics", "PyTorch", "Transformers", "Research"], spacing_after=Spacing.MD)

                with page.Container(css_class="d-flex gap-2 mt-3"):
                    page.Button("EXPLORE PROJECTS", link="/projects.html", style_type=ButtonType.PRIMARY)
                    page.Button("READ BLOG", link="/blog.html", style_type=ButtonType.OUTLINE_PRIMARY)

        page.Image("/static/imgs/pengu.png", alt="Penguin", caption="penguine!!!", align=Alignment.CENTER)


# ============================================================
# Register project detail pages & blog posts
# ============================================================

def add_project_pages(site: Site):
    for proj in PROJECTS:
        site.add_project_page(
            proj["slug"],
            proj["title"],
            project_readme_file=proj.get("readme"),
            timeline_events=proj.get("timeline", []),
            technologies_used=proj.get("techs", []),
            project_documents=proj.get("documents", []),
            meta_info={"author": "Xild076", "project_id": proj["slug"].upper()},
        )


def add_blog_posts(site: Site):
    for post in BLOG_POSTS:
        site.add_blog_post(
            post["slug"],
            post["title"],
            post["file"],
            author=post.get("author"),
            date=post.get("date"),
        )


def add_html_pages(site: Site):
    import os
    content_dir = "content"

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


# ============================================================
# Main
# ============================================================

def main():
    print("Building site...")

    site = create_site()

    build_index_page(site)
    build_projects_page(site)
    build_blog_page(site)
    build_cool_stuff_page(site)
    build_cv_page(site)
    build_about_page(site)

    add_project_pages(site)
    add_blog_posts(site)
    add_html_pages(site)

    site.build()
    print("Site built successfully!")


if __name__ == "__main__":
    main()
