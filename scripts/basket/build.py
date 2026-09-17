#!/usr/bin/env python3
"""Generate the basket page.

The live basket's content - one configured line, its artwork and Pantone
capture, the deadline notice, discount code, shipping estimate and totals -
recomposed in the v4 system. Desktop layout only: a design reference for
estimation.

    python scripts/basket/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
FOOTER = (PDP / "_footer.html").read_text(encoding="utf-8").replace(
    '<script src="assets/js/pdp-v4.js?v=23"></script>',
    '<script src="assets/js/basket-v4.js?v=1"></script>')

VAT = 0.20


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


def money(v):
    return f"&pound;{v:,.2f}"


# --------------------------------------------------------------------------
# Content - the live basket
# --------------------------------------------------------------------------

BASKET = {
    "file": "basket-v4.html",
    "title": "Your basket | Bounce Creative Designs",
    "phone": "020 8318 9603",
    "lines": [{
        "name": "CARRO Folding Crate Container Trolley",
        "sku": "mid-MO6746-03",
        "img": "assets/img/products/office/carro-folding-crate-trolley.jpg",
        "area": "Front upper",
        "area_size": "30 × 80mm",
        "method": "Screen printing",
        "max_colours": 1,
        "qty": 25,
        "each": 22.79,
        "spot": True,          # screen printing asks for Pantone references
    }],
}


def line_item(i, ln):
    sub = ln["qty"] * ln["each"]
    pantone = ""
    if ln["spot"]:
        colours = chr(10).join(f"""              <label class="pan__field">
                <span class="pan__t">Colour {n} <b class="req" aria-hidden="true">*</b></span>
                <input type="text" name="pantone-{i}-{n}" placeholder="Pantone number" required>
              </label>""" for n in range(1, ln["max_colours"] + 1))
        pantone = f"""
          <div class="pan">
            <p class="pan__lbl">{esc(ln["method"])} &middot; your brand Pantone colours <b class="req" aria-hidden="true">*</b></p>
            <div class="pan__row">
{colours}
            </div>
            <label class="pan__dk">
              <input type="checkbox" name="pantone-{i}-unknown">
              <span>I don't know the Pantone colours &mdash; please match them and send me a final proof</span>
            </label>
          </div>"""

    return f"""        <article class="line" data-each="{ln["each"]}">
          <div class="line__main">
            <a href="#" class="line__media">
              <img src="{ln["img"]}" alt="{esc(ln["name"])}" width="700" height="700">
            </a>
            <div class="line__info">
              <h2 class="line__name"><a href="#">{esc(ln["name"])}</a></h2>
              <p class="line__sku">Product code <b>{esc(ln["sku"])}</b></p>
              <dl class="line__cfg">
                <div><dt>Print area</dt><dd>{esc(ln["area"])}</dd></div>
                <div><dt>Print type</dt><dd>{esc(ln["method"])}</dd></div>
                <div><dt>Max colours</dt><dd>{ln["max_colours"]}</dd></div>
                <div><dt>Print colours</dt><dd class="line__pending">Pantone below</dd></div>
              </dl>
              <div class="line__acts">
                <button class="linkbtn" type="button">Edit configuration</button>
                <button class="linkbtn linkbtn--quiet" type="button">Remove</button>
              </div>
            </div>
            <div class="line__qty">
              <span class="line__lbl">Qty</span>
              <div class="qty">
                <button class="qty__btn" type="button" data-step="down" aria-label="Decrease quantity">&minus;</button>
                <input type="number" value="{ln["qty"]}" min="1" step="1" inputmode="numeric" aria-label="Quantity">
                <button class="qty__btn" type="button" data-step="up" aria-label="Increase quantity">&plus;</button>
              </div>
              <span class="line__each">{money(ln["each"])} each</span>
            </div>
            <div class="line__sub">
              <span class="line__lbl">Subtotal</span>
              <b data-role="line-sub">{money(sub)}</b>
            </div>
          </div>

          <!-- Artwork for this line: where it goes, and the file to print -->
          <div class="art">
            <div class="art__pos">
              <img src="{ln["img"]}" alt="{esc(ln["name"])} showing the {esc(ln["area"].lower())} print position" width="700" height="700">
              <p class="art__cap"><b>Branding location</b> {esc(ln["area"])} &middot; {esc(ln["area_size"])}</p>
              <p class="art__note">This image may not show the exact product colour &mdash; refer to the product image above.</p>
            </div>
            <div class="art__up">
              <label class="drop">
                <input type="file" name="artwork-{i}" accept=".eps,.ai,.jpg,.jpeg,.pdf,.png,.svg">
                <span class="drop__in">
                  {icon("i-transfer", 28)}
                  <b>Upload your logo or artwork</b>
                  <span>Click or drag a file here &middot; EPS, AI or JPEG</span>
                </span>
              </label>
              <p class="art__cap"><b>Logo preview</b> <span class="art__empty">Nothing uploaded yet</span></p>
            </div>
          </div>
{pantone}
          <p class="line__approve">{icon("i-eye", 16)}<span><b>Nothing goes to bulk production until it is fully approved.</b> Our designers check every file and send you a proof first.</span></p>
        </article>"""


def page(c):
    lines = c["lines"]
    subtotal = sum(l["qty"] * l["each"] for l in lines)
    vat = subtotal * VAT
    units = sum(l["qty"] for l in lines)
    items_html = chr(10).join(line_item(i, ln) for i, ln in enumerate(lines, 1))

    body = f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol>
        <li><a href="index-v4.html">Home</a></li>
        <li aria-current="page">Basket</li>
      </ol>
    </div>
  </nav>

  <section class="sec sec--flush" aria-labelledby="basket-h">
    <div class="wrap">

      <!-- Reward points prompt, dismissible -->
      <aside class="reward-note" id="reward-note">
        {icon("i-tag", 18)}
        <p><b>Earn reward points on this order.</b> Log in or create an account before you check out
        &mdash; you collect a point for every &pound;10 you spend, worth 50p off your next order.</p>
        <a href="#" class="btn btn--outline btn--sm">Log in or sign up</a>
        <button class="reward-note__x" type="button" aria-label="Dismiss" data-dismiss="reward-note">{icon("i-close", 16)}</button>
      </aside>

      <div class="basket-head">
        <div>
          <span class="eyebrow">Your order</span>
          <h1 id="basket-h">Your <span class="hl">basket.</span></h1>
        </div>
        <p class="basket-head__meta"><b>{len(lines)} item</b> &middot; <b id="unit-count">{units}</b> units &middot;
          <a href="products-v4.html">Continue shopping {icon("i-arrow", 14)}</a></p>
      </div>

      <div class="basket">
        <div class="basket__lines">
          <div class="basket__cols" aria-hidden="true"><span>Item</span><span>Qty</span><span>Subtotal</span></div>
{items_html}
          <div class="basket__foot">
            <a href="products-v4.html" class="btn btn--outline">{icon("i-arrow", 16)}Continue shopping</a>
            <button class="btn btn--outline" type="button">Update basket</button>
          </div>
        </div>

        <aside class="summary-card" aria-labelledby="sum-h">
          <h2 class="summary-card__t" id="sum-h">Order summary</h2>

          <dl class="totals">
            <div><dt>Subtotal</dt><dd id="t-sub">{money(subtotal)}</dd></div>
            <div><dt>VAT <span>20%</span></dt><dd id="t-vat">{money(vat)}</dd></div>
            <div class="totals__ship"><dt>Delivery</dt><dd>Calculated at checkout</dd></div>
            <div class="totals__grand"><dt>Total</dt><dd id="t-total">{money(subtotal + vat)}</dd></div>
          </dl>

          <a href="#" class="btn btn--solid summary-card__cta">Proceed to checkout {icon("i-arrow", 18)}</a>

          <form class="code" onsubmit="return false;">
            <label class="code__t" for="code">Do you have a discount code?</label>
            <div class="code__row">
              <input type="text" id="code" placeholder="Enter discount code">
              <button class="btn btn--outline btn--sm" type="submit">Apply</button>
            </div>
          </form>

          <details class="ship">
            <summary>Estimate shipping and tax</summary>
            <div class="ship__body">
              <label class="qfield"><span class="qfield__t">Country</span>
                <select><option>United Kingdom</option><option>Ireland</option><option>Other &mdash; request a quote</option></select></label>
              <label class="qfield"><span class="qfield__t">Postcode</span><input type="text" placeholder="e.g. BS1 4DJ"></label>
              <p class="ship__note">Tracked UK delivery to one mainland address. Free on orders over &pound;3,000 excluding VAT.</p>
            </div>
          </details>

          <div class="deadline">
            {icon("i-bolt", 18)}
            <p><b>Do you have a no-fail deadline for this order?</b> Call us on
            <a href="tel:+442083189603">{c["phone"]}</a> so we can confirm we can deliver on time with this product.</p>
          </div>

          <p class="accept"><span>We accept</span>
            <span class="accept__card">Mastercard</span><span class="accept__card">Visa</span><span class="accept__card">Amex</span>
          </p>
        </aside>
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
<title>{esc(c["title"])}</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=114">
<link rel="stylesheet" href="assets/css/list-v4.css?v=21">
<link rel="stylesheet" href="assets/css/pdp-v4.css?v=65">
<link rel="stylesheet" href="assets/css/basket-v4.css?v=3">
<script>document.documentElement.className += " js";</script>
"""
    # the footer partial opens with </main>; this page closes main itself
    footer = FOOTER.replace("</main>\n", "", 1)
    return head + CHROME + body + footer


def main():
    out = ROOT / BASKET["file"]
    out.write_text(page(BASKET), encoding="utf-8")
    print(f"wrote {BASKET['file']}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
