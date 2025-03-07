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
    app = Website("Harry's Blog", footer="&copy; 2025 My Site. All rights reserved.", custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("(Xild076) Harry's Blog")
        page.write("Hello and welcome to my blog. Here you will find a few of my thoughts and ideas, whether they be about programming or philosophy. I've also included a few of my projects and some other neat stuff. Enjoy!")
        page.divider()
        page.heading("Latest Blog Posts")
        page.widget("", "Test Blog", "This is a test blog post.", "blog")
        page.divider()
        page.heading("Projects")
        page.timeline_entry("2023-06-01", "Began project StockPred")
        page.timeline_entry("2023-09-01", "Completed first version of project StockPred")
    with app.page("blog", "Blog") as page:
        page.heading("Blog")
        page.write("Here is a list of blog posts.")
        page.widget("", "Test Blog", "This is a test blog post.", "blog_1")
    app.add_blog_page("blog_1", "Test Blog", "blog_sample.md")
    with app.page("projects", "Projects") as page:
        page.heading("Projects")
        page.write("Here is a list of projects.")
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.write("About me!")
    app.compile(".")
