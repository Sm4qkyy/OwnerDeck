# Rebuilds key -> English from the markup, so a new language pack can be
# written against the actual source text rather than against another
# translation. Writes _en_source.json.
import io, json, re

FILES = ['index.html', 'demo.html', 'demo.js', 'chat-widget.js',
         'terms.html', 'privacy.html']

ATTR = re.compile(r'data-i18n="(k[0-9a-f]{8})"\s*>([^<]+)<')
# The JS literals are single-quoted and full of apostrophes ("I'm", "Friday's"),
# so the closing quote has to be matched by kind, not by "any quote".
CALL = re.compile(r'[ST]\(\s*(["\'])(k[0-9a-f]{8})\1\s*,\s*(["\'])((?:[^\\]|\\.)*?)\3')

def collect():
    src = {}
    for f in FILES:
        try:
            t = io.open(f, encoding='utf-8').read()
        except FileNotFoundError:
            continue
        for k, txt in ATTR.findall(t):
            src.setdefault(k, txt.strip())
        for _q1, k, _q2, txt in CALL.findall(t):
            src.setdefault(k, txt.replace("\\'", "'").replace('\\"', '"'))
    return src

if __name__ == '__main__':
    el = json.load(io.open('lang/el.json', encoding='utf-8'))
    src = collect()
    missing = [k for k in el if k not in src]
    print('keys in el.json: %d | english recovered: %d | unmatched: %d'
          % (len(el), len(src), len(missing)))
    if missing:
        print('no english found for:')
        for k in missing:
            print('   %s   el=%r' % (k, el[k][:60]))
    out = {k: src[k] for k in el if k in src}
    io.open('_en_source.json', 'w', encoding='utf-8').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('wrote _en_source.json (%d entries)' % len(out))
