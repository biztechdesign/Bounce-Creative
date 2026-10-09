/* ==========================================================================
   Product list page behaviour.
   Filtering, sorting, the mobile filter disclosure, and the weekly top four.
   All progressive: with JS off the full grid is still rendered and readable.
   ========================================================================== */
(function () {
  'use strict';

  var grid = document.getElementById('product-grid');
  if (!grid) return;

  var cards = [].slice.call(grid.querySelectorAll('.prod'));
  var form = document.getElementById('filters');
  if (!form) return;
  var sortSel = document.getElementById('sort');
  var countEl = document.getElementById('result-count');
  var noneEl = document.getElementById('no-results');

  /* Collection icon previews live outside the scrollable option list. */
  var preview = document.createElement('div');
  preview.id = 'collection-preview';
  preview.className = 'collection-preview';
  preview.setAttribute('role', 'tooltip');
  preview.hidden = true;
  var previewImage = document.createElement('img');
  previewImage.alt = '';
  var previewLabel = document.createElement('strong');
  preview.appendChild(previewImage);
  preview.appendChild(previewLabel);
  document.body.appendChild(preview);
  var previewInput;
  var hideTimer;
  function hidePreview() {
    window.clearTimeout(hideTimer);
    preview.hidden = true;
    if (previewInput) previewInput.removeAttribute('aria-describedby');
    previewInput = null;
  }
  function scheduleHide() { hideTimer = window.setTimeout(hidePreview, 120); }
  function showPreview(row) {
    hidePreview();
    previewImage.src = row.dataset.preview;
    previewLabel.textContent = row.querySelector('span').textContent;
    previewInput = row.querySelector('input');
    previewInput.setAttribute('aria-describedby', preview.id);
    preview.hidden = false;
    var rect = row.querySelector('img').getBoundingClientRect();
    var height = preview.offsetHeight;
    var top = rect.top - height - 10;
    if (top < 8) top = rect.bottom + 10;
    preview.style.top = Math.max(8, Math.min(top, window.innerHeight - height - 8)) + 'px';
    preview.style.left = Math.max(8, Math.min(rect.left, window.innerWidth - preview.offsetWidth - 8)) + 'px';
  }
  [].forEach.call(form.querySelectorAll('[data-preview]'), function (row) {
    row.addEventListener('pointerenter', function (event) { if (event.pointerType !== 'touch') showPreview(row); });
    row.addEventListener('pointerleave', scheduleHide);
    row.addEventListener('focusin', function () { showPreview(row); });
    row.addEventListener('focusout', scheduleHide);
  });
  preview.addEventListener('pointerenter', function () { window.clearTimeout(hideTimer); });
  preview.addEventListener('pointerleave', scheduleHide);
  document.addEventListener('keydown', function (event) { if (event.key === 'Escape') hidePreview(); });
  document.addEventListener('scroll', hidePreview, true);
  window.addEventListener('resize', hidePreview);
  form.addEventListener('reset', hidePreview);

  /* ---------- Filter + sort ---------- */
  function checkedValues(name) {
    return [].slice.call(form.querySelectorAll('input[name="' + name + '"]:checked'))
             .map(function (i) { return i.value; });
  }

  function apply() {
    var names = ['material', 'cert', 'lead', 'print', 'collection', 'swag', 'co2', 'quote', 'colour', 'brand', 'size', 'gender'];
    var selected = names.map(function (name) { return { name: name, values: checkedValues(name) }; });
    var minInput = form.elements.priceMin;
    var maxInput = form.elements.priceMax;
    var minPrice = minInput && minInput.value !== '' ? Number(minInput.value) : 0;
    var maxPrice = maxInput && maxInput.value !== '' ? Number(maxInput.value) : Infinity;
    var priceBands = checkedValues('priceBand');
    var shown = 0;

    cards.forEach(function (card) {
      // OR within a facet, AND across facets. Additional attributes on the
      // static page are representative fixtures, pending catalogue integration.
      var ok = selected.every(function (facet) {
        var values = (card.dataset[facet.name] || '').split(' ');
        return !facet.values.length || facet.values.some(function (value) { return values.indexOf(value) !== -1; });
      }) && Number(card.dataset.price) >= minPrice && Number(card.dataset.price) <= maxPrice
        && (!priceBands.length || priceBands.some(function (band) {
          var bounds = band.split('-').map(Number);
          var price = Number(card.dataset.price);
          return price >= bounds[0] && (bounds[0] === 60 || price < bounds[1]);
        }));
      card.hidden = !ok;
      if (ok) shown++;
    });

    var order = sortSel ? sortSel.value : 'popular';
    var visible = cards.filter(function (c) { return !c.hidden; });
    visible.sort(function (a, b) {
      if (order === 'price-asc')  return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
      if (order === 'price-desc') return parseFloat(b.dataset.price) - parseFloat(a.dataset.price);
      if (order === 'rating')     return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);
      return cards.indexOf(a) - cards.indexOf(b);
    });
    visible.forEach(function (c) { grid.appendChild(c); });

    if (countEl) countEl.textContent = String(shown);
    if (noneEl) noneEl.hidden = shown !== 0;
    renderApplied();
  }

  /* ---------- Applied filters, mirrored above the grid ---------- */
  var appliedBar = document.getElementById('applied');
  var appliedChips = document.getElementById('applied-chips');

  function renderApplied() {
    if (!appliedBar || !appliedChips || !form) return;
    var on = [].slice.call(form.querySelectorAll('input[type="checkbox"]:checked, input[type="number"]'))
      .filter(function (input) { return input.type === 'checkbox' || input.value !== ''; });
    appliedChips.textContent = '';

    on.forEach(function (input) {
      var label = input.closest('.facet__row');
      var text = label ? label.querySelector('span').textContent :
        (input.name === 'priceMin' ? 'Min price: £' : 'Max price: £') + Number(input.value).toFixed(2);
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'applied__chip';
      // Named for screen readers, since the visible label is just the value
      chip.setAttribute('aria-label', 'Remove filter: ' + text);
      chip.appendChild(document.createTextNode(text));
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'ic'); svg.setAttribute('width', '14');
      svg.setAttribute('height', '14'); svg.setAttribute('aria-hidden', 'true');
      var use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttribute('href', '#i-close');
      svg.appendChild(use); chip.appendChild(svg);
      chip.addEventListener('click', function () {
        if (input.type === 'checkbox') input.checked = false;
        else input.value = '';
        apply();
        input.focus();          // keep the keyboard user somewhere sensible
      });
      appliedChips.appendChild(chip);
    });

    appliedBar.hidden = on.length === 0;
  }

  if (form) {
    form.addEventListener('change', apply);
    function searchOptions(input) {
      var group = document.getElementById('options-' + input.dataset.facetSearch);
      var query = input.value.trim().toLowerCase();
      [].forEach.call(group.querySelectorAll('.facet__row'), function (row) {
        row.hidden = row.textContent.toLowerCase().indexOf(query) === -1;
      });
    }
    form.addEventListener('input', function (event) {
      if (event.target.type === 'number') apply();
      if (event.target.hasAttribute('data-facet-search')) searchOptions(event.target);
    });
    form.addEventListener('submit', function (event) { event.preventDefault(); apply(); });
    form.addEventListener('reset', function () { window.setTimeout(function () {
      [].forEach.call(form.querySelectorAll('[data-facet-search]'), searchOptions);
      apply();
    }, 0); });
  }
  if (sortSel) sortSel.addEventListener('change', apply);

  var appliedClear = document.getElementById('applied-clear');
  if (appliedClear && form) {
    appliedClear.addEventListener('click', function () { form.reset(); apply(); });
  }

  var inlineClear = document.getElementById('clear-inline');
  if (inlineClear && form) {
    inlineClear.addEventListener('click', function () { form.reset(); window.setTimeout(apply, 0); });
  }

  /* ---------- Filter rail as a disclosure on narrow screens ---------- */
  var toggle = document.querySelector('.listbar__toggle');
  if (toggle && form) {
    toggle.addEventListener('click', function () {
      var open = form.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---------- Weekly top four ----------
     The client asked for four recommendations that change every week, chosen
     at random. Seeding the shuffle with the ISO week number rather than
     Math.random keeps the four stable for everyone all week, and changes them
     on the same day for everyone — random per page load would mean a different
     four on every refresh, which is not what "changes every week" means. */
  function isoWeek(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    t.setUTCDate(t.getUTCDate() + 4 - (t.getUTCDay() || 7));           // nearest Thursday
    var start = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil((((t - start) / 86400000) + 1) / 7);
  }

  function seeded(seed) {                    // small deterministic PRNG
    var x = seed * 9301 + 49297;
    return function () { x = (x * 9301 + 49297) % 233280; return x / 233280; };
  }

  function pickWeekly(pool, n, seed) {
    var rand = seeded(seed);
    var copy = pool.slice();
    for (var i = copy.length - 1; i > 0; i--) {     // Fisher-Yates, seeded
      var j = Math.floor(rand() * (i + 1));
      var tmp = copy[i]; copy[i] = copy[j]; copy[j] = tmp;
    }
    return copy.slice(0, n);
  }

  var slot = document.getElementById('weekly-picks');
  if (slot && cards.length) {
    var now = new Date();
    var week = isoWeek(now);
    var picks = pickWeekly(cards, Math.min(4, cards.length), week + now.getFullYear() * 53);

    picks.forEach(function (src) {
      var clone = src.cloneNode(true);
      clone.hidden = false;
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
  }

  apply();
})();
