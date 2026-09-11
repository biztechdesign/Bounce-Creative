/* ==========================================================================
   Product detail page behaviour.

   Field set and cost model follow the live bouncecreativedesigns.co.uk
   configurator: product colour, branding positions picked from a strip of
   thumbnails (single, or several behind the "multiple branding location"
   toggle), a configuration panel per chosen position, quantity against
   available stock with selectable price breaks, then a breakdown of product,
   branding, setup, surcharges and express.

   Every page carries its own configuration in a JSON island (#pdp-config), so
   one script serves the whole catalogue and the numbers on the page can never
   drift from the numbers in the script.

   Progressive: with JS off the page still shows the product, its gallery, the
   full price table, the printed cost notes and every detail tab. The live
   calculator is an enhancement over a page that already answers the question.
   ========================================================================== */
(function () {
  'use strict';

  var cfgEl = document.getElementById('pdp-config');
  if (!cfgEl) return;

  var CFG;
  try {
    CFG = JSON.parse(cfgEl.textContent);
  } catch (e) {
    // A malformed island must not take the static page down with it.
    return;
  }

  var GBP = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });
  var NUM = new Intl.NumberFormat('en-GB');
  var VAT = 0.2;

  function money(n) { return GBP.format(n); }
  function $(id) { return document.getElementById(id); }
  function all(sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); }

  /* ---------- Gallery ---------- */
  var stage = $('gal-main');
  var thumbs = all('.gal__thumb');

  function showImage(src, alt) {
    if (!stage || !src) return;
    stage.src = src;
    if (alt) stage.alt = alt;
    thumbs.forEach(function (t) {
      var on = t.dataset.img === src;
      t.classList.toggle('is-on', on);
      if (on) t.setAttribute('aria-current', 'true');
      else t.removeAttribute('aria-current');
    });
  }

  thumbs.forEach(function (t) {
    t.addEventListener('click', function () { showImage(t.dataset.img, t.dataset.alt); });
  });

  /* ---------- Option groups ----------
     Product colour and size are the same widget with different labels, so they
     share one roving-radio implementation including keyboard support. */
  function radioGroup(selector, onPick) {
    var items = all(selector);
    if (!items.length) return;

    function select(el, focus) {
      items.forEach(function (o) {
        var on = o === el;
        o.classList.toggle('is-on', on);
        o.setAttribute('aria-checked', on ? 'true' : 'false');
        o.tabIndex = on ? 0 : -1;
      });
      if (focus) el.focus();
      onPick(el);
    }

    items.forEach(function (el, i) {
      el.tabIndex = el.classList.contains('is-on') ? 0 : -1;
      el.addEventListener('click', function () { select(el, false); });
      el.addEventListener('keydown', function (ev) {
        var d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
        if (!d) return;
        ev.preventDefault();
        select(items[(i + d + items.length) % items.length], true);
      });
    });
  }

  var colourVal = $('colour-val');
  var currentCode = (document.querySelector('.sw.is-on') || {}).dataset ? document.querySelector('.sw.is-on').dataset.code : '';
  radioGroup('.sw', function (el) {
    if (colourVal) colourVal.textContent = el.dataset.name;
    showImage(el.dataset.img, el.dataset.alt);
    currentCode = el.dataset.code || '';
    // The position thumbnails show the garment you are actually buying: the
    // supplier's per-position image for this colourway where we have one,
    // otherwise the product photo.
    all('.loc__thumb, .area__img:not(.area__img--pos)').forEach(function (img) { img.src = el.dataset.img; });
    if (CFG.positionImg && currentCode) {
      all('.area__img--pos').forEach(function (img) {
        img.src = CFG.positionImg.replace('{code}', currentCode).replace('{pos}', img.dataset.pos);
      });
    }
    syncGrid(el.dataset.name);
    update();
  });

  var sizeVal = $('size-val');
  radioGroup('.size', function (el) {
    if (sizeVal) sizeVal.textContent = el.dataset.name;
  });

  /* ---------- Configure your product: quantity by size ----------
     One row per size for the chosen colour, each capped at its stock level.
     The rows sum to the order quantity; the slider and stepper stand down. */
  var grid = $('cfg');
  var gridInputs = grid ? all('.cfg__qty', grid) : [];

  function gridStock(colourName) {
    var sw = all('.sw').filter(function (b) { return b.dataset.name === colourName; })[0];
    var code = sw ? sw.dataset.code : currentCode;
    return (CFG.stockBySize || {})[code] || {};
  }

  function syncGrid(colourName) {
    if (!grid) return;
    var stock = gridStock(colourName);
    var total = 0;
    var colEl = grid.querySelector('[data-role="colour"]');
    if (colEl) colEl.textContent = colourName;
    all('[data-size].cfg__row', grid).forEach(function (tr) {
      var sz = tr.dataset.size, n = stock[sz] || 0;
      tr.querySelector('[data-role="stock"]').textContent = n;
      var inp = tr.querySelector('.cfg__qty');
      inp.max = n;
      if (parseInt(inp.value, 10) > n) inp.value = n;
      inp.disabled = n === 0;
      total += n;
    });
    var st = $('cfg-stock');
    if (st) st.textContent = NUM.format(total);
  }

  function gridTotal() {
    return gridInputs.reduce(function (sum, i) { return sum + (parseInt(i.value, 10) || 0); }, 0);
  }

  gridInputs.forEach(function (i) {
    i.addEventListener('input', function () {
      var max = parseInt(i.max, 10);
      if (max >= 0 && parseInt(i.value, 10) > max) i.value = max;
      if (qtyEl) qtyEl.value = Math.max(gridTotal(), 0);
      update();
    });
  });

  /* ---------- Branding positions ----------
     The strip is the source of truth for which positions are branded. Each
     selected position owns a configuration panel below it, and each panel
     carries its own setup charge. */
  var areaBtns = all('.area');
  var multiEl = $('multi-location');
  var locWrap = $('locations');
  var locTpl = $('loc-tpl');
  var MAX = CFG.maxLocations || 4;

  function locs() { return locWrap ? all('.loc', locWrap) : []; }
  function role(loc, name) { return loc.querySelector('[data-role="' + name + '"]'); }

  /* Branding type, colour count and logo size are tile groups, so the chosen
     value is read off the pressed tile rather than a select's value. */
  function chosen(loc, r) {
    return loc.querySelector('[data-role="' + r + '"].is-on');
  }

  var METHODS = CFG.methods || [];

  function methodOf(loc) {
    var t = chosen(loc, 'type');
    var i = t ? parseInt(t.dataset.method, 10) : 0;
    return METHODS[i] || METHODS[0] || { ladder: [], colours: [], logoSizes: [], lead: 0, cmyk: false, extraColour: 0, sample: 0 };
  }

  /* Per-unit price at quantity n from a (min, each) ladder. */
  function ladderAt(ladder, n) {
    var each = ladder.length ? ladder[0].each : 0;
    for (var i = 0; i < ladder.length; i++) {
      if (n >= ladder[i].min) each = ladder[i].each;
    }
    return each;
  }

  function tileValue(loc, r, fallback) {
    var el = chosen(loc, r);
    return el ? (parseInt(el.dataset.value, 10) || fallback) : fallback;
  }

  /* Print colours only mean something for spot-colour methods; CMYK methods
     generate their colour from process ink, which is what the live site's
     "CMYK: Yes" flag is telling you. */
  function syncLocation(loc) {
    var m = methodOf(loc);

    /* Every type's options are in the markup; reveal the ones this type
       offers, and if the current pick is not among them move it to the first
       that is. */
    function limit(r, allowed) {
      var tiles = all('[data-role="' + r + '"]', loc);
      var current = chosen(loc, r);
      var currentOk = current && allowed.indexOf(parseInt(current.dataset.value, 10)) !== -1;
      tiles.forEach(function (tile) {
        var v = parseInt(tile.dataset.value, 10);
        var ok = allowed.indexOf(v) !== -1;
        tile.hidden = !ok;
        var on = ok && (currentOk ? tile === current : v === allowed[0]);
        tile.classList.toggle('is-on', on);
        tile.setAttribute('aria-checked', on ? 'true' : 'false');
        tile.tabIndex = on ? 0 : -1;
      });
    }
    limit('colours', m.colours || []);
    limit('logo', m.logoSizes || []);

    var cf = role(loc, 'colours-field'), kf = role(loc, 'cmyk-field'), lf = role(loc, 'logo-field');
    if (cf) cf.hidden = !(m.colours && m.colours.length);
    if (kf) kf.hidden = !m.cmyk;
    if (lf) lf.hidden = !(m.logoSizes && m.logoSizes.length);
  }

  function wireLocation(loc) {
    /* Each tile row is a radiogroup: pressing one clears its siblings, and the
       arrow keys move through it. */
    ['type', 'colours', 'logo'].forEach(function (r) {
      var tiles = all('[data-role="' + r + '"]', loc);
      tiles.forEach(function (tile, i) {
        tile.tabIndex = tile.classList.contains('is-on') ? 0 : -1;
        function pick(focus) {
          tiles.forEach(function (o) {
            var on = o === tile;
            o.classList.toggle('is-on', on);
            o.setAttribute('aria-checked', on ? 'true' : 'false');
            o.tabIndex = on ? 0 : -1;
          });
          if (focus) tile.focus();
          syncLocation(loc);
          update();
        }
        tile.addEventListener('click', function () { pick(false); });
        tile.addEventListener('keydown', function (ev) {
          var d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
          if (!d) return;
          ev.preventDefault();
          // Step past tiles the current branding type does not offer.
          var j = i, guard = tiles.length;
          do { j = (j + d + tiles.length) % tiles.length; } while (tiles[j].hidden && --guard);
          tiles[j].click();
          tiles[j].focus();
        });
      });
    });
    var rm = role(loc, 'remove');
    if (rm) {
      rm.addEventListener('click', function () {
        // Deselecting in the strip is the single path that removes a panel, so
        // the two can never disagree about what is being branded.
        var btn = areaBtns.filter(function (b) { return b.dataset.area === loc.dataset.area; })[0];
        if (btn) toggleArea(btn, false);
      });
    }
    syncLocation(loc);
  }

  function panelFor(areaName) {
    return locs().filter(function (l) { return l.dataset.area === areaName; })[0];
  }

  function allowedMethods(areaName) {
    var pos = (CFG.positions || []).filter(function (x) { return x.name === areaName; })[0];
    return pos && pos.methods ? pos.methods : null;
  }

  /* A position may offer only some branding types (the jacket's chest is
     embroidery only; its biceps add a screenprint). Tiles the position does
     not offer are hidden, and the pick moves to the first that is. */
  function limitTypes(loc) {
    var allowed = allowedMethods(loc.dataset.area);
    var tiles = all('[data-role="type"]', loc);
    if (!allowed) { tiles.forEach(function (t) { t.hidden = false; }); return; }
    var current = chosen(loc, 'type');
    var ok = function (t) { return allowed.indexOf(t.dataset.id) !== -1; };
    var keep = current && ok(current) ? current : tiles.filter(ok)[0];
    tiles.forEach(function (t) {
      t.hidden = !ok(t);
      var on = t === keep;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-checked', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
  }

  function addPanel(areaName) {
    if (!locTpl || !locWrap || panelFor(areaName)) return;
    var loc = locTpl.content.firstElementChild.cloneNode(true);
    loc.dataset.area = areaName;
    locWrap.appendChild(loc);
    limitTypes(loc);
    wireLocation(loc);
  }

  function removePanel(areaName) {
    var loc = panelFor(areaName);
    if (loc) loc.remove();
  }

  function renumber() {
    var list = locs();
    list.forEach(function (loc, i) {
      var label = 'Branding location ' + (i + 1) + ' — ' + loc.dataset.area;
      var n = role(loc, 'n');
      if (n) n.textContent = label;
      // Panels are cloned, so they cannot carry ids for aria-labelledby; the
      // fieldset is named directly instead.
      loc.setAttribute('aria-label', label);
      var rm = role(loc, 'remove');
      // At least one position must stay branded, or there is nothing to price.
      if (rm) rm.hidden = list.length < 2;
    });
  }

  function selectedAreas() {
    return areaBtns.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; });
  }

  function toggleArea(btn, want) {
    var multi = multiEl && multiEl.checked;
    var on = btn.getAttribute('aria-pressed') === 'true';
    var next = (typeof want === 'boolean') ? want : !on;

    if (!multi) {
      // Single mode: picking a position replaces whatever was picked before.
      if (!next) return;                     // never leave nothing selected
      areaBtns.forEach(function (b) {
        b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
        b.classList.toggle('is-on', b === btn);
        if (b !== btn) removePanel(b.dataset.area);
      });
      addPanel(btn.dataset.area);
    } else {
      if (!next && selectedAreas().length < 2) return;   // keep at least one
      if (next && selectedAreas().length >= MAX) return;
      btn.setAttribute('aria-pressed', next ? 'true' : 'false');
      btn.classList.toggle('is-on', next);
      if (next) addPanel(btn.dataset.area);
      else removePanel(btn.dataset.area);
    }
    renumber();
    update();
  }

  areaBtns.forEach(function (btn, i) {
    btn.addEventListener('click', function () { toggleArea(btn); });
    btn.addEventListener('keydown', function (ev) {
      var d = { ArrowRight: 1, ArrowLeft: -1 }[ev.key];
      if (!d) return;
      ev.preventDefault();
      areaBtns[(i + d + areaBtns.length) % areaBtns.length].focus();
    });
  });

  if (multiEl) {
    multiEl.addEventListener('change', function () {
      areaBtns.forEach(function (b) { b.classList.toggle('is-multi', multiEl.checked); });
      if (!multiEl.checked) {
        // Collapsing back to one position: keep the first, drop the rest.
        var keep = selectedAreas()[0];
        areaBtns.forEach(function (b) {
          if (b === keep) return;
          b.setAttribute('aria-pressed', 'false');
          b.classList.remove('is-on');
          removePanel(b.dataset.area);
        });
        renumber();
        update();
      }
    });
  }

  /* ---------- Price ---------- */
  var tiers = (CFG.tiers || []).slice().sort(function (a, b) { return b.min - a.min; });

  function tierFor(n) {
    for (var i = 0; i < tiers.length; i++) {
      if (n >= tiers[i].min) return tiers[i];
    }
    return tiers[tiers.length - 1];
  }

  var qtyEl = $('qty');
  var expressEl = $('express');
  var vatEl = $('vat-toggle');
  var ukEl = $('uk-mainland');
  var cartBtn = $('add-to-cart');

  var out = {
    product: $('c-product'), branding: $('c-branding'), setup: $('c-setup'),
    surcharge: $('c-surcharge'), express: $('c-express'), total: $('c-total'),
    totalNote: $('c-total-note'), perUnit: $('c-perunit'), points: $('c-points'),
    stock: $('c-stock'),
    freeDelivery: $('c-free-delivery'), pointsGbp: $('c-points-gbp'), vatLbl: $('c-vat-lbl')
  };
  var rangeEl = $('qty-range');
  var badgeEl = $('qty-badge');

  function set(el, v) { if (el) el.textContent = v; }

  /* Costs for the current configuration at quantity n.

     Each branding type carries its own per-unit ladder that already includes
     the branding, so the product line is the unprinted price and the branding
     line is whatever the chosen type adds on top of it. Extra ink colours add
     a per-colour uplift. A small-order charge lands once on any order whose
     value is under the threshold - this is the fifty pounds the live table
     shows on its lower rows and nowhere else. */
  /* Branding price each from a matrix of quantity breaks x colour counts. */
  function matrixEach(m, inks, n) {
    var mx = m.matrix, cols = (m.colours && m.colours.length) ? m.colours : [1];
    var ci = Math.max(0, cols.indexOf(inks));
    var row = mx.rows[0];
    for (var i = 0; i < mx.qtys.length; i++) if (n >= mx.qtys[i]) row = mx.rows[i];
    return ci < row.length ? row[ci] : row[row.length - 1];
  }

  function setupFor(m, inks) {
    var st = m.setup || {};
    if (st[inks] != null) return st[inks];
    if (st['1'] != null) return st['1'];
    var k = Object.keys(st); return k.length ? st[k[0]] : 0;
  }

  function costsAt(n, sample) {
    var matrix = CFG.pricing === 'matrix';
    var q = sample ? 1 : n;
    var unprinted = tierFor(q).each;
    var branding = 0, setup = 0, extraLead = 0;
    locs().forEach(function (loc) {
      var m = methodOf(loc);
      var inks = (m.colours && m.colours.length) ? tileValue(loc, 'colours', m.colours[0]) : 1;
      var brandingEach;
      if (matrix) {
        /* Live engine model: unprinted price plus a branding price each read
           off the matrix, plus a setup per colour count for every position. */
        brandingEach = matrixEach(m, inks, q);
        setup += setupFor(m, inks);
      } else if (sample) {
        brandingEach = m.sample - unprinted;
      } else {
        brandingEach = ladderAt(m.ladder, q) + Math.max(0, inks - 1) * (m.extraColour || 0) - unprinted;
      }
      branding += brandingEach * q;
      if (m.lead > extraLead) extraLead = m.lead;
    });
    var product = unprinted * q;
    var value = product + branding;
    var surcharge = value < (CFG.smallOrderUnder || 0) ? (CFG.smallOrderFee || 0) : 0;
    return { product: product, branding: branding, setup: setup, surcharge: surcharge,
             value: value, lead: extraLead };
  }

  /* ---------- Quantity price breaks ----------
     Every row is priced from the same tiers and the same branding configuration
     as the calculator, so picking a break can never quote a different number
     from the breakdown it fills in. */
  var breakRows = all('.break');

  function updateBreaks(n, incVat) {
    var f = incVat ? (1 + VAT) : 1;
    /* Pinned to the default type at the entry break, so a dearer type reads
       as a negative saving rather than the ladder quietly re-basing itself. */
    var baseEach = CFG.baseline || 0;

    breakRows.forEach(function (row) {
      var q = parseInt(row.dataset.qty, 10) || 1;
      var sample = row.classList.contains('break--sample');
      var c = costsAt(q, sample);
      var each = c.value / (sample ? 1 : q);
      var sub = c.value + c.setup + c.surcharge;

      set(row.querySelector('[data-role="each"]'), money(each * f));
      set(row.querySelector('[data-role="sub"]'), money(sub * f));

      var saveEl = row.querySelector('[data-role="save"]');
      if (saveEl) {
        var pct = baseEach > 0 ? (1 - each / baseEach) * 100 : 0;
        saveEl.textContent = 'Save ' + pct.toFixed(2) + '%';
        saveEl.classList.toggle('is-neg', pct < 0);
      }
      row.classList.toggle('is-on', q === n);
      var radio = row.querySelector('input[type="radio"]');
      if (radio) radio.checked = (q === n);
    });
  }

  var moreBtn = $('breaks-more');
  if (moreBtn) {
    moreBtn.addEventListener('click', function () {
      var open = moreBtn.getAttribute('aria-expanded') === 'true';
      all('.break--more').forEach(function (r) { r.hidden = open; });
      moreBtn.setAttribute('aria-expanded', open ? 'false' : 'true');
      moreBtn.firstChild.textContent = open ? 'Show more price breaks ' : 'Show fewer price breaks ';
      moreBtn.querySelector('span').textContent = open ? '+' : '\u2212';
    });
  }

  /* With the size grid, a chosen break is spread into the size rows: into one
     size if it has the stock, otherwise across sizes in order until the
     quantity is met. The rows stay editable afterwards. */
  function distribute(q) {
    var rows = all('[data-size].cfg__row', grid);
    var caps = rows.map(function (r) { return parseInt(r.querySelector('.cfg__qty').max, 10) || 0; });
    var inputs = rows.map(function (r) { return r.querySelector('.cfg__qty'); });
    inputs.forEach(function (i) { i.value = ''; });
    var single = caps.findIndex(function (c) { return c >= q; });
    if (single !== -1) { inputs[single].value = q; return q; }
    var left = q;
    for (var i = 0; i < inputs.length && left > 0; i++) {
      var take = Math.min(caps[i], left);
      if (take > 0) { inputs[i].value = take; left -= take; }
    }
    return q - left;
  }

  breakRows.forEach(function (row) {
    var radio = row.querySelector('input[type="radio"]');
    if (!radio || !qtyEl) return;
    radio.addEventListener('change', function () {
      if (!radio.checked) return;
      var q = parseInt(radio.value, 10) || 1;
      if (grid) q = distribute(q);
      qtyEl.value = q;
      update();
    });
  });

  function update() {
    if (!qtyEl) return;

    var min = parseInt(qtyEl.min, 10) || 1;
    /* With the size grid, each row is already capped at its own stock level,
       so the total is not clamped again here. */
    var stock = grid ? Infinity : (CFG.stock || Infinity);
    var n = parseInt(qtyEl.value, 10);
    if (isNaN(n) || n < 0) n = 0;
    if (!grid && n < 1) n = min;
    if (n > stock) n = stock;
    var empty = grid && n === 0;
    if (empty) n = 1;   // price the single-unit row until sizes are entered

    /* Anything under the minimum is the single pre-production sample, priced
       at the type's sample rate rather than off the volume ladder. */
    var sample = n < min;
    var c = costsAt(n, sample);
    var productCost = c.product;

    var express = expressEl && expressEl.checked
      ? (CFG.expressRate || 0) * n + (CFG.expressFee || 0)
      : 0;

    var net = productCost + c.branding + c.setup + c.surcharge + express;
    var incVat = vatEl && vatEl.checked;
    var f = incVat ? (1 + VAT) : 1;
    var total = net * f;
    var each = total / n;

    var lead = (CFG.baseLead || 0) + c.lead - (express ? (CFG.expressSaving || 0) : 0);
    if (lead < 1) lead = 1;
    var ship = express ? (CFG.expressShip || 1) : (CFG.baseShip || 2);

    set(out.product, money(productCost * f));
    set(out.branding, c.branding ? money(c.branding * f) : 'Included');
    set(out.setup, c.setup ? money(c.setup * f) : 'None');
    set(out.surcharge, c.surcharge ? money(c.surcharge * f) : 'None');
    set(out.express, express ? money(express * f) : 'Not selected');
    set(out.total, money(total));
    set(out.totalNote, NUM.format(n) + ' units, ' + (incVat ? 'inc.' : 'excl.') + ' VAT');
    set($('cfg-total'), NUM.format(grid ? gridTotal() : n));
    set(out.perUnit, money(each) + ' per unit');
    var pts = Math.round(net * (CFG.pointsPerPound || 0));
    set(out.points, NUM.format(pts) + ' points');
    set(out.pointsGbp, money(pts * (CFG.pointValue || 0)));
    set(out.vatLbl, incVat ? 'Inc VAT' : 'Ex VAT');

    /* Keep the three quantity controls telling the same story. */
    if (rangeEl) {
      rangeEl.value = n;
      var lo = parseInt(rangeEl.min, 10) || 0, hi = parseInt(rangeEl.max, 10) || 1;
      var pct = Math.max(0, Math.min(100, (n - lo) / (hi - lo) * 100));
      rangeEl.style.setProperty('--fill', pct + '%');
    }
    if (badgeEl) badgeEl.textContent = NUM.format(n);
    if (qtyEl && String(qtyEl.value) !== String(n)) qtyEl.value = n;

    /* The live site tells you whether the order has cleared the free delivery
       threshold, which is worth more than a static footnote. */
    if (out.freeDelivery) {
      var qualifies = net >= (CFG.freeDeliveryOver || Infinity);
      out.freeDelivery.textContent = qualifies
        ? 'This order qualifies for free UK delivery'
        : 'Free UK delivery over £' + NUM.format(CFG.freeDeliveryOver || 0) + ' excluding VAT';
      out.freeDelivery.classList.toggle('is-on', qualifies);
    }

    var setupNote = $('c-setup-note');
    if (setupNote) setupNote.hidden = !c.setup;

    updateBreaks(n, incVat);
  }

  [qtyEl, expressEl, vatEl].forEach(function (el) {
    if (!el) return;
    el.addEventListener('input', update);
    el.addEventListener('change', update);
  });

  /* Checkout is mainland UK only, so the cart needs an explicit confirmation and
     everything else is routed to a quote. Validated on submit rather than by
     disabling the button: a greyed-out primary button on page load reads as a
     broken control, and gives no reason for being unavailable. */
  var gateMsg = $('uk-mainland-error');
  if (ukEl && cartBtn) {
    cartBtn.addEventListener('click', function (ev) {
      var ok = ukEl.checked;
      if (gateMsg) gateMsg.hidden = ok;
      ukEl.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (!ok) { ev.preventDefault(); ukEl.focus(); }
    });
    ukEl.addEventListener('change', function () {
      if (!ukEl.checked) return;
      if (gateMsg) gateMsg.hidden = true;
      ukEl.setAttribute('aria-invalid', 'false');
    });
  }

  /* ---------- Quantity: slider and stepper ----------
     Both write to #qty and let update() reconcile everything else. */
  if (rangeEl && qtyEl) {
    rangeEl.addEventListener('input', function () {
      qtyEl.value = rangeEl.value;
      update();
    });
  }
  /* A stepper drives the number field beside it: the order quantity on a
     configured product, or the quantity asked for on a quote-only one. */
  all('.qty__btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var field = b.parentElement.querySelector('input[type="number"]');
      if (!field) return;
      var step = parseInt(field.step, 10) || 1;
      var min = parseInt(field.min, 10) || 1;
      var max = field === qtyEl ? (CFG.stock || Infinity) : Infinity;
      var n = (parseInt(field.value, 10) || min) + (b.dataset.step === 'up' ? step : -step);
      field.value = Math.min(max, Math.max(min, n));
      if (field === qtyEl) update();
    });
  });

  /* The (i) beside the price opens the line-by-line breakdown. */
  var infoBtn = document.querySelector('.summary__info');
  var breakdown = $('breakdown');
  if (infoBtn && breakdown) {
    infoBtn.addEventListener('click', function () {
      var open = infoBtn.getAttribute('aria-expanded') === 'true';
      breakdown.hidden = open;
      infoBtn.setAttribute('aria-expanded', open ? 'false' : 'true');
      infoBtn.setAttribute('aria-label', (open ? 'Show' : 'Hide') + ' the price breakdown');
    });
  }

  /* ---------- Get a quote ----------
     A native <dialog>: focus is trapped, Escape closes it and the backdrop is
     inert without any of that being reimplemented. Every "request a quote"
     link on the page opens the same dialog. */
  var quoteModal = $('quote-modal');
  if (quoteModal && typeof quoteModal.showModal === 'function') {
    all('#quote-open, [data-opens="quote-modal"]').forEach(function (b) {
      b.addEventListener('click', function () { quoteModal.showModal(); });
    });
    // Click on the backdrop (outside the form) closes, as the live popup does.
    quoteModal.addEventListener('click', function (ev) {
      if (ev.target === quoteModal) quoteModal.close('close');
    });
    var quoteForm = quoteModal.querySelector('form');
    if (quoteForm) {
      quoteForm.addEventListener('submit', function (ev) {
        // "Cancel" and the close button submit with value=close, which the
        // dialog method handles; a send needs the required fields first.
        if (ev.submitter && ev.submitter.value === 'send' && !quoteForm.checkValidity()) {
          ev.preventDefault();
          quoteForm.reportValidity();
        }
      });
    }
  }

  // The first panel belongs to the position selected in the markup.
  var firstArea = selectedAreas()[0] || areaBtns[0];
  locs().forEach(function (loc) {
    if (!loc.dataset.area && firstArea) loc.dataset.area = firstArea.dataset.area;
    limitTypes(loc);
    wireLocation(loc);
  });
  renumber();
  if (grid) {
    var sw0 = document.querySelector('.sw.is-on');
    syncGrid(sw0 ? sw0.dataset.name : '');
    if (qtyEl) qtyEl.value = 0;
  }
  update();
})();
