"""Normalise supplier product photography.

The images arrive framed inconsistently: white borders from 0 to 145px, some on a
grey studio card, a couple on grey throughout. Left as-is they render as nested
rectangles inside the product tile. This peels every uniform border away, then
recomposites each product onto one shared ground at one padding, so the whole grid
reads as a single set.
"""
import io, os, re, urllib.request
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = r"d:\work\Bounce-Creative"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgcache")
OUT = os.path.join(ROOT, "assets", "img", "products")
GROUND = (245, 244, 241)          # --band; matches the tile the product sits on
SIZE, PAD, MAX_UP = 560, 0.05, 1.7

os.makedirs(OUT, exist_ok=True)


def fetch(url):
    key = os.path.join(CACHE, re.sub(r'[^A-Za-z0-9._-]', '_', url)[-110:])
    if not os.path.exists(key):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        open(key, 'wb').write(urllib.request.urlopen(req, timeout=60).read())
    return key


def peel(im, tol=10, rounds=4):
    """Strip uniform borders repeatedly - white frame first, then any studio card."""
    for _ in range(rounds):
        w, h = im.size
        corner = im.getpixel((1, 1))
        diff = ImageChops.difference(im, Image.new('RGB', im.size, corner)).convert('L')
        bbox = diff.point(lambda v: 255 if v > tol else 0).getbbox()
        if not bbox:
            break
        if bbox == (0, 0, w, h):
            break
        # ignore a "trim" that would eat almost everything - that means the product
        # itself matched the corner colour
        if (bbox[2] - bbox[0]) < w * 0.25 or (bbox[3] - bbox[1]) < h * 0.25:
            break
        im = im.crop(bbox)
    return im


def whiten(im, target=252):
    """A few shots sit on a flat grey studio ground. Lift their white point so
    every product ends up on the same white as the rest."""
    c = im.getpixel((1, 1))
    if min(c) >= 248:
        return im
    gain = [min(2.0, target / max(v, 1)) for v in c]
    return im.point([min(255, int(i * gain[ch])) for ch in range(3) for i in range(256)])


SENTINEL = (255, 0, 255)


def key_out(im, tol=20):
    """Remove the photo's own background so the product sits straight on the tile.

    Flood-fills inward from the border rather than thresholding globally, so white
    highlights *inside* a product survive while the connected backdrop goes. The
    resulting alpha is feathered slightly to avoid a cut-out edge.
    """
    work = im.copy()
    d = ImageDraw.floodfill
    w, h = work.size
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    for sd in seeds:
        if work.getpixel(sd) != SENTINEL:
            d(work, sd, SENTINEL, thresh=tol)

    # Background enclosed by the product - the gap between a tote's handles - is not
    # reachable from the border, so seed a coarse grid as well. The seed must be very
    # close to pure white, which keeps cream products and small specular highlights.
    probe = work.load()
    for y in range(0, h, 8):
        for x in range(0, w, 8):
            c = probe[x, y]
            if c != SENTINEL and min(c) >= 246:
                d(work, (x, y), SENTINEL, thresh=tol)
    px = work.load()
    alpha = Image.new('L', (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == SENTINEL:
                ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
    out = im.convert('RGBA')
    out.putalpha(alpha)
    return out


def normalise(src):
    im = Image.open(src).convert('RGB')
    im = peel(im)
    im = whiten(im)
    im = key_out(im)
    # thumbnail() only ever shrinks, so a small trimmed product would stay small.
    # Scale to fit the box, but cap the upscale so nothing turns to mush.
    box = int(SIZE * (1 - 2 * PAD))
    im = im.crop(im.getbbox() or (0, 0, im.width, im.height))
    k = min(box / im.width, box / im.height, MAX_UP)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    canvas = Image.new('RGB', (SIZE, SIZE), GROUND)
    canvas.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2), im)
    return canvas


mapfile = os.path.join(CACHE, 'prodmap.txt')
if os.path.exists(mapfile):
    # the page now points at local copies, so re-derive the source list from the map
    urls = [l.split('	')[0] for l in io.open(mapfile, encoding='utf-8').read().splitlines() if l.strip()]
else:
    html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    urls = sorted(set(re.findall(r'src="(https://[^"]*catalog/product[^"]+)"', html)))
mapping = {}
for u in urls:
    name = re.sub(r'[^A-Za-z0-9._-]', '-', u.split('/')[-1])
    name = os.path.splitext(name)[0][:60] + '.jpg'
    normalise(fetch(u)).save(os.path.join(OUT, name), 'JPEG', quality=86, optimize=True)
    mapping[u] = 'assets/img/products/' + name
    print(f'  {name}')

io.open(os.path.join(CACHE, 'prodmap.txt'), 'w', encoding='utf-8').write(
    '\n'.join(f'{k}\t{v}' for k, v in mapping.items()))
print(f'\n{len(mapping)} images normalised to {SIZE}x{SIZE} on {GROUND}')
