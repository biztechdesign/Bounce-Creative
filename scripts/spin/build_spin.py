#!/usr/bin/env python3
"""Spin & Win - the shared wheel, its dialog and the floating "Spin & Win"
tab, written into every page.

Spec (meeting notes, 16 Oct 2026, TICKET/40123; client round 3, Nov 2026):
  - Everyone can spin. The first form is the account step (client, Nov 2026):
    the customer enters their email - a NEW email fills in their details and
    an account is created (a set-password link is emailed); an EXISTING email
    logs in with the password. Then the wheel shows, and the prize goes
    straight into the account - no claim step after the spin.
  - Form fields as the client's reference (MageDelight Spin to Win): first /
    last name, email, phone, job title (designation), company.
  - One spin per customer per day.
  - Prize expiry: points 24 hours; free delivery, coupons and the free gift
    30 days. The free gift is a plain, unbranded product the admin chooses
    based on order spend.
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

# The free gift: a plain, UNBRANDED product the admin picks based on the
# customer's order spend (client round 3).
FREE_PRODUCT = {
    "name": "plain, unbranded gift chosen by our team based on your order spend",
    "short": "Free gift",
}

# Clockwise from the top. Weights are prototype odds only - the build sets
# them server-side. "code" is what goes in the offer-code field.
PRIZES = [
    {"label": "50", "unit": "points", "kind": "points", "value": 50, "weight": 26,
     "fill": "#133935", "ink": "#EEE9DE", "title": "50 reward points", "expHours": 24},
    {"label": "5%", "unit": "off", "kind": "code", "value": 5, "code": "SPIN5", "weight": 14,
     "fill": "#F37259", "ink": "#133935", "title": "5% off your next order", "expDays": 30},
    {"label": "100", "unit": "points", "kind": "points", "value": 100, "weight": 18,
     "fill": "#D8E4D1", "ink": "#133935", "title": "100 reward points", "expHours": 24},
    {"label": "Free", "unit": "delivery", "kind": "delivery", "value": 0, "code": "SPINSHIP", "weight": 12,
     "fill": "#EEE9DE", "ink": "#133935", "title": "Free delivery on your next order", "expDays": 30},
    {"label": "150", "unit": "points", "kind": "points", "value": 150, "weight": 11,
     "fill": "#133935", "ink": "#EEE9DE", "title": "150 reward points", "expHours": 24},
    {"label": "10%", "unit": "off", "kind": "code", "value": 10, "code": "SPIN10", "weight": 6,
     "fill": "#F37259", "ink": "#133935", "title": "10% off your next order", "expDays": 30},
    {"label": "200", "unit": "points", "kind": "points", "value": 200, "weight": 9,
     "fill": "#D8E4D1", "ink": "#133935", "title": "200 reward points", "expHours": 24},
    {"label": "Free", "unit": "gift", "kind": "product", "value": 0, "code": "SPINGIFT", "weight": 4,
     "fill": "#EEE9DE", "ink": "#B93B1C", "title": "A free gift", "expDays": 30},
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
        "prizes": [{k: p[k] for k in ("label", "unit", "kind", "value", "weight", "title", "code", "expHours", "expDays") if k in p}
                   for p in PRIZES],
        "freeProduct": FREE_PRODUCT,
    })
    return f"""<!-- SPIN:START - generated by scripts/spin/build_spin.py; edit there -->
<link rel="stylesheet" href="assets/css/spin-v4.css?v=13">

<!-- Floating entry point, every page -->
<button class="spintab" type="button" id="spin-tab" aria-haspopup="dialog" aria-controls="spin-dlg">
  {wheel_svg(30, "spintab__wheel")}
  <span class="spintab__t"><b>Spin &amp; Win</b><small id="spin-tab-sub">1 free spin every day</small></span>
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

      <!-- 0. Not logged in: the details form first (client reference).
           A new email creates the account; an existing email swaps the
           details for a password and logs in. Then the wheel. -->
      <div class="spinstate" data-state="details" hidden>
        <p class="spinlead__brand">Spin &amp; Win</p>
        <h2 class="spinlead__t">Enter your details</h2>
        <p class="spinlead__p">Join our community and try your luck to win exclusive offers!</p>
        <form class="spinlead" id="spin-lead" novalidate>
          <fieldset class="spinlead__group" data-lead-new>
            <legend class="vh">Your name</legend>
            <label class="spinlead__f"><span>First name <b class="req" aria-hidden="true">*</b></span>
              <input name="first" autocomplete="given-name" placeholder="John" required></label>
            <label class="spinlead__f"><span>Last name</span>
              <input name="last" autocomplete="family-name" placeholder="Doe"></label>
          </fieldset>
          <label class="spinlead__f spinlead__f--wide"><span>Email address <b class="req" aria-hidden="true">*</b></span>
            <input name="email" type="email" autocomplete="email" placeholder="john.doe@example.com" required aria-describedby="spin-lead-status"></label>
          <!-- Checked as it is typed: an existing email switches to log in. -->
          <p class="spinlead__status" id="spin-lead-status" role="status" aria-live="polite" hidden></p>
          <fieldset class="spinlead__group" data-lead-new>
            <legend class="vh">Your details</legend>
            <label class="spinlead__f spinlead__f--wide"><span>Phone number <b class="req" aria-hidden="true">*</b></span>
              <input name="phone" type="tel" autocomplete="tel" placeholder="020 8318 9603" required></label>
            <label class="spinlead__f"><span>Designation <b class="req" aria-hidden="true">*</b></span>
              <input name="title" autocomplete="organization-title" placeholder="Manager" required></label>
            <label class="spinlead__f"><span>Company <b class="req" aria-hidden="true">*</b></span>
              <input name="company" autocomplete="organization" placeholder="Acme Ltd" required></label>
          </fieldset>
          <fieldset class="spinlead__group" data-lead-old hidden>
            <legend class="vh">Log in</legend>
            <label class="spinlead__f spinlead__f--wide"><span>Password <b class="req" aria-hidden="true">*</b></span>
              <input name="password" type="password" autocomplete="current-password" required></label>
            <div class="spinlead__meta"><a href="#" class="linkbtn">Forgot your password?</a></div>
          </fieldset>
          <button class="btn btn--coral spinlead__go" type="submit" data-lead-submit><span data-lead-label>Get ready to spin</span> {icon("i-arrow", 16)}</button>
          <p class="spinlead__n" data-lead-note>One free spin a day. New here? We&rsquo;ll create your free account and email you a link to set your password.</p>
        </form>
      </div>

      <!-- 1. Ready - everyone, guests included. Logged in, the strip shows
           who you are and your points. -->
      <div class="spinstate" data-state="ready">
        <div class="spinme" data-member-only>
          <span class="spinme__av" data-spin-initials aria-hidden="true">AS</span>
          <span class="spinme__who"><small>Welcome back</small><b data-spin-name>Anjana Solanki</b></span>
          <span class="spinme__bal"><small>Your points</small><b><span data-spin-bal>500</span> <em>= <span data-spin-worth>&pound;250.00</span></em></b></span>
        </div>
        <span class="spin__tag" data-spin-left>{icon("i-star", 14)}1 free spin every day</span>
        <h2 class="spindlg__t" id="spin-dlg-t"><span data-spin-hello>Spin &amp; <span class="hl">win.</span></span></h2>
        <p class="spindlg__p">Everyone gets a free spin every day &mdash; and every spin wins. Points, discounts, free delivery or a free gift.</p>
        <button class="btn btn--coral spindlg__go" type="button" data-spin-go>Try your luck {icon("i-arrow", 16)}</button>
{RULES}
      </div>

      <!-- 2. Spinning -->
      <div class="spinstate" data-state="busy" hidden>
        <span class="spin__tag">{icon("i-bolt", 14)}Spinning&hellip;</span>
        <h2 class="spindlg__t">Good <span class="hl">luck!</span></h2>
        <p class="spindlg__p">Every segment wins &mdash; let&rsquo;s see what you get.</p>
      </div>

      <!-- 4. Claimed - credited to the account, with its expiry -->
      <div class="spinstate" data-state="claimed" hidden role="status" aria-live="polite">
        <span class="spin__tag spin__tag--won">{icon("i-check", 14)}<span data-spin-claimtag>You won</span></span>
        <p class="spinwin__big" data-spin-prize>&mdash;</p>
        <p class="spindlg__p" data-spin-how>&mdash;</p>
        <p class="spin__exp" data-spin-exp>&mdash;</p>
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

      <!-- 5. Already used today -->
      <div class="spinstate" data-state="used" hidden>
        <span class="spin__tag">{icon("i-star", 14)}0 spins left today</span>
        <h2 class="spindlg__t">Come back <span class="hl">tomorrow.</span></h2>
        <p class="spindlg__p">You&rsquo;ve had today&rsquo;s spin. Your next free spin is ready in</p>
        <p class="spinwin__big spinwin__big--clock" data-spin-countdown>&mdash;</p>
        <a href="account-rewards-v4.html" class="btn btn--outline">See my rewards {icon("i-arrow", 16)}</a>
      </div>
    </div>
  </div>
  <p class="spindlg__demo">Design preview: any new email creates an account; chirag.t@biztechcs.com (any password) logs in. Today&rsquo;s spin is remembered in this browser.
    <button class="linkbtn" type="button" data-spin-reset>Reset the demo</button></p>
</dialog>
<script src="assets/js/spin-v4.js?v=16" defer></script>
<!-- SPIN:END -->"""


# The rules, shown under the wheel (client round 3). The rewards card on the
# account page uses RULES_ITEMS too.
RULES_ITEMS = [
    "Everyone gets <b>one free spin a day</b>.",
    "Enter your email to spin &mdash; new customers get a free account, existing customers log in. Your prize goes straight into your account.",
    "<b>Points</b> expire 24 hours after you win.",
    "<b>Free delivery</b> and <b>coupons</b> (5% / 10%) expire after 30 days.",
    "<b>Free gift</b> expires after 30 days &mdash; a plain, unbranded product our team picks based on your order spend.",
    "Codes go in the offer-code field at checkout. No minimum order.",
]
RULES = ("""        <details class="spinrules">
          <summary>How it works &amp; prize rules</summary>
          <ul>
""" + "\n".join(f"            <li>{r}</li>" for r in RULES_ITEMS) + """
          </ul>
        </details>""")


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
