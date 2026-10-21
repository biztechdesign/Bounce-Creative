#!/usr/bin/env python3
"""Spin & Win - the shared wheel, its dialog and the floating "Spin & Win"
tab, written into every page.

Spec (meeting notes, 16 Oct 2026, TICKET/40123):
  - Logged-in customers only (client update, 21 Oct): a visitor who opens
    Spin & Win gets a log-in form first, with an option to create an account.
  - One spin per registered customer per day.
  - Eight prizes: 50, 100, 150, 200 reward points, free delivery, a free
    product, 5% off, 10% off. No "better luck next time".
  - Points go into the Magento rewards balance; discounts are codes for the
    offer-code field; the free product is set by the admin and is shown so
    customers can see what they could win. No minimum order value.

The markup goes between <!-- SPIN:START --> and <!-- SPIN:END --> in the
footer partial (so every generated page gets it) and in the two hand-written
pages. The account page renders its own card from wheel_svg().

    python scripts/spin/build_spin.py
"""

import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
FOOTER = ROOT / "scripts" / "pdp" / "_footer.html"
HAND_WRITTEN = ["index-v4.html", "products-v4.html"]

# Admin-configurable in the build. The image is what the customer sees.
FREE_PRODUCT = {
    "name": "Natural cotton shopper, printed with your logo",
    "short": "Branded cotton shopper",
    "img": "assets/img/products/bags/custom/shopper-natural-front.jpg",
}

# Clockwise from the top. Weights are prototype odds only - the build sets
# them server-side. "code" is what goes in the offer-code field.
PRIZES = [
    {"label": "50", "unit": "points", "kind": "points", "value": 50, "weight": 26,
     "fill": "#133935", "ink": "#EEE9DE", "title": "50 reward points"},
    {"label": "5%", "unit": "off", "kind": "code", "value": 5, "code": "SPIN5", "weight": 14,
     "fill": "#F37259", "ink": "#133935", "title": "5% off your next order"},
    {"label": "100", "unit": "points", "kind": "points", "value": 100, "weight": 18,
     "fill": "#D8E4D1", "ink": "#133935", "title": "100 reward points"},
    {"label": "Free", "unit": "delivery", "kind": "delivery", "value": 0, "code": "SPINSHIP", "weight": 12,
     "fill": "#EEE9DE", "ink": "#133935", "title": "Free delivery on your next order"},
    {"label": "150", "unit": "points", "kind": "points", "value": 150, "weight": 11,
     "fill": "#133935", "ink": "#EEE9DE", "title": "150 reward points"},
    {"label": "10%", "unit": "off", "kind": "code", "value": 10, "code": "SPIN10", "weight": 6,
     "fill": "#F37259", "ink": "#133935", "title": "10% off your next order"},
    {"label": "200", "unit": "points", "kind": "points", "value": 200, "weight": 9,
     "fill": "#D8E4D1", "ink": "#133935", "title": "200 reward points"},
    {"label": "Free", "unit": "product", "kind": "product", "value": 0, "code": "SPINGIFT", "weight": 4,
     "fill": "#EEE9DE", "ink": "#B93B1C", "title": "A free " + FREE_PRODUCT["short"].lower()},
]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


def wheel_svg(size=360, cls="wheel__disc"):
    """Segment i is centred i*45 degrees clockwise from the top, so the
    script lands segment k by turning the disc to -k*45."""
    n = len(PRIZES)
    step = 360 / n
    c, r = 100, 96
    parts = []
    for i, p in enumerate(PRIZES):
        a0 = math.radians(i * step - step / 2 - 90)
        a1 = math.radians(i * step + step / 2 - 90)
        x0, y0 = c + r * math.cos(a0), c + r * math.sin(a0)
        x1, y1 = c + r * math.cos(a1), c + r * math.sin(a1)
        parts.append(f'<path d="M{c} {c} L{x0:.2f} {y0:.2f} A{r} {r} 0 0 1 {x1:.2f} {y1:.2f} Z" '
                     f'fill="{p["fill"]}" stroke="#133935" stroke-width="1"/>')
        parts.append(
            f'<g transform="rotate({i * step:.1f} {c} {c})" fill="{p["ink"]}" text-anchor="middle">'
            f'<text x="{c}" y="35" font-family="Space Grotesk, Arial, sans-serif" font-size="16" font-weight="700">{esc(p["label"])}</text>'
            f'<text x="{c}" y="48" font-family="DM Mono, Menlo, monospace" font-size="7.5" letter-spacing=".8">{esc(p["unit"].upper())}</text>'
            f'</g>')
    for i in range(n):
        a = math.radians(i * step - step / 2 - 90)
        parts.append(f'<circle cx="{c + 92 * math.cos(a):.2f}" cy="{c + 92 * math.sin(a):.2f}" r="2.4" '
                     f'fill="#EEE9DE" stroke="#133935" stroke-width=".8"/>')
    return (f'<svg class="{cls}" viewBox="0 0 200 200" width="{size}" height="{size}" aria-hidden="true">'
            f'<circle cx="{c}" cy="{c}" r="99" fill="#133935"/>{"".join(parts)}</svg>')


def snippet():
    data = json.dumps({
        "prizes": [{k: p[k] for k in ("label", "unit", "kind", "value", "weight", "title", "code") if k in p}
                   for p in PRIZES],
        "freeProduct": FREE_PRODUCT,
    })
    legend = "".join(
        f'<li><span class="wheel__sw" style="--sw:{p["fill"]}"></span>{esc(p["title"])}</li>' for p in PRIZES)
    fp = FREE_PRODUCT
    return f"""<!-- SPIN:START - generated by scripts/spin/build_spin.py; edit there -->
<link rel="stylesheet" href="assets/css/spin-v4.css?v=6">

<!-- Floating entry point, every page -->
<button class="spintab" type="button" id="spin-tab" aria-haspopup="dialog" aria-controls="spin-dlg" data-login-url="login">
  {wheel_svg(30, "spintab__wheel")}
  <span class="spintab__t"><b>Spin &amp; Win</b><small id="spin-tab-sub">Log in to spin</small></span>
</button>

<dialog class="spindlg" id="spin-dlg" aria-labelledby="spin-dlg-t">
  <script type="application/json" id="spin-data">{data}</script>
  <div class="spindlg__in">
    <button class="spindlg__x" type="button" data-spin-close aria-label="Close">{icon("i-close", 18)}</button>

    <div class="spindlg__wheel">
      <div class="wheel">
        <span class="wheel__pointer" aria-hidden="true"></span>
        <div class="wheel__rot" id="wheel-rot">{wheel_svg()}</div>
        <button class="wheel__hub" type="button" data-spin-go aria-label="Spin the wheel">Spin</button>
      </div>
    </div>

    <div class="spindlg__side">


      <!-- 1. Ready -->
      <div class="spinstate" data-state="ready">
        <div class="spinme">
          <span class="spinme__av" data-spin-initials aria-hidden="true">AS</span>
          <span class="spinme__who"><small>Welcome back</small><b data-spin-name>Anjana Solanki</b></span>
          <span class="spinme__bal"><small>Your points</small><b><span data-spin-bal>500</span> <em>= <span data-spin-worth>&pound;250.00</span></em></b></span>
        </div>
        <span class="spin__tag" data-spin-left>{icon("i-star", 14)}1 free spin every day</span>
        <h2 class="spindlg__t" id="spin-dlg-t">Spin &amp; <span class="hl">win.</span></h2>
        <p class="spindlg__p">Every spin wins. Points, discounts, free delivery &mdash; or this month&rsquo;s free product.</p>
        <button class="btn btn--coral spindlg__go" type="button" data-spin-go>Spin the wheel {icon("i-arrow", 16)}</button>
        <p class="spindlg__terms">Logged-in customers only, one spin per account per day. Points are added to your rewards; codes go in the offer-code field at checkout. No minimum order.</p>
      </div>

      <!-- 2. Spinning -->
      <div class="spinstate" data-state="busy" hidden>
        <span class="spin__tag">{icon("i-bolt", 14)}Spinning&hellip;</span>
        <h2 class="spindlg__t">Good <span class="hl">luck!</span></h2>
        <p class="spindlg__p">Every segment wins &mdash; let&rsquo;s see what you get.</p>
      </div>

      <!-- 3. Won - credited to the account -->
      <div class="spinstate" data-state="claimed" hidden role="status" aria-live="polite">
        <span class="spin__tag spin__tag--won">{icon("i-check", 14)}You won</span>
        <p class="spinwin__big" data-spin-prize>&mdash;</p>
        <p class="spindlg__p" data-spin-how>&mdash;</p>
        <p class="spinme__new" data-spin-newbal hidden>{icon("i-star", 14)}New balance <b data-spin-bal>500</b> points <em>= <span data-spin-worth>&pound;250.00</span></em></p>
        <div class="spinwin__code" data-spin-codebox hidden>
          <span class="spinwin__code-v" data-spin-code>SPIN5</span>
          <button class="btn btn--outline btn--sm" type="button" data-spin-copy>Copy code</button>
        </div>
        <div class="spinwin__acts">
          <a href="products-v4.html" class="btn btn--solid" data-spin-use>Start shopping {icon("i-arrow", 16)}</a>
          <a href="account-rewards-v4.html" class="btn btn--outline">My rewards</a>
        </div>
        <p class="spindlg__next">{icon("i-bolt", 14)}Next free spin in <b data-spin-countdown>&mdash;</b></p>
      </div>

      <!-- 4. Already used today -->
      <div class="spinstate" data-state="used" hidden>
        <span class="spin__tag">{icon("i-star", 14)}0 spins left today</span>
        <h2 class="spindlg__t">Come back <span class="hl">tomorrow.</span></h2>
        <p class="spindlg__p">You&rsquo;ve had today&rsquo;s spin. Your next free spin is ready in</p>
        <p class="spinwin__big spinwin__big--clock" data-spin-countdown>&mdash;</p>
        <a href="account-rewards-v4.html" class="btn btn--outline">See my rewards {icon("i-arrow", 16)}</a>
      </div>
    </div>
  </div>
  <p class="spindlg__demo">Design preview: logged out, Spin &amp; Win goes to the log-in page; today&rsquo;s spin is remembered in this browser.
    <button class="linkbtn" type="button" data-spin-reset>Reset the demo</button></p>
</dialog>
<script src="assets/js/spin-v4.js?v=6" defer></script>
<!-- SPIN:END -->"""


def inject(text, block):
    if "<!-- SPIN:START" in text:
        return re.sub(r"<!-- SPIN:START.*?<!-- SPIN:END -->", lambda _: block, text, count=1, flags=re.S)
    return text.replace("</body>", block + "\n</body>", 1)


def main():
    block = snippet()
    FOOTER.write_text(inject(FOOTER.read_text(encoding="utf-8"), block), encoding="utf-8")
    print("_footer.html: spin block in place")
    for name in HAND_WRITTEN:
        p = ROOT / name
        p.write_text(inject(p.read_text(encoding="utf-8"), block), encoding="utf-8")
        print(name, ": spin block in place")


if __name__ == "__main__":
    main()
