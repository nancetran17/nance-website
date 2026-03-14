/* ============================================
   NANCE â Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // --- Mobile Nav Toggle ---
  const toggle = document.querySelector('.nav__toggle');
  const navLinks = document.querySelector('.nav__links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('nav__toggle--open');
      navLinks.classList.toggle('nav__links--open');
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('.nav__link').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('nav__toggle--open');
        navLinks.classList.remove('nav__links--open');
      });
    });
  }

  // --- Scroll-based nav background ---
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 50) {
        nav.classList.add('nav--scrolled');
      } else {
        nav.classList.remove('nav--scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // --- Scroll-triggered fade-in animations ---
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    fadeEls.forEach((el, i) => {
      el.style.transitionDelay = `${i * 0.05}s`;
      observer.observe(el);
    });
  }

  // --- Active page detection ---
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('nav__link--active');
    }
  });

  // --- Typing effect for hero (home page only) ---
  const heroTyping = document.querySelector('.hero__typing');
  if (heroTyping) {
    const phrases = [
      'building something new.',
      'writing funny thoughts.',
      'geeking out over space.',
      'tinkering with robotics.',
      'exploring mountains.',
      'tending to my plants.',
      'understanding the world better.'
    ];
    let phraseIndex = 0;
    let charIndex = 0;
    let deleting = false;
    let pause = false;

    function type() {
      const current = phrases[phraseIndex];

      if (pause) {
        pause = false;
        setTimeout(type, 1800);
        return;
      }

      if (!deleting) {
        heroTyping.textContent = current.substring(0, charIndex + 1);
        charIndex++;
        if (charIndex === current.length) {
          deleting = true;
          pause = true;
        }
      } else {
        heroTyping.textContent = current.substring(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          deleting = false;
          phraseIndex = (phraseIndex + 1) % phrases.length;
        }
      }

      const speed = deleting ? 40 : 80;
      setTimeout(type, speed);
    }

    setTimeout(type, 1200);
  }

  // --- Gallery lightbox ---
  const galleryItems = document.querySelectorAll('.gallery-grid__item');
  if (galleryItems.length > 0) {
    // Create lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = `
      <div class="lightbox__backdrop"></div>
      <div class="lightbox__content">
        <img class="lightbox__img" src="" alt="" />
        <p class="lightbox__caption"></p>
        <button class="lightbox__close" aria-label="Close">&times;</button>
      </div>
    `;
    document.body.appendChild(lightbox);

    // Add lightbox styles
    const lbStyle = document.createElement('style');
    lbStyle.textContent = `
      .lightbox {
        position: fixed; inset: 0; z-index: 9999;
        display: none; align-items: center; justify-content: center;
      }
      .lightbox--open { display: flex; }
      .lightbox__backdrop {
        position: absolute; inset: 0;
        background: rgba(6, 8, 16, 0.92);
        backdrop-filter: blur(8px);
      }
      .lightbox__content {
        position: relative; max-width: 90vw; max-height: 85vh;
        display: flex; flex-direction: column; align-items: center;
        animation: lbIn 0.3s ease;
      }
      @keyframes lbIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
      .lightbox__img {
        max-width: 90vw; max-height: 75vh;
        border-radius: 8px; object-fit: contain;
      }
      .lightbox__caption {
        color: rgba(232,228,223,0.7); font-size: 0.9rem;
        margin-top: 12px; text-align: center;
      }
      .lightbox__close {
        position: absolute; top: -40px; right: -10px;
        background: none; border: none; color: #e8e4df;
        font-size: 2rem; cursor: pointer; padding: 8px;
        transition: color 0.2s;
      }
      .lightbox__close:hover { color: #74c69d; }
    `;
    document.head.appendChild(lbStyle);

    galleryItems.forEach(item => {
      item.addEventListener('click', () => {
        const img = item.querySelector('img');
        const caption = item.querySelector('.gallery-grid__caption');
        if (img) {
          lightbox.querySelector('.lightbox__img').src = img.src;
          lightbox.querySelector('.lightbox__img').alt = img.alt;
          lightbox.querySelector('.lightbox__caption').textContent = caption ? caption.textContent : '';
          lightbox.classList.add('lightbox--open');
        }
      });
    });

    lightbox.querySelector('.lightbox__backdrop').addEventListener('click', () => {
      lightbox.classList.remove('lightbox--open');
    });
    lightbox.querySelector('.lightbox__close').addEventListener('click', () => {
      lightbox.classList.remove('lightbox--open');
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') lightbox.classList.remove('lightbox--open');
    });
  }

});
