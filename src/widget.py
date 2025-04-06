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
    html_content = re.sub(r'\`(.*?)\`', r'<code>\1</code>', html_content)
    html_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html_content)
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
        self.website.pages[self.slug] = {
            "title": self.title,
            "content": self.content,
            "is_blog": self.is_blog,
            "is_project": self.is_project
        }
        
    def heading(self, text, level=1, align="left"):
        self.content.append(f"<h{level} class='heading heading-{level}' style='text-align: {align};'>{text}</h{level}>")
        
    def write(self, text, align="left"):
        self.content.append(f"<p class='content-paragraph' style='text-align: {align};'>{text}</p>")
        
    def custom(self, html):
        self.content.append(html)
        
    def timeline_entry(self, date, event, icon=""):
        icon_html = f"<i class='{icon}'></i> " if icon else ""
        self.content.append(f'<div class="timeline-item scroll-animate"><div class="timeline-date">{date}</div><div class="timeline-content">{icon_html}{event}</div></div>')
        
    def timeline_full(self, events):
        try:
            sorted_events = sorted(events, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
        except:
            sorted_events = events
            
        timeline_html = '<div class="timeline">'
        for idx, (date, event) in enumerate(sorted_events):
            side = "left" if idx % 2 == 0 else "right"
            timeline_html += f'<div class="timeline-item {side} scroll-animate"><div class="timeline-date">{date}</div><div class="timeline-content">{event}</div></div>'
        timeline_html += '</div>'
        self.content.append(timeline_html)
        
    def widget(self, image_url, title, description, link):
        image_url = image_url or "images/placeholder.png"
        self.content.append(f'''
<div class="card widget-card mb-3">
  <a href="{link}.html" class="widget-card-link">
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
        
    def image(self, image_url, alt_text="", width=None, height=None, wrap=None, crop=False, shrink=False, smart_fit=False, caption=""):
        img_style = ""
        figure_style = ""
        
        if width:
            img_style += f'{"width" if smart_fit or not shrink else "max-width"}:{width}px;'
        if height:
            img_style += f'{"height" if smart_fit else "height"}:{height}px;'
        if crop or smart_fit:
            img_style += " object-fit:cover;"
        elif shrink:
            img_style += " object-fit:contain;"
            
        if wrap in ["left", "right"]:
            margin_style = f"float:{wrap}; margin:0 {0 if wrap == 'right' else 20}px 20px {20 if wrap == 'right' else 0}px;"
            figure_style = margin_style if caption else ""
            img_style += margin_style if not caption else ""
            
        if caption:
            self.content.append(
                f'<figure class="image-figure" style="{figure_style}">'
                f'<img src="{image_url}" alt="{alt_text}" class="enhanced-image" style="{img_style}">'
                f'<figcaption class="image-caption">{caption}</figcaption></figure>'
            )
        else:
            self.content.append(
                f'<img src="{image_url}" alt="{alt_text}" class="enhanced-image" style="{img_style}">'
            )
            
    def email_link(self, email, text=None, newline=True):
        display_text = text if text else email
        newline_tag = "<br>" if newline else ""
        self.content.append(f'<a href="mailto:{email}" class="email-link">{display_text}</a>{newline_tag}')
        
    def link(self, url, text=None, newline=True):
        display_text = text if text else url
        newline_tag = "<br>" if newline else ""
        self.content.append(f'<a href="{url}" class="site-link">{display_text}</a>{newline_tag}')
        
    def code_block(self, code, language=""):
        self.content.append(f"<pre class='code-block'><code class='language-{language}'>{code}</code></pre>")
        
    def video(self, video_url, width=560, height=315):
        self.content.append(f'<div class="video-container"><iframe width="{width}" height="{height}" src="{video_url}" frameborder="0" allowfullscreen></iframe></div>')
        
    def blockquote(self, quote, author=None):
        author_html = f'<footer class="blockquote-footer"><small>{author}</small></footer>' if author else ''
        self.content.append(f"<blockquote class='blockquote theme-blockquote'><p><em>&ldquo;{quote}&rdquo;</em></p>{author_html}</blockquote>")
        
    def alert_box(self, message, alert_type="info"):
        self.content.append(f'<div class="alert alert-{alert_type}" role="alert">{message}</div>')
        
    def gallery(self, images):
        gallery_html = '<div class="gallery-grid row">'
        for img in images:
            gallery_html += f'<div class="col-md-4 gallery-item"><img src="{img}" class="img-fluid gallery-image"></div>'
        gallery_html += '</div>'
        self.content.append(gallery_html)
        
    def rotating_gallery(self, images, container_width=800, container_height=600, interval=3000, smart_fit=False, captions=None):
        captions_js = "null"
        if captions and isinstance(captions, list) and len(captions) == len(images):
            captions_js = '[' + ','.join(f'"{cap}"' for cap in captions) + ']'
            
        image_spans = ''.join([
            f'<span class="gallery-slide {("active" if i==0 else "")}" data-index="{i}"><img src="{img}" alt="Gallery Image" class="gallery-slide-image"></span>' 
            for i, img in enumerate(images)
        ])
        
        gallery_html = f"""
        <div id="rotatingGallery" class="rotating-gallery-container" style="width:{container_width}px; height:{container_height}px;">
            <div class="image-container">{image_spans}</div>
            <div class="overlay" id="overlay">
                <img class="popup-img" id="popup-img" src="" alt="Popup Image">
            </div>
            <div class="btn-container">
                <button class="btn btn-secondary" id="prev">Left</button>
                <button class="btn btn-secondary" id="next">Right</button>
            </div>
        </div>
        """
        
        if captions and isinstance(captions, list) and len(captions) == len(images):
            gallery_html += f'<div id="galleryCaption" class="gallery-caption">{captions[0]}</div>'
            
        self.content.append(gallery_html)
        self.content.append(f"""
        <script>
        (function() {{
            const container = document.querySelector("#rotatingGallery .image-container");
            const spans = container.getElementsByTagName("span");
            let current = 0;
            const captions = {captions_js};
            const captionElem = document.getElementById("galleryCaption");
            
            function showImage(index) {{
                for (let i = 0; i < spans.length; i++) {{
                    spans[i].classList.remove("active");
                    spans[i].style.opacity = "0";
                }}
                spans[index].classList.add("active");
                spans[index].style.opacity = "1";
                if (captions && captionElem) {{
                    captionElem.innerText = captions[index];
                }}
            }}
            
            showImage(current);
            
            const nextBtn = document.getElementById("next");
            const prevBtn = document.getElementById("prev");
            
            nextBtn.addEventListener("click", function() {{
                current = (current + 1) % spans.length;
                showImage(current);
            }});
            
            prevBtn.addEventListener("click", function() {{
                current = (current - 1 + spans.length) % spans.length;
                showImage(current);
            }});
            
            let intervalId = setInterval(function() {{
                current = (current + 1) % spans.length;
                showImage(current);
            }}, {interval});
            
            [nextBtn, prevBtn].forEach(btn => {{
                btn.addEventListener("click", () => clearInterval(intervalId));
            }});
        }})();
        </script>
        """)
        
    def tabs(self, tabs, tab_id="tabsExample"):
        nav_html = f'<ul class="nav nav-tabs custom-tabs" id="{tab_id}" role="tablist">'
        content_html = f'<div class="tab-content custom-tab-content mt-3" id="{tab_id}Content">'
        
        for idx, (tab_title, tab_content) in enumerate(tabs):
            active = "active" if idx == 0 else ""
            nav_html += f'<li class="nav-item"><a class="nav-link {active}" id="tab{idx}" data-toggle="tab" href="#content{idx}" role="tab">{tab_title}</a></li>'
            content_html += f'<div class="tab-pane fade show {active}" id="content{idx}" role="tabpanel">{tab_content}</div>'
            
        nav_html += '</ul>'
        content_html += '</div>'
        self.content.append(nav_html + content_html)
        
    def tooltip(self, text, tooltip_text):
        self.content.append(f'<span class="custom-tooltip" data-toggle="tooltip" title="{tooltip_text}">{text}</span>')
        
    def map(self, location, width=600, height=450):
        self.content.append(f'<div class="map-container"><iframe src="https://www.google.com/maps?q={location}&output=embed" width="{width}" height="{height}" frameborder="0" allowfullscreen aria-hidden="false" tabindex="0"></iframe></div>')
        
    def animated(self, html, animation="animate__fadeInUp"):
        self.content.append(f'<div class="animate__animated {animation} scroll-animate">{html}</div>')
        
    def container(self, content, class_name="container"):
        self.content.append(f'<div class="{class_name}">{content}</div>')
        
    def divider(self):
        self.content.append('<hr class="custom-divider">')
        
    def button(self, text, link, style="primary", size="md", icon=""):
        icon_html = f'<i class="{icon} btn-icon"></i> ' if icon else ""
        self.content.append(f'<a href="{link}" class="btn btn-{style} btn-{size}">{icon_html}{text}</a>')
        
    def file_download(self, file_url, text="Download File", download=True, icon=""):
        download_attr = 'download' if download else 'target="_blank" rel="noopener noreferrer"'
        icon_html = f'<i class="{icon} download-icon"></i> ' if icon else ""
        self.content.append(f'<a href="{file_url}" {download_attr} class="btn btn-primary download-btn">{icon_html}{text}</a>')
        
    def jumbotron(self, title, subtitle, button_text=None, button_link=None, bg_image=None):
        style = f'background-image: url({bg_image}); background-size: cover; background-position: center;' if bg_image else ''
        btn_html = f'<a class="btn btn-primary btn-lg action-btn" href="{button_link}" role="button">{button_text}</a>' if button_text and button_link else ""
        self.content.append(f'''
<div class="jumbotron custom-jumbotron" style="{style}">
  <h1 class="display-4">{title}</h1>
  <p class="lead">{subtitle}</p>
  {btn_html}
</div>
''')
        
    def carousel(self, images, carousel_id="carouselExample"):
        indicators = "".join([
            f'<li data-target="#{carousel_id}" data-slide-to="{i}" {"class=\'active\'" if i==0 else ""}></li>' 
            for i in range(len(images))
        ])
        
        slides = "".join([
            f'<div class="carousel-item {("active" if i==0 else "")}"><img src="{img}" class="d-block w-100" alt="Slide {i+1}"></div>'
            for i, img in enumerate(images)
        ])
        
        self.content.append(f'''
<div id="{carousel_id}" class="carousel slide custom-carousel" data-ride="carousel">
  <ol class="carousel-indicators">{indicators}</ol>
  <div class="carousel-inner">{slides}</div>
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
        
    def row(self, columns, equal_height=True):
        row_class = "row h-100" if equal_height else "row"
        row_html = f'<div class="{row_class}">'
        for col in columns:
            row_html += f'<div class="col">{col}</div>'
        row_html += '</div>'
        self.content.append(row_html)
        
    def spacer(self, height):
        self.content.append(f'<div class="spacer" style="height:{height}px;"></div>')
        
    def import_text(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            content = convert_markdown_full(content)
            self.content.append(content)
        except Exception as e:
            self.content.append(f'<div class="alert alert-danger">Error loading file: {e}</div>')
            
    def accordion(self, items, accordion_id="accordionExample"):
        accordion_html = f'<div class="accordion custom-accordion" id="{accordion_id}">'
        
        for idx, (title, content) in enumerate(items):
            accordion_html += f'''
<div class="card accordion-card">
  <div class="card-header" id="heading{idx}">
    <h2 class="mb-0">
      <button class="btn btn-link accordion-btn" type="button" data-toggle="collapse" data-target="#collapse{idx}">
        {title}
      </button>
    </h2>
  </div>
  <div id="collapse{idx}" class="collapse" aria-labelledby="heading{idx}" data-parent="#{accordion_id}">
    <div class="card-body accordion-content">
      {content}
    </div>
  </div>
</div>'''
        
        accordion_html += '</div>'
        self.content.append(accordion_html)
    
    def progress_bar(self, percentage, label=None, style="primary", height=20, striped=False, animated=False):
        label_html = label if label else f"{percentage}%"
        striped_class = "progress-bar-striped" if striped else ""
        animated_class = "progress-bar-animated" if animated else ""
        
        self.content.append(f'''
<div class="progress" style="height: {height}px;">
  <div class="progress-bar bg-{style} {striped_class} {animated_class}" role="progressbar" 
       style="width: {percentage}%" aria-valuenow="{percentage}" aria-valuemin="0" aria-valuemax="100">
    {label_html}
  </div>
</div>
''')
    
    def card(self, title, content, image=None, footer=None, style="primary", outline=False):
        card_class = f"card-outline-{style}" if outline else ""
        image_html = f'<img src="{image}" class="card-img-top" alt="{title}">' if image else ""
        footer_html = f'<div class="card-footer">{footer}</div>' if footer else ""
        
        self.content.append(f'''
<div class="card custom-card {card_class} mb-3">
  {image_html}
  <div class="card-body">
    <h5 class="card-title">{title}</h5>
    <div class="card-text">{content}</div>
  </div>
  {footer_html}
</div>
''')

    def social_share(self, url, title="", platforms=None):
        if platforms is None:
            platforms = ["facebook", "twitter", "linkedin", "email"]
            
        share_html = '<div class="social-share">'
        
        encoded_url = url.replace("&", "%26").replace("?", "%3F")
        encoded_title = title.replace(" ", "%20")
        
        for platform in platforms:
            if platform == "facebook":
                share_html += f'<a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank" class="social-btn facebook-btn">Facebook</a>'
            elif platform == "twitter":
                share_html += f'<a href="https://twitter.com/intent/tweet?url={encoded_url}&text={encoded_title}" target="_blank" class="social-btn twitter-btn">Twitter</a>'
            elif platform == "linkedin":
                share_html += f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" target="_blank" class="social-btn linkedin-btn">LinkedIn</a>'
            elif platform == "email":
                share_html += f'<a href="mailto:?subject={encoded_title}&body={encoded_url}" class="social-btn email-btn">Email</a>'
        
        share_html += '</div>'
        self.content.append(share_html)
    
    def modal(self, trigger_text, title, content, modal_id, trigger_style="btn-primary"):
        self.content.append(f'''
<button type="button" class="btn {trigger_style}" data-toggle="modal" data-target="#{modal_id}">
  {trigger_text}
</button>

<div class="modal fade" id="{modal_id}" tabindex="-1" role="dialog" aria-labelledby="{modal_id}Label" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="{modal_id}Label">{title}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        {content}
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
''')
    
    def masonry_grid(self, items, columns=3):
        grid_html = f'<div class="masonry-grid" style="column-count: {columns};">'
        
        for item in items:
            grid_html += f'<div class="masonry-item">{item}</div>'
            
        grid_html += '</div>'
        self.content.append(grid_html)
    
    def breadcrumbs(self, items):
        breadcrumb_html = '<nav aria-label="breadcrumb"><ol class="breadcrumb">'
        
        for i, (text, link) in enumerate(items):
            if i == len(items) - 1:
                breadcrumb_html += f'<li class="breadcrumb-item active" aria-current="page">{text}</li>'
            else:
                breadcrumb_html += f'<li class="breadcrumb-item"><a href="{link}">{text}</a></li>'
                
        breadcrumb_html += '</ol></nav>'
        self.content.append(breadcrumb_html)
    
    def feature_box(self, icon, title, text, bg_color="#f8f9fa", text_color="#212529"):
        self.content.append(f'''
<div class="feature-box" style="background-color: {bg_color}; color: {text_color};">
  <div class="feature-icon"><i class="{icon}"></i></div>
  <h4 class="feature-title">{title}</h4>
  <div class="feature-text">{text}</div>
</div>
''')
    
    def pricing_table(self, plans):
        table_html = '<div class="pricing-container row">'
        
        for plan in plans:
            name = plan.get("name", "Basic")
            price = plan.get("price", "$0")
            period = plan.get("period", "month")
            features = plan.get("features", [])
            cta_text = plan.get("cta_text", "Sign Up")
            cta_link = plan.get("cta_link", "#")
            featured = plan.get("featured", False)
            
            featured_class = " featured" if featured else ""
            
            feature_list = ""
            for feature in features:
                feature_list += f'<li class="pricing-feature">{feature}</li>'
                
            table_html += f'''
<div class="col-lg-4 col-md-6 mb-4">
  <div class="pricing-card{featured_class}">
    <div class="pricing-header">
      <h3 class="pricing-title">{name}</h3>
      <div class="pricing-price">{price}</div>
      <div class="pricing-period">per {period}</div>
    </div>
    <ul class="pricing-features">
      {feature_list}
    </ul>
    <div class="pricing-footer">
      <a href="{cta_link}" class="btn btn-primary pricing-button">{cta_text}</a>
    </div>
  </div>
</div>'''
            
        table_html += '</div>'
        self.content.append(table_html)

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
                page.write(f"<small class='blog-date'>{date}</small>")
                
            if author:
                page.write(f"<small class='blog-author'>By {author}</small>")
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    
                word_count = len(content.split())
                read_time = max(1, round(word_count / 200))
                page.write(f"<small class='read-time'>Estimated read time: {read_time} minute{'s' if read_time != 1 else ''}</small>")
                
                page.divider()
                
                if file_path.lower().endswith(".md"):
                    html_content = convert_markdown_full(content)
                    page.custom(html_content)
                elif file_path.lower().endswith(".html"):
                    if "<body" in content.lower():
                        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
                        if body_match:
                            body_content = body_match.group(1)
                        else:
                            body_content = content
                        page.custom(body_content)
                    else:
                        page.custom(content)
                else:
                    page.write(content)
            except Exception as e:
                page.alert_box(f"Error loading blog content: {e}", "danger")
                
        return page
        
    def add_project_page(self, slug, title, timeline_events, project_intro, github_owner, github_repo, papers, technologies=None):
        with self.page(slug, title) as page:
            page.is_project = True
            
            try:
                with open(project_intro, "r", encoding="utf-8") as f:
                    project_intro = f.read().strip()
                    
                intro_html = '<div class="project-intro">' + convert_markdown_full(project_intro) + '</div>'
                
                try:
                    sorted_events = sorted(timeline_events, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)
                except:
                    sorted_events = timeline_events
                    
                timeline_html = '<div class="timeline project-timeline">'
                for idx, (date, event) in enumerate(sorted_events):
                    side = "left" if idx % 2 == 0 else "right"
                    timeline_html += f'''
                <div class="timeline-item {side} scroll-animate">
                <div class="timeline-date">{date}</div>
                <div class="timeline-content">{event}</div>
                </div>
                '''
                timeline_html += '</div>'

                code_html = f'''
                <div id="codeViewerContainer" class="code-viewer-container mb-3">
                <div id="fileList" class="file-list"></div>
                <div id="codeViewer" class="code-viewer"></div>
                <a href="https://github.com/{github_owner}/{github_repo}" target="_blank" class="btn btn-secondary mt-2">
                    Star on GitHub
                </a>
                </div>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/codemirror.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/javascript/javascript.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/python/python.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/htmlmixed/htmlmixed.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/mode/css/css.min.js"></script>
                <script>
                const repoOwner = "{github_owner}";
                const repoName = "{github_repo}";
                const fileListElem = document.getElementById("fileList");
                const codeViewerElem = document.getElementById("codeViewer");
                const editor = CodeMirror(codeViewerElem, {{
                    value: "",
                    mode: "javascript",
                    lineNumbers: true,
                    lineWrapping: true,
                    theme: document.documentElement.classList.contains('dark-mode') ? 'material-darker' : 'default'
                }});
                
                editor.setSize("100%", "100%");
                let currentPath = "";
                
                function getLanguageFromFilename(filename) {{
                    const ext = filename.split('.').pop().toLowerCase();
                    const mapping = {{
                        'js': 'javascript',
                        'py': 'python',
                        'html': 'htmlmixed',
                        'css': 'css',
                        'json': 'application/json',
                        'md': 'markdown',
                        'txt': 'text'
                    }};
                    return mapping[ext] || 'text';
                }}

                function loadFileContent(path) {{
                    fetch(`https://api.github.com/repos/${{repoOwner}}/${{repoName}}/contents/${{path}}`)
                        .then(r => r.json())
                        .then(data => {{
                            if (data.encoding && data.encoding === 'base64') {{
                                const content = atob(data.content);
                                editor.setValue(content);
                                editor.setOption('mode', getLanguageFromFilename(path));
                            }} else {{
                                fetch(data.download_url)
                                    .then(r => r.text())
                                    .then(text => {{
                                        editor.setValue(text);
                                        editor.setOption('mode', getLanguageFromFilename(path));
                                    }});
                            }}
                            editor.refresh();
                        }})
                        .catch(err => console.error("Error loading file:", err));
                }}

                function fetchDirectory(path) {{
                    fileListElem.innerHTML = "";
                    if (path !== "") {{
                        const backBtn = document.createElement("button");
                        backBtn.innerHTML = "⬅️ Back";
                        backBtn.className = "btn btn-secondary btn-sm mb-2";
                        backBtn.onclick = function() {{
                            const parts = currentPath.split("/");
                            parts.pop();
                            parts.pop();
                            currentPath = parts.length > 0 ? parts.join("/") + "/" : "";
                            fetchDirectory(currentPath);
                        }};
                        fileListElem.appendChild(backBtn);
                    }}
                    
                    fetch(`https://api.github.com/repos/${{repoOwner}}/${{repoName}}/contents/${{path}}`)
                        .then(r => r.json())
                        .then(files => {{
                            files.sort((a, b) => {{
                                if (a.type === b.type) return a.name.localeCompare(b.name);
                                return a.type === 'dir' ? -1 : 1;
                            }}).forEach(file => {{
                                const btn = document.createElement("button");
                                if (file.type === "dir") {{
                                    btn.innerHTML = "📁 " + file.name;
                                    btn.className = "btn btn-info btn-sm m-1";
                                    btn.onclick = function() {{
                                        currentPath = path + file.name + "/";
                                        fetchDirectory(currentPath);
                                    }};
                                }} else {{
                                    btn.innerHTML = "📄 " + file.name;
                                    btn.className = "btn btn-light btn-sm m-1";
                                    btn.onclick = function() {{
                                        loadFileContent(file.path);
                                    }};
                                }}
                                fileListElem.appendChild(btn);
                            }});
                        }})
                        .catch(err => {{
                            fileListElem.innerHTML = `<div class="alert alert-danger">Error loading directory: ${{err.message}}</div>`;
                        }});
                }}

                document.addEventListener('DOMContentLoaded', () => {{
                    document.querySelectorAll('[data-toggle="tab"]').forEach(trigger => {{
                        trigger.addEventListener('shown.bs.tab', () => editor.refresh());
                    }});
                    
                    document.getElementById('toggleTheme').addEventListener('click', () => {{
                        setTimeout(() => {{
                            editor.setOption('theme', document.documentElement.classList.contains('dark-mode') ? 'material-darker' : 'default');
                        }}, 100);
                    }});
                }});

                fetchDirectory(currentPath);
                </script>
                '''

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
                <div class="card paper-card mb-3">
                <a href="{link_target}" class="paper-link">
                    <div class="row no-gutters">
                    <div class="col-5 paper-img-container">
                        <img src="images/placeholder.png" class="card-img" alt="{paper_title}">
                    </div>
                    <div class="col-7">
                        <div class="card-body paper-card-body">
                        <h5 class="card-title paper-title">{paper_title}</h5>
                        <p class="card-text paper-desc">{paper_desc}</p>
                        </div>
                    </div>
                    </div>
                </a>
                </div>
                '''
                    papers_html += f'<div class="paper-widget-container">{widget_html}</div>'
                papers_html += '</div>'

                tech_html = ""
                if technologies:
                    tech_badges = ""
                    for tech in technologies:
                        if isinstance(tech, tuple):
                            tech_name, tech_desc, tech_link = tech
                            tech_badges += f"<a href='{tech_link}' target='_blank' class='badge badge-primary tech-badge' title='{tech_desc}'>{tech_name}</a>"
                        else:
                            tech_badges += f"<span class='badge badge-primary tech-badge'>{tech}</span>"
                    tech_html = f"<div class='project-technologies'><h5>Technologies Used</h5><div class='tech-badge-container'>{tech_badges}</div></div>"

                tabs = [("Introduction", intro_html), ("Timeline", timeline_html)]
                if tech_html:
                    tabs.append(("Technologies", tech_html))
                tabs.extend([("Code", code_html), ("Papers", papers_html)])
                page.tabs(tabs)
                
            except Exception as e:
                page.alert_box(f"Error creating project page: {e}", "danger")
                
        return page
        
    def compile(self, output_dir="."):
        if output_dir != "." and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        nav_links = "".join([
            f'<li class="nav-item"><a class="nav-link" href="{slug}.html">{data["title"]}</a></li>'
            for slug, data in self.pages.items()
            if not data.get("is_blog") and not data.get("is_project")
        ])

        def base_template(title, content):
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script>if(localStorage.getItem('theme')==='dark'){{document.documentElement.classList.add('dark-mode');}}</script>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.5/theme/material-darker.min.css">
<style>
:root {{
  --text-color: #333;
  --bg-color: #f5f5f5;
  --card-bg: #ffffff;
  --timeline-bg: #e9ecef;
  --border-color: #dee2e6;
  --shadow-color: rgba(0,0,0,0.1);
  --blockquote-color: #6c757d;
  --accent-color: #007bff;
  --header-color: #495057;
  --footer-bg: #f8f9fa;
  --footer-text: #6c757d;
}}

html.dark-mode {{
  --text-color: #e9e9e9;
  --bg-color: #252525;
  --card-bg: #2e2e2e;
  --timeline-bg: #3a3a3a;
  --border-color: #444;
  --shadow-color: rgba(0,0,0,0.25);
  --blockquote-color: #aaa;
  --accent-color: #61afef;
  --header-color: #e0e0e0;
  --footer-bg: #1a1a1a;
  --footer-text: #aaa;
}}

body {{
  font-family: 'Roboto', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-size: 18px;
  line-height: 1.6;
  transition: all 0.3s ease;
  overflow-x: hidden;
}}

h1, h2, h3, h4, h5, h6 {{
  color: var(--header-color);
  margin-bottom: 1rem;
  font-weight: 500;
}}

.heading {{
  position: relative;
  padding-bottom: 0.5rem;
}}

.heading:after {{
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 50px;
  background-color: var(--accent-color);
}}

p {{
  margin-bottom: 1.2rem;
}}

a {{
  color: var(--accent-color);
  transition: color 0.2s;
}}

a:hover {{
  text-decoration: none;
  color: #0056b3;
}}

.navbar {{
  background-color: #6c757d;
  box-shadow: 0 2px 10px var(--shadow-color);
  transition: all 0.3s ease;
  padding: 1rem;
}}

.navbar.dark-mode {{
  background-color: #343a40;
}}

.navbar-brand {{
  font-weight: 700;
  letter-spacing: 1px;
}}

.nav-link {{
  position: relative;
  margin: 0 0.5rem;
}}

.nav-link:after {{
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #fff;
  transition: width 0.3s;
}}

.nav-link:hover:after {{
  width: 100%;
}}

.card {{
  background-color: var(--card-bg);
  box-shadow: 0 4px 8px var(--shadow-color);
  border: none;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}}

.card:hover {{
  transform: translateY(-5px);
  box-shadow: 0 8px 16px var(--shadow-color);
}}

.custom-card {{
  position: relative;
  z-index: 1;
}}

.card-title {{
  font-weight: 500;
  color: var(--header-color);
}}

.card-body {{
  padding: 1.5rem;
}}

.custom-divider {{
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0,0,0,0), var(--border-color), rgba(0,0,0,0));
  margin: 2rem 0;
}}

.timeline {{
  position: relative;
  max-width: 1000px;
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
  background: var(--accent-color);
  transform: translateX(-50%);
  border-radius: 20px;
}}

.timeline-item {{
  position: relative;
  width: 50%;
  padding: 20px 40px;
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
  padding: 20px;
  background: var(--timeline-bg);
  border-radius: 8px;
  box-shadow: 0 4px 8px var(--shadow-color);
  position: relative;
  transition: all 0.3s ease;
}}

.timeline-content:hover {{
  transform: scale(1.02);
}}

.timeline-item.left .timeline-content::after {{
  content: "";
  position: absolute;
  top: 20px;
  right: -20px;
  width: 20px;
  height: 4px;
  background: var(--accent-color);
}}

.timeline-item.right .timeline-content::after {{
  content: "";
  position: absolute;
  top: 20px;
  left: -20px;
  width: 20px;
  height: 4px;
  background: var(--accent-color);
}}

.timeline-date {{
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--accent-color);
  font-size: 1.1rem;
}}

.scroll-animate {{
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}}

.animate__fadeInUp {{
  opacity: 1 !important;
  transform: translateY(0) !important;
}}

.theme-blockquote {{
  border-left: 5px solid var(--accent-color);
  padding: 1rem 1.5rem;
  color: var(--blockquote-color);
  background-color: rgba(0,0,0,0.03);
  border-radius: 0 8px 8px 0;
  margin: 1.5rem 0;
  transition: all 0.3s ease;
}}

.theme-blockquote p {{
  font-size: 1.1rem;
  line-height: 1.8;
}}

.theme-blockquote footer {{
  margin-top: 0.5rem;
  opacity: 0.8;
}}

.enhanced-image {{
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px var(--shadow-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.enhanced-image:hover {{
  transform: scale(1.02);
  box-shadow: 0 8px 16px var(--shadow-color);
}}

figure {{
  display: block;
  margin: 1.5rem 0;
  transition: all 0.3s ease;
}}

figcaption {{
  margin-top: 10px;
  font-size: 0.9rem;
  font-style: italic;
  text-align: center;
  color: var(--blockquote-color);
}}

pre {{
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px var(--shadow-color);
  margin: 1.5rem 0;
  overflow-x: auto;
}}

code {{
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
}}

.code-block {{
  border-radius: 8px;
  margin: 1.5rem 0;
}}

.btn {{
  transition: all 0.3s ease;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  font-weight: 500;
}}

.btn:hover {{
  transform: translateY(-3px);
  box-shadow: 0 6px 12px var(--shadow-color);
}}

.btn-icon {{
  margin-right: 8px;
}}

.download-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0.75rem 1.5rem;
}}

.download-icon {{
  font-size: 1.2rem;
}}

.custom-jumbotron {{
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 3rem 2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px var(--shadow-color);
}}

.custom-jumbotron::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: var(--accent-color);
}}

.custom-jumbotron .display-4 {{
  font-weight: 700;
  margin-bottom: 1rem;
}}

.custom-jumbotron .lead {{
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}}

.action-btn {{
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}}

.custom-carousel {{
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px var(--shadow-color);
  margin: 2rem 0;
}}

.custom-carousel .carousel-control-prev,
.custom-carousel .carousel-control-next {{
  width: 10%;
  opacity: 0;
  transition: opacity 0.3s ease;
}}

.custom-carousel:hover .carousel-control-prev,
.custom-carousel:hover .carousel-control-next {{
  opacity: 0.8;
}}

.spacer {{
  width: 100%;
}}

.widget-card {{
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  max-width: 540px;
  margin: 0 auto 1.5rem;
}}

.widget-card:hover {{
  transform: translateY(-5px);
}}

.widget-card-link {{
  text-decoration: none;
  color: inherit;
  display: block;
}}

.gallery-grid {{
  margin: 1.5rem -15px;
}}

.gallery-item {{
  padding: 15px;
  transition: all 0.3s ease;
}}

.gallery-item:hover {{
  transform: scale(1.03);
}}

.gallery-image {{
  border-radius: 8px;
  box-shadow: 0 4px 8px var(--shadow-color);
  transition: all 0.3s ease;
}}

.rotating-gallery-container {{
  position: relative;
  overflow: hidden;
  margin: 2rem auto;
  border-radius: 8px;
  box-shadow: 0 6px 12px var(--shadow-color);
}}

.gallery-slide {{
  position: absolute;
  display: block;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 1;
}}

.gallery-slide.active {{
  opacity: 1;
}}

.gallery-slide-image {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
}}

.gallery-caption {{
  text-align: center;
  font-size: 0.9rem;
  font-style: italic;
  margin-top: 10px;
  color: var(--blockquote-color);
}}

.custom-tabs {{
  border-bottom: 2px solid var(--border-color);
}}

.custom-tabs .nav-link {{
  border: none;
  color: var(--text-color);
  font-weight: 500;
  border-bottom: 3px solid transparent;
  padding: 0.75rem 1.5rem;
  margin-bottom: -2px;
}}

.custom-tabs .nav-link.active {{
  color: var(--accent-color);
  background: transparent;
  border-bottom: 3px solid var(--accent-color);
}}

.custom-tab-content {{
  padding: 1.5rem 0;
}}

.custom-tooltip {{
  border-bottom: 1px dotted;
  cursor: help;
}}

.map-container {{
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px var(--shadow-color);
  margin: 1.5rem 0;
}}

.map-container iframe {{
  width: 100%;
  border: none;
}}

.video-container {{
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px var(--shadow-color);
  margin: 1.5rem 0;
}}

.video-container iframe {{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}}

.email-link, .site-link {{
  font-weight: 500;
  transition: all 0.2s ease;
}}

.email-link:hover, .site-link:hover {{
  text-decoration: none;
  color: #0056b3;
}}

.project-intro {{
  margin-bottom: 2rem;
}}

.code-viewer-container {{
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
}}

.file-list {{
  max-height: 300px;
  overflow: auto;
  padding: 15px;
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
}}

.code-viewer {{
  height: 600px;
  overflow: auto;
}}

.CodeMirror {{
  height: 100%;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
}}

.paper-widgets {{
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}}

.paper-widget-container {{
  flex: 1 1 300px;
  max-width: 500px;
}}

.paper-card {{
  height: 100%;
  transition: all 0.3s ease;
}}

.paper-link {{
  text-decoration: none;
  color: inherit;
  display: block;
}}

.paper-img-container {{
  padding: 0;
  overflow: hidden;
}}

.paper-img-container img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}}

.paper-card:hover .paper-img-container img {{
  transform: scale(1.05);
}}

.paper-card-body {{
  padding: 1rem;
}}

.paper-title {{
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}}

.paper-desc {{
  font-size: 0.9rem;
  color: var(--blockquote-color);
}}

.project-technologies {{
  margin: 2rem 0;
}}

.tech-badge-container {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}}

.tech-badge {{
  font-size: 0.95rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 400;
  box-shadow: 0 2px 4px var(--shadow-color);
  transition: all 0.2s ease;
  background-color: var(--accent-color);
  color: white;
}}

.tech-badge:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 8px var(--shadow-color);
}}

.blog-date, .blog-author, .read-time {{
  display: block;
  margin-bottom: 0.5rem;
  color: var(--blockquote-color);
}}

.footer {{
  background-color: var(--footer-bg);
  padding: 2rem 0;
  transition: all 0.3s ease;
}}

.footer .text-muted {{
  color: var(--footer-text) !important;
}}

.custom-accordion {{
  margin: 1.5rem 0;
}}

.accordion-card {{
  margin-bottom: 0.5rem;
  background-color: var(--card-bg);
  border: none;
  border-radius: 8px;
  overflow: hidden;
}}

.accordion-card:last-child {{
  margin-bottom: 0;
}}

.accordion-btn {{
  color: var(--text-color);
  font-weight: 500;
  text-align: left;
  width: 100%;
  text-decoration: none;
  position: relative;
  padding: 1rem;
}}

.accordion-btn:hover {{
  text-decoration: none;
  color: var(--accent-color);
}}

.accordion-content {{
  padding: 1rem;
}}

.progress {{
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--timeline-bg);
}}

.social-share {{
  display: flex;
  gap: 10px;
  margin: 1.5rem 0;
}}

.social-btn {{
  padding: 0.5rem 1rem;
  border-radius: 6px;
  color: white;
  font-weight: 500;
  text-align: center;
  transition: all 0.2s ease;
}}

.facebook-btn {{ background-color: #3b5998; }}
.twitter-btn {{ background-color: #1da1f2; }}
.linkedin-btn {{ background-color: #0e76a8; }}
.email-btn {{ background-color: #ea4335; }}

.social-btn:hover {{
  opacity: 0.9;
  transform: translateY(-2px);
  color: white;
  text-decoration: none;
}}

.masonry-grid {{
  column-gap: 1.5rem;
  margin: 1.5rem 0;
}}

.masonry-item {{
  break-inside: avoid;
  margin-bottom: 1.5rem;
}}

.breadcrumb {{
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  box-shadow: 0 2px 4px var(--shadow-color);
}}

.feature-box {{
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 8px var(--shadow-color);
  margin: 1.5rem 0;
  transition: all 0.3s ease;
}}

.feature-box:hover {{
  transform: translateY(-5px);
  box-shadow: 0 8px 16px var(--shadow-color);
}}

.feature-icon {{
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: var(--accent-color);
}}

.feature-title {{
  margin-bottom: 1rem;
  font-weight: 600;
}}

.pricing-container {{
  margin: 2rem -15px;
}}

.pricing-card {{
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--card-bg);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px var(--shadow-color);
  transition: all 0.3s ease;
}}

.pricing-card.featured {{
  transform: scale(1.05);
  box-shadow: 0 8px 20px var(--shadow-color);
  position: relative;
  z-index: 2;
}}

.pricing-card:hover {{
  transform: translateY(-10px);
}}

.pricing-header {{
  background-color: var(--accent-color);
  color: white;
  padding: 2rem 1.5rem;
  text-align: center;
}}

.pricing-title {{
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}}

.pricing-price {{
  font-size: 2.5rem;
  font-weight: 700;
  margin: 1rem 0;
}}

.pricing-period {{
  font-size: 0.9rem;
  opacity: 0.8;
}}

.pricing-features {{
  list-style: none;
  padding: 1.5rem;
  margin: 0;
  flex-grow: 1;
}}

.pricing-feature {{
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border-color);
}}

.pricing-feature:last-child {{
  border-bottom: none;
}}

.pricing-footer {{
  padding: 1.5rem;
  text-align: center;
}}

.pricing-button {{
  width: 100%;
  padding: 0.75rem;
}}

@media (max-width: 768px) {{
  .timeline::before {{
    left: 10px;
  }}
  .timeline-item {{
    width: 100%;
    text-align: left;
    padding-left: 30px;
  }}
  .timeline-item.left, .timeline-item.right {{
    left: 0;
  }}
  .timeline-item.left .timeline-content::after,
  .timeline-item.right .timeline-content::after {{
    left: -20px;
    right: auto;
  }}
}}
{self.custom_css}
</style>
</head>
<body>
<a id="top"></a>
<nav class="navbar navbar-expand-lg navbar-dark">
  <div class="container">
    <a class="navbar-brand" href="index.html">{self.title}</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        {nav_links}
        <li class="nav-item">
          <button id="toggleTheme" class="btn btn-outline-light">🌓</button>
        </li>
      </ul>
    </div>
  </div>
</nav>
<div class="container mt-5">
{content}
<div style="text-align:center; margin:20px;"><a href="#top" class="btn btn-secondary">Back to top</a></div>
</div>
<footer class="footer mt-5 py-3 text-center">
  <div class="container">
    <span class="text-muted">{self.footer}</span>
  </div>
</footer>
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {{
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
        observer.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.3, rootMargin: '0px 0px -50px 0px' }});
  
  document.querySelectorAll('.scroll-animate').forEach(el => observer.observe(el));

  const themeToggle = document.getElementById("toggleTheme");
  themeToggle.addEventListener("click", function() {{
    document.documentElement.classList.toggle("dark-mode");
    localStorage.setItem('theme', document.documentElement.classList.contains("dark-mode") ? 'dark' : 'light');
    
    const footer = document.querySelector('footer');
    if (document.documentElement.classList.contains("dark-mode")) {{
      footer.classList.replace('bg-light', 'bg-dark');
    }} else {{
      footer.classList.replace('bg-dark', 'bg-light');
    }}
  }});
  
  if (document.documentElement.classList.contains('dark-mode')) {{
    document.querySelector('footer').classList.replace('bg-light', 'bg-dark');
  }}

  document.querySelectorAll('a[href="#top"]').forEach(function(link) {{
    link.addEventListener("click", function(e) {{
      e.preventDefault();
      window.scrollTo({{top: 0, behavior: "smooth"}});
    }});
  }});

  document.querySelectorAll('[data-toggle="tooltip"]').forEach(el => {{
    new bootstrap.Tooltip(el);
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