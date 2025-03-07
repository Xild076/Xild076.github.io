import os

class Page:
    def __init__(self, slug, title, website):
        self.slug = slug
        self.title = title
        self.website = website
        self.content = []
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.website.pages[self.slug] = {"title": self.title, "content": self.content}
    def heading(self, text, level=1):
        self.content.append(f"<h{level}>{text}</h{level}>")
    def write(self, text):
        self.content.append(f"<p>{text}</p>")
    def custom(self, html):
        self.content.append(html)
    def timeline_entry(self, date, event):
        entry_html = f'<div class="timeline-entry"><strong>{date}:</strong> {event}</div>'
        self.content.append(entry_html)
    def widget(self, image_url, title, description, link):
        widget_html = f'''
<div class="card" style="width: 18rem;">
  <a href="{link}">
    <img src="{image_url}" class="card-img-top" alt="{title}">
  </a>
  <div class="card-body">
    <h5 class="card-title">{title}</h5>
    <p class="card-text">{description}</p>
    <a href="{link}" class="btn btn-primary">Learn More</a>
  </div>
</div>
'''
        self.content.append(widget_html)
    def image(self, image_url, alt_text="", width=None, height=None):
        style = ""
        if width:
            style += f'width:{width}px;'
        if height:
            style += f'height:{height}px;'
        self.content.append(f'<img src="{image_url}" alt="{alt_text}" style="{style}">')
    def email_link(self, email, text=None):
        display_text = text if text else email
        self.content.append(f'<a href="mailto:{email}">{display_text}</a>')

class Website:
    def __init__(self, title):
        self.title = title
        self.pages = {}
    def page(self, slug, title):
        return Page(slug, title, self)
    def compile(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        nav_links = "".join([f'<li class="nav-item"><a class="nav-link" href="{slug}.html">{page["title"]}</a></li>' for slug, page in self.pages.items()])
        base_template = lambda title, content: f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<style>
.timeline-entry {{
  margin-bottom: 10px;
  padding: 10px;
  border-left: 3px solid #007bff;
}}
</style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="index.html">{self.title}</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav ml-auto">
      {nav_links}
    </ul>
  </div>
</nav>
<div class="container mt-5">
{content}
</div>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""
        for slug, page in self.pages.items():
            content = "\n".join(page["content"])
            html = base_template(page["title"], content)
            with open(os.path.join(output_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
                f.write(html)

if __name__ == "__main__":
    app = Website("My Site")
    with app.page("index", "Home") as page:
        page.heading("Welcome to My Site")
        page.write("Discover my work and projects.")
        page.widget("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fdog%2F&psig=AOvVaw05D1JMPT9UPjxPHbFhl0BI&ust=1741398584533000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCOD94bHt9osDFQAAAAAdAAAAABAE", "Sample Widget", "This is a clickable widget.", "blog.html")
        page.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fdog%2F&psig=AOvVaw05D1JMPT9UPjxPHbFhl0BI&ust=1741398584533000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCOD94bHt9osDFQAAAAAdAAAAABAE", "Sample Image", 300, 200)
        page.email_link("harry.d.yin.gpc@gmail.com", "Contact Me")
    with app.page("about", "About Me") as page:
        page.heading("About Me")
        page.write("Information about me goes here.")
    with app.page("blog", "Blog") as page:
        page.heading("Blog")
        page.write("Here is a list of blog posts.")
    with app.page("timeline", "Project Timeline") as page:
        page.heading("Project Timeline")
        page.timeline_entry("2025-01-01", "Project started")
        page.timeline_entry("2025-03-01", "First milestone reached")
    with app.page("news", "News") as page:
        page.heading("News")
        page.write("Latest news updates.")
    app.compile("site")
