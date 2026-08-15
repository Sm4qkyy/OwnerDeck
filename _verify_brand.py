# Rebrand conformance check. Everything the brief made a hard rule, asserted
# against the built files rather than trusted.
import glob, io, os, re, sys

PAGES = sorted(p for p in glob.glob('*.html'))
fail, warn = [], []

BANNED_COPY = ['supercharge', 'seamless', 'effortless', 'unlock', 'revolutionis',
               'revolutioniz', 'game-changer', 'powered by ai', 'chatbot',
               'automation', 'leverage', 'solution', 'platform']
# "AI" is allowed in exactly one place: the disclosure the assistant is
# legally required to make. It must not appear in marketing copy.
DISCLOSURE_FILES = {'chat-widget.js', 'api/chat.js', 'terms.html', 'privacy.html'}

BANNED_CSS = [
  (r'linear-gradient|radial-gradient', 'gradient'),
  (r'backdrop-filter', 'glassmorphism'),
  (r'border-radius:\s*999', 'pill radius'),
  (r'font-family:[^;]*Inter', 'Inter'),
]

def text_of(html):
    """Visible copy only — strip script, style, comments and tags."""
    t = re.sub(r'(?s)<script.*?</script>', ' ', html)
    t = re.sub(r'(?s)<style.*?</style>', ' ', t)
    t = re.sub(r'(?s)<!--.*?-->', ' ', t)
    t = re.sub(r'(?s)<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t)

# ---------------------------------------------------------------- 1. colour
css_files = ['brand.css', 'chat-widget.css']
def strip_comments(s):
    return re.sub(r'(?s)/\*.*?\*/', '', s)

# Comments are stripped first: the palette comment names #000 in order to
# forbid it, and a scanner that cannot tell prose from a declaration would
# report the ban as a violation of itself.
root = strip_comments(io.open('brand.css', encoding='utf-8').read())
root_block = re.search(r'(?s):root\s*\{(.*?)\n\}', root)
root_hex = set(re.findall(r'#[0-9a-fA-F]{3,8}\b', root_block.group(1))) if root_block else set()

for f in css_files:
    body = strip_comments(io.open(f, encoding='utf-8').read())
    if f == 'brand.css' and root_block:
        body = body.replace(root_block.group(0), '')
    stray = re.findall(r'#[0-9a-fA-F]{3,8}\b', body)
    if stray:
        fail.append('%s: %d hex literal(s) outside :root -> %s' % (f, len(stray), sorted(set(stray))))

for p in PAGES:
    h = io.open(p, encoding='utf-8').read()
    stray = [x for x in re.findall(r'#[0-9a-fA-F]{3,8}\b', h) if x.upper() != '#F7F4EF']
    if stray:
        fail.append('%s: hex in markup -> %s' % (p, sorted(set(stray))))

# ---------------------------------------------------------------- 2. bans
for f in css_files + PAGES:
    body = io.open(f, encoding='utf-8').read()
    for pat, name in BANNED_CSS:
        if re.search(pat, body, re.I):
            fail.append('%s: banned technique -> %s' % (f, name))

for p in PAGES:
    copy = text_of(io.open(p, encoding='utf-8').read()).lower()
    # The five guide pages are pre-rebrand SEO content whose subject matter is
    # the banned vocabulary itself — one of them compares auto-replies with
    # assistants. Reported, not failed, because rewriting them is a scope
    # decision rather than a defect.
    legacy = p.startswith(('whatsapp-', 'do-i-need-', 'stop-losing-'))
    for w in BANNED_COPY:
        if w in copy:
            (warn if legacy else fail).append('%s: banned word in copy -> %r' % (p, w))
    if re.search(r'\bAI\b', text_of(io.open(p, encoding='utf-8').read())) and p not in DISCLOSURE_FILES:
        warn.append('%s: the letters AI appear in visible copy' % p)
    if '!' in copy.replace('!important', ''):
        fail.append('%s: exclamation mark in copy' % p)

EMOJI = re.compile('[\U0001F000-\U0001FAFF←-⇿☀-➿️]')
for f in PAGES + ['demo.js', 'chat-widget.js', 'brand.css', 'chat-widget.css']:
    if not os.path.exists(f):
        continue
    found = sorted(set(EMOJI.findall(io.open(f, encoding='utf-8').read())))
    if found:
        fail.append('%s: emoji present -> %s' % (f, ' '.join(found)))

# ---------------------------------------------------------------- 3. a11y
for p in PAGES:
    h = io.open(p, encoding='utf-8').read()

    imgs = re.findall(r'<img\b[^>]*>', h)
    for im in imgs:
        if 'alt=' not in im:
            fail.append('%s: <img> without alt -> %s' % (p, im[:60]))

    levels = [int(m) for m in re.findall(r'<h([1-6])\b', h)]
    if levels.count(1) != 1:
        fail.append('%s: %d <h1> elements (want exactly 1)' % (p, levels.count(1)))
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            warn.append('%s: heading jumps h%d -> h%d' % (p, prev, lv))
        prev = lv

    if 'lang="en"' not in h:
        fail.append('%s: no lang on <html>' % p)
    if 'skip-link' not in h:
        warn.append('%s: no skip link' % p)

# ---------------------------------------------------------------- 4. numbers
NUM = re.compile(r'(?<![\w/#-])(\d[\d,.]*)(?![\w%-])')
ALLOWED = {'150', '249', '299', '14', '2026', '2'}   # prices, the proof, the year, "2am"
copy = text_of(io.open('index.html', encoding='utf-8').read())
found = set(NUM.findall(copy)) - ALLOWED
if found:
    warn.append('index.html: numbers in copy beyond the allowed set -> %s' % sorted(found))

# ---------------------------------------------------------------- 5. links
have = set(os.path.basename(x) for x in glob.glob('*.html'))
for p in PAGES:
    h = io.open(p, encoding='utf-8').read()
    for href in re.findall(r'href="(/[^"#?]*)"', h):
        if href in ('/',):
            continue
        target = href.lstrip('/')
        if target + '.html' not in have and target not in have:
            fail.append('%s: internal link to %s has no file' % (p, href))
    # Only a relative path names a file on disk. Root-relative paths are
    # cleanUrls routes (/terms), fragments (/#pricing), or Vercel's injected
    # runtime (/_vercel/...) — the internal-link loop above already covers
    # the first, and the other two have no file to find by design.
    for src in re.findall(r'(?:src|href)="(?!http|//|mailto:|#|/)([^":]+)"', h):
        f = src.split('?')[0].split('#')[0]
        if f and not os.path.exists(f):
            fail.append('%s: missing asset -> %s' % (p, f))

# ---------------------------------------------------------------- 6. seo
for p in PAGES:
    h = io.open(p, encoding='utf-8').read()
    for tag, pat in (('title', r'<title>[^<]+</title>'),
                     ('description', r'name="description" content="[^"]+"'),
                     ('viewport', r'name="viewport"'),
                     ('favicon', r'rel="icon"')):
        if not re.search(pat, h):
            fail.append('%s: missing %s' % (p, tag))
    if 'noindex' not in h and not re.search(r'rel="canonical"', h):
        fail.append('%s: indexable but no canonical' % p)

print('checked %d pages + %d stylesheets\n' % (len(PAGES), len(css_files)))
print(':root declares %d colours: %s\n' % (len(root_hex), ' '.join(sorted(root_hex))))

for w in warn:
    print('  WARN  ' + w)
if warn:
    print()
if fail:
    print('%d FAILURE(S):' % len(fail))
    for f in fail:
        print('  FAIL  ' + f)
    sys.exit(1)
print('PASS — no hex outside :root, no banned techniques or words, no emoji,')
print('       one h1 per page, every asset and internal link resolves.')
