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
    var spent = pointsSpent();
    var off = Math.min(sub, spent * PT_VALUE);
    var net = sub - off;
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
