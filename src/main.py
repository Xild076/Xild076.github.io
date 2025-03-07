from widget import Website

"""
if __name__ == "__main__":
    app = Website("My Site", footer="&copy; 2025 My Site. All rights reserved.", custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("Welcome to My Site")
        page.write("Discover my work and projects.")
        page.widget("", "Sample Widget", "This is a clickable widget with image on the left.", "blog.html")
        page.image("https://via.placeholder.com/300x200", "Sample Image", 300, 200)
        page.email_link("example@example.com", "Contact Us")
        page.video("https://www.youtube.com/embed/dQw4w9WgXcQ")
        page.code_block("print('Hello, world!')", "python")
        page.blockquote("This is an inspiring quote.", "Author Name")
        page.alert_box("This is an important alert!", "warning")
        page.gallery(["https://via.placeholder.com/200", "https://via.placeholder.com/200", "https://via.placeholder.com/200"])
        page.markdown("This is **bold** text and *italic* text with ~~strikethrough~~.")
        page.list(["Item 1", "Item 2", "Item 3"])
        page.accordion([("Section 1", "Content for section 1."), ("Section 2", "Content for section 2.")])
        page.tabs([("Tab 1", "Content for tab 1."), ("Tab 2", "Content for tab 2.")])
        page.tooltip("Hover over me", "This is a tooltip")
        page.map("New York, NY", 600, 450)
        page.animated("<p>This text bounces!</p>", "animate__bounce")
        page.container("<p>This is inside a container.</p>")
        page.divider()
        page.button("Click Me", "https://example.com")
        page.jumbotron("Jumbotron Title", "This is a jumbotron subtitle.", "Learn More", "https://example.com")
        page.carousel(["https://via.placeholder.com/800x400", "https://via.placeholder.com/800x400", "https://via.placeholder.com/800x400"])
        page.row(["Column 1 content", "Column 2 content", "Column 3 content"])
        page.spacer(50)
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.write("Information about me goes here.")
    with app.page("blog", "Blog") as page:
        page.heading("Blog")
        page.write("Here is a list of blog posts.")
        page.timeline_entry("2025-01-01", "Project started")
        page.timeline_entry("2025-03-01", "First milestone reached")
    with app.page("news", "News") as page:
        page.heading("News")
        page.write("Latest news updates.")
    app.compile(".")
"""

if __name__ == "__main__":
    app = Website("Harry's Blog", footer="&copy; 2025 Harry Yin. All rights reserved.", custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("Harry's Blog", align="center")
        page.write("Hello and welcome to my blog! :D", align="center")
        page.write("My name is Harry and I am an aspiring data scientist (specifically in the form of data collection and AI models) with a focus on computational linguistics. I am currently a student at Leland High School in San Jose, California and am looking for opportunities to further my knowledge in the field.")
        page.write("This blog is dedicated to uploading my projects and sharing my thoughts on various topics, whether they be about programming or philosophy. I hope you enjoy your stay!")

        page.divider()
        page.email_link("harry.d.yin.gpc@gmail.com", "Contact Me\n")
        page.link("https://www.github.com/Xild076", "GitHub\n")
        page.link("https://www.linkedin.com/in/harry-yin-5493152b0/", "LinkedIn")
        
        page.divider()
        
        page.heading("Latest Blog Posts")

        page.spacer(10)
        page.button("View All Blog Posts", "blog")
        page.spacer(10)
        page.widget("", "Hello Blog!", "This is a test/hello blog post!", "hello_blog")
        
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
    )
    
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.write("About me!")
    
    app.compile(".")
