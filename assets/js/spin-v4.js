/* ==========================================================================
   Spin & Win - prototype behaviour for the design review.

   States: ready -> busy -> claim (visitor) | claimed (member) -> used.
   Today's spin is kept in localStorage so a refresh shows "come back
   tomorrow". [BUILD] The real feature must decide the prize and enforce one
   spin per customer per day on the server - a browser can be cleared.
   ========================================================================== */
(function () {
  'use strict';

  var dlg = document.getElementById('spin-dlg');
  var dataEl = document.getElementById('spin-data');
  if (!dlg || !dataEl) return;

  var DATA = JSON.parse(dataEl.textContent);
  var PRIZES = DATA.prizes;
  var STEP = 360 / PRIZES.length;
  var POINT_VALUE = 0.5;                       // pounds per reward point
  var KEY = 'bounce-spin';
  var HOLD_SECONDS = 15 * 60;

  var rot = document.getElementById('wheel-rot');
  var card = document.getElementById('spin-card');      // account page only
  var member = !!card;
  var tab = document.getElementById('spin-tab');
  var angle = 0, spinning = false, holdLeft = HOLD_SECONDS;
  // On the rewards page the card is the way in; the floating tab would only
  // cover the account menu.
  if (member && tab) tab.hidden = true;

  function $all(sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); }
  function today() { var d = new Date(); return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function load() {
    try { var s = JSON.parse(localStorage.getItem(KEY) || 'null'); return s && s.date === today() ? s : null; }
    catch (e) { return null; }
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  var state = load();

  /* ---------- States ---------- */
  function show(name) {
    $all('.spinstate', dlg).forEach(function (el) { el.hidden = el.dataset.state !== name; });
    $all('[data-spin-go]', dlg).forEach(function (b) { b.disabled = name !== 'ready'; });
  }

  function prizeText(p) {
    if (p.kind === 'points') return p.value + ' reward points';
    if (p.kind === 'code') return p.value + '% off your next order';
    if (p.kind === 'delivery') return 'Free delivery';
    return 'A free ' + DATA.freeProduct.short.toLowerCase();
  }
  function howText(p) {
    if (p.kind === 'points') return 'Added to your reward balance — worth £' + (p.value * POINT_VALUE).toFixed(2) + ' off a future order.';
    if (p.kind === 'code') return 'Use this code in the offer-code field at checkout. No minimum order.';
    if (p.kind === 'delivery') return 'Use this code at checkout for free delivery on your next order.';
    return 'We’ll add a free ' + DATA.freeProduct.name.toLowerCase() + ' to your next order — use this code at checkout.';
  }

  function fillResult(p) {
    $all('[data-spin-prize]', dlg).forEach(function (el) { el.textContent = prizeText(p); });
    $all('[data-spin-how]', dlg).forEach(function (el) { el.textContent = howText(p); });
    var box = dlg.querySelector('[data-spin-codebox]');
    box.hidden = !p.code;
    if (p.code) dlg.querySelector('[data-spin-code]').textContent = p.code;
    var use = dlg.querySelector('[data-spin-use]');
    use.href = p.code ? 'basket-v4.html?code=' + p.code : 'products-v4.html';
    use.firstChild.nodeValue = p.code ? 'Use it now ' : 'Start shopping ';
  }

  function landOn(i, animate) {
    var target = -i * STEP + (Math.random() * 2 - 1) * (STEP * 0.32);
    if (animate) {
      var base = Math.ceil(angle / 360) * 360 + 360 * 6;
      angle = base + ((target % 360) + 360) % 360;
    } else {
      angle = target;
      rot.style.transition = 'none';
    }
    rot.style.transform = 'rotate(' + angle + 'deg)';
    if (!animate) { rot.getBoundingClientRect(); rot.style.transition = ''; }
  }

  function pick() {
    var total = PRIZES.reduce(function (s, p) { return s + p.weight; }, 0);
    var r = Math.random() * total;
    for (var i = 0; i < PRIZES.length; i++) { r -= PRIZES[i].weight; if (r < 0) return i; }
    return 0;
  }

  /* ---------- Spin ---------- */
  function spin() {
    if (spinning || state) return;
    spinning = true;
    var i = pick();
    show('busy');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    landOn(i, true);
    var done = function () {
      rot.removeEventListener('transitionend', done);
      spinning = false;
      state = { date: today(), prize: i, claimed: member };
      save(state);
      fillResult(PRIZES[i]);
      if (member) { credit(PRIZES[i]); show('claimed'); }
      else { holdLeft = HOLD_SECONDS; show('claim'); }
      sync();
    };
    if (reduced) done(); else rot.addEventListener('transitionend', done);
  }

  /* ---------- Member: credit the account page ---------- */
  function credit(p) {
    var bal = document.getElementById('bal-v');
    if (bal && p.kind === 'points') {
      var b = parseInt(bal.dataset.balance, 10) + p.value;
      bal.textContent = b.toLocaleString('en-GB');
      var worth = document.getElementById('bal-worth');
      if (worth) worth.textContent = '£' + (b * POINT_VALUE).toFixed(2);
      var earned = document.getElementById('earned-v');
      if (earned) earned.textContent = (parseInt(earned.dataset.earned, 10) + p.value).toLocaleString('en-GB');
    }
    var body = document.getElementById('tx-body');
    if (body && !document.getElementById('tx-spin')) {
      var d = new Date();
      var row = document.createElement('tr');
      row.id = 'tx-spin';
      row.innerHTML = '<td class="acct-table__muted">#39</td><td>' + ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth() + 1)).slice(-2) + '/' + d.getFullYear() +
        '</td><td>Daily spin — ' + prizeText(p).toLowerCase() + '</td><td class="acct-table__num"><b>' + (p.kind === 'points' ? '+' + p.value : (p.code || '')) +
        '</b></td><td><span class="status status--ok">Completed</span></td><td class="acct-table__muted">' + (p.kind === 'points' ? 'N/A' : '30 days') + '</td>';
      body.insertBefore(row, body.firstChild);
    }
  }

  /* ---------- Visitor: register (or log in) to claim ---------- */
  var form = document.getElementById('spin-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $all('input[required]', form).forEach(function (inp) {
        var bad = !inp.value.trim() || (inp.type === 'email' && !/^\S+@\S+\.\S+$/.test(inp.value)) ||
                  (inp.type === 'password' && inp.value.length < 8);
        inp.classList.toggle('is-bad', bad);
        inp.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad && ok) { inp.focus(); ok = false; }
      });
      if (!ok) return;
      claim();
    });
    var login = dlg.querySelector('[data-spin-login]');
    if (login) login.addEventListener('click', function (e) { e.preventDefault(); claim(); });
  }
  function claim() {
    if (!state) return;
    state.claimed = true;
    save(state);
    fillResult(PRIZES[state.prize]);
    show('claimed');
    sync();
  }

  /* ---------- Countdowns ---------- */
  function untilMidnight() {
    var n = new Date(), m = new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1);
    var s = Math.max(0, Math.floor((m - n) / 1000));
    var h = Math.floor(s / 3600), mi = Math.floor(s / 60) % 60, se = s % 60;
    return ('0' + h).slice(-2) + ':' + ('0' + mi).slice(-2) + ':' + ('0' + se).slice(-2);
  }
  function sync() {
    var used = !!state;
    var left = used ? '0 spins left today' : '1 free spin today';
    if (tab) {
      tab.classList.toggle('is-used', used);
      document.getElementById('spin-tab-sub').textContent = used ? 'Next spin ' + untilMidnight() : '1 free spin today';
    }
    $all('[data-spin-left]').forEach(function (el) { el.lastChild.nodeValue = used ? '0 spins left today' : (member ? '1 spin left today' : left); });
    if (card) {
      card.classList.toggle('is-used', used);
      var btn = document.getElementById('spin-open');
      btn.firstChild.nodeValue = used ? 'See today’s prize ' : 'Spin now ';
      var next = document.getElementById('spin-card-next');
      next.innerHTML = used ? 'You can spin again in <b>' + untilMidnight() + '</b>' : 'Next spin available <b>tomorrow at 00:00</b>';
    }
  }
  setInterval(function () {
    $all('[data-spin-countdown]', dlg).forEach(function (el) { el.textContent = untilMidnight(); });
    if (state) sync();
    if (state && !state.claimed && holdLeft > 0) {
      holdLeft--;
      $all('[data-spin-hold]', dlg).forEach(function (el) {
        el.textContent = Math.floor(holdLeft / 60) + ':' + ('0' + holdLeft % 60).slice(-2);
      });
    }
  }, 1000);

  /* ---------- Open / close ---------- */
  function open() {
    if (state) {
      landOn(state.prize, false);
      fillResult(PRIZES[state.prize]);
      show(state.claimed ? (member ? 'claimed' : 'used') : 'claim');
    } else {
      show('ready');
    }
    $all('[data-spin-countdown]', dlg).forEach(function (el) { el.textContent = untilMidnight(); });
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
  }
  if (tab) tab.addEventListener('click', open);
  var openBtn = document.getElementById('spin-open');
  if (openBtn) openBtn.addEventListener('click', open);
  $all('[data-spin-go]', dlg).forEach(function (b) { b.addEventListener('click', spin); });
  $all('[data-spin-close]', dlg).forEach(function (b) { b.addEventListener('click', function () { dlg.close(); }); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

  var copy = dlg.querySelector('[data-spin-copy]');
  if (copy) copy.addEventListener('click', function () {
    var code = dlg.querySelector('[data-spin-code]').textContent;
    var done = function () { copy.textContent = 'Copied'; setTimeout(function () { copy.textContent = 'Copy code'; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(code).then(done, done); else done();
  });

  var reset = dlg.querySelector('[data-spin-reset]');
  if (reset) reset.addEventListener('click', function () {
    try { localStorage.removeItem(KEY); } catch (e) {}
    window.location.reload();
  });

  /* On the account page, a claimed spin shows on the balance after a reload. */
  if (state && member && state.claimed) credit(PRIZES[state.prize]);
  sync();
})();
