"""Prepare a supplied photograph for a bento category tile.

Each tile has a fixed pixel size, so the image is centre-cropped to that exact
ratio and written at 2x for retina. Cropping here rather than leaving it to
`object-fit: cover` means we choose what survives, and the file carries no
pixels the layout will throw away.

    python scripts/category-image.py "D:\\path\\photo.png" notebooks
    python scripts/category-image.py "D:\\path\\photo.png" tech --bias 0.56

Tile sizes come from the grid: 4 columns of 345px, 236px rows, 20px gaps.
"""
import argparse, os, sys
from PIL import Image

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'assets', 'img', 'categories')

COL, ROW, GAP = 345, 236, 20

# name -> (columns spanned, rows spanned)
TILES = {
    'eco-sustainable': (2, 2),
    'tech':            (1, 2),
    'notebooks':       (1, 1),
    'home-living':     (1, 1),
    'outdoors':        (2, 1),
    'pens':            (1, 1),
    'office':          (1, 1),
    'giveaways':       (2, 1),
    'themes-events':   (2, 1),
}


def tile_size(name):
    c, r = TILES[name]
    return c * COL + (c - 1) * GAP, r * ROW + (r - 1) * GAP


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('tile', choices=sorted(TILES))
    ap.add_argument('--bias', type=float, default=0.5,
                    help='0 = keep the left/top of the crop, 1 = the right/bottom (default centre)')
    ap.add_argument('--quality', type=int, default=87)
    a = ap.parse_args()

    tw, th = tile_size(a.tile)
    ratio = tw / th
    im = Image.open(a.src).convert('RGB')
    w, h = im.size

    if w / h > ratio:                       # source is wider - slice the width
        nw = int(h * ratio)
        left = int((w - nw) * a.bias)
        im = im.crop((left, 0, left + nw, h))
        kept = f'{nw}/{w}px wide'
    else:                                   # source is taller - slice the height
        nh = int(w / ratio)
        top = int((h - nh) * a.bias)
        im = im.crop((0, top, w, top + nh))
        kept = f'{nh}/{h}px tall'

    im = im.resize((tw * 2, th * 2), Image.LANCZOS)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, a.tile + '.jpg')
    im.save(out, 'JPEG', quality=a.quality, optimize=True, progressive=True)
    print(f'{a.tile}: tile {tw}x{th} -> {im.width}x{im.height} @2x, '
          f'kept {kept}, {os.path.getsize(out)/1024:.0f} KB')
    print(f'  {out}')


if __name__ == '__main__':
    sys.exit(main())
