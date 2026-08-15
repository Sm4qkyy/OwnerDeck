# Re-chassis the long-form pages onto brand.css.
#
# terms.html is not just a page: _build_guides.py and _build_stats.py read
# their head/header/footer out of it by slicing on the literal strings
# "<main>" and "</main>". So the <main> tag here stays bare and unattributed —
# put a class on it and six other pages stop building.
import io, re, sys

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
    <a class="btn btn--quiet masthead__cta" href="/#pricing">See pricing</a>
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
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

%s
""" % (title, desc, canon, robots, FONT_HEAD, HEADER)


TAIL = """
%s

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

    # Swap the old design-system classes for the brand ones.
    inner = re.sub(r'<a href="/" class="back">.*?</a>\s*', '', inner, flags=re.S)
    inner = re.sub(r'<div class="eyebrow">.*?</div>\s*', '', inner, flags=re.S)
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
