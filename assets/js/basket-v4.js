/* ==========================================================================
   Basket: quantity steppers, live line and order totals, dismissable notes.
   ========================================================================== */
(function () {
  'use strict';
  var GBP = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });
  var VAT = 0.2;

  // Reward points: the slider and the number field mirror each other; the
  // discount comes off the ex-VAT subtotal and cannot exceed it.
  var pts = document.querySelector('.pts');
  var ptsRange = document.getElementById('pts-range');
  var ptsN = document.getElementById('pts-n');
  var ptsMax = document.getElementById('pts-max');
  var PT_VALUE = pts ? parseFloat(pts.dataset.value) || 0 : 0;
  var PT_BAL = pts ? parseInt(pts.dataset.balance, 10) || 0 : 0;

  function pointsSpent() {
    if (!ptsN) return 0;
    var n = parseInt(ptsN.value, 10) || 0;
    return Math.min(PT_BAL, Math.max(0, n));
  }

  /* Discount codes. QUOTE5 arrives from the email quote's "Order now and
     save an extra 5%" button (?code=QUOTE5) and is applied automatically;
     the same code typed into the field applies too. */
  var CODES = {
    QUOTE5: { pct: 0.05, desc: '5% off for ordering from your email quote' },
    // Spin & Win prizes, entered in the same offer-code field
    SPIN5: { pct: 0.05, desc: '5% off - your Spin & Win prize' },
    SPIN10: { pct: 0.10, desc: '10% off - your Spin & Win prize' },
    SPINSHIP: { pct: 0, ship: true, desc: 'free delivery - your Spin & Win prize' },
    SPINGIFT: { pct: 0, gift: true, desc: 'a free branded cotton shopper is added to this order' }
  };
  var codePct = 0;
  var codeForm = document.querySelector('form.code');
  var codeInput = document.getElementById('code');
  function applyCode(raw) {
    var key = String(raw || '').trim().toUpperCase();
    var hit = CODES[key];
    var ok = document.getElementById('code-ok');
    codePct = hit ? hit.pct : 0;
    var shipDd = document.querySelector('.totals__ship dd');
    if (shipDd) shipDd.textContent = hit && hit.ship ? 'Free' : 'Calculated at checkout';
    var codeRow = document.getElementById('t-code-row');
    if (codeRow) codeRow.dataset.always = hit && (hit.ship || hit.gift) ? '1' : '';
    if (ok) {
      ok.hidden = !hit;
      if (hit) {
        document.getElementById('code-name').textContent = key;
        document.getElementById('code-desc').textContent = hit.desc;
        document.getElementById('t-code-n').textContent = key;
      }
    }
    if (codeInput && hit) codeInput.value = key;
    return !!hit;
  }
  if (codeForm) codeForm.addEventListener('submit', function () { applyCode(codeInput.value); recalc(); });
  var fromUrl = new URLSearchParams(window.location.search).get('code');
  if (fromUrl) applyCode(fromUrl);

  function recalc() {
    var sub = 0, units = 0;
    [].forEach.call(document.querySelectorAll('.line'), function (line) {
      var each = parseFloat(line.dataset.each) || 0;
      // A line ordered by size totals its size fields; any other line has one qty.
      var sizes = line.querySelectorAll('[data-size-qty]');
      var q = 0;
      if (sizes.length) {
        [].forEach.call(sizes, function (f) { q += parseInt(f.value, 10) || 0; });
        var tot = line.querySelector('[data-role="line-units"]');
        if (tot) tot.textContent = q;
      } else if (line.dataset.units) {
        q = parseInt(line.dataset.units, 10) || 0;   // ordered by size: a fixed total
      } else {
        q = parseInt(line.querySelector('.qty input').value, 10) || 0;
      }
      units += q;
      var s = each * q; sub += s;
      line.querySelector('[data-role="line-sub"]').textContent = GBP.format(s);
    });
    var set = function (id, v) { var el = document.getElementById(id); if (el) el.textContent = v; };
    // Points: when maximising, spend only what the subtotal can absorb
    var maxUseful = PT_VALUE ? Math.min(PT_BAL, Math.floor(sub / PT_VALUE)) : 0;
    if (ptsMax && ptsMax.checked) { ptsN.value = maxUseful; ptsRange.value = maxUseful; }
    // Discount code first (a percentage of the subtotal), then points on what's left.
    var codeOff = sub * codePct;
    var codeRow = document.getElementById('t-code-row');
    if (codeRow) {
      codeRow.hidden = !codePct && !codeRow.dataset.always;
      set('t-code', codePct ? '−' + GBP.format(codeOff) : 'Applied');
    }
    var afterCode = sub - codeOff;
    if (ptsMax && ptsMax.checked && PT_VALUE) {
      maxUseful = Math.min(PT_BAL, Math.floor(afterCode / PT_VALUE));
      ptsN.value = maxUseful; ptsRange.value = maxUseful;
    }
    var spent = pointsSpent();
    var off = Math.min(afterCode, spent * PT_VALUE);
    var net = afterCode - off;
    var row = document.getElementById('t-pts-row');
    if (row) {
      row.hidden = !spent;
      set('t-pts-n', spent + ' pts');
      set('t-pts', '−' + GBP.format(off));
    }
    set('pts-worth', '= ' + GBP.format(off) + ' off');
    set('t-sub', GBP.format(sub));
    set('t-vat', GBP.format(net * VAT));
    set('t-total', GBP.format(net * (1 + VAT)));
    set('unit-count', units);
  }

  if (pts) {
    ptsRange.addEventListener('input', function () { ptsN.value = ptsRange.value; if (ptsMax.checked) ptsMax.checked = false; recalc(); });
    ptsN.addEventListener('input', function () { ptsRange.value = pointsSpent(); if (ptsMax.checked) ptsMax.checked = false; recalc(); });
    ptsN.addEventListener('change', function () { ptsN.value = pointsSpent(); recalc(); });
    ptsMax.addEventListener('change', recalc);
  }

  [].forEach.call(document.querySelectorAll('.qty__btn'), function (b) {
    b.addEventListener('click', function () {
      var field = b.parentElement.querySelector('input');
      var min = parseInt(field.min, 10) || 1;
      var n = (parseInt(field.value, 10) || min) + (b.dataset.step === 'up' ? 1 : -1);
      field.value = Math.max(min, n);
      recalc();
    });
  });
  [].forEach.call(document.querySelectorAll('.qty input, [data-size-qty]'), function (i) { i.addEventListener('input', recalc); });

  [].forEach.call(document.querySelectorAll('[data-dismiss]'), function (b) {
    b.addEventListener('click', function () {
      var t = document.getElementById(b.dataset.dismiss); if (t) t.hidden = true;
    });
  });

  // Name the chosen file in the preview caption.
  [].forEach.call(document.querySelectorAll('.drop input[type="file"]'), function (inp) {
    inp.addEventListener('change', function () {
      var cap = inp.closest('.art__up').querySelector('.art__empty');
      if (cap && inp.files.length) { cap.textContent = inp.files[0].name; cap.style.fontStyle = 'normal'; }
    });
  });

  /* ---------- Download quote ----------
     Builds a printable quote from what is on the page right now (lines,
     quantities, discount, points, VAT) and opens the print dialog, where
     "Save as PDF" gives the file. [BUILD] replace with the server-generated
     quote PDF. */
  var dl = document.getElementById('dl-quote');
  if (dl) dl.addEventListener('click', function () {
    var esc = function (t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
    var txt = function (el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; };
    var now = new Date(), valid = new Date(now.getTime() + 30 * 86400000);
    var fmt = function (d) { return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); };
    var ref = 'BC-Q' + now.getFullYear() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0') + '-' + String(Math.floor(1000 + Math.random() * 9000));
    var rows = '';
    [].forEach.call(document.querySelectorAll('.line'), function (line) {
      var cfg = [].map.call(line.querySelectorAll('.line__cfg > div'), function (d) {
        var dt = txt(d.querySelector('dt')), dd = txt(d.querySelector('dd'));
        return dd && !/pantone below/i.test(dd) ? esc(dt) + ': ' + esc(dd) : '';
      }).filter(Boolean).join(' &middot; ');
      var units = line.querySelector('[data-role="line-units"]') ? txt(line.querySelector('[data-role="line-units"]')) :
        (line.dataset.units || (line.querySelector('.qty input') || {}).value || '');
      rows += '<tr><td><b>' + esc(txt(line.querySelector('.line__name'))) + '</b><br><span class="m">' + esc(txt(line.querySelector('.line__sku'))) + '</span>' +
        (cfg ? '<br><span class="m">' + cfg + '</span>' : '') + '</td><td class="r">' + esc(units) + '</td><td class="r">' +
        GBP.format(parseFloat(line.dataset.each) || 0) + '</td><td class="r">' + esc(txt(line.querySelector('[data-role="line-sub"]'))) + '</td></tr>';
    });
    var tot = '';
    [].forEach.call(document.querySelectorAll('.totals > div'), function (d) {
      if (d.hidden) return;
      var grand = d.classList.contains('totals__grand');
      tot += '<tr' + (grand ? ' class="g"' : '') + '><td>' + esc(txt(d.querySelector('dt'))) + '</td><td class="r">' + esc(txt(d.querySelector('dd'))) + '</td></tr>';
    });
    var html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Quote ' + ref + '</title><style>' +
      '@page{margin:16mm}body{font:14px/1.45 Arial,Helvetica,sans-serif;color:#10302a;margin:0}' +
      'h1{font-size:26px;margin:0}.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid #10302a;padding-bottom:14px;margin-bottom:20px}' +
      '.top p{margin:2px 0}.brand{font-weight:800;font-size:18px}table{width:100%;border-collapse:collapse}' +
      'th{text-align:left;font-size:11px;letter-spacing:.08em;text-transform:uppercase;border-bottom:1px solid #10302a;padding:8px 6px}' +
      'td{padding:10px 6px;border-bottom:1px solid #d9d9d4;vertical-align:top}.r{text-align:right;white-space:nowrap}th.r{text-align:right}' +
      '.m{color:#55665f;font-size:12px}.tot{width:55%;margin:18px 0 0 auto}.tot td{border:0;padding:5px 6px}' +
      '.g td{border-top:2px solid #10302a;font-size:18px;font-weight:800;padding-top:10px}.note{margin-top:26px;font-size:12px;color:#55665f}' +
      '</style></head><body><div class="top"><div><div class="brand">Bounce Creative Designs</div><p class="m">020 8318 9603</p></div>' +
      '<div style="text-align:right"><h1>Quote</h1><p>Ref <b>' + ref + '</b></p><p>Issued ' + fmt(now) + '</p><p>Valid until ' + fmt(valid) + '</p></div></div>' +
      '<table><thead><tr><th>Item</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Subtotal</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      '<table class="tot"><tbody>' + tot + '</tbody></table>' +
      '<p class="note">Delivery is calculated at checkout. Nothing goes to bulk production until your artwork is fully approved &mdash; our designers check every file and send a proof first. Prices are shown in GBP.</p>' +
      '</body></html>';
    var fr = document.createElement('iframe');
    fr.setAttribute('aria-hidden', 'true');
    fr.style.cssText = 'position:fixed;right:0;bottom:0;width:0;height:0;border:0';
    document.body.appendChild(fr);
    fr.contentDocument.open(); fr.contentDocument.write(html); fr.contentDocument.close();
    setTimeout(function () {
      fr.contentWindow.focus(); fr.contentWindow.print();
      setTimeout(function () { fr.remove(); }, 2000);
    }, 150);
  });

  recalc();
})();