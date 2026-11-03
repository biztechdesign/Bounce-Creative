/* ==========================================================================
   Spin & Win - prototype behaviour for the design review.

   Everyone can spin, guests included (client round 3). A guest who wins
   is asked to create an account or log in to CLAIM; the log-in page
   returns here with ?spin=open and the prize is claimed. States:
     details (not logged in) -> ready -> busy -> claimed -> used (next visit)
   The first form is the account step: a new email creates an account (the
   details are filled in, a set-password link is emailed); an existing email
   logs in. The prize then goes straight into the account.
   One spin per customer per day. Expiry: points 24 hours, the rest 30 days.

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
  var KEY = 'bounce-spin', LOGIN_KEY = 'bounce-login', LEAD_KEY = 'bounce-spin-lead';

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
    try {
      var held = JSON.parse(get(KEY) || 'null');
      // Back from log-in with a prize waiting: keep it so it is claimed below.
      if (guest || !(held && held.claimed === false)) localStorage.removeItem(KEY);
      if (guest) { ['bounce-name', 'bounce-new-account', 'bounce-accounts', LOGIN_KEY, LEAD_KEY].forEach(function (k) { localStorage.removeItem(k); }); }
    } catch (e) {}
    params.delete('spin');
    var qs = params.toString();
    history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : '') + window.location.hash);
  }
  var state = load();
  var loggedIn = member || get(LOGIN_KEY) === '1';
  // The guest's details from the first step ([BUILD] stored server-side as a lead).
  var lead = null;
  try { lead = JSON.parse(get(LEAD_KEY) || 'null'); } catch (e) {}
  // Points before today's spin: the demo account has 500, a new account 0.
  var BASE_BALANCE = get('bounce-new-account') === '1' ? 0 : 500;
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
    if (newBal) newBal.hidden = !(state && state.claimed !== false && PRIZES[state.prize].kind === 'points');
    // Guests see the "no account needed" line; members see their strip.
    $all('[data-member-only]', dlg).forEach(function (el) { el.hidden = !loggedIn; });
    $all('[data-guest-only]', dlg).forEach(function (el) { el.hidden = loggedIn; });
    // A guest who has entered their details is greeted by name.
    var hello = dlg.querySelector('[data-spin-hello]');
    if (hello && !loggedIn && lead && lead.first) hello.textContent = 'Good luck, ' + lead.first + '!';
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
    // The details step is a full-width form; the wheel shows once it is done.
    dlg.classList.toggle('is-details', name === 'details');
    $all('[data-spin-go]', dlg).forEach(function (b) { b.disabled = name !== 'ready'; });
  }

  function prizeText(p) {
    if (p.kind === 'points') return p.value + ' reward points';
    if (p.kind === 'code') return p.value + '% off your next order';
    if (p.kind === 'delivery') return 'Free delivery';
    return 'A free gift';
  }
  function howText(p) {
    if (p.kind === 'points') return 'Added to your reward balance — worth £' + (p.value * POINT_VALUE).toFixed(2) + ' off your next order.';
    if (p.kind === 'code') return 'Use this code in the offer-code field at checkout. No minimum order.';
    if (p.kind === 'delivery') return 'Use this code at checkout for free delivery on your next order.';
    return 'A ' + DATA.freeProduct.name + ' — added to your next order with this code.';
  }
  /* Expiry from the moment it was won: points 24 hours, the rest 30 days. */
  function expText(p, at) {
    var won = new Date(at || Date.now());
    if (p.expHours) {
      var end = new Date(won.getTime() + p.expHours * 3600000);
      return 'Use within 24 hours — expires ' + end.toLocaleString('en-GB', { weekday: 'short', hour: '2-digit', minute: '2-digit' }) + '.';
    }
    var d = new Date(won.getTime() + (p.expDays || 30) * 86400000);
    return 'Valid for ' + (p.expDays || 30) + ' days — until ' + d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) + '.';
  }

  function fillResult(p) {
    $all('[data-spin-prize]', dlg).forEach(function (el) { el.textContent = prizeText(p); });
    $all('[data-spin-exp]', dlg).forEach(function (el) { el.textContent = expText(p, state && state.at); });
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

  /* ---------- Spin - everyone, guests included ---------- */
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
      // A guest's prize is held until they claim it with an account.
      state = { date: today(), prize: i, at: Date.now(), claimed: loggedIn };
      put(KEY, JSON.stringify(state));
      fillResult(PRIZES[i]);
      if (loggedIn) { credit(PRIZES[i]); paintCustomer(); show('claimed'); }
      else show('won');
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
        p.kind === 'points' ? '24 hours' : '30 days'];
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
    var used = !!state;
    var pending = used && state.claimed === false;
    if (tab) {
      tab.classList.toggle('is-used', used && !pending);
      document.getElementById('spin-tab-sub').textContent =
        pending ? 'Claim your prize' : used ? 'Next spin ' + untilMidnight() : LABEL_FREE;
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
    if (state) sync();
  }, 1000);

  /* ---------- Open / close ---------- */
  function claim() {
    // Back from log-in / create account with a prize waiting: claim it.
    state.claimed = true;
    put(KEY, JSON.stringify(state));
    credit(PRIZES[state.prize]);
    paintCustomer();
    var tag = dlg.querySelector('[data-spin-claimtag]');
    if (tag) tag.textContent = 'Prize claimed';
  }
  function open() {
    // Not logged in: always the account step first (email -> create or log in).
    if (!loggedIn) {
      show('details');
    } else if (state) {
      landOn(state.prize, false);
      if (state.claimed === false && loggedIn) claim();
      fillResult(PRIZES[state.prize]);
      if (state.claimed === false) show('won');
      else if (returned || member) show('claimed');
      else show('used');
    } else {
      show(loggedIn ? 'ready' : 'details');
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

  /* ---------- The account step: email, then create or log in ----------
     [BUILD] Look the email up: an unknown email creates the customer from the
     details (and emails a set-password link); a known one logs in. The demo
     knows the demo account and any account made in this browser. */
  var KNOWN = ['chirag.t@biztechcs.com'];
  function accounts() { try { return JSON.parse(get('bounce-accounts') || '{}'); } catch (e) { return {}; } }
  var leadForm = document.getElementById('spin-lead');
  if (leadForm) {
    var step = 'new';
    var groupsNew = $all('[data-lead-new]', leadForm);
    var groupOld = leadForm.querySelector('[data-lead-old]');
    var label = leadForm.querySelector('[data-lead-label]');
    var note = leadForm.querySelector('[data-lead-note]');
    var status = document.getElementById('spin-lead-status');
    var EMAIL = /^\S+@\S+\.[^\s.]{2,}$/;
    var newInputs = function () { return $all('input', leadForm).filter(function (i) { return i.closest('[data-lead-new]'); }); };
    /* The full form shows first. An existing email swaps the details for the
       password; a new (or unfinished) email keeps the full form. */
    var setStep = function (next) {
      step = next;
      groupsNew.forEach(function (g) { g.hidden = next !== 'new'; });
      groupOld.hidden = next !== 'old';
      newInputs().forEach(function (i) { i.disabled = next !== 'new'; });
      $all('input', groupOld).forEach(function (i) { i.disabled = next !== 'old'; });
      label.textContent = next === 'old' ? 'Log in & spin' : 'Get ready to spin';
      note.hidden = next === 'old';
    };
    var check = function (inputs) {
      var ok = true;
      inputs.forEach(function (inp) {
        var v = inp.value.trim();
        var bad = (inp.required && !v) || (inp.type === 'email' && v && !EMAIL.test(v));
        inp.classList.toggle('is-bad', bad);
        inp.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad && ok) { inp.focus(); ok = false; }
      });
      return ok;
    };
    var known = function (email) {
      return accounts()[email] || (KNOWN.indexOf(email) !== -1 ? { first: 'Anjana', last: 'Solanki' } : null);
    };
    var lookup = function () {
      var email = leadForm.email.value.trim().toLowerCase();
      if (!EMAIL.test(email)) { status.hidden = true; if (step !== 'new') setStep('new'); return; }
      var who = known(email);
      status.hidden = false;
      status.className = 'spinlead__status ' + (who ? 'is-old' : 'is-new');
      status.textContent = who
        ? 'Welcome back, ' + who.first + ' - you already have an account. Enter your password to spin.'
        : 'New here - we\u2019ll create your free account with these details.';
      if (step !== (who ? 'old' : 'new')) setStep(who ? 'old' : 'new');
    };
    var timer;
    leadForm.email.addEventListener('input', function () {
      // Editing the email clears the old answer straight away; it is checked
      // again once typing pauses.
      status.hidden = true;
      clearTimeout(timer);
      timer = setTimeout(lookup, 450);
    });
    leadForm.email.addEventListener('change', function () { clearTimeout(timer); lookup(); });
    var signIn = function (name, isNew) {
      put(LOGIN_KEY, '1');
      put('bounce-name', name);
      put('bounce-new-account', isNew ? '1' : '0');
      loggedIn = true;
      BASE_BALANCE = isNew ? 0 : 500;
      paintCustomer();
      sync();
      if (state) { landOn(state.prize, false); fillResult(PRIZES[state.prize]); show('used'); }
      else show('ready');
      var go = dlg.querySelector('.spindlg__go');
      if (go) go.focus();
    };
    setStep('new');
    leadForm.addEventListener('submit', function (e) {
      e.preventDefault();
      lookup();
      var email = leadForm.email.value.trim().toLowerCase();
      if (step === 'new') {
        if (!check(newInputs().slice(0, 2).concat([leadForm.email], newInputs().slice(2)))) return;
        var acc = {};
        newInputs().forEach(function (i) { acc[i.name] = i.value.trim(); });
        var all2 = accounts(); all2[email] = acc; put('bounce-accounts', JSON.stringify(all2));
        lead = acc; lead.email = email; put(LEAD_KEY, JSON.stringify(lead));
        signIn((acc.first + ' ' + acc.last).trim(), true);
        return;
      }
      if (!check([leadForm.email, leadForm.password])) return;
      var who = known(email) || { first: 'Anjana', last: 'Solanki' };
      signIn((who.first + ' ' + (who.last || '')).trim(), false);
    });
  }

  var reset = dlg.querySelector('[data-spin-reset]');
  if (reset) reset.addEventListener('click', function () {
    try { ['bounce-name', 'bounce-new-account', 'bounce-accounts', KEY, LOGIN_KEY, LEAD_KEY].forEach(function (k) { localStorage.removeItem(k); }); } catch (e) {}
    window.location.reload();
  });

  /* A spin already taken today still shows on the balance after a reload. */
  if (state && member && state.claimed !== false) credit(PRIZES[state.prize]);
  if (state) fillResult(PRIZES[state.prize]);
  paintCustomer();
  sync();
  if (returned || guest) open();
})();
