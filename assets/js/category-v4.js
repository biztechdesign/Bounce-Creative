/* ==========================================================================
   Category landing page: the weekly top four.
   Four products drawn from the page's own grid, seeded by ISO week so the
   pick is the same for everyone all week and changes on Monday.
   ========================================================================== */
(function () {
  'use strict';

  var grid = document.getElementById('product-grid');
  var slot = document.getElementById('weekly-picks');
  if (!grid || !slot) return;
  var cards = [].slice.call(grid.querySelectorAll('.prod'));
  if (!cards.length) return;

  function isoWeek(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    var day = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - day);
    var y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil(((t - y0) / 86400000 + 1) / 7);
  }

  // Seeded shuffle, so "random" is stable for the week.
  function pick(list, n, seed) {
    var copy = list.slice(), s = seed;
    for (var i = copy.length - 1; i > 0; i--) {
      s = (s * 9301 + 49297) % 233280;
      var j = Math.floor((s / 233280) * (i + 1));
      var tmp = copy[i]; copy[i] = copy[j]; copy[j] = tmp;
    }
    return copy.slice(0, n);
  }

  var now = new Date();
  var week = isoWeek(now);
  pick(cards, Math.min(4, cards.length), week + now.getFullYear() * 53).forEach(function (src) {
    var clone = src.cloneNode(true);
    var flag = clone.querySelector('.prod__flag');
    if (flag) {
      flag.className = 'prod__flag prod__flag--best';
      flag.lastChild.nodeValue = 'Best seller';
      var use = flag.querySelector('use');
      if (use) use.setAttribute('href', '#i-star');
    }
    slot.appendChild(clone);
  });

  var weekNo = document.getElementById('week-no');
  if (weekNo) weekNo.textContent = week + ', ' + now.getFullYear();
})();
