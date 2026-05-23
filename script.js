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

// Hide Stripe direct-subscribe link if the placeholder hasn't been filled
const stripeDirect = document.getElementById('stripe-direct');
if (stripeDirect && stripeDirect.href.includes('STRIPE_PAYMENT_LINK_HERE')) {
  const parent = stripeDirect.closest('.price-cta-secondary');
  if (parent) parent.style.display = 'none';
}

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
