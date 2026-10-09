# Products page feedback revision

Local preview: http://127.0.0.1:8000/products-v4.html

Replaced the dark photographic banner with a compact category heading. Retained and retitled the category guidance immediately above the FAQ, with one full-width photograph between the guidance and FAQ. The photograph reuses assets/img/hero-bags.png.

Filter group reference: https://www.bouncecreativedesigns.co.uk/bags/shopping-bags/tote-bags (reviewed 9 October 2026). The public page exposes gender, collection, branding techniques, swag box, instant quote, colours, price, brand, size and material groups. Added these groups plus the requested CO₂ group, retaining certification and lead time.

Inspected the rendered live page to import its complete facet option lists: 1 gender, 7 collections, 5 branding techniques, 1 swag box option, 1 instant quote option, 104 colours, 5 price bands, 11 brands, 43 sizes and 41 materials. The source snapshot is saved in live-tote-filters.json. Preserved source values; corrected the visible typo “Laser engaving” to “Laser engraving”. CO₂ Products is present in Collection as on the live page, with an additional dedicated CO₂ control for the client's request. Larger groups have search fields and scrollable option lists.

Option values now match the reference page. Product attributes in products-v4.html remain demo fixtures, including CO₂ availability, swag suitability, brands, quote mode and branding methods. They are not verified supplier data or a production catalogue integration. Detailed size and material options have no matching sample products unless existing card data maps exactly (Cotton and Jute). Some options therefore return an empty result in this 15-product preview. No footprint measurements have been invented. Replace the fixtures with catalogue data before production.

Verified in browser at 1440px and 390px: price filtering; combined material and price filters; OR within material; CO₂ and brand filtering; clear-all reset to all 15 products; mobile disclosure; no horizontal overflow. All inspected product images loaded. JavaScript syntax and git diff whitespace checks passed.

After importing the live options, verified exact option-value parity across all 10 source groups, price band filtering, eco collection filtering, colour search and restoration of all 104 colours after clearing. Desktop and mobile screenshots refreshed.
