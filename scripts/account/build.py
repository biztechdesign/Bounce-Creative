#!/usr/bin/env python3
"""Generate the customer-account pages.

Three pages from the live account area, recomposed in the v4 system and
sharing one account shell (side navigation + recently-ordered widget):

    account-address-v4.html       customer/address/
    account-address-new-v4.html   customer/address/new/
    account-rewards-v4.html       customer/rewards/

Desktop layout only: a design reference for estimation.

    python scripts/account/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
FOOTER = (PDP / "_footer.html").read_text(encoding="utf-8").replace(
    '<script src="assets/js/pdp-v4.js?v=23"></script>',
    '<script src="assets/js/account-v4.js?v=1"></script>')

CSS_V = 1


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


# --------------------------------------------------------------------------
# Shared content - the live account menu and customer
# --------------------------------------------------------------------------

CUSTOMER = {
    "name": "Anjana Solanki",
    "prefix": "Mr",
    "initials": "AS",
}

# The live "My Account" menu, in order.
NAV = [
    ("info",      "Account information",        "#"),
    ("address",   "Address book",               "account-address-v4.html"),
    ("orders",    "My orders",                  "#"),
    ("downloads", "My downloadable products",   "#"),
    ("wishlist",  "My wish list",               "#"),
    ("payments",  "Stored payment methods",     "#"),
    ("reviews",   "My product reviews",         "#"),
    ("news",      "Newsletter subscriptions",   "#"),
    ("rewards",   "My points and rewards",      "account-rewards-v4.html"),
    ("subs",      "My subscriptions",           "#"),
    ("stock",     "My out of stock subscriptions", "#"),
]

RECENT = {
    "name": "Brite-Americano® Recycled 350 ml insulated tumbler",
}

ADDRESS = {
    "name": "Mr Anjana Solanki",
    "company": "",
    "street": ["asdhasj", "sjkfhasj"],
    "city": "adasjhd",
    "region": "Anjana",
    "postcode": "38009",
    "country": "United Kingdom",
    "phone": "32423432234",
}

PREFIXES = ["Mr", "Ms", "Mrs", "Miss", "Sir", "Dr"]

REWARDS = {
    "balance": 500,
    "earned": 0,
    "spent": 0,
    "rate": 0.50,          # pounds per point
    "transactions": [
        {"id": 38, "date": "31/07/2025", "comment": "Updated by admin",
         "amount": 500, "status": "Completed", "expires": "N/A"},
    ],
}


# --------------------------------------------------------------------------
# Shell
# --------------------------------------------------------------------------

def side_nav(active):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'          <li><a href="{href}"{cur}>{esc(label)}</a></li>')
    return f"""      <aside class="acct__side">
        <nav class="acct-nav" aria-label="My account">
          <div class="acct-nav__who">
            <span class="acct-nav__avatar" aria-hidden="true">{CUSTOMER["initials"]}</span>
            <span><b>{esc(CUSTOMER["name"])}</b><small>Signed in</small></span>
          </div>
          <ul class="acct-nav__list">
{chr(10).join(items)}
          </ul>
          <a href="#" class="acct-nav__out">{icon("i-arrow", 14)}Sign out</a>
        </nav>

        <!-- Recently ordered: quick re-order, as on the live account -->
        <section class="recent" aria-labelledby="recent-h">
          <h2 class="recent__t" id="recent-h">Recently ordered</h2>
          <label class="recent__item">
            <input type="checkbox" name="reorder" checked>
            <span>{esc(RECENT["name"])}</span>
          </label>
          <div class="recent__acts">
            <button class="btn btn--solid btn--sm" type="button">{icon("i-bag", 15)}Add to basket</button>
            <a href="#" class="btn btn--outline btn--sm">View all</a>
          </div>
        </section>
      </aside>"""


def shell(c, active, crumbs, head_extra, main_html):
    crumb_items = "".join(
        f'<li><a href="{h}">{esc(t)}</a></li>' if h else f'<li aria-current="page">{esc(t)}</li>'
        for t, h in crumbs)
    body = f"""
<main id="main" tabindex="-1">

  <!-- ============ BREADCRUMB ============ -->
  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol><li><a href="index-v4.html">Home</a></li>{crumb_items}</ol>
    </div>
  </nav>

  <section class="sec sec--flush" aria-labelledby="acct-h">
    <div class="wrap">
      <div class="acct-head">
        <div>
          <span class="eyebrow">My account</span>
          <h1 id="acct-h">{c["h1"]}</h1>
        </div>
{head_extra}
      </div>

      <div class="acct">
{side_nav(active)}
        <div class="acct__main">
{main_html}
        </div>
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
<link rel="stylesheet" href="assets/css/account-v4.css?v={CSS_V}">
<script>document.documentElement.className += " js";</script>
"""
    footer = FOOTER.replace("</main>\n", "", 1)
    return head + CHROME + body + footer


# --------------------------------------------------------------------------
# Address book
# --------------------------------------------------------------------------

def address_lines(a):
    parts = [esc(a["name"])]
    if a["company"]:
        parts.append(esc(a["company"]))
    parts += [esc(s) for s in a["street"]]
    parts.append(esc(f'{a["city"]}, {a["region"]}, {a["postcode"]}'))
    parts.append(esc(a["country"]))
    return "<br>".join(parts)


def default_card(kind, a):
    return f"""            <article class="addr">
              <span class="addr__tag">{icon("i-check", 14)}Default {kind}</span>
              <p class="addr__body">{address_lines(a)}</p>
              <p class="addr__tel">{icon("i-phone", 14)}<a href="tel:{a["phone"]}">{a["phone"]}</a></p>
              <a href="account-address-new-v4.html" class="linkbtn">Change {kind} address</a>
            </article>"""


def address_page():
    a = ADDRESS
    head_extra = f"""        <a href="account-address-new-v4.html" class="btn btn--solid">{icon("i-tag", 16)}Add new address</a>"""
    main = f"""          <section class="acct-sec" aria-labelledby="def-h">
            <div class="acct-sec__head">
              <h2 id="def-h">Default addresses</h2>
              <p>Used for billing and delivery unless you choose another at checkout.</p>
            </div>
            <div class="addr-grid">
{default_card("billing", a)}
{default_card("shipping", a)}
            </div>
          </section>

          <section class="acct-sec" aria-labelledby="book-h">
            <div class="acct-sec__head">
              <h2 id="book-h">Address book</h2>
              <p>Every address saved to your account.</p>
            </div>
            <table class="acct-table">
              <thead>
                <tr>
                  <th scope="col">Company</th>
                  <th scope="col">Name</th>
                  <th scope="col">Street address</th>
                  <th scope="col">City</th>
                  <th scope="col">Country</th>
                  <th scope="col"><span class="vh">Actions</span></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="acct-table__muted">{esc(a["company"]) or "&mdash;"}</td>
                  <td><b>Solanki, Anjana</b></td>
                  <td>{esc(", ".join(a["street"]))}</td>
                  <td>{esc(a["city"])}</td>
                  <td>{esc(a["country"])}</td>
                  <td class="acct-table__acts">
                    <a href="account-address-new-v4.html" class="linkbtn">Edit</a>
                    <button class="linkbtn linkbtn--quiet" type="button">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="acct-table__foot">
              <span><b>1</b> item</span>
              <label class="show">Show
                <select aria-label="Addresses per page"><option>10</option><option>20</option><option>50</option></select>
                per page</label>
            </div>
          </section>

          <div class="acct-acts">
            <a href="#" class="btn btn--outline">{icon("i-arrow", 16)}Back</a>
          </div>"""
    return shell(
        {"title": "Address book | My account | Bounce Creative Designs",
         "h1": 'Address <span class="hl">book.</span>'},
        "address",
        [("My account", "#"), ("Address book", None)],
        head_extra, main)


# --------------------------------------------------------------------------
# New address
# --------------------------------------------------------------------------

def field(label, name, kind="text", required=False, wide=False, placeholder="", autocomplete=""):
    req = ' <b class="req" aria-hidden="true">*</b>' if required else ""
    r = " required" if required else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    ph = f' placeholder="{esc(placeholder)}"' if placeholder else ""
    cls = "qfield qfield--wide" if wide else "qfield"
    return f"""              <label class="{cls}"><span class="qfield__t">{esc(label)}{req}</span>
                <input type="{kind}" name="{name}"{r}{ac}{ph}></label>"""


def select(label, name, options, required=False, cls="qfield"):
    req = ' <b class="req" aria-hidden="true">*</b>' if required else ""
    opts = "".join(f"<option>{esc(o)}</option>" for o in options)
    return f"""              <label class="{cls}"><span class="qfield__t">{esc(label)}{req}</span>
                <select name="{name}">{opts}</select></label>"""


def new_address_page():
    main = f"""          <form class="aform" action="#" method="post" novalidate>
            <fieldset class="aform__set">
              <legend class="aform__legend">Contact information</legend>
              <div class="aform__grid aform__grid--name">
{select("Prefix", "prefix", PREFIXES, required=True)}
{field("First name", "firstname", required=True, autocomplete="given-name")}
{field("Last name", "lastname", required=True, autocomplete="family-name")}
              </div>
              <div class="aform__grid">
{field("Company", "company", autocomplete="organization")}
{field("Phone number", "telephone", kind="tel", required=True, autocomplete="tel")}
              </div>
            </fieldset>

            <fieldset class="aform__set">
              <legend class="aform__legend">Address</legend>
              <div class="aform__grid">
{field("Street address", "street[]", required=True, wide=True, autocomplete="address-line1")}
{field("Street address 2", "street[]", wide=True, autocomplete="address-line2")}
{field("Postcode", "postcode", required=True, autocomplete="postal-code")}
{field("City", "city", required=True, autocomplete="address-level2")}
{select("Country", "country_id", ["United Kingdom"], required=True)}
{field("County / state", "region", autocomplete="address-level1")}
              </div>
              <div class="aform__checks">
                <label class="check"><input type="checkbox" name="default_billing"><span>Use as my default billing address</span></label>
                <label class="check"><input type="checkbox" name="default_shipping"><span>Use as my default shipping address</span></label>
              </div>
            </fieldset>

            <div class="aform__foot">
              <p class="aform__req"><b class="req" aria-hidden="true">*</b> Required field</p>
              <div class="acct-acts">
                <button class="btn btn--solid" type="submit">Save address {icon("i-arrow", 16)}</button>
                <a href="account-address-v4.html" class="btn btn--outline">{icon("i-arrow", 16)}Go back</a>
              </div>
            </div>
          </form>"""
    return shell(
        {"title": "Add new address | My account | Bounce Creative Designs",
         "h1": 'Add a new <span class="hl">address.</span>'},
        "address",
        [("My account", "#"), ("Address book", "account-address-v4.html"), ("Add new address", None)],
        "", main)


# --------------------------------------------------------------------------
# Points and rewards
# --------------------------------------------------------------------------

def pts(n):
    return f"{n:,} point" + ("" if n == 1 else "s")


def rewards_page():
    r = REWARDS
    worth = r["balance"] * r["rate"]
    rows = chr(10).join(f"""                <tr>
                  <td class="acct-table__muted">#{t["id"]}</td>
                  <td>{t["date"]}</td>
                  <td>{esc(t["comment"])}</td>
                  <td class="acct-table__num"><b>{"+" if t["amount"] > 0 else ""}{t["amount"]:,}</b></td>
                  <td><span class="status status--ok">{icon("i-check", 13)}{t["status"]}</span></td>
                  <td class="acct-table__muted">{t["expires"]}</td>
                </tr>""" for t in r["transactions"])

    head_extra = f"""        <div class="chips acct-tabs" role="tablist" aria-label="Rewards">
          <a href="#" class="chip" role="tab" aria-selected="true">Reward dashboard</a>
          <a href="#" class="chip" role="tab" aria-selected="false">Transactions</a>
        </div>"""

    main = f"""          <div class="stats">
            <article class="stat stat--hero">
              <span class="stat__t">Available balance</span>
              <b class="stat__v">{r["balance"]:,}<small>points</small></b>
              <span class="stat__sub">Worth <b>&pound;{worth:,.2f}</b> off your next order</span>
            </article>
            <article class="stat">
              <span class="stat__t">Total earned</span>
              <b class="stat__v">{r["earned"]:,}<small>points</small></b>
              <span class="stat__sub">From orders and account activity</span>
            </article>
            <article class="stat">
              <span class="stat__t">Total spent</span>
              <b class="stat__v">{r["spent"]:,}<small>points</small></b>
              <span class="stat__sub">Redeemed against orders</span>
            </article>
          </div>

          <section class="acct-sec" aria-labelledby="info-h">
            <div class="acct-sec__head">
              <h2 id="info-h">Reward information</h2>
            </div>
            <div class="rate">
              {icon("i-tag", 22)}
              <div>
                <p class="rate__t">Current exchange rate</p>
                <p class="rate__v">Each <b>1 point</b> can be redeemed for <b>&pound;{r["rate"]:.2f}</b>.</p>
                <p class="rate__n">Points are applied at checkout against the order subtotal.</p>
              </div>
            </div>
          </section>

          <section class="acct-sec" aria-labelledby="tx-h">
            <div class="acct-sec__head acct-sec__head--row">
              <h2 id="tx-h">Recent transactions</h2>
              <a href="#" class="linkbtn">View all {icon("i-arrow", 13)}</a>
            </div>
            <table class="acct-table">
              <thead>
                <tr>
                  <th scope="col">Transaction</th>
                  <th scope="col">Date</th>
                  <th scope="col">Comment</th>
                  <th scope="col" class="acct-table__num">Amount</th>
                  <th scope="col">Status</th>
                  <th scope="col">Expires</th>
                </tr>
              </thead>
              <tbody>
{rows}
              </tbody>
            </table>
          </section>

          <form class="notify" action="#" method="post" aria-labelledby="notify-h">
            <div class="acct-sec__head">
              <h2 id="notify-h">Email notifications</h2>
              <p>Choose what we email you about your points.</p>
            </div>
            <div class="aform__checks">
              <label class="check"><input type="checkbox" name="update_balance" checked><span>Subscribe to balance updates</span></label>
              <label class="check"><input type="checkbox" name="update_expiration" checked><span>Subscribe to points expiration notifications</span></label>
            </div>
            <div class="acct-acts">
              <button class="btn btn--solid" type="submit">Save preferences {icon("i-arrow", 16)}</button>
            </div>
          </form>"""
    return shell(
        {"title": "My points and rewards | My account | Bounce Creative Designs",
         "h1": 'Points and <span class="hl">rewards.</span>'},
        "rewards",
        [("My account", "#"), ("My points and rewards", None)],
        head_extra, main)


PAGES = [
    ("account-address-v4.html", address_page),
    ("account-address-new-v4.html", new_address_page),
    ("account-rewards-v4.html", rewards_page),
]


def main():
    for name, fn in PAGES:
        out = ROOT / name
        out.write_text(fn(), encoding="utf-8")
        print(f"wrote {name}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
