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
        self.content.append(f'<a href="mailto:{email}">{display_text}</a><br>')
    def link(self, url, text=None):
        display_text = text if text else url
        self.content.append(f'<a href="{url}">{display_text}</a><br>')
    def code_block(self, code, language=""):
        self.content.append(f"<pre><code class='{language}'>{code}</code></pre>")
    def video(self, video_url, width=560, height=315):
        self.content.append(f'<iframe width="{width}" height="{height}" src="{video_url}" frameborder="0" allowfullscreen></iframe>')
    def blockquote(self, quote, author=None):
        if author:
            self.content.append(f"<blockquote class='blockquote theme-blockquote'><p><em>&ldquo;{quote}&rdquo;</em></p><footer class='blockquote-footer'><small>{author}</small></footer></blockquote>")
        else:
            self.content.append(f"<blockquote class='blockquote theme-blockquote'><p><em>&ldquo;{quote}&rdquo;</em></p></blockquote>")
    def alert_box(self, message, alert_type="info"):
        self.content.append(f'<div class="alert alert-{alert_type}" role="alert">{message}</div>')
    def gallery(self, images):
        gallery_html = '<div class="row">'
        for img in images:
            gallery_html += f'<div class="col-md-4"><img src="{img}" class="img-fluid"></div>'
        gallery_html += '</div>'
        self.content.append(gallery_html)
    def rotating_gallery(self, images, carousel_id="rotatingGallery", interval=3000):
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
    <div id="{carousel_id}" class="carousel slide" data-ride="carousel" data-interval="{interval}">
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
    def custom_rotating_gallery(self, images, container_width=800, container_height=600, interval=3000):
        self.content.append(f"""
        <div id="rotatingGallery" class="rotating-gallery-container" style="width: {container_width}px; height: {container_height}px; position: relative; overflow: hidden; margin: auto;">
            <div class="image-container" style="width: 100%; height: 100%; position: relative;">
                {''.join([f'<span style="position: absolute; display: block; width: 100%; height: 100%; top: 0; left: 0; opacity: {1 if i == 0 else 0}; transition: opacity 0.5s ease; z-index: 1;" data-index="{i}" class="{("active" if i == 0 else "")}"><img src="{img}" alt="Gallery Image" style="width: 100%; height: 100%; object-fit: cover;"></span>' for i, img in enumerate(images)])}
            </div>
            <div class="overlay" id="overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: none; justify-content: center; align-items: center; z-index: 2;">
                <img class="popup-img" id="popup-img" src="" alt="Popup Image" style="max-width: 90%; max-height: 90%; object-fit: cover;">
            </div>
            <div class="btn-container" style="position: absolute; bottom: 10px; width: 100%; display: flex; justify-content: space-between; padding: 0 20px; z-index: 3;">
                <button class="btn btn-secondary" id="prev">Left</button>
                <button class="btn btn-secondary" id="next">Right</button>
            </div>
        </div>
        <style>
        .rotating-gallery-container {{}}
        .image-container span.active {{ opacity: 1 !important; }}
        </style>
        <script>
        (function() {{
            var container = document.querySelector("#rotatingGallery .image-container");
            var spans = container.getElementsByTagName("span");
            var current = 0;
            
            function showImage(index) {{
                for (var i = 0; i < spans.length; i++) {{
                    spans[i].classList.remove("active");
                    spans[i].style.opacity = "0";
                }}
                spans[index].classList.add("active");
                spans[index].style.opacity = "1";
            }}
            
            // Make sure the first image is visible initially
            showImage(current);
            
            document.getElementById("next").addEventListener("click", function() {{
                current = (current + 1) % spans.length;
                showImage(current);
            }});
            
            document.getElementById("prev").addEventListener("click", function() {{
                current = (current - 1 + spans.length) % spans.length;
                showImage(current);
            }});
            
            // Auto-rotation
            var intervalId = setInterval(function() {{
                current = (current + 1) % spans.length;
                showImage(current);
            }}, {interval});
            
            // Stop auto-rotation when user interacts with gallery
            document.getElementById("next").addEventListener("click", function() {{
                clearInterval(intervalId);
            }});
            
            document.getElementById("prev").addEventListener("click", function() {{
                clearInterval(intervalId);
            }});
        }})();
        </script>
        """)
    def tabs(self, tabs, tab_id="tabsExample"):
        nav_html = f'<ul class="nav nav-tabs" id="{tab_id}" role="tablist">'
        content_html = f'<div class="tab-content mt-3" id="{tab_id}Content">'
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
            page.divider()
            if file_path.lower().endswith(".md"):
                html_content = convert_markdown_full(content)
                page.custom(html_content)
            else:
                page.write(content)
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
            papers_html = '<div class="paper-widgets">'
            for paper in papers:
                if len(paper) >= 4:
                    paper_title, paper_link, paper_type, paper_desc = paper
                else:
                    paper_title, paper_link, paper_type = paper
                    paper_desc = ""
                if paper_type.lower() == "md":
                    paper_slug = f"paper_{re.sub(r'\\W+', '', paper_title).lower()}"
                    self.add_blog_page(paper_slug, paper_title, paper_link)
                    link_target = f"{paper_slug}.html"
                else:
                    link_target = paper_link
                widget_html = f'''
<div class="card mb-3" style="max-width: 300px;">
  <a href="{link_target}" style="text-decoration: none; color: inherit;">
    <div class="row no-gutters">
      <div class="col-4" style="padding:0;">
        <img src="images/placeholder.png" class="card-img" alt="{paper_title}" style="width:100%; height:100%; object-fit:cover;">
      </div>
      <div class="col-8">
        <div class="card-body" style="padding: 0.5rem;">
          <h5 class="card-title" style="font-size:1rem;">{paper_title}</h5>
          <p class="card-text" style="font-size:0.8rem;">{paper_desc}</p>
        </div>
      </div>
    </div>
  </a>
</div>
'''
                papers_html += f'<div style="margin-bottom: 15px;">{widget_html}</div>'
            papers_html += '</div>'
            tech_html = ""
            if technologies is not None:
                tech_badges = ""
                for tech in technologies:
                    if isinstance(tech, tuple):
                        tech_name, tech_desc, tech_link = tech
                        tech_badges += f"<a href='{tech_link}' target='_blank' class='badge badge-primary badge-pill mr-2 mb-2' style='font-size:1.2em; padding:10px 15px;' title='{tech_desc}'>{tech_name}</a>"
                    else:
                        tech_badges += f"<span class='badge badge-primary badge-pill mr-2 mb-2' style='font-size:1.2em; padding:10px 15px;'>{tech}</span>"
                tech_html = f"<div class='project-technologies'><h5>Technologies Used</h5><div class='d-flex flex-wrap'>{tech_badges}</div></div>"
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
  width: 4px;
  background: #6c757d;
  transform: translateX(-50%);
}}
.timeline-item {{
  position: relative;
  width: 50%;
  padding: 20px;
  box-sizing: border-box;
  margin-bottom: 30px;
}}
.timeline-item.left {{
  left: 0;
  text-align: right;
}}
.timeline-item.right {{
  left: 50%;
  text-align: left;
}}
.timeline-content {{
  padding: 15px;
  background: #e9ecef;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
}}
.timeline-item.left .timeline-content::after {{
  content: "";
  position: absolute;
  top: 50%;
  right: -20px;
  width: 20px;
  height: 2px;
  background: #6c757d;
}}
.timeline-item.right .timeline-content::after {{
  content: "";
  position: absolute;
  top: 50%;
  left: -20px;
  width: 20px;
  height: 2px;
  background: #6c757d;
}}
.timeline-date {{
  font-weight: bold;
  margin-bottom: 6px;
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
html.dark-mode .timeline-content {{
  background: #444 !important;
  color: #dcdcdc !important;
}}
.theme-blockquote {{
    border-left: 4px solid #6c757d;
    padding-left: 1rem;
    color: #6c757d;
}}
html.dark-mode .theme-blockquote {{
    border-left-color: #dcdcdc;
    color: #dcdcdc;
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
  document.querySelectorAll('a[href="#top"]').forEach(function(link){{
    link.addEventListener("click", function(e){{
      e.preventDefault();
      window.scrollTo({{top: 0, behavior: "smooth"}});
    }});
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
