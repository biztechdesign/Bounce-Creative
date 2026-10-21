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
      var q = parseInt(line.querySelector('.qty input').value, 10) || 0;
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
  [].forEach.call(document.querySelectorAll('.qty input'), function (i) { i.addEventListener('input', recalc); });

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

  recalc();
})();
