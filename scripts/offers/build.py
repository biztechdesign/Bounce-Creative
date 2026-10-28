#!/usr/bin/env python3
"""Generate the Offers page.

The client's brief: a dynamic page of 50 products on offer. Each offer has
its own discount and its own end date (set per product in the catalogue), so
the page promises neither one percentage nor one deadline: every card shows
its own saving and its own countdown, and the hero sums them up. The design shows the pool we
have imagery for (the bags listing plus the product-page lines), with the
same card the list page uses so the two never drift.

    python scripts/offers/build.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
# Swap the product-page script for the offers scripts, whatever its version.
FOOTER = re.sub(r'<script src="assets/js/pdp-v4\.js\?v=\d+"></script>',
                '<script src="assets/js/deals-v4.js?v=3"></script>\n<script src="assets/js/offers-v4.js?v=2"></script>',
                re.sub(r'<script src="assets/js/quote-artwork-v4\.js\?v=\d+"></script>\n', "",
                       (PDP / "_footer.html").read_text(encoding="utf-8")))

# Demo values per product, standing in for the catalogue's special price
# and special-price end date. Picked from the name so they stay put between
# builds: a discount from DISCOUNTS and an end 1-14 days out.
DISCOUNTS = [5, 10, 12, 15, 18, 20, 25, 30]


def offer_terms(name):
    h = 0
    for ch in name:
        h = (h * 131 + ord(ch)) % 1000003
    return DISCOUNTS[h % len(DISCOUNTS)], 1 + (h // 7) % 14


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


def money(v):
    return f"&pound;{v:,.2f}"


# --------------------------------------------------------------------------
# The pool: the bags listing's cards, read from the list page so the data is
# the same, plus the lines that have their own product pages.
# --------------------------------------------------------------------------

def bag_cards():
    html = (ROOT / "products-v4.html").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<a href="#" class="prod" (.*?)>\n(.*?)\n        </a>', html, re.S):
        attrs, body = m.group(1), m.group(2)
        price = float(re.search(r'data-price="([\d.]+)"', attrs).group(1))
        img = re.search(r'<img src="([^"]+)" alt="([^"]*)"', body)
        name = re.search(r'<span class="prod__name">(.*?)</span>', body).group(1)
        rate = re.search(r'<b>([\d.]+)</b> \((\d+)\)', body)
        flag = re.search(r'<span class="prod__flag[^>]*>.*?</span>', body, re.S)
        sw = re.search(r'<span class="prod__sw">.*?</span>', body, re.S)
        out.append({
            "name": name, "img": img.group(1), "alt": img.group(2), "price": price,
            "rating": rate.group(1) if rate else None, "count": rate.group(2) if rate else None,
            "flag": flag.group(0) if flag else "", "sw": sw.group(0) if sw else "",
            "cat": "bags", "href": "#",
        })
    return out


RAIL_CATS = {"bags": "bags", "drink": "drinkware", "tech": "tech", "pens": "pens",
             "office": "office", "give": "giveaways"}


def home_cards():
    """The home page's category and eco rails - the rest of the range the
    mocks have imagery for."""
    html = (ROOT / "index-v4.html").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'id="rail-([a-z-]+)"[^>]*>(.*?)\n      </div>', html, re.S):
        key, block = m.group(1), m.group(2)
        cat = "eco" if key.startswith("eco") else RAIL_CATS.get(key)
        if not cat:
            continue
        for c in re.finditer(r'<a href="[^"]*" class="prod">(.*?)</a>', block, re.S):
            body = c.group(1)
            img = re.search(r'<img src="([^"]+)" alt="([^"]*)"', body)
            name = re.search(r'<span class="prod__name">(.*?)</span>', body)
            price = re.search(r'<b>&pound;([\d.,]+)</b>', body)
            if not (img and name and price):
                continue
            rate = re.search(r'<b>([\d.]+)</b> \((\d+)\)', body)
            flag = re.search(r'<span class="prod__flag[^>]*>.*?</span>', body, re.S)
            sw = re.search(r'<span class="prod__sw">.*?</span>', body, re.S)
            out.append({
                "name": name.group(1), "img": img.group(1), "alt": img.group(2),
                "price": float(price.group(1).replace(",", "")),
                "rating": rate.group(1) if rate else None, "count": rate.group(2) if rate else None,
                "flag": flag.group(0) if flag else "", "sw": sw.group(0) if sw else "",
                "cat": cat, "href": "#",
            })
    return out


def week_pool(n=50):
    """Up to `n` distinct products, a mix across categories (round-robin, so
    one big category never crowds out the rest)."""
    seen, by_cat = set(), {}
    for p in bag_cards() + EXTRA + home_cards():
        k = p["name"].lower()
        if k in seen:
            continue
        seen.add(k)
        by_cat.setdefault(p["cat"], []).append(p)
    out, lists = [], list(by_cat.values())
    while len(out) < n and any(lists):
        for lst in lists:
            if lst and len(out) < n:
                out.append(lst.pop(0))
    return out


EXTRA = [
    {"name": "Hi-Vis Vest VISICOAT", "img": "assets/img/products/clothing/hi-vis-vest-visicoat-yellow.jpg",
     "alt": "Hi-Vis Vest VISICOAT in fluorescent yellow", "price": 1.75, "rating": "4.7", "count": "84",
     "flag": f'<span class="prod__flag">{icon("i-check", 17)}EN ISO 20471</span>',
     "sw": '<span class="prod__sw"><i style="--sw:#E3F04A"></i><i style="--sw:#F4791F"></i></span>',
     # Links to the vest's on-offer product page, so the terms match it.
     "cat": "clothing", "href": "product-hivis-offer-v4.html", "offer": (18, 3)},
    {"name": "Minsk Unisex Hybrid Insulated Jacket", "img": "assets/img/products/clothing/minsk-jacket-black-heather.jpg",
     "alt": "Minsk jacket in black with heather black panels", "price": 18.69, "rating": "4.8", "count": "37",
     "flag": f'<span class="prod__flag">{icon("i-star", 17)}Premium</span>',
     "sw": '<span class="prod__sw"><i style="--sw:#1D1D1F"></i><i style="--sw:#1F2E5A"></i><i style="--sw:#4A4E54"></i><i style="--sw:#B32222"></i></span>',
     "cat": "clothing", "href": "product-minsk-v4.html"},
    {"name": "LARQ PureVis™ 2.0 680 ml water bottle", "img": "assets/img/news/larq-680.jpg",
     "alt": "LARQ PureVis 2.0 680 ml bottle", "price": 75.93, "rating": None, "count": None,
     "flag": f'<span class="prod__flag">{icon("i-bolt", 17)}Self-cleaning</span>', "sw": "", "cat": "drinkware", "href": "#"},
    {"name": "LARQ PureVis™ 2.0 1000 ml water bottle", "img": "assets/img/news/larq-1000.jpg",
     "alt": "LARQ PureVis 2.0 1000 ml bottle", "price": 83.52, "rating": None, "count": None,
     "flag": f'<span class="prod__flag">{icon("i-bolt", 17)}Self-cleaning</span>', "sw": "", "cat": "drinkware", "href": "#"},
    {"name": "LARQ Swig Top 680 ml water bottle", "img": "assets/img/news/larq-swig-680.jpg",
     "alt": "LARQ Swig Top 680 ml bottle", "price": 42.91, "rating": None, "count": None,
     "flag": "", "sw": "", "cat": "drinkware", "href": "#"},
    {"name": "LARQ Swig Top 1000 ml water bottle", "img": "assets/img/news/larq-swig-1000.jpg",
     "alt": "LARQ Swig Top 1000 ml bottle", "price": 50.32, "rating": None, "count": None,
     "flag": "", "sw": "", "cat": "drinkware", "href": "#"},
    {"name": "CARRO Folding Crate Container Trolley", "img": "assets/img/products/office/carro-folding-crate-trolley.jpg",
     "alt": "CARRO folding crate trolley", "price": 22.79, "rating": "4.6", "count": "19",
     "flag": f'<span class="prod__flag">{icon("i-box", 17)}Folds flat</span>', "sw": "", "cat": "office", "href": "#"},
    {"name": "Gift Card Box With Magnetic Closure HAKO", "img": "assets/img/email/mo6666-03.jpg",
     "alt": "Black gift card box with magnetic closure", "price": 3.76, "rating": None, "count": None,
     "flag": "", "sw": '<span class="prod__sw"><i style="--sw:#FFFFFF"></i><i style="--sw:#111111"></i></span>',
     "cat": "office", "href": "#"},
]

CATS = [("all", "All offers"), ("bags", "Bags"), ("tech", "Tech"), ("drinkware", "Drinkware"), ("clothing", "Clothing"),
        ("pens", "Pens"), ("office", "Office"), ("giveaways", "Giveaways"), ("eco", "Eco")]


def terms(p):
    return p.get("offer") or offer_terms(p["name"])


def card(p):
    pct, days = terms(p)
    now = p["price"] * (1 - pct / 100)
    rate = (f'          <span class="prod__rate">{icon("i-star", 14)}<b>{p["rating"]}</b> ({p["count"]})</span>\n'
            if p["rating"] else "")
    return f"""        <a href="{p["href"]}" class="prod" data-cat="{p["cat"]}" data-price="{now:.2f}" data-discount="{pct}" data-ends-days="{days}">
          <span class="prod__media"><span class="prod__flag prod__flag--deal">{icon("i-tag", 17)}{pct}% off</span><img src="{p["img"]}" alt="{esc(p["alt"])}" loading="lazy" width="360" height="360"></span>
{rate}          <span class="prod__name">{p["name"]}</span>
          {p["sw"]}
          <span class="prod__price"><span class="prod__aslow">Offer price, as low as</span><b>{money(now)}</b> <s>{money(p["price"])}</s></span>
          <span class="prod__ends">{icon("i-bolt", 13)}Offer ends in <b data-countdown="short" data-ends-days="{days}">&mdash;</b></span>
          <span class="prod__cta">Explore {icon("i-arrow", 15)}</span>
        </a>"""


def page():
    pool = week_pool()
    cards = chr(10).join(card(p) for p in pool)
    top = max(terms(p)[0] for p in pool)
    soonest = min(terms(p)[1] for p in pool)
    chips = chr(10).join(
        f'          <button class="chip" type="button" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{label}</button>'
        for k, label in CATS)

    body = f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol><li><a href="index-v4.html">Home</a></li><li aria-current="page">Offers</li></ol>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="lhero lhero--compact offers-hero" aria-labelledby="offers-h">
    <div class="wrap">
      <div class="lhero__grid">
        <div class="lhero__copy">
          <span class="eyebrow eyebrow--onforest">Offers</span>
          <h1 id="offers-h">{len(pool)} offers, <span class="hl">up to {top}% off.</span></h1>
          <p>Every offer has its own saving and its own end date &mdash; the price and the clock are on each
          product. When an offer ends its price goes back to normal and a new one takes its place.</p>
          <div class="lhero__cta">
            <a href="#offers" class="btn btn--onforest">See the offers {icon("i-arrow", 18)}</a>
            <a href="products-v4.html" class="btn btn--outline btn--outline-onforest">Browse everything</a>
          </div>
        </div>
        <!-- A summary, not one deadline: offers end on different days. -->
        <div class="offers-clock">
          <dl class="offers-sum">
            <div><dt>Biggest saving</dt><dd>{top}%</dd></div>
            <div><dt>Offers live</dt><dd>{len(pool)}</dd></div>
          </dl>
          <span class="countdown__t">Next offer ends in</span>
          <div class="countdown__clock countdown__clock--big" data-countdown data-ends-days="{soonest}">
            <span><b>&ndash;</b><small>days</small></span><span><b>&ndash;</b><small>hrs</small></span><span><b>&ndash;</b><small>min</small></span><span><b>&ndash;</b><small>sec</small></span>
          </div>
          <p class="offers-clock__n">Each product shows its own end date.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ HOW IT WORKS ============ -->
  <section class="trust" aria-label="How the weekly offers work">
    <div class="wrap">
      <ul class="trust__list trust__list--three">
        <li>{icon("i-tag", 22)}<span><b>Up to {top}% off</b><span>The branded price, with the same branding options as always</span></span></li>
        <li>{icon("i-bolt", 22)}<span><b>Each offer has its own end date</b><span>The clock on every product shows how long is left</span></span></li>
        <li>{icon("i-star", 22)}<span><b>Earn points as you go</b><span>Order online and collect reward points off your next order</span></span></li>
      </ul>
    </div>
  </section>

  <!-- ============ OFFERS ============ -->
  <section class="sec" id="offers" aria-labelledby="grid-h">
    <div class="wrap">
      <div class="offers-bar">
        <div class="chips" role="group" aria-label="Filter offers by category">
{chips}
        </div>
        <div class="offers-bar__end">
          <p class="offers-bar__count"><b id="offers-count">{len(pool)}</b> offers</p>
          <label class="listbar__sort">
            <span>Sort by</span>
            <select id="offers-sort">
              <option value="ending">Ending soonest</option>
              <option value="discount">Biggest discount</option>
              <option value="price-asc">Price, low to high</option>
              <option value="price-desc">Price, high to low</option>
            </select>
          </label>
        </div>
      </div>
      <h2 id="grid-h" class="vh">Current offers</h2>
      <div class="rail rail--grid" id="offers-grid">
{cards}
      </div>
      <p class="listing__none" id="offers-none" hidden>No offers in that category right now &mdash; new ones are added as others end.</p>
    </div>
  </section>

  <!-- ============ NUDGE ============ -->
  <section class="sec sec--band" aria-labelledby="nudge-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Missed something?</span>
          <h2 id="nudge-h">Every product still comes with a <span class="hl">free visual.</span></h2>
          <p>Offer or not, send us your logo and we come back with a print-accurate mock-up in two hours.</p>
        </div>
        <a href="products-v4.html" class="btn btn--solid">Browse all products {icon("i-arrow", 18)}</a>
      </div>
    </div>
  </section>

</main>
"""
    head = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta name="robots" content="noindex, nofollow">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Offers | Bounce Creative Designs</title>
<meta name="description" content="Branded merchandise on offer, each with its own saving and end date.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=121">
<link rel="stylesheet" href="assets/css/list-v4.css?v=32">
<link rel="stylesheet" href="assets/css/category-v4.css?v=5">
<link rel="stylesheet" href="assets/css/offers-v4.css?v=2">
<link rel="stylesheet" href="assets/css/mega-v4.css?v=6">
<script>document.documentElement.className += " js";</script>
"""
    footer = FOOTER.replace("</main>\n", "", 1)
    return head + CHROME + body + footer


def main():
    out = ROOT / "offers-v4.html"
    out.write_text(page(), encoding="utf-8")
    print(f"wrote offers-v4.html  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
