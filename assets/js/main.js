/* ================================================================
   HAKODATE TOURISM STRATEGY — Main JS
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initScrollReveal();
  initHeaderScroll();
  initSubNavHighlight();
});

/* --- Mobile Navigation --- */
function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!toggle || !mobileMenu) return;

  toggle.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('is-open');
    toggle.classList.toggle('is-active');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close on link click
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('is-open');
      toggle.classList.remove('is-active');
      document.body.style.overflow = '';
    });
  });

  // Accordion for 主要施策
  const accToggles = mobileMenu.querySelectorAll('.mobile-accordion__toggle');
  accToggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const body = btn.nextElementSibling;
      btn.classList.toggle('is-open');
      body.classList.toggle('is-open');
    });
  });
}

/* --- Header hide on scroll down --- */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  let lastY = 0;
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const y = window.scrollY;
        if (y > 200 && y > lastY) {
          header.classList.add('is-hidden');
        } else {
          header.classList.remove('is-hidden');
        }
        lastY = y;
        ticking = false;
      });
      ticking = true;
    }
  });
}

/* --- Scroll Reveal (fade-in) --- */
function initScrollReveal() {
  const els = document.querySelectorAll('.fade-in');
  if (els.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px'
    });
    els.forEach(el => observer.observe(el));
  }

  /* Staggered reveal for cards/grid items */
  const staggerEls = document.querySelectorAll('.fade-in-stagger');
  if (staggerEls.length) {
    const staggerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const parent = entry.target.parentElement;
          const siblings = parent.querySelectorAll('.fade-in-stagger');
          siblings.forEach((el, i) => {
            el.style.transitionDelay = (i * 120) + 'ms';
            el.classList.add('is-visible');
          });
          siblings.forEach(el => staggerObserver.unobserve(el));
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -30px 0px'
    });
    staggerEls.forEach(el => staggerObserver.observe(el));
  }
}

/* --- Sub-nav scroll highlight (for anchor-based sub-navs) --- */
function initSubNavHighlight() {
  const subNav = document.querySelector('.header-lower');
  if (!subNav) return;

  const links = subNav.querySelectorAll('a[href^="#"]');
  if (!links.length) return;

  const sections = [];
  links.forEach(link => {
    const id = link.getAttribute('href').slice(1);
    const section = document.getElementById(id);
    if (section) sections.push({ el: section, link: link });
  });

  if (!sections.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const match = sections.find(s => s.el === entry.target);
      if (match) {
        if (entry.isIntersecting) {
          links.forEach(l => l.classList.remove('is-active'));
          match.link.classList.add('is-active');
        }
      }
    });
  }, {
    threshold: 0.2,
    rootMargin: '-120px 0px -50% 0px'
  });

  sections.forEach(s => observer.observe(s.el));
}
