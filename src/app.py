import os
from urllib.parse import urljoin
from sitegen import Site, Page, Alignment, Spacing, ButtonType, AnimationType, ColorTheme, ObjectFit, InputType, FlexDirection, FlexWrap, build_tab_content

site = Site(source_dir="src", output_dir="docs")
site.set_meta(
    site_title="Harry Yin's Portfolio", 
    description="A showcase of my projects and thoughts :D",
    author="Harry Yin (Xild076)",
    keywords="portfolio, projects, blog, developer",
    base_url="https://xild076.github.io",
    default_og_image=urljoin("https://xild076.github.io/", "static/img/social.png")
)

main_nav_items = [
    {"text":"Home", "url": "./index.html"},
    {"text":"Projects", "url": "./projects.html"},
    {"text":"Blog", "url": "./blog.html"},
    {"text":"About", "url": "./about.html"},
]

index_page = site.add_page("index", "Home")

with index_page.Background(color="var(--light)", padding=Spacing.XL, animation=AnimationType.ZOOM_IN, css_class="rounded-lg"):
        index_page.Write("Welcome to Harry Yin's Portfolio!", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="50px")
        index_page.Write("A showcase of my projects and other random and cool stuff.", align=Alignment.CENTER, spacing_after=Spacing.LG)

with index_page.Container(css_class="my_lg"):
    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    index_page.Write("Featured", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="40px")
    with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
        with index_page.Columns(n=2, gap=Spacing.LG, spacing_before=Spacing.LG):
            with index_page.Container(css_class="rounded-lg"):
                index_page.Image("/static/imgs/placeholder.png", alt="Placeholder 1", caption="A placeholder image", width="300px", height="300px", object_fit=ObjectFit.COVER, align=Alignment.CENTER)
            
            with index_page.Container(css_class="rounded-lg"):
                index_page.Markdown("### Project Title", align=Alignment.CENTER, spacing_after=Spacing.LG)
    
    index_page.Divider(spacing_before=Spacing.XL, spacing_after=Spacing.XL, thickness=2.5)

    with index_page.Columns(2):
        with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
            index_page.Markdown("### Latest Project:", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Widget("Project [xxx]", "This is a placeholder blog post", link="#", image_url="/static/imgs/placeholder.png", scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Button("View all projects", link="#", style_type=ButtonType.PRIMARY, animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15)
        
        with index_page.Card(animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15):
            index_page.Markdown("### Latest Blog Post:", align=Alignment.CENTER, spacing_after=Spacing.LG, scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Widget("Blog Post [xxx]", "This is a placeholder blog post", link="#", image_url="/static/imgs/placeholder.png", scroll_animation=True, scroll_animation_delay=0.15)
            index_page.Button("View all blog posts", link="#", style_type=ButtonType.PRIMARY, animation=AnimationType.FADE_IN, scroll_animation=True, scroll_animation_delay=0.15)
    
about_page = site.add_page("about", "About Me")

with about_page.Container(css_class="my_lg"):
    about_page.Write("About Me", align=Alignment.CENTER, spacing_after=Spacing.LG, text_size="40px")
    about_page.Write("I'm a High School student lol", align=Alignment.CENTER, spacing_after=Spacing.LG)
    about_page.Image("/static/imgs/placeholder.png", alt="Placeholder 1", caption="A placeholder image", width="300px", height="300px", object_fit=ObjectFit.COVER, align=Alignment.CENTER)
    about_page.Markdown("### My Interests:", align=Alignment.CENTER, spacing_after=Spacing.LG)
    about_page.Markdown("- AI and Machine Learning")
    about_page.Markdown("- Data Science and Analytics")
    about_page.Markdown("- Game Development")
    about_page.Markdown("- Web Development")

site.build()