/* ==========================================================================
   Basket: quantity steppers, live line and order totals, dismissable notes.
   ========================================================================== */
(function () {
  'use strict';
  var GBP = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' });
  var VAT = 0.2;

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
    set('t-sub', GBP.format(sub));
    set('t-vat', GBP.format(sub * VAT));
    set('t-total', GBP.format(sub * (1 + VAT)));
    set('unit-count', units);
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
