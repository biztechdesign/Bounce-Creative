/* ==========================================================================
   Account pages: static design reference. Forms don't submit; the reward
   tabs are links. Nothing to wire up beyond stopping demo submits.
   ========================================================================== */
(function () {
  'use strict';
  [].forEach.call(document.querySelectorAll('.aform, .notify'), function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });
})();
