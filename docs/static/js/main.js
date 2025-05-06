document.addEventListener('DOMContentLoaded', () => {

    const themeToggleButton = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const currentTheme = localStorage.getItem('theme') || (prefersDarkScheme.matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', currentTheme);
  
    if (themeToggleButton) {
      themeToggleButton.addEventListener('click', () => {
        let newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
      });
    }
  
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };
  
    const observerCallback = (entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const animationName = el.getAttribute('data-scroll-animation');
          const animationDelay = el.getAttribute('data-scroll-animation-delay');
  
          if (animationName) {
            el.classList.add(`animate-${animationName}`);
            if (animationDelay) {
              el.style.animationDelay = animationDelay;
            }
            el.classList.add('in-view');
          }
          observer.unobserve(el);
        }
      });
    };
  
    const scrollObserver = new IntersectionObserver(observerCallback, observerOptions);
    const animatedElements = document.querySelectorAll('[data-scroll-animation]');
    animatedElements.forEach(el => {
      scrollObserver.observe(el);
    });
  
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === "#" || href.startsWith("#!") ) return; // Exclude simple hash or hashbang for JS frameworks
  
        try {
          const targetElement = document.querySelector(href);
          if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({ behavior: 'smooth' });
          }
        } catch (error) {
          // If querySelector fails (e.g. invalid selector), let the browser handle normally
          console.warn('Smooth scroll failed for selector:', href, error);
        }
      });
    });
  
  
    const tabButtons = document.querySelectorAll('.nav-tabs .nav-link:not(.disabled)');
    tabButtons.forEach(button => {
      button.addEventListener('click', (event) => {
          if (typeof bootstrap !== 'undefined' && bootstrap.Tab.getInstance(button)) {
              return;
          }
          event.preventDefault();
          const targetPaneId = button.getAttribute('data-bs-target');
          if (!targetPaneId) return;
          const targetPane = document.querySelector(targetPaneId);
          if (!targetPane) return;
  
          const tabContainer = button.closest('.nav-tabs');
          if (tabContainer) {
              tabContainer.querySelectorAll('.nav-link').forEach(link => {
                  link.classList.remove('active');
                  link.setAttribute('aria-selected', 'false');
              });
          }
  
          const contentContainer = targetPane.closest('.tab-content');
          if (contentContainer) {
              contentContainer.querySelectorAll('.tab-pane').forEach(pane => {
                  pane.classList.remove('active', 'show');
              });
          }
  
          button.classList.add('active');
          button.setAttribute('aria-selected', 'true');
          targetPane.classList.add('active');
          requestAnimationFrame(() => {
               targetPane.classList.add('show');
          });
      });
    });
  
    const accordionButtons = document.querySelectorAll('.accordion-button');
    accordionButtons.forEach(button => {
      button.addEventListener('click', () => {
          if (typeof bootstrap !== 'undefined' && bootstrap.Collapse.getInstance(document.querySelector(button.getAttribute('data-bs-target')))) {
              return;
          }
  
          const targetCollapseId = button.getAttribute('data-bs-target');
          if (!targetCollapseId) return;
          const targetCollapse = document.querySelector(targetCollapseId);
          if (!targetCollapse) return;
  
          const accordion = button.closest('.accordion');
          const isExpanded = button.getAttribute('aria-expanded') === 'true';
          
          const parentSelector = accordion ? accordion.getAttribute('id') : null;
  
  
          if (accordion && parentSelector && accordion.getAttribute('data-bs-parent')) { // Check if data-bs-parent is set for "always_open=False" behavior
               accordion.querySelectorAll(`#${parentSelector} .accordion-collapse.show`).forEach(openCollapse => {
                   if (openCollapse !== targetCollapse) {
                       const otherButton = accordion.querySelector(`[data-bs-target="#${openCollapse.id}"]`);
                       if (otherButton) {
                           otherButton.classList.add('collapsed');
                           otherButton.setAttribute('aria-expanded', 'false');
                       }
                       openCollapse.classList.remove('show');
                   }
               });
          }
  
          button.classList.toggle('collapsed');
          button.setAttribute('aria-expanded', String(!isExpanded));
          targetCollapse.classList.toggle('show');
      });
    });
  
  });