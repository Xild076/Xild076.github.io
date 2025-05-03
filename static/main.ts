const sections = document.querySelectorAll('main section');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      (e.target as HTMLElement).classList.add('visible');
    }
  });
});
sections.forEach(s => observer.observe(s));
