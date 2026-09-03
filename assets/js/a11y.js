/* ==========================================================================
   Accessibility behaviours.

   1. Mobile drawer - the header hides .nav and .hdr__search below 900px, so
      the burger has to open a real panel. Modal while open: focus is trapped,
      the page behind is inert to scrolling, Esc closes, and focus returns to
      the button that opened it.
   2. Marquee pause - WCAG 2.2.2 wants a control on the page, not only a
      prefers-reduced-motion honour, for motion that runs past five seconds.
   ========================================================================== */
(function () {
  'use strict';

  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
                  'select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  /* ---------- 1. Mobile drawer ---------- */
  function initDrawer() {
    var burger = document.querySelector('.burger');
    var drawer = document.getElementById('mobile-nav');
    var scrim  = document.querySelector('.drawer-scrim');
    if (!burger || !drawer) return;

    var closeBtn = drawer.querySelector('.drawer__close');
    var isOpen = false;

    function focusable() {
      return [].slice.call(drawer.querySelectorAll(FOCUSABLE)).filter(function (el) {
        return el.offsetWidth > 0 || el.offsetHeight > 0;
      });
    }

    function open() {
      if (isOpen) return;
      isOpen = true;
      drawer.hidden = false;
      if (scrim) scrim.hidden = false;
      burger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('is-locked');
      var first = focusable()[0];
      if (first) first.focus();
      document.addEventListener('keydown', onKeydown, true);
    }

    function close(returnFocus) {
      if (!isOpen) return;
      isOpen = false;
      drawer.hidden = true;
      if (scrim) scrim.hidden = true;
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
      document.removeEventListener('keydown', onKeydown, true);
      if (returnFocus !== false) burger.focus();
    }

    function onKeydown(e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;

      var items = focusable();
      if (!items.length) return;
      var first = items[0];
      var last  = items[items.length - 1];

      // Wrap at both ends so focus cannot escape the panel behind it.
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!drawer.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }

    burger.addEventListener('click', function () { isOpen ? close() : open(); });
    if (closeBtn) closeBtn.addEventListener('click', function () { close(); });
    if (scrim) scrim.addEventListener('click', function () { close(); });

    // Following a link inside the drawer should dismiss it.
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a[href]')) close(false);
    });

    // Resizing back to desktop reveals the real nav - drop the drawer with it.
    window.addEventListener('resize', function () {
      if (isOpen && window.innerWidth > 900) close(false);
    });
  }

  /* ---------- 2. Marquee pause ---------- */
  function initMarqueePause() {
    var button = document.querySelector('.brandrow__pause');
    var row = button && button.closest('.brandrow');
    if (!button || !row) return;

    // If the OS already asks for reduced motion the track is not animating,
    // so the control has nothing to offer and is better removed than inert.
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (reduced.matches) { button.hidden = true; return; }

    button.addEventListener('click', function () {
      var paused = row.classList.toggle('is-paused');
      button.setAttribute('aria-pressed', paused ? 'true' : 'false');
      button.textContent = paused ? 'Play logo scroll' : 'Pause logo scroll';
    });
  }

  function start() {
    initDrawer();
    initMarqueePause();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
