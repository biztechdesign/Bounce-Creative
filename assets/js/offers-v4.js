/* ==========================================================================
   Offers page: filter the week's offers by category. The countdowns and the
   colour swatches come from deals-v4.js.
   ========================================================================== */
(function () {
  'use strict';
  var grid = document.getElementById('offers-grid');
  var chips = [].slice.call(document.querySelectorAll('.offers-bar .chip'));
  if (!grid || !chips.length) return;
  var cards = [].slice.call(grid.querySelectorAll('.prod'));
  var count = document.getElementById('offers-count');
  var none = document.getElementById('offers-none');

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
})();
