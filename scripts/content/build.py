#!/usr/bin/env python3
"""Generate the About page, the News listing and one News article.

Content is the live site's, recomposed in the v4 system. Desktop layout
only: design references for estimation.

    about-v4.html        /about
    news-v4.html         /news/
    news-larq-v4.html    /news/printed-larq-bottle

    python scripts/content/build.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDP = ROOT / "scripts" / "pdp"

CHROME = (PDP / "_chrome.html").read_text(encoding="utf-8")
FOOTER = (PDP / "_footer.html").read_text(encoding="utf-8").replace(
    '<script src="assets/js/pdp-v4.js?v=23"></script>', "")

CSS_V = 4


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def icon(name, size):
    return (f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true">'
            f'<use href="#{name}"/></svg>')


def arrow(size=18):
    return icon("i-arrow", size)


def crumb(items):
    lis = "".join(
        f'<li><a href="{h}">{esc(t)}</a></li>' if h else f'<li aria-current="page">{esc(t)}</li>'
        for t, h in items)
    return f"""  <nav class="crumb" aria-label="Breadcrumb">
    <div class="wrap">
      <ol><li><a href="index-v4.html">Home</a></li>{lis}</ol>
    </div>
  </nav>
"""


def page(title, body, css):
    head = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Manrope:wght@400;500;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style-v4.css?v=114">
<link rel="stylesheet" href="assets/css/list-v4.css?v=21">
<link rel="stylesheet" href="assets/css/category-v4.css?v=3">
<link rel="stylesheet" href="assets/css/{css}?v={CSS_V}">
<script>document.documentElement.className += " js";</script>
"""
    footer = FOOTER.replace("</main>\n", "", 1)
    return head + CHROME + "\n<main id=\"main\" tabindex=\"-1\">\n" + body + "\n</main>\n" + footer


# ==========================================================================
# ABOUT
# ==========================================================================

VALUES = [
    ("i-star", "Exceptional service",
     "We value all of our clients and we are committed to the highest standards of service, whether you are a new client or have been working with us for years. We work hard to raise the bar and deliver exceptional service to every client, every day."),
    ("i-bolt", "Driving change",
     "The promotional branded products sector is forever changing and evolving, and we aim to lead the change. We gain great pleasure when seeking out the new – not just the latest and coolest innovative products, but also new ways of working."),
    ("i-tag", "Uniqueness",
     "We are a design-led team with an eye for detail, aesthetics, and unique, innovative products. No two projects are the same, and every brief is as unique as the brands we work with. We always think outside the box and offer creative solutions."),
    ("i-check", "Trust",
     "We ensure our actions match our words, and we deliver on every promise that we make. We are open and honest, and we always recommend products that are in our clients’ best interests."),
    ("i-team", "Healthy work culture",
     "We ensure all our team members are happy in their job roles by treating everyone with respect, recognising potential, listening to ideas, appreciating efforts, and connecting on a personal level. We have respect for all of our team members and clients regardless of race, religion, or any other individual differences."),
]

STAND_OUT = [
    ("Our staff are highly-trained designers and consultants, not just call handlers.",
     "We train our staff in all aspects of the business, from Photoshop and design skills to invoicing, so they are empowered to handle your project from start to finish."),
    ("We make ordering easy.",
     "Check stock levels, print areas, instant accurate prices and online ordering. Just upload your artwork and a single point of contact would be assigned to your order. Your Promotional Merchandise Consultant will manage the production proofs and make sure delivery timescales are met. If you need further help then your Consultant will handle your enquiry, help you pick out the ideal products for your promotion, mock up design options for you to choose from, and handle the production and delivery timescale."),
    ("We handle all design work in-house,",
     "so you get the benefit of our design expertise plus as many visuals as you want, when you need them (no three-day waits for artwork changes!). It also means we guarantee the quality of the print, so there is no room for errors and no nasty surprises when the product is delivered."),
    ("We only offer products we believe in,",
     "and we only use known and trusted suppliers. This gives us complete confidence in product quality."),
    ("Our high-quality products have staying power and value.",
     "Your branded promotional items will earn pride of place on your customer’s desk or in their home, showcasing your brand for years to come."),
]

BPMA_WHY = [
    "You can buy with complete confidence from BPMA members",
    "Members go through a rigorous vetting process, which reduces your risk when purchasing promotional products",
    "BPMA members are the most respected and reputable within the industry",
    "All members follow the BPMA’s strict Code of Conduct which governs quality, accurate advertising, fair trade terms and managing customer complaints",
]

BPMA_WILL = [
    "Comply with all relevant quality standards, legislation and European Directives to maintain our BPMA accreditation",
    "Consistently follow best industry practices",
    "Offer the highest level of customer service",
    "Stay up-to-date with changes in regulation, industry knowledge and consumer trends",
    "Ethically source merchandise to the highest labour standards",
]

ADVANTAGE = [
    ("Best possible prices, including spot pricing.",
     "The Advantage Group negotiates fantastic deals on members’ behalf and we pass these discounts on to you."),
    ("The latest products to market, fast.",
     "The Advantage Group are continually in touch with the supply chain, meaning we are the first to know about new product lines."),
    ("A secure and trusted supply chain.",
     "The Advantage Group shares our high-quality standards, carefully vetting and selecting all suppliers."),
]

AWARDS = [
    ("awards/bpma-1.svg", "BPMA accredited member"),
    ("awards/psi-1.svg", "PSI member number 17366"),
    ("awards/bounce-creative-designs-award-winning-merchandise1-1.svg", "Distributor of the Year 2019, third place"),
    ("awards/bounce-creative-designs-award-winning-merchandise2-1.svg", "Distributor of the Year 2018, first place"),
    ("awards/bpma-winners-bounce-creative-designs-promotional-products-uk.png", "BPMA Distributor of the Year 2020 winner"),
    ("awards/bpma-winners-2023-bounce-creative-designs-promotional-products-uk.png", "BPMA Distributor of the Year 2023 winner"),
    ("awards/bpma2-1.svg", "British Promotional Merchandise Association member"),
]


def check_list(items, cls="story__list story__list--one"):
    lis = chr(10).join(f'            <li>{icon("i-check", 18)}<span>{esc(i)}</span></li>' for i in items)
    return f'          <ul class="{cls}">\n{lis}\n          </ul>'


def about_page():
    vals = chr(10).join(f"""        <div class="val">
          <svg class="ic val__ic" width="30" height="30" aria-hidden="true"><use href="#{ic}"/></svg>
          <h3>{esc(h)}</h3>
          <p>{esc(p)}</p>
        </div>""" for ic, h, p in VALUES)

    stand = chr(10).join(f"""          <li><span class="pt__n">{i:02d}</span><p><b>{esc(h)}</b> {esc(p)}</p></li>"""
                         for i, (h, p) in enumerate(STAND_OUT, 1))
    adv = chr(10).join(f"""          <li>{icon("i-check", 20)}<p><b>{esc(h)}</b> {esc(p)}</p></li>""" for h, p in ADVANTAGE)
    awards = chr(10).join(f'        <li><img src="assets/img/{f}" alt="{esc(a)}" loading="lazy"></li>' for f, a in AWARDS)

    body = f"""
  <!-- ============ HERO ============ -->
  <section class="lhero" aria-labelledby="about-h">
    <div class="wrap">
      <div class="lhero__grid">
        <div class="lhero__copy">
          <span class="eyebrow eyebrow--onforest">About Bounce Creative Designs</span>
          <h1 id="about-h">Design-led merchandise,<br><span class="hl">valued, used and kept.</span></h1>
          <p>An award-winning merchandise and brand management company based in London. We offer beautiful design paired with high-quality promotional products, all at great value &mdash; sourcing any product you can imagine, from our bestselling pens, notebooks, gadgets, sports and sweets through to innovative bespoke gifts.</p>
          <div class="lhero__cta">
            <a href="#video" class="btn btn--onforest">Watch our story {arrow()}</a>
            <a href="#values" class="btn btn--outline btn--outline-onforest">Our values</a>
          </div>
        </div>
        <div class="lhero__media lhero__media--photo">
          <img src="assets/img/about/team-studio.jpg" alt="The Bounce Creative Designs team reviewing merchandise samples in the studio" width="800" height="600">
        </div>
      </div>
    </div>
  </section>

  <!-- ============ WHAT SETS US APART ============ -->
  <section class="sec" aria-labelledby="apart-h">
    <div class="wrap">
      <div class="sechead" data-reveal>
        <span class="eyebrow">What sets us apart?</span>
        <h2 id="apart-h">Products that showcase your brand <span class="hl">long after the promotion.</span></h2>
        <p>Our passion is in creating promotional products that will be valued, used and kept. This ethos of using high-quality, durable products sits perfectly with our commitment to sustainability.</p>
      </div>
      <div class="vals vals--three" data-reveal>
        <div class="val">
          <svg class="ic val__ic" width="30" height="30" aria-hidden="true"><use href="#i-star"/></svg>
          <h3>High-quality products</h3>
          <p>We only offer products we believe in, and we only use known and trusted suppliers &mdash; including a range made from recycled and reclaimed materials to demonstrate your green credentials.</p>
        </div>
        <div class="val">
          <svg class="ic val__ic" width="30" height="30" aria-hidden="true"><use href="#i-cart"/></svg>
          <h3>Online ordering</h3>
          <p>Check stock levels, print areas and instant accurate prices, then order online. Upload your artwork and a single point of contact is assigned to your order.</p>
        </div>
        <div class="val">
          <svg class="ic val__ic" width="30" height="30" aria-hidden="true"><use href="#i-check"/></svg>
          <h3>100% compliant</h3>
          <p>Accredited members of the British Promotional Merchandise Association. Our designers are experts in the industry, branding techniques and manufacturing processes.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ COMPLIANCE / BPMA ============ -->
  <section class="sec sec--band" aria-labelledby="bpma-h">
    <div class="wrap">
      <div class="split" data-reveal>
        <figure class="split__media">
          <img src="assets/img/about/compliance.jpg" alt="A branded insulated bottle on a desk beside a laptop" width="716" height="529" loading="lazy">
        </figure>
        <div class="split__copy">
          <span class="eyebrow">100% compliant</span>
          <h2 id="bpma-h">Why buy from BPMA <span class="hl">accredited companies?</span></h2>
{check_list(BPMA_WHY)}
          <p class="split__note">Members can also access the BPMA’s powerful education programme, enabling increased customer confidence by demonstrating they are trusted professionals, able to deliver compliant and effective promotional solutions.</p>
          <img class="split__badge" src="assets/img/about/bpma-member.png" alt="BPMA accredited member" width="600" height="101" loading="lazy">
        </div>
      </div>

      <div class="story story--tight" data-reveal>
        <div class="story__aside">
          <span class="eyebrow">BPMA members</span>
          <h2>Accredited members <span class="hl">for over 50 years of best practice.</span></h2>
          <p class="story__stand">We are proud to be accredited members of the BPMA, the professional body dedicated to promoting best practices around the sourcing, manufacturing and distribution of promotional products.</p>
          <img class="story__badge" src="assets/img/about/bpma-psi.png" alt="BPMA accredited member and PSI member" width="600" height="177" loading="lazy">
        </div>
        <div class="story__body">
          <section class="story__part">
            <h3>You can be confident that as BPMA members we will:</h3>
{check_list(BPMA_WILL, "story__list")}
            <p>We are committed to meeting and exceeding BPMA standards, and to achieve this we continually monitor our practices and processes throughout the business.</p>
          </section>
          <section class="story__part">
            <blockquote class="pull">
              <p>&ldquo;Bounce Creative Designs are a vibrant and forward-thinking company with cutting edge design as the key driver for their business. They see promotional merchandise and premiums as more than just the product itself, but how the items they design and source can deliver a high impact to support their clients’ brands and campaign messages. <span class="hl">We are pleased to have them as a member of the BPMA, together we help bring brands to life.</span>&rdquo;</p>
              <footer class="quote__by"><b>Jon Birrell</b> <span>CEO, British Promotional Merchandise Association</span></footer>
            </blockquote>
          </section>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ WHY WE STAND OUT ============ -->
  <section class="sec" aria-labelledby="stand-h">
    <div class="wrap">
      <div class="story" data-reveal>
        <div class="story__aside">
          <span class="eyebrow">Here’s why we stand out</span>
          <h2 id="stand-h">Designers and consultants, <span class="hl">not call handlers.</span></h2>
          <figure class="story__fig">
            <img src="assets/img/about/design-team.jpg" alt="Designers working together around a table in the Bounce studio" width="800" height="600" loading="lazy">
          </figure>
        </div>
        <ol class="pts pts--one">
{stand}
        </ol>
      </div>
    </div>
  </section>

  <!-- ============ WHY DIFFERENT ============ -->
  <section class="sec sec--band" aria-labelledby="diff-h">
    <div class="wrap">
      <div class="split" data-reveal>
        <figure class="split__media">
          <img src="assets/img/about/design-desk.jpg" alt="A designer’s desk with a lamp and computer" width="800" height="600" loading="lazy">
        </figure>
        <div class="split__copy">
          <span class="eyebrow">Why are we different?</span>
          <h2 id="diff-h">Started in a hallway <span class="hl">back in 2013.</span></h2>
          <p>Bounce Creative Designs started in the founder’s hallway operating from a single PC, and rapidly grew into the successful and industry-leading company it is today.</p>
          <p>We are a company centered around design first and foremost, and because of this, we operate differently to others in the industry.</p>
          <p>What sets us apart is our commitment to product quality and great design, our extensive staff training, and the way we support our clients throughout the process. We are passionate about our products, the way we work, and the skills of our team. Once you have worked with us, we’re confident you won’t want to go anywhere else!</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ VALUES ============ -->
  <section class="sec" id="values" aria-labelledby="values-h">
    <div class="wrap">
      <div class="split split--rev split--lead" data-reveal>
        <div class="split__copy">
          <span class="eyebrow">Company values</span>
          <h2 id="values-h">Delivering the <span class="hl">WOW factor.</span></h2>
          <p>Our company values shape our culture and ensure we remain trusted partners of our clients and suppliers.</p>
        </div>
        <figure class="split__media">
          <img src="assets/img/about/team-values.jpg" alt="The Bounce team gathered in the studio" width="1074" height="854" loading="lazy">
        </figure>
      </div>
      <div class="vals vals--five" data-reveal>
{vals}
      </div>
    </div>
  </section>

  <!-- ============ BUYING POWER ============ -->
  <section class="sec sec--band" aria-labelledby="buy-h">
    <div class="wrap">
      <div class="story" data-reveal>
        <div class="story__aside">
          <span class="eyebrow">Buying power</span>
          <h2 id="buy-h">Exceptional products at <span class="hl">competitive prices.</span></h2>
          <p class="story__stand">Our high sales volume gives us fantastic buying power &mdash; so whatever you have in mind, we can source exceptional products for you at great prices.</p>
        </div>
        <div class="story__body">
          <section class="story__part">
            <p>We have cultivated strong relationships with suppliers across the UK, Europe and the Far East, resulting in us winning the Sourcing City Award &mdash; as voted for by suppliers &mdash; for three years running.</p>
          </section>
          <section class="story__part">
            <h3>We are members of the Advantage Group, which gives us some great benefits:</h3>
            <ul class="adv">
{adv}
            </ul>
          </section>
          <section class="story__part">
            <blockquote class="pull">
              <p>&ldquo;The success of Bounce Creative Designs and what has brought them to prominence is by being genuinely creative, innovative and having a great eye for product. They have that intuitive ability to match the right product for the right client, also, within budget and, by working with a proven and trusted supply chain. The team have their finger on the pulse of the latest trends and work hard to bring relevant products to market swiftly for the benefit of their clients. <span class="hl">We have worked with Bounce Creative Designs for over 6 years now and find them a joy to be around.</span> Their energy and passion for the business and their clients is an inspiration, earning them their rightful place up among the peer companies in the industry.&rdquo;</p>
              <footer class="quote__by"><b>Lawrence Angelow</b> <span>Director, Advantage Group</span></footer>
            </blockquote>
          </section>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ VIDEO ============ -->
  <section class="sec" id="video" aria-labelledby="video-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">We sell branded merchandise</span>
          <h2 id="video-h">Two minutes on <span class="hl">how we work.</span></h2>
        </div>
      </div>
      <div class="vid" data-reveal>
        <video controls playsinline preload="none" poster="assets/img/about/video-poster.jpg" width="1280" height="720">
          <source src="https://www.bouncecreativedesigns.co.uk/wp/wp-content/uploads/2021/07/Bounce-Creative-Designs-Compressed2.mp4" type="video/mp4">
        </video>
      </div>
    </div>
  </section>

  <!-- ============ AWARDS ============ -->
  <section class="sec sec--tight sec--band" aria-labelledby="awards-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">We’re really proud</span>
          <h2 id="awards-h">Our awards.</h2>
        </div>
      </div>
      <ul class="awards awards--seven" data-reveal>
{awards}
      </ul>
    </div>
  </section>

  <!-- ============ NEWSLETTER ============ -->
  <section class="sec" aria-labelledby="nl-h">
    <div class="wrap">
      <div class="newsband" data-reveal>
        <div>
          <span class="eyebrow">Get newsletter updates</span>
          <h2 id="nl-h">New products, offers and ideas, <span class="hl">once a month.</span></h2>
        </div>
        <form class="signup" action="#" onsubmit="return false;">
          <div class="signup__field">
            <input type="email" name="email" autocomplete="email" placeholder="Enter your email address" aria-label="Email address">
            <button class="btn btn--solid" type="submit">Sign up</button>
          </div>
          <span class="signup__note">No spam. Unsubscribe any time.</span>
        </form>
      </div>
    </div>
  </section>
"""
    return page("About Bounce Creative Designs", crumb([("About", None)]) + body, "about-v4.css")


# ==========================================================================
# NEWS
# ==========================================================================

POSTS = [
    {"slug": "news-larq-v4.html", "img": "news/larq.jpg", "date": "7 September 2026", "cat": "Product news",
     "title": "Future of Hydration with the LARQ PureVis™ 2.0 Water Bottle",
     "ex": "Promotional LARQ bottle – the self-cleaning water bottle. Discover the future of hydration with the LARQ PureVis™ 2.0.",
     "alt": "A woman drinking from a LARQ PureVis bottle at an outdoor table"},
    {"slug": "#", "img": "news/Custom-Keyring-Set-600x470.jpg", "date": "August 2026", "cat": "Industry news",
     "title": "Smart Merchandise Buying",
     "ex": "Smart promotional merchandise buying with Bounce Creative Designs – don’t let print quality let your merchandise down.",
     "alt": "Branded keyring and compact mirror gift set"},
    {"slug": "#", "img": "news/Custom-Advent-Calendars-600x470.jpg", "date": "August 2026", "cat": "Product news",
     "title": "Chocolate Calendar Custom Gifts",
     "ex": "Promotional custom chocolate advent calendars. Get ready for Christmas with custom advent calendars from Bounce Creative Designs.",
     "alt": "Custom printed chocolate advent calendars"},
    {"slug": "#", "img": "news/Lindt-Advents-600x470.jpg", "date": "August 2026", "cat": "Product news",
     "title": "Lindt Advent Calendars",
     "ex": "Promotional Lindt chocolate advent calendars. Discover the magic of Lindt advent calendars and festive gifts this season.",
     "alt": "Branded Lindt chocolate advent calendar gift box"},
    {"slug": "#", "img": "news/copper.jpg", "date": "August 2026", "cat": "Product news",
     "title": "Copper Vacuum Insulated Bottles",
     "ex": "Promotional copper bottles. Discover the perfect blend of style and function: copper vacuum insulated bottles with your brand.",
     "alt": "Two navy copper vacuum insulated bottles on a peach background"},
    {"slug": "#", "img": "news/parka.jpg", "date": "August 2026", "cat": "Eco",
     "title": "IQONIQ Thelon Recycled Polyester Parka Jacket: Style Meets Sustainability",
     "ex": "Promotional recycled parka jacket. Discover the IQONIQ Thelon recycled polyester parka jacket: style meets sustainability.",
     "alt": "Models wearing IQONIQ Thelon recycled parka jackets"},
]

CATEGORIES = ["Reviews", "Eco", "Industry news", "Product news", "Business news"]

MONTHS = ["September 2026", "August 2026", "June 2026", "May 2026", "April 2026", "March 2026", "February 2026",
          "October 2025", "August 2024", "May 2024", "April 2024", "March 2024", "February 2024", "January 2024",
          "November 2023", "August 2023", "July 2023", "June 2023", "February 2023", "January 2023",
          "October 2022", "July 2022", "May 2022", "April 2022", "March 2022", "February 2022",
          "November 2021", "February 2021", "January 2021", "December 2020", "November 2020", "October 2020",
          "July 2020", "March 2020", "May 2019"]


def post_card(p):
    return f"""          <a href="{p["slug"]}" class="post">
            <span class="post__media"><img src="assets/img/{p["img"]}" alt="{esc(p["alt"])}" loading="lazy"></span>
            <span class="post__meta">{esc(p["cat"])} &middot; {esc(p["date"])}</span>
            <h3 class="post__title">{esc(p["title"])}</h3>
            <span class="post__ex">{esc(p["ex"])}</span>
            <span class="post__cta">Read the story {icon("i-arrow", 16)}</span>
          </a>"""


def news_page():
    lead, rest = POSTS[0], POSTS[1:]
    cards = chr(10).join(post_card(p) for p in rest)
    cats = chr(10).join(f'            <li><a href="#"{" aria-current=\"page\"" if i == 0 else ""}>{esc(c)}</a></li>'
                        for i, c in enumerate(["All stories"] + CATEGORIES))
    months = "".join(f"<option>{esc(m)}</option>" for m in MONTHS)
    pages = "".join(f'<a href="#" class="pager__link"{" aria-current=\"page\"" if n == 1 else ""}>{n}</a>' for n in range(1, 13))

    body = f"""
  <section class="sec sec--flush" aria-labelledby="news-h">
    <div class="wrap">
      <div class="newshead">
        <div>
          <span class="eyebrow">News</span>
          <h1 id="news-h">Stories, launches <span class="hl">and ideas.</span></h1>
          <p>Product launches, buying guides and what we have been working on &mdash; from the Bounce studio.</p>
        </div>
        <form class="sortbar" onsubmit="return false;">
          <span class="sortbar__count">Page <b>1</b> of 12</span>
          <label class="sortbar__sort">Sort by
            <select aria-label="Sort stories"><option>Date</option><option>Title</option></select>
          </label>
        </form>
      </div>

      <div class="newsgrid">
        <aside class="newsside">
          <section class="nsec" aria-labelledby="cat-h">
            <h2 class="nsec__t" id="cat-h">Category</h2>
            <ul class="nsec__list">
{cats}
            </ul>
          </section>
          <section class="nsec" aria-labelledby="month-h">
            <h2 class="nsec__t" id="month-h">Month</h2>
            <label class="nsec__select"><span class="vh">Browse by month</span>
              <select><option>All months</option>{months}</select></label>
          </section>
          <section class="nsec" aria-labelledby="search-h">
            <h2 class="nsec__t" id="search-h">Search articles</h2>
            <form class="nsec__search" onsubmit="return false;">
              <input type="search" placeholder="Enter keywords" aria-label="Search articles">
              <button class="btn btn--solid btn--sm" type="submit" aria-label="Search">{icon("i-search", 16)}</button>
            </form>
          </section>
        </aside>

        <div class="newsmain">
          <a href="{lead["slug"]}" class="lead" data-reveal>
            <span class="lead__media"><img src="assets/img/{lead["img"]}" alt="{esc(lead["alt"])}" width="600" height="470"></span>
            <span class="lead__copy">
              <span class="post__meta">Latest &middot; {esc(lead["cat"])} &middot; {esc(lead["date"])}</span>
              <h2 class="lead__title">{esc(lead["title"])}</h2>
              <span class="post__ex">{esc(lead["ex"])}</span>
              <span class="post__cta">Read the story {icon("i-arrow", 16)}</span>
            </span>
          </a>

          <div class="posts posts--news" data-reveal>
{cards}
          </div>

          <nav class="pager" aria-label="Pagination">
            {pages}
            <a href="#" class="pager__next">Next page {icon("i-arrow", 16)}</a>
          </nav>
        </div>
      </div>
    </div>
  </section>
"""
    return page("News | Bounce Creative Designs", crumb([("News", None)]) + body, "news-v4.css")


# ==========================================================================
# ARTICLE
# ==========================================================================

LARQ_FEATURES = [
    ("2-stage filtration and UV-C purification:", "The bottle doesn’t just filter your water; it actively purifies it. The UV-C LED in the cap activates every two hours automatically, zapping away bacteria and odours to keep your bottle spotless and your water pure."),
    ("Manual PureVis™ cycle:", "Want to refresh your bottle on demand? Just press a button, and the UV-C purification kicks in for an extra clean boost."),
    ("Long-lasting battery life:", "Forget daily charging – this bottle runs for 2 to 3 weeks on a full charge, conveniently powered through a USB-C port. Talk about low maintenance!"),
    ("Smart hydration tracking:", "Equipped with sensors, the bottle tracks your water intake automatically. Paired with the LARQ app, it gives you personalised insights and progress updates, making hydration goals easier and more fun to hit."),
    ("User-friendly design:", "The cap includes a built-in, detachable soft-touch handle, perfect for carrying around whether you’re hitting the gym, the office, or your favourite hiking trail."),
]

ONLINE_POINTS = [
    ("Instant pricing:", "No more waiting days for quotes or guessing what your final costs might be. Online platforms show you the exact prices upfront, so you can make informed decisions without any surprises."),
    ("Easy customisation:", "Want your logo on a mug or a custom message on a tote bag? With just a few clicks, you can explore branding options and see live prices."),
    ("Order anytime, anywhere:", "Whether you’re at your desk at work, on your couch at home, or even travelling, placing an order is always just a tap away. This flexibility means you’re not tied to business hours or limited by location."),
]

BENEFITS = [
    ("BPMA accreditation", "Bounce Creative Designs is a BPMA (British Promotional Merchandise Association) accredited company. Buying from BPMA members can provide you with confidence in your purchase as they have gone through a rigorous vetting process, reducing your risk when purchasing promotional products."),
    ("Extensive knowledge and experience", "Bounce Creative Designs is an award-winning promotional merchandise supplier with extensive knowledge and experience in the promotional and corporate gift industry. Their expertise allows them to provide solutions tailored to your specific needs."),
    ("Wide range of sustainable and eco-friendly options", "From notebooks made from recycled materials to branded merchandise with eco-friendly options, they have a selection of products that align with your environmental values."),
    ("Quality and creative branding service", "Bounce Creative Designs is committed to providing quality products and a creative branding service to their clients. Their goal is to help you effectively promote your brand while maintaining high standards of design and creativity."),
    ("Recognition and awards", "Bounce Creative Designs has received recognition and awards for their work in the industry. Their reputation and track record of excellence suggest that they are a reliable choice when it comes to promotional products."),
]

LARQ_PRODUCTS = [
    ("news/larq-680.jpg", "LARQ PureVis™ 2.0 680 ml water bottle", "75.93"),
    ("news/larq-1000.jpg", "LARQ PureVis™ 2.0 1000 ml water bottle", "83.52"),
    ("news/larq-swig-680.jpg", "LARQ Swig Top 680 ml water bottle", "42.91"),
    ("news/larq-swig-1000.jpg", "LARQ Swig Top 1000 ml water bottle", "50.32"),
]


def bold_list(items):
    return chr(10).join(f'          <li>{icon("i-check", 18)}<p><b>{esc(h)}</b> {esc(p)}</p></li>' for h, p in items)


def article_page():
    feats = bold_list(LARQ_FEATURES)
    online = bold_list(ONLINE_POINTS)
    bens = chr(10).join(f"""          <div class="ben">
            <span class="ben__n">{i:02d}</span>
            <h3>{esc(h)}</h3>
            <p>{esc(p)}</p>
          </div>""" for i, (h, p) in enumerate(BENEFITS, 1))
    prods = chr(10).join(f"""            <a href="#" class="mini">
              <span class="mini__media"><img src="assets/img/{img}" alt="{esc(n)}" loading="lazy"></span>
              <span class="mini__name">{esc(n)}</span>
              <span class="mini__price">From &pound;{pr}</span>
            </a>""" for img, n, pr in LARQ_PRODUCTS)

    body = f"""
  <article class="art" aria-labelledby="post-h">
    <header class="arthead">
      <div class="wrap">
        <a href="news-v4.html" class="arthead__back">{icon("i-arrow", 14)}Back to news</a>
        <span class="eyebrow">Product news</span>
        <h1 id="post-h">Future of hydration with the <span class="hl">LARQ PureVis™ 2.0</span> water bottle</h1>
        <p class="arthead__stand">Promotional LARQ bottle &mdash; the self-cleaning water bottle.</p>
        <dl class="arthead__meta">
          <div><dt>Author</dt><dd>Bounce Creative</dd></div>
          <div><dt>Published</dt><dd><time datetime="2026-09-07">7 September 2026</time></dd></div>
          <div><dt>Reading time</dt><dd>6 min</dd></div>
        </dl>
      </div>
    </header>

    <div class="wrap">
      <figure class="arthero">
        <img src="assets/img/news/larq-hero.jpg" alt="A woman drinking from a printed LARQ PureVis 2.0 bottle at an outdoor table" width="1350" height="900">
      </figure>

      <div class="artgrid">
        <div class="artbody">
          <h2>Discover the future of hydration with the LARQ PureVis™ 2.0</h2>
          <p>Welcome to a fresh take on staying hydrated! If you’ve ever wished your promotional water bottle could do more than just hold water, the LARQ PureVis™ 2.0 might just be the game-changer you’ve been waiting for. This week, we’re diving into the features of a new water bottle that not only keeps your water clean but also tracks your hydration habits smartly and effortlessly.</p>

          <figure class="artfig artfig--pair">
            <img src="assets/img/news/larq-3.jpg" alt="LARQ PureVis 2.0 bottle in white with its gift box and app" width="313" height="470" loading="lazy">
            <img src="assets/img/news/larq-4.jpg" alt="LARQ PureVis 2.0 self-cleaning bottle being filled" width="313" height="470" loading="lazy">
          </figure>

          <h2>Why the LARQ PureVis™ 2.0 stands out</h2>
          <p>At first glance, it’s a sleek, 1000 ml bottle &mdash; but beneath that stylish exterior lies a powerhouse of innovation. The printed LARQ PureVis™ 2.0 combines self-cleaning and water filtration technologies to deliver water that tastes better and feels fresher. Here’s what makes it truly special:</p>
          <ul class="artlist">
{feats}
          </ul>
          <p>The LARQ PureVis™ 2.0 isn’t just about technology &mdash; it’s about enhancing your everyday routine by making clean water accessible and hydration effortless.</p>

          <h2>Keeping it fresh</h2>
          <p>One key to maintaining optimal performance is regular filter replacement. This ensures your water stays as crisp and clean as intended. It’s a small task that makes a big difference in your bottle’s effectiveness.</p>
          <p>Invest in smart promotional products with Bounce Creative Designs, print smart, and watch your merchandise do the talking &mdash; loud and proud.</p>

          <blockquote class="artpull">
            <p>If you’re someone who values clean water and smart tech that blends seamlessly into daily life, the LARQ PureVis™ 2.0 offers an impressive package. It’s more than a water bottle &mdash; it’s a hydration companion designed to keep you refreshed and informed.</p>
          </blockquote>

          <figure class="artfig">
            <img src="assets/img/news/larq-black.jpg" alt="LARQ PureVis 2.0 in black with the smaller 680 ml bottle" width="600" height="384" loading="lazy">
            <figcaption>Also available in black and a smaller 680 ml &mdash; <a href="#">LARQ PureVis™ 2.0 680 ml water bottle</a>.</figcaption>
          </figure>

          <div class="artlead">
            <p>Ordering promotional products directly online offers unmatched convenience and control. With fast and efficient ordering, transparent pricing, and instant access to exact costs, you can make informed decisions without waiting for quotes.</p>
            <p class="artlead__sub">Explore branding options at your fingertips, customise products in just a few clicks, and place orders anytime, from anywhere. It’s the quickest, easiest, and most transparent way to source high-quality promotional merchandise for your business.</p>
          </div>

          <h2>Why this matters for your business</h2>
          <p>Promotional products are a powerful marketing tool, but they lose impact if the ordering experience is complicated. By simplifying how you source these items, you free up time and energy to focus on what really counts &mdash; building relationships with your customers and growing your brand.</p>
          <p>Online ordering also means you can quickly replenish stock, try out new products without long lead times, and respond to changing marketing needs with agility. It’s a win-win situation for efficiency and creativity.</p>
          <p>Plus, the selection is often vast, covering everything from classic pens and apparel to trendy tech gadgets and eco-friendly items. All high-quality, ready to make your brand shine.</p>
          <ul class="artlist">
{online}
          </ul>

          <h2>Bringing the human touch back to online ordering</h2>
          <p>At Bounce Creative Designs, we believe that online orders shouldn’t feel cold or impersonal. Instead, they should feel like a conversation &mdash; with real people who care about your project just as much as you do.</p>
          <p>So, what does that mean for you when you place an order with us? It means that every piece of artwork gets a thorough, careful check by our team before anything goes into production. We don’t just hit “print” and hope for the best; we provide proofs to you so you can see exactly how your design will look. That way, there are no surprises, only satisfaction.</p>
          <p>And it doesn’t stop there. Once your order is placed, we’re not disappearing into the digital void. We’re here &mdash; ready to answer your calls and emails, to handle any questions or tweaks you might want to make. This blend of technology and human attention ensures that your experience is smooth, friendly, and reliable.</p>
          <p>In an age dominated by automation, Bounce Creative Designs stands out by keeping the heart in the process. We’re proud to offer the convenience of online ordering without losing the warmth and care that comes from human interaction.</p>

          <h2>Product recommendation</h2>
          <figure class="artfig artfig--rec">
            <img src="assets/img/news/nordic-drift.jpg" alt="Nordic Drift Trail RCS single-wall water bottle 750 ml" width="313" height="470" loading="lazy">
            <figcaption><b>Nordic Drift Trail RCS single-wall water bottle, 750 ml</b> <a href="#">View product {arrow(14)}</a></figcaption>
          </figure>

          <h2>Why buy promotional products from Bounce Creative Designs?</h2>
          <p>When considering purchasing promotional products from Bounce Creative Designs in the UK, there are several benefits to keep in mind.</p>
          <div class="bens">
{bens}
          </div>
          <p>By choosing Bounce Creative Designs as your promotional products supplier, you can benefit from their BPMA accreditation, extensive knowledge and experience, wide range of sustainable options, quality branding service, and their recognition in the industry.</p>

          <blockquote class="artpull artpull--close">
            <p>Bounce Creative Designs stands out not just for exceptional creative product sourcing and online instant ordering, but for an exceptional customer experience. When you reach out, you connect with a real person &mdash; a human at the end of the phone or email &mdash; ready to listen, understand, and deliver with care. It’s personalised service that makes every interaction feel thoughtful, easy, and truly valued.</p>
          </blockquote>

          <nav class="artnav" aria-label="More articles">
            <a href="#" class="artnav__prev">{icon("i-arrow", 16)}<span><small>Previous article</small>Smart merchandise buying</span></a>
            <div class="share">
              <span class="share__t">Share</span>
              <a href="#" aria-label="Share on Pinterest">{icon("i-pinterest", 16)}</a>
              <a href="#" aria-label="Share on X">{icon("i-x", 16)}</a>
              <a href="#" aria-label="Share on Facebook">{icon("i-facebook", 16)}</a>
              <a href="#" aria-label="Share">{icon("i-share", 16)}</a>
            </div>
          </nav>
        </div>

        <aside class="artside">
          <section class="sidecard" aria-labelledby="shop-h">
            <span class="eyebrow">Featured in this story</span>
            <h2 id="shop-h">Shop the LARQ range</h2>
            <div class="minis">
{prods}
            </div>
            <a href="products-v4.html" class="btn btn--outline btn--sm">All drinkware {icon("i-arrow", 16)}</a>
          </section>
          <section class="sidecard sidecard--forest">
            <span class="eyebrow eyebrow--onforest">Order online</span>
            <p><b>Instant prices, free artwork check, a proof before print.</b> Upload your logo and a named consultant follows your order from proof to delivery.</p>
            <a href="#" class="btn btn--onforest btn--sm">Get a visual {icon("i-arrow", 16)}</a>
          </section>
        </aside>
      </div>
    </div>
  </article>

  <!-- ============ MORE STORIES ============ -->
  <section class="sec sec--band" aria-labelledby="more-h">
    <div class="wrap">
      <div class="sechead sechead--row" data-reveal>
        <div class="sechead__t">
          <span class="eyebrow">More stories</span>
          <h2 id="more-h">Keep <span class="hl">reading.</span></h2>
        </div>
        <a href="news-v4.html" class="tlink">All news {icon("i-arrow", 16)}</a>
      </div>
      <div class="posts" data-reveal>
{chr(10).join(post_card(p) for p in POSTS[1:4])}
      </div>
    </div>
  </section>
"""
    return page("Future of Hydration with the LARQ PureVis™ 2.0 Water Bottle | News | Bounce Creative Designs",
                crumb([("News", "news-v4.html"), ("Future of Hydration with the LARQ PureVis™ 2.0 Water Bottle", None)]) + body,
                "news-v4.css")


PAGES = [
    ("about-v4.html", about_page),
    ("news-v4.html", news_page),
    ("news-larq-v4.html", article_page),
]


def main():
    for name, fn in PAGES:
        out = ROOT / name
        out.write_text(fn(), encoding="utf-8")
        print(f"wrote {name}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
