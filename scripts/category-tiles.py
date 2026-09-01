"""Placeholder category images for the bento tiles that have no lifestyle photo.

Bounce has no shot for Pens, Office, Giveaways or Themes & Events, so each tile is
composed from real normalised product photography on the same ground. They are stand-ins
meant to be swapped for real photography, but they use genuine products rather than a
grey box, so the layout can be judged properly.
"""
import os
from PIL import Image

ROOT = r"d:\work\Bounce-Creative"
SRC = os.path.join(ROOT, 'assets', 'img', 'products')
OUT = os.path.join(ROOT, 'assets', 'img', 'categories')
GROUND = (245, 244, 241)
# canvas per tile, matching the cell it lands in so cover-cropping keeps the products
SIZES = {'pens': (900, 700), 'office': (900, 700),
         'giveaways': (1500, 580), 'themes-events': (1500, 580)}

os.makedirs(OUT, exist_ok=True)

# tile -> product files, largest first; positions are fractions of the canvas
TILES = {
    'pens': ['branded_bamboo_exec_pen.jpg', 'promotional_bamboo_cub_pen.jpg',
             'branded_elis_recycled_pen_black.jpg'],
    'office': ['000001015143-011999999-2d090-ins-pro01-2023-fal_1.jpg',
               'tingo_oversize_solar_powered_calculator_blue.jpg',
               'mini_optical_usb_mouse_blue_chrome.jpg'],
    'giveaways': ['bucket_hats.jpg', 'bee-shaped_seed_bombs_1.jpg',
                  'custom_bespoke_shaped_seed_bombs.jpg'],
    'themes-events': ['branded_full_colour_bucket_hat.jpg', 'milan_glass_cup_340ml_black.jpg',
                      'promotional_seedballs_proudly_sustainable._made_in_britain.jpg'],
}
# scale (of canvas height), x, y as fractions - one layout for tall cells, one for wide
LAYOUT_TALL = [(0.62, 0.02, 0.10), (0.40, 0.56, 0.04), (0.36, 0.52, 0.56)]
LAYOUT_WIDE = [(0.86, 0.02, 0.07), (0.62, 0.40, 0.06), (0.56, 0.66, 0.30)]


def resolve(name):
    p = os.path.join(SRC, name)
    if os.path.exists(p):
        return p
    stem = os.path.splitext(name)[0][:28]
    for f in sorted(os.listdir(SRC)):
        if f.startswith(stem):
            return os.path.join(SRC, f)
    return None


for slug, files in TILES.items():
    W, H = SIZES[slug]
    LAYOUT = LAYOUT_TALL if W < H * 1.6 else LAYOUT_WIDE
    canvas = Image.new('RGB', (W, H), GROUND)
    placed = 0
    for f, (scale, fx, fy) in zip(files, LAYOUT):
        p = resolve(f)
        if not p:
            print(f'  ? missing source for {slug}: {f}')
            continue
        im = Image.open(p).convert('RGB')
        side = int(H * scale * 1.5)
        im = im.resize((side, side), Image.LANCZOS)
        canvas.paste(im, (int(W * fx), int(H * fy)))
        placed += 1
    canvas.save(os.path.join(OUT, f'{slug}.jpg'), 'JPEG', quality=88, optimize=True)
    print(f'  {slug}.jpg  ({placed} products)')
print('done ->', OUT)
