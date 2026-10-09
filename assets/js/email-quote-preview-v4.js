/* Hydrates the browser email preview from the configured quote. Email delivery
   must render the same snapshot on the server; email clients do not run JS. */
(async function () {
  'use strict';
  var q;
  try { q = JSON.parse(sessionStorage.getItem('bounce-quote-preview')); } catch (error) { return; }
  if (!q || !q.costs || !q.contact || !Array.isArray(q.locations)) return;
  function $(id) { return document.getElementById(id); }
  function text(id, value) { if ($(id)) $(id).textContent = value; }
  var GBP = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });
  function money(n) { return GBP.format(n); }
  var tax = q.incVat ? 'Inc VAT' : 'Ex VAT';
  text('email-total', money(q.costs.total)); text('email-vat', tax);
  var preheader = document.querySelector('body > div');
  if (preheader) preheader.textContent = 'Your quote for ' + q.product + ' — ' + money(q.costs.total) + ' ' + tax.toLowerCase() + '.';
  text('email-number', '#PREVIEW-' + q.sku);
  text('email-date', new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', day: 'numeric', month: 'short', year: 'numeric' }).format(new Date()));
  text('email-contact-name', q.contact.company || q.contact.name); text('email-recipient', q.contact.email);
  $('email-recipient').href = 'mailto:' + q.contact.email;
  var productTitle = $('email-product-title').querySelector('a');
  productTitle.textContent = q.product;
  var source = /^product[-\w]*-v4\.html$/.test(q.source) ? q.source : 'product-hivis-v4.html';
  document.querySelectorAll('[data-email-product-link]').forEach(function (a) { a.href = source; });
  text('email-product-code', 'Product code ' + q.sku);
  if (q.image && /^(https?:\/\/|assets\/)/.test(q.image)) $('email-product-image').src = q.image;
  $('email-product-image').alt = q.product;
  text('email-product-description', q.description || '');
  $('email-product-colour').textContent = '';
  var colourRow = $('email-product-colour').insertRow();
  colourRow.insertCell().textContent = q.colour;
  text('email-production', q.production || 'To be confirmed');
  text('email-delivery', q.ukMainland ? q.delivery || 'To be confirmed' : 'Destination quote required');
  var config = $('email-configuration'); config.textContent = '';
  function addConfig(label, value) {
    var row = config.insertRow(), key = row.insertCell(), content = row.insertCell();
    key.textContent = label; content.textContent = value;
    key.style.cssText = 'padding:7px 0;font:13px Arial;color:#33564F;border-bottom:1px solid #DCD6C9;';
    content.style.cssText = 'padding:7px 0;font:bold 13px Arial;color:#133935;text-align:right;border-bottom:1px solid #DCD6C9;';
  }
  if (q.contact.colleague) addConfig('Copy to', q.contact.colleague);
  addConfig('Product colour', q.colour); addConfig('Quantity', q.costs.quantity);
  if (q.size) addConfig('Size', q.size);
  q.locations.forEach(function (loc, index) {
    addConfig('Branding ' + (index + 1), loc.area + ' — ' + loc.method + ', ' + loc.colours + (loc.logoSize ? ', ' + loc.logoSize : ''));
  });
  addConfig('Production', q.express ? 'Express' : 'Standard');
  addConfig('Delivery destination', q.ukMainland ? 'UK mainland' : 'To be confirmed');
  addConfig('Product cost (ex VAT)', money(q.costs.product));
  addConfig('Branding cost (ex VAT)', money(q.costs.branding));
  addConfig('Setup cost (ex VAT)', money(q.costs.setup));
  if (q.costs.surcharge) addConfig('Surcharges (ex VAT)', money(q.costs.surcharge));
  if (q.costs.express) addConfig('Express charge (ex VAT)', money(q.costs.express));
  var table = $('email-breaks-table');
  Array.from(table.rows).slice(1).forEach(function (row) { row.remove(); });
  if (!q.breaks || !q.breaks.length) $('email-breaks-section').hidden = true;
  else {
    // Unit figure excludes one-off costs, while the total includes them.
    var factor = q.incVat ? 1.2 : 1;
    var baseline = (q.breaks[0].product + q.breaks[0].branding) / q.breaks[0].quantity;
    q.breaks.forEach(function (tier) {
      var unit = (tier.product + tier.branding) / tier.quantity;
      var save = baseline ? ((baseline - unit) / baseline * 100).toFixed(2) : '0.00';
      var row = table.insertRow();
      [tier.quantity, 'Save ' + save + '%', money(unit * factor), money(tier.total)].forEach(function (value, index) {
        var cell = row.insertCell(); cell.textContent = value;
        cell.style.cssText = 'padding:9px 12px;font:13px Arial;color:#133935;border-bottom:1px solid #DCD6C9;' + (index > 1 ? 'text-align:right;' : '');
      });
    });
  }
  var priceNote = document.createElement('p');
  priceNote.textContent = 'All prices ' + tax.toLowerCase() + ', as selected in your quote request.';
  priceNote.style.cssText = 'font:12px Arial;color:#33564F;';
  $('email-vat').parentElement.appendChild(priceNote);
  var artworks = Array.isArray(q.artworks) ? q.artworks : q.artwork ? [q.artwork] : [];
  text('email-artwork-status', q.mockup ? 'Mock-up requested using your supplied artwork for each branding location.' : artworks.length ? 'Artwork supplied for the selected branding locations.' : 'No mock-up requested for this quote.');
  text('email-artwork-name', '');
  var artworkTable = document.createElement('table');
  artworkTable.setAttribute('role', 'presentation');
  artworkTable.setAttribute('cellpadding', '0'); artworkTable.setAttribute('cellspacing', '0');
  artworkTable.style.cssText = 'width:100%;max-width:350px;border-collapse:separate;border-spacing:0 10px;font:14px Arial;';
  $('email-artwork-image').appendChild(artworkTable);
  for (var artwork of artworks) {
    var row = artworkTable.insertRow(), label = row.insertCell(), action = row.insertCell();
    label.textContent = 'LOGO';
    label.style.cssText = 'width:35%;padding:9px 10px;background:#fff;color:#000;font-weight:bold;border-right:2px solid #e7e9e8;';
    action.style.cssText = 'padding:9px 10px;background:#fff;';
    try {
      var file = await window.BounceQuoteArtwork.load(artwork.id);
      if (!file) throw new Error('Artwork not found');
      var link = document.createElement('a'), url = URL.createObjectURL(file);
      link.href = url; link.download = artwork.name; link.textContent = 'Download';
      link.title = (artwork.area ? artwork.area + ': ' : '') + artwork.name;
      link.setAttribute('aria-label', 'Download ' + artwork.name + (artwork.area ? ' for ' + artwork.area : ''));
      link.style.cssText = 'color:#d50040;font-weight:bold;text-decoration:underline;';
      action.appendChild(link);
      (function (objectURL) { window.addEventListener('pagehide', function () { URL.revokeObjectURL(objectURL); }); })(url);
    } catch (error) {
      action.textContent = 'File unavailable'; action.style.color = '#33564F';
    }
  }
  if (q.mockup && !artworks.length) text('email-artwork-status', 'Mock-up requested. No artwork is attached to this quote.');
  document.title = 'Email quote preview — ' + q.product;
})();
