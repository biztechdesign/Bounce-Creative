/* ==========================================================================
   Home page v4 - behaviour.
   Carries forward the accessibility work from v3: a real mobile drawer with a
   focus trap, a pause control for the marquee, and a proper tab pattern for
   the product rails.
   ========================================================================== */
(function () {
  'use strict';

  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
                  'select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  /* ---------- Mobile drawer ---------- */
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
      document.addEventListener('keydown', onKey, true);
    }
    function close(returnFocus) {
      if (!isOpen) return;
      isOpen = false;
      drawer.hidden = true;
      if (scrim) scrim.hidden = true;
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
      document.removeEventListener('keydown', onKey, true);
      if (returnFocus !== false) burger.focus();
    }
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      var items = focusable();
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!drawer.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }

    burger.addEventListener('click', function () { isOpen ? close() : open(); });
    if (closeBtn) closeBtn.addEventListener('click', function () { close(); });
    if (scrim) scrim.addEventListener('click', function () { close(); });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a[href]')) close(false);
    });
    window.addEventListener('resize', function () {
      if (isOpen && window.innerWidth > 900) close(false);
    });
  }

  /* ---------- Product rail tabs (roving tabindex, arrow keys) ---------- */
  function initTabs(list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;
    var panels = tabs.map(function (t) {
      return document.getElementById(t.getAttribute('aria-controls'));
    });

    function select(i, focus) {
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (panels[n]) panels[n].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }

    tabs.forEach(function (t, i) {
      t.tabIndex = t.getAttribute('aria-selected') === 'true' ? 0 : -1;
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

  /* ---------- Marquee pause (WCAG 2.2.2) ---------- */
  /* There is more than one auto-scrolling row now, so each pause control
     drives whichever marquee it sits inside. */
  function initMarqueePause(button) {
    /* The control may sit outside the row it drives, so aria-controls is the
       link; falling back to an ancestor when it is nested. */
    var row = document.getElementById(button.getAttribute('aria-controls') || '') ||
              button.closest('.brandrow, .clientrow');
    if (!row) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      button.hidden = true;
      return;
    }
    button.addEventListener('click', function () {
      var paused = row.classList.toggle('is-paused');
      button.setAttribute('aria-pressed', paused ? 'true' : 'false');
      button.textContent = paused ? 'Play logo scroll' : 'Pause logo scroll';
    });
  }

  /* ---------- Scroll reveal ----------
     Purely decorative. A rAF-throttled scroll check rather than
     IntersectionObserver: this is deterministic, and since the hidden state is
     what we are undoing, an observer that silently misses an element would
     leave real content invisible. If anything is unavailable, all is shown. */
  function initReveal() {
    var items = [].slice.call(document.querySelectorAll('[data-reveal]'));
    if (!items.length) return;

    function showAll() { items.forEach(function (el) { el.classList.add('is-in'); }); items = []; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { showAll(); return; }

    var ticking = false;
    function check() {
      ticking = false;
      var limit = window.innerHeight * 0.94;
      for (var i = items.length - 1; i >= 0; i--) {
        if (items[i].getBoundingClientRect().top < limit) {
          items[i].classList.add('is-in');
          items.splice(i, 1);              // reveal once, then forget it
        }
      }
      if (!items.length) {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onScroll);
      }
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(check);
    }

    check();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    // Belt and braces: if anything above is still hidden once everything has
    // loaded, show it rather than risk a blank block.
    window.addEventListener('load', check);
  }

  function start() {
    initDrawer();
    initReveal();
    [].forEach.call(document.querySelectorAll('[role="tablist"]'), initTabs);
    [].forEach.call(document.querySelectorAll('.marquee-pause'), initMarqueePause);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
