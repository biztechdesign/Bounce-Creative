/* ==========================================================================
   Spin & Win - prototype behaviour for the design review.

   Logged-in customers only. Logged out, the wheel shows with log-in
   buttons that go to the log-in page, which returns to this page with
   ?spin=open. States:
     guest (logged out) | ready -> busy -> claimed -> used (next visit)
   One spin per account per day.

   Prototype only: "logged in" and today's spin are kept in localStorage.
   There is no log-in page in the design, so ?spin=open stands in for
   "back from log-in": it logs in the demo customer and opens the wheel.
   [BUILD] Check the real session, decide the prize and enforce the daily
   limit on the server - a browser can be cleared.
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
  var KEY = 'bounce-spin', LOGIN_KEY = 'bounce-login';

  var rot = document.getElementById('wheel-rot');
  var card = document.getElementById('spin-card');      // account page = logged in
  var member = !!card;
  var tab = document.getElementById('spin-tab');
  var angle = 0, spinning = false;

  function $all(sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); }
  function today() { var d = new Date(); return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load() {
    try { var s = JSON.parse(get(KEY) || 'null'); return s && s.date === today() ? s : null; }
    catch (e) { return null; }
  }
  // Back from log-in (or the shared after-login link): log in, fresh spin.
  var params = new URLSearchParams(window.location.search);
  // ?spin=guest is the shared logged-out link: log out and open the wheel.
  var returned = params.get('spin') === 'open', guest = params.get('spin') === 'guest';
  if (returned || guest) {
    if (returned) put(LOGIN_KEY, '1');
    try { localStorage.removeItem(KEY); if (guest) { localStorage.removeItem(LOGIN_KEY); localStorage.removeItem('bounce-name'); } } catch (e) {}
    params.delete('spin');
    var qs = params.toString();
    history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
  }
  var state = load();
  var loggedIn = member || get(LOGIN_KEY) === '1';
  var BASE_BALANCE = 500;                      // demo account's points before today's spin
  var LABEL_FREE = '1 free spin every day';

  /* ---------- The logged-in customer: name, points, header greeting ---------- */
  function customer() { return get('bounce-name') || 'Anjana Solanki'; }
  function balance() {
    var b = BASE_BALANCE;
    if (state && PRIZES[state.prize].kind === 'points') b += PRIZES[state.prize].value;
    return b;
  }
  function paintCustomer() {
    var name = customer();
    var initials = name.split(/\s+/).map(function (w) { return w.charAt(0); }).join('').slice(0, 2).toUpperCase();
    $all('[data-spin-name]', dlg).forEach(function (el) { el.textContent = name; });
    $all('[data-spin-initials]', dlg).forEach(function (el) { el.textContent = initials; });
    $all('[data-spin-bal]', dlg).forEach(function (el) { el.textContent = balance().toLocaleString('en-GB'); });
    $all('[data-spin-worth]', dlg).forEach(function (el) { el.textContent = '£' + (balance() * POINT_VALUE).toFixed(2); });
    var newBal = dlg.querySelector('[data-spin-newbal]');
    if (newBal) newBal.hidden = !(state && PRIZES[state.prize].kind === 'points');
    // Header: "Account" becomes "Hi, <first name>" once logged in.
    if (loggedIn) {
      $all('.hdr__act').forEach(function (a) {
        var t = a.lastChild;
        if (t && t.nodeType === 3 && /Account|Hi,/.test(t.nodeValue)) t.nodeValue = 'Hi, ' + name.split(/\s+/)[0];
      });
    }
  }

  // On the rewards page the card is the way in; the floating tab would only
  // cover the account menu.
  if (member && tab) tab.hidden = true;
  // Same on the log-in / create-account pages: the customer is mid log-in.
  if (document.querySelector('[data-auth-form]') && tab) tab.hidden = true;

  /* ---------- States ---------- */
  function show(name) {
    $all('.spinstate', dlg).forEach(function (el) { el.hidden = el.dataset.state !== name; });
    $all('[data-spin-go]', dlg).forEach(function (b) { b.disabled = name !== 'ready' && name !== 'guest'; });
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

  /* ---------- Spin (logged in only) ---------- */
  function spin() {
    if (!loggedIn) { goLogin(); return; }
    if (spinning || state) return;
    spinning = true;
    var i = pick();
    show('busy');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    landOn(i, true);
    var done = function () {
      rot.removeEventListener('transitionend', done);
      spinning = false;
      state = { date: today(), prize: i };
      put(KEY, JSON.stringify(state));
      fillResult(PRIZES[i]);
      credit(PRIZES[i]);
      paintCustomer();
      show('claimed');
      sync();
    };
    if (reduced) done(); else rot.addEventListener('transitionend', done);
  }

  /* ---------- Credit the account page (balance + transactions) ---------- */
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
      var cells = ['#39',
        ('0' + d.getDate()).slice(-2) + '/' + ('0' + (d.getMonth() + 1)).slice(-2) + '/' + d.getFullYear(),
        'Daily spin — ' + prizeText(p).toLowerCase(),
        p.kind === 'points' ? '+' + p.value : (p.code || ''),
        'Completed',
        p.kind === 'points' ? 'N/A' : '30 days'];
      cells.forEach(function (text, k) {
        var td = document.createElement('td');
        if (k === 0 || k === 5) td.className = 'acct-table__muted';
        if (k === 3) { td.className = 'acct-table__num'; var b2 = document.createElement('b'); b2.textContent = text; td.appendChild(b2); }
        else if (k === 4) { var st = document.createElement('span'); st.className = 'status status--ok'; st.textContent = text; td.appendChild(st); }
        else td.textContent = text;
        row.appendChild(td);
      });
      body.insertBefore(row, body.firstChild);
    }
  }

  /* ---------- Logged out: go to the log-in / create-account page ----------
     The referer brings the customer back to this page with ?spin=open, so
     the wheel opens on return.
     [BUILD] Magento customer/account/login and /create with that referer. */
  function goLogin(url) {
    var back = (window.location.pathname.replace(/^.*\//, '') || 'index-v4.html') + '?spin=open';
    window.location.href = (url || 'login-v4.html') + '?referer=' + encodeURIComponent(back);
  }

  /* ---------- Countdowns and labels ---------- */
  function untilMidnight() {
    var n = new Date(), m = new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1);
    var s = Math.max(0, Math.floor((m - n) / 1000));
    var h = Math.floor(s / 3600), mi = Math.floor(s / 60) % 60, se = s % 60;
    return ('0' + h).slice(-2) + ':' + ('0' + mi).slice(-2) + ':' + ('0' + se).slice(-2);
  }
  function sync() {
    var used = !!state && loggedIn;
    if (tab) {
      tab.classList.toggle('is-used', used);
      document.getElementById('spin-tab-sub').textContent =
        !loggedIn ? 'Log in to spin' : used ? 'Next spin ' + untilMidnight() : LABEL_FREE;
    }
    $all('[data-spin-left]').forEach(function (el) { el.lastChild.nodeValue = used ? '0 spins left today' : LABEL_FREE; });
    if (card) {
      card.classList.toggle('is-used', used);
      document.getElementById('spin-open').firstChild.nodeValue = used ? 'See today’s prize ' : 'Spin now ';
      document.getElementById('spin-card-next').innerHTML = used
        ? 'You can spin again in <b>' + untilMidnight() + '</b>'
        : 'Next spin available <b>tomorrow at 00:00</b>';
    }
  }
  setInterval(function () {
    $all('[data-spin-countdown]', dlg).forEach(function (el) { el.textContent = untilMidnight(); });
    if (state && loggedIn) sync();
  }, 1000);

  /* ---------- Open / close ---------- */
  function open() {
    if (!loggedIn) {
      show('guest');
    } else if (state) {
      landOn(state.prize, false);
      fillResult(PRIZES[state.prize]);
      show(member ? 'claimed' : 'used');
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
  $all('[data-spin-login]', dlg).forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); goLogin(a.getAttribute('href')); }); });
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
    try { localStorage.removeItem(KEY); localStorage.removeItem(LOGIN_KEY); localStorage.removeItem('bounce-name'); } catch (e) {}
    window.location.reload();
  });

  /* A spin already taken today still shows on the balance after a reload. */
  if (state && member) credit(PRIZES[state.prize]);
  if (state) fillResult(PRIZES[state.prize]);
  paintCustomer();
  sync();
  if (returned || guest) open();
})();
