# Bring the generated trade images into the site.
#
# Replaces _images.py, which pulled CC0 stock from Openverse. These are
# commissioned images that Ownerdeck owns, so there is nothing to fetch and
# nothing to attribute — the source of truth is now a folder on disk.
#
# Reads a folder, sorts by filename, and maps position to slug in the order the
# prompts were written. It refuses to run if the count is wrong rather than
# quietly mis-assigning, because a boat labelled "private clinics" is worse
# than no image at all.
#
#   python _ingest_trades.py "C:\Users\honey\Pictures\trades"
#
# Re-runnable. Overwrites whatever is in img/ for the slugs it handles.
import io
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')
MAX_EDGE = 1600

# Filename -> slug, established by opening each image and looking at it.
#
# This was position-in-sorted-order until the files arrived named with UUIDs,
# which sort arbitrarily. Mapping by position would have put the barber's chair
# under "car and 4x4 rental". An explicit map is the only safe way when the
# filenames carry no meaning.
MAP = {
    '00ca81a7-50a2-4663-8337-9da70bf70030.png': ('barber',       'Barbers'),
    '12576359-a94a-40cb-be17-1549d22b9ead.png': ('watersports',  'Watersports rental'),
    '1cb64074-a1da-4fa5-add5-35cfb2d2c3a8.png': ('estate',       'Estate agencies'),
    '3727c1b3-f964-424f-a77b-66a86d4900bb.png': ('salon',        'Salons and spas'),
    '4aba5925-1a01-4e18-a1af-7dbf364c9b76.png': ('photographer', 'Photographers and studios'),
    '5121766a-fb5b-4e52-8686-d657e6f43597.png': ('boat',         'Boat and jetski charter'),
    '91c43e29-289c-49e0-b2ae-0544d632a36c.png': ('scooter',      'Scooter and bike hire'),
    'c81e90bd-4896-45b3-86b5-d4f10d177ffc.png': ('fitness',      'Fitness and yoga studios'),
    'd4ed197e-9942-465d-a995-a36dc1c50b88.png': ('car',          'Car and 4x4 rental'),
    'd5585879-e67c-4b44-9de1-cf0e7de90fd4.png': ('dentist',      'Dentists'),
    'e111c97a-8bcb-4cab-b7a8-481cbc4b5934.png': ('clinic',       'Private clinics'),
    'f8bcad15-7260-49f7-b5d3-280e8bb4bb87.png': ('restaurant',   'Restaurants and tavernas'),
    '28575c78-ff98-415f-aa6b-056a57b1e88c.png': ('hotel',        'Guesthouses and small hotels'),
    'b255e6c5-a8ea-407c-9207-6a98764523e6.png': ('villa-pool',   'Villas and short-term rentals'),
    'df596832-7598-407b-80f2-5a75f2d76e9f.png': ('diving',       'Tours, excursions and diving'),
}

# Every trade now has commissioned imagery. Kept as an empty list so the
# reporting below still works if one is ever pulled.
MISSING = []

EXTS = ('.png', '.jpg', '.jpeg', '.webp')


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\honey\Pictures\trades'
    if not os.path.isdir(src):
        raise SystemExit('not a folder: %s' % src)

    files = sorted(f for f in os.listdir(src) if f.lower().endswith(EXTS))
    print('  source : %s' % src)
    print('  found  : %d image(s), %d in the map\n' % (len(files), len(MAP)))

    unknown = [f for f in files if f not in MAP]
    if unknown:
        print('  Not in the map. Open each one, identify the trade, and add it')
        print('  before running — guessing is how a barber chair ends up under')
        print('  "car and 4x4 rental".\n')
        for f in unknown:
            print('    %s' % f)
        sys.exit(1)

    os.makedirs(IMG, exist_ok=True)
    print('  %-3s %-14s %-28s %-13s %s' % ('#', 'SLUG', 'TRADE', 'SIZE', 'WEBP'))
    for i, fname in enumerate(files, 1):
        slug, label = MAP[fname]
        im = Image.open(os.path.join(src, fname))
        if im.mode in ('P', 'RGBA', 'LA'):
            im = im.convert('RGB')
        elif im.mode != 'RGB':
            im = im.convert('RGB')

        w, h = im.size
        if max(w, h) > MAX_EDGE:
            scale = MAX_EDGE / float(max(w, h))
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)

        webp = os.path.join(IMG, slug + '.webp')
        jpg = os.path.join(IMG, slug + '.jpg')
        im.save(webp, 'WEBP', quality=82, method=6)
        im.save(jpg, 'JPEG', quality=84, optimize=True, progressive=True)

        print('  %-3d %-14s %-28s %-13s %.0f KB'
              % (i, slug, label, '%dx%d' % im.size, os.path.getsize(webp) / 1024))

    # These are owned images, so the credits file records provenance rather
    # than licence obligations. Saying "CC0 from Openverse" here would now be
    # false for every row.
    with io.open(os.path.join(IMG, 'CREDITS.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Image credits\n\n'
                'Every image in this folder was generated to brief for Ownerdeck and is\n'
                'owned by Ownerdeck. There is no third-party licence to honour and no\n'
                'attribution requirement.\n\n'
                'They replaced a set of CC0 / Public Domain Mark photographs sourced\n'
                'through Openverse, which were correctly licensed but had been chosen for\n'
                'subject alone — nine different styles that read as unrelated stock on one\n'
                'page.\n\n'
                'The brief they were generated from is `IMAGE-PROMPT.md`. Regenerate from\n'
                'source files with `python _ingest_trades.py <folder>`.\n\n'
                '| File | Trade | Provenance |\n|---|---|---|\n')
        for _fn, (slug, label) in sorted(MAP.items(), key=lambda kv: kv[1][0]):
            f.write('| `img/%s.webp` | %s | Generated to brief, owned |\n' % (slug, label))
        for slug, label in MISSING:
            f.write('| `img/%s.webp` | %s | **Retired CC0 stock, awaiting replacement** |\n'
                    % (slug, label))

    print('\n  %d images written, CREDITS.md rewritten.' % len(MAP))
    print('  Still on retired stock: %s' % ', '.join(s for s, _ in MISSING))
    print('  Next: python _build_site.py && python _verify.py')


if __name__ == '__main__':
    main()
