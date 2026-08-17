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

# Position in the sorted folder -> slug. This is the order the prompts are
# written in IMAGE-PROMPT.md and must stay in step with it.
ORDER = [
    ('car',          'Car and 4x4 rental'),
    ('scooter',      'Scooter and bike hire'),
    ('boat',         'Boat and jetski charter'),
    ('diving',       'Tours, excursions and diving'),
    ('villa-pool',   'Villas and short-term rentals'),
    ('hotel',        'Guesthouses and small hotels'),
    ('estate',       'Estate agencies'),
    ('clinic',       'Private clinics'),
    ('salon',        'Salons and spas'),
    ('restaurant',   'Restaurants and tavernas'),
    ('watersports',  'Watersports rental'),
    ('fitness',      'Fitness and yoga studios'),
    ('photographer', 'Photographers and studios'),
    ('dentist',      'Dentists'),
    ('barber',       'Barbers'),
]

EXTS = ('.png', '.jpg', '.jpeg', '.webp')


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\honey\Pictures\trades'
    if not os.path.isdir(src):
        raise SystemExit('not a folder: %s' % src)

    files = sorted(f for f in os.listdir(src) if f.lower().endswith(EXTS))
    print('  source : %s' % src)
    print('  found  : %d image(s)\n' % len(files))

    if len(files) != len(ORDER):
        print('  Expected %d, found %d. Refusing to guess which is which —' %
              (len(ORDER), len(files)))
        print('  a boat labelled "private clinics" is worse than no image.\n')
        for i, f in enumerate(files, 1):
            print('    %2d  %s' % (i, f))
        print('\n  Expected order:')
        for i, (slug, name) in enumerate(ORDER, 1):
            print('    %2d  %-14s %s' % (i, slug, name))
        sys.exit(1)

    os.makedirs(IMG, exist_ok=True)
    print('  %-3s %-26s %-14s %-13s %s' % ('#', 'FILE', 'SLUG', 'SIZE', 'WEBP'))
    for i, (fname, (slug, label)) in enumerate(zip(files, ORDER), 1):
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

        print('  %-3d %-26s %-14s %-13s %.0f KB'
              % (i, fname[:26], slug, '%dx%d' % im.size, os.path.getsize(webp) / 1024))

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
                '| File | Trade |\n|---|---|\n')
        for slug, label in ORDER:
            f.write('| `img/%s.webp` | %s |\n' % (slug, label))

    print('\n  %d images written, CREDITS.md rewritten.' % len(ORDER))
    print('  Next: python _build_site.py && python _verify.py')


if __name__ == '__main__':
    main()
