#!/usr/bin/env python3
"""Generate the category landing page(s).

Content is the live category page's, restyled in the v4 system, plus the two
sections the client asked for on category pages: a weekly-rotating top four
and the category copy with an FAQ at the bottom. Desktop layout only - this
is a design reference for estimation, not a responsive build.

    python scripts/category/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
FOOTER = (PDP / "_footer.html").read_text(encoding="utf-8").replace(
    '<script src="assets/js/pdp-v4.js?v=23"></script>',
    '<script src="assets/js/category-v4.js?v=1"></script>')


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


# --------------------------------------------------------------------------
# Content - the live /marketing-bags page
# --------------------------------------------------------------------------

BAGS = {
    "file": "category-bags-v4.html",
    "title": "Printed Bags — Branded Promotional Bags | Bounce Creative Designs",
    "meta": ("Custom printed promotional bags: tote bags, shoppers, backpacks, anti-theft, "
             "travel and sports bags. Eco-conscious materials, instant quotes for bulk orders."),
    "crumb": "Bags",
    "eyebrow": "Printed bags",
    "h1": ("Printed bags", "for your brand."),
    "lede": ("Custom printed promotional bags are mobile billboards for your brand. From classic "
             "tote bags to innovative anti-theft designs, there's a range to suit every style and "
             "purpose - with instant quotes for bulk orders."),
    "hero_img": "assets/img/categories/bags/hero-promotional-bags.png",

    # The five featured tiles at the top of the live page.
    "featured": [
        ("Anti theft bags", "tile-anti-theft.jpg"),
        ("Tote bags", "tile-tote.jpg"),
        ("Travel & leisure bags", "tile-travel-leisure.jpg"),
        ("Sports bags", "tile-sports.jpg"),
        ("rPET bags", "tile-rpet.jpg"),
    ],

    # Every sub-category the live page lists, in its groups.
    "groups": [
        ("Business bags", ["Anti theft bags", "Conference bags", "Document bags", "Laptop bags", "Exhibition bags"]),
        ("Backpacks & drawstring bags", ["Anti theft backpacks", "Backpacks", "Drawstring bags"]),
        ("Shopping bags", ["Shopper bags", "Foldable bags", "Tote bags", "Jute bags", "Canvas bags", "Paper bags", "Cotton bags", "Non woven bags"]),
        ("Travel and leisure bags", ["Beach bags", "Cooler bags", "Picnic bags", "Toiletry bags", "Suitcases & trolleys", "Waist bags", "Weekend holdalls"]),
        ("Sports bags", ["Gym bags", "Sports backpacks", "Sports duffel bags", "Sports holdalls"]),
        ("Trending", ["New bags", "Recommended", "Top 10 budget", "Top 10 picks"]),
    ],

    # "Our popular bags products" - name, price, as-low-as, order online?, image, link
    "products": [
        ("Shiny Silver or Gold Metallic Tote Bags", "1.27", "1.14", True, "bags/metallic-tote-92850.jpg", "#"),
        ("Next Day Organic Fashion Tote Bag", "5.12", None, False, "v4/organic_fashion_tote_bag_green.jpg", "#"),
        ("Next Day Heavy Organic Shopper Tote Bag", "3.66", None, False, "bags/heavy-organic-shopper-tote-bag-black.jpg", "#"),
        ("Next Day Westcove Canvas Tote", "8.41", None, False, "v4/westcove_canvas_tote_black.jpg", "#"),
        ("Next Day EarthAware® Organic Siena Tote Bag XL", "8.16", None, False, "bags/next-day-earthaware-organic-siena-tote-bag-xl-frech-navy.jpg", "#"),
        ("Next Day EarthAware® Organic Siena Tote Bag", "5.69", None, False, "bags/earthaware-organic-siena-tote-natural.jpg", "#"),
        ("Next Day Organic Festival Backpack", "6.32", None, False, "v4/organic_festival_backpack.jpg", "#"),
        ("Next Day Sling Bag For Life", "4.25", None, False, "v4/next_day_sling_bag_for_life_black.jpg", "#"),
        ("Next Day Jumbo Non Woven Exhibition Bag", "3.40", None, False, "v4/jumbo_exhibition_bag_yellow.jpg", "#"),
        ("Next Day Non Woven Bag", "3.10", None, False, "bags/next-day-non-woven-royal-blue.jpg", "#"),
        ("Next Day Coloured Cotton Shopper", "3.93", None, False, "v4/next_day_coloured_cotton_shopper_blue.jpg", "#"),
        ("Next Day Natural Cotton Shopper", "3.48", None, False, "v4/same_day_natural_cotton_shopper.jpg", "product-v4.html"),
        ("DAEGU LAP Recycled Laptop Backpack", "20.70", None, True, "bags/daegu-laptop-backpack.jpg", "#"),
        ("Impact AWARE™ Recycled Cotton Tote 145g", "1.88", None, True, "bags/impact-aware-cotton-tote.jpg", "#"),
        ("Odessa 220 g/m² Cotton Tote Bag 13L", "1.97", "1.97", True, "bags/odessa-cotton-tote.jpg", "#"),
        ("Bungalow Foldable Tote Bag 7L", "1.02", "1.02", True, "bags/bungalow-foldable-tote.jpg", "#"),
    ],

    # The five tiles at the foot of the live page.
    "more": [
        ("Laptop bags", "tile-laptop.jpg"),
        ("Luggage", "tile-luggage.jpg"),
        ("Cooler bags", "tile-beach.jpg"),
        ("Beach bags", "tile-beach.jpg"),
        ("Cosmetics bags", "tile-cosmetics.jpg"),
    ],

    # The live page's copy, verbatim, moved to the foot of the page as the
    # client's brief asks.
    "copy": [
        ("Discover the perfect promotional bags for your brand", [
            "In today's world, making a lasting impression is more important than ever - and what "
            "better way to do that than with custom printed promotional bags? Whether you're gearing "
            "up for a corporate event, a trade show, or simply want to enhance your brand's "
            "visibility in an eco-friendly way, the right bag can say a lot about your business.",
            "From classic tote bags to innovative anti-theft designs, there's a vast range of options "
            "to suit every bag style and purpose. Plus, with the growing demand for sustainability, "
            "many businesses are choosing promotional bags made from eco-conscious materials.",
        ]),
        ("Why custom printed bags?", [
            "Custom printed bags are more than just carriers - they're mobile billboards for your "
            "brand. Imagine your logo and message travelling with your customers, whether at "
            "conferences, shopping trips, or outdoor events.",
            "And thanks to our easy online ordering platform, getting your hands on these bags is now "
            "simpler than ever. Instant quotes for bulk orders mean you can plan your branding budget "
            "with confidence.",
        ]),
        ("Explore a variety of bag styles", None),   # rendered as the list below
        ("Eco and sustainable branding", [
            "Choosing eco and sustainable promotional bags doesn't just help the planet - it sends a "
            "powerful message about your company's values. Materials like jute, cotton, and canvas "
            "are biodegradable and reusable, making them a favourite for those striving to reduce "
            "plastic waste.",
        ]),
        ("Easy ordering and instant quotes", [
            "One of the best parts about ordering promotional bags with Bounce Creative Designs is how "
            "streamlined the process has become. You can browse styles, customise your design, and "
            "get instant quotes for bulk orders - all from your office or home.",
        ]),
        ("Bringing the human touch back to online ordering", [
            "At Bounce Creative Designs, we believe online orders shouldn't feel cold or impersonal. "
            "Every piece of artwork gets a thorough check by our team before anything goes into "
            "production. We provide proofs so you can see exactly how your design will look.",
            "Once your order is placed, we're here - ready to answer your calls and emails, and to "
            "handle any questions or tweaks you might want to make.",
        ]),
    ],
    "styles": [
        ("Shopping bags & tote bags", "Perfect for everyday use, these bags are versatile and roomy."),
        ("Foldable bags", "Compact and convenient, great for on-the-go customers."),
        ("Eco-friendly choices", "Jute, canvas, cotton, and non-woven bags offer sustainable options."),
        ("Business & conference bags", "Designed to hold documents, laptops, and essentials."),
        ("Anti-theft bags", "Modern security features that combine style and safety."),
        ("Travel & leisure bags", "Cooler bags, beach bags, weekend holdalls, and picnic bags."),
        ("Specialty bags", "Waist bags, toiletry bags, and exhibition bags."),
    ],

    # The FAQ the client's brief asks for at the foot of category pages. The
    # questions are the ones in their reference; answers are drawn from the
    # site's own copy and are placeholders for the client to sign off.
    "faq": [
        ("What is the most eco-friendly material for promotional bags?",
         "Jute, cotton and canvas are biodegradable and reusable, and recycled rPET carries a GRS "
         "certificate. Organic cotton certified to GOTS costs a little more and comes with the "
         "paperwork an ESG team will ask for."),
        ("Can the logo be printed on both sides?",
         "Yes. Most of our shoppers and totes have a large print area on both sides, and you choose "
         "the positions when you configure the bag. Setup is charged per position."),
        ("What is the most cost-effective option for large quantities?",
         "Screen printing. Setup is charged once per colour, so the unit cost falls quickly as the "
         "run grows - it is the best balance of quality, cost and durability for simple artwork."),
        ("What is the delivery lead time?",
         "Production is 5-7 working days from artwork approval, then 2-3 working days for tracked UK "
         "delivery. Next day lines are stocked in the UK; express production is available."),
        ("Can personalised bags be washed?",
         "Cotton and canvas bags can be machine washed at 30°C, inside out. Screen prints and "
         "embroidery hold up well; avoid tumble drying, which can crack a transfer over time."),
        ("What size of bag is most recommended?",
         "A standard 380 × 420mm shopper carries an A4 folder without straining the seams and is the "
         "most ordered size. Go larger for exhibitions and heavier loads, smaller for gift bags."),
        ("What can promotional bags be used for?",
         "Exhibitions and conference welcome packs, retail purchases, campaign giveaways, staff "
         "onboarding kits and events - anywhere a reusable bag will keep your logo in circulation."),
        ("What products can I include in a promotional bag?",
         "Notebooks, pens, drinkware, tech accessories and giveaways all pack well. Ask us about "
         "swag boxes and welcome kits if you want the bag filled and shipped as one order."),
    ],
}


# --------------------------------------------------------------------------
# Blocks
# --------------------------------------------------------------------------

def head(c):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(c["title"])}</title>
<meta name="description" content="{esc(c["meta"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=114">
<link rel="stylesheet" href="assets/css/list-v4.css?v=21">
<link rel="stylesheet" href="assets/css/category-v4.css?v=3">
<script>document.documentElement.className += " js";</script>
"""


def hero(c):
    h1a, h1b = c["h1"]
    return f"""  <!-- ============ CATEGORY HERO ============ -->
  <section class="lhero" aria-labelledby="cat-h">
    <div class="wrap">
      <div class="lhero__grid">
        <div class="lhero__copy">
          <span class="eyebrow eyebrow--onforest">{esc(c["eyebrow"])}</span>
          <h1 id="cat-h">{esc(h1a)}<br><span class="hl">{esc(h1b)}</span></h1>
          <p>{esc(c["lede"])}</p>
          <div class="lhero__cta">
            <a href="products-v4.html" class="btn btn--onforest">View all bags {icon("i-arrow", 18)}</a>
            <a href="#styles" class="btn btn--outline btn--outline-onforest">Browse by style</a>
          </div>
        </div>
        <div class="lhero__media">
          <img src="{c["hero_img"]}" alt="Promotional bags from Bounce Creative Designs" width="1200" height="896">
        </div>
      </div>
    </div>
  </section>"""


def featured(c):
    tiles = chr(10).join(f"""        <a href="#" class="ftile">
          <img src="assets/img/categories/bags/{img}" alt="" loading="lazy" width="512" height="760">
          <span class="ftile__name">{esc(name)}</span>
        </a>""" for name, img in c["featured"])
    return f"""  <!-- ============ FEATURED TYPES ============ -->
  <section class="sec" aria-labelledby="feat-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Shop by type</span>
          <h2 id="feat-h">Start with <span class="hl">the style.</span></h2>
        </div>
      </div>
      <div class="ftiles" data-reveal>
{tiles}
      </div>
    </div>
  </section>"""


def groups(c):
    cols = []
    for title, items in c["groups"]:
        li = chr(10).join(f'            <li><a href="#">{esc(x)}</a></li>' for x in items)
        trending = ' subcat--trend' if title == "Trending" else ''
        cols.append(f"""        <div class="subcat{trending}">
          <h3 class="subcat__t">{esc(title)}</h3>
          <ul class="subcat__list">
{li}
          </ul>
        </div>""")
    return f"""  <!-- ============ ALL SUB-CATEGORIES ============ -->
  <section class="sec sec--band" id="styles" aria-labelledby="styles-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Every bag we print</span>
          <h2 id="styles-h">Browse all <span class="hl">bag styles.</span></h2>
        </div>
        <span class="sticker"><b>31</b><span>sub-categories</span></span>
      </div>
      <div class="subcats" data-reveal>
{chr(10).join(cols)}
      </div>
    </div>
  </section>"""


def card(name, price, low, online, img, href):
    flag = (f'<span class="prod__flag">{icon("i-bolt", 17)}Order online</span>' if online
            else f'<span class="prod__flag prod__flag--quote">{icon("i-tag", 17)}Bespoke quote</span>')
    if low and low != price:
        price_html = f'<b>&pound;{low}</b> <small>as low as &middot; from &pound;{price}</small>'
    elif low:
        price_html = f'<b>&pound;{low}</b> <small>as low as</small>'
    else:
        price_html = f'<b>&pound;{price}</b> <small>from</small>'
    return f"""        <a href="{href}" class="prod" data-price="{low or price}">
          <span class="prod__media">{flag}<img src="assets/img/products/{img}" alt="{esc(name)}" loading="lazy" width="360" height="360"></span>
          <span class="prod__name">{esc(name)}</span>
          <span class="prod__price">{price_html}</span>
          <span class="prod__cta">{"Order online" if online else "Get a quote"} {icon("i-arrow", 15)}</span>
        </a>"""


def popular(c):
    cards = chr(10).join(card(*p) for p in c["products"])
    return f"""  <!-- ============ POPULAR PRODUCTS ============ -->
  <section class="sec" aria-labelledby="pop-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Most ordered</span>
          <h2 id="pop-h">Our popular <span class="hl">bags.</span></h2>
        </div>
        <a href="products-v4.html" class="btn btn--outline btn--sm">View all products {icon("i-arrow", 16)}</a>
      </div>
      <div class="rail rail--grid" id="product-grid" data-reveal>
{cards}
      </div>
    </div>
  </section>"""


def weekly(c):
    return """  <!-- ============ WEEKLY TOP 4 ============ -->
  <section class="sec sec--band" aria-labelledby="week-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">This week&rsquo;s picks</span>
          <h2 id="week-h">Top four, <span class="hl">refreshed weekly.</span></h2>
          <p>A different four every week, drawn at random from the range. Week
          <b id="week-no">&mdash;</b>.</p>
        </div>
      </div>
      <div class="rail rail--four" id="weekly-picks" data-reveal></div>
    </div>
  </section>"""


def more(c):
    tiles = chr(10).join(f"""        <a href="#" class="mtile">
          <img src="assets/img/categories/bags/{img}" alt="" loading="lazy" width="800" height="500">
          <span class="mtile__name">{esc(name)} {icon("i-arrow", 16)}</span>
        </a>""" for name, img in c["more"])
    return f"""  <!-- ============ MORE TO EXPLORE ============ -->
  <section class="sec" aria-labelledby="more-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">Keep looking</span>
          <h2 id="more-h">More bags <span class="hl">to explore.</span></h2>
        </div>
      </div>
      <div class="mtiles" data-reveal>
{tiles}
      </div>
    </div>
  </section>"""


def copy_block(c):
    """The live category copy as one editorial article: heading and standfirst
    pinned on the left, the sections flowing on the right, with the styles
    list set as a two-column checklist inside the flow."""
    parts = []
    intro = c["copy"][0][1][0]
    stand, rest = intro.split(" Whether", 1)
    for i, (h, ps) in enumerate(c["copy"]):
        if i == 0:
            # The heading and first sentence are already the aside; the
            # article picks up where the standfirst leaves off.
            ps = ["Whether" + rest] + ps[1:]
            h = None
        if ps is None:
            items = chr(10).join(
                f"""              <li>{icon("i-check", 16)}<span><b>{esc(t)}</b> {esc(d)}</span></li>"""
                for t, d in c["styles"])
            body = f"""            <ul class="story__list">
{items}
            </ul>"""
        else:
            body = chr(10).join(f"            <p>{esc(x)}</p>" for x in ps)
        heading = (chr(10) + "            <h3>" + esc(h) + "</h3>") if h else ""
        parts.append(f"""          <section class="story__part">{heading}
{body}
          </section>""")
    return f"""  <!-- ============ CATEGORY TEXT ============ -->
  <section class="sec sec--band" aria-labelledby="about-h">
    <div class="wrap">
      <div class="story" data-reveal>
        <div class="story__aside">
          <span class="eyebrow">About printed bags</span>
          <h2 id="about-h">Discover the perfect promotional bags <span class="hl">for your brand.</span></h2>
          <p class="story__stand">{esc(stand)}</p>
          <a href="products-v4.html" class="btn btn--outline btn--sm">Browse the range {icon("i-arrow", 16)}</a>
        </div>
        <div class="story__body">
{chr(10).join(parts)}
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
        <h2 id="faq-h">Frequently asked questions <span class="hl">about corporate bags.</span></h2>
      </div>
      <div class="faq" data-reveal>
{items}
      </div>
    </div>
  </section>"""


def page(c):
    return "".join([
        head(c),
        CHROME,
        f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol>
        <li><a href="index-v4.html">Home</a></li>
        <li aria-current="page">{esc(c["crumb"])}</li>
      </ol>
    </div>
  </nav>

{hero(c)}

{featured(c)}

{groups(c)}

{popular(c)}

{weekly(c)}

{more(c)}

{copy_block(c)}

{faq(c)}

""",
        FOOTER,
    ])


def main():
    out = ROOT / BAGS["file"]
    out.write_text(page(BAGS), encoding="utf-8")
    print(f"wrote {BAGS['file']}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
