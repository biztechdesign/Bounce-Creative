/* ==========================================================================
   Mega menu - behaviour.

   One panel open at a time. Opens on hover with a short intent delay (so a
   pointer crossing the strip does not flash every panel), on focus of the
   category link, or on the chevron button. Escape closes and hands focus back
   to the trigger. Tabbing out of the panel, clicking outside it, or the
   viewport dropping to the drawer breakpoint all close it.

   Touch: the first tap on a category link opens its panel instead of leaving
   the page; the second tap follows the link.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.querySelector('.nav');
  if (!nav) return;
  var items = [].slice.call(nav.querySelectorAll('.nav__item'));
  if (!items.length) return;

  var scrim = document.createElement('div');
  scrim.className = 'mega-scrim';
  scrim.setAttribute('aria-hidden', 'true');
  document.body.appendChild(scrim);

  var OPEN_DELAY = 110, CLOSE_DELAY = 220;
  var current = null, openTimer = null, closeTimer = null;
  var coarse = window.matchMedia('(hover: none), (pointer: coarse)');
  var desktop = window.matchMedia('(min-width: 901px)');

  items.forEach(function (li) {
    var panel = li.querySelector('.mega');
    if (panel) panel.removeAttribute('hidden');
  });

  function clearTimers() {
    clearTimeout(openTimer); clearTimeout(closeTimer);
    openTimer = closeTimer = null;
  }

  function open(li) {
    clearTimers();
    if (current === li) return;
    if (current) setState(current, false);
    setState(li, true);
    current = li;
    scrim.classList.add('is-on');
    document.addEventListener('keydown', onKey, true);
    document.addEventListener('pointerdown', onOutside, true);
  }

  function close(returnFocus) {
    clearTimers();
    if (!current) return;
    var li = current;
    setState(li, false);
    current = null;
    scrim.classList.remove('is-on');
    document.removeEventListener('keydown', onKey, true);
    document.removeEventListener('pointerdown', onOutside, true);
    if (returnFocus) {
      var tog = li.querySelector('.nav__tog') || li.querySelector('a');
      if (tog) tog.focus();
    }
  }

  function setState(li, on) {
    li.classList.toggle('is-open', on);
    var tog = li.querySelector('.nav__tog');
    if (tog) tog.setAttribute('aria-expanded', on ? 'true' : 'false');
  }

  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(true); }
  }
  function onOutside(e) {
    if (current && !current.contains(e.target)) close(false);
  }

  items.forEach(function (li) {
    var link  = li.querySelector(':scope > a');
    var tog   = li.querySelector('.nav__tog');
    var panel = li.querySelector('.mega');
    if (!panel) return;

    /* Hover intent */
    li.addEventListener('pointerenter', function (e) {
      if (e.pointerType === 'touch' || !desktop.matches) return;
      clearTimeout(closeTimer);
      if (current === li) return;
      openTimer = setTimeout(function () { open(li); }, current ? 40 : OPEN_DELAY);
    });
    li.addEventListener('pointerleave', function (e) {
      if (e.pointerType === 'touch') return;
      clearTimeout(openTimer);
      closeTimer = setTimeout(function () { if (current === li) close(false); }, CLOSE_DELAY);
    });

    /* Keyboard: focus on the category link opens its panel. */
    if (link) {
      link.addEventListener('focus', function () { if (desktop.matches) open(li); });
      link.addEventListener('click', function (e) {
        if (coarse.matches && desktop.matches && current !== li) {
          e.preventDefault(); open(li);
        }
      });
    }
    if (tog) {
      tog.addEventListener('click', function () {
        current === li ? close(false) : open(li);
      });
    }

    /* Tabbing out of the item closes it. */
    li.addEventListener('focusout', function (e) {
      if (current !== li) return;
      var next = e.relatedTarget;
      if (!next || !li.contains(next)) {
        /* Let a focus move into a sibling trigger open that one instead. */
        setTimeout(function () {
          if (current === li && !li.contains(document.activeElement)) close(false);
        }, 0);
      }
    });
  });

  window.addEventListener('resize', function () {
    if (current && !desktop.matches) close(false);
  });
})();
