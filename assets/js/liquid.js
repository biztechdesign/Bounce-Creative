/* ==========================================================================
   Liquid CTA buttons
   A pill is drawn as an SVG path behind the label. On hover the path's
   perimeter points are pushed outward toward the cursor with a gaussian
   falloff, so the shape bulges and follows the pointer, while the fill and
   label colour swap. Reference: the CTA treatment on labs.google.
   ========================================================================== */
(function () {
  'use strict';

  var SAMPLES = 72;      // perimeter points — enough to stay smooth under deformation
  var BULGE = 0.115;     // peak displacement, as a fraction of button height
  var REACH = 0.60;      // gaussian sigma, as a fraction of button height
  var EASE = 0.18;       // per-frame approach toward the target state

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Sample a stadium (pill) outline, returning each point and its outward normal. */
  function outline(w, h) {
    var r = Math.min(h, w) / 2;
    var edge = Math.max(0, w - 2 * r);
    var arc = Math.PI * r;
    var total = 2 * edge + 2 * arc;
    var pts = [];

    for (var i = 0; i < SAMPLES; i++) {
      var s = total * i / SAMPLES;
      var x, y, nx, ny, a;

      if (s < edge) {                       // top edge, left to right
        x = r + s; y = 0; nx = 0; ny = -1;
      } else if (s < edge + arc) {          // right cap
        a = -Math.PI / 2 + (s - edge) / r;
        nx = Math.cos(a); ny = Math.sin(a);
        x = (w - r) + r * nx; y = r + r * ny;
      } else if (s < 2 * edge + arc) {      // bottom edge, right to left
        x = (w - r) - (s - edge - arc); y = h; nx = 0; ny = 1;
      } else {                              // left cap
        a = Math.PI / 2 + (s - 2 * edge - arc) / r;
        nx = Math.cos(a); ny = Math.sin(a);
        x = r + r * nx; y = r + r * ny;
      }
      pts.push({ x: x, y: y, nx: nx, ny: ny });
    }
    return pts;
  }

  /* Closed Catmull-Rom through the points, emitted as cubic beziers. */
  function toPath(p) {
    var n = p.length, d = 'M' + p[0].x.toFixed(2) + ',' + p[0].y.toFixed(2);
    for (var i = 0; i < n; i++) {
      var p0 = p[(i - 1 + n) % n], p1 = p[i], p2 = p[(i + 1) % n], p3 = p[(i + 2) % n];
      d += 'C' + (p1.x + (p2.x - p0.x) / 6).toFixed(2) + ',' + (p1.y + (p2.y - p0.y) / 6).toFixed(2) +
           ' ' + (p2.x - (p3.x - p1.x) / 6).toFixed(2) + ',' + (p2.y - (p3.y - p1.y) / 6).toFixed(2) +
           ' ' + p2.x.toFixed(2) + ',' + p2.y.toFixed(2);
    }
    return d + 'Z';
  }

  function init(btn) {
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'liquid');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    svg.appendChild(path);

    // Lift the existing label + icon above the shape.
    var inner = document.createElement('span');
    inner.className = 'btn__in';
    while (btn.firstChild) inner.appendChild(btn.firstChild);
    btn.appendChild(svg);
    btn.appendChild(inner);
    btn.classList.add('has-liquid');

    var base = [], w = 0, h = 0;
    var amp = 0, ampTo = 0;          // 0 at rest, 1 while hovered
    var cx = 0, cy = 0, tx = 0, ty = 0;
    var frame = null;

    function measure() {
      w = btn.offsetWidth; h = btn.offsetHeight;
      if (!w || !h) return;
      svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      base = outline(w, h);
      draw();
    }

    function draw() {
      if (!base.length) return;
      var reach = h * REACH, peak = h * BULGE;
      var pts = base.map(function (p) {
        if (amp < 0.001) return p;
        var dx = cx - p.x, dy = cy - p.y;
        var f = Math.exp(-(dx * dx + dy * dy) / (2 * reach * reach));
        var d = peak * amp * f;
        return { x: p.x + p.nx * d, y: p.y + p.ny * d };
      });
      path.setAttribute('d', toPath(pts));
    }

    function tick() {
      amp += (ampTo - amp) * EASE;
      cx += (tx - cx) * EASE;
      cy += (ty - cy) * EASE;
      draw();
      if (Math.abs(ampTo - amp) > 0.002 || Math.abs(tx - cx) > 0.4 || Math.abs(ty - cy) > 0.4) {
        frame = requestAnimationFrame(tick);
      } else {
        amp = ampTo; cx = tx; cy = ty; draw(); frame = null;
      }
    }

    function run() { if (frame === null) frame = requestAnimationFrame(tick); }

    function point(e) {
      var r = btn.getBoundingClientRect();
      tx = e.clientX - r.left; ty = e.clientY - r.top;
    }

    btn.addEventListener('pointerenter', function (e) {
      point(e); cx = tx; cy = ty;
      ampTo = 1;
      btn.setAttribute('data-liquid-hover', 'true');
      run();
    });
    btn.addEventListener('pointermove', function (e) { point(e); run(); });
    btn.addEventListener('pointerleave', function () {
      ampTo = 0;
      btn.removeAttribute('data-liquid-hover');
      run();
    });

    measure();
    if (window.ResizeObserver) new ResizeObserver(measure).observe(btn);
    else window.addEventListener('resize', measure);

    // Web fonts change the button's width after layout.
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  }

  function start() {
    if (reduced.matches) return;   // plain colour transition instead
    var btns = document.querySelectorAll('.btn');
    for (var i = 0; i < btns.length; i++) init(btns[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
