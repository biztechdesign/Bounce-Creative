# Bounce Creative Designs — Home Page Redesign (v3)

Design direction agreed with Abidur via Namita: clean, bold, modern; proper spacing and
hierarchy; **no boxed/card-heavy layouts**; **no dark theme**; a limited palette of two
primary colours plus one for buttons. Reference: giftcampaign.co.uk.

This prototype is the source of truth for the Figma build. Everything below is measured
from `assets/css/style.css`, so the Figma file and the eventual build stay in sync.

---

## 1. Colour

Two colours carry the brand. Everything else is a neutral ground.

| Token | Hex | Role |
|---|---|---|
| **Ink** (primary 1) | `#12141A` | Headlines, body type, announcement bar, footer |
| **Bounce Red** (primary 2) | `#E50E46` | Brand accent, all primary buttons, stats, eyebrows |
| Red pressed | `#BF0B3A` | Button hover/active only |
| Eco green | `#1F8A5B` | **Reserved** — the leaf icon and nothing else |
| White | `#FFFFFF` | Page ground, product tiles |
| Band | `#F5F4F1` | Alternating section bands, image grounds |
| Band deep | `#EBE9E4` | Large-numeral watermarks, media placeholder |
| Menu | `#F1F0ED` | Light grey strip behind the category nav |
| Line | `#E2E0DB` | The few remaining hairlines |
| Muted | `#6E737C` | Body copy, secondary text |
| Muted soft | `#9A9EA6` | Meta, counts, placeholders |

Bounce Red is sampled directly from the supplied logo (`#E50E46`), so the wordmark and the
buttons are the same red. Beyond that the page introduces exactly one more colour: a green
used **only** for the leaf icon, wherever it appears — the Eco nav item, the CO₂e USP and
the per-item CO₂e line under each product. The leaf therefore means one thing everywhere,
and no other element on the page is green. All remaining variety comes from photography.

**Section rhythm** (top to bottom): ink announcement → white header → **light grey menu
strip** → white hero → band → white → white → band → white → band → white → band → ink
footer. The menu strip is the only tinted band above the hero, and it replaces the two
hairlines that used to fence the header in.

---

## 2. Typography

| | Family | Weights | Notes |
|---|---|---|---|
| Display / headings | **Archivo** | 600, 700, 800 | Tracking −0.03em; −0.042em on the H1 |
| Body / UI | **Instrument Sans** | 400, 500, 600 | Tracking 0 |

### Scale (desktop @1440)

| Style | Size / line-height | Weight | Tracking |
|---|---|---|---|
| H1 hero | 80 / 0.98 | 700 | −0.042em |
| H2 section | 50 / 1.04 | 700 | −0.03em |
| H2 pull-quote | 40 / 1.24 | 600 | −0.03em |
| H3 | 21–23 / 1.04 | 700 | −0.025em |
| Stat numeral | 42 / 1.0 | 700 | −0.035em |
| Body large | 19 / 1.6 | 400 | 0 |
| Body | 16–17 / 1.65 | 400 | 0 |
| Small / meta | 13–14 / 1.5 | 400–500 | 0 |
| Eyebrow | 12 / 1.4 | 600 | +0.16em, uppercase, red |
| Button | 15 | 600 | +0.01em |

Headings clamp down fluidly on smaller viewports — H1 bottoms out at 38px, H2 at 32px.

### Widow control

Three layers, because none alone is sufficient:

1. `text-wrap: balance` on `h1`–`h4` — evens the lines of a heading.
2. `text-wrap: pretty` on `p` — discourages a lone last word in body copy.
3. `assets/js/typography.js` — binds the final two words of every heading and body
   paragraph with a non-breaking space, which *guarantees* it at any width. Skipped inside
   product cards, bento tiles and the marquee, where forcing a pair can overflow a narrow
   column instead of tidying it.

The hero H1 needed a fourth fix: at 80px "Branded merchandise" was wider than its column, so
it wrapped to four lines and stranded "keep." on its own. The type scale now tops out at
**60px**, which holds the intended two lines.

**Auditing this:** walk every `h1`–`h4` and `p`, range-measure each word's client rect and
group by line top. Two traps — attribute a hyphenated word to its *last* rect, or a word
broken across lines reads as a false orphan; and ignore elements mixing font sizes inline
(the `4.9/5` scores), where the smaller `<em>` sits lower on the same line and looks like a
second line.

---

## 2b. Icons

**Solar Linear** ([iconify.design/solar](https://icon-sets.iconify.design/solar/?suffixes=Linear))
is the only icon family on the page. Every glyph is inlined as an SVG `<symbol>` sprite and
referenced with `<use>`, so nothing is fetched at runtime.

| Use | Icon |
|---|---|
| Search | `solar:magnifer-linear` |
| Phone (announcement bar) | `solar:phone-linear` |
| Account | `solar:user-linear` |
| Basket | `solar:bag-4-linear` |
| Mobile menu | `solar:hamburger-menu-linear` |
| Button + link arrows | `solar:arrow-right-linear` |
| Product flags | `solar:delivery-bold`, `solar:cart-large-2-bold` |
| Reassurance ticks | `solar:check-circle-linear` |
| Value props | `solar:bolt`, `chart-2`, `tag-price`, `users-group-rounded` (Linear) |
| Per-item CO2e, Eco nav, eco USP | `solar:leaf-linear` (green) |
| USP: products in stock | `solar:box-linear` |
| USP: speed | `solar:bolt-linear` |
| USP: bulk pricing | `solar:tag-price-linear` |
| Ratings | `solar:star-bold` |

Solar's native 1.5px stroke on a 24 viewBox is kept, which is why the icons read lighter and
rounder than the buttons. Icons inherit `currentColor`; the CTA ticks and USP icons are
overridden to Bounce Red, and every leaf to Eco Green. The rating star, the two product-flag icons and
the back-to-top chevron are Bold weight: a 1.5px stroke on a 24 viewBox renders sub-pixel at 13–14px and turns
to mush, and a hollow star in a rating reads as *unfilled*, which would be wrong.

**Exception:** LinkedIn, Instagram and X in the footer are brand marks, not UI icons — Solar
has no logo glyphs, and substituting generic shapes would misrepresent the platforms.

---

## 3. Grid & spacing

- Container **1440px**, full-bleed — no side padding, so content spans the whole 1440 at
  desktop. Gutters return below 1180px (28px, then 20px ≤900px) so nothing touches the
  screen edge once the viewport is narrower than the container. Note this means at viewport
  widths between roughly 1180 and 1440 the content runs edge to edge.
- 8pt spacing base.
- Section padding: **88px** desktop → 76px ≤1180 → 56px ≤900. Tight sections use 64px.
  That puts **176px between sections** — generous but standard for commerce. It started at
  128px (256px between sections), which read as gaps rather than rhythm.
- Section header to content: **44px** (34px on centred headings, 40px above a tab row).
- Category grid: 4 cols, 32px column gap, 40px row gap. Feature tiles span 2 columns.
- Product rail: 5 cols, 36px gap.
- Value props: 4 cols separated by 40px margins and a 2px ink top rule — no dividers between.

### Breakpoints
`1180px` · `900px` · `560px`

---

## 4. The anti-card rules

These are the rules that keep the design off the "boxed" look Abidur rejected:

1. **No box-shadows anywhere.** Not one.
2. **No bordered containers.** Separation comes from whitespace, or from a 1px `Line`
   hairline *under* content — never a rectangle around it.
3. **Product tiles have no plate.** The tile ground is pure white, the same as the section,
   and product photography is set `mix-blend-mode: multiply` so cut-outs dissolve into the
   page. The product "card" is just an image, a name and a price sitting on the page.
4. **Category tiles are image + caption.** No frame, no fill, and since the last pass no
   caption rule either — the name and count sit straight on the page, and hover is carried
   by the name turning red and the arrow sliding. The same treatment runs in the hero.
5. **Supplier logos sit on tiles, in full colour.** The original grey `#EDEDED` plates baked
   into the source PNGs were knocked out and the marks trimmed (`assets/img/brands/`), then
   each is placed on a white 16px-radius tile against the cream band and scrolled as a
   single row. This is the one place a contained shape is right: a logo needs its own clear
   field, and greyscale was flattening brands the client sells on.
6. **Rounded, not boxed.** Corners are soft so the page reads modern, but nothing is
   enclosed: `--r-sm 10px` (inputs), `--r 18px` (product and category media),
   `--r-lg 28px` (hero and editorial media). Buttons, flags and social marks are full pills.

---

## 4b. CTA hover - the liquid button

Modelled on the CTA treatment at [labs.google](https://labs.google/). Behind each `.btn`
label sits an SVG pill (`assets/js/liquid.js`). On hover its outline deforms toward the
cursor and follows it, while the fill and label colour swap:

| Button | Rest | Hover |
|---|---|---|
| Primary | Red fill, white label | **Ink** fill, white label |
| Ghost | Ink 1.25px outline, ink label | **Ink** fill, white label |

How it works: the pill perimeter is sampled at 72 points, each carrying an outward normal.
Points are pushed along their normal by `0.115 x height`, attenuated by a gaussian on the
distance to the cursor (sigma `0.60 x height`); the displaced points are re-joined as a
closed Catmull-Rom curve. Amplitude and cursor position are eased per frame, so the shape
swells on enter and relaxes on leave rather than snapping.

Two guards: buttons keep an ordinary CSS background until the script tags them
`.has-liquid`, so they still look right if the JS never runs; and the effect is skipped
entirely under `prefers-reduced-motion`, leaving a plain colour transition.

---

## 5. Page structure

| # | Section | Ground | Purpose |
|---|---|---|---|
| 1 | Announcement bar | Ink | Offer code, the two-hour visual promise, and the phone number as a red-icon `tel:` link — the one actionable item up there, so it alone carries an icon |
| 1 | Announcement bar | Ink | Offer code, the two-hour visual promise, and the phone number as a red-icon `tel:` link — the one actionable item up there, so it alone carries an icon |
| 2 | Header | White | Logo left, **search centred**, account + basket right. No rules above or below |
| 3 | Category nav | Light grey | Led by **All Products** (per giftcampaign.co.uk). The tint replaces the hairlines |
| 4 | **Hero — the whole first fold** | White | See below |
| 5 | **USP strip** | Band | 4 icon-led facts: stock, speed, bulk pricing, published CO₂e |
| 6 | Shop by category | White | **Bento grid** — see below |
| 7 | **Our popular products** | White | Tabbed browser: 6 category tabs x 4 products, then a *View all products* CTA |
| 7b | **Our eco products** | White | Tabbed by material: Bamboo, Organic cotton, Recycled, Plantable |
| 8 | Why Bounce | Band | 4 value props, each led by a Solar icon. The 01–04 numerals went first (four independent reasons are not a sequence, so the numbering implied an order that did not exist), then the 2px ink rules above them — once the icon marked each column, the rule was a line doing nothing |
| 9 | Sustainability | White | The differentiator: published carbon data, 3 red stats |
| 10 | How it works | Band | 3 steps, red tick rules |
| 11 | Testimonial | White | Oversized pull-quote + Trustpilot / Google / repeat-rate scores |
| 12 | Brands we supply | Band | 12 supplier marks, each on its own white tile, scrolling as one row |
| 13 | **The standards behind the products** | White | 7 tabs: Promotional, Branding, GRS, RCS, Blockchain, ESG, CO₂ |
| 14 | **Our awards** | Band | 6 real badges: PSI, Distributor of the Year 2018/2019, BPMA winner 2020/2023, BPMA member |
| 15 | **Latest news** | White | 3 articles, image + title + excerpt, CTA on hover |
| 16 | Closing CTA | Band | Email capture, three reassurances |
| 17 | Footer | Ink | See below |

### The footer

The creative device comes from the brand itself rather than being applied to it: the Bounce
logo is a matrix of dots, so the footer ground carries that dot grid (a CSS radial-gradient,
masked to fade), and the wordmark runs oversized along the baseline at 5.5% white — texture,
not a second headline. The logo's three red dots sit beside it and **bounce**, staggered by
130ms, which the brand name earns. Stopped under `prefers-reduced-motion`.

Deliberately **no CTA here** — the closing section directly above already asks for the
enquiry, and repeating it would be the third ask in two screens.

Also carries real contact detail (phone as a `tel:` link, email, London) with Solar icons,
four link columns, and a back-to-top control.

**Payment marks** are drawn, not typed. Mastercard is exact geometry — two r=10 circles 10
apart, plus the lens where they overlap in `#FF5F00`. Visa and Amex are set in their brand
blues (`#1434CB`, `#016FD0`), and bank transfer uses a Solar mark, since BACS matters to B2B
buyers and has no card logo. Each sits on its own light tile, the same reasoning as the
supplier row: a brand mark needs a clear field to read.

**Watch the line-height.** The wordmark at `line-height: .78` made the line box shorter than
the glyphs, so the baseline fell outside it and the footer's `overflow: hidden` clipped the
letters. It is `line-height: 1` with 30px of bottom padding, which leaves 17px clearance.

**Background alternation is verified, not assumed** — a check walks every `<section>` and
compares each background to the one before it. The only adjacent match allowed is the
white run across categories → popular → eco, which is a deliberate single shopping expanse.
Adding sections silently broke this twice (Brands beside Standards, Awards beside News).

### The category bento

Nine tiles, four columns, 236px rows, **every tile carrying an image**. Tile weight encodes
range size rather than varying for effect: Eco & Sustainable (2,100 products) takes the 2x2
hero cell, Tech a tall 1x2, Notebooks and Home & Living single cells, then Outdoors,
Giveaways and Themes & Events take 2x1 bands. Labels sit on the image under a
bottom-weighted scrim so the photography stays clean; no borders, no shadows.

**Photography status per tile.** Eco & Sustainable, Tech, Notebooks and Outdoors & Leisure
use supplied photography, prepared by `scripts/category-image.py` — it centre-crops to the
tile's exact pixel ratio and writes at 2x, so we choose what survives the crop rather than
leaving it to `object-fit: cover`, and the file carries no pixels the layout discards.

    python scripts/category-image.py "path\photo.png" outdoors --bias 0.46

Eight of the nine tiles now use supplied photography. **Giveaways is the last placeholder**
— a composite built by `scripts/category-tiles.py` from real product shots on the shared
ground — and beside the rest it now reads as the odd one out.

**The label scrim was rebuilt for this photography.** The supplied shots are far brighter
than the site originals, and the original gradient (0.72 black rising to nothing at 62%)
stopped carrying the type. It now runs 0.88 → 0.62 at 22% → 0.30 at 42% → clear at 76%,
with a soft text-shadow behind the name, count and blurb. Anything lighter and the labels
fail on the pale wood backgrounds.

---

### The standards section

Seven tabs carrying the credential copy from the live site's own panels, verbatim in
substance. The right column holds **three facts instead of a photograph**: Bounce has no
distinct image for seven tabs, and a credentials section reads better as type and fact than
as stock photography. Every fact is drawn from that same copy — 81% / 2x / BPMA on the
promotional tab, cradle-to-grave and all-GHG on CO₂ — so nothing is invented.

The certifications row used to sit inside "Brands we supply", which conflated two different
things — the brands Bounce stocks, and the standards it works to. It now lives at the foot
of this section, reduced to a single line: GRS and RCS already have full tabs here, so only
FSC and ISO 14001 remain to be stated. BPMA came out earlier for the same reason, once the
awards section landed and it was being said three times on one page.

---

### The eco section

The same Option A card, tabbed by **what the product is actually made of** — Bamboo,
Organic cotton, Recycled, Plantable — rather than by category, which is how a buyer
shopping sustainably actually thinks. The badge shows the material with the green leaf, so
it reads as an eco claim without introducing a second accent colour.

Products are grouped by the material named in their own product titles, so the grouping is
real. Two constraints worth knowing: the site's `/eco` listing does not associate prices
with products reliably enough to scrape, so everything here comes from the validated
category data; and the per-product CO₂e figure could not be extracted reliably, so the
section states that the figure is published rather than inventing numbers.

---

### The tabbed product browser

Modelled on the *Our Popular Products* block on the live site. Six tabs — Bags, Drinkware,
Tech, Pens, Office, Giveaways — each showing four products, with a centred *View all
products* CTA below.

**Five products per row** in both tabbed sections, four tabs deep in eco and six in
popular. `.prod__name` carries a `min-height` of two lines so a wrapping product name does
not push its price out of line with the rest of the row.

**One chip treatment across every product**: a light pill with a hairline and ink text. Only
the icon changes — `delivery` for next-day, `cart` for order-online, and the green `leaf` for
an eco material. Colour is never used to distinguish them.

**Card treatment: Option A - enriched borderless** (chosen from five options; the
comparison page is kept at `options/product-styles.html`). Each card carries a rating, the
product name, colourway swatches, a *from* price with the minimum order, and a *Get a
visual* link that fades in on hover. The CTA occupies its row at rest with `opacity: 0`, so
revealing it never shifts the grid. On touch, where there is no hover, it is always shown.

- **Tabs carry no fill.** The reference uses grey boxes; here the active tab is ink at
  weight 600 with a red rule that scales in from the centre, inactive tabs are muted text.
  Same language as the nav hover, and it keeps the no-boxes rule intact.
- **Cards are name-left, price-right on one baseline**, no divider between them and no rule
  above — the reference's two dividers per card are what make it read as a grid of boxes.
- `NEXT DAY` is pulled out of the product name into the flag pill, because it is a lead
  time, not part of the name.
- Every name, price and photograph is **real, scraped from the live site** (prices come from
  the `data-price-amount` field). Clothing is absent from the tabs because its prices are
  gated behind login and I would have had to invent them.
- Keyboard support: arrow keys, Home and End move between tabs; panels are plain markup and
  the first ships visible, so it degrades to a static product grid without JS.

**Two bugs worth remembering** if this is rebuilt: `.rail{display:grid}` overrides the
browser's `[hidden]{display:none}`, so panels need `.rail[hidden]{display:none}` or every
tab renders at once; and a modifier like `.sechead--center` must be declared *after*
`.sechead`, or the base rule's `align-items` wins and the heading silently right-aligns.

**Photography note.** Supplier images arrive on mixed grounds — some pure white, some light
grey studio. Every tile therefore gets the same `--band` ground and the image is set to
`mix-blend-mode: multiply`, which dissolves white-ground shots into the tile exactly and
brings the grey ones close. Two of the Tech shots still show a faint inner rectangle; those
source images want re-cutting before launch.

---

### The first fold

Everything a visitor needs to judge Bounce sits above 1000px at 1440 wide:

- **Left** — eyebrow, H1, supporting copy, two liquid CTAs.
- **Right** — three **hero category tiles**: one tall (Drinkware) beside two stacked
  (Bags, Clothing), the stacked pair pushed down 56px so the trio reads as a composition
  rather than a grid. Column bottoms are flush; only the tops stagger.
- **Below both** — the proof strip: *"Chosen by companies across the UK"* on the left with
  an auto-scrolling logo marquee, and the Trustpilot / Google scores on the right.

**The logo marquee.** Five logos are visible at a time in a 740px window (five 148px slots).
The track holds the seven-logo set twice and translates exactly `-50%`, so the loop is
seamless with no snap. Hovering pauses the scroll and returns the logo under the cursor to
full brand colour from its resting grayscale; `prefers-reduced-motion` stops it outright.
One gotcha worth keeping: a flex item's automatic minimum size is `max-content`, so
`.proof__l` needs `min-width: 0` or the 2072px track escapes its `overflow: hidden` parent
and shoves the review scores off screen.

Two things were removed to make room, and neither is lost: the standalone client-logo band
(now inside the fold) and the hero stats row (25,000+ / 2 hrs already appear in the
announcement bar, the hero copy and the value props).

**No repeated imagery.** The hero owns Drinkware, Bags and Clothing, so the category grid
below covers what the hero does not — Eco, Tech, Notebooks, Home & Living, then the text
tile. No category and no photograph appears twice on the page.

**The strategic move:** the hero, the product rail and a whole section are built around
Bounce's published per-item CO₂e figure. It is on the live site already but buried — no
competitor, including Gift Campaign, can show that number. It is the one thing that makes
this page not a Gift Campaign clone.

---

## 6. Content notes

- All product names, prices and category counts come from the live site; CO₂e figures follow
  the format already published on Bounce product pages. Testimonial copy, review scores and
  the 41% / 87% figures are **placeholders** — swap for real numbers before client sign-off.
- Photography is pulled from the live Bounce media library, so the client sees their own
  products. Final build should re-shoot or re-crop the category images to a consistent
  4:5 / 8:5 pair.

---

## 7. Files

```
index.html                      Full home page prototype
assets/css/style.css            Design system + all section styles
assets/img/bounce-logo-ink.png  Wordmark recoloured for the white header
assets/img/bounce-logo-white.png Original wordmark, for the ink footer
assets/js/liquid.js             Liquid CTA hover behaviour
assets/js/tabs.js               Tabs - drives all three tabbed sections
assets/img/awards/*             6 real award badges (PSI, BPMA, Distributor of the Year)
assets/img/news/*               3 real article images
assets/img/categories/*         4 placeholder category stills - replace with photography
assets/img/brands/*.png         12 supplier marks, plates removed and trimmed
artifact/bounce-home.html       Self-contained single file (images inlined) for sharing
preview/                        Desktop and mobile full-page renders
```

Run locally with any static server, e.g. `python -m http.server 8788`.

To bring this into Figma, import `index.html` with the **html.to.design** plugin — it will
land as editable frames with the type styles and colours above already applied.
