from jinja2 import Environment, FileSystemLoader
import shutil, os, json
from datetime import datetime
from markdown import markdown

class Widget:
    def render(self) -> str:
        return ""

class Text(Widget):
    def __init__(self, content: str, align: str = "left"):
        self.content, self.align = content, align
    def render(self):
        return f"<p class='content-paragraph' style='text-align:{self.align};'>{self.content}</p>"

class Heading(Widget):
    def __init__(self, text: str, level: int = 1, align: str = "left"):
        self.text, self.level, self.align = text, level, align
    def render(self):
        return f"<h{self.level} class='heading heading-{self.level}' style='text-align:{self.align};'>{self.text}</h{self.level}>"

class MarkdownWidget(Widget):
    def __init__(self, md: str):
        self.md = md
    def render(self):
        return markdown(self.md)

class Container(Widget):
    def __init__(self, children: list, layout: str = "row", gap: str = "1rem"):
        self.children, self.layout, self.gap = children, layout, gap
    def render(self):
        inner = "".join(c.render() for c in self.children)
        return f"<div style='display:flex;flex-direction:{self.layout};gap:{self.gap};'>{inner}</div>"

class BrythonSimulation(Widget):
    def __init__(self, canvas_id: str, script_src: str, width: str = "100%", height: str = "400px"):
        self.canvas_id, self.script_src, self.width, self.height = canvas_id, script_src, width, height
    def render(self):
        return (
            f"<canvas id='{self.canvas_id}' style='width:{self.width};height:{self.height};'></canvas>"
            f"<script type='text/python' src='static/{self.script_src}'></script>"
        )

class Slider(Widget):
    def __init__(self, label: str, min: int, max: int, step: int, default: int):
        self.label, self.min, self.max, self.step, self.default = label, min, max, step, default
    def render(self):
        return (
            f"<label for='{self.label}'>{self.label}</label>"
            f"<input type='range' id='{self.label}' min='{self.min}' max='{self.max}' "
            f"step='{self.step}' value='{self.default}'>"
        )

class Button(Widget):
    def __init__(self, text: str, onclick: str = "", style: str = "primary", size: str = "md"):
        self.text, self.onclick, self.style, self.size = text, onclick, style, size
    def render(self):
        action = f"onclick='{self.onclick}()'" if self.onclick else ""
        return f"<button class='btn btn-{self.style} btn-{self.size}' {action}>{self.text}</button>"

class SiteLink(Widget):
    def __init__(self, url: str, text: str = None):
        self.url, self.text = url, text or url
    def render(self):
        return f"<a href='{self.url}' class='site-link'>{self.text}</a>"

class Page:
    def __init__(self, name: str, title: str, theme: str = "light"):
        self.name, self.title, self.theme = name, title, theme
        self.widgets = []
    def add(self, widget: Widget):
        self.widgets.append(widget)

class Site:
    def __init__(self, name: str):
        self.name = name
        self.pages = []
    def add_page(self, page: Page):
        self.pages.append(page)
    def build(self, output_dir: str = "output"):
        env = Environment(loader=FileSystemLoader("templates"))
        from datetime import datetime
        env = Environment(loader=FileSystemLoader("templates"))
        env.globals['now'] = datetime.now

        tpl = env.get_template("base.html")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(os.path.join(output_dir, "static"), exist_ok=True)
        for page in self.pages:
            body_html = "".join(w.render() for w in page.widgets)
            html = tpl.render(
                title=page.title,
                theme=page.theme,
                nav=self.pages,
                current=page.name,
                body=body_html
            )
            with open(os.path.join(output_dir, f"{page.name}.html"), "w") as f:
                f.write(html)
        for asset in os.listdir("static"):
            shutil.copy(f"static/{asset}", f"{output_dir}/static/{asset}")
