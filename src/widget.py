import os
import re
from datetime import datetime

try:
    import markdown as md
except ImportError:
    md = None

def convert_markdown_full(markdown_text):
    if md:
        return md.markdown(markdown_text)
    else:
        lines = markdown_text.splitlines()
        html_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            heading_match = re.match(r'^(#{1,6})\s*(.*)', line)
            if heading_match:
                level = len(heading_match.group(1))
                content = heading_match.group(2)
                html_lines.append(f"<h{level}>{content}</h{level}>")
            else:
                html_lines.append(f"<p>{line}</p>")
        html_content = "\n".join(html_lines)
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
        html_content = re.sub(r'\~\~(.*?)\~\~', r'<del>\1</del>', html_content)
        return html_content

class Page:
    def __init__(self, slug, title, website):
        self.slug = slug
        self.title = title
        self.website = website
        self.content = []
        self.is_blog = False
        self.is_project = False
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.website.pages[self.slug] = {"title": self.title, "content": self.content, "is_blog": self.is_blog, "is_project": self.is_project}
    def heading(self, text, level=1, align="left"):
        self.content.append(f"<h{level} style='text-align: {align};'>{text}</h{level}>")
    def write(self, text, align="left"):
        self.content.append(f"<p style='text-align: {align};'>{text}</p>")
    def custom(self, html):
        self.content.append(html)
    def timeline_entry(self, date, event, icon=""):
        icon_html = f"<i class='{icon}'></i> " if icon else ""
        self.content.append(f'<div class="timeline-item scroll-animate"><div class="timeline-date">{date}</div><div class="timeline-content">{icon_html}{event}</div></div>')
    def timeline_full(self, events):
        try:
            sorted_events = sorted(events, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
        except Exception:
            sorted_events = events
        timeline_html = '<div class="timeline">'
        for idx, (date, event) in enumerate(sorted_events):
            side = "left" if idx % 2 == 0 else "right"
            timeline_html += f'<div class="timeline-item {side} scroll-animate"><div class="timeline-date">{date}</div><div class="timeline-content">{event}</div></div>'
        timeline_html += '</div>'
        self.content.append(timeline_html)
    def widget(self, image_url, title, description, link):
        if not image_url:
            image_url = "images/placeholder.png"
        self.content.append(f'''
<div class="card mb-3" style="max-width: 540px;">
  <a href="{link}.html" style="text-decoration: none; color: inherit;">
    <div class="row no-gutters">
      <div class="col-md-4">
        <img src="{image_url}" class="card-img" alt="{title}">
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h5 class="card-title">{title}</h5>
          <p class="card-text">{description}</p>
        </div>
      </div>
    </div>
  </a>
</div>
''')
    def image(self, image_url, alt_text="", width=None, height=None):
        style = ""
        if width:
            style += f'width:{width}px;'
        if height:
            style += f'height:{height}px;'
        self.content.append(f'<img src="{image_url}" alt="{alt_text}" style="{style}">')
    def email_link(self, email, text=None):
        display_text = text if text else email
        self.content.append(f'<a href="mailto:{email}">{display_text}</a>\n')
    def link(self, url, text=None):
        display_text = text if text else url
        self.content.append(f'<a href="{url}">{display_text}</a>\n')
    def code_block(self, code, language=""):
        self.content.append(f"<pre><code class='{language}'>{code}</code></pre>")
    def video(self, video_url, width=560, height=315):
        self.content.append(f'<iframe width="{width}" height="{height}" src="{video_url}" frameborder="0" allowfullscreen></iframe>')
    def blockquote(self, quote, author=None):
        if author:
            self.content.append(f"<blockquote class='blockquote'><p>{quote}</p><footer class='blockquote-footer'>{author}</footer></blockquote>")
        else:
            self.content.append(f"<blockquote class='blockquote'><p>{quote}</p></blockquote>")
    def alert_box(self, message, alert_type="info"):
        self.content.append(f'<div class="alert alert-{alert_type}" role="alert">{message}</div>')
    def gallery(self, images):
        gallery_html = '<div class="row">'
        for img in images:
            gallery_html += f'<div class="col-md-4"><img src="{img}" class="img-fluid"></div>'
        gallery_html += '</div>'
        self.content.append(gallery_html)
    def markdown(self, text, align="left"):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\~\~(.*?)\~\~', r'<del>\1</del>', text)
        self.content.append(f"<p style='text-align: {align};'>{text}</p>")
    def list(self, items, ordered=False):
        tag = "ol" if ordered else "ul"
        list_html = f"<{tag}>" + "".join([f"<li>{item}</li>" for item in items]) + f"</{tag}>"
        self.content.append(list_html)
    def accordion(self, sections, accordion_id="accordionExample"):
        accordion_html = f'<div class="accordion" id="{accordion_id}">'
        for idx, (header, body) in enumerate(sections):
            accordion_html += f'''
<div class="card">
  <div class="card-header" id="heading{idx}">
    <h2 class="mb-0">
      <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{idx}" aria-expanded="true" aria-controls="collapse{idx}">
        {header}
      </button>
    </h2>
  </div>
  <div id="collapse{idx}" class="collapse" aria-labelledby="heading{idx}" data-parent="#{accordion_id}">
    <div class="card-body">
      {body}
    </div>
  </div>
</div>
'''
        accordion_html += "</div>"
        self.content.append(accordion_html)
    def tabs(self, tabs, tab_id="tabsExample"):
        nav_html = f'<ul class="nav nav-tabs" id="{tab_id}" role="tablist">'
        content_html = f'<div class="tab-content" id="{tab_id}Content">'
        for idx, (tab_title, tab_content) in enumerate(tabs):
            active = "active" if idx == 0 else ""
            nav_html += f'<li class="nav-item"><a class="nav-link {active}" id="tab{idx}" data-toggle="tab" href="#content{idx}" role="tab">{tab_title}</a></li>'
            content_html += f'<div class="tab-pane fade show {active}" id="content{idx}" role="tabpanel">{tab_content}</div>'
        nav_html += '</ul>'
        content_html += '</div>'
        self.content.append(nav_html + content_html)
    def tooltip(self, text, tooltip_text):
        self.content.append(f'<span data-toggle="tooltip" title="{tooltip_text}">{text}</span>')
    def map(self, location, width=600, height=450):
        self.content.append(f'<iframe src="https://www.google.com/maps?q={location}&output=embed" width="{width}" height="{height}" frameborder="0" style="border:0;" allowfullscreen aria-hidden="false" tabindex="0"></iframe>')
    def animated(self, html, animation="animate__fadeInUp"):
        self.content.append(f'<div class="animate__animated {animation} scroll-animate">{html}</div>')
    def container(self, content, class_name="container"):
        self.content.append(f'<div class="{class_name}">{content}</div>')
    def divider(self):
        self.content.append('<hr>')
    def button(self, text, link, style="primary"):
        self.content.append(f'<a href="{link}" class="btn btn-{style}">{text}</a>')
    def jumbotron(self, title, subtitle, button_text=None, button_link=None):
        btn_html = f'<a class="btn btn-primary btn-lg" href="{button_link}" role="button">{button_text}</a>' if button_text and button_link else ""
        self.content.append(f'''
<div class="jumbotron">
  <h1 class="display-4">{title}</h1>
  <p class="lead">{subtitle}</p>
  {btn_html}
</div>
''')
    def carousel(self, images, carousel_id="carouselExample"):
        indicators = "".join([f'<li data-target="#{carousel_id}" data-slide-to="{i}" {"class=\'active\'" if i==0 else ""}></li>' for i in range(len(images))])
        slides = ""
        for i, img in enumerate(images):
            active = "active" if i == 0 else ""
            slides += f'''
<div class="carousel-item {active}">
  <img src="{img}" class="d-block w-100" alt="Slide {i+1}">
</div>
'''
        self.content.append(f'''
<div id="{carousel_id}" class="carousel slide" data-ride="carousel">
  <ol class="carousel-indicators">
    {indicators}
  </ol>
  <div class="carousel-inner">
    {slides}
  </div>
  <a class="carousel-control-prev" href="#{carousel_id}" role="button" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="carousel-control-next" href="#{carousel_id}" role="button" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>
''')
    def row(self, columns):
        row_html = '<div class="row">'
        for col in columns:
            row_html += f'<div class="col">{col}</div>'
        row_html += '</div>'
        self.content.append(row_html)
    def spacer(self, height):
        self.content.append(f'<div style="height: {height}px;"></div>')
    def import_text(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        paragraphs = content.split("\n\n")
        for para in paragraphs:
            self.markdown(para)
            self.content.append("<br>")

class Website:
    def __init__(self, title, footer="", custom_css="", custom_js=""):
        self.title = title
        self.footer = footer
        self.custom_css = custom_css
        self.custom_js = custom_js
        self.pages = {}
    def page(self, slug, title):
        return Page(slug, title, self)
    def add_blog_page(self, slug, title, file_path, date=None, featured_image=None, author=None):
        with self.page(slug, title) as page:
            page.is_blog = True
            if featured_image:
                page.image(featured_image)
            page.heading(title)
            if date:
                page.write(f"<small>{date}</small>")
            if author:
                page.write(f"<small>By {author}</small>")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            word_count = len(content.split())
            read_time = max(1, round(word_count / 200))
            page.write(f"<small>Estimated read time: {read_time} minute{'s' if read_time != 1 else ''}</small>")
            if file_path.lower().endswith(".md"):
                html_content = convert_markdown_full(content)
                page.custom(html_content)
            else:
                page.write(content)
            share_html = f'<div class="share-links"><a href="https://twitter.com/share?url={slug}.html">Twitter</a> | <a href="https://www.facebook.com/sharer/sharer.php?u={slug}.html">Facebook</a> | <a href="https://www.linkedin.com/shareArticle?mini=true&url={slug}.html">LinkedIn</a></div>'
            page.custom(share_html)
        return page
    def add_project_page(self, slug, title, timeline_events, project_intro, github_gist_url, github_desc, papers, technologies=None):
        with self.page(slug, title) as page:
            page.is_project = True
            with open(project_intro, "r", encoding="utf-8") as f:
                project_intro = f.read().strip()
            intro_html = '<div style="height: 10px;"></div>' + convert_markdown_full(project_intro)
            try:
                sorted_events = sorted(timeline_events, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)
            except Exception:
                sorted_events = timeline_events
            timeline_html = '<div class="timeline">'
            for idx, (date, event) in enumerate(sorted_events):
                side = "left" if idx % 2 == 0 else "right"
                timeline_html += f'''
<div class="timeline-item {side} scroll-animate">
  <div class="timeline-date">{date}</div>
  <div class="timeline-content">{event}</div>
</div>
'''
            timeline_html += '</div>'
            code_html = '<div style="height: 10px;"></div>' + f"<p>{github_desc}</p>" + f'<script src="{github_gist_url}.js"></script>'
            papers_html = '<div style="height: 10px;"></div>'
            for paper in papers:
                if len(paper) >= 4:
                    paper_title, paper_link, paper_type, paper_desc = paper
                else:
                    paper_title, paper_link, paper_type = paper
                    paper_desc = ""
                if paper_type.lower() == "md":
                    paper_slug = f"paper_{re.sub(r'\\W+', '', paper_title).lower()}"
                    self.add_blog_page(paper_slug, paper_title, paper_link)
                    papers_html += f'<div class="paper-section"><h5>{paper_title}</h5><p>{paper_desc}</p><p><a href="{paper_slug}.html" target="_blank">View Paper</a></p></div>'
                else:
                    papers_html += f'<div class="paper-section"><h5>{paper_title}</h5><p>{paper_desc}</p><p><a href="{paper_link}" target="_blank">View PDF</a></p></div>'
            tech_html = ""
            if technologies is not None:
                tech_html = "<div class='project-technologies'><h5>Technologies Used</h5><ul>" + "".join([f"<li>{tech}</li>" for tech in technologies]) + "</ul></div>"
            tabs = [("Introduction", intro_html), ("Timeline", timeline_html)]
            if tech_html:
                tabs.append(("Technologies", tech_html))
            tabs.extend([("Code", code_html), ("Papers", papers_html)])
            page.tabs(tabs)
        return page
    def compile(self, output_dir="."):
        if output_dir != "." and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        nav_links = "".join([f'<li class="nav-item"><a class="nav-link" href="{slug}.html">{data["title"]}</a></li>' 
                             for slug, data in self.pages.items() if not data.get("is_blog") and not data.get("is_project")])
        base_template = lambda title, content: f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script>
if(localStorage.getItem('theme')==='dark'){{document.documentElement.classList.add('dark-mode');}}
</script>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
<style>
body {{
  font-family: 'Roboto', sans-serif;
  background-color: #f5f5f5;
  color: #333;
  transition: background-color 0.3s, color 0.3s;
}}
html.dark-mode body {{
  background-color: #2e2e2e;
  color: #dcdcdc;
}}
.navbar {{
  background-color: #6c757d;
}}
.navbar.dark-mode {{
  background-color: #343a40;
}}
.card {{
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: none;
}}
html.dark-mode .card {{
  background-color: #3a3a3a;
}}
.timeline {{
  position: relative;
  max-width: 800px;
  margin: 40px auto;
  padding: 20px 0;
}}
.timeline::before {{
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 2px;
  background: #ccc;
  transform: translateX(-50%);
}}
.timeline-item {{
  padding: 20px;
  position: relative;
  width: 50%;
  box-sizing: border-box;
}}
.timeline-item.left {{
  left: 0;
  text-align: right;
}}
.timeline-item.right {{
  left: 50%;
  text-align: left;
}}
.timeline-item::after {{
  content: "";
  position: absolute;
  top: 15px;
  width: 12px;
  height: 12px;
  background: #fff;
  border: 2px solid #6c757d;
  border-radius: 50%;
  z-index: 1;
}}
.timeline-item.left::after {{
  right: -6px;
}}
.timeline-item.right::after {{
  left: -6px;
}}
.timeline-date {{
  font-weight: bold;
  margin-bottom: 6px;
}}
.timeline-content {{
  padding: 15px;
  background: #e9ecef;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
html.dark-mode .timeline-content {{
  background: #444;
}}
.scroll-animate {{
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}}
.animate__fadeInUp {{
  opacity: 1 !important;
  transform: translateY(0) !important;
}}
{self.custom_css}
</style>
</head>
<body>
<a id="top"></a>
<nav class="navbar navbar-expand-lg navbar-dark">
  <a class="navbar-brand" href="index.html">{self.title}</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav ml-auto">
      {nav_links}
      <li class="nav-item">
        <button id="toggleTheme" class="btn btn-secondary">Toggle Theme</button>
      </li>
    </ul>
  </div>
</nav>
<div class="container mt-5">
{content}
<div style="text-align: center; margin: 20px;"><a href="#top" class="btn btn-secondary">Back to top</a></div>
</div>
<footer class="footer mt-5">
  <div class="container">
    <span class="text-muted">{self.footer}</span>
  </div>
</footer>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {{
  const observer = new IntersectionObserver((entries, observer) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
        observer.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.3 }});
  document.querySelectorAll('.scroll-animate').forEach(el => observer.observe(el));
  document.getElementById("toggleTheme").addEventListener("click", function() {{
    document.documentElement.classList.toggle("dark-mode");
    if(document.documentElement.classList.contains("dark-mode")) {{
      localStorage.setItem('theme', 'dark');
    }} else {{
      localStorage.setItem('theme', 'light');
    }}
  }});
  {self.custom_js}
}});
</script>
</body>
</html>
"""
        for slug, data in self.pages.items():
            content = "\n".join(data["content"])
            html = base_template(data["title"], content)
            file_path = os.path.join(output_dir, f"{slug}.html") if output_dir != "." else f"{slug}.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

"""
if __name__ == "__main__":
    app = Website("My Site", footer="&copy; 2025 Harry. All rights reserved.",
                  custom_css="body { padding-bottom: 50px; }", custom_js="console.log('Custom JS loaded');")
    with app.page("index", "Home") as page:
        page.heading("Welcome to My Site", align="center")
        page.write("Discover my work and projects.", align="center")
        page.widget("", "Sample Widget", "This is a clickable widget linking to our blog.", "blog_1")
        page.image("https://via.placeholder.com/300x200", "Sample Image", 300, 200)
        page.email_link("example@example.com", "Contact Us")
        page.video("https://www.youtube.com/embed/dQw4w9WgXcQ")
        page.code_block("print('Hello, world!')", "python")
        page.blockquote("This is an inspiring quote.", "Author Name")
        page.alert_box("This is an important alert!", "warning")
        page.gallery(["https://via.placeholder.com/200", "https://via.placeholder.com/200", "https://via.placeholder.com/200"])
        page.markdown("This is **bold** text and *italic* text with ~~strikethrough~~.", align="center")
        page.list(["Item 1", "Item 2", "Item 3"])
        page.accordion([("Section 1", "Content for section 1."), ("Section 2", "Content for section 2.")])
        page.tabs([("Tab 1", "Content for tab 1."), ("Tab 2", "Content for tab 2.")])
        page.tooltip("Hover over me", "This is a tooltip")
        page.map("New York, NY", 600, 450)
        page.animated("<p>This text fades in on scroll!</p>")
        page.container("<p>This is inside a container.</p>")
        page.divider()
        page.button("Click Me", "https://example.com")
        page.jumbotron("Jumbotron Title", "This is a jumbotron subtitle.", "Learn More", "https://example.com")
        page.carousel(["https://via.placeholder.com/800x400", "https://via.placeholder.com/800x400", "https://via.placeholder.com/800x400"])
        page.row(["Column 1 content", "Column 2 content", "Column 3 content"])
        page.spacer(50)
        page.timeline_full([("2025-01-01", "Project initiated."), ("2025-02-15", "First milestone reached."), ("2025-04-01", "Beta launch."), ("2025-06-30", "Official release.")])
    with app.page("about", "About Me") as page:
        page.heading("About Me", align="center")
        page.write("Information about me goes here.", align="center")
    app.add_blog_page("blog_1", "Test Blog", "blog_sample.md", date="2025-03-07", featured_image="https://via.placeholder.com/600x300", author="Harry")
    app.add_project_page("project_1", "Project One",
                          [("2021-01-01", "Project started"), ("2021-06-01", "Prototype completed"), ("2021-12-31", "Official release")],
                          "project_intro.md",
                          "https://gist.github.com/username/gistid",
                          "This project demonstrates the awesome features of our site.",
                          [("Paper One", "http://linktopaper1.com", "pdf", "A description of Paper One."),
                           ("Paper Two", "blog_paper_sample.md", "md", "A description of Paper Two.")],
                          technologies=["Python", "Flask", "Docker"])
    with app.page("news", "News") as page:
        page.heading("News", align="center")
        page.write("Latest news updates.", align="center")
    app.compile(".")
"""
