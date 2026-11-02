#!/usr/bin/env python3
"""Generate the 404 page (client round 3): site header and footer, a search,
popular categories and the ways back.

Writes 404-v4.html (the design page) and 404.html - GitHub Pages serves that
for any missing address, so it carries a <base> to keep assets resolving
from a nested path. [BUILD] Magento's CMS no-route page.

    python scripts/notfound/build.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
# No product-page or artwork script on this page.
FOOTER = re.sub(r'<script src="assets/js/(pdp-v4|quote-artwork-v4)\.js\?v=\d+"></script>\n?', "",
                (PDP / "_footer.html").read_text(encoding="utf-8"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


CATS = [
    ("Bags", "Totes, backpacks, drawstrings", "assets/img/hero-bags.png", "category-bags-v4.html"),
    ("Drinkware", "Bottles, cups and mugs", "assets/img/hero-drinkware.png", "products-v4.html"),
    ("Clothing", "Tees, hoodies, hi-vis", "assets/img/hero-clothing.png", "products-v4.html"),
    ("Tech", "Chargers, cables, speakers", "assets/img/categories/tech.png", "products-v4.html"),
    ("Eco &amp; Sustainable", "Carbon figure on every line", "assets/img/categories/eco-sustainable.png", "products-v4.html"),
    ("Home &amp; Living", "Kitchen, blankets, gifts", "assets/img/categories/home-living.png", "products-v4.html"),
    ("Outdoors &amp; Leisure", "Umbrellas, picnic, travel", "assets/img/categories/outdoors.png", "products-v4.html"),
    ("Themes &amp; Events", "Christmas, summer, sports", "assets/img/categories/themes-events.png", "products-v4.html"),
]


def page(base=""):
    tiles = "\n".join(f"""        <a href="{href}" class="cat nf__cat">
          <img src="{img}" alt="" loading="lazy">
          <span class="cat__meta"><span class="cat__name">{name}</span><span class="cat__n">{sub}</span></span>
        </a>""" for name, sub, img, href in CATS)
    body = f"""
<main id="main" tabindex="-1">

  <!-- ============ NOT FOUND ============ -->
  <section class="sec nf" aria-labelledby="nf-h">
    <div class="wrap nf__grid">
      <div class="nf__copy">
        <span class="eyebrow">Error 404 &middot; page not found</span>
        <h1 id="nf-h">This page has <span class="hl">gone walkabout.</span></h1>
        <p class="nf__lede">It may have moved, or the link has a typo. Search 25,000+ branded products,
        or start from one of our popular categories below.</p>

        <form class="nf__search" action="products-v4.html" role="search">
          <label class="vh" for="nf-q">Search products</label>
          <input id="nf-q" name="q" type="search" placeholder="Search 25,000+ branded products" autocomplete="off">
          <button class="btn btn--solid" type="submit">{icon("i-search", 18)}Search</button>
        </form>

        <div class="nf__acts">
          <a href="index-v4.html" class="btn btn--outline nf__back">{icon("i-arrow", 16)}Back to home</a>
          <a href="offers-v4.html" class="tlink">See today&rsquo;s offers {icon("i-arrow", 16)}</a>
          <a href="tel:+442083189603" class="tlink">Call 020 8318 9603 {icon("i-phone", 15)}</a>
        </div>
      </div>
      <p class="nf__code" aria-hidden="true">4<span>0</span>4</p>
    </div>
  </section>

  <!-- ============ POPULAR CATEGORIES ============ -->
  <section class="sec sec--band" aria-labelledby="nf-cats-h">
    <div class="wrap">
      <div class="sechead">
        <span class="eyebrow">Popular categories</span>
        <h2 id="nf-cats-h">Start <span class="hl">somewhere good.</span></h2>
      </div>
      <div class="nf__cats">
{tiles}
      </div>
    </div>
  </section>

</main>
"""
    head = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>Page not found | Bounce Creative Designs</title>
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=122">
<link rel="stylesheet" href="assets/css/notfound-v4.css?v=2">
<link rel="stylesheet" href="assets/css/mega-v4.css?v=6">
<script>document.documentElement.className += " js";</script>
"""
    return head + CHROME + body + FOOTER.replace("</main>\n", "", 1)


def main():
    (ROOT / "404-v4.html").write_text(page(), encoding="utf-8")
    # GitHub Pages serves /404.html for any missing address, at any depth.
    (ROOT / "404.html").write_text(page('<base href="/Bounce-Creative/">\n'), encoding="utf-8")
    print("wrote 404-v4.html and 404.html")


if __name__ == "__main__":
    main()
