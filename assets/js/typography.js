/* ==========================================================================
   Widow control.

   `text-wrap: balance` handles headings and `pretty` catches most body copy,
   but neither guarantees the last line carries more than one word. This binds
   the final two words of headings and body paragraphs with a non-breaking
   space, which does guarantee it at any width.

   Skipped where a forced pair would hurt: product cards and bento tiles are
   narrow, so binding two words there can overflow instead of tidy.
   ========================================================================== */
(function () {
  'use strict';

  var SELECTOR = 'h1, h2, h3, h4, p';
  var SKIP = '.prod, .bento, .marquee, .announce, .ftr, .std__facts, .usp, .cert';

  function bindLastTwoWords(el) {
    if (el.closest(SKIP)) return;

    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var last = null, node;
    while ((node = walker.nextNode())) {
      if (node.textContent.trim()) last = node;
    }
    if (!last) return;

    var text = last.textContent.replace(/\s+$/, '');
    var i = text.lastIndexOf(' ');
    // needs at least two words in this node, or there is nothing to bind
    if (i <= 0) return;
    last.textContent = text.slice(0, i) + ' ' + text.slice(i + 1);
  }

  function run(root) {
    var els = (root || document).querySelectorAll(SELECTOR);
    for (var i = 0; i < els.length; i++) bindLastTwoWords(els[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { run(); });
  } else {
    run();
  }
})();
