/* ==========================================================================
   Offers page: filter the offers by category and sort them. Each card has
   its own discount and end date (data-discount, data-ends-days); the
   countdowns and the colour swatches come from deals-v4.js.
   ========================================================================== */
(function () {
  'use strict';
  var grid = document.getElementById('offers-grid');
  var chips = [].slice.call(document.querySelectorAll('.offers-bar .chip'));
  if (!grid || !chips.length) return;
  var cards = [].slice.call(grid.querySelectorAll('.prod'));
  var count = document.getElementById('offers-count');
  var none = document.getElementById('offers-none');
  var sortSel = document.getElementById('offers-sort');

  function num(c, k) { return parseFloat(c.dataset[k]) || 0; }

  function sort() {
    var by = sortSel ? sortSel.value : 'ending';
    cards.slice().sort(function (a, b) {
      if (by === 'discount') return num(b, 'discount') - num(a, 'discount') || num(a, 'endsDays') - num(b, 'endsDays');
      if (by === 'price-asc') return num(a, 'price') - num(b, 'price');
      if (by === 'price-desc') return num(b, 'price') - num(a, 'price');
      return num(a, 'endsDays') - num(b, 'endsDays') || num(b, 'discount') - num(a, 'discount');
    }).forEach(function (c) { grid.appendChild(c); });
  }

  function show(cat) {
    var n = 0;
    cards.forEach(function (c) {
      var on = cat === 'all' || c.dataset.cat === cat;
      c.hidden = !on;
      if (on) n++;
    });
    if (count) count.textContent = n;
    if (none) none.hidden = n > 0;
    chips.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.cat === cat ? 'true' : 'false'); });
  }
  chips.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.cat); }); });
  if (sortSel) sortSel.addEventListener('change', sort);
  sort();
})();
