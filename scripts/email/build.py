#!/usr/bin/env python3
"""Generate the quote email in the v4 system.

Email HTML: nested tables, inline styles, absolute image URLs, a 640px
container. Arial throughout - no web fonts.

    python scripts/email/build.py
"""

import pathlib
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://biztechdesign.github.io/Bounce-Creative/"

# Palette - the v4 tokens, as hex for inline use
FOREST = "#133935"
FOREST_MID = "#33564F"
OAT = "#EEE9DE"
PAPER = "#F6F3EB"
WHITE = "#FFFFFF"
LINE = "#DCD6C9"
CORAL = "#F37259"
CORAL_TEXT = "#B93B1C"
GREEN = "#19754C"
SAGE = "#D8E4D1"

FONT = "Arial, Helvetica, sans-serif"
DISPLAY = "Arial, Helvetica, sans-serif"
MONO = "Arial, Helvetica, sans-serif"

QUOTE = {
    "number": "MID-MO6666-TVDAWUGGCF",
    "date": "17 Sep 2026",
    "company": "",
    "email": "chirag.t@biztechcs.com",
    "product": {
        "name": "Gift Card Box With Magnetic Closure HAKO",
        "url": "https://www.bouncecreativedesigns.co.uk/gift-card-box-with-magnetic-closure-hako",
        "code": "Mid-MO6666",
        "img": "assets/img/email/mo6666-03.jpg",
        "colour": "Black",
        "stock": 0,
        "swatches": [("White", "#FFFFFF"), ("Black", "#111111")],
        "desc": "Branded Gift Card Box With Magnetic Closure. Gift card box with magnetic closure in kraft paper. 120 gr/m². Present a giftcard in style with this box. The magnetic closure makes it feel more luxurious and makes it even more fun to unpack the giftcard inside.",
    },
    "config": [
        ("Product colour", "Black"),
        ("Print area", "Top"),
        ("Branding type", "Screen printing"),
        ("Number of colours", "1"),
        ("Product cost (ex VAT)", "£1.46"),
        ("Branding cost (ex VAT)", "£1.58"),
        ("Setup cost (ex VAT)", "£35.00"),
        ("Surcharges (ex VAT)", "£50.00"),
    ],
    "inc_vat": False,
    "source_inc_vat": False,  # Store quote amounts net; format using the email VAT choice.
    "mockup_requested": False,
    "artworks": [
        {"area": "Top", "name": "bounce-logo-ink.png", "url": BASE + "assets/img/bounce-logo-ink.png"},
        {"area": "Bottom", "name": "bounce-logo-white.png", "url": BASE + "assets/img/bounce-logo-white.png"},
        {"area": "Inside", "name": "eco-products.png", "url": BASE + "assets/img/filters/eco-products.png"},
        {"area": "Artwork 4", "name": "co2-products.png", "url": BASE + "assets/img/filters/co2-products.png"},
    ],
    "example_artwork": True,
    "qty": 1,
    "total": "88.04",
    "production": "5–7 working days",
    "delivery": "2–3 working days",
    "min_order": 25,
    "breaks": [
        (1,    "Pre-production", "3.04", "88.04"),
        (25,   "0.00%",  "3.13", "163.25"),
        (50,   "12.78%", "2.73", "221.50"),
        (100,  "18.85%", "2.54", "289.00"),
        (250,  "25.56%", "2.33", "617.50"),
        (500,  "30.03%", "2.19", "1,130.00"),
        (750,  "30.03%", "2.19", "1,677.50"),
        (1000, "34.50%", "2.05", "2,085.00"),
        (1500, "34.50%", "2.05", "3,110.00"),
        (2000, "34.50%", "2.05", "4,135.00"),
        (5000, "36.74%", "1.98", "9,935.00"),
    ],
}

COMPANY = {
    "site": "bouncecreativedesigns.co.uk",
    "email": "enquiries@promo-brand.co.uk",
    "no": "07145385",
    "vat": "GB 127 7569 81",
    "eori": "GB127756981000",
    "address": ["Bounce Creative Designs", "Unit 18 Clyde Terrace", "Forest Hill, London", "SE23 3BA"],
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def img(path):
    return BASE + path


def label(text):
    return (f'<span style="font-family:{MONO}; font-size:11px; letter-spacing:1.5px; '
            f'text-transform:uppercase; color:{FOREST_MID};">{text}</span>')


def btn(text, href, solid=True):
    if solid:
        style = f"background:{FOREST}; color:{OAT}; border:2px solid {FOREST};"
    else:
        style = f"background:{WHITE}; color:{FOREST}; border:2px solid {FOREST};"
    return (f'<a href="{href}" style="display:inline-block; padding:13px 22px; font-family:{FONT}; '
            f'font-size:14px; font-weight:800; text-decoration:none; {style}">{text}</a>')


def preview_hooks(html):
    import re
    def section(name, end_name, callback):
        nonlocal html
        start = html.index(f'<!-- ===== {name} ===== -->')
        end = html.index(f'<!-- ===== {end_name} ===== -->', start)
        html = html[:start] + callback(html[start:end]) + html[end:]
    def meta(s):
        s = re.sub(r'(<span[^>]*>)(#[^<]+)(</span>)', r'<span id="email-number">\2\3', s, count=1)
        s = re.sub(r'(>Date</span><br>\s*)<span ', r'\1<span id="email-date" ', s, count=1)
        s = re.sub(r'(>Company name</span><br>\s*)<span ', r'\1<span id="email-contact-name" ', s, count=1)
        return s.replace('<a href="mailto:', '<a id="email-recipient" href="mailto:', 1)
    section('Quote meta', 'Product', meta)
    def product(s):
        s = s.replace('<img ', '<img id="email-product-image" ', 1)
        s = s.replace('<a href=', '<a data-email-product-link href=')
        s = s.replace('<h2 ', '<h2 id="email-product-title" ', 1)
        s = re.sub(r'(<span[^>]*>)(Product code [^<]+)', r'<span id="email-product-code">\2', s, count=1)
        s = s.replace('<p ', '<p id="email-product-description" ', 1)
        # Replace colour / stock swatches for a live quote, leaving the fixture intact otherwise.
        s = re.sub(r'<table ([^>]*style="margin-top:14px;"[^>]*)>', r'<table id="email-product-colour" \1>', s, count=1)
        return s
    section('Product', 'Your quote', product)
    def summary(s):
        s = re.sub(r'<table ([^>]*style="margin-top:10px;[^>]*)>', r'<table id="email-configuration" \1>', s, count=1)
        s = re.sub(r'<div ([^>]*font-size:36px;[^>]*)>', r'<div id="email-total" \1>', s, count=1)
        s = re.sub(r'<div ([^>]*margin-top:4px;[^>]*)>', r'<div id="email-vat" \1>', s, count=1)
        s = re.sub(r'(Estimated production<br>)<b ', r'\1<b id="email-production" ', s)
        s = re.sub(r'(Estimated delivery<br>)<b ', r'\1<b id="email-delivery" ', s)
        return s
    section('Your quote', 'Actions', summary)
    def actions(s):
        return s.replace('<a href=', '<a data-email-product-link href=')
    section('Actions', 'Price breaks', actions)
    def breaks(s):
        return s.replace('<tr><td ', '<tr id="email-breaks-section"><td ', 1).replace('<table ', '<table id="email-breaks-table" ', 1)
    section('Price breaks', 'Rewards + awards', breaks)
    return html


def build(quote=None):
    q = quote or QUOTE
    p = q["product"]
    tax_label = "Inc VAT" if q.get("inc_vat", False) else "Ex VAT"
    def price_display(value):
        amount = Decimal(str(value).replace(",", ""))
        if q.get("source_inc_vat", False):
            amount /= Decimal("1.2")
        if q.get("inc_vat", False):
            amount *= Decimal("1.2")
        return f"{amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"
    artworks = q.get("artworks")
    if artworks is None:
        artworks = [q["artwork"]] if q.get("artwork") else []
    if artworks:
        artwork_status = "Mock-up requested using your supplied artwork for each branding location." if q.get("mockup_requested") else "Artwork supplied for the selected branding locations."
        if q.get("example_artwork"):
            artwork_status = "Example artwork files for review."
        artwork_name = ""
        items = []
        for artwork in artworks:
            title = (artwork.get("area", "") + ": " if artwork.get("area") else "") + artwork["name"]
            action = '<span style="color:#33564F;">File unavailable</span>'
            if artwork.get("url", "").startswith(("https://", "http://")):
                action = '<a href="' + esc(artwork["url"]) + '" title="' + esc(title) + '" style="color:#d50040;font-weight:bold;text-decoration:underline;">Download</a>'
            items.append('<tr><td style="width:35%;padding:9px 10px;background:#fff;color:#000;font-weight:bold;border-right:2px solid #e7e9e8;">LOGO</td><td style="padding:9px 10px;background:#fff;">' + action + '</td></tr>')
        artwork_image = '<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="max-width:350px;border-collapse:separate;border-spacing:0 10px;font:14px Arial;">' + "".join(items) + '</table>'
    elif q.get("mockup_requested"):
        artwork_status, artwork_name, artwork_image = "Mock-up requested. No artwork is attached to this example quote.", "", ""
    else:
        artwork_status, artwork_name, artwork_image = "No mock-up requested for this quote.", "", ""


    swatches = "".join(
        f'<td style="padding:0 8px 0 0;"><div style="width:22px; height:22px; border-radius:50%; background:{hexv}; '
        f'border:{"3px solid " + FOREST if name == p["colour"] else "1px solid " + LINE}; box-sizing:border-box;" title="{name}"></div></td>'
        for name, hexv in p["swatches"])

    config_rows = "".join(
        f'<tr><td style="padding:7px 0; border-bottom:1px solid {LINE}; font-family:{FONT}; font-size:13px; color:{FOREST_MID};">{esc(k)}</td>'
        f'<td align="right" style="padding:7px 0; border-bottom:1px solid {LINE}; font-family:{FONT}; font-size:13px; font-weight:800; color:{FOREST};">{esc(v)}</td></tr>'
        for k, v in q["config"])

    def brow(n, save, price, sub, i):
        bg = PAPER if i % 2 else WHITE
        if n == 1:
            save_html = f'<span style="color:{FOREST_MID}; font-style:italic;">{save}</span>'
        else:
            save_html = f'<span style="color:{GREEN}; font-weight:700;">Save {save}</span>'
        return (f'<tr style="background:{bg};">'
                f'<td style="padding:9px 12px; font-family:{FONT}; font-size:13px; font-weight:800; color:{FOREST};">{n:,}</td>'
                f'<td style="padding:9px 12px; font-family:{FONT}; font-size:13px;">{save_html}</td>'
                f'<td align="right" style="padding:9px 12px; font-family:{FONT}; font-size:13px; color:{FOREST};">&pound;{price_display(price)}</td>'
                f'<td align="right" style="padding:9px 12px; font-family:{FONT}; font-size:13px; font-weight:800; color:{FOREST};">&pound;{price_display(sub)}</td>'
                f'</tr>')

    break_rows = []
    for i, (n, save, price, sub) in enumerate(q["breaks"]):
        break_rows.append(brow(n, save, price, sub, i))
        if n == 1:
            break_rows.append(
                f'<tr><td colspan="4" style="padding:8px 12px; background:{SAGE}; font-family:{MONO}; font-size:11px; '
                f'letter-spacing:1px; text-transform:uppercase; color:{FOREST};">Minimum order {q["min_order"]} units</td></tr>')
    breaks_html = "".join(break_rows)

    company_line = esc(q["company"]) if q["company"] else f'<span style="color:{FOREST_MID}; font-weight:400;">&mdash;</span>'

    html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-GB">
<head>
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>Your quote #{q["number"]} | Bounce Creative Designs</title>
<style>
  body{{ margin:0; padding:0; background:{OAT}; -webkit-text-size-adjust:100%; }}
  table{{ border-collapse:collapse; }}
  img{{ border:0; display:block; }}
  a{{ color:{CORAL_TEXT}; }}
</style>
</head>
<body style="margin:0; padding:0; background:{OAT};">
<div style="display:none; max-height:0; overflow:hidden; opacity:0; font-size:1px; line-height:1px; color:{OAT};">Your quote for the {esc(p["name"])} &mdash; &pound;{price_display(q["total"])} {tax_label.lower()}, with price breaks from {q["min_order"]} units.</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{OAT};">
<tr><td align="center" style="padding:28px 12px;">

<table role="presentation" width="640" cellpadding="0" cellspacing="0" style="width:640px; max-width:640px; background:{WHITE};">

  <!-- ===== Header ===== -->
  <tr><td style="background:{FOREST}; padding:22px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
      <td valign="middle"><a href="https://www.{COMPANY["site"]}"><img src="{img("assets/img/bounce-logo-white.png")}" width="170" height="50" alt="Bounce Creative Designs" style="width:170px; height:auto;"></a></td>
      <td valign="middle" align="right" style="font-family:{MONO}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{OAT};">Quote &middot; {esc(q["date"])}</td>
    </tr></table>
  </td></tr>

  <!-- ===== Intro ===== -->
  <tr><td style="padding:36px 32px 0;">
    <span style="font-family:{MONO}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{CORAL_TEXT};">&#9679;&nbsp; Your quote</span>
    <h1 style="margin:12px 0 0; font-family:{DISPLAY}; font-size:34px; line-height:1.1; letter-spacing:-0.5px; font-weight:700; color:{FOREST};">Your quote is <span style="color:{CORAL_TEXT};">ready.</span></h1>
    <p style="margin:14px 0 0; font-family:{FONT}; font-size:15px; line-height:1.6; color:{FOREST_MID};">Thanks for configuring with us. Here is the price for the product exactly as you set it up, plus the price breaks if you order more.</p>
  </td></tr>

  <!-- ===== Quote meta ===== -->
  <tr><td style="padding:24px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}; border:1px solid {LINE};"><tr>
      <td width="50%" valign="top" style="padding:16px 18px; border-right:1px solid {LINE};">
        {label("Quote number")}<br>
        <span style="font-family:{FONT}; font-size:14px; font-weight:800; color:{FOREST};">#{esc(q["number"])}</span>
        <div style="height:12px;"></div>
        {label("Date")}<br>
        <span style="font-family:{FONT}; font-size:14px; font-weight:800; color:{FOREST};">{esc(q["date"])}</span>
      </td>
      <td width="50%" valign="top" style="padding:16px 18px;">
        {label("Company name")}<br>
        <span style="font-family:{FONT}; font-size:14px; font-weight:800; color:{FOREST};">{company_line}</span>
        <div style="height:12px;"></div>
        {label("Email address")}<br>
        <a href="mailto:{q["email"]}" style="font-family:{FONT}; font-size:14px; font-weight:800; color:{CORAL_TEXT}; text-decoration:none;">{esc(q["email"])}</a>
      </td>
    </tr></table>
  </td></tr>

  <!-- ===== Product ===== -->
  <tr><td style="padding:32px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="220" valign="top" style="padding-right:24px;">
        <a href="{p["url"]}"><img src="{img(p["img"])}" width="220" height="220" alt="{esc(p["name"])}" style="width:220px; height:220px; border:1px solid {LINE}; background:{WHITE};"></a>
      </td>
      <td valign="top">
        {label("Product code " + esc(p["code"]))}
        <h2 style="margin:8px 0 0; font-family:{DISPLAY}; font-size:20px; line-height:1.25; letter-spacing:-0.3px; font-weight:700; color:{FOREST};"><a href="{p["url"]}" style="color:{FOREST}; text-decoration:none;">{esc(p["name"])}</a></h2>
        <table role="presentation" cellpadding="0" cellspacing="0" style="margin-top:14px;"><tr>
          {swatches}
          <td style="padding-left:6px; font-family:{FONT}; font-size:13px; color:{FOREST_MID};"><b style="color:{FOREST};">{esc(p["colour"])}</b> &middot; Stock level {p["stock"]}</td>
        </tr></table>
        <p style="margin:14px 0 0; font-family:{FONT}; font-size:13px; line-height:1.6; color:{FOREST_MID};">{esc(p["desc"])}</p>
      </td>
    </tr></table>
  </td></tr>

  <!-- ===== Your quote ===== -->
  <tr><td style="padding:32px 32px 0;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}; border:1px solid {LINE};"><tr>
      <td width="55%" valign="top" style="padding:22px 22px 22px 22px; border-right:1px solid {LINE};">
        {label("Your configuration")}
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px; border-top:2px solid {FOREST};">
          {config_rows}
          <tr><td style="padding:7px 0; font-family:{FONT}; font-size:13px; color:{FOREST_MID};">Quantity</td>
              <td align="right" style="padding:7px 0; font-family:{FONT}; font-size:13px; font-weight:800; color:{FOREST};">{q["qty"]}</td></tr>
        </table>
      </td>
      <td width="45%" valign="top" style="padding:22px;">
        {label("Updated price with configuration")}
        <div style="margin-top:8px; font-family:{DISPLAY}; font-size:36px; line-height:1; letter-spacing:-1px; font-weight:700; color:{FOREST};">&pound;{price_display(q["total"])}</div>
        <div style="margin-top:4px; font-family:{MONO}; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:{FOREST_MID};">{tax_label}</div>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:16px; border-top:1px solid {LINE};">
          <tr><td style="padding:10px 0 0; font-family:{FONT}; font-size:12px; line-height:1.5; color:{FOREST_MID};">Estimated production<br><b style="color:{FOREST};">{q["production"]}</b></td></tr>
          <tr><td style="padding:8px 0 0; font-family:{FONT}; font-size:12px; line-height:1.5; color:{FOREST_MID};">Estimated delivery<br><b style="color:{FOREST};">{q["delivery"]}</b></td></tr>
        </table>
      </td>
    </tr></table>
  </td></tr>

  <!-- ===== Actions ===== -->
  <tr><td style="padding:20px 32px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr>
      <td style="padding-right:10px;">{btn("Order online &rarr;", p["url"])}</td>

    </tr></table>
    <div id="email-artwork" style="margin-top:20px; padding:16px; background:#e7e9e8; border:1px solid {LINE};">
      {label("Uploaded artwork")}
      <p id="email-artwork-status" style="margin:10px 0 0; font-family:{FONT}; font-size:13px; color:{FOREST_MID};">{artwork_status}</p>
      <p id="email-artwork-name" style="margin:8px 0; font-family:{FONT}; font-size:13px; color:{FOREST};">{artwork_name}</p>
      <div id="email-artwork-image">{artwork_image}</div>
    </div>
  </td></tr>

  <!-- ===== Price breaks ===== -->
  <tr><td style="padding:36px 32px 0;">
    {label("More price breaks with the same branding")}
    <h2 style="margin:8px 0 16px; font-family:{DISPLAY}; font-size:22px; line-height:1.2; letter-spacing:-0.3px; font-weight:700; color:{FOREST};">Order more, pay less per unit.</h2>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:2px solid {FOREST}; border-bottom:1px solid {LINE};">
      <tr>
        <th align="left" style="padding:10px 12px; font-family:{MONO}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID}; border-bottom:1px solid {LINE};">Quantity</th>
        <th align="left" style="padding:10px 12px; font-family:{MONO}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID}; border-bottom:1px solid {LINE};">Saving</th>
        <th align="right" style="padding:10px 12px; font-family:{MONO}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID}; border-bottom:1px solid {LINE};">Per unit</th>
        <th align="right" style="padding:10px 12px; font-family:{MONO}; font-size:11px; font-weight:400; letter-spacing:1.5px; text-transform:uppercase; color:{FOREST_MID}; border-bottom:1px solid {LINE};">Subtotal</th>
      </tr>
      {breaks_html}
    </table>
    <p style="margin:10px 0 0; font-family:{FONT}; font-size:12px; color:{FOREST_MID};">Same print area, branding type and number of colours at every quantity.</p>
  </td></tr>

  <!-- ===== Rewards + awards ===== -->
  <tr><td style="padding:32px 32px 36px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{FOREST};"><tr>
      <td valign="middle" style="padding:22px 24px;">
        <span style="font-family:{MONO}; font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:{CORAL};">Reward points</span>
        <p style="margin:8px 0 0; font-family:{DISPLAY}; font-size:18px; line-height:1.3; font-weight:700; color:{OAT};">Order online to earn reward points off your next order.</p>
        <p style="margin:8px 0 0; font-family:{FONT}; font-size:13px; line-height:1.5; color:#C9C2B3;">One point for every &pound;10 you spend, worth 50p off next time.</p>
      </td>
      <td width="190" valign="middle" align="right" style="padding:22px 24px 22px 0;">
        <table role="presentation" cellpadding="0" cellspacing="0"><tr>
          <td style="padding-left:8px;"><img src="{img("assets/img/awards/bpma-winners-bounce-creative-designs-promotional-products-uk.png")}" width="80" height="69" alt="BPMA Distributor of the Year 2020 winner" style="width:80px; height:auto; background:{WHITE}; border-radius:50%;"></td>
          <td style="padding-left:8px;"><img src="{img("assets/img/awards/bpma-winners-2023-bounce-creative-designs-promotional-products-uk.png")}" width="80" height="69" alt="BPMA Distributor of the Year 2023 winner" style="width:80px; height:auto; background:{WHITE}; border-radius:50%;"></td>
        </tr></table>
      </td>
    </tr></table>
  </td></tr>

  <!-- ===== Footer ===== -->
  <tr><td style="background:{OAT}; border-top:1px solid {LINE}; padding:28px 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="34%" valign="top" style="font-family:{FONT}; font-size:12px; line-height:1.7; color:{FOREST_MID};">
        <img src="{img("assets/img/bounce-logo-ink.png")}" width="130" height="38" alt="Bounce Creative Designs" style="width:130px; height:auto; margin-bottom:10px;">
        <a href="https://www.{COMPANY["site"]}" style="color:{CORAL_TEXT}; text-decoration:none; font-weight:700;">{COMPANY["site"]}</a><br>
        <a href="mailto:{COMPANY["email"]}" style="color:{FOREST}; text-decoration:none;">{COMPANY["email"]}</a>
      </td>
      <td width="33%" valign="top" style="font-family:{FONT}; font-size:12px; line-height:1.7; color:{FOREST_MID};">
        Company No. {COMPANY["no"]}<br>
        VAT No. {COMPANY["vat"]}<br>
        EORI {COMPANY["eori"]}
      </td>
      <td width="33%" valign="top" style="font-family:{FONT}; font-size:12px; line-height:1.7; color:{FOREST_MID};">
        <b style="color:{FOREST};">{COMPANY["address"][0]}</b><br>
        {"<br>".join(COMPANY["address"][1:])}
      </td>
    </tr></table>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:18px; border-top:1px solid {LINE};">
      <tr><td style="padding-top:14px; font-family:{MONO}; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:{FOREST_MID};">
        <a href="#" style="color:{FOREST}; text-decoration:none;">YouTube</a> &nbsp;&middot;&nbsp;
        <a href="#" style="color:{FOREST}; text-decoration:none;">Facebook</a> &nbsp;&middot;&nbsp;
        <a href="#" style="color:{FOREST}; text-decoration:none;">X</a> &nbsp;&middot;&nbsp;
        <a href="#" style="color:{FOREST}; text-decoration:none;">Instagram</a> &nbsp;&middot;&nbsp;
        <a href="#" style="color:{FOREST}; text-decoration:none;">LinkedIn</a> &nbsp;&middot;&nbsp;
        <a href="#" style="color:{FOREST}; text-decoration:none;">Pinterest</a>
      </td></tr>
      <tr><td style="padding-top:10px; font-family:{FONT}; font-size:11px; color:{FOREST_MID};">&copy; 2026 Bounce Creative Designs Ltd</td></tr>
    </table>
  </td></tr>

</table>

</td></tr>
</table>
</body>
</html>
"""
    return preview_hooks(html)


def main():
    out = ROOT / "email-quote-v4.html"
    html = build()
    browser_scripts = '<script src="assets/js/quote-artwork-v4.js?v=1"></script>\n<script src="assets/js/email-quote-preview-v4.js?v=5"></script>\n'
    out.write_text(html.replace('</body>', browser_scripts + '</body>'), encoding="utf-8")
    print(f"wrote {out.name}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
