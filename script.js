// Nav scroll state
const nav = document.getElementById('nav');
const onScroll = () => {
  if (window.scrollY > 20) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Mobile nav toggle
const hamburger = document.getElementById('nav-hamburger');
if (hamburger) {
  hamburger.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('nav-mobile-open');
    hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    hamburger.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
  });
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('nav-mobile-open');
      hamburger.setAttribute('aria-expanded', 'false');
      hamburger.setAttribute('aria-label', 'Open menu');
    });
  });
}

// FAQ accordion
document.querySelectorAll('.faq-q').forEach(q => {
  q.setAttribute('aria-expanded', 'false');
  q.addEventListener('click', () => {
    const item = q.parentElement;
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => {
      i.classList.remove('open');
      i.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
    });
    if (!wasOpen) {
      item.classList.add('open');
      q.setAttribute('aria-expanded', 'true');
    }
  });
});

// Hide any Stripe subscribe links that still have a placeholder URL
document.querySelectorAll('.stripe-subscribe-link').forEach(link => {
  if (link.href.includes('STRIPE_PAYMENT_LINK')) {
    const container = link.closest('.tier-subscribe, .price-cta-secondary');
    if (container) container.style.display = 'none';
    else link.style.display = 'none';
  }
});

// Reveal-on-scroll animation
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('.reveal:not(.visible)').forEach(el => io.observe(el));
