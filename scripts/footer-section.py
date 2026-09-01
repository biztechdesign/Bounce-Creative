"""Rebuild the footer.

Creative device is taken from the brand itself: the Bounce logo is a matrix of
dots, so the footer ground carries that dot grid, and the wordmark is set
oversized along the baseline as texture rather than as another shout. No second
CTA - the closing section above already asks for the enquiry.
"""
import io, os, re

ROOT = r"d:\work\Bounce-Creative"
ICONS = r"C:\Users\CHIRAG~1.THA\AppData\Local\Temp\claude\d--work-Bounce-Creative\0bc03f9d-03ca-46d1-a37c-28abe06872f7\scratchpad\icons"
os.chdir(ROOT)


def sym(sid, f):
    svg = io.open(os.path.join(ICONS, f + '.svg'), encoding='utf-8').read()
    inner = re.search(r'viewBox="0 0 24 24">(.*)</svg>', svg, re.S).group(1).strip()
    return f'  <symbol id="{sid}" viewBox="0 0 24 24">{inner}</symbol>'


def ic(sid, size):
    return f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true"><use href="#{sid}"/></svg>'


COLS = [
    ('Shop', ['All products', 'Bags', 'Drinkware', 'Clothing', 'Tech', 'Eco &amp; Sustainable']),
    ('Services', ['Create a Swag Box', 'Full colour printing', 'Online order products',
                  'Bespoke sourcing', 'Global fulfilment']),
    ('Company', ['About Bounce', 'Sustainability &amp; ESG', 'Case studies', 'Careers', 'Contact']),
    ('Help', ['Artwork guidelines', 'Delivery &amp; lead times', 'Request samples',
              'Track my order', 'FAQs']),
]

cols = '\n'.join(
    '      <div class="ftr__col">\n'
    f'        <h4>{title}</h4>\n        <ul>\n'
    + '\n'.join(f'          <li><a href="#">{l}</a></li>' for l in links)
    + '\n        </ul>\n      </div>'
    for title, links in COLS)

SOCIAL = {
 'LinkedIn': '<path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0ZM.5 8h4V24h-4V8Zm7.5 0h3.8v2.2h.05c.53-1 1.83-2.2 3.77-2.2 4.03 0 4.78 2.65 4.78 6.1V24h-4v-7.9c0-1.9-.03-4.3-2.62-4.3-2.62 0-3.02 2.05-3.02 4.16V24H8V8Z"/>',
 'Instagram': '<rect x="2.5" y="2.5" width="19" height="19" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.6" cy="6.4" r="1.2"/>',
 'X': '<path d="M18.2 2h3.4l-7.4 8.5L23 22h-6.8l-5.3-7-6.1 7H1.4l7.9-9.1L1 2h7l4.8 6.4L18.2 2Zm-1.2 18h1.9L7.1 3.9H5.1L17 20Z"/>',
}
social = '\n'.join(
    f'          <a href="#" aria-label="{k}"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">{v}</svg></a>'
    for k, v in SOCIAL.items())

footer = f'''<footer class="ftr">
  <div class="ftr__dots" aria-hidden="true"></div>

  <div class="wrap">
    <div class="ftr__top">
      <div class="ftr__brand">
        <a href="#" class="logo">
          <img src="assets/img/bounce-logo-white.png" alt="Bounce Creative Designs" width="240" height="71">
        </a>
        <p class="ftr__blurb">Design-led promotional merchandise from London since 2013. 25,000+ products, real carbon data, and a team that answers the phone.</p>

        <ul class="ftr__contact">
          <li>{ic('i-phone', 16)}<a href="tel:+442071014444">020 7101 4444</a></li>
          <li>{ic('i-letter', 16)}<a href="mailto:hello@bouncecreativedesigns.co.uk">hello@bouncecreativedesigns.co.uk</a></li>
          <li>{ic('i-pin', 16)}<span>London, United Kingdom</span></li>
        </ul>

        <div class="ftr__social">
{social}
        </div>
      </div>

{cols}
    </div>

    <div class="ftr__bot">
      <p>&copy; 2026 Bounce Creative Designs Ltd. Registered in England &amp; Wales.</p>
      <ul>
        <li><a href="#">Privacy</a></li>
        <li><a href="#">Terms</a></li>
        <li><a href="#">Cookies</a></li>
        <li><a href="#">Modern slavery statement</a></li>
      </ul>
      <div class="ftr__pay">
        <span>VISA</span><span>MASTERCARD</span><span>AMEX</span><span>BACS</span>
      </div>
      <a href="#top" class="ftr__top-link" aria-label="Back to top">{ic('i-up', 16)}</a>
    </div>
  </div>

  <div class="ftr__mark" aria-hidden="true">
    <span>bounce</span>
    <i></i><i></i><i></i>
  </div>
</footer>'''

s = io.open('index.html', encoding='utf-8').read()
s = s[:s.index('<footer class="ftr">')] + footer + '\n\n' + s[s.index('<script src="assets/js/typography.js">'):]

# new icons into the sprite
s = s.replace('  <symbol id="i-star"',
              sym('i-letter', 'letter-linear') + '\n' + sym('i-pin', 'map-point-linear') + '\n'
              + sym('i-up', 'alt-arrow-up-linear') + '\n' + '  <symbol id="i-star"')
io.open('index.html', 'w', encoding='utf-8').write(s)
print('footer rebuilt | contact rows:', s.count('ftr__contact'), '| mark:', s.count('ftr__mark'))
