from py2web import Site, Page, Heading, Text, Slider, Button, BrythonSimulation, SiteLink, Container

site = Site("EvolutionDemo")

home = Page("index", "Evolution ML Demo", theme="dark")
home.add(Heading("Evolutionary Simulation", level=1, align="center"))
home.add(Text("Watch organisms evolve toward the center line.", align="center"))
home.add(BrythonSimulation("evoCanvas", "evolution_sim.py", "100%", "300px"))
home.add(Container([
    Slider("Speed", 1, 10, 1, 5),
    Slider("Population", 10, 200, 10, 60),
    Button("Restart", onclick="animate")
], layout="row", gap="2rem"))
home.add(SiteLink("about.html", "Learn More"))
site.add_page(home)

about = Page("about", "About", theme="light")
about.add(Text("This demo uses a simple evolutionary algorithm to illustrate selection and mutation."))
about.add(SiteLink("index.html", "← Back to Demo"))
site.add_page(about)

site.build("output")
