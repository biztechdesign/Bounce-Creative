"""Add the standards / credentials tabbed section.

Copy is lifted from the live site's own tab panels. The right column carries three
facts drawn from that same copy rather than a photograph - Bounce has no distinct
image for seven tabs, and a credentials section reads better as type and fact than
as stock imagery.
"""
import io, os, re

ROOT = r"d:\work\Bounce-Creative"
os.chdir(ROOT)

# label, eyebrow, heading, [paragraphs], [(term, definition) x3]
TABS = [
 ('Promotional', 'Why promotional products', 'The reach a campaign keeps.',
  ["Whether it is an event, a product launch, a rebrand or a marketing incentive, promotional items offer a tangible reach that drives awareness over a far longer time frame than a paid impression.",
   "BPMA research found that 81% of consumers keep a promotional item for at least a year, and that promotional items are twice as likely to motivate consumer action."],
  [('81%', 'Keep an item for at least a year'), ('2x', 'More likely to motivate action'),
   ('BPMA', 'Source of the research')]),

 ('Branding', 'Quality branded merchandise', 'Retail quality, ordered at 2am.',
  ["Our promotional products are more than the old-fashioned giveaway — they are genuinely good products, alongside retail brands you already know.",
   "Use the filters to find the right gift, with instant prices and live stock levels available around the clock, so you can order whenever it suits you."],
  [('24/7', 'Instant prices and live stock'), ('3,000+', 'Branded products in the range'),
   ('Retail', 'Quality benchmark, not giveaway')]),

 ('GRS', 'Global Recycle Standard', 'Recycled content, independently verified.',
  ["The Global Recycled Standard tracks and verifies the recycled content of a finished product, defining the requirements that make a recycled-content claim accurate.",
   "The label carries strict guidelines and a certification process backed by independent certification of the input material, and it also addresses the social conditions of production."],
  [('Verified', 'Independent certification of inputs'),
   ('Tracked', 'Chain of custody through the supply chain'),
   ('Social', 'Labour and safety criteria included')]),

 ('RCS', 'Recycled Claim Standard', 'A claim you can follow back.',
  ["The Recycled Claim Standard is a voluntary international content claim standard that gives credibility to recycled material claims by tracking recycled input through the supply chain.",
   "It applies chain of custody requirements, so the claim on the finished product can be traced back to the material it was made from."],
  [('Voluntary', 'International content claim standard'),
   ('Input', 'Recycled material tracked from source'),
   ('Custody', 'Chain of custody requirements applied')]),

 ('Blockchain', 'Promotional products and blockchain', 'Transparency, on the record.',
  ["We expect it will not be long before promotional products carry some form of blockchain record. Transparency is becoming vital to consumers and to product reputation as sustainability demands grow.",
   "The textile side will benefit first, alongside innovations already in use such as the AWARE tracer, which verifies recycled content physically rather than on paper."],
  [('AWARE', 'Tracer already verifying recycled content'),
   ('Anti-greenwash', 'Claims recorded, not asserted'),
   ('Textiles', 'First category to adopt it')]),

 ('ESG', 'Environmental, social, governance', 'Merchandise your report can carry.',
  ["ESG forms part of Agenda 2030 and the sustainable development goals, previously known as the millennium development goals.",
   "A growing environmental movement has pushed companies to rethink products and packaging. Choosing merchandise for ESG means weighing the materials, the production method and the impact of each item."],
  [('Agenda 2030', 'The framework ESG sits within'),
   ('Materials', 'Weighed alongside production method'),
   ('Reportable', 'Data formatted for your disclosure')]),

 ('CO&#8322;', 'Choose lower carbon emissions', 'CO&#8322; — changing the way we give.',
  ["We are committed to lowering our carbon emissions, and our CO2 collection publishes the carbon footprint of each product so you can see it before you order.",
   "The scope is cradle-to-grave: the life cycle assessment covers all greenhouse gas emissions a product generates, from raw material extraction to end-of-life treatment."],
  [('Per product', 'Footprint published on every item'),
   ('Cradle-to-grave', 'Full life cycle assessment scope'),
   ('All GHG', 'Not carbon dioxide alone')]),
]


def ic(sid, size):
    return f'<svg class="ic" width="{size}" height="{size}" aria-hidden="true"><use href="#{sid}"/></svg>'


tabs, panels = [], []
for i, (label, eyebrow, heading, paras, facts) in enumerate(TABS):
    slug = re.sub(r'[^a-z0-9]+', '-', re.sub(r'&#\d+;', '2', label.lower())).strip('-')
    on = i == 0
    tabs.append(f'        <button class="tab{" is-active" if on else ""}" role="tab" '
                f'aria-selected="{str(on).lower()}" aria-controls="std-{slug}" '
                f'id="stdtab-{slug}">{label}</button>')
    body = '\n'.join(f'          <p>{p}</p>' for p in paras)
    fl = '\n'.join(f'          <div><dt>{t}</dt><dd>{d}</dd></div>' for t, d in facts)
    panels.append(f'''      <div class="std" role="tabpanel" id="std-{slug}" '''
                  f'''aria-labelledby="stdtab-{slug}"{"" if on else " hidden"}>
        <div class="std__copy">
          <span class="eyebrow">{eyebrow}</span>
          <h3>{heading}</h3>
{body}
        </div>
        <dl class="std__facts">
{fl}
        </dl>
      </div>''')

section = f'''<!-- ============ STANDARDS (tabbed) ============ -->
<section class="sec sec--band">
  <div class="wrap">
    <div class="sechead sechead--center">
      <div class="sechead__t">
        <span class="eyebrow">How we work</span>
        <h2 class="h2">The standards behind the products.</h2>
      </div>
    </div>

    <div class="tabs" role="tablist" aria-label="Standards and credentials">
{chr(10).join(tabs)}
    </div>

{chr(10).join(panels)}
  </div>
</section>
'''

s = io.open('index.html', encoding='utf-8').read()
anchor = '<!-- ============ AWARDS ============ -->'
assert anchor in s
s = s.replace(anchor, section + '\n' + anchor)
io.open('index.html', 'w', encoding='utf-8').write(s)
print('standards panels:', s.count('class="std"'), '| tabs:', len(TABS))
