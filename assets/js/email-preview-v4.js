/* Browser preview only - email clients do not run scripts. Email images use
   the published (absolute) address, so an image that is not published yet
   falls back to this copy of the site. */
(function () {
  'use strict';
  var BASE = 'https://biztechdesign.github.io/Bounce-Creative/';
  [].forEach.call(document.querySelectorAll('img[src^="' + BASE + '"]'), function (img) {
    var local = img.getAttribute('src').slice(BASE.length);
    var fallback = function () { img.removeEventListener('error', fallback); img.src = local; };
    if (img.complete && img.naturalWidth === 0) fallback();
    else img.addEventListener('error', fallback);
  });
})();
