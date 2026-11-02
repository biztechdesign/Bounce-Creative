#!/usr/bin/env python3
"""Point the demo's placeholder links (href="#") at the designed pages, so
the prototype can be clicked through end to end.

Only pages that exist are linked: a link whose target is not designed yet
(privacy policy, careers, app stores, page 2 of results...) stays "#".
Runs over every *-v4.html page and the shared header / footer partials, so
re-run it after rebuilding pages:

    python scripts/links/build.py
"""

import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]

LISTING = "products-v4.html"
BAGS = "category-bags-v4.html"
BRANDS = "category-brands-v4.html"
OFFERS = "offers-v4.html"
NEWS = "news-v4.html"
ARTICLE = "news-larq-v4.html"
PDP = "product-hivis-v4.html"        # the priced product template
PDP_BAG = "product-v4.html"          # the bag (bespoke) product page
PDP_JACKET = "product-minsk-v4.html"

BRAND_NAMES = {"americano", "camelbak", "cross", "moleskine", "nordic drift", "ocean bottle", "parker",
               "stanley", "waterman", "swiss peak", "lindt", "bodum", "hidratespark", "iqoniq", "karst",
               "mepal", "sharpie", "skross", "ukiyo", "urban vitamin", "vinga", "larq", "brands"}
OFFER_TEXT = ("discounted products", "offers", "deals", "special offers", "sale")
# Exact texts -> page, wherever they appear.
TEXT = {
    "all products": LISTING, "shop all": LISTING, "view all products": LISTING,
    "shop all eco products": LISTING, "build a gift set": LISTING, "explore branded merchandise": LISTING,
    "new bags": LISTING, "recommended": LISTING, "top 10 budget": LISTING, "top 10 picks": LISTING,
    "see how we measure it": "about-v4.html", "sustainability & esg": "about-v4.html", "about bounce": "about-v4.html",
    "all news": NEWS, "all stories": NEWS, "industry news": NEWS, "product news": NEWS, "business news": NEWS,
    "eco": NEWS,   # only reached on the news page body; the header Eco link is handled first
    "track my order": "login-v4.html", "log in or sign up": "login-v4.html", "sign out": "login-v4.html",
    "my account": "account-address-v4.html", "account information": "account-address-v4.html",
    "reward dashboard": "account-rewards-v4.html", "transactions": "account-rewards-v4.html",
    "proceed to checkout": "email-order-v4.html",   # the order confirmation stands in for checkout
    "view product": PDP,
}
# Classes -> page (first class on the link).
CLASS = {
    "offer": OFFERS, "post": ARTICLE, "artnav__prev": ARTICLE, "mini": PDP, "brandcell": LISTING,
    "brandfeat": LISTING, "brandcard": LISTING, "ftile": LISTING, "mtile": LISTING, "az__l": None,
    "cat": LISTING,
}


def plain(inner):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner))).strip()


def product_page(name):
    n = name.lower()
    if "vest" in n or "hi-vis" in n or "visicoat" in n:
        return PDP
    if "minsk" in n or "jacket" in n:
        return PDP_JACKET
    if any(w in n for w in ("bag", "tote", "shopper", "backpack", "rolltop", "holdall")):
        return PDP_BAG
    return PDP


def target(attrs, inner, in_header):
    cls = re.search(r'class="([^"]*)"', attrs)
    first = cls.group(1).split()[0] if cls else ""
    text = plain(inner).lower()
    if first == "prod":
        name = re.search(r'class="prod__name">(.*?)</span>', inner, re.S)
        return product_page(plain(name.group(1)) if name else text)
    if first == "cat" and text.startswith("bags"):
        return BAGS
    if first in CLASS:
        return CLASS[first]
    if text in BRAND_NAMES:
        return BRANDS
    if any(text.startswith(o) for o in OFFER_TEXT):
        return OFFERS
    if in_header:
        # The mega menu: category headings and sub-categories open the listing,
        # Bags opens its landing page, the featured tiles their product.
        if text == "bags":
            return BAGS
        if "minsk" in text or "softshell jacket" in text:
            return PDP_JACKET
        if "hi-vis" in text or "hi vis" in text:
            return PDP
        return LISTING
    if text in TEXT:
        return TEXT[text]
    if first == "" and any(w in text for w in (" bags", "backpacks", "holdalls", "trolleys")):
        return LISTING          # sub-category text links on the bags landing page
    if "larq" in text:
        return PDP
    return None


LINK = re.compile(r'<a href="#"([^>]*)>(.*?)</a>', re.S)


def rewrite(text, header_end):
    out, last, n = [], 0, 0
    for m in LINK.finditer(text):
        href = target(m.group(1), m.group(2), m.start() < header_end)
        if not href:
            continue
        out.append(text[last:m.start()])
        out.append(f'<a href="{href}"{m.group(1)}>{m.group(2)}</a>')
        last = m.end()
        n += 1
    out.append(text[last:])
    return "".join(out), n


def main():
    total = 0
    for f in sorted(ROOT.glob("*-v4.html")):
        if f.name.startswith("email-"):
            continue
        t = f.read_text(encoding="utf-8")
        end = t.find('<main')
        t2, n = rewrite(t, end if end >= 0 else 0)
        if n:
            f.write_text(t2, encoding="utf-8")
        total += n
        print(f"{f.name:32} {n:4} linked, {len(LINK.findall(t2)):4} left as #")
    for part, is_header in (("scripts/pdp/_chrome.html", True), ("scripts/pdp/_footer.html", False)):
        p = ROOT / part
        t = p.read_text(encoding="utf-8")
        t2, n = rewrite(t, len(t) if is_header else 0)
        p.write_text(t2, encoding="utf-8")
        print(f"{part:32} {n:4} linked")
    print("total linked:", total)


if __name__ == "__main__":
    main()
