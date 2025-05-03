(() => {
  // static/main.ts
  var sections = document.querySelectorAll("main section");
  var observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
      }
    });
  });
  sections.forEach((s) => observer.observe(s));
})();
