import os
import shutil
import datetime
import html
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown2
import sass
import re
from urllib.parse import quote_plus, urljoin, urlparse, quote

from enums import (
    Alignment, Spacing, ButtonType, AnimationType, ObjectFit, ColorTheme,
    InputType, FlexDirection, FlexWrap
)

_DEFAULT_SPACING_MAP = {
    Spacing.NONE: '0', Spacing.XS: 'var(--spacing-xs)', Spacing.SM: 'var(--spacing-sm)',
    Spacing.MD: 'var(--spacing-md)', Spacing.LG: 'var(--spacing-lg)', Spacing.XL: 'var(--spacing-xl)',
    Spacing.AUTO: 'auto', Spacing.DEFAULT: 'var(--spacing-md)'
}

def build_tab_content(site_instance, build_func):
    unique_slug = "_tab_content_for_" + site_instance.meta.get('site_title', 'site').replace(" ", "_") + "_" + str(id(build_func))
    temp_page = Page(site_instance, slug=unique_slug)
    build_func(temp_page)
    return temp_page.get_html()

class ContextWrapper:
    def __init__(self, component, context_type):
        self.component = component
        self.context_type = context_type

    def __enter__(self):
        self.component._context_stack.append(self)
        return self.component

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.component._context_stack:
            popped_context_wrapper = self.component._context_stack.pop()
            if popped_context_wrapper is not self:
                pass
            html_content_map = {
                "Card": "</div></div>",
                "Container": "</div>", "Columns": "</div>", "Background": "</div>", "Grid": "</div>",
                "Header": "</header>", "Footer": "</footer>", "Navigation": "</nav>",
                "Form": "</form>", "FormGroup": "</div>", "FlexContainer": "</div>"
            }
            html_content = html_content_map.get(self.context_type, "")
            if html_content:
                if self.component._context_stack:
                    self.component._context_stack[-1].component._html_elements.append(html_content)
                else:
                    self.component._html_elements.append(html_content)

class BaseComponent:
    def __init__(self):
        self._html_elements = []
        self._context_stack = []
        self.site = None 

    def _append_html(self, html_content):
        if self._context_stack:
            self._context_stack[-1].component._html_elements.append(str(html_content))
        else:
            self._html_elements.append(str(html_content))

    def get_html(self):
        return "".join(self._html_elements)

    def _format_size(self, value):
        if isinstance(value, Spacing): return _DEFAULT_SPACING_MAP.get(value, _DEFAULT_SPACING_MAP[Spacing.DEFAULT])
        if isinstance(value, (int, float)): return f"{value}px"
        if isinstance(value, str): return value
        return _DEFAULT_SPACING_MAP[Spacing.DEFAULT]

    def _get_style_attr(self, styles):
        if not styles: return ""
        style_str = "; ".join(f"{k.strip()}: {str(v).strip()}" for k, v in styles.items() if v is not None and str(v).strip())
        return f' style="{style_str}"' if style_str else ""

    def _apply_spacing_styles(self, spacing_before, spacing_after):
        styles = {}
        if spacing_before != Spacing.DEFAULT: styles['margin-top'] = self._format_size(spacing_before)
        if spacing_after != Spacing.DEFAULT: styles['margin-bottom'] = self._format_size(spacing_after)
        elif spacing_after == Spacing.DEFAULT and spacing_before == Spacing.DEFAULT :
             styles['margin-bottom'] = _DEFAULT_SPACING_MAP[Spacing.DEFAULT]
        return styles

    def _get_animation_class(self, animation):
        return f" animate-{animation.value}" if animation and animation != AnimationType.NONE else ""

    def _get_alignment_class(self, align):
        if align in [Alignment.LEFT, Alignment.CENTER, Alignment.RIGHT, Alignment.JUSTIFY]: return f" text-{align.value}"
        return ""

    def _build_attributes_string(self, classes_str, styles_dict, data_attrs_dict, other_attrs=None):
        attrs_list = []
        if classes_str and classes_str.strip(): attrs_list.append(f'class="{classes_str.strip()}"')
        
        style_attribute = self._get_style_attr(styles_dict)
        if style_attribute: attrs_list.append(style_attribute)
        
        if data_attrs_dict:
            for k, v in data_attrs_dict.items():
                if v is not None: attrs_list.append(f'{k}="{html.escape(str(v))}"')
        
        if other_attrs:
            for k_orig,v_orig in other_attrs.items():
                k = k_orig.replace('_', '-')
                v = v_orig
                if v is True: attrs_list.append(k)
                elif v is False: pass
                elif v is not None: attrs_list.append(f'{k}="{html.escape(str(v))}"')
        return " ".join(attrs_list)

    def _get_combined_attributes(self, spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, css_class, specific_styles=None, other_attrs=None):
        final_classes_list = []
        if css_class:
            final_classes_list.extend(css_class.split())

        current_styles = self._apply_spacing_styles(spacing_before, spacing_after)
        data_attrs = {}

        if scroll_animation and animation and animation != AnimationType.NONE:
            data_attrs['data-scroll-animation'] = animation.value
            if scroll_animation_delay > 0: data_attrs['data-scroll-animation-delay'] = f"{scroll_animation_delay}s"
        elif animation and animation != AnimationType.NONE:
            final_classes_list.append(self._get_animation_class(animation).strip())
        
        if specific_styles: current_styles.update(specific_styles)
        
        final_classes_str = " ".join(sorted(list(set(filter(None, final_classes_list)))))
        
        return self._build_attributes_string(final_classes_str, current_styles, data_attrs, other_attrs)

    def Header(self, spacing_before=Spacing.NONE, spacing_after=Spacing.LG, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="site-header", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, css_class, None, kwargs)
        self._append_html(f'<header {attrs_str}>')
        return ContextWrapper(self, "Header")

    def Footer(self, spacing_before=Spacing.XL, spacing_after=Spacing.NONE, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="site-footer", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, css_class, None, kwargs)
        self._append_html(f'<footer {attrs_str}>')
        return ContextWrapper(self, "Footer")

    def Navigation(self, items: list[dict], nav_type="main", align=Alignment.LEFT, spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        align_class_map = { Alignment.CENTER: "justify-content-center", Alignment.END: "justify-content-end", Alignment.START: "justify-content-start", Alignment.BETWEEN: "justify-content-between", Alignment.AROUND: "justify-content-around", Alignment.EVENLY: "justify-content-evenly" }
        align_flex_class = align_class_map.get(align, "justify-content-start")
        combined_css_class = f"nav-{nav_type} {align_flex_class} {css_class}".strip()
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, combined_css_class, None, kwargs)
        list_items_html = "".join(f'<li class="nav-item"><a class="nav-link {"active" if item.get("active") else ""}" href="{item.get("url", "#")}">{html.escape(item.get("text", "Link"))}</a></li>' for item in items)
        self._append_html(f'<nav {attrs_str}><ul class="nav">{list_items_html}</ul></nav>')
        return self

    def Container(self, fluid=False, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"container{'-fluid' if fluid else ''} {css_class}".strip(), None, kwargs)
        self._append_html(f'<div {attrs_str}>')
        return ContextWrapper(self, "Container")

    def FlexContainer(self, direction=FlexDirection.ROW, wrap=FlexWrap.NOWRAP, justify_content=Alignment.START, align_items=Alignment.START, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        flex_classes = f"d-flex flex-{direction.value} flex-{wrap.value} justify-content-{justify_content.value} align-items-{align_items.value}"
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"{flex_classes} {css_class}".strip(), None, kwargs)
        self._append_html(f'<div {attrs_str}>')
        return ContextWrapper(self, "FlexContainer")

    def Columns(self, n=2, gap=Spacing.DEFAULT, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        specific_styles = {'--column-count': str(n), '--column-gap': self._format_size(gap)}
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"columns {css_class}".strip(), specific_styles, kwargs)
        self._append_html(f'<div {attrs_str}>')
        return ContextWrapper(self, "Columns")

    def Grid(self, cols=None, gap=Spacing.DEFAULT, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        grid_classes = "grid"
        if cols: grid_classes += f" grid-cols-{cols}"
        grid_classes += f" gap-{gap.value if isinstance(gap, Spacing) else 'md'}"
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"{grid_classes} {css_class}".strip(), None, kwargs)
        self._append_html(f'<div {attrs_str}>')
        return ContextWrapper(self, "Grid")

    def Background(self, color=None, image=None, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, padding=Spacing.XL, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        specific_styles = {'padding': self._format_size(padding)}
        if color: specific_styles['background-color'] = color
        if image: specific_styles.update({'background-image': f"url('{image}')", 'background-size': 'cover', 'background-position': 'center'})
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"background-section {css_class}".strip(), specific_styles, kwargs)
        self._append_html(f'<div {attrs_str}>')
        return ContextWrapper(self, "Background")

    def Card(self, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"card {css_class}".strip(), None, kwargs)
        self._append_html(f'<div {attrs_str}><div class="card-body">')
        return ContextWrapper(self, "Card")

    def Write(self, text, align=Alignment.LEFT, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", text_size=None, text_color=None, **kwargs):
        alignment_class = self._get_alignment_class(align)
        combined_css_class = f"{alignment_class} {css_class}".strip()
        specific_styles = {}
        if text_size: specific_styles["font-size"] = text_size
        if text_color: specific_styles["color"] = text_color
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, combined_css_class, specific_styles if specific_styles else None, kwargs)
        self._append_html(f'<p {attrs_str}>{html.escape(text)}</p>')

    def Markdown(self, md_text, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        processed_md_text = md_text
        if hasattr(self, 'site') and self.site:
            processed_md_text = re.sub(
                r'(src|href)=(["\'])((?:\.\/|\/)?static\/)([^"\']+)\2',
                lambda m: f'{m.group(1)}={m.group(2)}{self.site._get_static_url(m.group(4))}{m.group(2)}',
                md_text,
                flags=re.IGNORECASE
            )
        
        html_content = ""
        try:
            html_content = markdown2.markdown(processed_md_text, extras=["fenced-code-blocks", "tables", "footnotes", "cuddled-lists", "nofollow", "spoiler", "strike", "target-blank-links", "task_list"])
        except Exception as e_md:
            error_message = f"ERROR converting Markdown to HTML. Input MD snippet: {html.escape(processed_md_text[:200])}... Error: {html.escape(str(e_md))}"
            print(error_message)
            html_content = f'<div class="alert alert-danger" role="alert">{error_message}</div>'

        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"markdown-content {css_class}".strip(), None, kwargs)
        self._append_html(f'<div {attrs_str}>{html_content}</div>')


    def BlockQuote(self, quote, author=None, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"blockquote {css_class}".strip(), None, kwargs)
        footer = f'<footer><cite title="Source Title">{html.escape(author)}</cite></footer>' if author else ''
        self._append_html(f'<blockquote {attrs_str}><p>{html.escape(quote)}</p>{footer}</blockquote>')

    def CodeBlock(self, code, language=None, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs_str = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"code-block {css_class}".strip(), None, kwargs)
        lang_class = f"language-{language}" if language else ""
        escaped_code = html.escape(code)
        self._append_html(f'<div {attrs_str}><pre><code class="{lang_class}">{escaped_code}</code></pre></div>')

    def Image(self, src, alt="", caption=None, width=None, height=None, object_fit=ObjectFit.COVER, align=Alignment.LEFT, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.FADE_IN, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        wrapper_css_class = f"image-wrapper align-{align.value} {css_class}".strip()
        attrs_wrapper = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, wrapper_css_class, None, kwargs)
        img_styles = {'object-fit': object_fit.value}
        if width: img_styles['width'] = self._format_size(width)
        if height: img_styles['height'] = self._format_size(height)
        img_style_attr = self._get_style_attr(img_styles)
        img_tag = f'<img src="{src}" alt="{html.escape(alt)}"{img_style_attr}>'
        caption_tag = f'<figcaption>{html.escape(caption)}</figcaption>' if caption else ''
        self._append_html(f'<figure {attrs_wrapper}>{img_tag}{caption_tag}</figure>')

    def Gallery(self, images: list[dict], columns=3, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.FADE_IN_UP, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs_container = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"gallery {css_class}".strip(), None, kwargs.pop("container_kwargs", {}))
        style_attr_inner = self._get_style_attr({'--gallery-columns': str(columns)})
        items_html = ""
        for i, img in enumerate(images):
            caption_tag = f'<figcaption>{html.escape(img.get("caption", ""))}</figcaption>' if img.get("caption") else ''
            item_attrs = self._get_combined_attributes(Spacing.NONE, Spacing.NONE, AnimationType.FADE_IN_UP, True, i * 0.1, "", None, img.get("item_kwargs", {}))
            items_html += f'<figure {item_attrs}><img src="{img["src"]}" alt="{html.escape(img.get("alt", ""))}">{caption_tag}</figure>'
        self._append_html(f'<div {attrs_container}><div class="gallery-grid"{style_attr_inner}>{items_html}</div></div>')

    def Carousel(self, slides: list[dict], autoplay=True, interval=5000, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"carousel slide {css_class}".strip(), None, kwargs)
        carousel_id = f"carousel-{id(self)}"
        slides_html, indicators_html = "", ""
        for i, slide in enumerate(slides):
            active_class = " active" if i == 0 else ""
            img_html = f'<img src="{slide["image"]}" class="d-block w-100" alt="{html.escape(slide.get("alt", ""))}">' if slide.get('image') else ""
            caption_html = f'<div class="carousel-caption d-none d-md-block"><h5>{html.escape(slide.get("title",""))}</h5><p>{html.escape(slide.get("text",""))}</p></div>' if slide.get('title') or slide.get('text') else ""
            slides_html += f'<div class="carousel-item{active_class}">{img_html}{caption_html}</div>'
            indicators_html += f'<button type="button" data-bs-target="#{carousel_id}" data-bs-slide-to="{i}" class="{active_class.strip()}" aria-current="{ "true" if i==0 else "false" }" aria-label="Slide {i+1}"></button>'
        controls_html = ""
        if len(slides) > 1: controls_html = f'<button class="carousel-control-prev" type="button" data-bs-target="#{carousel_id}" data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span class="visually-hidden">Previous</span></button><button class="carousel-control-next" type="button" data-bs-target="#{carousel_id}" data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span class="visually-hidden">Next</span></button>'
        interval_attr = f'data-bs-interval="{interval}"' if autoplay else ""
        self._append_html(f'<div id="{carousel_id}" {attrs} data-bs-ride="{"carousel" if autoplay else "false"}" {interval_attr}><div class="carousel-indicators">{indicators_html}</div><div class="carousel-inner">{slides_html}</div>{controls_html}</div>')

    def Button(self, text, link="#", style_type=ButtonType.PRIMARY, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        combined_css_class = f"btn btn-{style_type.value} {css_class}".strip()
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, combined_css_class, None, kwargs)
        self._append_html(f'<a href="{link}" {attrs} role="button">{html.escape(text)}</a>')

    def Link(self, url, text=None, new_tab=False, css_class="", **kwargs):
        display_text = html.escape(text or url)
        link_kwargs = {**kwargs, **({'target':'_blank', 'rel':'noopener noreferrer'} if new_tab else {})}
        attrs = self._get_combined_attributes(Spacing.NONE, Spacing.NONE, AnimationType.NONE, False, 0.0, css_class, None, link_kwargs)
        self._append_html(f'<a href="{url}" {attrs}>{display_text}</a>')

    def Tabs(self, items: list[dict], spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, css_class="", animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"tabs-container {css_class}".strip(), None, kwargs)
        tabs_id = f"tabs-{id(self)}"
        nav_html, content_html = '<ul class="nav nav-tabs" role="tablist">', '<div class="tab-content">'
        active_found = any(item.get('active', False) for item in items)
        for i, item in enumerate(items):
            tab_id, pane_id = f"{tabs_id}-tab-{i}", f"{tabs_id}-pane-{i}"
            title, content = item.get('title', f'Tab {i+1}'), item.get('content', '')
            is_active = item.get('active', False) if active_found else (i == 0)
            active_nav, active_pane = (" active", " show active") if is_active else ("", "")
            nav_html += f'<li class="nav-item" role="presentation"><button class="nav-link{active_nav}" id="{tab_id}" data-bs-toggle="tab" data-bs-target="#{pane_id}" type="button" role="tab" aria-controls="{pane_id}" aria-selected="{str(is_active).lower()}">{html.escape(title)}</button></li>'
            content_html += f'<div class="tab-pane fade{active_pane}" id="{pane_id}" role="tabpanel" aria-labelledby="{tab_id}">{content}</div>'
        nav_html += '</ul>'; content_html += '</div>'
        self._append_html(f'<div {attrs}>{nav_html}{content_html}</div>')

    def Accordion(self, items: list[dict], spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", always_open=False, **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"accordion {css_class}".strip(), None, kwargs)
        accordion_id = f"accordion-{id(self)}"
        items_html, parent_attr = "", f' data-bs-parent="#{accordion_id}"' if not always_open else ''
        for i, item in enumerate(items):
            heading_id, collapse_id = f"heading-{accordion_id}-{i}", f"collapse-{accordion_id}-{i}"
            title, content = item.get("title", f"Item {i+1}"), item.get("content", "")
            expanded = item.get('open', False)
            btn_class, collapse_class = ("accordion-button" + (" collapsed" if not expanded else "")), ("accordion-collapse collapse" + (" show" if expanded else ""))
            item_attrs = self._get_combined_attributes(Spacing.NONE, Spacing.NONE, AnimationType.FADE_IN_UP, True, i * 0.1, "accordion-item", None, item.get("item_kwargs", {}))
            items_html += f'<div {item_attrs}><h2 class="accordion-header" id="{heading_id}"><button class="{btn_class}" type="button" data-bs-toggle="collapse" data-bs-target="#{collapse_id}" aria-expanded="{str(expanded).lower()}" aria-controls="{collapse_id}">{html.escape(title)}</button></h2><div id="{collapse_id}" class="{collapse_class}" aria-labelledby="{heading_id}"{parent_attr}><div class="accordion-body">{content}</div></div></div>'
        self._append_html(f'<div {attrs} id="{accordion_id}">{items_html}</div>')

    def SocialShare(self, platforms=None, url=None, title=None, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, css_class="", align=Alignment.LEFT, **kwargs):
        alignment_class = self._get_alignment_class(align)
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, f"social-share {alignment_class} {css_class}".strip(), None, kwargs)
        supported = {"facebook", "twitter", "linkedin", "pinterest", "email", "whatsapp", "reddit"}
        platforms = platforms or supported
        share_url, share_title = quote_plus(url or ""), quote_plus(title or "")
        links_html = ""
        for p in platforms:
            p_lower = p.lower()
            if p_lower in supported:
                s_url = {"facebook": f"https://www.facebook.com/sharer/sharer.php?u={share_url}", "twitter": f"https://twitter.com/intent/tweet?url={share_url}&text={share_title}", "linkedin": f"https://www.linkedin.com/shareArticle?mini=true&url={share_url}&title={share_title}", "pinterest": f"https://pinterest.com/pin/create/button/?url={share_url}&description={share_title}", "email": f"mailto:?subject={share_title}&body={share_url}", "whatsapp": f"https://api.whatsapp.com/send?text={share_title}%20{share_url}", "reddit": f"https://www.reddit.com/submit?url={share_url}&title={share_title}"}.get(p_lower, "#")
                links_html += f'<a href="{s_url}" class="social-icon social-{p_lower}" target="_blank" rel="noopener noreferrer" aria-label="Share on {p.capitalize()}"><i class="icon-{p_lower}"></i></a> '
        self._append_html(f'<div {attrs}>{links_html.strip()}</div>')

    def Breadcrumbs(self, items: list[dict], spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, css_class="", **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, f"breadcrumbs-nav {css_class}".strip(), None, kwargs)
        items_html = ""
        if not items: return
        for i, item in enumerate(items):
            content = html.escape(item.get('text', ''))
            if not content: continue
            if 'link' in item and i < len(items) - 1: items_html += f'<li class="breadcrumb-item"><a href="{item["link"]}">{content}</a></li>'
            else: items_html += f'<li class="breadcrumb-item active" aria-current="page">{content}</li>'
        self._append_html(f'<nav aria-label="breadcrumb" {attrs}><ol class="breadcrumb">{items_html}</ol></nav>')

    def Table(self, headers, rows, striped=True, hover=True, bordered=False, small=False, responsive=True, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        tbl_classes = ["table"] + [cls for cond, cls in [(striped, "table-striped"), (hover, "table-hover"), (bordered, "table-bordered"), (small, "table-sm")] if cond]
        wrapper_attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"{'table-responsive' if responsive else ''} {css_class}".strip(), None, kwargs)
        thead = "<thead><tr>" + "".join(f'<th scope="col">{html.escape(str(h))}</th>' for h in headers) + "</tr></thead>"
        tbody = "<tbody>" + "".join("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows) + "</tbody>"
        table_html = f'<table class="{" ".join(tbl_classes)}">{thead}{tbody}</table>'
        if responsive: self._append_html(f'<div {wrapper_attrs}>{table_html}</div>')
        else:
            attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, " ".join(tbl_classes), None, kwargs)
            self._append_html(f'<table {attrs}>{thead}{tbody}</table>')

    def ProgressBar(self, percent, label=None, style_type=ColorTheme.PRIMARY, striped=False, animated=False, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, css_class="", height=None, **kwargs):
        specific_styles = {'height': self._format_size(height)} if height else {}
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, f"progress {css_class}".strip(), specific_styles, kwargs)
        bar_classes = ["progress-bar", f"bg-{style_type.value}"] + [cls for cond, cls in [(striped, "progress-bar-striped"), (animated, "progress-bar-animated")] if cond]
        label_text = f"{percent}%" if label is True else (html.escape(label) if isinstance(label, str) else "")
        self._append_html(f'<div {attrs}><div class="{" ".join(bar_classes)}" role="progressbar" style="width: {percent}%" aria-valuenow="{percent}" aria-valuemin="0" aria-valuemax="100">{label_text}</div></div>')

    def Timeline(self, events: list[dict], spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"timeline {css_class}".strip(), None, kwargs)
        items_html = ""
        if not events: return

        for i, event_item in enumerate(events):
            time_val, title_val, description_val = "", "", ""
            item_specific_kwargs = {}

            if isinstance(event_item, dict):
                time_val = event_item.get("time", "")
                title_val = event_item.get("title", "")
                description_val = event_item.get("description", "")
                item_specific_kwargs = event_item.get("item_kwargs", {})
            else:
                print(f"Warning: Timeline event at index {i} is not a dictionary: {event_item}. Rendering with default/empty values.")

            time_html = f'<div class="timeline-time">{html.escape(time_val)}</div>' if time_val else ""
            title_html = f'<h5 class="timeline-title">{html.escape(title_val)}</h5>' if title_val else ""
            desc_html = f'<p>{html.escape(description_val)}</p>' if description_val else ""
            
            item_attrs = self._get_combined_attributes(Spacing.NONE, Spacing.LG, AnimationType.FADE_IN_LEFT, True, i * 0.15, "timeline-item", None, item_specific_kwargs)
            items_html += f'<div {item_attrs}><div class="timeline-marker"></div><div class="timeline-content">{time_html}{title_html}{desc_html}</div></div>'
        
        self._append_html(f'<div {attrs}>{items_html}</div>')

    def Widget(self, title, description, link="#", link_text="Learn More", image_url=None,
                 image_width=None, image_height=None, image_object_fit=ObjectFit.COVER,
                 spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT,
                 animation=AnimationType.FADE_IN_UP, scroll_animation=False, scroll_animation_delay=0.0,
                 css_class="", **kwargs):
        base_widget_class = "widget-horizontal-layout"
        combined_css_class = f"{base_widget_class} {css_class}".strip()
        attrs = self._get_combined_attributes(
            spacing_before, spacing_after, animation, scroll_animation,
            scroll_animation_delay, combined_css_class, None, kwargs
        )
        img_html = ""
        if image_url:
            img_tag_styles = {
                'object-fit': image_object_fit.value,
                'display': 'block',
                'width': '100%',
                'height': '100%',
            }
            img_tag_style_attr = self._get_style_attr(img_tag_styles)
            img_container_styles = {}
            if image_width:
                img_container_styles['flex-basis'] = self._format_size(image_width)
                img_container_styles['width'] = self._format_size(image_width)
            if image_height:
                img_container_styles['height'] = self._format_size(image_height)
            
            img_container_style_attr = self._get_style_attr(img_container_styles)
            img_html = f'<div class="widget-image-container"{img_container_style_attr}><img src="{image_url}" alt="{html.escape(title)}"{img_tag_style_attr}></div>'

        link_html = f'<a href="{link}" class="btn btn-sm btn-outline-primary mt-auto widget-link">{html.escape(link_text)}</a>' if link and link_text else ""
        content_html = f"""
            <div class="widget-content-container d-flex flex-column">
                <h5 class="widget-title">{html.escape(title)}</h5>
                <p class="widget-description flex-grow-1">{html.escape(description)}</p>
                {link_html}
            </div>
        """
        self._append_html(f'<div {attrs}>{img_html}{content_html}</div>')

    def Icon(self, icon_name, size=Spacing.MD, color=None, spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, css_class="", **kwargs):
        size_map = { Spacing.XS: 'fa-xs', Spacing.SM: 'fa-sm', Spacing.MD: '', Spacing.LG: 'fa-lg', Spacing.XL: 'fa-2x' }
        size_val = self._format_size(size)
        size_class = size_map.get(size, '') if isinstance(size, Spacing) else ''
        specific_styles = {'color': color} if color else {}
        if not isinstance(size, Spacing) or not size_class:
             specific_styles.update({'font-size': size_val if size_val else '1em', 'line-height': '1', 'vertical-align': 'middle'})
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, f"{icon_name} {size_class} {css_class}".strip(), specific_styles, kwargs)
        self._append_html(f'<i {attrs} aria-hidden="true"></i>')

    def Divider(self, spacing_before=Spacing.LG, spacing_after=Spacing.LG, thickness=1, color="var(--bs-border-color)", css_class="", **kwargs):
        styles = self._apply_spacing_styles(spacing_before, spacing_after)
        styles['border'] = '0'
        styles['border-top-width'] = self._format_size(thickness)
        styles['border-top-style'] = 'solid'
        styles['border-top-color'] = color
        styles['height'] = '0'
        styles['opacity'] = kwargs.pop('opacity', '0.25')
        if 'style' in kwargs and isinstance(kwargs['style'], dict):
            kwarg_styles = kwargs.pop('style')
            styles.update(kwarg_styles)
        style_attr = self._get_style_attr(styles)
        final_classes = ["divider"]
        if css_class: final_classes.append(css_class)
        if 'class' in kwargs:
            kwarg_class_val = kwargs.pop('class')
            if isinstance(kwarg_class_val, str): final_classes.extend(kwarg_class_val.split())
            elif isinstance(kwarg_class_val, list): final_classes.extend(kwarg_class_val)
        unique_classes_list = list(dict.fromkeys(filter(None, final_classes)))
        class_attr_str = f' class="{" ".join(unique_classes_list)}"' if unique_classes_list else ""
        other_attrs_list = [f'{html.escape(str(k_attr))}="{html.escape(str(v_attr))}"' for k_attr, v_attr in kwargs.items()]
        other_attrs_str = " " + " ".join(other_attrs_list) if other_attrs_list else ""
        self._append_html(f'<hr{class_attr_str}{style_attr}{other_attrs_str}>')

    def Badge(self, text, style_type=ColorTheme.SECONDARY, pill=False, css_class="", spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, **kwargs):
        badge_classes = ["badge", f"bg-{style_type.value}"] + (["rounded-pill"] if pill else [])
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, f"{' '.join(badge_classes)} {css_class}".strip(), None, kwargs)
        self._append_html(f'<span {attrs}>{html.escape(text)}</span>')

    def Alert(self, text, style_type=ColorTheme.INFO, dismissible=False, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        alert_classes = ["alert", f"alert-{style_type.value}"] + (["alert-dismissible", "fade", "show"] if dismissible else [])
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, f"{' '.join(alert_classes)} {css_class}".strip(), None, kwargs)
        dismiss_btn = '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' if dismissible else ''
        self._append_html(f'<div {attrs} role="alert">{html.escape(text)}{dismiss_btn}</div>')

    def Form(self, action="#", method="post", spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, animation=AnimationType.NONE, scroll_animation=False, scroll_animation_delay=0.0, css_class="", **kwargs):
        other_attrs = {'action': action, 'method': method, **kwargs}
        attrs = self._get_combined_attributes(spacing_before, spacing_after, animation, scroll_animation, scroll_animation_delay, css_class, None, other_attrs)
        self._append_html(f'<form {attrs}>')
        return ContextWrapper(self, "Form")

    def FormGroup(self, spacing_before=Spacing.DEFAULT, spacing_after=Spacing.DEFAULT, css_class="form-group", **kwargs):
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, css_class, None, kwargs)
        self._append_html(f'<div {attrs}>')
        return ContextWrapper(self, "FormGroup")

    def Label(self, text, for_id=None, css_class="form-label", **kwargs):
        attrs_dict = {'for': for_id} if for_id else {}
        attrs_dict.update(kwargs)
        attrs = self._get_combined_attributes(Spacing.NONE, Spacing.XS, AnimationType.NONE, False, 0.0, css_class, None, attrs_dict)
        self._append_html(f'<label {attrs}>{html.escape(text)}</label>')

    def Input(self, input_type=InputType.TEXT, name="", value=None, placeholder=None, label=None, input_id=None, required=False, checked=None, css_class=None, spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, **kwargs):
        if not input_id and label: input_id = f"input-{name}-{id(self)}"
        final_css_class = css_class
        if final_css_class is None:
             final_css_class = "form-check-input" if input_type in [InputType.CHECKBOX, InputType.RADIO] else "form-control"
        input_attrs = {'type': input_type.value, 'name': name, 'id': input_id, 'placeholder': placeholder, 'value': value}
        if required: input_attrs['required'] = True
        if input_type in [InputType.CHECKBOX, InputType.RADIO] and checked is not None:
            if checked: input_attrs['checked'] = True
        input_attrs.update(kwargs)
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, final_css_class, None, input_attrs)
        if input_type in [InputType.CHECKBOX, InputType.RADIO] and label:
            self._append_html(f'<div class="form-check">')
            self._append_html(f'<input {attrs}>')
            self.Label(label, for_id=input_id, css_class="form-check-label")
            self._append_html('</div>')
        else:
            if label: self.Label(label, for_id=input_id)
            self._append_html(f'<input {attrs}>')

    def Textarea(self, name="", value=None, placeholder=None, label=None, input_id=None, required=False, rows=3, css_class="form-control", spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, **kwargs):
        if not input_id and label: input_id = f"textarea-{name}-{id(self)}"
        if label: self.Label(label, for_id=input_id)
        textarea_attrs = {'name': name, 'id': input_id, 'placeholder': placeholder, 'rows': rows}
        if required: textarea_attrs['required'] = True
        textarea_attrs.update(kwargs)
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, css_class, None, textarea_attrs)
        content = html.escape(value) if value else ""
        self._append_html(f'<textarea {attrs}>{content}</textarea>')

    def Select(self, name="", options=None, selected_value=None, label=None, input_id=None, required=False, css_class="form-select", spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, **kwargs):
        if options is None: options = []
        if not input_id and label: input_id = f"select-{name}-{id(self)}"
        if label: self.Label(label, for_id=input_id)
        select_attrs = {'name': name, 'id': input_id}
        if required: select_attrs['required'] = True
        select_attrs.update(kwargs)
        attrs = self._get_combined_attributes(spacing_before, spacing_after, AnimationType.NONE, False, 0.0, css_class, None, select_attrs)
        options_html = ""
        for opt in options:
            opt_value = opt.get('value', opt.get('text', ''))
            opt_text = html.escape(opt.get('text', opt.get('value', '')))
            is_selected = ' selected' if str(opt_value) == str(selected_value) else ''
            opt_disabled = ' disabled' if opt.get('disabled') else ''
            options_html += f'<option value="{html.escape(str(opt_value))}"{is_selected}{opt_disabled}>{opt_text}</option>'
        self._append_html(f'<select {attrs}>{options_html}</select>')

class Page(BaseComponent):
    def __init__(self, site, slug, title=""):
        super().__init__()
        self.site = site
        self.slug = slug.strip('/')
        self.title = title or slug.replace('-', ' ').replace('_', ' ').capitalize()
        self.meta = {}
        self.site_header_content = None
        self.site_footer_content = None

    def render(self, output_dir):
        env = self.site.jinja_env
        template = env.get_template("layout.j2")
        
        if self.site.meta.get('main_nav_items'):
            site_title_text = self.site.meta.get('site_title', 'My Site')
            
            site_title_link_href_orig = self.site.meta.get('site_header_title_link', './index.html')
            site_title_link_href = site_title_link_href_orig
            
            base_path_component_for_links = ""
            if self.site.meta.get('base_url'):
                parsed_base_url = urlparse(self.site.meta['base_url'])
                if parsed_base_url.path and parsed_base_url.path != "/":
                    base_path_component_for_links = parsed_base_url.path.rstrip('/')

            if site_title_link_href_orig.startswith('./'):
                cleaned_href = site_title_link_href_orig[2:]
                site_title_link_href = f"{base_path_component_for_links}/{cleaned_href}".replace('//','/')
            elif site_title_link_href_orig.startswith('/'):
                 site_title_link_href = f"{base_path_component_for_links}{site_title_link_href_orig}".replace('//','/')
            elif not urlparse(site_title_link_href_orig).scheme: 
                 site_title_link_href = f"{base_path_component_for_links}/{site_title_link_href_orig}".replace('//','/')
            
            if not site_title_link_href.startswith('/') and not urlparse(site_title_link_href).scheme:
                site_title_link_href = '/' + site_title_link_href
            if site_title_link_href == '/': site_title_link_href = base_path_component_for_links + '/' if base_path_component_for_links else '/'


            site_title_css_class = self.site.meta.get('site_header_title_css_class', 'site-title')
            site_title_html = f'<div class="{site_title_css_class.strip()}"><a href="{site_title_link_href}">{html.escape(site_title_text)}</a></div>'

            nav_items_list_original = self.site.meta['main_nav_items']
            nav_items_list_processed = []
            
            current_page_full_slug = self.slug 
            if current_page_full_slug == 'index': current_page_full_slug = '' 
                
            for item_orig in nav_items_list_original:
                item = item_orig.copy()
                item_url_parsed = urlparse(item.get("url", "#"))
                item_url_path_original = item_url_parsed.path 
                
                item_path_relative_to_base = item_url_path_original
                if base_path_component_for_links and item_url_path_original.startswith(base_path_component_for_links):
                    item_path_relative_to_base = item_url_path_original[len(base_path_component_for_links):]
                
                item_normalized_slug = item_path_relative_to_base.replace('.html', '').strip('/')
                if item_normalized_slug == 'index': item_normalized_slug = ''
                
                if item_normalized_slug == current_page_full_slug:
                    item['active'] = True
                else:
                    item['active'] = False
                nav_items_list_processed.append(item)

            nav_component_align = self.site.meta.get('main_nav_align', Alignment.CENTER) 
            nav_component_css_class = self.site.meta.get('main_nav_css_class', 'nav-main')

            nav_builder = BaseComponent()
            nav_builder.site = self.site 
            nav_builder.Navigation(
                items=nav_items_list_processed,
                align=nav_component_align,
                css_class=nav_component_css_class,
                spacing_before=Spacing.NONE, 
                spacing_after=Spacing.NONE
            )
            navigation_html_content = nav_builder.get_html()

            theme_toggle_button_html = ""
            if self.site.meta.get('site_header_theme_toggle_enabled', True):
                theme_toggle_icon_text = self.site.meta.get('site_header_theme_toggle_icon', '🌓')
                theme_toggle_css_class = self.site.meta.get('site_header_theme_toggle_css_class', '')
                theme_toggle_button_html = f'<button id="theme-toggle" title="Toggle theme" class="{theme_toggle_css_class.strip()}">{html.escape(theme_toggle_icon_text)}</button>'
            
            layout_container_base_class = 'container'
            if self.site.meta.get('site_header_layout_container_fluid', False):
                layout_container_base_class = 'container-fluid'
            
            default_layout_classes = "d-flex justify-content-between align-items-center"
            user_defined_layout_classes = self.site.meta.get('site_header_layout_container_css_class', default_layout_classes)
            
            if layout_container_base_class not in user_defined_layout_classes:
                 layout_container_css = f"{layout_container_base_class} {user_defined_layout_classes}".strip()
            else:
                layout_container_css = user_defined_layout_classes.strip()

            header_tag_main_css = self.site.meta.get('site_header_css_class', 'site-header')

            self.site_header_content = (
                f'<header class="{header_tag_main_css.strip()}">\n'
                f'  <div class="{layout_container_css}">\n'
                f'    {site_title_html}\n'
                f'    {navigation_html_content}\n'
                f'    {theme_toggle_button_html}\n'
                f'  </div>\n'
                f'</header>'
            )

        page_content = self.get_html()
        context_meta = {**self.site.meta, **self.meta}
        context_meta.setdefault('site_title', self.site.meta.get('site_title', 'My Site'))
        page_url_part = f"{self.slug}.html" if self.slug != "index" else ""
        base_url_abs = self.site.meta.get('base_url', '')
        if base_url_abs and not base_url_abs.endswith('/'): base_url_abs += '/'
        full_url = urljoin(base_url_abs, page_url_part)
        context_meta.setdefault('url', full_url)
        context_meta.setdefault('image', self.site.meta.get('default_og_image', ''))
        title_tag_content = self.title + (f" | {context_meta['site_title']}" if self.slug != "index" and context_meta.get('site_title') else "")
        output_path = os.path.join(output_dir, "index.html" if self.slug == "index" else f"{self.slug}.html")
        try:
            html_output = template.render(content=page_content, title=title_tag_content, meta=context_meta, current_year=datetime.datetime.now().year, page=self, site=self.site)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f: f.write(html_output)
        except Exception as e: print(f"    ERROR rendering template for page '{self.slug}': {e}")

class Site:
    def __init__(self, source_dir="src", content_dir="content", output_dir="docs"):
        self.source_dir, self.content_dir, self.output_dir = source_dir, content_dir, output_dir
        self.template_dir = os.path.join(source_dir, "templates")
        self.static_dir = os.path.join(source_dir, "static")
        self.scss_file = os.path.join(source_dir, "style.scss")
        self.pages, self.meta = {}, {'site_title': 'My Awesome Site', 'description': 'A site generated by sitegen.py', 'author': 'SiteGen User', 'keywords': 'static site generator, python', 'base_url': '', 'default_og_image': ''}
        self.jinja_env = Environment(loader=FileSystemLoader(self.template_dir), autoescape=select_autoescape(['html', 'xml', 'j2']), trim_blocks=True, lstrip_blocks=True)
        self.jinja_env.globals.update({'static_url': self._get_static_url, 'urljoin': urljoin, 'urlparse': urlparse, 'Alignment': Alignment, 'Spacing': Spacing, 'ButtonType': ButtonType, 'AnimationType': AnimationType, 'ObjectFit': ObjectFit, 'ColorTheme': ColorTheme, 'InputType': InputType, 'FlexDirection': FlexDirection, 'FlexWrap': FlexWrap, 'datetime': datetime})

    def set_meta(self, **kwargs): self.meta.update(kwargs)
    def add_page(self, slug, title="") -> Page:
        slug = slug.strip('/') or "index"
        if slug in self.pages: print(f"Warning: Page with slug '{slug}' already exists. Overwriting.")
        page_instance = Page(self, slug, title)
        self.pages[slug] = page_instance
        return page_instance
        
    def get_page(self, slug): return self.pages.get(slug.strip('/'))

    def _get_static_url(self, path_relative_to_static_dir, default=None):
        clean_path = path_relative_to_static_dir.lstrip('/')
        source_file_check_path = os.path.join(self.static_dir, clean_path)
        final_path_segment_after_static = clean_path
        
        if not os.path.exists(source_file_check_path):
            if default:
                default_clean_path = default.lstrip('/')
                print(f"Warning: Static file '{source_file_check_path}' not found, using default '{default_clean_path}'")
                final_path_segment_after_static = default_clean_path
            else:
                print(f"Warning: Static file '{source_file_check_path}' not found. Using original path: '{clean_path}'")
        
        base_path_component = ""
        if self.meta.get('base_url'):
            parsed_base_url = urlparse(self.meta['base_url'])
            if parsed_base_url.path and parsed_base_url.path != "/":
                base_path_component = parsed_base_url.path.rstrip('/')
        
        web_path = f"{base_path_component}/static/{final_path_segment_after_static}".replace("//", "/")
        if not web_path.startswith('/') and not urlparse(web_path).scheme: 
            web_path = '/' + web_path
        return web_path

    def _compile_scss(self):
        out_css_dir, out_css_path = os.path.join(self.output_dir, "static", "css"), os.path.join(self.output_dir, "static", "css", "style.css")
        os.makedirs(out_css_dir, exist_ok=True)
        if not os.path.exists(self.scss_file): raise FileNotFoundError(f"SCSS file not found: {self.scss_file}")
        try:
            print(f"Compiling {self.scss_file}...")
            css = sass.compile(filename=self.scss_file, output_style='compressed')
            with open(out_css_path, 'w', encoding='utf-8') as f: f.write(css)
            print(f"Successfully compiled SCSS to {out_css_path}")
            if os.path.getsize(out_css_path) == 0: raise RuntimeError("SCSS compilation resulted in an empty file.")
        except ImportError: print("Error: 'libsass' package not found. Install with: pip install libsass\nOr manually compile."); raise
        except sass.CompileError as e: print(f"Error compiling SCSS: {e}"); raise RuntimeError(f"SCSS compilation failed: {e}")
        except Exception as e: print(f"Unexpected SCSS compilation error: {e}"); raise RuntimeError(f"SCSS compilation failed unexpectedly: {e}")

    def _copy_static_files(self):
        out_static_dir = os.path.join(self.output_dir, "static")
        if os.path.exists(self.static_dir):
            if os.path.exists(out_static_dir):
                try: shutil.rmtree(out_static_dir)
                except OSError as e: print(f"Error removing '{out_static_dir}': {e}. Skipping static copy."); return
            try: shutil.copytree(self.static_dir, out_static_dir); print(f"Copied static files from {self.static_dir} to {out_static_dir}")
            except Exception as e: print(f"Error copying static files: {e}")
        else:
            print(f"Static source '{self.static_dir}' not found. Creating empty static subdirs in output.")
            for sub in ['css', 'js', 'img']: os.makedirs(os.path.join(out_static_dir, sub), exist_ok=True)

    def _generate_sitemap(self):
        base_url = self.meta.get('base_url')
        if not base_url or urlparse(base_url).hostname in ('localhost', '127.0.0.1', None) or not urlparse(base_url).scheme : print("Warning: 'base_url' not set to a valid absolute URL. Skipping sitemap."); return
        if not base_url.endswith('/'): base_url += '/'
        print("Generating sitemap.xml...")
        root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        today = datetime.date.today().isoformat()
        for slug, page in self.pages.items():
            doc = ET.SubElement(root, "url")
            loc = urljoin(base_url, f"{slug}.html" if slug != "index" else "")
            ET.SubElement(doc, "loc").text = loc
            ET.SubElement(doc, "lastmod").text = page.meta.get('lastmod', today)
            ET.SubElement(doc, "changefreq").text = page.meta.get('changefreq', 'weekly')
            ET.SubElement(doc, "priority").text = page.meta.get('priority', '1.0' if slug == 'index' else '0.8')
        try:
            tree = ET.ElementTree(root); ET.indent(tree, space="  ", level=0)
            tree.write(os.path.join(self.output_dir, "sitemap.xml"), encoding='utf-8', xml_declaration=True); print("Generated sitemap.xml")
        except Exception as e: print(f"Error generating sitemap: {e}")

    def build(self):
        print(f"Starting build process. Output directory: {self.output_dir}"); os.makedirs(self.output_dir, exist_ok=True)
        try:
            self._copy_static_files(); self._compile_scss()
            print(f"Rendering {len(self.pages)} pages...");
            if not self.pages: print("Warning: No pages defined.")
            for slug, page in self.pages.items(): print(f"  - Rendering: {slug}.html"); page.render(self.output_dir)
            self._generate_sitemap(); print("Build complete.")
        except (FileNotFoundError, ImportError, RuntimeError) as e: print(f"Build failed: {e}")
        except Exception as e: print(f"An unexpected error occurred during build: {e}")

    def _build_html_for_content(self, content_func, *args, **kwargs):
        unique_slug = "_temp_content_page_" + str(id(content_func))
        temp_page = Page(self, slug=unique_slug)
        temp_page.site = self 
        content_func(temp_page, *args, **kwargs)
        return temp_page.get_html()
    
    def _create_markdown_document_sub_page(self, project_main_page_slug, doc_content_filepath_relative_to_content_dir, doc_title, meta_info=None):
        md_source_path = os.path.join(self.content_dir, doc_content_filepath_relative_to_content_dir)
        if not os.path.exists(md_source_path):
            print(f"Warning: Markdown source for document page not found: {md_source_path}")
            return None

        doc_filename_stem = os.path.splitext(os.path.basename(doc_content_filepath_relative_to_content_dir))[0]
        doc_page_slug = f"{project_main_page_slug}/{doc_filename_stem}" 

        doc_page = self.add_page(doc_page_slug, doc_title)
        doc_page.site = self
        if meta_info:
            doc_page.meta.update(meta_info)
        doc_page.meta['is_subpage'] = True 
        
        try:
            with open(md_source_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            with doc_page.Container(css_class="py-lg document-page-container"):
                doc_page.Write(doc_title, align=Alignment.CENTER, css_class="h1 mb-lg", text_size="2.5rem")
                doc_page.Divider()
                doc_page.Markdown(md_content)
            return f"{doc_filename_stem}.html" 
        except Exception as e:
            print(f"Error creating markdown document page for {doc_content_filepath_relative_to_content_dir}: {e}")
            doc_page.Alert(f"Error loading content for {doc_title}: {e}", style_type=ColorTheme.DANGER)
            return f"{doc_filename_stem}.html"


    def add_blog_post(self, slug, title="", content_md_filename=None, author=None, date=None, meta_info=None):
        page_slug = f"blog/{slug.strip('/')}"
        blog_page = self.add_page(page_slug, title)
        blog_page.site = self
        
        effective_meta = meta_info.copy() if meta_info else {}
        if author: effective_meta['author'] = author
        if date: effective_meta['date'] = date
        blog_page.meta.update(effective_meta)

        md_content_to_render = None
        has_content_file_error = False

        if content_md_filename:
            md_path = os.path.join(self.content_dir, content_md_filename)
            try:
                with open(md_path, 'r', encoding='utf-8') as f: md_content_to_render = f.read()
            except FileNotFoundError:
                print(f"Warning: Markdown file '{content_md_filename}' not found for blog post '{title}'.")
                has_content_file_error = True
            except Exception as e:
                print(f"Warning: Could not read markdown file '{content_md_filename}' for blog post '{title}': {e}")
                has_content_file_error = True
        
        with blog_page.Container(css_class="py-lg"):
            blog_page.Write(title, css_class="h1 text-center mb-lg", text_size="3.5rem", scroll_animation=True, animation=AnimationType.FADE_IN_DOWN)
            
            meta_display_parts = []
            post_author = blog_page.meta.get('author')
            post_date = blog_page.meta.get('date')
            
            if post_author:
                meta_display_parts.append(f"By {post_author}")
            if post_date:
                meta_display_parts.append(f"Published on {post_date}")

            if md_content_to_render:
                try:
                    html_for_word_count = markdown2.markdown(md_content_to_render)
                    temp_et_root = ET.fromstring(f"<div>{html_for_word_count}</div>")
                    plain_text_for_word_count = "".join(temp_et_root.itertext())
                    word_count = len(plain_text_for_word_count.split())
                    WPM = 238 
                    reading_time_minutes = round(word_count / WPM)
                    if reading_time_minutes == 0 and word_count > 0: reading_time_minutes = 1 
                    if word_count > 0 : meta_display_parts.append(f"{reading_time_minutes} min read")
                except ET.ParseError:
                     plain_text_for_word_count = md_content_to_render
                     word_count = len(plain_text_for_word_count.split())
                     WPM = 238 
                     reading_time_minutes = round(word_count / WPM)
                     if reading_time_minutes == 0 and word_count > 0: reading_time_minutes = 1 
                     if word_count > 0 : meta_display_parts.append(f"{reading_time_minutes} min read")
                except Exception as e:
                    print(f"Warning: Could not calculate reading time for blog post '{title}': {e}")

            if meta_display_parts:
                with blog_page.FlexContainer(direction=FlexDirection.ROW, justify_content=Alignment.CENTER, wrap=FlexWrap.WRAP, css_class="text-muted blog-post-meta mb-md", spacing_before=Spacing.SM, spacing_after=Spacing.NONE):
                    for i, part_text in enumerate(meta_display_parts):
                        blog_page.Write(part_text, css_class="meta-item", spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, text_color="var(--bs-gray-600)")
                        if i < len(meta_display_parts) - 1:
                            blog_page.Write("•", css_class="meta-separator mx-sm", spacing_before=Spacing.NONE, spacing_after=Spacing.NONE, text_color="var(--bs-gray-600)")
            
            if meta_display_parts or md_content_to_render or has_content_file_error:
                 blog_page.Divider(spacing_before=Spacing.LG, spacing_after=Spacing.LG)

            if has_content_file_error:
                 blog_page.Alert(f"Content file '{content_md_filename}' could not be loaded for this post.", style_type=ColorTheme.DANGER, spacing_before=Spacing.MD)
            elif md_content_to_render:
                blog_page.Markdown(md_content_to_render)
            elif not content_md_filename: 
                blog_page.Write("No content provided for this blog post.", css_class="text-center", spacing_before=Spacing.MD)
        return blog_page

    def add_project_page(self, slug, title="", project_readme_file=None, timeline_events=None, technologies_used=None, project_documents=None, meta_info=None):
        if timeline_events is None: timeline_events = []
        if technologies_used is None: technologies_used = []
        if project_documents is None: project_documents = []
        
        project_slug_base_name = slug.strip('/') 
        page_slug_for_project = f"projects/{project_slug_base_name}"
        project_page = self.add_page(page_slug_for_project, title)
        project_page.site = self 
        if meta_info: project_page.meta.update(meta_info)
        
        tab_items = []
        has_active_tab = False

        if project_readme_file:
            readme_path = os.path.join(self.content_dir, project_readme_file)
            try:
                with open(readme_path, 'r', encoding='utf-8') as f: readme_md = f.read()
                readme_html = self._build_html_for_content(lambda p: p.Markdown(readme_md))
                tab_items.append({"title": "Overview", "content": readme_html, "active": True}); has_active_tab = True
            except Exception as e: 
                print(f"Error loading README {readme_path} for project {title}: {e}")
                tab_items.append({"title": "Overview", "content": f"<p>Error loading README: {html.escape(project_readme_file)}</p>", "active": True}); has_active_tab = True
        
        if timeline_events:
            timeline_html = self._build_html_for_content(lambda p: p.Timeline(events=timeline_events))
            tab_items.append({"title": "Timeline", "content": timeline_html, "active": not has_active_tab}); has_active_tab = True
        
        tech_docs_content_builder = BaseComponent()
        tech_docs_content_builder.site = self
        has_tech_docs_content = False

        if technologies_used:
            tech_html = "<p class='mb-sm'><strong>Technologies Used:</strong> " + "".join([f'<span class="badge bg-secondary me-xs mb-xs">{html.escape(tech)}</span>' for tech in technologies_used]) + "</p>"
            tech_docs_content_builder._append_html(tech_html)
            has_tech_docs_content = True

        if project_documents:
            tech_docs_content_builder._append_html("<h5 class='mt-md mb-sm'>Documents & Links:</h5>")
            doc_widgets_container = BaseComponent()
            doc_widgets_container.site = self

            with doc_widgets_container.Grid(cols=1, gap=Spacing.MD, css_class="project-document-widgets"):
                for doc_item in project_documents:
                    doc_title_text = doc_item.get("title", "Document")
                    doc_content_file_path = doc_item.get("url", "#") 
                    doc_description_text = doc_item.get("description", f"View {doc_title_text}.")
                    doc_image = doc_item.get("image_url", self._get_static_url("imgs/document_placeholder.png"))
                    
                    final_doc_link = "#"
                    
                    if doc_content_file_path.endswith(".md"):
                        relative_page_url_from_project_dir = self._create_markdown_document_sub_page(
                            page_slug_for_project, 
                            doc_content_file_path, 
                            doc_title_text,
                            meta_info={'project_parent_slug': page_slug_for_project}
                        )
                        if relative_page_url_from_project_dir:
                            final_doc_link = relative_page_url_from_project_dir 
                        else:
                            doc_description_text = f"Could not create page for {doc_title_text}"
                    elif not (doc_content_file_path.startswith(("http://", "https://")) or urlparse(doc_content_file_path).scheme):
                        source_doc_path = os.path.join(self.content_dir, doc_content_file_path)
                        target_doc_dir = os.path.join(self.output_dir, page_slug_for_project)
                        target_doc_filename = os.path.basename(doc_content_file_path)
                        target_doc_path = os.path.join(target_doc_dir, target_doc_filename)
                        
                        try:
                            os.makedirs(target_doc_dir, exist_ok=True)
                            if os.path.exists(source_doc_path):
                                shutil.copy2(source_doc_path, target_doc_path)
                                final_doc_link = quote(target_doc_filename) 
                            else:
                                print(f"Warning: Project document source file not found: {source_doc_path}")
                                doc_description_text = f"File not found: {doc_content_file_path}"
                        except Exception as e:
                            print(f"Error copying project document {source_doc_path} to {target_doc_path}: {e}")
                            doc_description_text = f"Error accessing file: {doc_content_file_path}"
                    else: 
                        final_doc_link = doc_content_file_path
                    
                    doc_widgets_container.Widget(
                        title=doc_title_text,
                        description=doc_description_text,
                        link= slug + "/" + final_doc_link,
                        link_text="View Document" if final_doc_link != "#" else "N/A",
                        image_url="/static/imgs/placeholder.png",
                        image_height="100px", 
                        image_width="100px",
                        object_fit=ObjectFit.CONTAIN
                    )
            tech_docs_content_builder._append_html(doc_widgets_container.get_html())
            has_tech_docs_content = True

        if has_tech_docs_content:
            tab_items.append({"title": "Tech & Docs", "content": tech_docs_content_builder.get_html(), "active": not has_active_tab}); has_active_tab = True
        
        if not tab_items:
             tab_items.append({"title": "Project Details", "content": "<p>No specific details provided for this project yet.</p>", "active": True})
        elif not any(t.get("active") for t in tab_items) and tab_items:
            tab_items[0]["active"] = True
            
        with project_page.Container(css_class="py-lg"):
            project_page.Write(title, css_class="h1 text-center mb-lg", scroll_animation=True, animation=AnimationType.FADE_IN_DOWN)
            if project_page.meta.get('subtitle'):
                 project_page.Write(project_page.meta['subtitle'], css_class="text-muted text-center mb-md", spacing_before=Spacing.NONE)
            project_page.Tabs(items=tab_items, spacing_before=Spacing.LG, scroll_animation=True, animation=AnimationType.FADE_IN_UP)
        return project_page

    def add_html_file_page(self, slug, title="", html_content_filepath=None, meta_info=None):
        page = self.add_page(slug, title)
        page.site = self
        if meta_info:
            page.meta.update(meta_info)

        if html_content_filepath:
            source_html_path = os.path.join(self.content_dir, html_content_filepath)
            try:
                with open(source_html_path, 'r', encoding='utf-8') as f:
                    raw_html_content = f.read()
                
                processed_html_content = raw_html_content
                if hasattr(page, 'site') and page.site:
                    processed_html_content = re.sub(
                        r'(src|href)=(["\'])((?:\.\/|\/)?static\/)([^"\']+)\2',
                        lambda m: f'{m.group(1)}={m.group(2)}{page.site._get_static_url(m.group(4))}{m.group(2)}',
                        raw_html_content,
                        flags=re.IGNORECASE
                    )
                page._append_html(processed_html_content)
            except FileNotFoundError:
                print(f"Warning: HTML content file not found: {source_html_path} for page '{slug}'")
                page.Alert(f"HTML content file '{html_content_filepath}' not found.", style_type=ColorTheme.DANGER)
            except Exception as e:
                print(f"Error reading HTML content file {source_html_path} for page '{slug}': {e}")
                page.Alert(f"Error reading HTML content file: {e}", style_type=ColorTheme.DANGER)
        else:
            page.Write("No HTML content file specified for this page.")
        return page
