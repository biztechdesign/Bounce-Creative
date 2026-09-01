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

  function initScrollers() {
    var rails = [].slice.call(document.querySelectorAll('.rail'));
    rails.forEach(function (rail) {
      if (rail.parentElement.classList.contains('rail-wrap')) return;

      var wrap = document.createElement('div');
      wrap.className = 'rail-wrap';
      rail.parentNode.insertBefore(wrap, rail);
      wrap.appendChild(rail);

      var controls = document.createElement('div');
      controls.className = 'rail-controls';

      var previous = document.createElement('button');
      previous.className = 'rail-control rail-control--prev';
      previous.type = 'button';
      previous.setAttribute('aria-label', 'Scroll products left');
      previous.innerHTML = '<svg class="ic" width="20" height="20" aria-hidden="true"><use href="#i-chevron"></use></svg>';

      var next = document.createElement('button');
      next.className = 'rail-control rail-control--next';
      next.type = 'button';
      next.setAttribute('aria-label', 'Scroll products right');
      next.innerHTML = '<svg class="ic" width="20" height="20" aria-hidden="true"><use href="#i-chevron"></use></svg>';

      controls.appendChild(previous);
      controls.appendChild(next);
      wrap.appendChild(controls);

      function update() {
        var overflowing = rail.scrollWidth > rail.clientWidth + 1;
        controls.hidden = !overflowing;
        var atStart = rail.scrollLeft <= 1;
        var atEnd = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 1;
        previous.hidden = !overflowing;
        next.hidden = !overflowing;
        previous.disabled = !overflowing || atStart;
        next.disabled = !overflowing || atEnd;
      }

      previous.addEventListener('click', function () { rail.scrollBy({ left:-rail.clientWidth * .82, behavior:'smooth' }); });
      next.addEventListener('click', function () { rail.scrollBy({ left:rail.clientWidth * .82, behavior:'smooth' }); });
      rail.addEventListener('scroll', update, { passive:true });
      window.addEventListener('resize', update);
      update();
    });
  }

  function start() {
    [].forEach.call(document.querySelectorAll('[role="tablist"]'), init);
    initScrollers();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
