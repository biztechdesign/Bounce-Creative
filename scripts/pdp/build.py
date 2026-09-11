#!/usr/bin/env python3
"""Generate the v4 product detail pages.

Three products, one design. The header, nav, drawer and footer are shared
partials (_chrome.html, _footer.html) so the chrome cannot drift between
pages; everything product-specific lives in PRODUCTS below.

The volume pricing table is computed from the same tier ladder and method
costs that the live calculator uses, so the printed table and the running
total can never disagree.

    python scripts/pdp/build.py
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent

CHROME = (HERE / "_chrome.html").read_text(encoding="utf-8")
FOOTER = (HERE / "_footer.html").read_text(encoding="utf-8")

# Shared commercial terms, quoted from the live site.
EXPRESS_RATE = 0.35      # per unit  (default; a product can override - the live
EXPRESS_FEE = 25.00      # one-off    engine charges a flat 100 per order)
EXPRESS_SAVING = 3       # working days off the lead time
POINTS_PER_POUND = 0.1   # 558 points on a £5,577 order, per the live panel
POINT_VALUE = 0.50       # "your points equal £279" - 50p a point
FREE_DELIVERY_OVER = 3000
BASE_SHIP = 2            # working days, tracked UK
EXPRESS_SHIP = 1
MAX_LOCATIONS = 4        # branding positions on one product
SMALL_ORDER_UNDER = 250.00   # order value below which the surcharge applies
SMALL_ORDER_FEE = 50.00      # the surcharge, once per order
BREAKS_SHOWN = 5             # price breaks visible before "show more"

# The tick badge a chosen tile or position card carries.
TICK = '<span class="tile__tick" aria-hidden="true"><svg class="ic" width="13" height="13"><use href="#i-check"/></svg></span>'


# --------------------------------------------------------------------------
# Products
# --------------------------------------------------------------------------

PRODUCTS = [
    # ---------------------------------------------------------------- vest
    {
        "file": "product-hivis-v4.html",
        "name": "Hi-Vis Vest VISICOAT",
        "sku": "mid-MO2243",
        "category": "Clothing",
        "category_href": "index-v4.html#catalogue",
        "title": "Hi-Vis Vest VISICOAT — Branded Safety Waistcoat | Bounce Creative Designs",
        "meta": (
            "Hi-Vis Vest VISICOAT from £2.19. EN ISO 20471 Class 2 safety waistcoat in "
            "100% knitted polyester, screen printed or transfer branded in the UK."
        ),
        "ld_desc": (
            "Safety waistcoat made in 100% knitted polyester with Class 2 high visibility "
            "reflective tape. EN ISO 20471."
        ),
        "lede": (
            "A Class 2 safety waistcoat in 100% knitted polyester, certified to EN ISO 20471. "
            "The site-standard vest, branded front and back and stocked in volume."
        ),
        "rating": "4.7",
        "reviews": 84,
        "customers": "1,940",
        "flag": ("i-check", "EN ISO 20471"),
        "colours": [
            ("Fluorescent yellow", "#E3F04A", "hi-vis-vest-visicoat-yellow.jpg",
             "Hi-Vis Vest VISICOAT in fluorescent yellow, shown unbranded"),
            ("Fluorescent orange", "#F4791F", "hi-vis-vest-visicoat-orange.jpg",
             "Hi-Vis Vest VISICOAT in fluorescent orange, shown unbranded"),
        ],
        "gallery": [
            ("hi-vis-vest-visicoat-yellow.jpg", "Fluorescent yellow, front"),
            ("hi-vis-vest-visicoat-yellow-back.jpg", "Fluorescent yellow, back"),
            ("hi-vis-vest-visicoat-orange.jpg", "Fluorescent orange, front"),
            ("hi-vis-vest-visicoat-orange-worn.jpg", "Fluorescent orange, worn"),
        ],
        "img_dir": "clothing",
        "sizes": None,
        "positions": [
            ("Left breast", 31, 27, 16, 11),
            ("Right breast", 53, 27, 16, 11),
            ("Front, centre", 34, 42, 32, 18),
            ("Back, centre", 30, 30, 40, 24),
        ],
        # Per-branding-type price ladders, as the live configurator quotes them:
        # each type has its own per-unit price at every break (one colour),
        # its own sub-options, and its own pre-production sample price. The
        # 25-500 figures are the live site's; 1,000 and 2,500 extend the curve.
        "methods": [
            {"name": "Transfer printing", "lead": 2, "cmyk": False,
             "colours": [1, 2, 3, 4, 5, 6, 7, 8], "extra_colour": 0.35, "logo_sizes": [150],
             "ladder": [(25, 5.53), (50, 4.46), (100, 3.93), (250, 3.55), (500, 3.11), (1000, 2.84), (2500, 2.62)],
             "sample": 39.13,
             # Branding price each by quantity and colour count - the live matrix.
             "matrix": {
                 "qtys": [1, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000],
                 "rows": [
                     [2.56, 3.92, 5.29, 6.66], [2.11, 3.01, 3.91, 4.81], [1.87, 2.67, 3.47, 4.28],
                     [1.70, 2.33, 2.97, 3.60], [1.22, 1.64, 2.06, 2.49], [1.06, 1.44, 1.82, 2.20],
                     [0.95, 1.25, 1.54, 1.84], [0.89, 1.13, 1.37, 1.61], [0.82, 1.02, 1.22, 1.41],
                     [0.74, 0.92, 1.10, 1.29],
                 ],
             }},
            {"name": "Digital transfer", "lead": 2, "cmyk": True,
             "colours": [], "extra_colour": 0, "logo_sizes": [150],
             "ladder": [(25, 4.46), (50, 3.70), (100, 3.32), (250, 3.07), (500, 2.98), (1000, 2.85), (2500, 2.74)],
             "sample": 38.06},
            {"name": "Transfer reflective", "lead": 3, "cmyk": False,
             "colours": [1], "extra_colour": 0, "logo_sizes": [150],
             "ladder": [(25, 6.80), (50, 5.77), (100, 4.93), (250, 4.46), (500, 3.76), (1000, 3.42), (2500, 3.15)],
             "sample": 40.40},
            {"name": "Screen printing", "lead": 0, "cmyk": False,
             "colours": [1, 2, 3, 4], "extra_colour": 0.22, "logo_sizes": [],
             "ladder": [(25, 5.17), (50, 4.07), (100, 3.53), (250, 3.11), (500, 2.90), (1000, 2.68), (2500, 2.50)],
             "sample": 38.77},
        ],
        "tiers": [(25, 2.19), (50, 2.08), (100, 1.98), (250, 1.82), (500, 1.67), (1000, 1.54), (2500, 1.42)],
        "min_qty": 25,
        "step": 25,
        "base_lead": 5,
        "stock": 12480,
        "spec": [
            ("Material", "100% knitted polyester"),
            ("Certification", "EN ISO 20471 Class 2"),
            ("Dimensions", "65.5 × 70cm"),
            ("Commodity code", "6110 3091"),
            ("Reflective tape", "Two body bands, two braces"),
            ("Closure", "Touch-and-close front"),
            ("Print area", "Up to 250 × 200mm, back"),
            ("Minimum order", "25 units"),
        ],
        "prose": [
            ("Built for the site",
             ["A Class 2 waistcoat certified to EN ISO 20471, with two body bands and two "
              "braces of reflective tape. Knitted polyester rather than the stiffer woven "
              "grade, so it sits over a jacket without riding up.",
              "Touch-and-close front, cut generously enough to layer over winter kit."]),
            ("Where it works",
             ["Construction and civils, event stewarding, car park marshalling, school trips "
              "and volunteer days.",
              "Ordered most often in fluorescent yellow with a back print, which is what a "
              "site induction expects to see."]),
            ("Branding notes",
             ["Print goes on the plain panels between the reflective bands, never over them — "
              "overprinting tape voids the certification.",
              "Back centre gives the largest usable area at 250 × 200mm; left breast is the "
              "usual second position."]),
        ],
        "faq": [
            ("Does printing affect the EN ISO 20471 rating?",
             "Not when it sits on the plain fabric panels. We never print over reflective tape, "
             "because that reduces the retroreflective area the certification is based on."),
            ("What is the minimum order?",
             "25 units. Below that, ask about our stocked plain vests, which ship from a single unit."),
            ("Can I have different colours in one order?",
             "Yes. Mix fluorescent yellow and orange freely across the run; the setup charge is "
             "per print colour, not per garment colour."),
            ("How quickly can these ship?",
             "Screen printed runs are 5–7 working days from artwork approval. Express takes that "
             "to 2–4 working days for a surcharge."),
        ],
        "related": [
            ("Minsk Unisex Hybrid Insulated Jacket", "clothing/minsk-jacket-black-heather.jpg",
             "18.69", "4.8", 37, "product-minsk-v4.html"),
            ("Natural Cotton Shopper", "v4/same_day_natural_cotton_shopper.jpg",
             "3.48", "4.8", 126, "product-v4.html"),
            ("Full Colour Bucket Hat", "branded_full_colour_bucket_hat.jpg",
             "4.62", "4.6", 41, "#"),
            ("Jumbo Non Woven Exhibition Bag", "v4/jumbo_exhibition_bag_yellow.jpg",
             "3.40", "4.9", 54, "#"),
        ],
    },

    # -------------------------------------------------------------- jacket
    {
        "file": "product-minsk-v4.html",
        "name": "Minsk Unisex Hybrid Insulated Jacket",
        "sku": "pf-R1120",
        "category": "Clothing",
        "category_href": "index-v4.html#catalogue",
        "title": "Minsk Unisex Hybrid Insulated Jacket — Branded Softshell | Bounce Creative Designs",
        "meta": (
            "Minsk unisex hybrid insulated jacket from £18.69. Quilted front with softshell "
            "sleeves and hood, embroidered or transfer branded in the UK. Sizes S to 3XL."
        ),
        # Verbatim from the live page, which also uses it as the lede under the price.
        "ld_desc": (
            'Unisex jacket in two-fabric combination: fixed adjusted hood. Raglan sleeves. Sleeves, side panels and hood in softshell fabric. Quilted feather touch fabric in front and back. Inverted zip with matching chin protector and puller. Two front pockets with zippers. Matching elastic trim in collar, cuffs and hem. Removable label. Wind-proof model. The male model is 184 cm and is wearing size L, and the female model is 179 cm and is wearing size S.'
        ),
        "lede": (
            'Unisex jacket in two-fabric combination: fixed adjusted hood. Raglan sleeves. Sleeves, side panels and hood in softshell fabric. Quilted feather touch fabric in front and back. Inverted zip with matching chin protector and puller. Two front pockets with zippers. Matching elastic trim in collar, cuffs and hem. Removable label. Wind-proof model. The male model is 184 cm and is wearing size L, and the female model is 179 cm and is wearing size S.'
        ),
        "rating": "4.8",
        "reviews": 37,
        "customers": "612",
        "flag": ("i-star", "Premium"),
        "colours": [
            ("Black / heather black", "#1D1D1F", "minsk-jacket-black-heather.jpg",
             "Minsk jacket in black with heather black panels, shown unbranded", "R11208M"),
            ("Navy blue / royal blue", "#1F2E5A", "minsk-jacket-navy-royal.jpg",
             "Minsk jacket in navy with royal blue panels, shown unbranded", "R11209T"),
            ("Black / lead", "#4A4E54", "minsk-jacket-black-lead.jpg",
             "Minsk jacket in black with lead grey panels, shown unbranded", "R1120C5"),
            ("Red / black", "#B32222", "minsk-jacket-red-black.jpg",
             "Minsk jacket in red with black panels, shown unbranded", "R11208K"),
        ],
        "gallery": [
            ("minsk-jacket-black-heather.jpg", "Black / heather black, front"),
            ("minsk-jacket-side.jpg", "Black / heather black, three-quarter"),
            ("minsk-jacket-black-heather-back.jpg", "Black / heather black, back"),
            ("minsk-jacket-detail.jpg", "Hood and zip detail"),
        ],
        "img_dir": "clothing",
        "sizes": ["S", "M", "L", "XL", "2XL", "3XL"],
        # Live stock levels per colourway and size, as the "configure your
        # product" grid shows them. Quantity is entered per size against these.
        "stock_by_size": {
            "R11208M": {"S": 111, "M": 287, "L": 456, "XL": 524, "2XL": 232, "3XL": 49},
            "R1120C5": {"S": 14, "M": 12, "L": 9, "XL": 9, "2XL": 16, "3XL": 16},
            "R11208K": {"S": 20, "M": 18, "L": 2, "XL": 10, "2XL": 6, "3XL": 19},
            "R11209T": {"S": 2, "M": 17, "L": 8, "XL": 19, "2XL": 22, "3XL": 2},
        },
        "express": {"rate": 0, "fee": 100.00},   # live: expressCharges 100, flat
        "co2_kg": 3.768416953,                   # live ESG footprint, per unit
        # The live positions. Each has a supplier image per colourway with the
        # print zone already marked, so no overlay box is drawn.
        "positions": [
            ("Left chest", "left-chest", ["EMBF03", "EMBF02"]),
            ("Right chest", "right-chest", ["EMBF03", "EMBF02"]),
            ("Impact upper back", "upper-back", ["EMBF03", "EMBF02"]),
            ("Right bicep", "right-bicep", ["EMBF02", "MR07"]),
            ("Left bicep", "left-bicep", ["EMBF02", "MR07"]),
        ],
        "position_img": "clothing/minsk-positions/{code}-{pos}.jpg",
        # Live pricing engine data for this product. Branding is priced from a
        # matrix of price-each by quantity and colour count, plus a setup per
        # colour count; the unprinted price is flat.
        "pricing": "matrix",
        "methods": [
            {"id": "EMBF03", "name": "Embroidery fixed 3", "lead": 3, "cmyk": False,
             "colours": [], "logo_sizes": [14], "setup": {1: 34.78},
             "matrix": {"qtys": [1, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000],
                        "rows": [[5.96], [3.75], [3.11], [2.18], [2.13], [2.10], [2.05], [2.04], [2.01], [2.00]]}},
            {"id": "EMBF02", "name": "Embroidery fixed 2", "lead": 3, "cmyk": False,
             "colours": [], "logo_sizes": [14], "setup": {1: 34.78},
             "matrix": {"qtys": [1, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000],
                        "rows": [[5.34], [3.45], [2.72], [1.97], [1.85], [1.69], [1.65], [1.64], [1.59], [1.58]]}},
            {"id": "MR07", "name": "Screenprint B Textile 2", "lead": 2, "cmyk": False,
             "colours": [1, 2, 3, 4, 5], "logo_sizes": [14], "setup": {1: 25, 2: 50, 3: 75, 4: 100, 5: 125},
             "matrix": {"qtys": [1, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000],
                        "rows": [[1.93, 2.53, 3.13, 3.73, 4.33], [1.38, 1.79, 1.98, 2.30, 2.66],
                                 [0.92, 1.22, 1.48, 1.80, 2.12], [0.68, 0.96, 1.21, 1.50, 1.80],
                                 [0.66, 0.89, 1.09, 1.38, 1.65], [0.64, 0.82, 1.02, 1.29, 1.54],
                                 [0.56, 0.76, 0.94, 1.18, 1.42], [0.51, 0.70, 0.85, 1.05, 1.27],
                                 [0.49, 0.69, 0.84, 1.03, 1.26], [0.48, 0.69, 0.82, 1.02, 1.25]]}},
        ],
        "tiers": [(1, 18.69)],
        "breaks": [1, 25, 50, 100, 250, 500, 750, 1000, 1500, 2000, 5000],
        "min_qty": 1,
        "step": 1,
        "base_lead": 7,
        "stock": 16,        # live: max available for the selected variant
        "spec": [
            ("EAN code", "8713159628811"),
            ("Collection", "CO₂ products"),
            ("Total CO₂ emissions", "3.77 kg CO₂e per unit"),
        ],
        "prose": [
            ("Two fabrics, one jacket",
             ["Quilted feather-touch panels front and back hold the warmth. Softshell sleeves, "
              "side panels and hood let the arms move and shed a shower.",
              "Raglan sleeves and a fixed adjustable hood, with matching elastic trim at the "
              "collar, cuffs and hem."]),
            ("Where it works",
             ["Staff kit that gets worn off shift — outdoor teams, dealership and events staff, "
              "and client gifting where a tote will not carry the message.",
              "The removable label means it can be rebranded properly rather than badged over."]),
            ("Branding notes",
             ["Embroidery is the right finish here and the one we quote first; it survives the "
              "washing this jacket will get.",
              "Left breast at 50cm² is included in the price. A back yoke logo is the usual "
              "second position and is charged by area."]),
        ],
        "faq": [
            ("Is this jacket unisex?",
             "Yes, cut as a single unisex block from S to 3XL. Most teams order one size up from "
             "a fitted shirt size because of the quilted panels."),
            ("Can I split sizes across one order?",
             "Yes. Mix sizes and colours freely — the minimum of 10 applies to the order, not to "
             "each variant, and setup is charged once per logo."),
            ("Why embroidery rather than print?",
             "Softshell and quilted fabrics do not hold a screen print well. Embroidery stitches "
             "into the face fabric and outlasts the jacket."),
            ("What is the published CO₂ figure?",
             "3.77 kg CO₂e per unit, supplied by the manufacturer as a cradle-to-gate figure "
             "covering all greenhouse gases."),
        ],
        "related": [
            ("Hi-Vis Vest VISICOAT", "clothing/hi-vis-vest-visicoat-yellow.jpg",
             "2.19", "4.7", 84, "product-hivis-v4.html"),
            ("Full Colour Bucket Hat", "branded_full_colour_bucket_hat.jpg",
             "4.62", "4.6", 41, "#"),
            ("Westcove Canvas Tote", "v4/westcove_canvas_tote_black.jpg",
             "8.41", "4.7", 210, "#"),
            ("Organic Festival Backpack", "v4/organic_festival_backpack.jpg",
             "9.85", "4.8", 33, "#"),
        ],
    },

    # ------------------------------------------------------------- shopper
    {
        "file": "product-v4.html",
        "name": "Next Day Natural Cotton Shopper",
        "sku": "SAME DAY NATURAL COTTON SHOPPER",
        # Live: a bespoke-quote product. No options, no configurator, no cart -
        # an inline quote form in place of the buy flow.
        "mode": "quote",
        "tagline": "Natural cotton shopper \u2014 custom branded",
        "category": "Bags",
        "category_href": "products-v4.html",
        "title": "Natural Cotton Shopper — Next Day Branded Tote Bag | Bounce Creative Designs",
        "meta": (
            "Natural Cotton Shopper, 5oz branded tote bag from £3.48. Stocked in the UK for "
            "next day print, 1 to 4 colour pantone or full colour digital."
        ),
        # Verbatim from the live page.
        "ld_desc": (
            'Natural 5oz cotton shopper with long handles. Premium quality bag. The perfect promotional giveaway. Large print area to both sides, therefore providing fantastic brand exposure.'
        ),
        "lede": (
            'Natural 5oz cotton shopper with long handles. Premium quality bag. The perfect promotional giveaway. Large print area to both sides, therefore providing fantastic brand exposure.'
        ),
        "desc_extra": [
            "Material: 100% cotton. Dimensions: 380 \u00d7 420mm. Weight: 5oz.",
            "All stocked in the UK, printing 1, 2, 3 or 4 colour Pantone print including full "
            "colour digital printing.",
        ],
        "rating": "4.8",
        "reviews": 126,
        "customers": "3,056",
        "flag": ("i-delivery", "Next day"),
        "colours": [
            ("Natural", "#E4DFCF", "v4/same_day_natural_cotton_shopper.jpg",
             "Next Day Natural Cotton Shopper, shown unbranded"),
        ],
        "gallery": [
            ("v4/same_day_natural_cotton_shopper.jpg", "Natural cotton shopper, front"),
            ("bags/samedaybags-natural-cotton-shopper.jpg", "Natural cotton shopper, in use"),
        ],
        "img_dir": "",
        "sizes": None,
        "positions": [],
        "methods": [],
        "tiers": [(1, 3.48)],
        "breaks": [],
        "min_qty": 1,
        "step": 1,
        "base_lead": 5,   # live: 5-7 working days
        "stock": 24500,
        "spec": [
            ("Colours", "Natural & black"),
            ("Collection", "Bespoke products, new products"),
        ],
        "prose": [
            ("An everyday shopper",
             ["5oz natural cotton with long handles, sized to carry an A4 folder without "
              "straining the seams. The most ordered bag in the range, and the one most likely "
              "to still be in use a year after the event.",
              "Supplied unbranded for sampling, or printed to your artwork from 25 units."]),
            ("Where it works",
             ["Exhibitions and conference welcome packs, retail purchases, campaign giveaways "
              "and staff onboarding kits.",
              "Because it gets reused, the cost per impression falls every time it leaves the "
              "house — which is what separates a bag from a leaflet."]),
            ("Care and longevity",
             ["Machine washable at 30°C, inside out. Screen prints and embroidery hold up well; "
              "avoid tumble drying, which can crack a transfer over time.",
              "Cotton softens with washing rather than wearing out, so a bag handed out in "
              "spring is usually still in circulation the following year."]),
        ],
        "faq": [
            ("How long does printing take?",
             "Stock is held in the UK, so screen printed runs are 3–5 working days from artwork "
             "approval. Express brings that inside 48 hours on 1 and 2 colour work."),
            ("Can I see the logo before I commit?",
             "Yes. Send artwork in any format and a print-accurate visual comes back within two "
             "working hours, free, with no obligation."),
            ("What is the minimum order?",
             "25 units on this line. Below that, look at our stock range, which starts at a "
             "single unit."),
            ("How many colours can you print?",
             "1 to 4 colour pantone by screen, or unlimited colours by full colour digital. "
             "Overlapping shades and gradients need the digital route."),
        ],
        "related": [
            ("Coloured Cotton Shopper", "v4/next_day_coloured_cotton_shopper_blue.jpg",
             "3.93", "4.8", 92, "#"),
            ("Jumbo Non Woven Exhibition Bag", "v4/jumbo_exhibition_bag_yellow.jpg",
             "3.40", "4.9", 54, "#"),
            ("Westcove Canvas Tote", "v4/westcove_canvas_tote_black.jpg",
             "8.41", "4.7", 210, "#"),
            ("Organic Fashion Tote Bag", "v4/organic_fashion_tote_bag_green.jpg",
             "5.12", "4.9", 61, "#"),
        ],
    },
]




# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


def img_path(p, rel):
    """Product images live in a per-category folder, or loose for older lines."""
    d = p["img_dir"]
    return f"assets/img/products/{d}/{rel}" if d else f"assets/img/products/{rel}"


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def money(v):
    return f"&pound;{v:,.2f}"


# --------------------------------------------------------------------------
# Blocks
# --------------------------------------------------------------------------

def head(p):
    ld = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": p["name"],
        "sku": p["sku"],
        "description": p["ld_desc"],
        "brand": {"@type": "Brand", "name": "Bounce Creative Designs"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": p["rating"],
            "reviewCount": str(p["reviews"]),
        },
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "GBP",
            "lowPrice": f'{p["tiers"][-1][1]:.2f}',
            "highPrice": f'{p["tiers"][0][1]:.2f}',
            "offerCount": str(len(p["tiers"])),
            "availability": "https://schema.org/InStock",
        },
    }
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["meta"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=114">
<link rel="stylesheet" href="assets/css/list-v4.css?v=21">
<link rel="stylesheet" href="assets/css/pdp-v4.css?v=65">
<!-- The reveal animation hides content until it is observed, so it is scoped to
     JS being available. Without this, a JS failure would leave a blank page. -->
<script>document.documentElement.className += " js";</script>

<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
"""


def config_island(p):
    cfg = {
        "tiers": [{"min": m, "each": e} for m, e in p["tiers"]],
        "pricing": p.get("pricing", "ladder"),
        "methods": [{
            "id": m.get("id", ""), "name": m["name"], "lead": m["lead"], "cmyk": m["cmyk"],
            "colours": m["colours"], "extraColour": m.get("extra_colour", 0),
            "logoSizes": m["logo_sizes"], "sample": m.get("sample", 0),
            "ladder": [{"min": q, "each": e} for q, e in m.get("ladder", [])],
            "setup": {str(k): v for k, v in m.get("setup", {}).items()},
            "matrix": m.get("matrix"),
        } for m in p["methods"]],
        "positions": [{"name": pos[0], "slug": pos[1] if isinstance(pos[1], str) else None,
                       "methods": pos[2] if len(pos) > 2 and isinstance(pos[2], list) else None}
                      for pos in p["positions"]],
        "positionImg": ("assets/img/products/" + p["position_img"]) if p.get("position_img") else None,
        "stockBySize": p.get("stock_by_size"),
        # Savings are measured against the default branding type at the entry
        # break and stay pinned there when the type changes - which is why a
        # dearer type reads as a negative saving, exactly as the live table does.
        "baseline": baseline_each(p),
        "smallOrderUnder": SMALL_ORDER_UNDER,
        "smallOrderFee": SMALL_ORDER_FEE,
        "expressRate": p.get("express", {}).get("rate", EXPRESS_RATE),
        "expressFee": p.get("express", {}).get("fee", EXPRESS_FEE),
        "expressSaving": EXPRESS_SAVING,
        "pointsPerPound": POINTS_PER_POUND,
        "pointValue": POINT_VALUE,
        "baseLead": p["base_lead"],
        "baseShip": BASE_SHIP,
        "expressShip": EXPRESS_SHIP,
        "stock": p["stock"],
        "freeDeliveryOver": FREE_DELIVERY_OVER,
        "maxLocations": MAX_LOCATIONS,
    }
    return ('<script type="application/json" id="pdp-config">\n'
            + json.dumps(cfg, indent=2) + "\n</script>")



def gallery(p):
    first_alt = p["colours"][0][3]
    thumbs = []
    for rel, label in p["gallery"]:
        src = img_path(p, rel)
        thumbs.append(f"""            <button class="gal__thumb" type="button" aria-label="View {esc(label)}"
                    data-img="{src}" data-alt="{esc(p["name"])} — {esc(label)}">
              <img src="{src}" alt="" loading="lazy" width="360" height="360">
            </button>""")
    # First thumbnail starts selected.
    thumbs[0] = thumbs[0].replace('class="gal__thumb"', 'class="gal__thumb is-on"', 1)
    thumbs[0] = thumbs[0].replace("<button", '<button aria-current="true"', 1)
    flag_icon, flag_text = p["flag"]
    return f"""        <!-- Gallery -->
        <div class="gal">
          <div class="gal__stage">
            <span class="prod__flag">{icon(flag_icon, 17)}{esc(flag_text)}</span>
            <img id="gal-main" src="{img_path(p, p["gallery"][0][0])}"
                 alt="{esc(first_alt)}" width="360" height="360">
          </div>
          <div class="gal__thumbs" role="group" aria-label="Product images">
{chr(10).join(thumbs)}
          </div>
        </div>"""


def swatches(p):
    rows = []
    for i, col in enumerate(p["colours"]):
        name, hex_, rel, alt = col[:4]
        code = col[4] if len(col) > 4 else ""
        on = ' is-on' if i == 0 else ''
        checked = 'true' if i == 0 else 'false'
        rows.append(f"""            <button class="sw{on}" type="button" role="radio" aria-checked="{checked}"
                    data-img="{img_path(p, rel)}" data-name="{esc(name)}" data-alt="{esc(alt)}" data-code="{code}">
              <span class="sw__dot" style="--sw:{hex_}"></span><span class="sw__name">{esc(name)}</span>
            </button>""")
    return f"""            <fieldset class="opt">
              <legend class="opt__t">Product colour <span class="opt__val" id="colour-val">{esc(p["colours"][0][0])}</span></legend>
              <div class="sw-row" role="radiogroup" aria-label="Product colour">
{chr(10).join(rows)}
              </div>
            </fieldset>"""


def size_grid(p):
    """The live "configure your product below" grid: one row per size for the
    chosen colour, with its stock level and a quantity field. Laid out two-up
    with narrow, three-digit columns so it takes little height."""
    c0 = p["colours"][0]
    code0 = c0[4]
    stock = p["stock_by_size"][code0]
    rows = []
    for sz in p["sizes"]:
        n = stock.get(sz, 0)
        rows.append(f"""                <div class="cfg__row" data-size="{sz}">
                  <span class="cfg__size">{sz}</span>
                  <span class="cfg__stock" data-role="stock" title="In stock">{n}</span>
                  <input class="cfg__qty" type="number" min="0" max="{n}" step="1" inputmode="numeric"
                         placeholder="Qty" aria-label="Quantity, size {sz}" data-size="{sz}">
                </div>""")
    return f"""
            <div class="cfg" id="cfg">
              <div class="cfg__head">
                <h2 class="cfg__t">Configure your product below</h2>
                <span class="cfg__col" data-role="colour">{esc(c0[0])}</span>
              </div>
              <p class="cfg__legend" aria-hidden="true"><span>Size</span><span>Stock</span><span>Qty required</span></p>
              <div class="cfg__rows" role="group" aria-label="Quantity by size: size, stock level, quantity required">
{chr(10).join(rows)}
              </div>
              <p class="cfg__sum">Total <b id="cfg-total">0</b> units &middot; <span id="cfg-stock">&mdash;</span> in stock in this colour</p>
            </div>"""


def size_picker(p):
    if not p["sizes"]:
        return ""
    if p.get("stock_by_size"):
        return size_grid(p)
    rows = []
    for i, s in enumerate(p["sizes"]):
        on = ' is-on' if i == 2 else ''          # L is the modal size
        checked = 'true' if i == 2 else 'false'
        rows.append(f'                <button class="size{on}" type="button" role="radio" '
                    f'aria-checked="{checked}" data-name="{s}">{s}</button>')
    return f"""
            <fieldset class="opt opt--aside">
              <legend class="opt__t">Size <span class="opt__val" id="size-val">{p["sizes"][2]}</span></legend>
              <a class="opt__link" href="#t-size">Size guide</a>
              <div class="size-row" role="radiogroup" aria-label="Size">
{chr(10).join(rows)}
              </div>
            </fieldset>"""


def area_picker(p):
    """The live site picks branding positions from a strip of thumbnails with the
    print zone drawn on the garment, not from a dropdown, and a toggle switches
    the strip between one position and several."""
    thumb = img_path(p, p["colours"][0][2])
    code0 = p["colours"][0][4] if len(p["colours"][0]) > 4 else None
    cards = []
    for i, pos in enumerate(p["positions"]):
        label = pos[0]
        on = " is-on" if i == 0 else ""
        if p.get("position_img"):
            # Supplier image with the zone already marked; swapped per colourway.
            src = "assets/img/products/" + p["position_img"].format(code=code0, pos=pos[1])
            media = f"""                  <span class="area__media">
                    <img class="area__img area__img--pos" src="{src}" alt="" loading="lazy" width="500" height="500" data-pos="{pos[1]}">
                  </span>"""
        else:
            _l, x, y, w, h = pos
            media = f"""                  <span class="area__media">
                    <img class="area__img" src="{thumb}" alt="" loading="lazy" width="360" height="360">
                    <span class="area__box" style="--x:{x}%;--y:{y}%;--w:{w}%;--h:{h}%"></span>
                  </span>"""
        cards.append(f"""                <button class="area{on}" type="button" aria-pressed="{'true' if i == 0 else 'false'}"
                        data-area="{esc(label)}" data-i="{i}">
{media}
                  <span class="area__name">{esc(label)}</span>
                  <span class="area__tick" aria-hidden="true">{icon("i-check", 15)}</span>
                </button>""")
    return f"""            <fieldset class="opt areas" aria-labelledby="areas-t">
              <div class="areas__head">
                <span class="opt__t" id="areas-t">Branding location</span>
                <label class="toggle">
                  <input type="checkbox" id="multi-location">
                  <span class="toggle__track" aria-hidden="true"></span>
                  <span class="toggle__lbl">Multiple branding location</span>
                </label>
              </div>
              <div class="areas__strip" role="group" aria-label="Branding location"
                   tabindex="0" aria-describedby="areas-help">
{chr(10).join(cards)}
              </div>
              <p class="areas__help" id="areas-help">Choose where the logo goes. Turn on multiple
              branding to print more than one position &mdash; setup is charged per position.</p>
            </fieldset>"""


# --------------------------------------------------------------------------
# Pricing, shared with the calculator so the pre-rendered table and the live
# one can never disagree.
# --------------------------------------------------------------------------

def tier_each(ladder, n):
    """Per-unit price at quantity n from a (min, each) ladder."""
    each = ladder[0][1]
    for mn, e in ladder:
        if n >= mn:
            each = e
    return each


def matrix_each(m, colours, n):
    """Branding price each from a (qtys x colour-count) matrix, at quantity n."""
    mx = m["matrix"]
    cols = m["colours"] or [1]
    ci = max(0, cols.index(colours)) if colours in cols else 0
    row = mx["rows"][0]
    for q, r in zip(mx["qtys"], mx["rows"]):
        if n >= q:
            row = r
    return row[ci] if ci < len(row) else row[-1]


def setup_for(m, colours):
    st = m.get("setup", {})
    if not st:
        return 0.0
    return st.get(colours, st.get(1, list(st.values())[0]))


def unit_price(p, method, colours, n):
    """All-in price each (product + branding) at quantity n."""
    if p.get("pricing") == "matrix":
        return tier_each(p["tiers"], n) + matrix_each(method, colours, n)
    return tier_each(method["ladder"], n) + max(0, colours - 1) * method.get("extra_colour", 0)


def sample_each(p, method):
    """The single pre-production unit."""
    if p.get("pricing") == "matrix":
        return tier_each(p["tiers"], 1) + matrix_each(method, (method["colours"] or [1])[0], 1)
    return method.get("sample", 0)


def baseline_each(p):
    """What savings are measured against: the default type at the entry break."""
    if not p["methods"]:
        return 0
    m0 = p["methods"][0]
    c0 = (m0["colours"] or [1])[0]
    return round(unit_price(p, m0, c0, p["breaks"][1] if p.get("breaks") else p["min_qty"]), 2)


def order_value(p, method, colours, n):
    """Product + branding for one location, before setup, surcharge and express."""
    return unit_price(p, method, colours, n) * n


def small_order(value):
    return SMALL_ORDER_FEE if value < SMALL_ORDER_UNDER else 0.0


# --------------------------------------------------------------------------
# Blocks
# --------------------------------------------------------------------------

def location_block(p):
    """Configuration for one chosen branding position.

    Tile groups, as on the live site. Every branding type's colour counts and
    logo sizes are rendered up front; the script shows only the tiles the
    chosen type offers, so switching type never has to build controls.
    """
    thumb = img_path(p, p["colours"][0][2])
    methods = p["methods"]
    all_colours = sorted({c for m in methods for c in m["colours"]})
    all_sizes = sorted({sz for m in methods for sz in m["logo_sizes"]})
    m0 = methods[0]

    types = []
    for i, m in enumerate(methods):
        on = " is-on" if i == 0 else ""
        types.append(f"""                    <button class="tile{on}" type="button" role="radio" aria-checked="{'true' if i == 0 else 'false'}"
                            data-role="type" data-method="{i}" data-id="{esc(m.get("id", ""))}">{esc(m["name"])}{TICK}</button>""")

    colours = []
    for n in all_colours:
        allowed = n in m0["colours"]
        on = " is-on" if allowed and n == m0["colours"][0] else ""
        colours.append(f"""                    <button class="tile tile--num{on}" type="button" role="radio" aria-checked="{'true' if on else 'false'}"
                            data-role="colours" data-value="{n}"{'' if allowed else ' hidden'}>{n}{TICK}</button>""")

    sizes = []
    for cm in all_sizes:
        allowed = cm in m0["logo_sizes"]
        on = " is-on" if allowed and cm == m0["logo_sizes"][0] else ""
        sizes.append(f"""                    <button class="tile tile--num{on}" type="button" role="radio" aria-checked="{'true' if on else 'false'}"
                            data-role="logo" data-value="{cm}"{'' if allowed else ' hidden'}>{cm}{TICK}</button>""")

    return f"""              <fieldset class="loc">
                <div class="loc__head">
                  <img class="loc__thumb" src="{thumb}" alt="" width="120" height="120" loading="lazy">
                  <span class="loc__n" data-role="n">Branding location 1</span>
                  <button class="loc__rm" type="button" data-role="remove" hidden>Remove this location</button>
                </div>

                <div class="tiles">
                  <span class="tiles__t">Branding type <b class="req" aria-hidden="true">*</b></span>
                  <div class="tiles__row tiles__row--wide" role="radiogroup" aria-label="Branding type" aria-required="true">
{chr(10).join(types)}
                  </div>
                </div>

                <div class="tiles" data-role="colours-field"{'' if m0["colours"] else ' hidden'}>
                  <span class="tiles__t">Number of colours <b class="req" aria-hidden="true">*</b></span>
                  <div class="tiles__row" role="radiogroup" aria-label="Number of colours" aria-required="true">
{chr(10).join(colours)}
                  </div>
                </div>

                <!-- Digital methods print in process colour, so the live site swaps
                     the colour count for a single confirming tile. -->
                <div class="tiles" data-role="cmyk-field"{'' if m0["cmyk"] else ' hidden'}>
                  <span class="tiles__t">CMYK</span>
                  <div class="tiles__row">
                    <span class="tile tile--num is-on tile--static">Yes{TICK}</span>
                  </div>
                </div>

                <div class="tiles" data-role="logo-field"{'' if m0["logo_sizes"] else ' hidden'}>
                  <span class="tiles__t">Choose logo size (cm&sup2;)</span>
                  <div class="tiles__row" role="radiogroup" aria-label="Logo size in square centimetres">
{chr(10).join(sizes)}
                  </div>
                </div>
              </fieldset>"""


def breaks_table(p):
    """Quantity price breaks as a selectable list: quantity, saving against the
    baseline, per-unit price, subtotal, and an artwork upload per row, with the
    deeper breaks behind "show more" - as the live table is laid out.

    Rows are pre-filled for the default configuration (one position, the
    first branding type, one colour) using the same arithmetic the calculator
    applies, so with JS off the table is a real price list.
    """
    m0 = p["methods"][0]
    c0 = m0["colours"][0] if m0["colours"] else 1
    baseline = baseline_each(p)
    setup0 = setup_for(m0, c0)

    def row(n, sample=False):
        each = sample_each(p, m0) if sample else unit_price(p, m0, c0, n)
        value = each * (1 if sample else n)
        sub = value + setup0 + small_order(value)
        return each, sub

    s_each, s_sub = row(1, sample=True)
    rows = [f"""                  <tr data-qty="1" class="break break--sample">
                    <td><input type="radio" name="qty-break" id="break-sample" value="1"></td>
                    <th scope="row"><label for="break-sample">1</label></th>
                    <td class="break__save">Pre-production</td>
                    <td class="break__each" data-role="each">{money(s_each)}</td>
                    <td class="break__sub" data-role="sub">{money(s_sub)}</td>
                    <td><button class="break__up" type="button" aria-label="Upload artwork for 1 unit">{icon("i-transfer", 16)}</button></td>
                  </tr>"""]

    qtys = [q for q in p.get("breaks", [t for t, _ in p["tiers"]]) if q > 1]
    for i, mn in enumerate(qtys):
        each, sub = row(mn)
        pct = (1 - each / baseline) * 100 if baseline else 0
        checked = " checked" if i == 0 else ""
        on = " is-on" if i == 0 else ""
        more = " break--more" if i >= BREAKS_SHOWN else ""
        hidden = " hidden" if i >= BREAKS_SHOWN else ""
        rows.append(f"""                  <tr data-qty="{mn}" class="break{on}{more}"{hidden}>
                    <td><input type="radio" name="qty-break" id="break-{mn}" value="{mn}"{checked}></td>
                    <th scope="row"><label for="break-{mn}">{mn:,}</label></th>
                    <td class="break__save" data-role="save">Save {pct:.2f}%</td>
                    <td class="break__each" data-role="each">{money(each)}</td>
                    <td class="break__sub" data-role="sub">{money(sub)}</td>
                    <td><button class="break__up" type="button" aria-label="Upload artwork for {mn:,} units">{icon("i-transfer", 16)}</button></td>
                  </tr>""")

    hidden_count = max(0, len(qtys) - BREAKS_SHOWN)
    more_btn = "" if not hidden_count else f"""
              <button class="breaks__more" type="button" id="breaks-more" aria-expanded="false" aria-controls="breaks">
                Show more price breaks <span aria-hidden="true">+</span>
              </button>"""

    return f"""            <div class="breaks" id="breaks">
              <h2 class="breaks__t">Quantity price breaks</h2>
              <div class="breaks__scroll" role="region" aria-label="Quantity price breaks" tabindex="0">
                <table class="breaks__table">
                  <caption class="vh">Choose a quantity. Prices reflect the branding you have configured.</caption>
                  <thead>
                    <tr>
                      <th scope="col"><span class="vh">Select</span></th>
                      <th scope="col">Quantity</th>
                      <th scope="col">Saving</th>
                      <th scope="col">Price</th>
                      <th scope="col">Subtotal</th>
                      <th scope="col"><span class="vh">Artwork</span></th>
                    </tr>
                  </thead>
                  <tbody>
{chr(10).join(rows)}
                  </tbody>
                </table>
              </div>{more_btn}
              <p class="breaks__note">Price is per unit for the branding you have configured. Subtotals
              include setup, exclude VAT, and carry a {money(SMALL_ORDER_FEE)} small-order charge on
              orders under {money(SMALL_ORDER_UNDER)}. Saving is measured against
              {esc(m0["name"]).lower()} at {qtys[0]} units. The pre-production line is a single
              branded sample.</p>
            </div>"""


def quote_box(p):
    """The live bespoke-quote buy box: code, price, tagline, an inline quote
    form with quantity and artwork upload, wishlist, and the lead times."""
    return f"""        <!-- Buy box: bespoke quote -->
        <div class="buy">
          <div class="buy__top">
            <p class="buy__sku">Product code <b>{esc(p["sku"])}</b></p>
            <ul class="share" aria-label="Share this product">
              <li><a href="#" aria-label="Share on Pinterest">{icon("i-pinterest", 16)}</a></li>
              <li><a href="#" aria-label="Share on X">{icon("i-x", 15)}</a></li>
              <li><a href="#" aria-label="Share on Facebook">{icon("i-facebook", 16)}</a></li>
              <li><a href="#" aria-label="Share">{icon("i-share", 16)}</a></li>
            </ul>
          </div>
          <h1 id="p-h">{esc(p["name"])}</h1>
          <p class="buy__rate">{icon("i-star", 15)}<b>{p["rating"]}</b> <span>({p["reviews"]} reviews)</span> &middot; <span>{p["customers"]} happy customers</span></p>

          <div class="buy__price">
            <b>{money(p["tiers"][0][1])}</b>
            <span class="buy__unit">Ex VAT</span>
          </div>
          <p class="buy__tag">{esc(p["tagline"])}</p>
          <p class="buy__lede">{esc(p["lede"])}</p>

          <form class="qform" onsubmit="return false;" aria-labelledby="qform-t">
            <h2 class="qform__t" id="qform-t">Get a quote for this product</h2>
            <div class="qmodal__grid">
              <label class="qfield">
                <span class="qfield__t">Full name <b class="req" aria-hidden="true">*</b></span>
                <input type="text" name="name" autocomplete="name" required>
              </label>
              <label class="qfield">
                <span class="qfield__t">Email address <b class="req" aria-hidden="true">*</b></span>
                <input type="email" name="email" autocomplete="email" required>
              </label>
              <label class="qfield qfield--wide">
                <span class="qfield__t">Company name</span>
                <input type="text" name="company" autocomplete="organization">
              </label>
            </div>

            <div class="qform__row">
              <div class="qfield">
                <span class="qfield__t" id="qq-lbl">Please type the quantity you need</span>
                <div class="qty">
                  <button class="qty__btn" type="button" data-step="down" aria-label="Decrease quantity">&minus;</button>
                  <input type="number" id="qty-quote" value="{p["min_qty"]}" min="1" step="1" inputmode="numeric" aria-labelledby="qq-lbl">
                  <button class="qty__btn" type="button" data-step="up" aria-label="Increase quantity">&plus;</button>
                </div>
              </div>
              <label class="qfield qfield--file">
                <span class="qfield__t">Please upload artwork for a visual</span>
                <span class="qform__drop">
                  <input type="file" name="artwork" accept=".ai,.eps,.pdf,.png,.jpg,.jpeg,.svg">
                  <span>{icon("i-transfer", 16)}Click or drag a file here to upload</span>
                </span>
              </label>
            </div>

            <div class="acts">
              <button class="btn btn--solid" type="submit">Submit for a quote {icon("i-arrow", 18)}</button>
              <button class="btn btn--outline wishlist" type="button">{icon("i-heart", 17)}Add to wishlist</button>
            </div>
          </form>

        </div>"""


def buy_box(p):
    if p.get("mode") == "quote":
        return quote_box(p)
    loc = location_block(p)

    return f"""        <!-- Buy box -->
        <div class="buy">
          <div class="buy__top">
            <p class="buy__sku">SKU <b>{esc(p["sku"])}</b> &middot; <span class="buy__stock">{icon("i-check", 14)}In stock</span></p>
            <ul class="share" aria-label="Share this product">
              <li><a href="#" aria-label="Share on Pinterest">{icon("i-pinterest", 16)}</a></li>
              <li><a href="#" aria-label="Share on X">{icon("i-x", 15)}</a></li>
              <li><a href="#" aria-label="Share on Facebook">{icon("i-facebook", 16)}</a></li>
              <li><a href="#" aria-label="Share">{icon("i-share", 16)}</a></li>
            </ul>
          </div>
          <h1 id="p-h">{esc(p["name"])}</h1>
          <p class="buy__rate">{icon("i-star", 15)}<b>{p["rating"]}</b> <span>({p["reviews"]} reviews)</span> &middot; <span>{p["customers"]} happy customers</span></p>

          <p class="buy__lede">{esc(p["lede"])}</p>

          <!-- The headline is the published from-price, unprinted, exactly as the
               counter quotes it. The configured price lives in the breakdown below,
               so the two are never confused for one another. -->
          <div class="buy__price">
            <span class="buy__from">From</span>
            <b>{money(p["tiers"][0][1])}</b>
            <span class="buy__unit">per unit, unprinted &middot; minimum {p["min_qty"]}</span>
          </div>

          <form class="buy__form" onsubmit="return false;">
{swatches(p)}{size_picker(p)}

{area_picker(p)}

            <!-- One configuration panel per chosen position, cloned from the
                 template as positions are picked in the strip above. -->
            <div class="locs" id="locations">
{loc}
            </div>
            <template id="loc-tpl">
{loc}
            </template>

{breaks_table(p)}

            <!-- Quantity. The slider runs from the minimum to the available
                 stock and the badge above the thumb reads out the value; the
                 price-break rows and the stepper beside the cart button move
                 the same figure. -->
            <div class="qrange"{" hidden" if p.get("stock_by_size") else ""}>
              <span class="qrange__t">Or any other quantity</span>
              <output class="qrange__val" for="qty-range" id="qty-badge">{p["min_qty"]}</output>
              <input type="range" id="qty-range" value="{p["min_qty"]}" min="{p["min_qty"]}" max="{p["stock"]}"
                     step="1" aria-label="Quantity">
              <div class="qrange__ends" aria-hidden="true">
                <span>Minimum<br>quantity</span>
                <span>Max available<br>stock</span>
              </div>
            </div>

            <!-- Summary, laid out as the live panel: order status and price on
                 the left, rewards and the account prompt on the right. -->
            <div class="summary">
              <div class="summary__main">
                <p class="summary__free" id="c-free-delivery">&mdash;</p>

                <label class="summary__gate">
                  <input type="checkbox" id="uk-mainland" aria-describedby="uk-mainland-note">
                  <span>I can confirm delivery is to the UK mainland</span>
                </label>
                <p class="summary__gatenote" id="uk-mainland-note">Checkout is mainland UK only. Anywhere
                else, or more than one address, needs a quote.</p>
                <p class="gate__err" id="uk-mainland-error" role="alert" hidden>
                  {icon("i-close", 15)}<span>Please confirm delivery is to mainland UK. Checkout covers a
                  single mainland UK address; for anywhere else, or more than one address,
                  <button class="linkbtn" type="button" data-opens="quote-modal">request a formal quote</button>
                  and the team will come back with shipping costs.</span>
                </p>

                <p class="summary__lbl">Updated price with configuration:</p>
                <p class="summary__price">
                  <b id="c-total">&mdash;</b>
                  <span class="summary__vat" id="c-vat-lbl">Ex VAT</span>
                  <button class="summary__info" type="button" aria-expanded="false" aria-controls="breakdown"
                          aria-label="Show the price breakdown">i</button>
                </p>
                <p class="summary__sub"><span id="c-total-note">&mdash;</span> &middot; <span id="c-perunit">&mdash;</span></p>

                <div class="calc" id="breakdown" hidden>
                  <ul class="calc__rows">
                    <li><span class="calc__k">Product cost</span><span class="calc__v" id="c-product">&mdash;</span></li>
                    <li><span class="calc__k">Branding cost</span><span class="calc__v" id="c-branding">&mdash;</span></li>
                    <li><span class="calc__k">Setup cost<span class="calc__note" id="c-setup-note">Included in the branded price</span></span><span class="calc__v" id="c-setup">&mdash;</span></li>
                    <li><span class="calc__k">Surcharges<span class="calc__note">{money(SMALL_ORDER_FEE)} small-order charge on orders under {money(SMALL_ORDER_UNDER)}</span></span><span class="calc__v" id="c-surcharge">&mdash;</span></li>
                    <li><span class="calc__k">Express</span><span class="calc__v" id="c-express">&mdash;</span></li>
                  </ul>
                </div>

                <label class="toggle">
                  <input type="checkbox" id="vat-toggle">
                  <span class="toggle__track" aria-hidden="true"></span>
                  <span class="toggle__lbl">Show price with VAT</span>
                </label>
                <label class="toggle">
                  <input type="checkbox" id="express">
                  <span class="toggle__track" aria-hidden="true"></span>
                  <span class="toggle__lbl">Express production <small>cuts {EXPRESS_SAVING} working days, {express_copy(p)}</small></span>
                </label>
              </div>

              <div class="summary__side">
                <p class="summary__pts">{icon("i-star", 18)}<span>Earn <b id="c-points">&mdash;</b>!</span></p>
                <p class="summary__ptsnote">Your points equal <b id="c-points-gbp">&mdash;</b>, redeemable
                off your next order.</p>
                <p class="summary__stock">Order now to secure the stock</p>
                <a class="summary__signup" href="#">
                  <span>Haven't got an account with us?</span>
                  <b>Sign up today</b>
                  <span>Start earning rewards</span>
                </a>
              </div>
            </div>

            <div class="acts">
              <button class="btn btn--outline" type="button" id="quote-open">Email a quote</button>
              <button class="btn btn--outline wishlist" type="button">{icon("i-heart", 17)}Add to wishlist</button>
            </div>
            <div class="acts acts--cart">
              <div class="qty"{" hidden" if p.get("stock_by_size") else ""}>
                <button class="qty__btn" type="button" data-step="down" aria-label="Decrease quantity">&minus;</button>
                <input type="number" id="qty" value="{p["min_qty"]}" min="{p["min_qty"]}" max="{p["stock"]}"
                       step="{p["step"]}" inputmode="numeric" aria-label="Quantity">
                <button class="qty__btn" type="button" data-step="up" aria-label="Increase quantity">&plus;</button>
              </div>
              <button class="btn btn--outline" type="button">Order a sample</button>
              <button class="btn btn--solid" type="submit" id="add-to-cart">Add to cart</button>
            </div>
{esg(p)}

          </form>

          <!-- Get a quote. A popup on the live site, opened from "Email a quote"
               and from the mainland-UK error; the three fields the team needs
               before they can price anything. -->
          <dialog class="qmodal" id="quote-modal" aria-labelledby="qmodal-t">
            <form class="qmodal__form" method="dialog">
              <div class="qmodal__head">
                <h2 class="qmodal__t" id="qmodal-t">Get a quote</h2>
                <button class="qmodal__x" type="submit" value="close" formnovalidate aria-label="Close">
                  {icon("i-close", 18)}
                </button>
              </div>

              <p class="qmodal__sku">Quoting on <b>{esc(p["name"])}</b> &middot; SKU {esc(p["sku"])}</p>

              <div class="qmodal__grid">
                <label class="qfield qfield--wide">
                  <span class="qfield__t">Full name <b class="req" aria-hidden="true">*</b></span>
                  <input type="text" name="name" autocomplete="name" required>
                </label>
                <label class="qfield">
                  <span class="qfield__t">Email address <b class="req" aria-hidden="true">*</b></span>
                  <input type="email" name="email" autocomplete="email" required>
                </label>
                <label class="qfield">
                  <span class="qfield__t">Phone number <b class="req" aria-hidden="true">*</b></span>
                  <input type="tel" name="phone" autocomplete="tel" required>
                </label>
              </div>

              <div class="qmodal__opts">
                <label class="qopt"><input type="checkbox" name="pricebreaks" checked> Include price breaks for different quantities</label>
                <label class="qopt"><input type="checkbox" name="mockup"> Send me a mock up proof</label>
                <label class="qopt"><input type="checkbox" name="vat"> Send me costs including VAT</label>
              </div>

              <div class="qmodal__cta">
                <button class="btn btn--solid" type="submit" value="send">Submit for a quote {icon("i-arrow", 18)}</button>
                <button class="btn btn--outline" type="submit" value="close" formnovalidate>Cancel</button>
              </div>
            </form>
          </dialog>

        </div>"""


# --------------------------------------------------------------------------
# Branding guides - the right-hand accordion on the live product page. Copy is
# the live site's, tidied for punctuation and case; the substance is theirs.
# --------------------------------------------------------------------------

BRANDING_GUIDES = [
    ("Promotional products branding types", [
        "Printing your promotional merchandise should be simple. Below are the corporate "
        "branding options, so you can choose the best branding method for your swag.",
    ], ["promotional-products-uk.jpg", "promotional-products-bounce.jpg"]),
    ("What is screen printing", [
        "Screen printing is the process of pressing ink through a stencilled mesh screen to "
        "create a printed design. It is also known as silk screening, silkscreen printing, or "
        "sometimes textile printing.",
        "Screen printing allows us to mix your exact brand Pantone colours to print onto the "
        "product - also known as spot colours. When you select screen printing you will be "
        "asked for your brand's Pantone references so the correct ink is mixed.",
        "The colours are vivid and rich and the prints are very durable. For the best results, "
        "screen print simple designs that do not have too many details or colours.",
    ], ["what-is-screen-printing.png"]),
    ("What is pad printing", [
        "Pad printing transfers a 2-D image onto a 3-D object - think of it as a design stamped "
        "onto the product. It works on curved and uneven surfaces and on products of all shapes "
        "and sizes, so it suits small, irregular and fragile items.",
        "The limitation is that the print cannot be large or wrap around a product. Each item is "
        "printed one at a time and each colour is a separate pass, so production takes longer "
        "the more colours you print.",
        "Pad printing uses your exact Pantone colours, and you will be asked for them when you "
        "select it. It prints onto almost any material - metal, plastic, glass, even sweets.",
    ]),
    ("What is transfer printing", [
        "Transfer printing first prints the design onto paper, then transfers it to the textile "
        "or product in a separate process, usually with a heat press. The finish is very crisp, "
        "and once transferred and fired the image is permanent.",
        "Transfer printing mixes your exact Pantone colours, so you will be asked for them. There "
        "is a limit to how many colours can be matched this way, and the process costs more than "
        "screen printing.",
        "If the product needs this method and the artwork is complex, a digital transfer is often "
        "the better choice: full colour generated from the digital artwork and then transferred.",
    ]),
    ("What is digital printing", [
        "Digital printing prints digital-based images directly onto a variety of products, "
        "materials and garments. It is the choice for full colour artwork - logos with multiple "
        "colours, shades and gradients.",
        "Turnaround is quick because there are no Pantone inks to mix: digital print uses CMYK "
        "to generate colour. When you select it you will not be asked for Pantone references. It "
        "is also labelled full colour printing when you filter our products.",
        "A loud, colourful design can only be done as a digital print - also called full colour "
        "or four colour process CMYK.",
    ]),
    ("What is CMYK", [
        "CMYK stands for cyan, magenta, yellow and black: the four colours used when branding "
        "anything full colour or digitally printed. If you choose digital print, digital transfer "
        "or full colour, CMYK is the process.",
        "Digital artwork is usually created in RGB for screens. To print it, it needs to be "
        "converted to CMYK. A good designer saves both - one for screen, one for print.",
    ]),
    ("What is wrap and 360", [
        "Wrap and 360 means branding that goes all the way around a product such as a bottle, "
        "mug or football. The options are usually screen print or digital only.",
        "A screen printed wrap is typically limited to one colour - a single spot or Pantone. "
        "The alternative is a digital wrap or digital 360 in full colour.",
        "Digital printing has come a long way, and personalised 360 print is now a popular choice "
        "because it lets you print on every side of the product.",
    ]),
    ("What is laser engraving", [
        "Laser engraving uses a laser to mark products made of metal, glass, wood, bamboo and "
        "even cork. The beam acts as a chisel, leaving a permanent, deep mark.",
        "It is subtle yet effective and harder-wearing than most print techniques, so your logo "
        "lasts a lot longer - if not forever. How large we can engrave depends entirely on the "
        "product; some have a small engraving area, others can be engraved all the way round.",
        "Engraving normally takes one working day, so it is a strong option on a tight deadline. "
        "You will not be asked for Pantone colours.",
    ]),
    ("What is debossing", [
        "Debossing presses your logo into the material, leaving a permanent indentation of the "
        "artwork. It is best on thicker materials - leather, suede, PU or rubber - and gives a "
        "subtle, premium, hard-wearing finish on notebooks, portfolios and laptop cases.",
        "It is not the quickest method: once your order and artwork are confirmed we have to "
        "order a debossing block unique to your design, so you may not find it offered on "
        "express items. No Pantone colours are needed.",
    ]),
    ("Artwork guidelines", [
        "At the checkout you will be prompted to upload artwork. All artwork should be an "
        "editable file - AI, EPS or PDF. High quality PNG or JPEG files are also accepted; if "
        "you send a JPEG we will convert it to the correct format and send a proof.",
        "No order goes straight to production. Our in-house designers check your artwork and "
        "send a proof for approval first. If you do not know your Pantone colours, select "
        "\"I don't know\" and we will match the closest and send a proof.",
        "How many colours is my artwork? Count every colour, including whites and blacks. Blue "
        "and white is two colours; white alone is one. If your artwork has many overlapping "
        "colours and shades, choose digital print where it is offered.",
    ]),
]

ABOUT_US = {
    "intro": (
        "Bounce Creative Designs, a leading UK promotional products supplier, offers tailored "
        "solutions to help your business thrive across several key areas."
    ),
    "growth": [
        ("Increase customer retention",
         "Thoughtful, branded items that keep your brand top of mind and encourage repeat business."),
        ("Generate qualified leads",
         "Creative, eye-catching products that attract people genuinely interested in what you offer."),
        ("Improve employee onboarding",
         "Welcome kits and branded merchandise that make new hires feel valued from day one."),
        ("Boost event attendance",
         "Memorable giveaways that lift an event's appeal and encourage active participation."),
        ("Reward customer loyalty",
         "Exclusive branded gifts that show appreciation and reward continued support."),
        ("Build employer branding",
         "Quality products that reflect your values and your commitment to your people."),
    ],
    "industries": [
        "Construction", "Universities", "Tech start-ups", "Pharmaceutical", "Sports clubs",
        "Hospitality", "Healthcare", "Recruitment agencies", "Financial services",
    ],
}


def paras(items, indent=12):
    pad = " " * indent
    return chr(10).join(f"{pad}<p>{esc(x)}</p>" for x in items)


MATRIX_ROWS = [1, 50, 100, 250, 500, 1000, 2500]


def branding_matrix(p, m):
    """Branding price each, by quantity and colour count, for one branding type.
    Uses the live matrix where we have it; otherwise derives it from the type's
    ladder against the unprinted price, so it agrees with the calculator."""
    cols = m["colours"] or [1]
    if m.get("matrix"):
        rows = []
        for r in m["matrix"]["rows"]:
            step = (r[-1] - r[0]) / (len(r) - 1) if len(r) > 1 else 0
            rows.append([round(r[i], 2) if i < len(r) else round(r[-1] + step * (i - len(r) + 1), 2)
                         for i in range(len(cols))])
        return {"qtys": m["matrix"]["qtys"], "cols": cols, "rows": rows}
    qtys = [q for q in MATRIX_ROWS if q == 1 or q >= p["min_qty"]]
    rows = []
    for q in qtys:
        if q == 1:
            base = m.get("sample", 0) - p["tiers"][0][1]
        else:
            base = tier_each(m["ladder"], q) - tier_each(p["tiers"], q)
        rows.append([round(base + (c - 1) * m.get("extra_colour", 0), 2) for c in cols])
    return {"qtys": qtys, "cols": cols, "rows": rows}


def matrix_tabs(p):
    """The branding-type sub-tabs under the description, each holding its
    price-each matrix - laid out as the live description tab is."""
    chips, panels = [], []
    for i, m in enumerate(p["methods"]):
        key = f"mx-{i}"
        chips.append(f'            <button class="chip chip--sub" role="tab" type="button" '
                     f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="tab-{key}" id="t-{key}">{esc(m["name"])}</button>')
        mx = branding_matrix(p, m)
        if m["cmyk"]:
            heads = ['<th scope="col">Full colour<br><small>price each</small></th>']
        else:
            heads = [f'<th scope="col">{c} colour<br><small>price each</small></th>' for c in mx["cols"]]
        body = chr(10).join(
            f'                <tr><th scope="row">{q:,}</th>' + "".join(f"<td>{v:.2f}</td>" for v in row) + "</tr>"
            for q, row in zip(mx["qtys"], mx["rows"]))
        panels.append(f"""          <div class="tab tab--sub" role="tabpanel" id="tab-{key}" aria-labelledby="t-{key}"{"" if i == 0 else " hidden"}>
            <div class="mx__scroll" role="region" aria-label="{esc(m["name"])} branding prices" tabindex="0">
              <table class="mx">
                <caption class="vh">{esc(m["name"])}: branding price per unit by quantity and number of colours, excluding VAT</caption>
                <thead><tr><th scope="col">Qty</th>{"".join(heads)}</tr></thead>
                <tbody>
{body}
                </tbody>
              </table>
            </div>
          </div>""")
    return f"""        <div class="mx-tabs">
          <div class="chips chips--sub" role="tablist" aria-label="Branding type prices">
{chr(10).join(chips)}
          </div>
{chr(10).join(panels)}
        </div>"""


def esg(p):
    """The live ESG footprint: CO2 used per unit, where the supplier publishes
    it. A slim strip under the cart actions, so the buttons keep the weight."""
    if not p.get("co2_kg"):
        return ""
    return f"""            <p class="esg">
              <span class="esg__t">ESG footprint</span>
              <span class="esg__body">This product used <b>{p["co2_kg"]:.2f} kg</b> CO&#8322; carbon emissions</span>
            </p>
"""


def express_copy(p):
    ex = p.get("express", {})
    rate, fee = ex.get("rate", EXPRESS_RATE), ex.get("fee", EXPRESS_FEE)
    return f"{money(fee)} per order" if not rate else f"{money(rate)} a unit plus {money(fee)}"


def tab_panel(key, body_html, first=False):
    return f"""      <div class="tab" role="tabpanel" id="tab-{key}" aria-labelledby="t-{key}"{"" if first else " hidden"}>
{body_html}
      </div>"""


def detail(p):
    """Product detail as the live site's tab set - Description, Specification,
    (Size guide), Delivery, Reviews, Order samples, About us - in one column."""

    tabs = [("desc", "Description"), ("spec", "Specification")]
    if p.get("size_chart"):
        tabs.append(("size", "Size guide"))
    tabs += [("del", "Delivery"), ("rev", "Reviews"), ("sam", "Order samples"), ("about", "About us")]

    chips = chr(10).join(
        f'          <button class="chip" role="tab" type="button" '
        f'aria-selected="{"true" if i == 0 else "false"}" aria-controls="tab-{k}" id="t-{k}">{label}</button>'
        for i, (k, label) in enumerate(tabs))

    # ---- Description ----
    prose = chr(10).join(
        "          <div>\n            <h3>%s</h3>\n%s\n          </div>" % (esc(h), paras(ps))
        for h, ps in p["prose"])
    description = tab_panel("desc", f"""        <p class="tab__lede">Description / <b>{esc(p["name"])}</b></p>
        <p class="tab__desc">{esc(p["ld_desc"])}</p>
{paras(p.get("desc_extra", []), 8)}
{matrix_tabs(p) if p["methods"] else ""}
        <div class="prose">
{prose}
        </div>""", first=True)

    # ---- Specification ----
    spec = "        <dl class=\"spec\">\n" + chr(10).join(
        f"          <div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in p["spec"]
    ) + "\n        </dl>"
    specification = tab_panel("spec", spec)

    # ---- Size guide ----
    size_panel = ""
    if p.get("size_chart"):
        sc = p["size_chart"]
        cols = "".join(f'<th scope="col">{esc(c)}</th>' for c in sc["cols"])
        rows = chr(10).join(
            f'              <tr><th scope="row">{esc(s)}</th>' + "".join(f"<td>{esc(v)}</td>" for v in vals) + "</tr>"
            for s, vals in sc["rows"])
        size_panel = tab_panel("size", f"""        <div class="sizes__scroll" role="region" aria-label="Size chart" tabindex="0">
          <table class="sizes">
            <caption class="vh">Body measurements by size</caption>
            <thead><tr><th scope="col">Size</th>{cols}</tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <p class="tab__note">{esc(sc["note"])}</p>""")

    # ---- Delivery (live copy) ----
    delivery = tab_panel("del", f"""        <div class="prose">
          <div>
            <h3>Order online</h3>
            <p>For every item you can add to the basket and check out immediately, production time
            is {p["base_lead"]}&ndash;{p["base_lead"] + 2} working days from artwork approval and shipping
            is 2&ndash;3 working days. On ordering you receive an order confirmation, and one of the
            sales team emails a visual proof for final approval before it goes into production.</p>
            <p>What might delay production? Artwork in the wrong format can hold up the proof.
            The correct format is vectored EPS or high-resolution PDF. We usually need your brand
            Pantone colours; if you do not have them, one of the team will match the closest
            available for your approval.</p>
          </div>
          <div>
            <h3>Delivery cost</h3>
            <p>To one single mainland UK address, calculated at the checkout stage. Order values
            above &pound;{FREE_DELIVERY_OVER:,} excluding VAT are free of charge.</p>
            <p>If your address is not mainland UK, or you need more than one delivery address, you
            will need to request a quote. One of the sales team will contact you with shipping
            costs and process the order for you.</p>
          </div>
          <div>
            <h3>Bespoke quote</h3>
            <p>For a customised quote or a bespoke item, delivery can be up to 3&ndash;4 weeks
            from artwork approval depending on the item. These are clearly labelled as bespoke
            quote and are not available for immediate checkout. Let us know your deadline and
            we will tell you if we can meet it.</p>
          </div>
        </div>""")

    # ---- Reviews ----
    stars = icon("i-star", 15) * 5
    stars4 = icon("i-star", 15) * 4
    r = p["reviews"]
    five, four, three, two_, one = (round(r * .78), round(r * .17), round(r * .04),
                                    max(1, round(r * .01)), max(1, round(r * .01)))
    reviews_panel = tab_panel("rev", f"""        <div class="rev">
          <div class="rev__summary">
            <p class="rev__score"><b>{p["rating"]}</b><span>out of 5</span></p>
            <p class="rev__count">Based on <b>{r} reviews</b> of this product</p>
            <ul class="rev__bars">
              <li><span>5</span><span class="rev__bar"><i style="--pct:78%"></i></span><em>{five}</em></li>
              <li><span>4</span><span class="rev__bar"><i style="--pct:17%"></i></span><em>{four}</em></li>
              <li><span>3</span><span class="rev__bar"><i style="--pct:4%"></i></span><em>{three}</em></li>
              <li><span>2</span><span class="rev__bar"><i style="--pct:1%"></i></span><em>{two_}</em></li>
              <li><span>1</span><span class="rev__bar"><i style="--pct:1%"></i></span><em>{one}</em></li>
            </ul>
            <a href="#" class="btn btn--outline btn--sm">Write your own review</a>
          </div>
          <div class="rev__list">
{reviews(p, stars, stars4)}
          </div>
        </div>""")

    # ---- Order samples (live copy) ----
    samples = tab_panel("sam", """        <div class="prose prose--one">
          <div>
            <h3>Order samples</h3>
            <p>We always recommend ordering a sample before placing a bulk order, to ensure you are
            happy with the product and it fits your requirements. Product samples are
            non-returnable and non-refundable and are subject to a small fee plus postage and
            packing, as the sample is your business expense in deciding whether to make a bulk
            purchase.</p>
            <p>You can contact us for a branded pre-production sample if required &mdash; let us
            know what you need and we will send a bespoke quote.</p>
          </div>
        </div>""")

    # ---- About us (live copy, condensed) ----
    growth = chr(10).join(
        f"            <li><b>{esc(t)}</b><span>{esc(d)}</span></li>" for t, d in ABOUT_US["growth"])
    industries = ", ".join(esc(x) for x in ABOUT_US["industries"])
    about = tab_panel("about", f"""        <div class="prose prose--one">
          <div>
            <h3>How Bounce Creative Designs supports your business growth</h3>
            <p>{esc(ABOUT_US["intro"])}</p>
          </div>
        </div>
        <ul class="facts">
{growth}
        </ul>
        <div class="prose prose--one">
          <div>
            <h3>Across every sector</h3>
            <p>We help {industries} and more build brand visibility, foster client loyalty and
            strengthen corporate identity with promotional products tailored to how each sector
            actually works.</p>
          </div>
        </div>""")

    panels = chr(10).join(x for x in [description, specification, size_panel, delivery, reviews_panel, samples, about] if x)

    return f"""  <!-- ============ DETAIL TABS ============ -->
  <section class="sec sec--rule" aria-labelledby="detail-h">
    <div class="wrap">
      <h2 id="detail-h" class="vh">Product detail</h2>
      <div class="chiprow" data-reveal>
        <div class="chips" role="tablist" aria-label="Product detail">
{chips}
        </div>
      </div>

{panels}
    </div>
  </section>"""


REVIEW_COPY = {
    "product-hivis-v4.html": [
        (5, "Ordered 300 for a civils contract and the back print was spot on. Sizing is "
            "generous, which is what you want over a jacket.", "Dean W."),
        (5, "Second order this year. The team matched our Pantone from a JPEG and had the "
            "proof back the same afternoon.", "Sarah L."),
        (4, "Good vest for the money. Would have liked a chest pocket, but the print quality "
            "is not in question.", "Owen R."),
    ],
    "product-minsk-v4.html": [
        (5, "Bought these for an outdoor team and they get worn at weekends too, which tells "
            "you everything. Embroidery still crisp after a winter.", "Chloe M."),
        (5, "The two-fabric thing actually works — warm across the chest without the arms "
            "feeling like a duvet.", "James P."),
        (4, "Sizing runs slightly small across the shoulders with the quilting. We went one "
            "size up on the second order and it was right.", "Ruth A."),
    ],
    "product-v4.html": [
        (5, "Ordered 400 for a conference and they landed two days early. Print was crisp and "
            "the natural cotton feels heavier than the price suggests.", "Hannah E."),
        (5, "Third order of these. The visual came back the same afternoon and the colour "
            "matched our brand guide exactly.", "Marcus T."),
        (4, "Great bag for the money. Handles are long enough to wear on a shoulder, which is "
            "what we needed for a walking tour.", "Priya S."),
    ],
}


def reviews(p, stars, stars4):
    out = []
    for score, body, by in REVIEW_COPY[p["file"]]:
        s = stars if score == 5 else stars4
        out.append(f"""            <article class="rev__item">
              <p class="rev__stars" aria-label="{score} out of 5">{s}</p>
              <p class="rev__body">{esc(body)}</p>
              <p class="rev__by"><b>{esc(by)}</b> <span>Verified buyer</span></p>
            </article>""")
    return chr(10).join(out)


# The "You'll love us" reviews the live page shows in its Reviews.io carousel,
# laid out open rather than auto-scrolling. Company-level, so shared by every
# product page.
LOVED = {
    "score": "4.97", "count": 111, "word": "Excellent",
    "reviews": [
        ("Anonymous", True, 5, "Very helpful customer support and fast delivery.", "1 year ago"),
        ("Clémence Geay", False, 5, "Great service, good quality product and quick turn around.", "1 year ago"),
        ("L", False, 5, "Super service: very quick turnaround and superb quality!", "1 year ago"),
        ("Esme", True, 5,
         "Bronwyn was so helpful - we needed an urgent delivery of branded balls. This company was "
         "the easiest and quickest to provide a quote and agree the design. The delivery was right "
         "on time - everyone is…", "1 year ago"),
    ],
}


def loved(p):
    cards = []
    for name, verified, stars, body, when in LOVED["reviews"]:
        vf = f'<span class="love__vf">{icon("i-check", 13)}Verified customer</span>' if verified else ""
        cards.append(f"""        <article class="love__card">
          <p class="love__who"><b>{esc(name)}</b><span class="love__stars" aria-label="{stars} out of 5">{icon("i-star", 13) * stars}</span></p>
          {vf}
          <p class="love__body">{esc(body)}</p>
          <p class="love__when">{esc(when)}</p>
        </article>""")
    return f"""  <!-- ============ YOU'LL LOVE US ============ -->
  <section class="sec sec--band" aria-labelledby="love-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">What customers say</span>
          <h2 id="love-h">You'll <span class="hl">love us.</span></h2>
        </div>
        <p class="love__sum"><b>{LOVED["word"]}</b> <span class="love__stars" aria-hidden="true">{icon("i-star", 15) * 5}</span>
          <b>{LOVED["score"]}</b> based on <b>{LOVED["count"]}</b> reviews</p>
      </div>
      <div class="love" data-reveal>
{chr(10).join(cards)}
      </div>
    </div>
  </section>"""


def related(p):
    cards = []
    for name, rel, price, rating, count, href in p["related"]:
        cards.append(f"""        <a href="{href}" class="prod">
          <span class="prod__media"><span class="prod__flag prod__flag--best">{icon("i-star", 17)}Best seller</span><img src="assets/img/products/{rel}" alt="{esc(name)}" loading="lazy" width="360" height="360"></span>
          <span class="prod__rate">{icon("i-star", 14)}<b>{rating}</b> ({count})</span>
          <span class="prod__name">{esc(name)}</span>
          <span class="prod__price"><b>&pound;{price}</b> <small>from</small></span>
          <span class="prod__meta">
            <span>{icon("i-delivery", 14)}Tracked UK delivery</span>
            <span>{icon("i-check", 14)}Free visual in two hours</span>
          </span>
          <span class="prod__cta">Get a visual {icon("i-arrow", 15)}</span>
        </a>""")
    return f"""  <!-- ============ YOU MIGHT ALSO LIKE ============ -->
  <section class="sec" aria-labelledby="rel-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Often ordered together</span>
          <h2 id="rel-h">You might <span class="hl">also like.</span></h2>
        </div>
        <a href="{p["category_href"]}" class="btn btn--outline btn--sm">All {p["category"].lower()} {icon("i-arrow", 16)}</a>
      </div>
      <div class="rail rail--four" data-reveal>
{chr(10).join(cards)}
      </div>
    </div>
  </section>"""


def faq(p):
    """The FAQ block, carrying the live site's branding guides - the
    "what is screen printing" set - rather than invented questions."""
    items = []
    for i, entry in enumerate(BRANDING_GUIDES):
        q, ps = entry[0], entry[1]
        imgs = entry[2] if len(entry) > 2 else []
        figs = ""
        if imgs:
            figs = "\n            <div class=\"faq__imgs\">" + "".join(
                f'<img src="assets/img/branding/{f}" alt="" loading="lazy">' for f in imgs
            ) + "</div>"
        items.append(f"""          <details{" open" if i == 0 else ""}>
            <summary>{esc(q)}</summary>
{paras(ps)}{figs}
          </details>""")
    return f"""  <!-- ============ BRANDING GUIDES ============ -->
  <section class="sec" id="faq" aria-labelledby="faq-h">
    <div class="wrap">
      <div class="sechead" data-reveal>
        <span class="eyebrow">Need to know</span>
        <h2 id="faq-h">Promotional products <span class="hl">branding types.</span></h2>
      </div>
      <div class="faq" data-reveal>
{chr(10).join(items)}
      </div>
    </div>
  </section>"""

def page(p):
    return "".join([
        head(p),
        config_island(p),
        "\n",
        CHROME,
        f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol>
        <li><a href="index-v4.html">Home</a></li>
        <li><a href="{p["category_href"]}">{esc(p["category"])}</a></li>
        <li aria-current="page">{esc(p["name"])}</li>
      </ol>
    </div>
  </nav>

  <!-- ============ PRODUCT ============ -->
  <section class="sec sec--flush" aria-labelledby="p-h">
    <div class="wrap">
      <div class="pdp">

{gallery(p)}

{buy_box(p)}
      </div>
    </div>
  </section>

{detail(p)}

{loved(p)}

{related(p)}

{faq(p)}

""",
        FOOTER,
    ])


def main():
    for p in PRODUCTS:
        out = ROOT / p["file"]
        out.write_text(page(p), encoding="utf-8")
        print(f"wrote {p['file']}  ({len(out.read_text(encoding='utf-8')):,} bytes)")


if __name__ == "__main__":
    main()
