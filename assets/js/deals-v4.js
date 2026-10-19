/* ==========================================================================
   Weekly deals and card colour swatches - list and category pages.

   Deals: four products drawn from the page's grid, seeded by ISO week so the
   same four show all week, at 10% off, with a countdown to Monday 00:00 when
   the price reverts and a new four take over. The same products would be
   listed on the Offers page.

   Swatches: a colour dot swaps the card photo where a colourway image is
   known; "+N" reveals the rest of the range.
   ========================================================================== */
(function () {
  'use strict';

  function isoWeek(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    var day = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - day);
    var y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil(((t - y0) / 86400000 + 1) / 7);
  }
  function pick(list, n, seed) {
    var copy = list.slice(), s = seed;
    for (var i = copy.length - 1; i > 0; i--) {
      s = (s * 9301 + 49297) % 233280;
      var j = Math.floor((s / 233280) * (i + 1));
      var tmp = copy[i]; copy[i] = copy[j]; copy[j] = tmp;
    }
    return copy.slice(0, n);
  }
  var GBP = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });

  /* ---------- Deals ---------- */
  var grid = document.getElementById('product-grid');
  var slot = document.getElementById('weekly-deals');
  if (grid && slot) {
    var cards = [].slice.call(grid.querySelectorAll('.prod'));
    var now = new Date();
    var week = isoWeek(now);
    // A different seed from the weekly picks, so the two fours never overlap by design.
    pick(cards, Math.min(4, cards.length), week * 7 + now.getFullYear() * 31 + 11).forEach(function (src) {
      var clone = src.cloneNode(true);
      clone.hidden = false;                    // the grid card may be filtered out
      var flag = clone.querySelector('.prod__flag');
      if (!flag) {
        flag = document.createElement('span');
        clone.querySelector('.prod__media').prepend(flag);
      }
      flag.className = 'prod__flag prod__flag--deal';
      flag.innerHTML = '<svg class="ic" width="17" height="17" aria-hidden="true"><use href="#i-tag"/></svg>10% off this week';
      var was = parseFloat(clone.dataset.price) || 0;
      var price = clone.querySelector('.prod__price');
      if (price && was) {
        price.innerHTML = '<span class="prod__aslow">This week, as low as</span><b>' + GBP.format(was * 0.9) + '</b> <s>' + GBP.format(was) + '</s> <small>per unit</small>';
      }
      slot.appendChild(clone);
    });
    var weekEl = document.getElementById('deals-week');
    if (weekEl) weekEl.textContent = 'Week ' + week + ', ' + now.getFullYear() + '.';

    // Countdown to the coming Monday, 00:00 local.
    var clock = document.getElementById('deals-clock');
    if (clock) {
      var cells = clock.querySelectorAll('b');
      function pad(n) { return (n < 10 ? '0' : '') + n; }
      function tick() {
        var t = new Date();
        var end = new Date(t.getFullYear(), t.getMonth(), t.getDate() + ((8 - t.getDay()) % 7 || 7));
        var left = Math.max(0, end - t);
        var d = Math.floor(left / 86400000), h = Math.floor(left / 3600000) % 24,
            m = Math.floor(left / 60000) % 60, s = Math.floor(left / 1000) % 60;
        cells[0].textContent = d; cells[1].textContent = pad(h); cells[2].textContent = pad(m); cells[3].textContent = pad(s);
      }
      tick();
      setInterval(tick, 1000);
    }
  }

  /* ---------- Swatches ---------- */
  document.addEventListener('click', function (ev) {
    var dot = ev.target.closest('.prod__sw i, .prod__sw em');
    if (!dot) return;
    ev.preventDefault();                       // the card is a link; the swatch is not
    var sw = dot.parentElement;
    if (dot.tagName === 'EM') {
      sw.classList.add('is-open');
      [].forEach.call(sw.querySelectorAll('i[hidden]'), function (i) { i.hidden = false; });
      return;
    }
    [].forEach.call(sw.querySelectorAll('i'), function (i) { i.classList.toggle('is-on', i === dot); });
    var img = dot.closest('.prod').querySelector('.prod__media img');
    if (img && dot.dataset.img) img.src = dot.dataset.img;
  });
})();
