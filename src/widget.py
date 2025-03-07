import os
import re

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
        self.content.append(f'<div class="timeline-entry"><strong>{date}:</strong> {event}</div>')
    def widget(self, image_url, title, description, link):
        if not image_url:
            image_url = "images/placeholder.png"
        self.content.append(f'''
<div class="card mb-3" style="max-width: 540px;">
  <a href="{link}" style="text-decoration: none; color: inherit;">
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
        self.content.append(f'<a href="mailto:{email}">{display_text}</a>')
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
    def markdown(self, text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\~\~(.*?)\~\~', r'<del>\1</del>', text)
        self.content.append(text)
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
    def animated(self, html, animation="animate__bounce"):
        self.content.append(f'<div class="animate__animated {animation}">{html}</div>')
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

class Website:
    def __init__(self, title, footer="", custom_css="", custom_js=""):
        self.title = title
        self.footer = footer
        self.custom_css = custom_css
        self.custom_js = custom_js
        self.pages = {}
    def page(self, slug, title):
        return Page(slug, title, self)
    def compile(self, output_dir="."):
        if output_dir != "." and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        nav_links = "".join([f'<li class="nav-item"><a class="nav-link" href="{slug}.html">{page["title"]}</a></li>' for slug, page in self.pages.items()])
        base_template = lambda title, content: f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
<style>
body {{
  font-family: "Calibri", sans-serif;
  background-color: #f8f9fa;
  color: #212529;
  transition: background-color 0.3s, color 0.3s;
}}
body.dark-mode {{
  background-color: #121212;
  color: #e0e0e0;
}}
.navbar {{
  background-color: #007bff;
}}
.navbar.dark-mode {{
  background-color: #0056b3;
}}
.card {{
  background-color: #ffffff;
}}
body.dark-mode .card {{
  background-color: #1e1e1e;
}}
.timeline-entry {{
  margin-bottom: 10px;
  padding: 10px;
  border-left: 3px solid #007bff;
}}
{self.custom_css}
</style>
</head>
<body>
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
document.getElementById("toggleTheme").addEventListener("click", function() {{
  document.body.classList.toggle("dark-mode");
}});
{self.custom_js}
</script>
</body>
</html>
"""
        for slug, page in self.pages.items():
            content = "\n".join(page["content"])
            html = base_template(page["title"], content)
            file_path = os.path.join(output_dir, f"{slug}.html") if output_dir != "." else f"{slug}.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

