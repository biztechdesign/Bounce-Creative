/* ==========================================================================
   Category tabs for the popular-products section.
   Panels are plain markup and ship visible-by-default, so the first panel
   still renders if this never runs.
   ========================================================================== */
(function () {
  'use strict';

  function init(list) {
    var tabs = [].slice.call(list.querySelectorAll('.tab'));
    if (!tabs.length) return;

    var panels = tabs.map(function (t) {
      return document.getElementById(t.getAttribute('aria-controls'));
    });

    function select(i, focus) {
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (panels[n]) panels[n].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }

    tabs.forEach(function (t, i) {
      t.tabIndex = t.classList.contains('is-active') ? 0 : -1;
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        var next = e.key === 'ArrowRight' ? i + 1
                 : e.key === 'ArrowLeft'  ? i - 1
                 : e.key === 'Home'       ? 0
                 : e.key === 'End'        ? tabs.length - 1
                 : null;
        if (next === null) return;
        e.preventDefault();
        select((next + tabs.length) % tabs.length, true);
      });
    });
  }

  function start() {
    [].forEach.call(document.querySelectorAll('[role="tablist"]'), init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
