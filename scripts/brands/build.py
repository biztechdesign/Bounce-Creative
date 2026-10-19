#!/usr/bin/env python3
"""Generate the Brands landing page.

The second instance of the category landing template (the bags page is the
first). Each landing page is one config dict: its own title, meta, URL and
copy, so none of them duplicates the list category.

    python scripts/brands/build.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
FOOTER = re.sub(r'<script src="assets/js/pdp-v4\.js\?v=\d+"></script>',
                '<script src="assets/js/category-v4.js?v=1"></script>\n<script src="assets/js/deals-v4.js?v=2"></script>',
                (PDP / "_footer.html").read_text(encoding="utf-8")).replace('<script src="assets/js/quote-artwork-v4.js?v=1"></script>\n', '')


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


BRANDS = {
    "file": "category-brands-v4.html",
    "title": "Branded Merchandise by Brand — Bodum, CamelBak, Sharpie, Vinga | Bounce Creative Designs",
    "meta": ("Promotional products from the brands your team already knows: Bodum, CamelBak, Sharpie, "
             "Waterman, Mepal, Vinga, IQONIQ and more, printed in the UK with instant quotes."),
    "crumb": "Brands",
    "eyebrow": "Shop by brand",
    "h1": ("Brands they know,", "printed by us."),
    "lede": ("Retail brands your customers already own, branded with your logo. The same quality they'd buy "
             "for themselves - which is why these are the gifts that get kept."),
    "hero_img": "assets/img/categories/tech.png",

    # Every brand we stock, with its logo. Counts are the live catalogue's.
    "brands": [
        ("Bodum", "Bodum.png", 24), ("CamelBak", "Camelbak.png", 18), ("HidrateSpark", "HidrateSpark.png", 6),
        ("IQONIQ", "iqoniq.png", 62), ("Karst", "KARST.png", 15), ("Mepal", "Mepal.png", 21),
        ("Sharpie", "Sharpie.png", 12), ("Skross", "Skross.png", 9), ("Ukiyo", "UKIYO.png", 28),
        ("Urban Vitamin", "Urban-Vitamin.png", 17), ("Vinga", "Vinga.png", 54), ("Waterman", "Waterman.png", 11),
    ],

    # Three brand stories with photography.
    "featured": [
        ("IQONIQ", "Recycled apparel that looks like retail", "assets/img/news/parka.jpg",
         "Models wearing IQONIQ Thelon recycled parka jackets", "iqoniq.png"),
        ("LARQ", "Self-cleaning bottles with your logo", "assets/img/news/larq.jpg",
         "A woman drinking from a LARQ PureVis bottle", None),
        ("Vinga", "Scandinavian design, Swedish quality", "assets/img/news/copper.jpg",
         "Two navy copper vacuum insulated bottles", "Vinga.png"),
    ],

    # Popular products across brands: name, brand, price, image, href
    "products": [
        ("IQONIQ Thelon Recycled Polyester Parka Jacket", "IQONIQ", "48.20", "news/parka.jpg", "#"),
        ("LARQ PureVis™ 2.0 680 ml water bottle", "LARQ", "75.93", "news/larq-680.jpg", "#"),
        ("LARQ PureVis™ 2.0 1000 ml water bottle", "LARQ", "83.52", "news/larq-1000.jpg", "#"),
        ("LARQ Swig Top 680 ml water bottle", "LARQ", "42.91", "news/larq-swig-680.jpg", "#"),
        ("LARQ Swig Top 1000 ml water bottle", "LARQ", "50.32", "news/larq-swig-1000.jpg", "#"),
        ("Minsk Unisex Hybrid Insulated Jacket", "Roly", "18.69", "products/clothing/minsk-jacket-black-heather.jpg", "product-minsk-v4.html"),
        ("CARRO Folding Crate Container Trolley", "midocean", "22.79", "products/office/carro-folding-crate-trolley.jpg", "#"),
        ("Hi-Vis Vest VISICOAT", "midocean", "2.19", "products/clothing/hi-vis-vest-visicoat-yellow.jpg", "product-hivis-v4.html"),
    ],

    "copy": [
        ("Why brand a brand?",
         ["A branded Bodum cafetière or CamelBak bottle carries two names: theirs and yours. The recipient "
          "already trusts the product, so your logo borrows that trust - and the piece stays on the desk, "
          "in the bag or in the kitchen for years rather than weeks.",
          "Every brand here is sourced through its official UK distributor, so the product, the warranty and "
          "the packaging are exactly what you'd find in a department store."]),
        ("How branding works on retail products",
         ["Most brands specify where and how their products can be decorated - a laser-engraved panel on a "
          "CamelBak, a pad print on a Sharpie barrel, an embroidered chest on an IQONIQ jacket. We show the "
          "approved positions on every product page and price each method live.",
          "Minimums are lower than you'd expect: many brands start at 10 units, and we hold UK stock for "
          "next-day plain and 5-10 working day branded delivery."]),
        ("Sustainability you can trace",
         ["IQONIQ, Ukiyo and Vinga publish the recycled content and the carbon footprint of every line. We "
          "print that figure on the product page and carry it through to your order confirmation, so it "
          "drops straight into your ESG reporting."]),
    ],

    "faq": [
        ("Can I brand any product from these brands?",
         "Almost all of them. Each brand approves specific decoration areas and methods, which we show on the product page; a handful of lines are supplied plain only."),
        ("Are these genuine branded products?",
         "Yes. Every line is sourced through the brand's official UK distributor and comes with the brand's own packaging and warranty."),
        ("What is the minimum order on branded-brand products?",
         "It varies by brand - most start at 10 or 25 units. The minimum is shown on each product page, and the price breaks run from there."),
        ("Can you send a visual on a specific brand product?",
         "Yes - send your logo and we'll come back with a mock-up on the exact product and position, free, within two hours in working time."),
    ],
}


def head(c):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta name="robots" content="noindex, nofollow">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c["title"])}</title>
<meta name="description" content="{esc(c["meta"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=119">
<link rel="stylesheet" href="assets/css/list-v4.css?v=32">
<link rel="stylesheet" href="assets/css/category-v4.css?v=5">
<link rel="stylesheet" href="assets/css/brands-v4.css?v=1">
<link rel="stylesheet" href="assets/css/mega-v4.css?v=2">
<script>document.documentElement.className += " js";</script>
"""


def hero(c):
    h1a, h1b = c["h1"]
    return f"""  <!-- ============ HERO ============ -->
  <section class="lhero" aria-labelledby="cat-h">
    <div class="wrap">
      <div class="lhero__grid">
        <div class="lhero__copy">
          <span class="eyebrow eyebrow--onforest">{esc(c["eyebrow"])}</span>
          <h1 id="cat-h">{esc(h1a)}<br><span class="hl">{esc(h1b)}</span></h1>
          <p>{esc(c["lede"])}</p>
          <div class="lhero__cta">
            <a href="#brands" class="btn btn--onforest">Browse all brands {icon("i-arrow", 18)}</a>
            <a href="#product-grid" class="btn btn--outline btn--outline-onforest">Popular products</a>
          </div>
        </div>
        <div class="lhero__media">
          <img src="{c["hero_img"]}" alt="Branded products from retail brands" width="1200" height="896">
        </div>
      </div>
    </div>
  </section>"""


def brand_grid(c):
    tiles = chr(10).join(f"""        <a href="#" class="brandcell">
          <span class="brandcell__logo"><img src="assets/img/brands/{logo}" alt="{esc(name)}" loading="lazy"></span>
          <span class="brandcell__name">{esc(name)}</span>
          <span class="brandcell__n">{n} products</span>
        </a>""" for name, logo, n in c["brands"])
    letters = "".join(f'<a href="#" class="az__l{" is-on" if ch in "BCHIKMSUVW" else ""}">{ch}</a>'
                      for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return f"""  <!-- ============ ALL BRANDS ============ -->
  <section class="sec" id="brands" aria-labelledby="brands-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Every brand we stock</span>
          <h2 id="brands-h">Browse brands <span class="hl">A to Z.</span></h2>
        </div>
        <span class="sticker"><b>{len(c["brands"])}</b><span>brands</span></span>
      </div>
      <nav class="az" aria-label="Brands by letter" data-reveal>{letters}</nav>
      <div class="brandgrid" data-reveal>
{tiles}
      </div>
    </div>
  </section>"""


def featured(c):
    tiles = []
    for name, line, img, alt, logo in c["featured"]:
        mark = (f'<img class="brandfeat__logo" src="assets/img/brands/{logo}" alt="" loading="lazy">' if logo
                else f'<span class="brandfeat__word">{esc(name)}</span>')
        tiles.append(f"""        <a href="#" class="brandfeat">
          <img src="{img}" alt="{esc(alt)}" loading="lazy" width="600" height="470">
          <span class="brandfeat__cap">{mark}<b>{esc(line)}</b><span>Shop {esc(name)} {icon("i-arrow", 15)}</span></span>
        </a>""")
    return f"""  <!-- ============ FEATURED BRANDS ============ -->
  <section class="sec sec--band" aria-labelledby="feat-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Featured this month</span>
          <h2 id="feat-h">Three brands <span class="hl">worth a look.</span></h2>
        </div>
      </div>
      <div class="brandfeats" data-reveal>
{chr(10).join(tiles)}
      </div>
    </div>
  </section>"""


def popular(c):
    cards = chr(10).join(f"""        <a href="{href}" class="prod" data-price="{price}">
          <span class="prod__media"><span class="prod__flag">{icon("i-star", 17)}{esc(brand)}</span><img src="assets/img/{img}" alt="{esc(name)}" loading="lazy" width="360" height="360"></span>
          <span class="prod__name">{esc(name)}</span>
          <span class="prod__price"><span class="prod__aslow">As low as</span><b>&pound;{price}</b> <small>per unit</small></span>
          <span class="prod__cta">Explore {icon("i-arrow", 15)}</span>
        </a>""" for name, brand, price, img, href in c["products"])
    return f"""  <!-- ============ POPULAR PRODUCTS ============ -->
  <section class="sec" aria-labelledby="pop-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Most ordered</span>
          <h2 id="pop-h">Popular <span class="hl">brand products.</span></h2>
        </div>
        <a href="products-v4.html" class="btn btn--outline btn--sm">View all products {icon("i-arrow", 16)}</a>
      </div>
      <div class="rail rail--grid" id="product-grid" data-reveal>
{cards}
      </div>
    </div>
  </section>"""


def weekly():
    return f"""  <!-- ============ WEEKLY TOP 4 ============ -->
  <section class="sec sec--band" aria-labelledby="week-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">This week&rsquo;s picks</span>
          <h2 id="week-h">Top four, <span class="hl">refreshed weekly.</span></h2>
          <p>A different four every week, drawn at random from the range. Week <b id="week-no">&mdash;</b>.</p>
        </div>
      </div>
      <div class="rail rail--four" id="weekly-picks" data-reveal></div>
    </div>
  </section>

  <!-- ============ WEEKLY DEALS ============ -->
  <section class="sec deals" aria-labelledby="deals-h">
    <div class="wrap">
      <div class="deals__head" data-reveal>
        <div class="sechead">
          <span class="eyebrow">This week&rsquo;s deals</span>
          <h2 id="deals-h">Top four deals, <span class="hl">10% off until Monday.</span></h2>
          <p>Four brand products at 10% off until the week closes &mdash; then a new four take over.</p>
        </div>
        <div class="countdown" aria-live="polite">
          <span class="countdown__t">Deal ends in</span>
          <div class="countdown__clock" data-countdown>
            <span><b>0</b><small>days</small></span><span><b>00</b><small>hrs</small></span><span><b>00</b><small>min</small></span><span><b>00</b><small>sec</small></span>
          </div>
        </div>
      </div>
      <div class="rail rail--four" id="weekly-deals" data-reveal></div>
      <p class="deals__foot">
        <span>Prices revert at midnight on Sunday. <b id="deals-week"></b></span>
        <a href="offers-v4.html" class="tlink">View all offers this week {icon("i-arrow", 16)}</a>
      </p>
    </div>
  </section>"""


def copy_block(c):
    parts = chr(10).join(f"""          <section class="story__part">
            <h3>{esc(h)}</h3>
{chr(10).join(f"            <p>{esc(x)}</p>" for x in ps)}
          </section>""" for h, ps in c["copy"])
    return f"""  <!-- ============ ABOUT ============ -->
  <section class="sec sec--band" aria-labelledby="about-h">
    <div class="wrap">
      <div class="story" data-reveal>
        <div class="story__aside">
          <span class="eyebrow">About branded brands</span>
          <h2 id="about-h">Retail names, <span class="hl">your logo.</span></h2>
          <p class="story__stand">Products people would buy for themselves, decorated the way the brand approves.</p>
          <a href="#brands" class="btn btn--outline btn--sm">Browse the brands {icon("i-arrow", 16)}</a>
        </div>
        <div class="story__body">
{parts}
        </div>
      </div>
    </div>
  </section>"""


def faq(c):
    items = chr(10).join(f"""          <details{" open" if i == 0 else ""}>
            <summary>{esc(q)}</summary>
            <p>{esc(a)}</p>
          </details>""" for i, (q, a) in enumerate(c["faq"]))
    return f"""  <!-- ============ FAQ ============ -->
  <section class="sec" id="faq" aria-labelledby="faq-h">
    <div class="wrap">
      <div class="sechead" data-reveal>
        <span class="eyebrow">Need to know</span>
        <h2 id="faq-h">Frequently asked questions <span class="hl">about brand products.</span></h2>
      </div>
      <div class="faq" data-reveal>
{items}
      </div>
    </div>
  </section>"""


def page(c):
    return "".join([head(c), CHROME, f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol><li><a href="index-v4.html">Home</a></li><li aria-current="page">{esc(c["crumb"])}</li></ol>
    </div>
  </nav>

{hero(c)}

{brand_grid(c)}

{featured(c)}

{popular(c)}

{weekly()}

{copy_block(c)}

{faq(c)}

""", FOOTER])


def main():
    out = ROOT / BRANDS["file"]
    out.write_text(page(BRANDS), encoding="utf-8")
    print(f"wrote {BRANDS['file']}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
