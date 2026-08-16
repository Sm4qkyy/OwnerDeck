# Conformance check for the generated site.
#
# Replaces _verify_brand.py, which was written against the terracotta palette
# and the single-page structure. The checks that mattered are carried over:
# colour discipline, no content hidden behind JavaScript, resolvable links and
# assets, one h1, alt text. The new ones are about the things this rebuild can
# get wrong — sub-pages that do not resolve under cleanUrls, translation keys
# that collide, and headings that skip a level.
#
# Run:  python _verify.py
import fnmatch
import io
import os
import re
import sys
import json
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index', 'what-we-build', 'how-it-works', 'pricing', 'who-its-for',
         'questions', 'demo', 'legal', 'privacy', 'cookies', 'terms']

# Served by the platform at request time, not present in the repo. Checking
# these as files is the same false positive the previous verifier hit.
RUNTIME_PREFIXES = ('/_vercel/',)

fails, warns = [], []


def fail(page, msg):
    fails.append((page, msg))


def warn(page, msg):
    warns.append((page, msg))


def read(name):
    with io.open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


# --------------------------------------------------------------- contrast
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_palette(css):
    """Colour lives on the palette blocks and nowhere else, and the pairs that
    carry text clear AA in both themes."""
    stripped = re.sub(r'/\*.*?\*/', '', css, flags=re.S)

    # Only blocks that actually define --paper are palettes. Matching every
    # :root rule swept up `:root.is-leaving main`, which has no colours in it
    # and made the dark palette look empty.
    blocks = [b for b in re.findall(r':root[^{]*\{(.*?)\}', stripped, re.S)
              if '--paper:' in b]
    if len(blocks) < 3:
        fail('od.css', 'expected light, media-dark and attribute-dark palette blocks, found %d'
             % len(blocks))

    outside = re.sub(r':root[^{]*\{.*?\}', '', stripped, flags=re.S)
    stray = re.findall(r'#[0-9a-fA-F]{3,8}\b', outside)
    if stray:
        fail('od.css', 'hex outside the palette blocks: %s' % ', '.join(sorted(set(stray))[:8]))

    def tokens(block):
        return dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})', block))

    light = tokens(blocks[0])
    dark = tokens(blocks[-1])

    for name, pal in (('light', light), ('dark', dark)):
        if not pal.get('--paper'):
            fail('od.css', '%s palette has no --paper' % name)
            continue
        bg = pal['--paper']
        for tok, need, what in (('--ink', 4.5, 'body text'),
                                ('--muted', 4.5, 'secondary text'),
                                ('--live', 3.0, 'live indicator')):
            if tok not in pal:
                fail('od.css', '%s palette missing %s' % (name, tok))
                continue
            r = ratio(pal[tok], bg)
            if r < need:
                fail('od.css', '%s %s on --paper is %.2f:1, needs %.1f (%s)'
                     % (name, tok, r, need, what))
        # The label on a filled primary button is --invert on --ink.
        if '--invert' in pal and '--ink' in pal:
            r = ratio(pal['--invert'], pal['--ink'])
            if r < 4.5:
                fail('od.css', '%s button label --invert on --ink is %.2f:1' % (name, r))

    # Anything hiding content must be scoped to .js, or a blocked script
    # leaves a blank page.
    # Selectors that may sit at opacity 0 without a .js guard, because what
    # they hide is not content. Keep this list short and justified.
    DECORATIVE = (
        '.mmenu__bars',   # the middle hamburger bar, which becomes an X
    )
    for m in re.finditer(r'([^{}]+)\{([^{}]*opacity\s*:\s*0\s*;[^{}]*)\}', stripped):
        sel = m.group(1).strip().splitlines()[-1].strip()
        if 'is-leaving' in sel or sel in ('from', 'to'):
            continue
        if any(d in sel for d in DECORATIVE):
            continue
        if '.js ' not in sel:
            fail('od.css', 'rule sets opacity:0 without a .js guard: %s' % sel[:70])


# ------------------------------------------------------------------ pages
def resolvable(href):
    """Does this path exist, given vercel.json cleanUrls?"""
    p = href.split('#')[0].split('?')[0]
    if not p or p == '/':
        return os.path.exists(os.path.join(HERE, 'index.html'))
    p = p.lstrip('/')
    for cand in (p, p + '.html', os.path.join(p, 'index.html')):
        if os.path.exists(os.path.join(HERE, cand)):
            return True
    return False


def check_page(slug, html):
    page = slug + '.html'

    # Exactly one h1.
    h1 = re.findall(r'<h1[\s>]', html)
    if len(h1) != 1:
        fail(page, 'expected 1 <h1>, found %d' % len(h1))

    # Heading levels must not skip.
    levels = [int(m) for m in re.findall(r'<h([1-4])[\s>]', html)]
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            fail(page, 'heading jumps from h%d to h%d' % (prev, lv))
            break
        prev = lv

    # Every image needs a resolvable src and real alt text.
    for m in re.finditer(r'<img\b([^>]*)>', html):
        attrs = m.group(1)
        src = re.search(r'src="([^"]+)"', attrs)
        alt = re.search(r'alt="([^"]*)"', attrs)
        if not src:
            fail(page, 'img with no src')
            continue
        if not resolvable(src.group(1)):
            fail(page, 'img src does not resolve: %s' % src.group(1))
        if alt is None:
            fail(page, 'img with no alt: %s' % src.group(1))
        elif not alt.group(1).strip():
            warn(page, 'img with empty alt (fine only if decorative): %s' % src.group(1))

    # Internal links must resolve.
    for m in re.finditer(r'<a\b[^>]*href="([^"]+)"', html):
        href = m.group(1)
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            continue
        if not href.startswith('/'):
            fail(page, 'relative link, ambiguous on sub-pages: %s' % href)
            continue
        if not resolvable(href):
            fail(page, 'link does not resolve: %s' % href)

    # Stylesheets and scripts.
    for m in re.finditer(r'(?:href|src)="(/[^"]+\.(?:css|js))(?:\?[^"]*)?"', html):
        path = m.group(1)
        if path.startswith(RUNTIME_PREFIXES):
            continue
        if not os.path.exists(os.path.join(HERE, path.lstrip('/'))):
            fail(page, 'asset missing: %s' % path)

    # The generator should have consumed every data-t.
    if re.search(r'\sdata-t[\s>=]', html.replace('data-theme', '')):
        fail(page, 'unprocessed data-t left in the output')

    # The theme bootstrap has to be inline in <head>, ahead of first paint.
    head = html.split('</head>')[0]
    if "classList.add('js')" not in head:
        fail(page, 'no inline .js bootstrap in <head> — reveals would never run')
    if 'od_theme' not in head:
        fail(page, 'theme is not restored before first paint')

    # Skip link, and it must point at something.
    if 'class="skip-link"' not in html:
        fail(page, 'no skip link')
    elif 'id="main"' not in html:
        fail(page, 'skip link has no target')

    # Copy rules carried over from the brand brief.
    for banned in ['cutting-edge', 'game-changing', 'revolutionise', 'revolutionize',
                   'synergy', 'leverage our', 'best-in-class', 'seamlessly',
                   'unlock the power', 'supercharge']:
        if banned in html.lower():
            fail(page, 'banned phrase: %s' % banned)
    body = html.split('<body>')[-1]
    if re.search(r'[\U0001F300-\U0001FAFF✀-➿]', body):
        fail(page, 'emoji in the markup')

    return len(re.findall(r'data-i18n="', html))


def check_deployable():
    """Does any served page ask for a file that .vercelignore keeps out of the
    deployment?

    This is the check that was missing. The four SEO guides linked brand.css
    for weeks while .vercelignore excluded it, so in production the stylesheet
    404'd and the pages rendered as raw text — and nothing caught it, because
    the old check only looked at the pages the generator produces and only
    asked whether files existed *locally*. They did. They just never shipped.
    """
    ignore_path = os.path.join(HERE, '.vercelignore')
    if not os.path.exists(ignore_path):
        return
    patterns = []
    for line in read('.vercelignore').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            patterns.append(line.rstrip('/'))

    def excluded(rel):
        rel = rel.lstrip('/')
        for pat in patterns:
            if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(os.path.basename(rel), pat):
                return pat
            # Directory patterns exclude everything beneath them.
            if rel.startswith(pat + '/'):
                return pat
        return None

    for name in sorted(os.listdir(HERE)):
        if not name.endswith('.html') or name.startswith('_'):
            continue
        html = read(name)
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            ref = m.group(1).split('?')[0].split('#')[0]
            if not ref or ref.startswith(('http', 'mailto:', 'tel:', 'data:', '//')):
                continue
            if ref.startswith(RUNTIME_PREFIXES):
                continue
            if not os.path.splitext(ref)[1]:
                continue          # a clean URL, not a file
            pat = excluded(ref)
            if pat:
                fail(name, 'references %s, which .vercelignore excludes (%s)' % (ref, pat))


def check_i18n():
    """Keys are a hash of the English, so two different sentences must never
    share one, and every key in the source map must be reachable."""
    src = json.loads(read('_en_source.json'))
    seen = defaultdict(set)
    for slug in PAGES:
        html = read('index.html' if slug == 'index' else slug + '.html')
        for m in re.finditer(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', html):
            seen[m.group(1)].add(' '.join(m.group(2).split()))

    for key, texts in seen.items():
        if len(texts) > 1:
            fail('i18n', 'key %s used for %d different strings: %r' % (key, len(texts), sorted(texts)[:2]))
        if key not in src:
            fail('i18n', 'key %s is in the markup but not in _en_source.json' % key)

    for key in src:
        if key not in seen:
            warn('i18n', 'key %s is in the source map but no longer in any page' % key)

    # Every pack must be valid JSON keyed the same way.
    langs = []
    for name in sorted(os.listdir(os.path.join(HERE, 'lang'))):
        if not name.endswith('.json'):
            continue
        code = name[:-5]
        try:
            pack = json.loads(read(os.path.join('lang', name)))
        except Exception as e:
            fail('lang/' + name, 'invalid JSON: %s' % e)
            continue
        hit = sum(1 for k in seen if k in pack)
        langs.append((code, hit, len(seen)))
    return langs


def main():
    check_palette(read('od.css'))

    total_keys = 0
    for slug in PAGES:
        name = 'index.html' if slug == 'index' else slug + '.html'
        if not os.path.exists(os.path.join(HERE, name)):
            fail(name, 'page missing — run _build_site.py')
            continue
        total_keys += check_page(slug, read(name))

    check_deployable()
    langs = check_i18n()

    print('=' * 74)
    print('  %d pages · %d translated nodes' % (len(PAGES), total_keys))
    print('=' * 74)
    print('\n  Translation coverage')
    for code, hit, tot in langs:
        bar = '#' * int(round(hit / max(tot, 1) * 30))
        print('    %-3s %4d / %-4d %5.0f%%  %s' % (code, hit, tot, hit / max(tot, 1) * 100, bar))

    if warns:
        print('\n  Warnings (%d)' % len(warns))
        for page, msg in warns[:12]:
            print('    %-18s %s' % (page, msg))
        if len(warns) > 12:
            print('    ... and %d more' % (len(warns) - 12))

    print()
    if fails:
        print('  FAILED (%d)' % len(fails))
        for page, msg in fails:
            print('    %-18s %s' % (page, msg))
        sys.exit(1)
    print('  All checks passed.')


if __name__ == '__main__':
    main()
