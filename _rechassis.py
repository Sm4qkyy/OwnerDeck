# Re-chassis the long-form pages onto brand.css.
#
# terms.html is not just a page: _build_guides.py and _build_stats.py read
# their head/header/footer out of it by slicing on the literal strings
# "<main>" and "</main>". So the <main> tag here stays bare and unattributed —
# put a class on it and six other pages stop building.
import io, re, sys

THEME_BOOT = """<script>
(function () {
  var r = document.documentElement;
  r.classList.add('js');
  try {
    var t = localStorage.getItem('od_theme');
    if (t === 'light' || t === 'dark') r.setAttribute('data-theme', t);
  } catch (e) {}
})();
</script>"""

FONT_HEAD = """<link rel="preload" href="fonts/fraunces-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/switzer-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="brand.css?v=20260815">"""

HEADER = """<header class="masthead">
  <div class="wrap masthead__bar">
    <a class="masthead__mark" href="/">Ownerdeck</a>
    <nav class="masthead__nav" aria-label="Sections">
      <a href="/#cards">The cards</a>
      <a href="/#pricing">Pricing</a>
      <a href="/#who">Who it is for</a>
    </nav>
    <div class="masthead__tools">
      <button id="theme-toggle" class="icon-btn" type="button" aria-label="Switch theme">
        <svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.2v2M12 19.8v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2.2 12h2M19.8 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
        <svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>
      </button>
      <a class="btn btn--quiet masthead__cta" href="/#pricing">See pricing</a>
      <details class="mmenu">
        <summary class="mmenu__trigger" aria-label="Open menu">
          <span class="mmenu__bars" aria-hidden="true"><i></i></span>
        </summary>
        <div class="mmenu__panel">
          <a href="/#cards">The five cards</a>
          <a href="/#how">How setup works</a>
          <a href="/#pricing">Pricing</a>
          <a href="/#faq">Questions</a>
          <a href="/demo">See it work</a>
          <p class="mmenu__note">mark@ownerdeck.com</p>
        </div>
      </details>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="footer">
  <div class="wrap footer__row">
    <span>&copy; 2026 Ownerdeck</span>
    <a href="https://www.instagram.com/ownerdeckcy/" rel="noopener">Instagram</a>
    <a href="mailto:mark@ownerdeck.com">mark@ownerdeck.com</a>
    <span class="footer__spacer"></span>
    <a href="/privacy">Privacy</a>
    <a href="/terms" rel="nofollow">Terms</a>
  </div>
</footer>"""


def head_for(title, desc, canonical, noindex):
    robots = '\n<meta name="robots" content="noindex">' if noindex else ''
    canon  = '\n<link rel="canonical" href="%s">' % canonical if canonical else ''
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%s</title>
<meta name="description" content="%s">
<meta name="viewport" content="width=device-width, initial-scale=1">%s%s
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="favicon.png">
<meta name="theme-color" content="#F7F4EF">
%s
%s
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

%s
""" % (title, desc, canon, robots, THEME_BOOT, FONT_HEAD, HEADER)


TAIL = """
%s

<script src="motion.js?v=20260815c" defer></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
""" % FOOTER


def rebuild(path, title, desc, canonical, eyebrow, noindex=True):
    src = io.open(path, encoding='utf-8').read()
    i, j = src.find('<main>'), src.find('</main>')
    if i < 0 or j < 0:
        sys.exit('%s: no <main> markers' % path)
    inner = src[i + len('<main>'):j]

    # Peel off any wrapper this script added on a previous run. Without this,
    # each rebuild nests another <div id="main"> inside the last one — three
    # runs, three elements sharing an id, and a skip link with no single target.
    #
    # Matching outermost-open to trailing-close does not work: an earlier
    # broken run left wrappers sitting mid-content, so the opens are not
    # necessarily at position zero. Count the opens, delete them all, and drop
    # that many closes off the end — which is where every one of them was
    # appended.
    opens = len(re.findall(r'<div id="main"[^>]*>', inner))
    if opens:
        inner = re.sub(r'<div id="main"[^>]*>\s*', '', inner)
        for _ in range(opens):
            inner = re.sub(r'\s*</div>\s*$', '', inner)

    # Swap the old design-system classes for the brand ones. These match both
    # the pre-rebrand markup and this script's own output, so a second run
    # rebuilds rather than duplicating.
    inner = re.sub(r'<a [^>]*class="back(?:-link)?"[^>]*>.*?</a>\s*', '', inner, flags=re.S)
    inner = re.sub(r'<(div|p) class="eyebrow">.*?</\1>\s*', '', inner, flags=re.S)
    inner = inner.strip()

    # <main> stays bare — see the note at the top of this file. The skip-link
    # target moves onto the wrapper instead.
    body = ('<main>\n'
            '  <div id="main" class="wrap section longform">\n'
            '    <a class="back-link" href="/">Back to ownerdeck.com</a>\n'
            '    <p class="eyebrow">%s</p>\n'
            '%s\n'
            '  </div>\n'
            '</main>' % (eyebrow, inner))

    io.open(path, 'w', encoding='utf-8', newline='').write(
        head_for(title, desc, canonical, noindex) + body + TAIL)
    print('  rebuilt %-14s (%d chars of content preserved)' % (path, len(inner)))


if __name__ == '__main__':
    rebuild('terms.html',
            'Terms of Service — Ownerdeck',
            'Ownerdeck terms of service: what you get on each plan, no VAT, cancel any '
            'time with no notice period on Answer, what you are responsible for, and how '
            'liability is limited.',
            'https://www.ownerdeck.com/terms', 'Legal')

    rebuild('privacy.html',
            'Privacy Policy — Ownerdeck',
            'How Ownerdeck collects, uses and protects data for the website, enquiries '
            'and bookings it runs on your behalf.',
            'https://www.ownerdeck.com/privacy', 'Legal')

    # The single-product price in the terms has to match the page that sells it.
    t = io.open('terms.html', encoding='utf-8').read()
    old = ('<p>The subscription is <strong>&euro;150 per month</strong>. Ownerdeck is not '
           'VAT registered, so no VAT is added and &euro;150 is the full amount you pay.</p>')
    new = ('<p>The subscription depends on the plan you choose: <strong>Answer at '
           '&euro;150 per month</strong>, <strong>Deck at &euro;249 per month</strong>, or '
           '<strong>Full Deck at &euro;299 per month</strong>. Ownerdeck is not VAT '
           'registered, so no VAT is added and the monthly figure is the full amount you '
           'pay. There is no setup fee.</p>')
    if old in t:
        io.open('terms.html', 'w', encoding='utf-8', newline='').write(t.replace(old, new))
        print('  terms.html: pricing clause updated to three plans')
    else:
        print('  WARNING: pricing clause not found in terms.html — check it by hand')
