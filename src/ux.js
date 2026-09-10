/* Page interaction layer: scroll reveal, section tracking, reading progress,
   card pointer spotlight, and flow-diagram animation. All additive and
   guarded, so nothing here can break the prototypes above. */
(function () {
  var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- scroll reveal ---------------------------------------------------- */
  var rv = document.querySelectorAll('[data-rv]');
  if (RM || !('IntersectionObserver' in window)) {
    for (var i = 0; i < rv.length; i++) rv[i].classList.add('in');
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    for (var j = 0; j < rv.length; j++) io.observe(rv[j]);
  }

  /* ---- flow diagrams animate only while on screen ----------------------- */
  var flows = document.querySelectorAll('.flow');
  if (!RM && 'IntersectionObserver' in window) {
    var fo = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('on', e.isIntersecting); });
    }, { threshold: 0.15 });
    for (var f = 0; f < flows.length; f++) fo.observe(flows[f]);
  }

  /* ---- reading progress ------------------------------------------------- */
  var bar = document.querySelector('.bar');
  var prog = null;
  if (bar) { prog = document.createElement('div'); prog.className = 'prog'; bar.appendChild(prog); }

  /* ---- active section in the nav ---------------------------------------- */
  var links = [].slice.call(document.querySelectorAll('.nav a'));
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });

  var ticking = false;
  function frame() {
    ticking = false;
    if (prog) {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      prog.style.width = (max > 0 ? Math.min(100, (h.scrollTop / max) * 100) : 0) + '%';
    }
    var best = -1, y = window.scrollY + 160;
    for (var k = 0; k < secs.length; k++) if (secs[k] && secs[k].offsetTop <= y) best = k;
    for (var m = 0; m < links.length; m++) links[m].classList.toggle('act', m === best);
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  frame();

  /* ---- pointer spotlight on cards --------------------------------------- */
  if (!RM && window.matchMedia && window.matchMedia('(hover: hover)').matches) {
    document.addEventListener('pointermove', function (e) {
      var c = e.target.closest && e.target.closest('.card');
      if (!c) return;
      var r = c.getBoundingClientRect();
      c.style.setProperty('--px', (e.clientX - r.left) + 'px');
      c.style.setProperty('--py', (e.clientY - r.top) + 'px');
    }, { passive: true });
  }

  /* ---- deep link straight to an open build ------------------------------ */
  function openFromHash() {
    var id = location.hash.slice(1);
    if (!id || id.indexOf('b-') !== 0) return;
    var el = document.getElementById(id);
    if (el) { el.classList.add('open'); el.scrollIntoView({ block: 'start' }); }
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();
