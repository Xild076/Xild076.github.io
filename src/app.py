from py2web import Site, Page, Heading, Text, Slider, Button, BrythonSimulation, SiteLink

site = Site("Harry Yin")

home = Page("index", "...", theme="dark")
home.add(Heading("Harry Yin", level=1, align="center"))
site.add_page(home)

about = Page("about", "About", theme="light")
about.add(SiteLink("index.html", "← Back to Demo"))
site.add_page(about)

site.build("docs")
