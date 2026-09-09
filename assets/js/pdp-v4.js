/* ==========================================================================
   Product detail page behaviour.
   Gallery swapping, colour selection, and a live price that reflects the
   volume tier and print method. Progressive: with JS off the page still shows
   the product, its gallery, the full price table and every detail tab.
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Gallery ---------- */
  var main = document.getElementById('gal-main');
  var thumbs = [].slice.call(document.querySelectorAll('.gal__thumb'));

  function showImage(src, label) {
    if (!main || !src) return;
    main.src = src;
    if (label) main.alt = 'Natural Cotton Shopper in ' + label + ', shown unbranded';
    thumbs.forEach(function (t) {
      var on = t.dataset.img === src;
      t.classList.toggle('is-on', on);
      if (on) t.setAttribute('aria-current', 'true');
      else t.removeAttribute('aria-current');
    });
  }

  thumbs.forEach(function (t) {
    t.addEventListener('click', function () { showImage(t.dataset.img); });
  });

  /* ---------- Colour ---------- */
  var swatches = [].slice.call(document.querySelectorAll('.sw'));
  var colourVal = document.getElementById('colour-val');

  swatches.forEach(function (s) {
    s.addEventListener('click', function () {
      swatches.forEach(function (o) {
        var on = o === s;
        o.classList.toggle('is-on', on);
        o.setAttribute('aria-checked', on ? 'true' : 'false');
      });
      if (colourVal) colourVal.textContent = s.dataset.name;
      showImage(s.dataset.img, s.dataset.name);
    });
  });

  /* ---------- Live price ----------
     Mirrors the printed tier table, so what the buy box quotes and what the
     table shows can never disagree. */
  var TIERS = [
    { min: 2500, each: 1.79 },
    { min: 1000, each: 1.98 },
    { min: 500,  each: 2.21 },
    { min: 250,  each: 2.54 },
    { min: 100,  each: 2.96 },
    { min: 25,   each: 3.48 }
  ];

  var qty = document.getElementById('qty');
  var method = document.getElementById('method');
  var unitEl = document.getElementById('unit-price');
  var noteEl = document.getElementById('price-note');
  var totalEl = document.getElementById('total-line');

  function money(n) {
    return '£' + n.toFixed(2);
  }

  function priceFor(n) {
    for (var i = 0; i < TIERS.length; i++) {
      if (n >= TIERS[i].min) return TIERS[i];
    }
    return TIERS[TIERS.length - 1];
  }

  function updatePrice() {
    if (!qty || !unitEl) return;
    var n = parseInt(qty.value, 10);
    if (!n || n < 25) n = 25;
    var tier = priceFor(n);
    var uplift = method ? parseFloat(method.value) || 0 : 0;
    var each = tier.each + uplift;

    unitEl.textContent = money(each);
    if (noteEl) noteEl.textContent = 'at ' + n.toLocaleString('en-GB');
    if (totalEl) {
      // Built as nodes rather than innerHTML - the values are ours, but there is
      // no reason to hand a string to the parser on every keystroke.
      var strong = document.createElement('b');
      strong.textContent = money(each * n);
      var note = document.createElement('span');
      note.textContent = 'excl. VAT, ' + n.toLocaleString('en-GB') + ' units';
      totalEl.textContent = 'Estimated total ';
      totalEl.appendChild(strong);
      totalEl.appendChild(document.createTextNode(' '));
      totalEl.appendChild(note);
    }
  }

  if (qty) { qty.addEventListener('input', updatePrice); qty.addEventListener('change', updatePrice); }
  if (method) method.addEventListener('change', updatePrice);
  updatePrice();
})();
