(function () {
  'use strict';
  var quote;
  try { quote = JSON.parse(sessionStorage.getItem('bounce-quote-preview')); } catch (error) { quote = null; }
  function $(id) { return document.getElementById(id); }
  if (!quote || !quote.costs || (!quote.pricingPending && !Number.isFinite(quote.costs.total)) || !quote.contact || !Array.isArray(quote.locations)) {
    $('quote-empty').hidden = false;
    return;
  }
  var currency = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });
  function money(value) { return currency.format(value); }
  function line(list, label, value) {
    var dt = document.createElement('dt'), dd = document.createElement('dd');
    dt.textContent = label; dd.textContent = value;
    list.appendChild(dt); list.appendChild(dd);
  }
  $('quote-result').hidden = false;
  $('quote-product').textContent = quote.product;
  $('quote-sku').textContent = 'SKU ' + quote.sku;
  line($('quote-configuration'), 'Quantity', quote.costs.quantity);
  line($('quote-configuration'), 'Product colour', quote.colour);
  if (quote.size) line($('quote-configuration'), 'Size', quote.size);
  (quote.sizes || []).forEach(function (size) { line($('quote-configuration'), 'Size ' + size.size, size.quantity + ' units'); });
  line($('quote-configuration'), 'Delivery', quote.ukMainland ? 'Single UK mainland address' : 'Delivery quote required');
  line($('quote-configuration'), 'Production', quote.express ? 'Express' : 'Standard');
  quote.locations.forEach(function (location) {
    var li = document.createElement('li');
    li.textContent = location.area + ' — ' + location.method + ', ' + location.colours + (location.colours === 'Full colour' ? '' : ' print colour(s)') + (location.logoSize ? ', ' + location.logoSize : '');
    $('quote-branding').appendChild(li);
  });
  $('quote-total').textContent = quote.pricingPending ? 'To be confirmed' : money(quote.costs.total);
  $('quote-tax').textContent = quote.costs.quantity + ' units · ' + (quote.incVat ? 'Including VAT at 20%' : 'Excluding VAT');
  $('quote-shipping').textContent = quote.ukMainland ? 'Delivery costs to be confirmed.' : 'Shipping requires a separate quote for your destination.';
  var factor = quote.incVat ? 1.2 : 1;
  if (quote.pricingPending) line($('quote-costs'), 'Branding and pricing', 'To be confirmed by the team');
  else [['Product', 'product'], ['Branding', 'branding'], ['Setup', 'setup'], ['Small-order surcharge', 'surcharge'], ['Express', 'express']].forEach(function (item) {
    line($('quote-costs'), item[0], money(quote.costs[item[1]] * factor));
  });
  if (quote.breaks && quote.breaks.length) {
    $('quote-breaks').hidden = false;
    quote.breaks.forEach(function (tier) {
      var row = document.createElement('tr');
      [tier.quantity, money(tier.total / tier.quantity), money(tier.total)].forEach(function (value) {
        var td = document.createElement('td'); td.textContent = value; row.appendChild(td);
      });
      $('quote-break-rows').appendChild(row);
    });
  }
  line($('quote-recipient'), 'Name', quote.contact.name);
  line($('quote-recipient'), 'Email', quote.contact.email);
  if (quote.contact.phone) line($('quote-recipient'), 'Phone', quote.contact.phone);
  if (quote.contact.company) line($('quote-recipient'), 'Company', quote.contact.company);
  $('quote-mockup').textContent = quote.mockup ? 'Mock-up proof requested.' : 'Mock-up proof not requested.';
  if (/^product[-\w]*-v4\.html$/.test(quote.source)) $('quote-back').href = quote.source;
})();
