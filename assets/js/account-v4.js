/* ==========================================================================
   Account pages: static design reference. Forms don't submit; the reward
   tabs are links. Nothing to wire up beyond stopping demo submits.

   Log in / create account: ?referer=<page> is where the customer came
   from (Spin & Win sends <page>?spin=open). Prototype only - a valid form
   "logs in" and goes back there.
   [BUILD] Magento customer login / create, then redirect to the referer.
   ========================================================================== */
(function () {
  'use strict';
  [].forEach.call(document.querySelectorAll('.aform, .notify'), function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });

  var form = document.querySelector('[data-auth-form]');
  if (!form) return;

  // Only same-site pages: the referer comes from the URL.
  var ref = new URLSearchParams(window.location.search).get('referer') || '';
  if (!/^[\w\-\/.]*\.html(\?[\w=&\-]*)?$/.test(ref.replace(/^.*\//, ''))) ref = '';
  var back = ref ? ref.replace(/^.*\//, '') : 'account-rewards-v4.html';

  var note = document.querySelector('[data-auth-spin]');
  if (note) note.hidden = !/spin=open/.test(ref);

  // Switching between log in and create account keeps the way back.
  [].forEach.call(document.querySelectorAll('[data-auth-keep]'), function (a) {
    if (ref) a.href = a.getAttribute('href') + '?referer=' + encodeURIComponent(ref);
  });

  form.addEventListener('submit', function () {
    var ok = true;
    [].forEach.call(form.querySelectorAll('input[required]'), function (inp) {
      var v = inp.value.trim();
      var bad = !v || (inp.type === 'email' && !/^\S+@\S+\.\S+$/.test(v)) ||
                (inp.type === 'password' && v.length < 8) ||
                (inp.name === 'password_confirmation' && v !== form.password.value);
      inp.classList.toggle('is-bad', bad);
      inp.setAttribute('aria-invalid', bad ? 'true' : 'false');
      if (bad && ok) { inp.focus(); ok = false; }
    });
    if (!ok) return;
    try {
      localStorage.setItem('bounce-login', '1');
      if (form.dataset.authForm === 'register') {
        localStorage.setItem('bounce-name', (form.firstname.value.trim() + ' ' + form.lastname.value.trim()).trim());
      }
    } catch (e) {}
    window.location.href = back;
  });
})();
