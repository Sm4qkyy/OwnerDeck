# Whole-site pack check: every language must carry the same key set, with no
# blanks and no stray English. Run after adding a language or editing copy.
import io, json, re, sys

LANGS = json.loads('["el","ru","de","pt","he","ar"]')

# Legitimately identical to the English: labels, brand names, abbreviations.
SAME_OK = {
    'k1fe917b0',   # FAQ
    'k727e346d',   # REF
    'k60d4e6b3',   # EXTRAS
    'k3af22b59',   # TOTAL
    'kbe0ba2bb',   # Instagram @ownerdeckcy
    'ka10a9bcd',   # Legal
    'k618b62ac',   # RU · auto-detected  (prefix is a language code)
}

en    = json.load(io.open('_en_source.json', encoding='utf-8'))
packs = {c: json.load(io.open('lang/%s.json' % c, encoding='utf-8')) for c in LANGS}
ref   = set(packs[LANGS[0]])
fail  = []

for c in LANGS:
    d = packs[c]
    if set(d) != ref:
        fail.append('%s: key set differs (+%s / -%s)'
                    % (c, sorted(set(d) - ref)[:5], sorted(ref - set(d))[:5]))
    blank = [k for k, v in d.items() if not str(v).strip()]
    if blank:
        fail.append('%s: %d blank value(s): %s' % (c, len(blank), blank[:5]))
    untouched = [k for k, v in d.items()
                 if k in en and v == en[k] and k not in SAME_OK]
    if untouched:
        fail.append('%s: %d value(s) still identical to the English: %s'
                    % (c, len(untouched), [(k, en[k][:34]) for k in untouched[:4]]))

# The switcher must list exactly the packs that exist on disk.
js = io.open('i18n.js', encoding='utf-8').read()
listed = re.findall(r"code:\s*'(\w+)'", js)
if listed[0] != 'en':
    fail.append('i18n.js: first language should be en, got %r' % listed[0])
if sorted(listed[1:]) != sorted(LANGS):
    fail.append('i18n.js lists %s but packs on disk are %s' % (listed[1:], LANGS))
for m in re.finditer(r"code:\s*'(\w+)'[^}]*dir:\s*'(\w+)'", js):
    code, d = m.groups()
    if d not in ('ltr', 'rtl'):
        fail.append('i18n.js: %s has dir=%r' % (code, d))

print('switcher lists: %s' % ', '.join(listed))
print('pack sizes:     %s' % {c: len(packs[c]) for c in LANGS})

if fail:
    print('\n%d PROBLEM(S):' % len(fail))
    for f in fail:
        print('  ' + f)
    sys.exit(1)
print('\nOK — %d languages, identical key sets, nothing blank or untranslated.' % len(LANGS))
