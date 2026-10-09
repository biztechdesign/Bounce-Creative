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

    set($('info-production'), lead + ' working days');
    set($('info-delivery'), ukEl && !ukEl.checked ? 'To be confirmed' : ship + ' working days');
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
    if (quoteModal && quoteModal.open) syncQuotePanel();

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
    if (CFG.quotePreview) {
      breakdown.classList.add('calc--popover');
      breakdown.setAttribute('role', 'region');
      breakdown.setAttribute('aria-label', 'Configured price breakdown');
      var timings = document.createElement('div'); timings.className = 'calc__timings';
      timings.innerHTML = '<p>Estimated production time:<br><b id="info-production"></b></p><p>Estimated delivery time:<br><b id="info-delivery"></b></p>';
      breakdown.appendChild(timings); document.body.appendChild(breakdown);
      var pinned = false, closeTimer;
      function positionBreakdown() {
        if (breakdown.hidden) return;
        var rect = infoBtn.getBoundingClientRect(), box = breakdown.getBoundingClientRect();
        breakdown.style.left = Math.max(12, Math.min(rect.left, window.innerWidth - box.width - 12)) + 'px';
        var top = rect.bottom + 10;
        if (top + box.height > window.innerHeight - 12) top = Math.max(12, rect.top - box.height - 10);
        breakdown.style.top = top + 'px';
      }
      function showBreakdown() {
        clearTimeout(closeTimer); breakdown.hidden = false;
        infoBtn.setAttribute('aria-expanded', 'true');
        infoBtn.setAttribute('aria-label', 'Hide the price breakdown');
        positionBreakdown();
      }
      function hideBreakdown() {
        clearTimeout(closeTimer); breakdown.hidden = true; pinned = false;
        infoBtn.setAttribute('aria-expanded', 'false');
        infoBtn.setAttribute('aria-label', 'Show the price breakdown');
      }
      function deferHide() {
        closeTimer = setTimeout(function () { if (!pinned) hideBreakdown(); }, 180);
      }
      infoBtn.addEventListener('pointerenter', function (ev) { if (ev.pointerType !== 'touch') showBreakdown(); });
      infoBtn.addEventListener('pointerleave', deferHide);
      infoBtn.addEventListener('focus', showBreakdown);
      infoBtn.addEventListener('blur', deferHide);
      infoBtn.addEventListener('click', function () {
        if (pinned) hideBreakdown(); else { pinned = true; showBreakdown(); }
      });
      breakdown.addEventListener('pointerenter', function () { clearTimeout(closeTimer); });
      breakdown.addEventListener('pointerleave', deferHide);
      document.addEventListener('click', function (ev) {
        if (!infoBtn.contains(ev.target) && !breakdown.contains(ev.target)) hideBreakdown();
      });
      document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') hideBreakdown(); });
      window.addEventListener('resize', positionBreakdown);
      window.addEventListener('scroll', positionBreakdown, true);
    } else {
      infoBtn.addEventListener('click', function () {
        var open = infoBtn.getAttribute('aria-expanded') === 'true';
        breakdown.hidden = open;
        infoBtn.setAttribute('aria-expanded', open ? 'false' : 'true');
        infoBtn.setAttribute('aria-label', (open ? 'Show' : 'Hide') + ' the price breakdown');
      });
    }
  }

  /* ---------- Get a quote ----------
     A native <dialog>: focus is trapped, Escape closes it and the backdrop is
     inert without any of that being reimplemented. Every "request a quote"
     link on the page opens the same dialog. */
  var quoteModal = $('quote-modal');
  function quoteSnapshot(form, skipUpdate) {
    if (!skipUpdate) update();
    var n = parseInt(qtyEl.value, 10);
    var min = parseInt(qtyEl.min, 10) || 1;
    var incVat = form.elements.vat.checked;
    function quoteAt(quantity) {
      var c = costsAt(quantity, quantity < min);
      var express = expressEl && expressEl.checked ? (CFG.expressRate || 0) * quantity + (CFG.expressFee || 0) : 0;
      var net = c.product + c.branding + c.setup + c.surcharge + express;
      return { quantity: quantity, product: c.product, branding: c.branding, setup: c.setup,
        surcharge: c.surcharge, express: express, net: net, vat: net * VAT,
        total: net * (incVat ? 1 + VAT : 1) };
    }
    return {
      product: $('p-h').textContent, sku: document.querySelector('.buy__sku b').textContent,
      image: stage ? stage.src : '', description: document.querySelector('.buy__lede').textContent,
      production: Math.max(1, (CFG.baseLead || 0) + costsAt(n, n < min).lead - (expressEl && expressEl.checked ? CFG.expressSaving || 0 : 0)) + ' working days',
      delivery: (expressEl && expressEl.checked ? CFG.expressShip || 1 : CFG.baseShip || 2) + ' working days',
      colour: $('colour-val') ? $('colour-val').textContent : '',
      size: sizeVal ? sizeVal.textContent : '',
      sizes: grid ? gridInputs.filter(function (input) { return Number(input.value) > 0; }).map(function (input) { return { size: input.dataset.size, quantity: Number(input.value) }; }) : [],
      locations: locs().map(function (loc) {
        var m = methodOf(loc), logoSize = chosen(loc, 'logo');
        return { area: loc.dataset.area, method: m.name,
          colours: m.cmyk ? 'Full colour' : String(tileValue(loc, 'colours', 1)),
          logoSize: logoSize && !role(loc, 'logo-field').hidden ? logoSize.dataset.value + ' cm²' : '' };
      }),
      contact: { name: form.elements.name.value.trim(), email: form.elements.email.value.trim(), phone: form.elements.phone.value.trim(), company: form.elements.company ? form.elements.company.value.trim() : '', colleague: form.elements.colleague ? form.elements.colleague.value.trim() : '' },
      ukMainland: !!(ukEl && ukEl.checked), express: !!(expressEl && expressEl.checked),
      incVat: incVat, mockup: form.elements.mockup.checked,
      costs: quoteAt(n),
      breaks: form.elements.pricebreaks.checked ? (CFG.tiers || []).filter(function (tier) { return tier.min >= min; }).map(function (tier) { return quoteAt(tier.min); }) : [],
      source: window.location.pathname.split('/').pop()
    };
  }
  // Use the actual configuration controls in the quote, preserving their handlers.
  var quoteMoves = [], quoteConfigSlot, quoteQtySlot, quoteArtworkByArea = new Map();
  if (quoteModal && CFG.quotePreview) {
    quoteModal.classList.add('qmodal--full');
    var qForm = quoteModal.querySelector('form');
    var contact = document.createElement('section');
    contact.className = 'qquote__contact';
    while (qForm.firstChild) contact.appendChild(qForm.firstChild);
    var layout = document.createElement('div');
    layout.className = 'qquote';
    layout.innerHTML = '<section class="qquote__options" aria-label="Product configuration"><div id="quote-options-slot"></div></section>' +
      '<section class="qquote__price" aria-label="Configured quote"><h3>Quantity</h3><div id="quote-quantity-slot"></div>' +
      '<h3>Updated price with configuration</h3><p class="qquote__total"><b id="quote-total"></b> <span id="quote-tax-label">Ex VAT</span></p>' +
      '<h4>Breakdown <small>(ex VAT)</small></h4><dl id="quote-costs"></dl>' +
      '<label class="toggle"><span class="toggle__lbl">Show price with VAT</span><input type="checkbox" id="quote-display-vat"><span class="toggle__track" aria-hidden="true"></span></label>' +
      '<p class="qquote__timing" id="quote-timing"></p></section>';
    var awards = document.createElement('div'); awards.className = 'qquote__awards';
    awards.innerHTML = '<img src="assets/img/logo/bounce-badge-cream.svg" alt="Bounce Creative Designs" width="76" height="76">' +
      '<img src="assets/img/awards/bpma-winners-bounce-creative-designs-promotional-products-uk.png" alt="Award-winning merchandise supplier" width="76" height="76">' +
      '<img src="assets/img/awards/bpma-winners-2023-bounce-creative-designs-promotional-products-uk.png" alt="Award-winning promotional products" width="76" height="76">';
    contact.appendChild(awards);
    layout.appendChild(contact); qForm.appendChild(layout);
    quoteConfigSlot = $('quote-options-slot'); quoteQtySlot = $('quote-quantity-slot');
    $('qmodal-t').textContent = 'Get a quote';
    // Match the reference's contact fields; name and phone remain optional data.
    ['name', 'phone'].forEach(function (name) {
      var input = qForm.elements[name]; input.required = false; input.closest('label').hidden = true;
    });
    contact.querySelector('.qmodal__sku').hidden = true;
    $('quote-config-summary').hidden = true;
    contact.querySelector('button[value="close"]:not(.qmodal__x)').hidden = true;
    contact.querySelector('button[value="send"]').firstChild.textContent = 'Submit for a quote ';
    contact.querySelector('.qmodal__grid').classList.add('qquote__fields');
    qForm.elements.email.placeholder = 'my email address*';
    qForm.elements.colleague.placeholder = 'my colleague’s email address';
    qForm.elements.company.placeholder = 'company name';
    qForm.elements.pricebreaks.closest('label').lastChild.textContent = ' Include price breaks for different qty';
    qForm.elements.mockup.closest('label').lastChild.textContent = ' Send me a mock-up proof';
    qForm.elements.vat.closest('label').lastChild.textContent = ' Send me costs including VAT';
    var artworkField = $('quote-artwork-field');
    artworkField.textContent = ''; artworkField.hidden = false;
    var artworkHelp = document.createElement('p');
    artworkHelp.id = 'quote-artwork-note'; artworkHelp.className = 'qmodal__note';
    artworkHelp.textContent = 'AI, EPS, PDF, SVG, PNG or JPEG, up to 10 MB per file. Supply artwork for each location when requesting a mock-up.';
    artworkField.appendChild(artworkHelp);
    qForm.elements.mockup.addEventListener('change', syncQuotePanel);
    $('quote-display-vat').addEventListener('change', syncQuotePanel);
    quoteModal.addEventListener('close', function () {
      quoteMoves.forEach(function (move) { move.marker.replaceWith(move.node); });
      quoteMoves = [];
    });
  }
  function moveQuoteControls() {
    if (!quoteConfigSlot || quoteMoves.length) return;
    var nodes = all('.buy__form > fieldset.opt');
    if (locWrap) nodes.push(locWrap);
    if (grid) nodes.push(grid);
    if (qtyEl && !grid) nodes.push(qtyEl.parentElement);
    nodes.forEach(function (node) {
      var marker = document.createComment('quote control position');
      node.before(marker); quoteMoves.push({ node: node, marker: marker });
      (node === grid || node.contains(qtyEl) ? quoteQtySlot : quoteConfigSlot).appendChild(node);
    });
  }
  function syncQuotePanel() {
    if (!quoteConfigSlot || !quoteModal.open) return;
    var snap = quoteSnapshot(quoteModal.querySelector('form'), true);
    if (grid && gridTotal() === 0) {
      set($('quote-total'), 'Select sizes'); set($('quote-tax-label'), '');
      $('quote-costs').textContent = ''; set($('quote-timing'), 'Enter the quantity needed for each size to calculate your quote.');
      syncQuoteArtwork(snap.locations); return;
    }
    var displayVat = $('quote-display-vat').checked;
    set($('quote-total'), money(snap.costs.net * (displayVat ? 1 + VAT : 1)));
    set($('quote-tax-label'), displayVat ? 'Inc VAT' : 'Ex VAT');
    var dl = $('quote-costs'); dl.textContent = '';
    [['Product cost', snap.costs.product], ['Branding cost', snap.costs.branding], ['Setup cost', snap.costs.setup], ['Surcharges', snap.costs.surcharge], ['Express', snap.costs.express]].forEach(function (cost) {
      var dt = document.createElement('dt'), dd = document.createElement('dd');
      dt.textContent = cost[0] + ':'; dd.textContent = money(cost[1]); dl.append(dt, dd);
    });
    set($('quote-timing'), 'Estimated production time: ' + snap.production + '\nEstimated delivery time: ' + (snap.ukMainland ? snap.delivery : 'To be confirmed'));
    locs().forEach(function (loc) {
      var area = areaBtns.filter(function (button) { return button.dataset.area === loc.dataset.area; })[0];
      var image = area && area.querySelector('img'), thumb = loc.querySelector('.loc__thumb');
      if (image && thumb) thumb.src = image.src;
    });
    syncQuoteArtwork(snap.locations);

  }
  function syncQuoteArtwork(locations) {
    var field = $('quote-artwork-field'), form = quoteModal.querySelector('form');
    var active = locations.map(function (location) { return location.area; });
    quoteArtworkByArea.forEach(function (entry, area) {
      if (active.indexOf(area) === -1) entry.label.remove();
    });
    locations.forEach(function (location) {
      var entry = quoteArtworkByArea.get(location.area);
      if (!entry) {
        var label = document.createElement('label'); label.className = 'qfield qquote__upload';
        var title = document.createElement('span'); title.className = 'qfield__t';
        title.textContent = 'Artwork for: ' + location.area;
        var input = document.createElement('input'); input.type = 'file';
        input.name = 'artwork-' + quoteArtworkByArea.size;
        input.accept = '.ai,.eps,.pdf,.svg,.png,.jpg,.jpeg,.webp';
        input.dataset.quoteArtwork = location.area;
        input.setAttribute('aria-describedby', 'quote-artwork-note');
        var caption = document.createElement('span'); caption.className = 'qquote__drop-caption';
        caption.textContent = 'Click here or drag file here to upload';
        label.append(title, input, caption);
        input.addEventListener('change', function () {
          var file = this.files[0];
          this.setCustomValidity(file && file.size > 10 * 1024 * 1024 ? 'Choose artwork smaller than 10 MB.' : '');
          caption.textContent = file ? file.name : 'Click here or drag file here to upload';
        });
        entry = { label: label, input: input }; quoteArtworkByArea.set(location.area, entry);
      }
      entry.input.required = form.elements.mockup.checked;
      // Reuse each input so uploads survive configuration changes and reopening.
      field.insertBefore(entry.label, $('quote-artwork-note'));
    });
    field.hidden = locations.length === 0;
  }
  if (quoteModal && typeof quoteModal.showModal === 'function') {
    all('#quote-open, [data-opens="quote-modal"]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (CFG.quotePreview) {
          update();
          var form = quoteModal.querySelector('form');
          // Email VAT is an independent preference, defaulting to ex VAT.
          set($('quote-config-summary'), qtyEl.value + ' units · ' + ($('colour-val') ? $('colour-val').textContent : '') + ' · ' + locs().map(function (loc) { return loc.dataset.area + ': ' + methodOf(loc).name; }).join('; '));
          if ($('quote-preview-error')) $('quote-preview-error').hidden = true;
        }
        if (CFG.quotePreview) moveQuoteControls();
        quoteModal.showModal();
        if (CFG.quotePreview) syncQuotePanel();
      });
    });
    // Click on the backdrop (outside the form) closes, as the live popup does.
    quoteModal.addEventListener('click', function (ev) {
      if (ev.target === quoteModal) quoteModal.close('close');
    });
    var quoteForm = quoteModal.querySelector('form');
    if (quoteForm) {
      quoteForm.addEventListener('submit', async function (ev) {
        // "Cancel" and the close button submit with value=close, which the
        // dialog method handles; a send needs the required fields first.
        if (ev.submitter && ev.submitter.value === 'send' && !quoteForm.checkValidity()) {
          ev.preventDefault();
          quoteForm.reportValidity();
          return;
        }
        if (CFG.quotePreview && ev.submitter && ev.submitter.value === 'send') {
          ev.preventDefault();
          try {
            if (grid && gridTotal() === 0) {
              set($('quote-preview-error'), 'Enter a quantity for at least one size.');
              $('quote-preview-error').hidden = false;
              gridInputs[0].focus(); return;
            }
            var snapshot = quoteSnapshot(quoteForm);
            snapshot.artworks = [];
            for (var input of all('[data-quote-artwork]', quoteForm)) {
              var file = input.files[0];
              if (file) {
                var attachment = await window.BounceQuoteArtwork.save(file);
                attachment.area = input.dataset.quoteArtwork;
                snapshot.artworks.push(attachment);
              }
            }
            if (snapshot.artworks.length) snapshot.artwork = snapshot.artworks[0];
            sessionStorage.setItem('bounce-quote-preview', JSON.stringify(snapshot));
            window.location.assign('email-quote-v4.html');
          } catch (error) {
            set($('quote-preview-error'), 'The quote preview could not be opened. Please try again.');
            if ($('quote-preview-error')) $('quote-preview-error').hidden = false;
          }
        }
      });
    }
  }

  // Bespoke products retain their request form; the team confirms the price.
  var bespokeForm = document.querySelector('.qform');
  if (bespokeForm) {
    var bespokeArtwork = bespokeForm.elements.artwork, bespokeQty = $('qty-quote');
    bespokeQty.required = true;
    var bespokeCaption = bespokeArtwork.parentElement.querySelector('span');
    bespokeArtwork.addEventListener('change', function () {
      var file = this.files[0];
      this.setCustomValidity(file && file.size > 10 * 1024 * 1024 ? 'Choose artwork smaller than 10 MB.' : '');
      bespokeCaption.textContent = file ? file.name : 'Click or drag a file here to upload';
    });
    bespokeForm.elements.mockup.addEventListener('change', function () { bespokeArtwork.required = this.checked; });
    bespokeForm.addEventListener('submit', async function (ev) {
      ev.preventDefault();
      if (!bespokeForm.reportValidity()) return;
      var error = $('bespoke-quote-error'); error.hidden = true;
      try {
        var request = {
          product: $('p-h').textContent, sku: document.querySelector('.buy__sku b').textContent,
          image: stage ? stage.src : '', description: document.querySelector('.buy__lede').textContent,
          source: window.location.pathname.split('/').pop(), pricingPending: true,
          costs: { quantity: Number(bespokeQty.value) }, breaks: [], locations: [],
          colour: 'To be confirmed', production: 'To be confirmed', delivery: 'To be confirmed',
          ukMainland: bespokeForm.elements.uk.checked, incVat: bespokeForm.elements.vat.checked,
          mockup: bespokeForm.elements.mockup.checked,
          contact: { name: bespokeForm.elements.name.value.trim(), email: bespokeForm.elements.email.value.trim(), company: bespokeForm.elements.company.value.trim() },
          artworks: []
        };
        if (bespokeArtwork.files[0]) {
          var attachment = await window.BounceQuoteArtwork.save(bespokeArtwork.files[0]);
          attachment.area = 'Artwork'; request.artworks.push(attachment);
        }
        sessionStorage.setItem('bounce-quote-preview', JSON.stringify(request));
        window.location.assign('email-quote-v4.html');
      } catch (failure) { error.textContent = 'The quote preview could not be opened. Please try again.'; error.hidden = false; }
    });
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
