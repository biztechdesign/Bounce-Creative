#!/usr/bin/env python3
"""Build the category navigation - desktop mega menu and mobile drawer - from
one data set, and write it into the shared header partial.

The categories and sub-categories are the live site's (scraped from its menu
on 19 Oct 2026), in its order. The live menu's search-result tags and
service quick links are left out, as the client asked.

    python scripts/nav/build_nav.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHROME = ROOT / "scripts" / "pdp" / "_chrome.html"

# label, nav link, intro (eyebrow, heading, coral half, sentence), feature tiles
# (image, title, caption, sticker), groups [(heading, [items])].
NAV = [
    ("Bags", "category-bags-v4.html",
     ("Printed bags", "Bags for", "every brand.", "Totes to anti-theft backpacks, printed in the UK with instant quotes on bulk orders."),
     [("assets/img/categories/bags/tile-anti-theft.jpg", "Anti theft bags", "Most ordered this month", "Top|pick"),
      ("assets/img/categories/bags/tile-rpet.jpg", "rPET bags", "Made from recycled bottles", None)],
     [("Shopping bags", ["Tote bags", "Foldable bags", "Jute bags", "Canvas bags", "Cotton bags", "Non woven bags", "Shopper bags", "Paper bags"]),
      ("Business bags", ["Conference bags", "Document bags", "Laptop bags", "Anti theft bags", "Exhibition bags"]),
      ("Travel and leisure bags", ["Beach bags", "Cooler bags", "Weekend holdalls", "Picnic bags", "Suitcases & trolleys", "Toiletry bags", "Waist bags"]),
      ("Backpacks & drawstring bags", ["Backpacks", "Drawstring bags", "Anti theft backpacks"]),
      ("Sports bags", ["Gym bags", "Sports backpacks", "Sports duffel bags", "Sports holdalls"]),
      ("Eco-friendly bags", [])]),

    ("Tech", "products-v4.html",
     ("Branded tech", "Tech they", "keep charged.", "Power banks, speakers and desk gadgets that earn a permanent spot on the desk."),
     [("assets/img/categories/tech.jpg", "Power banks", "Recycled and bamboo cases", "New|in"),
      ("assets/img/categories/tech.png", "Wireless chargers", "Magsafe and desk pads", None)],
     [("Music & audio", ["Speakers", "Headphones", "Earbuds"]),
      ("Mobile phone", ["Power banks", "Wireless chargers", "Charging cables", "Phone stands & holders", "Phone accessories", "Stylus pens"]),
      ("Tech accessories", ["Webcam covers", "RFID wallets", "Screen cleaners", "Computer accessories", "Gadgets"]),
      ("USB products", ["USB hubs", "USB flashdrives"]),
      ("Eco-friendly tech", [])]),

    ("Drinkware", "products-v4.html",
     ("Branded drinkware", "Bottles and mugs", "on every desk.", "Insulated steel, recycled plastic and glass, with the carbon figure on every line."),
     [("assets/img/products/40_oz_quencher_tumbler_in_black.jpg", "Quencher tumblers", "The bestseller this year", "Hot|pick"),
      ("assets/img/products/kivu_500ml_recycled_insulated_cup.jpg", "Recycled cups", "RCS certified steel", None)],
     [("Mugs", ["Ceramic mugs", "Plastic mugs", "China & porcelain mugs", "Camping mugs", "Glass mugs", "Full colour print mugs"]),
      ("Bottles", ["Sports bottles", "Water bottles", "Metal bottles", "Vacuum bottles", "Glass bottles", "Infuser bottles"]),
      ("Travel mugs", ["Metal travel mugs", "Plastic travel mugs", "Travel tumblers", "Thermo flasks", "Reusable coffee cups"]),
      ("Drinkware accessories", ["Bottle openers", "Coasters", "Straws", "Ice buckets", "Glassware", "Cocktail sets", "Barware", "Wine accessories"]),
      ("Eco-friendly drinkware", [])]),

    ("Clothing", "products-v4.html",
     ("Branded clothing", "Kit your team", "out properly.", "Embroidered and printed, from tees and polos to softshells and hi-vis."),
     [("assets/img/products/clothing/minsk-jacket-navy-royal.jpg", "Minsk softshell jacket", "Team favourite", None),
      ("assets/img/products/clothing/hi-vis-vest-visicoat-yellow.jpg", "Hi-vis vests", "Printed next day", "24|hr")],
     [("T-shirts", ["Womens fit T-shirts", "Mens T-shirts", "Unisex T-shirts", "Kids T-shirts"]),
      ("Polos", ["Womens fit polos", "Mens polos", "Unisex polos"]),
      ("Outdoor clothing", ["Jackets", "Fleece jackets", "Softshell jackets", "Bodywarmers & gilets", "Ponchos"]),
      ("Hoodies & sweatshirts", ["Sweatshirts", "Hoodies", "Jumpers"]),
      ("Sportswear", ["Sports T-shirts", "Sports polos", "Sportswear accessories"]),
      ("Clothing accessories", ["Socks", "Gloves", "Sunglasses", "Aprons", "Flip flops", "Towels"]),
      ("Workwear", ["Hi-vis", "Shirts", "Hospitality clothing"]),
      ("Headwear", ["Baseball caps", "Hats", "Beanies", "Bandanas", "Summer hats", "Winter hats", "Bucket hats"]),
      ("Eco-friendly clothing", [])]),

    ("Pens", "products-v4.html",
     ("Printed pens", "The giveaway", "that gets used.", "Budget plastic to premium metal, plus the brands people ask for by name."),
     [("assets/img/categories/pens.jpg", "Bamboo & recycled pens", "Low-carbon writing", None),
      ("assets/img/categories/pens.png", "Pen gift sets", "Boxed and ready to send", None)],
     [("Plastic pens", ["Budget plastic pens", "Premium plastic pens", "Stylus pens", "Highlighter pens", "Multifunctional pens", "Marker pens", "Novelty pens"]),
      ("Metal pens", ["Budget metal pens", "Premium metal pens", "Metal stylus pens", "Metal rollerball pens", "Multifunction metal pens"]),
      ("Pencils & accessories", ["Budget pencils", "Mechanical pencils", "Colouring sets", "Crayons", "Rubbers", "Pencil sharpeners", "Pencil cases", "Rulers"]),
      ("Pen gift sets", ["Notebook & pen sets", "Pen sets"]),
      ("Pens by brands", ["Cross", "Luxe", "Parker", "Prodir", "Sharpie", "Waterman"]),
      ("Eco-friendly pens", [])]),

    ("Notebooks", "products-v4.html",
     ("Branded notebooks", "Notebooks worth", "writing in.", "A5 and A6, soft feel or hard cover, embossed, debossed or full colour."),
     [("assets/img/categories/notebooks.jpg", "Recycled notebooks", "Kraft and stone paper", None),
      ("assets/img/categories/notebooks.png", "Premium A5", "Debossed to order", None)],
     [("Notebooks", ["A6 notebooks", "A5 notebooks", "Soft feel notebooks", "Hard cover notebooks"]),
      ("Notepads", ["A5 notepads", "A4 notepads", "Desk pads", "Paper noteblocks", "Sticky notes"]),
      ("Calendars", ["Desk calendars", "Wall calendars", "Diaries"]),
      ("Eco-friendly notebooks", [])]),

    ("Office", "products-v4.html",
     ("Office essentials", "The desk,", "on brand.", "Folders, desk tech and everyday essentials your team reaches for daily."),
     [("assets/img/categories/office.jpg", "Desk essentials", "Everyday, every desk", None),
      ("assets/img/categories/office.png", "Conference folders", "Leather and PU", None)],
     [("Desk essentials", ["Calculators", "Mouse mats", "Desk coasters", "Mobile phone stands", "Paper weights & trophies", "Office essentials"]),
      ("Folders", ["Conference folders", "Document wallets", "Leather & PU folders"]),
      ("Office tech", ["Desk hubs", "Desk chargers", "Computer mice", "Clocks", "Weather stations", "PC accessories"]),
      ("Eco-friendly office products", [])]),

    ("Outdoors", "products-v4.html",
     ("Outdoors & leisure", "Made for", "days out.", "Umbrellas, beach and picnic kit, sports and travel gear for every season."),
     [("assets/img/categories/outdoors.jpg", "Picnic & camping", "Built for summer events", None),
      ("assets/img/categories/outdoors.png", "Golf umbrellas", "Storm-proof, full colour", None)],
     [("Umbrellas", ["Automatic umbrellas", "Budget umbrellas", "Manual umbrellas", "Walking umbrellas", "Golf umbrellas", "Storm proof umbrellas", "Compact umbrellas", "Folding & telescopic"]),
      ("Beach", ["Summer bags", "Beach balls", "Beach towels", "Can coolers", "Beach games", "Beach accessories", "Fans", "Sunscreen"]),
      ("Picnic & camping", ["Picnic blankets", "Picnic accessories", "Picnic sets", "Camping accessories", "BBQ accessories", "BBQ sets"]),
      ("Sports & fitness", ["Activity trackers & watches", "Pedometers", "Cycling accessories", "Fitness equipment", "Yoga mats", "Resistance bands", "Sports balls", "Footballs", "Tennis balls", "Rugby balls", "Football items", "Sports towels", "Action cameras", "Golf"]),
      ("Car & motoring", ["Ice scrapers", "Car accessories"]),
      ("Travel products", ["Luggage tags", "Passport holders", "Travel wallets", "Travel adaptors", "Travel pillows", "Eye masks", "Travel sets", "Travel chargers"]),
      ("Eco-friendly outdoor & leisure", ["Footballs", "Travel adaptors", "Black + Blum", "Swiss Peak"])]),

    ("Giveaways", "products-v4.html",
     ("Event giveaways", "Small things,", "big reach.", "Keyrings, lanyards, sweets and stickers for events, freshers and fundraising."),
     [("assets/img/categories/giveaways.jpg", "Keyrings", "From 50p a unit", None),
      ("assets/img/categories/giveaways.png", "Sweets & treats", "Branded wrappers and tins", "Fun|size")],
     [("Keyrings", ["Bamboo keyrings", "Bottle opener keyrings", "Functional keyrings", "Metal keyrings", "Novelty keyrings", "Plastic keyrings", "PU & leather key fobs", "Recycled keyrings", "Shaped keyrings", "Teddy bear keyrings", "Torch keyrings", "Trolley coins", "Wood keyrings"]),
      ("Lanyards & wristbands", ["Lanyards", "Wristbands", "Lanyard accessories"]),
      ("Event giveaways", ["Awards", "Badges", "Charity & fundraising", "Fidget toys", "Flags & banners", "Fridge magnets", "Kids", "Logo bugs", "Novelty items", "Pet products", "Piggy banks", "Stickers", "Stress balls", "Teddy bears"]),
      ("Sweets & treats", ["Sweets", "Chocolate", "Mints", "Lollipops", "Snacks & sundries", "Drinks", "Advent calendars"]),
      ("Eco-friendly giveaways", ["Vegan sweets", "Christmas advents", "Hi!dea™", "Vinga"])]),

    ("Home & Living", "products-v4.html",
     ("Home & living", "Gifts that", "live at home.", "Kitchenware, wellbeing and home pieces people keep for years, not weeks."),
     [("assets/img/categories/home-living.jpg", "Wellbeing", "Candles, diffusers and bath", None),
      ("assets/img/categories/home-living.png", "Kitchenware", "Boards, boxes and carafes", None)],
     [("Health & wellbeing", ["First aid kits", "Condoms", "Hand sanitisers", "Face masks", "Bath accessories", "Bath bombs", "Bath towels", "Mental wellbeing", "Stress relievers", "Sun lotion", "Candles", "Diffusers"]),
      ("Beauty", ["Lip balms", "Compact mirrors", "Manicure sets", "Makeup bags", "Beauty accessories"]),
      ("Home", ["Blankets", "Seeds & plants", "Torches", "Tools", "Tape measures", "Home accessories", "Games & puzzles"]),
      ("Kitchenware", ["Kitchen knives", "Cheese boards", "Chopping boards", "Cooking aprons", "Lunch boxes", "Utensils & cutlery", "Food containers", "Cookware", "Serving boards", "Tableware", "Jugs & carafes"]),
      ("Eco-friendly home & living", ["Pocket tools", "Tape measures", "GearX", "Ukiyo"])]),

    ("Themes & Events", "products-v4.html",
     ("Themes & events", "Merch for", "the moment.", "Seasonal ranges, the brands people know, and what's trending this month."),
     [("assets/img/categories/themes-events.jpg", "Christmas", "Order by 1 December", "Xmas|ready"),
      ("assets/img/categories/themes-events.png", "Summer events", "Festivals and fun days", None)],
     [("Seasonal", ["Christmas", "Summer", "Winter", "Sports events", "Pride", "Festivals", "Freshers week", "Easter"]),
      ("Brands", ["Americano", "CamelBak", "Cross", "Moleskine", "Nordic Drift", "Ocean Bottle", "Parker", "Stanley", "Swiss Peak", "Waterman", "Xoopar"]),
      ("Trending", ["Discounted products", "Express products", "UK made", "Best sellers", "World Cup 2026", "Wimbledon", "Lindt"]),
      ("Eco-friendly themes & events", ["Christmas decorations", "Blankets"])]),

    ("Eco", "index-v4.html#eco-products",
     ("Eco & sustainable", "Small footprint,", "big welcome.", "Recycled, organic and plant-based, with GRS or RCS certification you can trace."),
     [("assets/img/categories/eco-sustainable.jpg", "Bamboo range", "FSC certified", None),
      ("assets/img/categories/eco-sustainable.png", "Recycled range", "GRS and RCS certified", "CO₂|data")],
     [("By category", ["Eco bags", "Eco pens", "Eco bottles", "Eco mugs", "Eco notebooks", "Eco gadgets", "Eco clothing", "Eco umbrellas", "Eco giveaways", "Eco keyrings"]),
      ("By type", ["Made in the UK", "Recycled", "Recyclable", "Solar powered", "Organic", "PVC free", "Sustainable collection"]),
      ("By material", ["Metal", "Wheat straw", "Stone", "Cork", "Glass", "Hemp", "Wood", "Denim", "Seed paper"]),
      ("Bamboo", ["Bamboo mugs", "Bamboo bottles", "Bamboo cheeseboards", "Bamboo pens", "Bamboo lunch boxes", "Bamboo power banks", "Bamboo wireless chargers", "Bamboo speakers", "Bamboo stationery", "Bamboo items", "Bamboo sunglasses"]),
      ("Recycled", ["Recycled pens", "Recycled bags", "Recycled notebooks", "Recycled bottles", "Recycled mugs", "Recycled umbrellas", "Recycled power banks", "Recycled chargers", "Recycled clothing", "Recycled lunch boxes", "CO₂ seal products", "FSC certified", "Ocean Bottle", "IQONIQ"])]),
]

SHOW = 8           # items per group before "+ N more"
SHOW_STACKED = 4   # when two groups share a column

# Groups with their own landing page in the mocks.
LINKS = {"Brands": "category-brands-v4.html"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def icon(name, size):
    return f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true"><use href="#{name}"/></svg>'


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def pack(groups, cols=5):
    """Lay the groups into at most `cols` columns, in order, with the columns
    as even in height as the order allows. A group costs its items plus two
    lines for its heading."""
    weights = [min(len(items), SHOW + 1) + 2 for _, items in groups]
    n = len(groups)
    if n <= cols:
        return [[g] for g in groups]
    # Contiguous split into `cols` columns minimising the tallest column.
    from functools import lru_cache
    pre = [0]
    for w in weights:
        pre.append(pre[-1] + w)

    @lru_cache(None)
    def best(i, k):
        """(tallest column, cut points) for groups[i:] in k columns."""
        if k == 1:
            return pre[n] - pre[i], ()
        out = None
        for j in range(i + 1, n - k + 2):
            rest, cuts = best(j, k - 1)
            cand = (max(pre[j] - pre[i], rest), (j,) + cuts)
            if out is None or cand[0] < out[0]:
                out = cand
        return out

    _, cuts = best(0, cols)
    bounds = (0,) + cuts + (n,)
    return [groups[a:b] for a, b in zip(bounds, bounds[1:])]


def group_html(head, items, show=None):
    show = show or SHOW
    eco = head.lower().startswith("eco-friendly")
    trend = head.lower() in ("trending",)
    cls = " mega__t--eco" if eco else (" mega__t--trend" if trend else "")
    href = LINKS.get(head)
    title = f'<a href="{href}">{esc(head)}</a>' if href else esc(head)
    # Long groups show their first eight and link to the rest, so every
    # column stays a readable length without scrolling inside the panel.
    shown, more = items[:show], len(items) - show
    lis = "\n".join(f'            <li><a href="#">{esc(x)}</a></li>' for x in shown)
    if more > 0:
        lis += f'\n            <li><a href="#" class="mega__more" aria-label="{more} more in {esc(head.lower())}">+ {more} more</a></li>'
    return f"""          <h4 class="mega__t{cls}">{title}</h4>
          <ul class="mega__list">
{lis}
          </ul>"""


def panel(label, href, intro, tiles, groups):
    key = slug(label)
    eyebrow, h_a, h_b, sentence = intro
    lists = [(h, i) for h, i in groups if i]
    eco_only = [h for h, i in groups if not i]
    n = sum(len(i) for _, i in lists)
    cols = "\n".join(
        '        <div class="mega__col">\n'
        + "\n".join(group_html(h, i, SHOW_STACKED if len(col) > 1 else SHOW) for h, i in col)
        + "\n        </div>"
        for col in pack(lists))
    eco_link = "".join(
        f'\n          <a href="#" class="mega__eco">{icon("i-leaf", 15)}{esc(h)}</a>' for h in eco_only)
    tile_html = []
    for img, t, cap, sticker in tiles:
        st = ""
        if sticker:
            a, b = sticker.split("|")
            st = f'\n          <span class="sticker sticker--coral"><b>{esc(a)}</b><span>{esc(b)}</span></span>'
        tile_html.append(f"""        <a href="#" class="mega__tile">
          <img src="{img}" alt="" loading="lazy" width="600" height="360">
          <span class="mega__tile__cap"><span><b>{esc(t)}</b><small>{esc(cap)}</small></span>{icon("i-arrow", 18)}</span>{st}
        </a>""")
    link = (f'<a href="{href}" class="is-eco">{icon("i-leaf", 16)}{esc(label)}</a>' if label == "Eco"
            else f'<a href="{href}">{esc(label)}</a>')
    return f"""        <li class="nav__item">
          {link}
          <button class="nav__tog" type="button" aria-expanded="false" aria-controls="mega-{key}" aria-label="{esc(label)} sub-categories">{icon("i-chevron", 14)}</button>
      <div class="mega" id="mega-{key}" hidden>
        <div class="wrap">
        <div class="mega__grid">
        <div class="mega__intro">
          <span class="eyebrow">{esc(eyebrow)}</span>
          <h3>{esc(h_a)} <span class="hl">{esc(h_b)}</span></h3>
          <p>{esc(sentence)}</p>
          <a href="{href}" class="tlink">View all {esc(label.lower())} {icon("i-arrow", 16)}</a>{eco_link}
          <div class="mega__stat"><b>{n}</b><span>sub-categories<br>of {esc(label.lower())}</span></div>
        </div>
{cols}
        <!-- Two editable feature tiles: image, title and caption are content
             fields so the team can swap them without a release. -->
        <div class="mega__feat">
{chr(10).join(tile_html)}
        </div>
        </div>
        </div>
      </div>
        </li>"""


def drawer_group(label, href, groups):
    parts = []
    for h, items in groups:
        if not items:
            continue
        lis = "\n".join(f'              <li><a href="#">{esc(x)}</a></li>' for x in items)
        parts.append(f'            <p class="drawer__sub-t">{esc(h)}</p>\n            <ul>\n{lis}\n            </ul>')
    return f"""      <li class="drawer__group">
        <details>
          <summary><span>{esc(label)}</span>{icon("i-chevron", 16)}</summary>
          <div class="drawer__sub">
            <a href="{href}" class="drawer__all">All {esc(label.lower())} {icon("i-arrow", 14)}</a>
{chr(10).join(parts)}
          </div>
        </details>
      </li>"""


def main():
    nav = "\n".join(panel(*c) for c in NAV)
    nav_ul = f"""<ul class="nav__list">
        <li><a href="products-v4.html">All Products</a></li>
{nav}
      </ul>"""
    drawer = "\n".join(drawer_group(c[0], c[1], c[4]) for c in NAV)
    drawer_ul = f"""<ul class="drawer__list">
      <li><a href="products-v4.html">All products</a></li>
{drawer}
    </ul>"""

    s = CHROME.read_text(encoding="utf-8")
    s, a = re.subn(r'<ul class="nav__list">.*?\n      </ul>', lambda _: nav_ul, s, count=1, flags=re.S)
    s, b = re.subn(r'<ul class="drawer__list">.*?\n    </ul>', lambda _: drawer_ul, s, count=1, flags=re.S)
    assert a == 1 and b == 1, (a, b)
    CHROME.write_text(s, encoding="utf-8")
    print(f"_chrome.html: {len(NAV)} categories, {s.count('class=\"mega\"')} panels")


if __name__ == "__main__":
    main()
