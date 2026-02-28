document.addEventListener('DOMContentLoaded', () => {

  // ===== Theme Toggle =====
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  function setTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (themeToggle) {
      themeToggle.textContent = theme === 'dark' ? '\u2600\uFE0F' : '\uD83C\uDF19';
      themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    }
  }

  const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      setTheme(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
  }

  // ===== Font Toggle =====
  const fontToggle = document.getElementById('font-toggle');

  function setFont(font) {
    html.setAttribute('data-font', font);
    localStorage.setItem('font', font);
    if (fontToggle) {
      fontToggle.textContent = font === 'hard' ? 'Aa' : 'Aa';
      fontToggle.style.fontFamily = font === 'hard' ? 'Georgia, serif' : 'Inter, sans-serif';
      fontToggle.setAttribute('aria-label', font === 'hard' ? 'Switch to sans-serif font' : 'Switch to serif font');
    }
  }

  const savedFont = localStorage.getItem('font') || 'soft';
  setFont(savedFont);

  if (fontToggle) {
    fontToggle.addEventListener('click', () => {
      setFont(html.getAttribute('data-font') === 'hard' ? 'soft' : 'hard');
    });
  }

  // ===== Mobile Hamburger =====
  const hamburgers = document.querySelectorAll('.hamburger');
  hamburgers.forEach(btn => {
    btn.addEventListener('click', () => {
      const nav = btn.closest('.site-header').querySelector('.nav-main');
      if (nav) {
        const isOpen = nav.classList.toggle('open');
        btn.setAttribute('aria-expanded', String(isOpen));
        btn.textContent = isOpen ? '\u2715' : '\u2630';
      }
    });
  });

  // Close mobile nav when a link is clicked
  document.querySelectorAll('.site-header .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      const nav = link.closest('.nav-main');
      const btn = link.closest('.site-header').querySelector('.hamburger');
      if (nav && nav.classList.contains('open')) {
        nav.classList.remove('open');
        if (btn) { btn.setAttribute('aria-expanded', 'false'); btn.textContent = '\u2630'; }
      }
    });
  });

  // ===== Scroll Animations =====
  const scrollObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const anim = el.getAttribute('data-scroll-animation');
        const delay = el.getAttribute('data-scroll-animation-delay');
        if (anim) {
          el.classList.add('animate-' + anim, 'in-view');
          if (delay) el.style.animationDelay = delay;
        }
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('[data-scroll-animation]').forEach(el => scrollObserver.observe(el));

  // ===== Smooth scroll for anchor links =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#' || href.startsWith('#!')) return;
      try {
        const target = document.querySelector(href);
        if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
      } catch (_) {}
    });
  });

  // ===== Tabs =====
  document.querySelectorAll('.nav-tabs .nav-link:not(.disabled)').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-bs-target');
      if (!targetId) return;
      const pane = document.querySelector(targetId);
      if (!pane) return;

      const tabBar = btn.closest('.nav-tabs');
      if (tabBar) {
        tabBar.querySelectorAll('.nav-link').forEach(l => { l.classList.remove('active'); l.setAttribute('aria-selected', 'false'); });
      }
      const content = pane.closest('.tab-content');
      if (content) {
        content.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active', 'show'));
      }
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      pane.classList.add('active');
      requestAnimationFrame(() => pane.classList.add('show'));
    });
  });

  // ===== Accordion =====
  document.querySelectorAll('.accordion-button').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-bs-target');
      if (!targetId) return;
      const collapse = document.querySelector(targetId);
      if (!collapse) return;

      const accordion = btn.closest('.accordion');
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';

      // Close other items if not always-open
      if (accordion && !accordion.dataset.alwaysOpen) {
        accordion.querySelectorAll('.accordion-collapse.show').forEach(open => {
          if (open !== collapse) {
            const otherBtn = accordion.querySelector('[data-bs-target="#' + open.id + '"]');
            if (otherBtn) { otherBtn.classList.add('collapsed'); otherBtn.setAttribute('aria-expanded', 'false'); }
            open.classList.remove('show');
          }
        });
      }

      btn.classList.toggle('collapsed');
      btn.setAttribute('aria-expanded', String(!isExpanded));
      collapse.classList.toggle('show');
    });
  });

  // ===== Back to Top =====
  const backToTop = document.querySelector('.back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ===== Lazy Loading Images =====
  if ('loading' in HTMLImageElement.prototype) {
    document.querySelectorAll('img:not([loading])').forEach(img => {
      img.setAttribute('loading', 'lazy');
    });
  }

  // ===== Animated Counters (for stat cards) =====
  const counters = document.querySelectorAll('[data-count-to]');
  if (counters.length) {
    const counterObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-count-to'), 10);
          if (isNaN(target)) return;
          const duration = 1500;
          const start = performance.now();
          const animate = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
            el.textContent = Math.round(eased * target);
            if (progress < 1) requestAnimationFrame(animate);
          };
          requestAnimationFrame(animate);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.3 });
    counters.forEach(el => counterObserver.observe(el));
  }

  // ===== Skill Bar Animation =====
  const skillBars = document.querySelectorAll('.skill-bar-fill[data-width]');
  if (skillBars.length) {
    const skillObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.getAttribute('data-width');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    skillBars.forEach(el => { el.style.width = '0'; skillObserver.observe(el); });
  }

});
