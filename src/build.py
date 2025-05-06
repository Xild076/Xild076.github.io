# -*- coding: utf-8 -*-
import os
from urllib.parse import urljoin
from sitegen import Site, Page, Alignment, Spacing, ButtonType, AnimationType, ColorTheme, ObjectFit, InputType, FlexDirection, FlexWrap, build_tab_content

def build_header_content_for_page(page_instance, site_meta, nav_items_list):
    header_page = Page(page_instance.site, slug="_header_for_" + page_instance.slug) # Temp page for header
    with header_page.Header(css_class="site-header shadow-lg", spacing_after=Spacing.NONE): # No bottom margin from header itself
        with header_page.Container(fluid=True):
            with header_page.FlexContainer(justify_content=Alignment.BETWEEN, align_items=Alignment.CENTER):
                header_page.Write(site_meta.get('site_title'), css_class="site-title h3 m-0")
                # Adjust active state for nav items based on the actual page slug
                current_slug = page_instance.slug
                processed_nav_items = []
                for item in nav_items_list:
                    new_item = item.copy()
                    # Simple check: if item's URL (relative) matches slug or index.html for root
                    if (current_slug == "index" and new_item["url"] == "./index.html") or \
                       (new_item["url"] == f"./{current_slug}.html"):
                        new_item["active"] = True
                    else:
                        new_item["active"] = False
                    processed_nav_items.append(new_item)
                header_page.Navigation(items=processed_nav_items, nav_type="main-header")
                # Theme toggle is in layout.j2
    return header_page.get_html()


site = Site(source_dir="src", output_dir="docs")

site.set_meta(
    site_title="Enhanced SSG Showcase",
    description="Demonstrating advanced features of the Python static site generator.",
    author="Xild076",
    keywords="python, ssg, static site, generator, advanced",
    base_url="https://Xild076.github.io",
    default_og_image=urljoin("https://Xild076.github.io/", "static/img/og-default.jpg")
)

# Define nav items once
main_nav_items = [
    {"text": "Home", "url": "./index.html"},
    {"text": "About", "url": "./about.html"},
    {"text": "Markdown", "url": "./from-markdown.html"},
    {"text": "Contact", "url": "./contact.html"}
]

index_page = site.add_page("index", "Welcome to the Enhanced Showcase!")
index_page.site_header_content = build_header_content_for_page(index_page, site.meta, main_nav_items) # Assign custom header

# Add a top margin to the first component after the custom header
index_page.Alert("This site showcases new components and scroll animations!", style_type=ColorTheme.INFO, dismissible=True, animation=AnimationType.FADE_IN_DOWN, scroll_animation=True, spacing_before=Spacing.XL)


with index_page.Container(css_class="my-lg"):
    index_page.Write("Scroll down to see components animate into view.", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, animation=AnimationType.FADE_IN, scroll_animation_delay=0.2)

    with index_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.ZOOM_IN, scroll_animation=True, css_class="rounded-lg mb-lg"):
         index_page.Write("Interactive Background Section", align=Alignment.CENTER)
         index_page.Button("Pulse Button", link="#", style_type=ButtonType.SUCCESS, animation=AnimationType.PULSE)
         index_page.Button("Delayed Fade-in", link="#", style_type=ButtonType.OUTLINE_INFO, spacing_before=Spacing.SM, scroll_animation=True, animation=AnimationType.FADE_IN_UP, scroll_animation_delay=0.4)

    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL)
    index_page.Write("Component Showcase (Grid Layout)", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, animation=AnimationType.FADE_IN)

    with index_page.Grid(cols=3, gap=Spacing.LG, spacing_before=Spacing.LG):
        with index_page.Card(animation=AnimationType.FADE_IN_LEFT, scroll_animation=True):
            index_page.Write("Card 1: Media & Badges", align=Alignment.CENTER)
            index_page.Image("/static/img/placeholder1.png", alt="Placeholder 1", caption="A placeholder image")
            index_page.Write("Some card content goes here.", spacing_before=Spacing.MD)
            index_page.Badge("Info", style_type=ColorTheme.INFO, spacing_after=Spacing.XS); index_page.Badge("Pill", style_type=ColorTheme.SUCCESS, pill=True)

        with index_page.Card(animation=AnimationType.SLIDE_UP, scroll_animation=True, scroll_animation_delay=0.1):
             index_page.Write("Card 2: Feedback & Progress", align=Alignment.CENTER)
             index_page.ProgressBar(65, label=True, style_type=ColorTheme.WARNING, striped=True, animated=True)
             index_page.Alert("This is a warning alert.", style_type=ColorTheme.WARNING, spacing_before=Spacing.MD)
             index_page.Button("Danger Button", style_type=ButtonType.DANGER, spacing_before=Spacing.MD)

        with index_page.Card(animation=AnimationType.FADE_IN_RIGHT, scroll_animation=True, scroll_animation_delay=0.2):
            index_page.Write("Card 3: Text & Code", align=Alignment.CENTER)
            index_page.BlockQuote("This is a blockquote.", author="Someone Famous")
            index_page.CodeBlock("print('Hello, World!')", language="python")
            index_page.Icon("fas fa-star", color="gold", size=Spacing.LG, spacing_before=Spacing.SM, spacing_after=Spacing.XS)
            index_page.Icon("fas fa-home", color="var(--primary)", size="2rem")

    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.LG)
    index_page.Write("Tabs and Accordion", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, animation=AnimationType.FADE_IN)
    tab1_html = build_tab_content(site, lambda p: [p.Write("Content for the first tab."), p.Image("/static/img/placeholder2.png", alt="Small", width=150, height=150, object_fit=ObjectFit.CONTAIN, align=Alignment.CENTER)])
    tab2_html = build_tab_content(site, lambda p: [p.Write("Content for the second tab."), p.Table(headers=["ID", "Name", "Role"], rows=[[1, "Alice", "Admin"], [2, "Bob", "User"], [3, "Charlie", "Editor"]])])
    index_page.Tabs(items=[{"title": "Image Tab", "content": tab1_html, "active": True}, {"title": "Table Tab", "content": tab2_html}, {"title": "Simple Tab", "content": "Plain text content."}], spacing_after=Spacing.LG, scroll_animation=True, animation=AnimationType.FADE_IN_UP)
    index_page.Accordion(items=[{"title": "Accordion Item 1", "content": "Details for item 1.", "open": True}, {"title": "Accordion Item 2", "content": build_tab_content(site, lambda p: [p.Write("Details for item 2."), p.Button("Button inside", style_type=ButtonType.INFO)])}, {"title": "Accordion Item 3", "content": "Plain text for item 3."}], scroll_animation=True)

about_page = site.add_page("about", "About Us")
about_page.site_header_content = build_header_content_for_page(about_page, site.meta, main_nav_items)
with about_page.Container(spacing_before=Spacing.XL): # Added spacing_before for content after custom header
    about_page.Breadcrumbs(items=[{'text': 'Home', 'link': './index.html'}, {'text': 'About'}])
    about_page.Write("About Our Project", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, animation=AnimationType.SLIDE_DOWN)
    about_page.Image("/static/img/placeholder_wide.png", alt="About Banner", spacing_before=Spacing.LG, spacing_after=Spacing.LG, animation=AnimationType.ZOOM_OUT, scroll_animation=True)
    about_page.Timeline(events=[{'time': '2023', 'title': 'Project Started', 'description': 'Initial concept.'}, {'time': '2024', 'title': 'Core Features', 'description': 'Components refined.'}, {'time': 'Today', 'title': 'Public Demo', 'description': 'Showcasing capabilities.'}], spacing_before=Spacing.LG, scroll_animation=True)
    share_url = urljoin(site.meta['base_url'] + '/', 'about.html')
    about_page.SocialShare(platforms=['twitter', 'linkedin', 'email'], url=share_url, title=f"{about_page.title} | {site.meta['site_title']}", align=Alignment.CENTER, spacing_before=Spacing.LG)

contact_page = site.add_page("contact", "Contact Us")
contact_page.site_header_content = build_header_content_for_page(contact_page, site.meta, main_nav_items)
with contact_page.Container(css_class="py-xl", spacing_before=Spacing.XL): # Added spacing_before
    contact_page.Breadcrumbs(items=[{'text': 'Home', 'link': './index.html'}, {'text': 'Contact'}])
    contact_page.Write("Get in Touch", align=Alignment.CENTER, css_class="h2 mb-lg", scroll_animation=True, animation=AnimationType.FADE_IN_DOWN)
    with contact_page.Form(action="/submit-form", method="post", css_class="needs-validation", scroll_animation=True, animation=AnimationType.FADE_IN_UP):
        with contact_page.Grid(cols=2, gap=Spacing.MD):
            contact_page.Input(label="First Name", name="fname", placeholder="John", required=True)
            contact_page.Input(label="Last Name", name="lname", placeholder="Doe", required=True)
        contact_page.Input(label="Email Address", input_type=InputType.EMAIL, name="email", placeholder="name@example.com", required=True)
        contact_page.Select(label="Reason for Contact", name="reason", options=[{"text":"General Inquiry"}, {"text":"Support"}, {"text":"Feedback"}], required=True)
        contact_page.Textarea(label="Your Message", name="message", rows=5, placeholder="Enter your message here...", required=True)
        with contact_page.FormGroup():
            contact_page.Input(input_type=InputType.CHECKBOX, name="subscribe", label="Subscribe to newsletter", checked=True)
        contact_page.Button("Send Message", style_type=ButtonType.PRIMARY, css_class="mt-lg", kwargs={'type':'submit'})

try:
    markdown_file_path = os.path.join(site.content_dir, "sample.md")
    with open(markdown_file_path, 'r', encoding='utf-8') as f: md_content = f.read()
    md_page = site.add_page("from-markdown", "Markdown Demo")
    md_page.site_header_content = build_header_content_for_page(md_page, site.meta, main_nav_items) # Custom header for MD page too
    with md_page.Container(spacing_before=Spacing.XL): # Added spacing_before
         md_page.Breadcrumbs(items=[{'text': 'Home', 'link': './index.html'}, {'text': 'Markdown Demo'}])
         md_page.Markdown(md_content, animation=AnimationType.FADE_IN, scroll_animation=True)
except FileNotFoundError: print(f"Skipping markdown page: {markdown_file_path} not found.")
except Exception as e: print(f"Error loading markdown file {markdown_file_path}: {e}")

site.build()