#!/usr/bin/env python3
"""Generate the order confirmation and invoice emails (client round 3).

Same style as the quote email: the head, header (new colour logo) and footer
are read from email-quote-v4.html, so the three emails never drift apart.
Email HTML: nested tables, inline styles, absolute image URLs, Arial only.

    python scripts/email/build_orders.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://biztechdesign.github.io/Bounce-Creative/"

FOREST, FOREST_MID, OAT, PAPER, WHITE, LINE = "#133935", "#33564F", "#EEE9DE", "#F6F3EB", "#FFFFFF", "#DCD6C9"
CORAL, CORAL_TEXT, GREEN, SAGE = "#F37259", "#B93B1C", "#19754C", "#D8E4D1"
F = "Arial, Helvetica, sans-serif"
VAT = 0.20

QUOTE = (ROOT / "email-quote-v4.html").read_text(encoding="utf-8")
HEAD = QUOTE[:QUOTE.index("<body")].replace(
    "    .em-h1{", "    .em-thumb{ display:none !important; }\n    .em-h1{", 1)   # item photos off on phones
HEADER = QUOTE[QUOTE.index("  <!-- ===== Header ===== -->"):QUOTE.index("  <!-- ===== Intro ===== -->")]
FOOTER = QUOTE[QUOTE.index("  <!-- ===== Footer ===== -->"):QUOTE.index("</table>\n\n</td></tr>\n</table>")]

# The basket's order (basket-v4.html): placed, paid, and invoiced.
ORDER = {
    "number": "BCD-100248",
    "invoice": "INV-100248",
    "date": "2 Nov 2026",
    "customer": "Anjana Solanki",
    "company": "Biztech",
    "email": "chirag.t@biztechcs.com",
    "payment": "Visa ending 4242",
    "billing": ["Anjana Solanki", "Biztech", "12 Example Street", "London", "EC1A 1AA", "United Kingdom"],
    "shipping": ["Anjana Solanki", "Biztech", "12 Example Street", "London", "EC1A 1AA", "United Kingdom"],
    "delivery": 12.50,
    "lines": [
        {"name": "CARRO Folding Crate Container Trolley", "sku": "mid-MO6746-03",
         "img": "assets/img/products/office/carro-folding-crate-trolley.jpg",
         "config": ["Front upper &middot; screen printing, 1 colour"], "qty": 25, "each": 22.79},
        {"name": "Minsk Unisex Hybrid Insulated Jacket", "sku": "pf-R1120",
         "img": "assets/img/products/clothing/minsk-jacket-black-heather.jpg",
         "config": ["Black / heather black", "S 10 &middot; M 15 &middot; L 15 &middot; XL 10",
                    "Left chest &amp; impact upper back &middot; embroidery"], "qty": 50, "each": 26.19},
    ],
}


def money(v):
    return f"&pound;{v:,.2f}"


def label(t, colour=FOREST_MID):
    return f'<span style="font-family:{F}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{colour};">{t}</span>'


def totals(o):
    sub = sum(l["qty"] * l["each"] for l in o["lines"])
    net = sub + o["delivery"]
    vat = round(net * VAT, 2)
    return sub, net, vat, net + vat


def header(text):
    return re.sub(r"Quote &middot; [^<]+", text, HEADER, count=1)


def intro(eyebrow, h1, p):
    return f"""  <!-- ===== Intro ===== -->
  <tr><td class="em-pad" style="padding:36px 32px 0;">
    <span style="font-family:{F}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{CORAL_TEXT};">&#9679;&nbsp; {eyebrow}</span>
    <h1 class="em-h1" style="margin:12px 0 0; font-family:{F}; font-size:34px; line-height:1.1; letter-spacing:-0.5px; font-weight:700; color:{FOREST};">{h1}</h1>
    <p style="margin:14px 0 0; font-family:{F}; font-size:15px; line-height:1.6; color:{FOREST_MID};">{p}</p>
  </td></tr>
"""


def meta(cells):
    """Two-column meta box: [(label, value), ...] split left / right."""
    half = (len(cells) + 1) // 2
    def col(items, last):
        rows = '\n        <div style="height:12px;"></div>\n'.join(
            f'        {label(k)}<br>\n        <span style="font-family:{F}; font-size:14px; font-weight:800; color:{FOREST};">{v}</span>'
            for k, v in items)
        border = "" if last else f" border-right:1px solid {LINE};"
        return f"""      <td width="50%" valign="top" class="em-stack" style="padding:16px 18px;{border}">
{rows}
      </td>"""
    return f"""  <!-- ===== Meta ===== -->
  <tr><td class="em-pad" style="padding:24px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}; border:1px solid {LINE};"><tr>
{col(cells[:half], False)}
{col(cells[half:], True)}
    </tr></table>
  </td></tr>
"""


def items(o, invoice=False):
    rows = []
    for l in o["lines"]:
        sub = l["qty"] * l["each"]
        cfg = "<br>".join(l["config"])
        vat_cell = (f'<td align="right" valign="top" style="padding:14px 0 14px 10px; font-family:{F}; font-size:13px; color:{FOREST_MID};">{money(sub * VAT)}</td>'
                    if invoice else "")
        rows.append(f"""      <tr>
        <td width="76" valign="top" class="em-thumb" style="padding:14px 14px 14px 0; border-bottom:1px solid {LINE};"><img src="{BASE}{l["img"]}" width="64" height="64" alt="" style="width:64px; height:64px; border:1px solid {LINE}; background:{WHITE};"></td>
        <td valign="top" style="padding:14px 0; border-bottom:1px solid {LINE}; font-family:{F}; font-size:13px; line-height:1.5; color:{FOREST_MID};">
          <b style="font-size:14px; color:{FOREST};">{l["name"]}</b><br>
          <span style="font-size:11px; letter-spacing:1px; text-transform:uppercase;">{l["sku"]}</span><br>
          {cfg}
        </td>
        <td align="right" valign="top" style="padding:14px 0 14px 10px; border-bottom:1px solid {LINE}; font-family:{F}; font-size:13px; color:{FOREST}; white-space:nowrap;">{l["qty"]} &times; {money(l["each"])}</td>
        {vat_cell.replace('style="', f'style="border-bottom:1px solid {LINE}; ', 1)}
        <td align="right" valign="top" style="padding:14px 0 14px 10px; border-bottom:1px solid {LINE}; font-family:{F}; font-size:14px; font-weight:800; color:{FOREST}; white-space:nowrap;">{money(sub)}</td>
      </tr>""")
    vat_th = (f'<th align="right" style="padding:10px 0 10px 10px; font-family:{F}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID};">VAT</th>'
              if invoice else "")
    return f"""  <!-- ===== Items ===== -->
  <tr><td class="em-pad" style="padding:32px 32px 0;">
    {label("Your order" if not invoice else "Items")}
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="em-prices" style="margin-top:10px; border-top:2px solid {FOREST};">
      <tr>
        <th colspan="2" align="left" style="padding:10px 0; font-family:{F}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID};">Product</th>
        <th align="right" style="padding:10px 0 10px 10px; font-family:{F}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID};">Qty &times; price</th>
        {vat_th}
        <th align="right" style="padding:10px 0 10px 10px; font-family:{F}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID};">{"Net" if invoice else "Subtotal"}</th>
      </tr>
{chr(10).join(rows)}
    </table>
  </td></tr>
"""


def totals_block(o, paid_line):
    sub, net, vat, total = totals(o)
    row = lambda k, v, strong=False: (
        f'<tr><td style="padding:7px 0; font-family:{F}; font-size:{15 if strong else 13}px; {"font-weight:800; " if strong else ""}color:{FOREST if strong else FOREST_MID};">{k}</td>'
        f'<td align="right" style="padding:7px 0; font-family:{F}; font-size:{20 if strong else 13}px; font-weight:800; color:{FOREST};">{v}</td></tr>')
    return f"""  <!-- ===== Totals ===== -->
  <tr><td class="em-pad" style="padding:8px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
      <td class="em-stack" width="45%"></td>
      <td class="em-stack" width="55%" valign="top">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
          {row("Subtotal (ex VAT)", money(sub))}
          {row("Delivery &middot; tracked UK", money(o["delivery"]))}
          {row("VAT 20%", money(vat))}
          <tr><td colspan="2" style="border-top:2px solid {FOREST}; height:4px; line-height:4px; font-size:4px;">&nbsp;</td></tr>
          {row("Total", money(total), True)}
          <tr><td colspan="2" align="right" style="padding:4px 0 0; font-family:{F}; font-size:12px; color:{GREEN}; font-weight:700;">{paid_line}</td></tr>
        </table>
      </td>
    </tr></table>
  </td></tr>
"""


def addresses(o, left="Billing address", right="Delivery address"):
    a = lambda lines: "<br>".join(lines)
    return f"""  <!-- ===== Addresses ===== -->
  <tr><td class="em-pad" style="padding:28px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}; border:1px solid {LINE};"><tr>
      <td width="50%" valign="top" class="em-stack" style="padding:16px 18px; border-right:1px solid {LINE}; font-family:{F}; font-size:13px; line-height:1.6; color:{FOREST};">
        {label(left)}<br>{a(o["billing"])}
      </td>
      <td width="50%" valign="top" class="em-stack" style="padding:16px 18px; font-family:{F}; font-size:13px; line-height:1.6; color:{FOREST};">
        {label(right)}<br>{a(o["shipping"])}
      </td>
    </tr></table>
  </td></tr>
"""


def btn(text, href, solid=True):
    style = (f"background:{FOREST}; color:{OAT}; border:2px solid {FOREST};" if solid
             else f"background:{WHITE}; color:{FOREST}; border:2px solid {FOREST};")
    return (f'<a href="{href}" class="em-btn" style="display:inline-block; padding:13px 22px; font-family:{F}; '
            f'font-size:14px; font-weight:800; text-decoration:none; {style}">{text}</a>')


def page(title, preheader, body):
    return (HEAD.replace(re.search(r"<title>.*?</title>", HEAD).group(0), f"<title>{title}</title>")
            + f"""<body style="margin:0; padding:0; background:{OAT};">
<div style="display:none; max-height:0; overflow:hidden; opacity:0; font-size:1px; line-height:1px; color:{OAT};">{preheader}</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{OAT};">
<tr><td align="center" style="padding:28px 12px;">

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="em-shell" style="width:100%; max-width:640px; background:{WHITE};">

{body}
{FOOTER}</table>

</td></tr>
</table>
<!-- Browser preview only; emitted email HTML is rendered without JavaScript. -->
<script src="assets/js/email-preview-v4.js?v=1"></script>
</body>
</html>
""")


def order_email(o):
    sub, net, vat, total = totals(o)
    points = int(sub // 10)
    steps = [("1", "Artwork check", "Our designers check your files today."),
             ("2", "Proof by email", "You approve a visual of every branding location."),
             ("3", "Production &amp; delivery", "Made after approval, then tracked UK delivery.")]
    step_cells = "\n".join(f"""      <td width="33%" valign="top" class="em-stack" style="padding:0 {10 if i < 2 else 0}px 12px 0;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:2px solid {FOREST};"><tr><td style="padding:12px 0 0; font-family:{F}; font-size:13px; line-height:1.5; color:{FOREST_MID};">
          <b style="display:block; font-size:22px; color:{CORAL_TEXT};">{n}</b><b style="color:{FOREST};">{t}</b><br>{d}
        </td></tr></table>
      </td>""" for i, (n, t, d) in enumerate(steps))
    body = (header(f"Order &middot; {o['date']}")
            + intro("Order confirmed", f'Thank you &mdash; your order is <span style="color:{CORAL_TEXT};">confirmed.</span>',
                    "We&rsquo;ve received your order and payment. Nothing goes to production until you approve a proof &mdash; here&rsquo;s what happens next.")
            + meta([("Order number", "#" + o["number"]), ("Order date", o["date"]),
                    ("Payment", o["payment"]), ("Email address", o["email"])])
            + items(o)
            + totals_block(o, f"&#10003; Paid in full &middot; {o['payment']}")
            + f"""  <!-- ===== What happens next ===== -->
  <tr><td class="em-pad" style="padding:32px 32px 0;">
    {label("What happens next")}
    <h2 style="margin:8px 0 16px; font-family:{F}; font-size:22px; line-height:1.2; font-weight:700; color:{FOREST};">Your proof is <span style="color:{CORAL_TEXT};">on its way.</span></h2>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
{step_cells}
    </tr></table>
  </td></tr>
"""
            + addresses(o)
            + f"""  <!-- ===== Actions ===== -->
  <tr><td class="em-pad" style="padding:28px 32px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr>
      <td class="em-btncell" style="padding-right:10px;">{btn("Track my order &rarr;", "#")}</td>
      <td class="em-btncell">{btn("View invoice", "email-invoice-v4.html", solid=False)}</td>
    </tr></table>
    <p style="margin:10px 0 0; font-family:{F}; font-size:12px; line-height:1.5; color:{FOREST_MID};">Questions about your order? Call <a href="tel:02083189603" style="color:{FOREST}; font-weight:700; text-decoration:none;">020 8318 9603</a> or reply to this email, quoting <b style="color:{FOREST};">#{o["number"]}</b>.</p>
  </td></tr>

  <!-- ===== Points earned ===== -->
  <tr><td class="em-pad" style="padding:32px 32px 36px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{FOREST};"><tr>
      <td valign="middle" style="padding:22px 24px;">
        <span style="font-family:{F}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{CORAL};">Reward points</span>
        <p style="margin:8px 0 0; font-family:{F}; font-size:18px; line-height:1.3; font-weight:700; color:{OAT};">You earned {points} points on this order &mdash; worth {money(points * 0.5)} off next time.</p>
        <p style="margin:8px 0 0; font-family:{F}; font-size:13px; line-height:1.5; color:#C9C2B3;">Added to your account once the order is dispatched.</p>
      </td>
    </tr></table>
  </td></tr>
""")
    return page(f"Order confirmed #{o['number']} | Bounce Creative Designs",
                f"Order #{o['number']} confirmed &mdash; {money(total)} paid. Your proof is on its way.", body)


def invoice_email(o):
    sub, net, vat, total = totals(o)
    body = (header(f"Invoice &middot; {o['date']}")
            + intro("Tax invoice", f'Invoice <span style="color:{CORAL_TEXT};">#{o["invoice"]}</span>',
                    f"Thanks for your order. This is your VAT invoice for order #{o['number']} &mdash; keep it for your records. A PDF copy is attached.")
            + meta([("Invoice number", "#" + o["invoice"]), ("Invoice date", o["date"]),
                    ("Order number", "#" + o["number"]), ("Payment status", f'<span style="color:{GREEN};">Paid &middot; {o["date"]}</span>')])
            + addresses(o, "Invoice to", "Delivered to")
            + items(o, invoice=True)
            + totals_block(o, f"&#10003; Paid {o['date']} &middot; {o['payment']}")
            + f"""  <!-- ===== VAT + supplier ===== -->
  <tr><td class="em-pad" style="padding:28px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}; border:1px solid {LINE};"><tr>
      <td width="50%" valign="top" class="em-stack" style="padding:16px 18px; border-right:1px solid {LINE}; font-family:{F}; font-size:12px; line-height:1.7; color:{FOREST_MID};">
        {label("VAT summary")}<br>
        Standard rate 20% on {money(net)}<br>
        <b style="color:{FOREST};">VAT {money(vat)}</b>
      </td>
      <td width="50%" valign="top" class="em-stack" style="padding:16px 18px; font-family:{F}; font-size:12px; line-height:1.7; color:{FOREST_MID};">
        {label("Supplier")}<br>
        <b style="color:{FOREST};">Bounce Creative Designs Ltd</b><br>
        Unit 18 Clyde Terrace, Forest Hill, London SE23 3BA<br>
        VAT No. GB 127 7569 81 &middot; Company No. 07145385
      </td>
    </tr></table>
  </td></tr>

  <!-- ===== Actions ===== -->
  <tr><td class="em-pad" style="padding:24px 32px 36px;">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr>
      <td class="em-btncell" style="padding-right:10px;">{btn("Download PDF invoice &darr;", "#")}</td>
      <td class="em-btncell">{btn("View order", "email-order-v4.html", solid=False)}</td>
    </tr></table>
    <p style="margin:10px 0 0; font-family:{F}; font-size:12px; line-height:1.5; color:{FOREST_MID};">Need the invoice addressed differently or a purchase order number added? Email <a href="mailto:sales@promo-brand.co.uk" style="color:{CORAL_TEXT}; font-weight:700; text-decoration:none;">sales@promo-brand.co.uk</a>.</p>
  </td></tr>
""")
    return page(f"Invoice #{o['invoice']} | Bounce Creative Designs",
                f"Invoice #{o['invoice']} for order #{o['number']} &mdash; {money(total)}, paid.", body)


def main():
    for name, html in (("email-order-v4.html", order_email(ORDER)), ("email-invoice-v4.html", invoice_email(ORDER))):
        out = ROOT / name
        out.write_text(html, encoding="utf-8")
        print(f"wrote {name}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
