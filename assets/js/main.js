/* ==========================================================================
   Eda Yalanız — interactions
   GSAP 3 (ScrollTrigger, SplitText) + Lenis. Every module checks the
   motion/pointer context first; reduced-motion users get a static, fully
   usable page and touch devices get a lighter version.
   ========================================================================== */
(function () {
  'use strict';

  var html = document.documentElement;
  var body = document.body;
  var PAGE = body.getAttribute('data-page');
  var mqReduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var REDUCED = mqReduce.matches;
  var FINE = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // Re-initialise cleanly if the visitor toggles their motion preference.
  if (mqReduce.addEventListener) mqReduce.addEventListener('change', function () { location.reload(); });

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Features that must work even if the animation libraries fail to load.
  initForm();

  if (!window.gsap || !window.ScrollTrigger || !window.SplitText) {
    html.classList.add('failsafe');
    html.classList.remove('is-entering', 'is-loading');
    initBasicMenu();
    return;
  }

  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  var SplitText = window.SplitText;
  gsap.registerPlugin(ScrollTrigger, SplitText);
  gsap.defaults({ ease: 'expo.out', duration: 1.1 });
  ScrollTrigger.config({ ignoreMobileResize: true });
  window.__eyReady = true;
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  var mm = gsap.matchMedia();
  var introQueue = [];
  var introsPlayed = false;

  /* ------------------------------------------------------------------------
     Smooth scroll (desktop only — touch keeps native, momentum scrolling)
     ------------------------------------------------------------------------ */
  var lenis = null;
  if (!REDUCED && FINE && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.085, smoothWheel: true, wheelMultiplier: 0.95 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  var locks = 0;
  var scroll = {
    lock: function () {
      if (locks++ > 0) return;
      if (lenis) lenis.stop(); else html.style.overflow = 'hidden';
    },
    unlock: function () {
      if (--locks > 0) return;
      locks = 0;
      if (lenis) lenis.start(); else html.style.overflow = '';
    },
    to: function (target, immediate) {
      if (lenis) {
        lenis.scrollTo(target, { duration: 1.6, immediate: !!immediate, offset: 0 });
      } else {
        var top = typeof target === 'number' ? target : target.getBoundingClientRect().top + window.scrollY;
        window.scrollTo({ top: top, behavior: REDUCED || immediate ? 'auto' : 'smooth' });
      }
    }
  };

  window.scrollTo(0, 0);

  /* ------------------------------------------------------------------------
     Header: hide on scroll down, show on scroll up
     ------------------------------------------------------------------------ */
  var header = $('.header');
  if (header) {
    ScrollTrigger.create({
      start: 0,
      end: 'max',
      onUpdate: function (self) {
        if (html.classList.contains('menu-open')) return;
        header.classList.toggle('is-hidden', self.direction === 1 && self.scroll() > 240);
      }
    });
  }

  /* ------------------------------------------------------------------------
     Page transitions
     ------------------------------------------------------------------------ */
  var pt = $('.pt');
  var ptCols = pt ? $$('.pt__cols i', pt) : [];
  var ptLabel = pt ? $('.pt__label span', pt) : null;
  var navigating = false;
  var PAGE_NAMES = {
    '': 'Ana Sayfa', 'index.html': 'Ana Sayfa', 'hizmetler.html': 'Hizmetler',
    'portfolyo.html': 'Portfolyo', 'iletisim.html': 'İletişim'
  };

  function labelFor(url, a) {
    if (a && a.getAttribute('data-pt-label')) return a.getAttribute('data-pt-label');
    var file = url.pathname.split('/').pop();
    return PAGE_NAMES[file] || (a ? a.textContent.trim().split('\n')[0] : '');
  }

  function enterPage() {
    return new Promise(function (resolve) {
      if (!pt || !html.classList.contains('is-entering')) { html.classList.remove('is-entering'); resolve(); return; }
      ptLabel.textContent = html.getAttribute('data-pt-label') || '';
      var tl = gsap.timeline({
        onComplete: function () {
          html.classList.remove('is-entering');
          gsap.set(ptCols, { clearProps: 'transform' });
          gsap.set(ptLabel, { clearProps: 'transform' });
        }
      });
      tl.set(ptCols, { scaleY: 1 })
        .set(ptLabel, { yPercent: 0 })
        .to(ptLabel, { yPercent: -120, duration: 0.6, ease: 'power3.in' }, 0.15)
        .to(ptCols, { scaleY: 0, transformOrigin: '50% 0%', duration: 1, ease: 'expo.inOut', stagger: 0.06 }, 0.4)
        .call(resolve, null, 0.85);
    });
  }

  function leavePage(href, label) {
    if (navigating) return;
    navigating = true;
    if (REDUCED || !pt) { location.href = href; return; }
    try { sessionStorage.setItem('ey-pt', label || ' '); } catch (e) { /* storage blocked */ }
    pt.classList.add('is-active');
    ptLabel.textContent = label;
    gsap.timeline({ onComplete: function () { location.href = href; } })
      .fromTo(ptCols, { scaleY: 0 }, { scaleY: 1, transformOrigin: '50% 100%', duration: 0.85, ease: 'expo.inOut', stagger: 0.05 })
      .fromTo(ptLabel, { yPercent: 120 }, { yPercent: 0, duration: 0.8, ease: 'expo.out' }, 0.5);
  }

  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    navigating = false;
    if (pt) {
      pt.classList.remove('is-active');
      gsap.set(ptCols, { scaleY: 0 });
      gsap.set(ptLabel, { yPercent: 120 });
    }
    closeMenu(true);
  });

  var prefetched = {};
  function internalUrl(a) {
    if (!a || !a.href) return null;
    if (a.target && a.target !== '_self') return null;
    if (a.hasAttribute('download') || a.hasAttribute('data-no-transition')) return null;
    var url = new URL(a.href, location.href);
    if (url.protocol !== location.protocol || url.host !== location.host) return null;
    if (!/^(https?|file):$/.test(url.protocol)) return null;
    return url;
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest('a[href]');
    var url = internalUrl(a);
    if (!url) return;
    var samePage = url.pathname === location.pathname && url.search === location.search;
    if (samePage) {
      e.preventDefault();
      var target = url.hash && document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (menuOpen) closeMenu();
      if (target) {
        scroll.to(target);
        activatePanelById(target.id);
        if (a.classList.contains('skip')) { target.tabIndex = -1; target.focus({ preventScroll: true }); }
      } else scroll.to(0);
      return;
    }
    e.preventDefault();
    leavePage(url.href, labelFor(url, a));
  });

  document.addEventListener('pointerover', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    var url = internalUrl(a);
    if (!url || url.pathname === location.pathname || prefetched[url.pathname]) return;
    prefetched[url.pathname] = true;
    var l = document.createElement('link');
    l.rel = 'prefetch';
    l.href = url.pathname;
    document.head.appendChild(l);
  });

  $$('[data-scroll-top]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); scroll.to(0); });
  });

  /* ------------------------------------------------------------------------
     Fullscreen editorial menu
     ------------------------------------------------------------------------ */
  var menu = $('#menu');
  var menuBtn = $('.menu-btn');
  var menuOpen = false;
  var menuTl = null;
  var menuImgs = menu ? $$('.menu__img', menu) : [];
  var menuLinks = menu ? $$('.menu__link', menu) : [];
  var menuZ = 2;
  var inertTargets = $$('main, footer');

  function setMenuImage(i, instant) {
    var fig = menuImgs[i];
    if (!fig || fig.classList.contains('is-active')) return;
    menuImgs.forEach(function (f) { f.classList.remove('is-active'); });
    fig.classList.add('is-active');
    fig.style.zIndex = ++menuZ;
    if (instant || REDUCED) { gsap.set(fig, { clipPath: 'inset(0% 0% 0% 0%)' }); return; }
    gsap.fromTo(fig, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.9, ease: 'expo.out', overwrite: true });
    gsap.fromTo($('img', fig), { scale: 1.3 }, { scale: 1.08, duration: 1.4, ease: 'expo.out', overwrite: true });
  }

  function buildMenuTl() {
    var split = SplitText.create($$('.menu__text', menu), { type: 'chars', charsClass: 'char' });
    var tl = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
    tl.fromTo($('.menu__bg', menu), { clipPath: 'inset(0% 0% 100% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'expo.inOut' })
      .fromTo($$('.menu__rule', menu), { scaleX: 0 }, { scaleX: 1, duration: 1.2, stagger: 0.06, ease: 'expo.inOut' }, 0.3)
      .fromTo(split.chars, { yPercent: 120 }, { yPercent: 0, duration: 1.1, stagger: 0.014 }, 0.45)
      .fromTo($$('.menu__num', menu), { autoAlpha: 0 }, { autoAlpha: 0.55, duration: 0.6, stagger: 0.06 }, 0.7)
      .fromTo($('.menu__media', menu), { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.2, ease: 'expo.inOut' }, 0.35)
      .fromTo($$('.menu__foot > *', menu), { y: 24, autoAlpha: 0 }, { y: 0, autoAlpha: 1, duration: 0.9, stagger: 0.08 }, 0.8);
    return tl;
  }

  function openMenu() {
    if (!menu || menuOpen) return;
    menuOpen = true;
    menu.inert = false;
    menu.classList.add('is-open');
    html.classList.add('menu-open');
    menuBtn.setAttribute('aria-expanded', 'true');
    menuBtn.setAttribute('aria-label', 'Menüyü kapat');
    inertTargets.forEach(function (el) { el.inert = true; });
    scroll.lock();
    var current = menuLinks.findIndex(function (a) { return a.getAttribute('aria-current') === 'page'; });
    setMenuImage(Math.max(0, current), true);
    if (REDUCED) {
      gsap.fromTo(menu, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'none' });
    } else {
      menuTl = menuTl || buildMenuTl();
      menuTl.timeScale(1).play(0);
    }
    setTimeout(function () { if (menuOpen && menuLinks[0]) menuLinks[0].focus({ preventScroll: true }); }, REDUCED ? 50 : 600);
  }

  function closeMenu(instant) {
    if (!menu || !menuOpen) return;
    menuOpen = false;
    html.classList.remove('menu-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.setAttribute('aria-label', 'Menüyü aç');
    inertTargets.forEach(function (el) { el.inert = false; });
    scroll.unlock();
    function done() { menu.classList.remove('is-open'); menu.inert = true; }
    if (instant || REDUCED || !menuTl) { if (menuTl) menuTl.pause(0); gsap.set(menu, { clearProps: 'opacity' }); done(); return; }
    menuTl.eventCallback('onReverseComplete', done);
    menuTl.timeScale(2.2).reverse();
  }

  if (menu && menuBtn) {
    menuBtn.addEventListener('click', function () {
      if (menuOpen) { closeMenu(); menuBtn.focus({ preventScroll: true }); } else openMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menuOpen) { closeMenu(); menuBtn.focus({ preventScroll: true }); }
    });
    menuLinks.forEach(function (a, i) {
      a.addEventListener('pointerenter', function () { setMenuImage(i); });
      a.addEventListener('focus', function () { setMenuImage(i); });
    });
  }

  /* ------------------------------------------------------------------------
     Custom cursor with contextual labels (VIEW, DISCOVER, NEXT …)
     ------------------------------------------------------------------------ */
  function initCursor() {
    var cur = $('.cursor');
    if (!cur || !FINE || REDUCED) return;
    var dot = $('.cursor__dot', cur);
    var ring = $('.cursor__ring', cur);
    var label = $('.cursor__label', cur);
    html.classList.add('has-cursor');
    cur.classList.add('is-hidden');
    gsap.set([dot, ring], { x: -100, y: -100 });
    var dx = gsap.quickTo(dot, 'x', { duration: 0.1, ease: 'power3' });
    var dy = gsap.quickTo(dot, 'y', { duration: 0.1, ease: 'power3' });
    var rx = gsap.quickTo(ring, 'x', { duration: 0.5, ease: 'power3' });
    var ry = gsap.quickTo(ring, 'y', { duration: 0.5, ease: 'power3' });
    var shown = false;

    window.addEventListener('pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse') return;
      if (!shown) { gsap.set([dot, ring], { x: e.clientX, y: e.clientY }); shown = true; }
      cur.classList.remove('is-hidden');
      dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY);
    }, { passive: true });
    document.documentElement.addEventListener('mouseleave', function () { cur.classList.add('is-hidden'); });
    window.addEventListener('pointerdown', function () { cur.classList.add('is-down'); });
    window.addEventListener('pointerup', function () { cur.classList.remove('is-down'); });

    var current = null;
    var SEL = '[data-cursor], a, button, input, textarea, select, label, [role="button"]';
    document.addEventListener('pointerover', function (e) {
      var t = e.target.closest ? e.target.closest(SEL) : null;
      if (t === current) return;
      current = t;
      cur.classList.remove('is-link', 'is-label', 'is-text');
      if (!t) return;
      var text = t.getAttribute('data-cursor');
      if (text === 'none') return;
      if (text) {
        label.textContent = text;
        cur.classList.add('is-label');
      } else if (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) {
        cur.classList.add('is-text');
      } else {
        cur.classList.add('is-link');
      }
    });
  }

  /* ------------------------------------------------------------------------
     Magnetic elements: pulled toward the pointer as it approaches
     ------------------------------------------------------------------------ */
  function initMagnetic() {
    if (!FINE || REDUCED) return;
    var items = $$('[data-magnetic]').map(function (el) {
      var inner = $('[data-magnetic-inner]', el);
      return {
        el: el,
        strength: parseFloat(el.getAttribute('data-magnetic')) || 0.35,
        xTo: gsap.quickTo(el, 'x', { duration: 0.8, ease: 'power3' }),
        yTo: gsap.quickTo(el, 'y', { duration: 0.8, ease: 'power3' }),
        ixTo: inner ? gsap.quickTo(inner, 'x', { duration: 0.8, ease: 'power3' }) : null,
        iyTo: inner ? gsap.quickTo(inner, 'y', { duration: 0.8, ease: 'power3' }) : null,
        active: false
      };
    });
    if (!items.length) return;
    var mx = 0, my = 0, raf = 0;
    function tick() {
      raf = 0;
      items.forEach(function (m) {
        var r = m.el.getBoundingClientRect();
        if (!r.width) return;
        var cx = r.left + r.width / 2 - (gsap.getProperty(m.el, 'x') || 0);
        var cy = r.top + r.height / 2 - (gsap.getProperty(m.el, 'y') || 0);
        var ddx = mx - cx, ddy = my - cy;
        var radius = Math.max(r.width, r.height) / 2 + 70;
        if (Math.hypot(ddx, ddy) < radius) {
          m.active = true;
          m.xTo(ddx * m.strength); m.yTo(ddy * m.strength);
          if (m.ixTo) { m.ixTo(ddx * m.strength * 0.45); m.iyTo(ddy * m.strength * 0.45); }
        } else if (m.active) {
          m.active = false;
          m.xTo(0); m.yTo(0);
          if (m.ixTo) { m.ixTo(0); m.iyTo(0); }
        }
      });
    }
    window.addEventListener('pointermove', function (e) {
      mx = e.clientX; my = e.clientY;
      if (!raf) raf = requestAnimationFrame(tick);
    }, { passive: true });
  }

  /* ------------------------------------------------------------------------
     Image hover: distortion ripple + colour mask reveal from the pointer
     ------------------------------------------------------------------------ */
  function initHoverFX() {
    if (!FINE || REDUCED) return;
    var disp = $('#fx-distort feDisplacementMap');
    var turb = $('#fx-distort feTurbulence');
    var lastInner = null;
    $$('[data-distort]').forEach(function (media) {
      var inner = $('.media__inner', media) || media;
      var base = $('img', inner);
      if (!base) return;
      base.classList.add('media__base');
      var clone = base.cloneNode();
      clone.className = 'media__reveal';
      clone.alt = '';
      clone.setAttribute('aria-hidden', 'true');
      clone.removeAttribute('fetchpriority');
      inner.appendChild(clone);
      media.classList.add('has-reveal');

      function point(e) {
        var r = media.getBoundingClientRect();
        return (e.clientX - r.left).toFixed(0) + 'px ' + (e.clientY - r.top).toFixed(0) + 'px';
      }
      media.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse') return;
        var p = point(e);
        gsap.fromTo(clone, { clipPath: 'circle(0% at ' + p + ')' }, { clipPath: 'circle(145% at ' + p + ')', duration: 1.1, ease: 'power3.out', overwrite: true });
        if (!disp) return;
        if (lastInner && lastInner !== inner) lastInner.style.filter = '';
        lastInner = inner;
        inner.style.filter = 'url(#fx-distort)';
        gsap.killTweensOf([disp, turb]);
        gsap.fromTo(turb, { attr: { baseFrequency: '0.018 0.05' } }, { attr: { baseFrequency: '0.006 0.014' }, duration: 0.8, ease: 'power2.out' });
        gsap.fromTo(disp, { attr: { scale: 0 } }, {
          attr: { scale: 38 }, duration: 0.35, ease: 'power2.out', yoyo: true, repeat: 1,
          onComplete: function () { inner.style.filter = ''; }
        });
      });
      media.addEventListener('pointerleave', function (e) {
        if (e.pointerType !== 'mouse') return;
        gsap.to(clone, { clipPath: 'circle(0% at ' + point(e) + ')', duration: 0.8, ease: 'power3.inOut', overwrite: true });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Text splits & scroll reveals
     ------------------------------------------------------------------------ */
  function initSplits() {
    if (REDUCED) return;

    $$('[data-split]').forEach(function (el) {
      var mode = el.getAttribute('data-split');
      var isIntro = el.hasAttribute('data-intro');
      SplitText.create(el, {
        type: mode === 'chars' ? 'lines,words,chars' : 'lines',
        mask: 'lines',
        linesClass: 'line',
        autoSplit: true,
        onSplit: function (self) {
          el.style.opacity = 1;
          var targets = mode === 'chars' ? self.chars : self.lines;
          var vars = {
            yPercent: 115,
            duration: mode === 'chars' ? 1.3 : 1.2,
            stagger: mode === 'chars' ? 0.024 : 0.09,
            ease: 'expo.out'
          };
          if (isIntro) {
            // Before the page cover lifts: wait. After (e.g. a re-split on
            // font load/resize): return a live tween, SplitText syncs its time.
            if (introsPlayed) return gsap.from(targets, vars);
            vars.paused = true;
            var tw = gsap.from(targets, vars);
            introQueue.push(tw);
            return tw;
          }
          vars.scrollTrigger = { trigger: el, start: 'top 88%', once: true };
          return gsap.from(targets, vars);
        }
      });
    });

    $$('[data-reveal]').forEach(function (el) {
      gsap.from(el, {
        y: 48, autoAlpha: 0, duration: 1.3,
        scrollTrigger: { trigger: el, start: 'top 90%', once: true }
      });
    });

    $$('[data-img-reveal]').forEach(function (el) {
      var img = $('img', el);
      var tl = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 85%', once: true } });
      tl.fromTo(el, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'expo.inOut' });
      if (img) tl.fromTo(img, { scale: 1.35 }, { scale: 1, duration: 2, ease: 'expo.out' }, 0.2);
    });

    $$('.media[data-parallax]').forEach(function (el) {
      var inner = $('.media__inner', el);
      if (!inner) return;
      gsap.fromTo(inner, { yPercent: -6 }, {
        yPercent: 6, ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });
  }

  function playIntros() {
    var delay = PAGE === 'home' ? 0.55 : 0.2;
    introsPlayed = true;
    introQueue.forEach(function (tw) { if (tw) tw.delay(delay).play(); });
    var items = $$('[data-intro]:not([data-split])');
    if (!items.length || REDUCED) return;
    gsap.fromTo(items, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 1.3, stagger: 0.08, delay: delay + 0.35, ease: 'expo.out' });
  }

  /* ------------------------------------------------------------------------
     Loader (home, first visit per session)
     ------------------------------------------------------------------------ */
  function runLoader() {
    var L = $('.loader');
    if (!L || !html.classList.contains('is-loading')) return Promise.resolve();
    try { sessionStorage.setItem('ey-seen', '1'); } catch (e) { /* ignore */ }
    var count = $('.loader__count', L);
    var bar = $('.loader__bar i', L);
    var heroImg = $('.hero__media img');
    var obj = { v: 0 };
    function paint() { count.textContent = String(Math.round(obj.v)).padStart(3, '0'); }

    var imgReady = heroImg && heroImg.decode ? heroImg.decode().catch(function () {}) : Promise.resolve();
    var nameSplit = SplitText.create($('.loader__name', L), { type: 'chars' });

    return new Promise(function (resolve) {
      var first = gsap.timeline();
      first.from(nameSplit.chars, { yPercent: 110, duration: 1, stagger: 0.03 })
        .to(obj, { v: 86, duration: 1.5, ease: 'power3.inOut', onUpdate: paint }, 0)
        .to(bar, { scaleX: 0.86, duration: 1.5, ease: 'power3.inOut' }, 0);

      Promise.all([first.then ? first.then() : wait(1500), Promise.race([imgReady, wait(3500)])]).then(function () {
        gsap.timeline({ onComplete: function () { html.classList.remove('is-loading'); } })
          .to(obj, { v: 100, duration: 0.5, ease: 'power2.out', onUpdate: paint })
          .to(bar, { scaleX: 1, duration: 0.5, ease: 'power2.out' }, 0)
          .to($('.loader__content', L), { autoAlpha: 0, duration: 0.35 }, '>')
          .to($('.loader__panel--top', L), { yPercent: -100, duration: 1.2, ease: 'expo.inOut' }, '<')
          .to($('.loader__panel--bottom', L), { yPercent: 100, duration: 1.2, ease: 'expo.inOut' }, '<')
          .call(resolve, null, '<0.35');
      });
    });
  }

  /* ------------------------------------------------------------------------
     HOME — cinematic hero
     ------------------------------------------------------------------------ */
  var heroIntroTl = null;
  function initHero() {
    var hero = $('.hero');
    if (!hero || REDUCED) return;
    var media = $('.hero__media', hero);
    var img = $('img', media);
    var lines = $$('.hero__line > span', hero);
    var bars = $$('.hero__bars i', hero);
    var content = $('.hero__content', hero);
    var shade = $('.hero__shade', hero);
    var charSets = lines.map(function (l) { return SplitText.create(l, { type: 'chars' }).chars; });
    gsap.set($('.hero__title', hero), { opacity: 1 });

    heroIntroTl = gsap.timeline({ paused: true });
    heroIntroTl.fromTo(img, { scale: 1.45 }, { scale: 1.08, duration: 2.6, ease: 'expo.out' }, 0)
      .fromTo(bars, { scaleY: 0 }, { scaleY: 1, duration: 1.6, ease: 'expo.inOut' }, 0.1);
    charSets.forEach(function (chars, i) {
      heroIntroTl.fromTo(chars, { yPercent: 115 }, { yPercent: 0, duration: 1.5, stagger: 0.055, ease: 'expo.out' }, 0.2 + i * 0.16);
    });

    // Scroll-out: the frame closes like a film ending
    gsap.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } })
      .to(media, { yPercent: 22, scale: 1.12, ease: 'none' }, 0)
      .to(lines[0] ? lines[0].parentNode : [], { xPercent: -14, ease: 'none' }, 0)
      .to(lines[1] ? lines[1].parentNode : [], { xPercent: 12, ease: 'none' }, 0)
      .to(content, { autoAlpha: 0, ease: 'none', duration: 0.6 }, 0)
      .to(shade, { opacity: 0.35, ease: 'none' }, 0)
      .to(bars, { height: '16vh', ease: 'none' }, 0);
  }

  /* ------------------------------------------------------------------------
     HOME — manifesto words light up with scroll
     ------------------------------------------------------------------------ */
  function initManifesto() {
    var text = $('.manifesto__text');
    if (!text || REDUCED) return;
    var split = SplitText.create(text, { type: 'words', wordsClass: 'word' });
    var st = { trigger: text, start: 'top 82%', end: 'bottom 55%', scrub: true };
    gsap.fromTo(split.words, { opacity: 0.13 }, { opacity: 1, stagger: 0.1, ease: 'none', scrollTrigger: st });
    gsap.fromTo($$('.pill-img', text), { scale: 0, rotate: -14 }, {
      scale: 1, rotate: 0, ease: 'none',
      scrollTrigger: { trigger: text, start: 'top 80%', end: 'center 55%', scrub: true }
    });
  }

  /* ------------------------------------------------------------------------
     HOME — big scroll-bound typography with velocity skew
     ------------------------------------------------------------------------ */
  function initBigType() {
    var sec = $('.bigtype');
    if (!sec || REDUCED) return;
    var rows = $$('.bigtype__row', sec);
    rows.forEach(function (row, i) {
      gsap.fromTo(row, { xPercent: i % 2 ? -28 : 0 }, {
        xPercent: i % 2 ? 0 : -28, ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom top', scrub: 0.6 }
      });
    });
    if (!FINE) return;
    var proxy = { skew: 0 };
    var setSkew = gsap.quickSetter(rows, 'skewX', 'deg');
    ScrollTrigger.create({
      trigger: sec, start: 'top bottom', end: 'bottom top',
      onUpdate: function (self) {
        var s = gsap.utils.clamp(-10, 10, self.getVelocity() / -260);
        if (Math.abs(s) > Math.abs(proxy.skew)) {
          proxy.skew = s;
          gsap.to(proxy, { skew: 0, duration: 0.9, ease: 'power3', overwrite: true, onUpdate: function () { setSkew(proxy.skew); } });
        }
      }
    });
  }

  /* ------------------------------------------------------------------------
     HOME — cinematic scrub: a pinned scene that advances with scroll
     ------------------------------------------------------------------------ */
  function initScrub() {
    var sec = $('.scrub');
    if (!sec || REDUCED) return;
    mm.add({ desktop: '(min-width: 701px)', mobile: '(max-width: 700px)' }, function (ctx) {
      var mobile = ctx.conditions.mobile;
      sec.classList.add('is-live');
      var stage = $('.scrub__stage', sec);
      var media = $('.scrub__media', sec);
      var frames = $$('.scrub__frame', sec);
      var imgs = frames.map(function (f) { return $('img', f); });
      var chapters = $$('.scrub__chapter', sec);
      var timeList = $('.scrub__time-list', sec);
      var bars = $$('.scrub__progress b', sec);
      var n = frames.length;

      gsap.set(frames.slice(1), { clipPath: 'inset(100% 0% 0% 0%)' });
      gsap.set(chapters, { autoAlpha: 0, y: 40 });
      gsap.set(chapters[0], { autoAlpha: 1, y: 0 });

      var tl = gsap.timeline({
        defaults: { ease: 'none' },
        scrollTrigger: {
          trigger: sec,
          start: 'top top',
          end: function () { return '+=' + window.innerHeight * (mobile ? 2.8 : 4.2); },
          pin: stage,
          scrub: mobile ? 0.4 : 1,
          anticipatePin: 1,
          invalidateOnRefresh: true
        }
      });

      tl.fromTo(media, { clipPath: mobile ? 'inset(8% 5% 8% 5% round 16px)' : 'inset(14% 20% 14% 20% round 24px)' },
        { clipPath: 'inset(0% 0% 0% 0% round 0px)', duration: 1, ease: 'power2.inOut' }, 0)
        .fromTo(imgs[0], { scale: 1.35 }, { scale: 1, duration: 1.4 }, 0)
        .fromTo(bars[0], { scaleX: 0 }, { scaleX: 1, duration: 1.4 }, 0);

      for (var i = 1; i < n; i++) {
        var at = 1.4 + (i - 1) * 1.6;
        tl.to(frames[i], { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'power3.inOut' }, at)
          .fromTo(imgs[i], { scale: 1.35, yPercent: 8 }, { scale: 1, yPercent: 0, duration: 1.6 }, at)
          .to(imgs[i - 1], { scale: 1.15, yPercent: -6, duration: 1, ease: 'power2.in' }, at)
          .to(chapters[i - 1], { autoAlpha: 0, y: -40, duration: 0.45, ease: 'power2.in' }, at)
          .to(chapters[i], { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out' }, at + 0.45)
          .to(timeList, { yPercent: -(100 / n) * i, duration: 0.9, ease: 'power3.inOut' }, at)
          .fromTo(bars[i], { scaleX: 0 }, { scaleX: 1, duration: 1.6 }, at);
      }
      tl.to({}, { duration: 0.5 });

      return function () { sec.classList.remove('is-live'); };
    });
  }

  /* ------------------------------------------------------------------------
     HOME — services list with a floating, cursor-following preview
     ------------------------------------------------------------------------ */
  function initServiceList() {
    var list = $('.svc-items');
    var float = $('.svc-float');
    if (!list || !float || !FINE || REDUCED) return;
    var inner = $('.svc-float__inner', float);
    var imgs = $$('.svc-float__img', float);
    var rows = $$('.svc-row', list);
    var xTo = gsap.quickTo(float, 'x', { duration: 0.7, ease: 'power3' });
    var yTo = gsap.quickTo(float, 'y', { duration: 0.7, ease: 'power3' });
    var rTo = gsap.quickTo(inner, 'rotation', { duration: 0.9, ease: 'power3' });
    var lastX = 0, active = -1, z = 1, settle = 0;

    list.addEventListener('pointermove', function (e) {
      xTo(e.clientX); yTo(e.clientY);
      rTo(gsap.utils.clamp(-12, 12, (e.clientX - lastX) * 0.7));
      lastX = e.clientX;
      clearTimeout(settle);
      settle = setTimeout(function () { rTo(0); }, 90);
    });
    list.addEventListener('pointerenter', function (e) {
      gsap.set(float, { x: e.clientX, y: e.clientY });
      lastX = e.clientX;
      gsap.to(inner, { scale: 1, duration: 0.8, ease: 'expo.out', overwrite: 'auto' });
    });
    list.addEventListener('pointerleave', function () {
      gsap.to(inner, { scale: 0, duration: 0.6, ease: 'expo.out', overwrite: 'auto' });
      active = -1;
    });
    rows.forEach(function (row, i) {
      row.addEventListener('pointerenter', function () {
        if (i === active || !imgs[i]) return;
        active = i;
        imgs[i].style.zIndex = ++z;
        gsap.fromTo(imgs[i], { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.8, ease: 'expo.out', overwrite: true });
        gsap.fromTo($('img', imgs[i]), { scale: 1.35 }, { scale: 1, duration: 1.2, ease: 'expo.out', overwrite: true });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Horizontal gallery: vertical scroll drives a horizontal track (desktop)
     ------------------------------------------------------------------------ */
  function initHGallery() {
    if (REDUCED) return;
    $$('[data-hgal]').forEach(function (sec) {
      mm.add('(min-width: 901px)', function () {
        sec.classList.add('is-live');
        var track = $('.hgal__track', sec);
        var prog = $('.hgal__progress i', sec);
        var counter = $('.hgal__counter', sec);
        var items = $$('.hgal__item', sec);
        var total = String(items.length).padStart(2, '0');
        function dist() { return Math.max(0, track.scrollWidth - window.innerWidth); }

        var tween = gsap.to(track, {
          x: function () { return -dist(); },
          ease: 'none',
          scrollTrigger: {
            trigger: sec,
            start: 'top top',
            end: function () { return '+=' + dist(); },
            pin: true,
            scrub: 1,
            anticipatePin: 1,
            invalidateOnRefresh: true,
            onUpdate: function (self) {
              if (prog) gsap.set(prog, { scaleX: self.progress });
              if (counter) counter.textContent = String(Math.min(items.length, Math.round(self.progress * (items.length - 1)) + 1)).padStart(2, '0') + ' / ' + total;
            }
          }
        });
        if (counter) counter.textContent = '01 / ' + total;

        items.forEach(function (item) {
          var inner = $('.media__inner', item);
          if (!inner) return;
          gsap.fromTo(inner, { xPercent: -7 }, {
            xPercent: 7, ease: 'none',
            scrollTrigger: { trigger: item, containerAnimation: tween, start: 'left right', end: 'right left', scrub: true }
          });
        });

        return function () { sec.classList.remove('is-live'); };
      });
    });
  }

  /* ------------------------------------------------------------------------
     Fullscreen lightbox with FLIP open/close and clip-path transitions
     ------------------------------------------------------------------------ */
  function initLightbox() {
    var lb = $('.lb');
    var triggers = $$('[data-lb]');
    if (!lb || !triggers.length) return;
    var bg = $('.lb__bg', lb);
    var ui = $('.lb__ui', lb);
    var countEl = $('.lb__count', lb);
    var capEl = $('.lb__cap', lb);
    var closeBtn = $('.lb__close', lb);
    var prevBtns = $$('[data-lb-prev]', lb);
    var nextBtns = $$('[data-lb-next]', lb);
    var stage = $('.lb__stage', lb);

    var items = triggers.map(function (btn) {
      var img = $('img', btn);
      return {
        btn: btn,
        media: $('.media', btn) || img,
        full: btn.getAttribute('data-lb'),
        cap: btn.getAttribute('data-caption') || img.alt,
        w: parseInt(img.getAttribute('width'), 10) || 4,
        h: parseInt(img.getAttribute('height'), 10) || 5
      };
    });
    var n = items.length;
    var frames = [0, 1].map(function () {
      var el = document.createElement('figure');
      el.className = 'lb__frame';
      var img = document.createElement('img');
      img.alt = '';
      img.decoding = 'async';
      el.appendChild(img);
      stage.appendChild(el);
      gsap.set(el, { autoAlpha: 0 });
      return { el: el, img: img };
    });
    var cur = 0, index = 0, isOpen = false, busy = false, lastFocus = null, hidden = null;

    function fit(it) {
      var small = window.innerWidth < 700;
      var padX = small ? 16 : 80;
      var padY = small ? 150 : 180;
      var s = Math.min((window.innerWidth - padX * 2) / it.w, (window.innerHeight - padY) / it.h);
      var w = it.w * s, h = it.h * s;
      return { x: (window.innerWidth - w) / 2, y: (window.innerHeight - h) / 2 - (small ? 24 : 10), width: w, height: h };
    }
    function rectOf(el) {
      var r = el.getBoundingClientRect();
      return { x: r.left, y: r.top, width: r.width, height: r.height, visible: r.bottom > 0 && r.top < window.innerHeight && r.right > 0 && r.left < window.innerWidth };
    }
    function setUI() {
      countEl.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(n).padStart(2, '0');
      capEl.textContent = items[index].cap;
    }
    function hideSource(i) {
      if (hidden) hidden.style.visibility = '';
      hidden = items[i].media;
      hidden.style.visibility = 'hidden';
    }
    function preload(i) { var im = new Image(); im.src = items[(i + n) % n].full; }

    function open(i) {
      if (isOpen) return;
      isOpen = true; busy = true; index = i; lastFocus = document.activeElement;
      var it = items[i], f = frames[cur];
      f.img.src = it.full; f.img.alt = it.cap;
      var from = rectOf(it.media), to = fit(it);
      lb.inert = false;
      lb.classList.add('is-open');
      scroll.lock();
      setUI();
      hideSource(i);
      preload(i + 1); preload(i - 1);
      gsap.set(frames[1 - cur].el, { autoAlpha: 0 });
      function finish() { busy = false; closeBtn.focus({ preventScroll: true }); }
      if (REDUCED) {
        gsap.set(f.el, { x: to.x, y: to.y, width: to.width, height: to.height, autoAlpha: 1, zIndex: 1, scale: 1 });
        gsap.set([bg, ui], { opacity: 1 });
        finish();
        return;
      }
      gsap.set(f.el, { x: from.x, y: from.y, width: from.width, height: from.height, autoAlpha: 1, zIndex: 1, scale: 1, clipPath: 'inset(0% 0% 0% 0%)' });
      gsap.timeline({ onComplete: finish })
        .to(bg, { opacity: 1, duration: 0.7, ease: 'power2.out' }, 0)
        .to(f.el, { x: to.x, y: to.y, width: to.width, height: to.height, duration: 1.1, ease: 'expo.inOut' }, 0)
        .to(ui, { opacity: 1, duration: 0.6, ease: 'power2.out' }, 0.7);
    }

    function go(dir) {
      if (!isOpen || busy) return;
      busy = true;
      var next = (index + dir + n) % n;
      var it = items[next];
      var out = frames[cur], inn = frames[1 - cur];
      inn.img.src = it.full; inn.img.alt = it.cap;
      var to = fit(it);
      index = next;
      setUI();
      hideSource(next);
      preload(next + dir);
      gsap.set(inn.el, {
        x: to.x, y: to.y, width: to.width, height: to.height, autoAlpha: 1, zIndex: 2, scale: 1,
        clipPath: dir > 0 ? 'inset(0% 0% 0% 100%)' : 'inset(0% 100% 0% 0%)'
      });
      gsap.set(out.el, { zIndex: 1 });
      function done() {
        gsap.set(out.el, { autoAlpha: 0, scale: 1 });
        cur = 1 - cur;
        busy = false;
      }
      if (REDUCED) { gsap.set(inn.el, { clipPath: 'inset(0% 0% 0% 0%)' }); done(); return; }
      gsap.timeline({ onComplete: done })
        .to(inn.el, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1, ease: 'expo.inOut' }, 0)
        .fromTo(inn.img, { scale: 1.25, xPercent: dir * 8 }, { scale: 1, xPercent: 0, duration: 1.3, ease: 'expo.out' }, 0.1)
        .to(out.el, { scale: 0.88, autoAlpha: 0.25, duration: 1, ease: 'expo.inOut' }, 0);
    }

    function close() {
      if (!isOpen || busy) return;
      isOpen = false; busy = true;
      var f = frames[cur];
      var target = rectOf(items[index].media);
      function done() {
        lb.classList.remove('is-open');
        lb.inert = true;
        gsap.set(frames.map(function (x) { return x.el; }), { autoAlpha: 0 });
        gsap.set([bg, ui], { opacity: 0 });
        if (hidden) { hidden.style.visibility = ''; hidden = null; }
        scroll.unlock();
        busy = false;
        if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
      }
      if (REDUCED) { done(); return; }
      var tl = gsap.timeline({ onComplete: done });
      tl.to(ui, { opacity: 0, duration: 0.3 }, 0)
        .to(bg, { opacity: 0, duration: 0.8, ease: 'power2.inOut' }, 0.1);
      if (target.visible) tl.to(f.el, { x: target.x, y: target.y, width: target.width, height: target.height, duration: 1, ease: 'expo.inOut' }, 0);
      else tl.to(f.el, { autoAlpha: 0, scale: 0.94, duration: 0.6, ease: 'power2.inOut' }, 0);
    }

    triggers.forEach(function (btn, i) {
      btn.addEventListener('click', function (e) { e.preventDefault(); open(i); });
    });
    closeBtn.addEventListener('click', close);
    prevBtns.forEach(function (b) { b.addEventListener('click', function () { if (!swiped) go(-1); }); });
    nextBtns.forEach(function (b) { b.addEventListener('click', function () { if (!swiped) go(1); }); });

    document.addEventListener('keydown', function (e) {
      if (!isOpen) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') go(1);
      else if (e.key === 'ArrowLeft') go(-1);
      else if (e.key === 'Tab') {
        var f = $$('button', lb).filter(function (b) { return b.offsetParent !== null; });
        var idx = f.indexOf(document.activeElement);
        e.preventDefault();
        var nextIdx = e.shiftKey ? (idx <= 0 ? f.length - 1 : idx - 1) : (idx + 1) % f.length;
        f[nextIdx].focus();
      }
    });

    var sx = 0, sy = 0, swiped = false;
    lb.addEventListener('pointerdown', function (e) { sx = e.clientX; sy = e.clientY; swiped = false; });
    lb.addEventListener('pointerup', function (e) {
      var ddx = e.clientX - sx, ddy = e.clientY - sy;
      if (Math.abs(ddx) > 50 && Math.abs(ddx) > Math.abs(ddy)) {
        swiped = true;
        go(ddx < 0 ? 1 : -1);
        setTimeout(function () { swiped = false; }, 60);
      }
    });

    window.addEventListener('resize', function () {
      if (!isOpen || busy) return;
      var to = fit(items[index]);
      gsap.set(frames[cur].el, { x: to.x, y: to.y, width: to.width, height: to.height });
    });
  }

  /* ------------------------------------------------------------------------
     SERVICES — interactive panels (hover/focus opens, tap on mobile)
     ------------------------------------------------------------------------ */
  var panels = $$('.panel');
  var mqDesk = window.matchMedia('(min-width: 901px)');
  function activatePanel(p) {
    panels.forEach(function (x) {
      var on = x === p;
      x.classList.toggle('is-active', on);
      var t = $('.panel__toggle', x);
      if (t) t.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    if (!mqDesk.matches) setTimeout(function () { ScrollTrigger.refresh(); }, 50);
  }
  function activatePanelById(id) {
    var p = panels.filter(function (x) { return x.id === id; })[0];
    if (p) activatePanel(p);
  }
  function initPanels() {
    if (!panels.length) return;
    panels.forEach(function (p) {
      var t = $('.panel__toggle', p);
      p.addEventListener('pointerenter', function (e) {
        if (e.pointerType === 'mouse' && mqDesk.matches) activatePanel(p);
      });
      t.addEventListener('click', function () {
        if (!mqDesk.matches && p.classList.contains('is-active')) {
          p.classList.remove('is-active');
          t.setAttribute('aria-expanded', 'false');
          setTimeout(function () { ScrollTrigger.refresh(); }, 50);
        } else {
          activatePanel(p);
        }
      });
      t.addEventListener('focus', function () { if (mqDesk.matches) activatePanel(p); });
    });
    if (location.hash) activatePanelById(location.hash.slice(1));
  }

  function initExpand() {
    var media = $('.expand__media');
    if (!media || REDUCED) return;
    var img = $('img', media);
    mm.add({ desktop: '(min-width: 701px)', mobile: '(max-width: 700px)' }, function (ctx) {
      var st = { trigger: media, start: 'top 95%', end: 'bottom bottom', scrub: true };
      gsap.fromTo(media, { clipPath: ctx.conditions.mobile ? 'inset(6% 8% 6% 8% round 16px)' : 'inset(10% 24% 10% 24% round 24px)' },
        { clipPath: 'inset(0% 0% 0% 0% round 18px)', ease: 'none', scrollTrigger: st });
      gsap.fromTo(img, { scale: 1.3 }, { scale: 1, ease: 'none', scrollTrigger: st });
    });
  }

  function initProcess() {
    var cards = $$('.process__card');
    if (cards.length < 2 || REDUCED) return;
    mm.add('(min-width: 701px)', function () {
      cards.forEach(function (card, i) {
        if (i === cards.length - 1) return;
        gsap.to(card, {
          scale: 0.92, ease: 'none',
          scrollTrigger: { trigger: cards[i + 1], start: 'top bottom', end: 'top 25%', scrub: true }
        });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Footer wordmark rises as the footer enters
     ------------------------------------------------------------------------ */
  function initFooter() {
    var mark = $('.footer__mark span');
    if (!mark || REDUCED) return;
    var split = SplitText.create(mark, { type: 'chars' });
    gsap.from(split.chars, {
      yPercent: 105, ease: 'power2.out', stagger: 0.04,
      scrollTrigger: { trigger: '.footer', start: 'top 85%', end: 'bottom bottom', scrub: 1 }
    });
  }

  /* ------------------------------------------------------------------------
     Menu fallback when GSAP is unavailable
     ------------------------------------------------------------------------ */
  function initBasicMenu() {
    var m = $('#menu'), b = $('.menu-btn');
    if (!m || !b) return;
    b.addEventListener('click', function () {
      var open = !m.classList.contains('is-open');
      m.classList.toggle('is-open', open);
      m.inert = !open;
      html.classList.toggle('menu-open', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ------------------------------------------------------------------------
     CONTACT — booking form composes a WhatsApp / e-mail message
     ------------------------------------------------------------------------ */
  function initForm() {
    var form = document.getElementById('booking');
    if (!form) return;
    var f = form.elements;
    var q = new URLSearchParams(location.search).get('hizmet');
    if (q && f.service) {
      for (var i = 0; i < f.service.options.length; i++) {
        if (f.service.options[i].value === q) { f.service.selectedIndex = i; break; }
      }
    }
    if (f.date) f.date.min = new Date().toISOString().slice(0, 10);

    var rules = [
      ['name', function (v) { return v.trim().length >= 2; }, 'Lütfen adını ve soyadını yaz.'],
      ['date', function (v) { return !!v; }, 'Lütfen etkinlik tarihini seç.'],
      ['service', function (v) { return !!v; }, 'Lütfen bir hizmet seç.']
    ];
    function validate() {
      var firstBad = null;
      rules.forEach(function (r) {
        var el = f[r[0]];
        var field = el.closest('.field');
        var err = field.querySelector('.field__error');
        var ok = r[1](el.value);
        field.classList.toggle('is-invalid', !ok);
        el.setAttribute('aria-invalid', ok ? 'false' : 'true');
        err.textContent = ok ? '' : r[2];
        if (!ok && !firstBad) firstBad = el;
      });
      if (firstBad) firstBad.focus();
      return !firstBad;
    }
    function message() {
      var date = f.date.value ? new Date(f.date.value + 'T12:00:00').toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) : '';
      var lines = [
        'Merhaba,',
        f.service.options[f.service.selectedIndex].text + ' için randevu almak istiyorum.',
        '',
        'Ad Soyad: ' + f.name.value.trim(),
        'Tarih: ' + date
      ];
      if (f.phone.value.trim()) lines.push('Telefon: ' + f.phone.value.trim());
      if (f.location.value.trim()) lines.push('Lokasyon: ' + f.location.value.trim());
      if (f.note.value.trim()) lines.push('Not: ' + f.note.value.trim());
      return lines.join('\n');
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) return;
      var via = e.submitter && e.submitter.value;
      var text = encodeURIComponent(message());
      if (via === 'mail') {
        location.href = 'mailto:' + form.getAttribute('data-email') + '?subject=' + encodeURIComponent('Randevu talebi') + '&body=' + text;
      } else {
        window.open('https://wa.me/' + form.getAttribute('data-whatsapp') + '?text=' + text, '_blank', 'noopener');
      }
    });
    rules.forEach(function (r) {
      f[r[0]].addEventListener('input', function () {
        var field = this.closest('.field');
        if (field.classList.contains('is-invalid') && r[1](this.value)) {
          field.classList.remove('is-invalid');
          this.setAttribute('aria-invalid', 'false');
          field.querySelector('.field__error').textContent = '';
        }
      });
    });
  }

  /* ------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  initCursor();
  initMagnetic();
  initHero();
  initSplits();
  initManifesto();
  initBigType();
  initScrub();
  initServiceList();
  initHGallery();
  initLightbox();
  initPanels();
  initExpand();
  initProcess();
  initFooter();
  initHoverFX();

  ScrollTrigger.sort();
  ScrollTrigger.refresh();

  var begin = PAGE === 'home' && html.classList.contains('is-loading') ? runLoader() : enterPage();
  begin.then(function () {
    if (heroIntroTl) heroIntroTl.play();
    playIntros();
    if (location.hash) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) setTimeout(function () { scroll.to(target, true); }, 60);
    }
  });

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
