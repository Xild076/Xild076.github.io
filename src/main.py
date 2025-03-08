from widget import Website

if __name__ == "__main__":
    app = Website("Harry's Blog", footer="&copy; 2025 Harry Yin. All rights reserved.", custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("Harry's Blog", align="center")
        page.write("Hello and welcome to my blog! :D", align="center")
        page.write("My name is Harry and I am an aspiring data scientist (specifically in the form of data collection and AI models) with a focus on computational linguistics. I am currently a student at Leland High School in San Jose, California and am looking for opportunities to further my knowledge in the field.")
        page.write("This blog is dedicated to uploading my projects and sharing my thoughts on various topics, whether they be about programming or philosophy. I hope you enjoy your stay!")

        page.divider()
        page.email_link("harry.d.yin.gpc@gmail.com", "✉ Contact Me")
        page.link("https://www.github.com/Xild076", "🔗 GitHub")
        page.link("https://www.linkedin.com/in/harry-yin-5493152b0/", "🔗 LinkedIn")
        
        page.divider()
        
        page.heading("Latest Blog Posts")
        page.widget("", "Hello Blog!", "This is a test/hello blog post!", "hello_blog")
        page.spacer(10)
        page.button("View All Blog Posts", "blog")
        
        page.divider()
        
        page.heading("Featured Project")
        page.widget("", "Alitheia AI", "A project that aims to create a comprehensive pipeline to locate, determine, and objectify news.", "objectivenews")

    with app.page("blog", "Blog") as page:
        page.heading("Blogposts")
        page.write("Here are a couple of blogposts!")
        page.widget("", "Hello Blog!", "This is a test/hello blog post!", "hello_blog")
    
    app.add_blog_page("hello_blog", "Hello Blog", "blogs/hello_blog.md", date="2025-03-07", author="Harry Yin")
    
    with app.page("projects", "Projects") as page:
        page.heading("Projects")
        page.write("Here is a list of projects.")
        page.widget("", "Alitheia AI", "This is a project that objectifies News.", "objectivenews")
    
    app.add_project_page(
        "objectivenews",
        "Alitheia AI (Objective News)",
        [("2024-10-01", "Began project Objective News"), 
         ("2024-12-15", "Completed the first beta version of Objective News"), 
         ("2025-01-02", "Completed the second beta version of Objective News"),
         ("2025-02-09", "Completed official proposal paper for full version of Objective News"),
         ("2025-03-06", "Renamed project to Alitheia AI (Greek for 'truth')")],
         "papers/objective_news_intro.md",
        "https://gist.github.com/Xild076/3c89ad41dcc72a5388226d732873bff0",
        "The code provided illustrates the two most critical components of the project: the grouping and objectification, both of which use novel techniques to achieve the desired results. See the paper for more details.",
        [("Beta Paper", "papers/paper_vbeta.md", "md", "This is the first paper written upon release of the Beta version of Alitheia AI"), ("Official Proposal", "papers/Proposal—Objective News.pdf", "pdf", "This is the official proposal paper for a full pipeline version of Alitheia AI, created after much consideration of new methodologies and techniques.")],
        [("Python 3.x for backend processing", "Python", "https://www.python.org/downloads/"), ("Streamlit for hosting", "Streamlit", "https://streamlit.io/"), ("Stanza for NLP", "Stanza", "https://stanfordnlp.github.io/stanza/"), ("Hugging Face Transformers for state-of-the-art models", "HuggingFace", "https://huggingface.co/"),
         ("Scikit-learn for clustering", "Scikit-learn", "https://scikit-learn.org/stable/"), ("BeautifulSoup for web scraping", "BeautifulSoup", "https://pypi.org/project/beautifulsoup4/"), ("Requests for HTTP requests", "Requests", "https://pypi.org/project/requests/"), ("Github for development", "Github", "https://github.com/")]
    )
    
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.divider()
        page.write("Contacts:")
        page.email_link("harry.d.yin.gpc@gmail.com", "Email ---")
        page.link("https://www.github.com/Xild076", "GitHub ---")
        page.link("https://www.linkedin.com/in/harry-yin-5493152b0/", "LinkedIn ---")
        page.image("images/very bad photo.png", "A very bad photo of me", 250, 325, "left", False, False, True, "A very bad photo of me lol")
        page.import_text("website_text/aboutme.md")
        page.divider()
        page.heading("Some Important Documents")
        page.write("Below, I've included my resume and transcripts just in case anyone might need them.")
        page.file_download("website_text/Harry Yin - Resume.pdf", "Resume", False)
        page.file_download("website_text/Transcript.pdf", "Transcript", False)
        page.divider()
        page.write("That aside, here are some photos of my cat (the small one was one our friend's cats)!")
        page.rotating_gallery(["images/archie_brownie.png", "images/archie.png", "images/brownie_archie.png"], container_height=300, container_width=400, interval=1000, smart_fit=True)
    
    app.compile(".")
