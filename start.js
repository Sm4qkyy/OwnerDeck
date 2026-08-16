/* ==========================================================================
   Ownerdeck — the get-started flow

   Three questions, then a handoff. The point is that the site does the
   qualifying: by the time a WhatsApp thread opens, it already says what the
   business is, which hand they want, and what they asked for. No more
   "hi, interested" threads that take four messages to get anywhere.

   Nothing is sent anywhere. Every answer stays in this page and ends up in a
   wa.me link the visitor chooses to open. That is deliberate — it means the
   flow collects no personal data, needs no consent, and cannot leak.

   Progressive enhancement: all four steps are in the markup. With scripting
   off they render as one long readable page with a working WhatsApp link at
   the bottom. This file only ever hides steps and fills in the summary.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('start');
  if (!root) return;

  var CFG = window.OD_CONFIG || {};
  var WA = (CFG.whatsappNumber || '447520689685').replace(/[^0-9]/g, '');

  var steps = Array.prototype.slice.call(root.querySelectorAll('[data-step]'));
  if (!steps.length) return;

  var answers = { trade: '', plan: '', planPrice: '', note: '' };
  var at = 0;

  /* Only now that scripting is confirmed do we collapse to one step at a
     time. Doing this in CSS would strand a no-JS visitor on step one. */
  root.classList.add('is-stepped');

  var dots = root.querySelector('.flow__dots');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function paintDots() {
    if (!dots) return;
    Array.prototype.forEach.call(dots.children, function (d, i) {
      d.setAttribute('aria-current', i === at ? 'step' : 'false');
      d.classList.toggle('is-done', i < at);
    });
  }

  function show(next) {
    if (next < 0 || next >= steps.length) return;
    var from = steps[at];
    at = next;

    steps.forEach(function (s, i) { s.hidden = i !== at; });
    paintDots();

    // Keep the top of the flow in view rather than the top of the document,
    // so the header does not swallow the question.
    var y = root.getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' });

    // Move focus to the new question so a screen reader announces it. The
    // heading is not naturally focusable, hence tabindex -1 in the markup.
    var h = steps[at].querySelector('[data-focus]');
    if (h) h.focus({ preventScroll: true });

    if (at === steps.length - 1) summarise();
    if (from) from.classList.remove('is-in');
    requestAnimationFrame(function () { steps[at].classList.add('is-in'); });
  }

  /* ---- choices --------------------------------------------------------- */
  root.addEventListener('click', function (e) {
    var pick = e.target.closest && e.target.closest('[data-pick]');
    if (pick) {
      var group = pick.getAttribute('data-pick');
      var siblings = root.querySelectorAll('[data-pick="' + group + '"]');
      Array.prototype.forEach.call(siblings, function (b) {
        b.setAttribute('aria-pressed', b === pick ? 'true' : 'false');
      });
      answers[group] = pick.getAttribute('data-value') || '';
      if (group === 'plan') answers.planPrice = pick.getAttribute('data-price') || '';
      // A choice is the answer to the question, so move on rather than making
      // them find a Next button.
      setTimeout(function () { show(at + 1); }, reduce ? 0 : 180);
      return;
    }

    var go = e.target.closest && e.target.closest('[data-go]');
    if (go) {
      e.preventDefault();
      show(at + (go.getAttribute('data-go') === 'back' ? -1 : 1));
    }
  });

  var note = root.querySelector('#flow-note');
  if (note) {
    note.addEventListener('input', function () {
      answers.note = note.value.trim().slice(0, 400);
    });
  }

  /* ---- the handoff ----------------------------------------------------- */
  function message() {
    var lines = ['Hi Mark — I came through the Ownerdeck site.'];
    if (answers.trade) lines.push('Business: ' + answers.trade);
    if (answers.plan) {
      lines.push('Interested in: ' + answers.plan +
                 (answers.planPrice ? ' (' + answers.planPrice + ')' : ''));
    }
    if (answers.note) lines.push('', answers.note);
    return lines.join('\n');
  }

  function summarise() {
    var out = root.querySelector('#flow-summary');
    if (out) {
      out.innerHTML = '';
      [['Business', answers.trade],
       ['Plan', answers.plan + (answers.planPrice ? ' · ' + answers.planPrice : '')],
       ['Notes', answers.note]
      ].forEach(function (row) {
        if (!row[1] || !row[1].trim() || row[1].trim() === '·') return;
        var dt = document.createElement('dt'); dt.textContent = row[0];
        var dd = document.createElement('dd'); dd.textContent = row[1];
        out.appendChild(dt); out.appendChild(dd);
      });
    }

    var link = root.querySelector('#flow-wa');
    if (link) link.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message());

    var mail = root.querySelector('#flow-mail');
    if (mail) {
      mail.href = 'mailto:' + (CFG.email || 'mark@ownerdeck.com') +
        '?subject=' + encodeURIComponent('Ownerdeck enquiry') +
        '&body=' + encodeURIComponent(message());
    }
  }

  /* ---- deposit ---------------------------------------------------------
     Optional and non-blocking. If the endpoint is not configured, or Stripe
     is unreachable, the button hides itself and the WhatsApp handoff beside
     it is untouched — a payment problem must never cost a lead. */
  var STORE = 'od_flow';

  function remember() {
    try { sessionStorage.setItem(STORE, JSON.stringify(answers)); } catch (e) {}
  }
  function recall() {
    try {
      var saved = JSON.parse(sessionStorage.getItem(STORE) || '{}');
      Object.keys(answers).forEach(function (k) {
        if (typeof saved[k] === 'string') answers[k] = saved[k];
      });
    } catch (e) {}
  }

  var payBtn = root.querySelector('#flow-pay');
  if (payBtn) {
    payBtn.addEventListener('click', function (e) {
      e.preventDefault();
      if (payBtn.getAttribute('aria-busy') === 'true') return;
      payBtn.setAttribute('aria-busy', 'true');
      var label = payBtn.querySelector('span');
      var was = label ? label.textContent : '';
      if (label) label.textContent = 'Opening secure checkout…';

      // The redirect leaves the page, so the answers have to survive it.
      remember();

      fetch('/api/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trade: answers.trade, plan: answers.plan, note: answers.note })
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (out) {
          if (out.ok && out.j && out.j.url) { window.location.href = out.j.url; return; }
          throw new Error((out.j && out.j.error) || 'failed');
        })
        .catch(function () {
          payBtn.removeAttribute('aria-busy');
          if (label) label.textContent = was;
          var box = root.querySelector('#flow-pay-wrap');
          if (box) box.hidden = true;   // fall back to the WhatsApp handoff
        });
    });
  }

  /* Coming back from Stripe. */
  (function fromCheckout() {
    var m = /[?&]deposit=(paid|cancelled)/.exec(window.location.search);
    if (!m) return;
    recall();
    var paid = m[1] === 'paid';
    var banner = root.querySelector('#flow-paid');
    if (banner && paid) {
      banner.hidden = false;
      var wrap = root.querySelector('#flow-pay-wrap');
      if (wrap) wrap.hidden = true;
      answers.note = (answers.note ? answers.note + '\n\n' : '') +
                     'I have paid the 75 EUR holding deposit.';
    }
    show(steps.length - 1);
  })();

  /* A plan can be chosen from the pricing page: /start?plan=Deck lands on the
     trade question with the plan already answered. */
  (function preselect() {
    if (/[?&]deposit=/.test(window.location.search)) return;   // handled above
    var m = /[?&]plan=([^&]+)/.exec(window.location.search);
    if (!m) return show(0);
    var want = decodeURIComponent(m[1]).toLowerCase();
    var btn = root.querySelector('[data-pick="plan"][data-value="' + want.replace(/"/g, '') + '" i]');
    if (!btn) {
      btn = Array.prototype.filter.call(
        root.querySelectorAll('[data-pick="plan"]'),
        function (b) { return (b.getAttribute('data-value') || '').toLowerCase() === want; })[0];
    }
    if (btn) {
      btn.setAttribute('aria-pressed', 'true');
      answers.plan = btn.getAttribute('data-value') || '';
      answers.planPrice = btn.getAttribute('data-price') || '';
    }
    show(0);
  })();
})();
