# -*- coding: utf-8 -*-
"""Finding 04: the photos were delivered at roughly eight times the width they
display, and there was no srcset, so every visitor downloaded the largest
version of all six homepage tiles regardless of screen.

    file      1448 x 1086       transferred
    rendered   177 x  177       strip tile, 1x
               371 x  278       trade tile, 1x
    six images 572,998 bytes  ·  whole page 735,142 bytes

Measured, not assumed: the strip needs 354px at 2x and the trade grid 742px,
so 400w and 800w cover both with headroom. Each source is rewritten at 800px
on the long edge — keeping the original filename valid everywhere it is
referenced — and a 400w companion is written beside it.

Re-runnable: it skips anything already at or below the target, so running it
twice does not degrade the images.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')
WIDE, NARROW = 800, 400
QUALITY = 82

try:
    from PIL import Image
except ImportError:
    sys.exit('  PIL is required: pip install pillow')


def scaled(im, target):
    if im.width <= target:
        return im.copy()
    h = round(im.height * target / im.width)
    return im.resize((target, h), Image.LANCZOS)


def main():
    before = after = 0
    rows = []
    for name in sorted(os.listdir(IMG)):
        if not name.endswith('.webp') or name.endswith('-400.webp'):
            continue
        path = os.path.join(IMG, name)
        slug = name[:-5]
        was = os.path.getsize(path)
        before += was

        with Image.open(path) as im:
            im.load()
            src_w = im.width
            big = scaled(im, WIDE)
            small = scaled(im, NARROW)

        big.save(path, 'WEBP', quality=QUALITY, method=6)
        narrow_path = os.path.join(IMG, slug + '-400.webp')
        small.save(narrow_path, 'WEBP', quality=QUALITY, method=6)

        now = os.path.getsize(path) + os.path.getsize(narrow_path)
        after += now
        rows.append((name, src_w, big.width, was, now))

    for name, sw, bw, was, now in rows:
        print('    %-22s %5d -> %3dpx   %7d -> %7d' % (name, sw, bw, was, now))
    print('    %-22s %19s %7d -> %7d  (%.0f%% smaller)'
          % ('total (both sizes)', '', before, after, (1 - after / before) * 100))


if __name__ == '__main__':
    main()
