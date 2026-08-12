# Checks the /demo translation wiring end to end.
#
# The load-bearing check is (3): every key must still be the md5 of the English
# sitting next to it. If someone edits the English and leaves the key, the
# lookup keeps hitting and the page silently serves a translation of a sentence
# that no longer exists.
import hashlib, io, json, re, sys

LANGS = ['el', 'ru', 'de', 'he', 'ar']
fail = []

def key(s):
    return 'k' + hashlib.md5(s.encode('utf-8')).hexdigest()[:8]

html = io.open('demo.html', encoding='utf-8').read()
js   = io.open('demo.js',   encoding='utf-8').read()
packs = {c: json.load(io.open('lang/%s.json' % c, encoding='utf-8')) for c in LANGS}

# ---- (1) collect every (key, english) pair the page actually ships ----
pairs = []

# <tag ... data-i18n="k...">English</tag>   (no nested elements)
for k, txt in re.findall(r'data-i18n="(k[0-9a-f]{8})"\s*>([^<]+)<', html):
    pairs.append((k, txt, 'demo.html'))
for k, txt in re.findall(r'data-i18n="(k[0-9a-f]{8})"\s*>([^<]+)<', js):
    pairs.append((k, txt, 'demo.js (markup)'))
# S("k...", "English")  and  T("k...", "English")
for k, txt in re.findall(r'[ST]\("(k[0-9a-f]{8})",\s*"((?:[^"\\]|\\.)*)"\)', js):
    pairs.append((k, txt.replace('\\"', '"').replace("\\'", "'"), 'demo.js (script)'))

print('found %d keyed strings\n' % len(pairs))

# ---- (2) key must equal md5 of the English beside it ----
bad_hash = [(k, t, w) for k, t, w in pairs if key(t) != k]
if bad_hash:
    for k, t, w in bad_hash:
        fail.append('HASH  %s in %s is really %s -> %r' % (k, w, key(t), t))

# ---- (3) every key present in all five packs ----
for k, t, w in pairs:
    missing = [c for c in LANGS if k not in packs[c]]
    if missing:
        fail.append('MISS  %s (%s) absent from %s -> %r' % (k, w, ','.join(missing), t[:60]))

# ---- (4) HTML data-i18n attributes that wrap child elements would be wiped ----
for m in re.finditer(r'<(\w+)[^>]*data-i18n="k[0-9a-f]{8}"[^>]*>(.*?)</\1>', html, re.S):
    if '<' in m.group(2):
        fail.append('NEST  <%s data-i18n> contains markup that paint() would delete: %r'
                    % (m.group(1), m.group(2)[:70]))

# ---- (5) no key declared in _i18n_demo.py goes unused ----
sys.path.insert(0, '.')
from _i18n_demo import EN
used = set(k for k, _, _ in pairs)
orphans = [(key(s), s) for s in EN if key(s) not in used]
for k, s in orphans:
    fail.append('ORPH  %s declared but never used -> %r' % (k, s[:60]))

# ---- (6) packs still parse and agree on size ----
sizes = {c: len(packs[c]) for c in LANGS}
if len(set(sizes.values())) != 1:
    fail.append('SIZE  packs disagree: %s' % sizes)

print('packs: %s' % sizes)
print('unique keys on the page: %d' % len(used))

if fail:
    print('\n%d PROBLEM(S):' % len(fail))
    for f in fail:
        print('  ' + f)
    sys.exit(1)
print('\nOK — every key hashes to its English, exists in all 5 packs, none orphaned.')
