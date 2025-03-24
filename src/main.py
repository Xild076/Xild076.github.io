from widget import Website

if __name__ == "__main__":
    app = Website("Harry's Blog", footer="&copy; 2025 Harry Yin. All rights reserved.", custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("Harry's Blog", align="center")
        page.write("Hello and welcome to my blog! :D", align="center")
        page.write("My name is Harry and I am an aspiring data scientist (specifically in the form of data collection and AI models) with a focus on computational linguistics. I am currently a student at Leland High School in San Jose, California and am looking for opportunities to further my knowledge in the field.")
        page.write("This blog is dedicated to uploading my projects and sharing my thoughts on various topics, whether they be about programming or philosophy. I hope you enjoy your stay!")

        page.divider()
        page.email_link("harry.d.yin.gpc@gmail.com", "@ Contact Me")
        page.link("https://www.github.com/Xild076", "🔗 GitHub")
        page.link("https://www.linkedin.com/in/harry-yin-5493152b0/", "🔗 LinkedIn")
        
        page.divider()

        page.heading("Featured Project")
        page.widget("images/objective_news.png", "Alitheia AI", "A project that aims to create a comprehensive pipeline to locate, determine, and objectify news.", "objectivenews")
        page.spacer(10)
        page.button("View All Projects", "projects")

        page.divider()
        page.heading("Latest Blog Posts")
        page.widget("images/question.png", "The Question We Forget", "This is a blog post on the question we forget.", "question")
        page.widget("images/polarization.png", "Polarization in Modern Media", "This is a blog post on my thoughts on the polarization of modern media.", "polarization")
        page.widget("images/ai_vs_algorithm.png", "Stockfish vs AlphaZero, Algorithm vs AI", "This is a blog post on the differences between algorithms and AI.", "ai_vs_algorithm")
        page.widget("images/bias_types.png", "Types of Bias", "This is a blog post on my thoughts on the types of biases.", "bias_types")
        page.spacer(10)
        page.button("View All Blog Posts", "blog")
        

    with app.page("blog", "Blog") as page:
        page.heading("Blogs")
        page.write("Here are a couple of blogposts!")
        page.widget("images/question.png", "The Question We Forget", "This is a blog post on the question we forget.", "question")
        page.widget("images/polarization.png", "Polarization in Modern Media", "This is a blog post on my thoughts on the polarization of modern media.", "polarization")
        page.widget("images/ai_vs_algorithm.png", "Stockfish vs AlphaZero, Algorithm vs AI", "This is a blog post on the differences between algorithms and AI.", "ai_vs_algorithm")
        page.widget("images/bias_types.png", "Types of Bias", "This is a blog post on my thoughts on the types of biases.", "bias_types")
        page.widget("images/fatalism.png", "My Thoughts on Fatalism", "This is a blog post on my thoughts about fatalism.", "fatalism")
        page.widget("images/bias_removal.png", "Removing Bias from Text", "This is a blog post about methods to algorithmically remove bias from text.", "debias")
        page.widget("images/fake_news.png", "Methods to Detect Fake News", "This is a blog post about methods to detect fake news.", "fake_news")
        page.widget("images/self_atten.png", "Self Attention in Textual Clustering", "This is a blog post about self attention in textual clustering.", "self_atten_blog")
        page.widget("images/likeable_character.png", "What makes a likeable character?", "This is a blog post about my thoughs on what makes a likeable character.", "likeable_character")
        page.widget("", "Hello Blog!", "This is the first blog post!", "hello_blog")
    
    app.add_blog_page("question", "Misc - The Question We Forget", "blogs/question_forget.md", date="2025-03-24", author="Harry Yin")
    app.add_blog_page("polarization", "Programming - Polarization in Modern Media", "blogs/polarization.md", date="2025-03-20", author="Harry Yin")
    app.add_blog_page("ai_vs_algorithm", "Programming - Stockfish vs AlphaZero, Algorithm vs AI", "blogs/ai_algorithm.md", date="2025-03-13", author="Harry Yin")
    app.add_blog_page("bias_types", "Programming - Types of Bias", "blogs/modern_media.md", date="2025-03-12", author="Harry Yin")
    app.add_blog_page("fatalism", "Misc - My Thoughts on Fatalism", "blogs/fatalism.md", date="2025-03-11", author="Harry Yin")
    app.add_blog_page("debias", "Programming - Removing Bias from Text", "blogs/bias_removal.md", date="2025-03-10", author="Harry Yin")
    app.add_blog_page("fake_news", "Programming - Methods to Detect Fake News", "blogs/fake_news.md", date="2025-03-09", author="Harry Yin")
    app.add_blog_page("self_atten_blog", "Programming - Self Attention in Textual Clustering", "blogs/self_atten_blog.md", date="2025-03-08", author="Harry Yin")
    app.add_blog_page("likeable_character", "Misc - What makes a likeable character?", "blogs/likeable_character.md", date="2025-03-08", author="Harry Yin")
    app.add_blog_page("hello_blog", "Hello Blog", "blogs/hello_blog.md", date="2025-03-07", author="Harry Yin")
    
    with app.page("projects", "Projects") as page:
        page.heading("Projects")
        page.write("Here is a list of the projects I did!")
        page.widget("images/objective_news.png", "Alitheia AI", "This is a project that objectifies News.", "objectivenews")
        page.widget("images/stock_pred.png", "Polystock AI", "This is a project that attempts to predict stock prices.", "stockpred")
        page.widget("images/lsd_ai.png", "LSD AI", "This is a project that uses AI to analyse speechs", "lsdai")
        page.widget("images/ai_cat.png", "AI Catalog", "This is a project that uses AI to catalogue data.", "aicat")
    
    app.add_project_page(
        "objectivenews",
        "Alitheia AI (Objective News)",
        [("2024-10-01", "Began project Objective News"), 
         ("2024-12-15", "Completed the first beta version of Objective News"), 
         ("2025-01-02", "Completed the second beta version of Objective News"),
         ("2025-02-09", "Completed official proposal paper for full version of Objective News"),
         ("2025-03-06", "Renamed project to Alitheia AI (Greek for 'truth')")],
         "website_text/objective_news_intro.md",
        "Xild076",
        "ObjectiveNews",
        [("Beta Paper", "papers/paper_vbeta.md", "md", "This is the first paper written upon release of the Beta version of Alitheia AI"), ("Official Proposal", "papers/Proposal—Objective News.pdf", "pdf", "This is the official proposal paper for a full pipeline version of Alitheia AI, created after much consideration of new methodologies and techniques.")],
        [("Python 3.x for backend processing", "Python", "https://www.python.org/downloads/"), ("Streamlit for hosting", "Streamlit", "https://streamlit.io/"), ("Stanza for NLP", "Stanza", "https://stanfordnlp.github.io/stanza/"), ("Hugging Face Transformers for state-of-the-art models", "HuggingFace", "https://huggingface.co/"),
         ("Scikit-learn for clustering", "Scikit-learn", "https://scikit-learn.org/stable/"), ("BeautifulSoup for web scraping", "BeautifulSoup", "https://pypi.org/project/beautifulsoup4/"), ("Requests for HTTP requests", "Requests", "https://pypi.org/project/requests/"), ("Github for development", "Github", "https://github.com/")]
    )

    app.add_project_page(
        "stockpred",
        "Polystock AI (Stock Prediction)",
        [("2023-06-11", "Began project Polystock AI"),
         ("2023-10-15", "Completed the first beta version of Polystock AI"),
         ("2023-11-20", "Wrote the first paper on Polystock AI"),
         ("2024-09-03", "Began to rework the project to use a more advanced techniques"),
         ("2024-11-10", "Completed the second beta version of Polystock AI with full functionality and partially trained models")],
         "website_text/stock_pred_intro.md",
         "Xild076",
         "StockPred",
         [("Beta Paper", "papers/RL_for_Stocks.pdf", "pdf", "This is the first paper written upon release of the first beta version of Polystock AI. Please note that it is very outdated.")],
         [("Python 3.x for backend processing", "Python", "https://www.python.org/downloads/"), ("FRED API for data", "FRED", "https://fred.stlouisfed.org/"), ("Streamlit for hosting", "Streamlit", "https://streamlit.io/"), ("Requests for HTTP requests", "Requests", "https://pypi.org/project/requests/"), ("Yfinance for stock data", "Yfinance", "https://pypi.org/project/yfinance/"),
          ("Pandas for data manipulation", "Pandas", "https://pandas.pydata.org/"), ("Numpy for numerical operations", "Numpy", "https://numpy.org/"), ("Matplotlib for plotting", "Matplotlib", "https://matplotlib.org/"), ("PyTorch for ML development", "PyTorch", "https://pytorch.org/"), ("Github for development", "Github", "https://github.com")]
    )

    app.add_project_page(
        "lsdai",
        "LSD AI (Speech and Debate AI)",
        [("2024-06-24", "Began project LSD AI"),
         ("2024-08-11", "Completed the first beta version of LSD AI"),
         ("2024-08-19", "Began reworking and updating the project"),
         ("2024-09-01", "Completed the second beta of LSDAI"),
         ("2024-10-27", "Migrated LSDAI from an app to Streamlit")],
         "website_text/lsd_ai_intro.md",
         "Xild076",
         "LSDAI",
         [("LSDAI README", "papers/lsd_ai_readme.md", "md", "This is the README for LSDAI, which includes a description of the project and how to use it.")],
         [("Python 3.x for backend processing", "Python", "https://www.python.org/downloads/"), ("Streamlit for hosting", "Streamlit", "https://streamlit.io/"), ("OpenAI API keys for audio/content analysis", "OpenAI", "https://platform.openai.com/docs/overview"),
          ("Kaggle for training data", "Kaggle", "https://www.kaggle.com/datasets"), ("Github for development", "Github", "https://github.com")]
    )

    app.add_project_page(
        "aicat",
        "AI Catalog (Basic PyTorch recreation)",
        [("2024-02-09", "Began project AI Catalog"),
         ("2024-04-05", "Finalized first version of VPG with only numpy"),
         ("2024-05-03", "Began creation of PyTorch structure with Karpathy's Micrograd as reference"),
         ("2024-07-10", "Completed first basic version of Micrograd")],
         "website_text/ai_catolog_intro.md",
         "Xild076",
         "AICatalogue",
         [],
         [("Python 3.x for backend processing", "Python", "https://www.python.org/downloads/"), ("Numpy for numerical processing", "Numpy", "https://numpy.org/"), ("Github for development", "Github", "https://github.com")]
    )
    
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.divider()
        page.write("Contacts:")
        page.email_link("harry.d.yin.gpc@gmail.com", "Email --- ", False)
        page.link("https://www.github.com/Xild076", "GitHub --- ", False)
        page.link("https://www.linkedin.com/in/harry-yin-5493152b0/", "LinkedIn --- ", False)
        page.divider()
        page.image("images/very bad photo.png", "A very bad photo of me", 250, 325, "left", False, False, True, "A very bad photo of me lol")
        page.import_text("website_text/aboutme.md")
        page.divider()
        page.heading("Some Important Documents")
        page.write("Below, I've included my resume and transcripts just in case anyone might need them.")
        page.file_download("website_text/Harry Yin - Resume.pdf", "Resume", False)
        page.file_download("website_text/Transcript.pdf", "Transcript", False)
        page.divider()
        page.write("That aside, here are some photos of my cat (the small one was one our friend's cats)!")
        cat_images = [
            "images/cats/archie_brownie.png",
            "images/cats/archie.png",
            "images/cats/brownie_archie.png",
            "images/cats/IMG_0285.png",
            "images/cats/IMG_1075.png",
            "images/cats/IMG_1122.png",
            "images/cats/IMG_1131.png",
            "images/cats/IMG_6074.png",
            "images/cats/IMG_6084.png",
            "images/cats/IMG_6094.png",
            "images/cats/IMG_6107.png",
            "images/cats/IMG_6110.png",
            "images/cats/IMG_6205.png",
            "images/cats/IMG_6275.png",
            "images/cats/IMG_6279.png",
            "images/cats/IMG_6403.png",
            "images/cats/IMG_6775.png",
            "images/cats/IMG_6998.png",
            "images/cats/IMG_7202.png",
            "images/cats/IMG_7285.png",
            "images/cats/IMG_7810.png",
            "images/cats/IMG_8588.png",
            "images/cats/IMG_9280.png",
            "images/cats/IMG_9297.png",
            "images/cats/IMG_9522.png",
            "images/cats/IMG_9976.png"
        ]
        page.rotating_gallery(cat_images, container_height=300, container_width=400, interval=1000, smart_fit=True)
    
    app.compile(".")
