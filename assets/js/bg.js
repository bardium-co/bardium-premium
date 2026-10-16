/* =========================================================
   BARDIUM — Background animation engine
   10 hand-built canvas scenes. No libraries, no downloads.
   Each <canvas data-bg="name"> gets its scene automatically.
   Scenes pause when off-screen and respect reduced-motion.
   ========================================================= */
(function () {
  "use strict";

  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var TAU = Math.PI * 2;
  var LOGO_PATH = "M29.00,3.00 52.50,16.57 52.50,114.58 5.00,142.00 5.00,114.86 29.00,101.00Z M53.30,142.00 123.50,101.47 123.50,74.47 76.50,47.33 76.50,74.33 99.50,87.61 53.30,114.29Z";
  var LOGO_BOX = { x: 4, y: 2, w: 121, h: 141 };

  var IS_TOUCH = (window.matchMedia && window.matchMedia("(hover: none), (pointer: coarse)").matches) || ("ontouchstart" in window);

  /* ---------- Haptics: Android vibration + iOS (Safari 18+) switch haptic ---------- */
  var Haptics = (function () {
    var last = 0, sw = null, lbl = null;
    var canVib = typeof navigator.vibrate === "function";
    function ios() {
      if (!lbl) {
        sw = document.createElement("input"); sw.type = "checkbox"; sw.setAttribute("switch", ""); sw.id = "bd-haptic-sw";
        sw.className = "bd-haptic"; sw.tabIndex = -1; sw.setAttribute("aria-hidden", "true");
        lbl = document.createElement("label"); lbl.htmlFor = "bd-haptic-sw"; lbl.className = "bd-haptic"; lbl.setAttribute("aria-hidden", "true");
        document.body.appendChild(sw); document.body.appendChild(lbl);
      }
      lbl.click(); if (sw.blur) sw.blur();
    }
    return {
      fire: function (pattern, force) {
        if (!IS_TOUCH || REDUCED) return;
        var now = performance.now(); if (!force && now - last < 45) return; last = now;
        try { if (canVib) navigator.vibrate(pattern); else ios(); } catch (e) { /* not supported */ }
      }
    };
  })();
  window.BardiumHaptics = Haptics;

  /* ---------- Pointer (mouse + finger) ---------- */
  var pointer = { x: -9999, y: -9999, active: false, touch: false };
  var releaseT;
  window.addEventListener("pointermove", function (e) {
    pointer.x = e.clientX; pointer.y = e.clientY; pointer.active = true; pointer.touch = e.pointerType !== "mouse";
  }, { passive: true });
  function touchAt(t) { pointer.x = t.clientX; pointer.y = t.clientY; pointer.active = true; pointer.touch = true; clearTimeout(releaseT); }
  window.addEventListener("touchstart", function (e) { if (e.touches[0]) touchAt(e.touches[0]); }, { passive: true });
  window.addEventListener("touchmove", function (e) { if (e.touches[0]) touchAt(e.touches[0]); }, { passive: true });
  window.addEventListener("touchend", function () { releaseT = setTimeout(function () { pointer.active = false; pointer.touch = false; }, 900); }, { passive: true });
  document.addEventListener("pointerleave", function () { if (!pointer.touch) pointer.active = false; });
  window.addEventListener("blur", function () { pointer.active = false; });

  /* ---------- Tilt (gyroscope) on phones & tablets ---------- */
  var tilt = { x: 0, y: 0, on: false };
  function onOrient(e) {
    if (e.gamma == null || e.beta == null) return;
    var ang = (screen.orientation && screen.orientation.angle) || window.orientation || 0;
    var gx = e.gamma, by = e.beta - 40;
    if (Math.abs(ang) === 90) { gx = ang === 90 ? e.beta : -e.beta; by = (ang === 90 ? -e.gamma : e.gamma) - 30; }
    gx = Math.max(-1, Math.min(1, gx / 22)); by = Math.max(-1, Math.min(1, by / 22));
    tilt.x += (gx - tilt.x) * 0.18; tilt.y += (by - tilt.y) * 0.18; tilt.on = true;
  }
  if (IS_TOUCH && !REDUCED && "DeviceOrientationEvent" in window) {
    if (typeof DeviceOrientationEvent.requestPermission !== "function") {
      window.addEventListener("deviceorientation", onOrient);
    } else {
      var asked = false;
      document.addEventListener("click", function (e) {
        if (asked || !e.isTrusted || e.target.closest("a,button,input,textarea,select,label,.hl-secure,.ai-flip")) return;
        if (!e.target.closest("section")) return;
        asked = true;
        DeviceOrientationEvent.requestPermission().then(function (st) { if (st === "granted") window.addEventListener("deviceorientation", onOrient); }).catch(function () {});
      });
    }
  }

  /* ---------- Simplex-ish noise (compact 3D value-gradient noise) ---------- */
  var perm = new Uint8Array(512);
  (function () {
    var p = []; for (var i = 0; i < 256; i++) p[i] = i;
    var seed = 1337;
    for (i = 255; i > 0; i--) { seed = (seed * 16807) % 2147483647; var j = seed % (i + 1); var t = p[i]; p[i] = p[j]; p[j] = t; }
    for (i = 0; i < 512; i++) perm[i] = p[i & 255];
  })();
  function fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function grad(h, x, y, z) {
    var u = (h & 15) < 8 ? x : y, v = (h & 15) < 4 ? y : ((h & 15) === 12 || (h & 15) === 14) ? x : z;
    return ((h & 1) ? -u : u) + ((h & 2) ? -v : v);
  }
  function noise3(x, y, z) {
    var X = Math.floor(x) & 255, Y = Math.floor(y) & 255, Z = Math.floor(z) & 255;
    x -= Math.floor(x); y -= Math.floor(y); z -= Math.floor(z);
    var u = fade(x), v = fade(y), w = fade(z);
    var A = perm[X] + Y, AA = perm[A] + Z, AB = perm[A + 1] + Z, B = perm[X + 1] + Y, BA = perm[B] + Z, BB = perm[B + 1] + Z;
    return lerp(lerp(lerp(grad(perm[AA], x, y, z), grad(perm[BA], x - 1, y, z), u),
      lerp(grad(perm[AB], x, y - 1, z), grad(perm[BB], x - 1, y - 1, z), u), v),
      lerp(lerp(grad(perm[AA + 1], x, y, z - 1), grad(perm[BA + 1], x - 1, y, z - 1), u),
        lerp(grad(perm[AB + 1], x, y - 1, z - 1), grad(perm[BB + 1], x - 1, y - 1, z - 1), u), v), w);
  }
  function rand(a, b) { return a + Math.random() * (b - a); }

  /* ---------- Base scene ---------- */
  function Scene(canvas, opts) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.opts = opts || {};
    this.w = 0; this.h = 0; this.dpr = 1;
    this.visible = false; this.t = 0; this.last = 0; this.started = false;
    this.mx = -9999; this.my = -9999; this.hover = false; this.rect = null;
  }
  Scene.prototype.resize = function () {
    var r = this.canvas.getBoundingClientRect();
    var maxDpr = this.opts.maxDpr || 2;
    this.dpr = Math.min(window.devicePixelRatio || 1, maxDpr);
    var w = Math.max(1, Math.round(r.width)), h = Math.max(1, Math.round(r.height));
    if (w === this.w && h === this.h && this.started) return;
    this.w = w; this.h = h;
    this.canvas.width = Math.round(w * this.dpr);
    this.canvas.height = Math.round(h * this.dpr);
    this.ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    this.setup();
    this.started = true;
    if (REDUCED || !this.visible) this.frame(16);
  };
  Scene.prototype.updatePointer = function () {
    var r = this.canvas.getBoundingClientRect();
    this.rect = r;
    this.tilting = false;
    if (pointer.active && pointer.x >= r.left && pointer.x <= r.right && pointer.y >= r.top && pointer.y <= r.bottom) {
      this.mx = pointer.x - r.left; this.my = pointer.y - r.top; this.hover = true;
    } else if (tilt.on && !pointer.active) {
      // phone tilt drives a virtual "finger" inside the visible part of the scene
      var vt = Math.max(0, -r.top), vb = Math.min(r.height, window.innerHeight - r.top);
      if (vb - vt > 40) {
        this.mx = r.width / 2 + tilt.x * r.width * 0.38;
        this.my = (vt + vb) / 2 + tilt.y * (vb - vt) * 0.38;
        this.hover = true; this.tilting = true;
      } else this.hover = false;
    } else { this.hover = false; }
  };
  Scene.prototype.frame = function (dt) {
    this.updatePointer();
    this.t += dt / 1000;
    this.draw(dt / 16.67);
  };
  Scene.prototype.setup = function () {};
  Scene.prototype.draw = function () {};
  Scene.prototype.density = function () { // scale particle counts by area
    var a = this.w * this.h;
    var base = window.innerWidth < 700 ? 0.55 : 1;
    return Math.min(1.25, Math.max(0.35, a / (1440 * 820))) * base;
  };
  function inherit(Child) { Child.prototype = Object.create(Scene.prototype); Child.prototype.constructor = Child; return Child; }

  /* =========================================================
     1. LOGO PARTICLES — the Bardium mark assembled from light
     ========================================================= */
  var LogoParticles = inherit(function (c, o) { Scene.call(this, c, o); this.opts.maxDpr = 1.75; });
  LogoParticles.prototype.setup = function () {
    var w = this.w, h = this.h, mobile = w < 760 || (w < 1000 && h > w * 0.9);
    var tablet = mobile && w >= 600, short = mobile && !tablet && h < 790;
    var size = tablet ? Math.min(h * 0.34, w * 0.5, 440) : short ? Math.min(h * 0.2, w * 0.45) : mobile ? Math.min(h * 0.25, w * 0.55, 300) : Math.min(h * 0.66, w * 0.36);
    var cx = mobile ? w * 0.5 : w * 0.74;
    var cy = tablet ? h * 0.26 : short ? h * 0.175 : mobile ? h * 0.215 : h * 0.5;
    var scale = size / LOGO_BOX.h;
    var lw = LOGO_BOX.w * scale, lh = LOGO_BOX.h * scale;
    var ox = cx - lw / 2, oy = cy - lh / 2;
    this.center = { x: cx, y: cy, r: size * 0.75 };

    var off = document.createElement("canvas");
    off.width = Math.ceil(w); off.height = Math.ceil(h);
    var o = off.getContext("2d");
    o.setTransform(scale, 0, 0, scale, ox - LOGO_BOX.x * scale, oy - LOGO_BOX.y * scale);
    o.fillStyle = "#fff";
    o.fill(new Path2D(LOGO_PATH));
    var data = o.getImageData(0, 0, off.width, off.height).data;

    var target = Math.round((mobile ? 1500 : 2600) * Math.min(1.2, size / 520 + 0.35));
    var area = 0, step0 = 2;
    for (var yy = 0; yy < off.height; yy += step0) for (var xx = 0; xx < off.width; xx += step0) if (data[(yy * off.width + xx) * 4 + 3] > 128) area++;
    area *= step0 * step0;
    var gap = Math.max(2.2, Math.sqrt(area / target));
    var pts = [];
    for (var y = 0; y < off.height; y += gap) {
      for (var x = 0; x < off.width; x += gap) {
        var jx = x + rand(-gap * .35, gap * .35), jy = y + rand(-gap * .35, gap * .35);
        var ix = Math.round(jx), iy = Math.round(jy);
        if (ix < 0 || iy < 0 || ix >= off.width || iy >= off.height) continue;
        if (data[(iy * off.width + ix) * 4 + 3] > 128) pts.push([jx, jy]);
      }
    }
    var prev = this.parts;
    this.parts = pts.map(function (p, i) {
      var ang = rand(0, TAU), dist = rand(w * .3, w * .9);
      var old = prev && prev[i];
      return {
        x: old ? old.x : cx + Math.cos(ang) * dist, y: old ? old.y : cy + Math.sin(ang) * dist,
        vx: 0, vy: 0, tx: p[0], ty: p[1], z: rand(.35, 1), s: rand(.7, 1.7), ph: rand(0, TAU)
      };
    });
    // ambient star dust
    var n = Math.round(160 * this.density());
    this.dust = [];
    for (var k = 0; k < n; k++) this.dust.push({ x: rand(0, w), y: rand(0, h), z: rand(.2, 1), ph: rand(0, TAU) });
    this.burst = 0;
    var self = this;
    if (!this.bound) {
      this.bound = true;
    }
    if (REDUCED) this.parts.forEach(function (p) { p.x = p.tx; p.y = p.ty; });
  };
  LogoParticles.prototype.burst = function (x, y) {
    this.parts.forEach(function (p) {
      var dx = p.x - x, dy = p.y - y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      var f = (30 * Math.exp(-d / 240) + 4) * p.z;
      p.vx += dx / d * f; p.vy += dy / d * f;
    });
  };
  LogoParticles.prototype.explode = function () {
    var c = this.center;
    this.parts.forEach(function (p) {
      var dx = p.x - c.x, dy = p.y - c.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      var f = rand(8, 22) * p.z;
      p.vx += dx / d * f; p.vy += dy / d * f;
    });
  };
  LogoParticles.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    k = Math.min(k, 2.5);

    // dust
    for (var i = 0; i < this.dust.length; i++) {
      var d = this.dust[i];
      d.y -= 0.08 * d.z * k; d.x += Math.sin(t * .3 + d.ph) * 0.05 * k;
      if (d.y < -4) { d.y = h + 4; d.x = rand(0, w); }
      ctx.globalAlpha = (0.15 + 0.35 * d.z) * (0.6 + 0.4 * Math.sin(t * 1.5 + d.ph));
      ctx.fillStyle = "#fff";
      ctx.fillRect(d.x, d.y, d.z * 1.4, d.z * 1.4);
    }

    // auto pulse every ~9s
    if (!REDUCED && Math.floor(t / 9) !== this.lastPulse) { this.lastPulse = Math.floor(t / 9); if (t > 4) this.explode(); }

    var mx = this.mx, my = this.my, hover = this.hover, R = pointer.touch ? 130 : 110, R2 = R * R, touched = 0;
    var band = ((t * 0.35) % 2.2 - 0.6); // shimmer sweep
    var c = this.center;
    for (var j = 0; j < this.parts.length; j++) {
      var p = this.parts[j];
      var nx = noise3(p.tx * .006, p.ty * .006, t * .25) * 6;
      var ny = noise3(p.tx * .006 + 40, p.ty * .006, t * .25) * 6;
      var tx = p.tx + nx * p.z, ty = p.ty + ny * p.z;
      var ax = (tx - p.x) * 0.018, ay = (ty - p.y) * 0.018;
      if (hover) {
        var dx = p.x - mx, dy = p.y - my, dd = dx * dx + dy * dy;
        if (dd < R2) { var f = (1 - dd / R2) * (this.tilting ? 1.6 : 3.2); var dl = Math.sqrt(dd) || 1; ax += dx / dl * f; ay += dy / dl * f; touched++; }
      }
      p.vx = (p.vx + ax * k) * Math.pow(0.9, k);
      p.vy = (p.vy + ay * k) * Math.pow(0.9, k);
      p.x += p.vx * k; p.y += p.vy * k;

      var rel = ((p.tx - c.x) + (p.ty - c.y) * 0.6) / (c.r * 2) + 0.5;
      var shine = Math.max(0, 1 - Math.abs(rel - band) * 6);
      var a = (0.35 + 0.55 * p.z) * (0.75 + 0.25 * Math.sin(t * 2 + p.ph)) + shine * 0.5;
      ctx.globalAlpha = Math.min(1, a);
      var s = p.s * (0.8 + p.z * 0.6) + shine * 0.8;
      ctx.fillRect(p.x - s / 2, p.y - s / 2, s, s);
    }
    ctx.globalAlpha = 1;
    // "touching sand" haptic ticks while a finger drags through the logo
    if (pointer.touch && hover && !this.tilting && touched > 30 && performance.now() - (this.lastTick || 0) > 95) {
      this.lastTick = performance.now(); Haptics.fire(Math.min(14, 4 + touched / 40));
    }
  };

  /* =========================================================
     2. DOT WAVE — a 3D ocean of points
     ========================================================= */
  var DotWave = inherit(function (c, o) { Scene.call(this, c, o); });
  DotWave.prototype.setup = function () {
    var d = this.density();
    this.cols = Math.round(64 * Math.sqrt(d) + 10);
    this.rows = Math.round(34 * Math.sqrt(d) + 6);
    this.rips = this.rips || [];
  };
  DotWave.prototype.burst = function (x, y) { this.rips.push({ x: x, y: y, t: this.t }); };
  DotWave.prototype.draw = function () {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "#fff";
    var cols = this.cols, rows = this.rows;
    var fov = 340, camY = this.opts.cam || 170, horizon = h * (this.opts.horizon || 0.42);
    var spreadX = w * 1.5, depth = 1400;
    var mxn = this.hover ? (this.mx / w - 0.5) : 0;
    for (var qq = this.rips.length - 1; qq >= 0; qq--) if (t - this.rips[qq].t > 2.6) this.rips.splice(qq, 1);
    for (var r = 0; r < rows; r++) {
      var z = (r / (rows - 1)) * depth + 40;
      var scale = fov / (fov + z);
      for (var c = 0; c < cols; c++) {
        var xw = (c / (cols - 1) - 0.5) * spreadX * 2;
        var y = Math.sin(xw * 0.0045 + t * 0.9) * 38 + Math.cos(z * 0.006 - t * 0.7) * 44 + noise3(xw * .0015, z * .0015, t * .2) * 70;
        if (this.hover || this.rips.length) {
          var sx0 = w / 2 + xw * scale, sy0 = horizon + (camY - y) * scale;
          if (this.hover) {
            var dx = sx0 - this.mx, dy = sy0 - this.my, dd = Math.sqrt(dx * dx + dy * dy);
            y += Math.max(0, 1 - dd / 220) * 60 * Math.sin(dd * 0.05 - t * 6);
          }
          for (var q = 0; q < this.rips.length; q++) {
            var rp = this.rips[q], age = t - rp.t, ex = sx0 - rp.x, ey = sy0 - rp.y, ed = Math.sqrt(ex * ex + ey * ey);
            var front = age * 420, band = Math.max(0, 1 - Math.abs(ed - front) / 110);
            y += band * 120 * (1 - age / 2.6) * Math.sin(ed * 0.04 - age * 9);
          }
        }
        var sx = w / 2 + (xw + mxn * 200 * (1 - scale)) * scale;
        var sy = horizon + (camY - y) * scale;
        if (sx < -10 || sx > w + 10 || sy < -10 || sy > h + 10) continue;
        var a = Math.pow(scale, 1.1) * 1.9;
        ctx.globalAlpha = Math.min(0.95, a) * (r === 0 ? 0.6 : 1);
        var s = Math.max(0.6, scale * 3.4);
        ctx.fillRect(sx, sy, s, s);
      }
    }
    ctx.globalAlpha = 1;
  };

  /* =========================================================
     3. DOT SPHERE — breathing planet with orbit ring
     ========================================================= */
  var DotSphere = inherit(function (c, o) { Scene.call(this, c, o); });
  DotSphere.prototype.setup = function () {
    var n = Math.round((this.opts.count || 1100) * Math.max(0.6, Math.min(1, this.density() * 1.4)));
    this.pts = [];
    var g = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < n; i++) {
      var y = 1 - (i / (n - 1)) * 2, r = Math.sqrt(1 - y * y), th = g * i;
      this.pts.push([Math.cos(th) * r, y, Math.sin(th) * r]);
    }
    this.ring = [];
    for (var k = 0; k < 3; k++) for (var m = 0; m < 110; m++) this.ring.push([m / 110 * TAU + k * 0.02, 1.42 + k * 0.07, 0]);
    this.rx = 0.35; this.ry = 0; this.spin = 0; this.pulse = 0;
  };
  DotSphere.prototype.burst = function () { this.spin += 0.22; this.pulse = 1; };
  DotSphere.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    var cx = w * (this.opts.cx || 0.5), cy = h * (this.opts.cy || 0.5);
    var R = Math.min(w, h) * (this.opts.r || 0.32);
    var trx = 0.35 + (this.hover ? (this.my / h - 0.5) * 0.8 : 0);
    this.rx += (trx - this.rx) * 0.05;
    this.ry += 0.0035 * k + (this.hover ? (this.mx / w - 0.5) * 0.02 : 0) + this.spin * k;
    this.spin *= Math.pow(0.95, k); this.pulse *= Math.pow(0.94, k);
    R *= 1 + this.pulse * 0.12 * Math.sin(this.pulse * 12);
    var cX = Math.cos(this.rx), sX = Math.sin(this.rx), cY = Math.cos(this.ry), sY = Math.sin(this.ry);
    ctx.fillStyle = "#fff";
    for (var i = 0; i < this.pts.length; i++) {
      var p = this.pts[i];
      var m = 1 + 0.07 * Math.sin(p[1] * 6 + t * 1.4) * Math.cos(Math.atan2(p[2], p[0]) * 3 + t * 0.8);
      var x = p[0] * m, y = p[1] * m, z = p[2] * m;
      var x1 = x * cY - z * sY, z1 = x * sY + z * cY;
      var y1 = y * cX - z1 * sX, z2 = y * sX + z1 * cX;
      var persp = 2.4 / (2.4 + z2);
      var sx = cx + x1 * R * persp, sy = cy + y1 * R * persp;
      var front = (1 - z2) / 2;
      ctx.globalAlpha = 0.08 + front * 0.85;
      var s = 0.6 + front * 1.9;
      ctx.fillRect(sx - s / 2, sy - s / 2, s, s);
    }
    // orbit ring (tilted)
    var tilt = 1.15;
    for (var j = 0; j < this.ring.length; j++) {
      var q = this.ring[j];
      var a = q[0] + t * 0.25;
      var rx = Math.cos(a) * q[1], rz = Math.sin(a) * q[1], ry = q[2];
      var y2 = ry * Math.cos(tilt) - rz * Math.sin(tilt), z3 = ry * Math.sin(tilt) + rz * Math.cos(tilt);
      var x2 = rx * Math.cos(0.4) - y2 * Math.sin(0.4), y3 = rx * Math.sin(0.4) + y2 * Math.cos(0.4);
      var pp = 2.4 / (2.4 + z3 * 0.6);
      var ff = (1 - z3 / 1.75) / 2;
      ctx.globalAlpha = 0.1 + ff * 0.6;
      var ss = 0.6 + ff * 1.4;
      ctx.fillRect(cx + x2 * R * pp - ss / 2, cy + y3 * R * pp - ss / 2, ss, ss);
    }
    ctx.globalAlpha = 1;
  };

  /* =========================================================
     4. NETWORK — secure nodes with radar pulses
     ========================================================= */
  var Network = inherit(function (c, o) { Scene.call(this, c, o); });
  Network.prototype.setup = function () {
    var n = Math.round(95 * this.density() + 20);
    this.nodes = [];
    for (var i = 0; i < n; i++) this.nodes.push({ x: rand(0, this.w), y: rand(0, this.h), vx: rand(-.25, .25), vy: rand(-.25, .25), r: rand(1, 2.2), glow: 0 });
    this.pulses = []; this.nextPulse = 0;
  };
  Network.prototype.burst = function (x, y) {
    this.pulses.push({ r: 0, x: x, y: y, strong: 1 });
    this.nodes.forEach(function (a) { var dx = a.x - x, dy = a.y - y, d = Math.sqrt(dx * dx + dy * dy) || 1; if (d < 220) { a.vx += dx / d * 1.6; a.vy += dy / d * 1.6; a.glow = 1; } });
  };
  Network.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    var cx = w * (this.opts.cx || 0.72), cy = h * (this.opts.cy || 0.48);
    if (w < 760) { cx = w * 0.5; cy = h * 0.3; }
    if (t > this.nextPulse) { this.pulses.push({ r: 0 }); this.nextPulse = t + 2.4; }
    var maxR = Math.max(w, h) * 0.9;
    // shield hexagon
    var hs = Math.min(w, h) * (w < 760 ? 0.17 : 0.2);
    ctx.save(); ctx.translate(cx, cy);
    for (var ring = 0; ring < 3; ring++) {
      var sz = hs * (1 + ring * 0.42), rot = t * (ring % 2 ? -0.12 : 0.08) + ring * 0.3;
      ctx.beginPath();
      for (var v = 0; v <= 6; v++) { var an = rot + v * TAU / 6; var px = Math.cos(an) * sz, py = Math.sin(an) * sz; v ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
      ctx.strokeStyle = "rgba(255,255,255," + (0.5 - ring * 0.14) + ")";
      ctx.lineWidth = 1;
      if (ring === 1) ctx.setLineDash([4, 8]); else ctx.setLineDash([]);
      ctx.stroke();
    }
    ctx.setLineDash([]);
    // lock glyph
    var L = hs * 0.32;
    ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.lineWidth = 1.5;
    ctx.strokeRect(-L * 0.6, -L * 0.1, L * 1.2, L * 0.95);
    ctx.beginPath(); ctx.arc(0, -L * 0.1, L * 0.38, Math.PI, 0); ctx.stroke();
    ctx.beginPath(); ctx.arc(0, L * 0.3, L * 0.09, 0, TAU); ctx.fillStyle = "#fff"; ctx.fill();
    // sweep
    var sweep = t * 0.9;
    var grd = ctx.createRadialGradient(0, 0, 0, 0, 0, hs * 2.6);
    grd.addColorStop(0, "rgba(255,255,255,.16)"); grd.addColorStop(1, "rgba(255,255,255,0)");
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.arc(0, 0, hs * 2.6, sweep, sweep + 0.5); ctx.closePath();
    ctx.fillStyle = grd; ctx.fill();
    ctx.restore();

    // pulses
    for (var p = this.pulses.length - 1; p >= 0; p--) {
      var pu = this.pulses[p]; pu.r += 2.6 * k;
      if (pu.r > maxR) { this.pulses.splice(p, 1); continue; }
      ctx.beginPath(); ctx.arc(pu.x != null ? pu.x : cx, pu.y != null ? pu.y : cy, pu.r, 0, TAU);
      ctx.strokeStyle = "rgba(255,255,255," + ((pu.strong ? 0.5 : 0.22) * (1 - pu.r / maxR)) + ")"; ctx.lineWidth = pu.strong ? 1.5 : 1; ctx.stroke();
    }
    // nodes
    var nodes = this.nodes, D = w < 760 ? 110 : 150, D2 = D * D;
    for (var i = 0; i < nodes.length; i++) {
      var a = nodes[i];
      a.x += a.vx * k; a.y += a.vy * k;
      if (a.x < 0 || a.x > w) a.vx *= -1;
      if (a.y < 0 || a.y > h) a.vy *= -1;
      if (this.hover) { var mdx = a.x - this.mx, mdy = a.y - this.my; var md = mdx * mdx + mdy * mdy; if (md < 16000) { a.x += mdx * 0.01; a.y += mdy * 0.01; a.glow = 1; } }
      var dcx = a.x - cx, dcy = a.y - cy, dc = Math.sqrt(dcx * dcx + dcy * dcy);
      for (var q = 0; q < this.pulses.length; q++) {
        var pq = this.pulses[q], dpc = pq.x != null ? Math.sqrt((a.x - pq.x) * (a.x - pq.x) + (a.y - pq.y) * (a.y - pq.y)) : dc;
        if (Math.abs(dpc - pq.r) < 6) a.glow = 1;
      }
      a.glow *= Math.pow(0.96, k);
      var sp = Math.sqrt(a.vx * a.vx + a.vy * a.vy); if (sp > 0.4) { a.vx *= 0.97; a.vy *= 0.97; }
    }
    ctx.lineWidth = 0.7;
    for (i = 0; i < nodes.length; i++) {
      for (var j = i + 1; j < nodes.length; j++) {
        var b = nodes[j], dx = nodes[i].x - b.x, dy = nodes[i].y - b.y, dd = dx * dx + dy * dy;
        if (dd < D2) {
          ctx.strokeStyle = "rgba(255,255,255," + ((1 - dd / D2) * (0.14 + Math.max(nodes[i].glow, b.glow) * 0.4)) + ")";
          ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
    }
    if (this.hover) {
      for (i = 0; i < nodes.length; i++) {
        var nx = nodes[i].x - this.mx, ny = nodes[i].y - this.my, nd = nx * nx + ny * ny;
        if (nd < D2 * 1.4) { ctx.strokeStyle = "rgba(255,255,255," + (0.35 * (1 - nd / (D2 * 1.4))) + ")"; ctx.beginPath(); ctx.moveTo(this.mx, this.my); ctx.lineTo(nodes[i].x, nodes[i].y); ctx.stroke(); }
      }
    }
    ctx.fillStyle = "#fff";
    for (i = 0; i < nodes.length; i++) {
      var nn = nodes[i];
      ctx.globalAlpha = 0.45 + nn.glow * 0.55;
      ctx.beginPath(); ctx.arc(nn.x, nn.y, nn.r + nn.glow * 1.5, 0, TAU); ctx.fill();
    }
    ctx.globalAlpha = 1;
  };

  /* =========================================================
     5. HEX SCAN — security lattice lit by a rotating beam
     ========================================================= */
  var HexScan = inherit(function (c, o) { Scene.call(this, c, o); });
  HexScan.prototype.setup = function () {
    var size = this.w < 760 ? 26 : 34;
    this.size = size;
    var hw = Math.sqrt(3) * size, vh = 1.5 * size;
    this.cells = [];
    for (var row = -1; row * vh < this.h + size * 2; row++) {
      for (var col = -1; col * hw < this.w + hw; col++) {
        var x = col * hw + (row % 2 ? hw / 2 : 0), y = row * vh;
        this.cells.push({ x: x, y: y, e: 0, r: Math.random() });
      }
    }
    this.rings = [];
  };
  HexScan.prototype.burst = function (x, y) { this.rings.push({ x: x, y: y, r: 0 }); };
  HexScan.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t, s = this.size;
    ctx.clearRect(0, 0, w, h);
    var cx = w * 0.5, cy = h * 0.5;
    var ang = (t * 0.55) % TAU;
    for (var rr = this.rings.length - 1; rr >= 0; rr--) { this.rings[rr].r += 7 * k; if (this.rings[rr].r > Math.max(w, h) * 1.2) this.rings.splice(rr, 1); }
    var maxD = Math.sqrt(cx * cx + cy * cy);
    for (var i = 0; i < this.cells.length; i++) {
      var c = this.cells[i];
      var a = Math.atan2(c.y - cy, c.x - cx); if (a < 0) a += TAU;
      var diff = (ang - a + TAU) % TAU;
      if (diff < 0.12) c.e = 1;
      if (this.hover) { var dx = c.x - this.mx, dy = c.y - this.my; if (dx * dx + dy * dy < 9000) c.e = Math.max(c.e, 0.9); }
      if (c.r > 0.985 && Math.random() < 0.004) c.e = 1;
      for (var g = 0; g < this.rings.length; g++) { var rg = this.rings[g], rdx = c.x - rg.x, rdy = c.y - rg.y; if (Math.abs(Math.sqrt(rdx * rdx + rdy * rdy) - rg.r) < s) c.e = 1; }
      c.e *= Math.pow(0.975, k);
      var dist = Math.sqrt((c.x - cx) * (c.x - cx) + (c.y - cy) * (c.y - cy)) / maxD;
      var base = 0.05 + (1 - dist) * 0.06;
      var alpha = base + c.e * 0.55;
      ctx.beginPath();
      for (var v = 0; v < 6; v++) { var an = Math.PI / 6 + v * TAU / 6; var px = c.x + Math.cos(an) * (s - 2), py = c.y + Math.sin(an) * (s - 2); v ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
      ctx.closePath();
      ctx.strokeStyle = "rgba(255,255,255," + alpha + ")"; ctx.lineWidth = 1; ctx.stroke();
      if (c.e > 0.25) { ctx.fillStyle = "rgba(255,255,255," + (c.e * 0.09) + ")"; ctx.fill(); }
    }
    // beam
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang);
    var g = ctx.createLinearGradient(0, 0, maxD, 0);
    g.addColorStop(0, "rgba(255,255,255,.5)"); g.addColorStop(1, "rgba(255,255,255,0)");
    ctx.strokeStyle = g; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(maxD, 0); ctx.stroke();
    ctx.restore();
  };

  /* =========================================================
     6. FLOW FIELD — silk threads drawn by noise
     ========================================================= */
  var FlowField = inherit(function (c, o) { Scene.call(this, c, o); this.opts.maxDpr = 1.5; });
  FlowField.prototype.setup = function () {
    var n = Math.round(700 * this.density() + 120);
    this.ps = [];
    for (var i = 0; i < n; i++) this.ps.push({ x: rand(0, this.w), y: rand(0, this.h), life: rand(50, 300), a: rand(.15, .55) });
    this.ctx.fillStyle = "#000"; this.ctx.fillRect(0, 0, this.w, this.h);
  };
  FlowField.prototype.burst = function (x, y) {
    this.swirl = { x: x, y: y, s: 1 };
    for (var i = 0; i < this.ps.length; i += 3) { var a = rand(0, TAU), d = rand(0, 60); this.ps[i].x = x + Math.cos(a) * d; this.ps[i].y = y + Math.sin(a) * d; this.ps[i].life = rand(60, 200); }
  };
  FlowField.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.globalAlpha = 1;
    ctx.fillStyle = "rgba(0,0,0,0.075)"; ctx.fillRect(0, 0, w, h);
    ctx.lineWidth = 0.9;
    if (this.swirl) this.swirl.s *= Math.pow(0.985, k);
    for (var i = 0; i < this.ps.length; i++) {
      var p = this.ps[i];
      var ang = noise3(p.x * 0.0022, p.y * 0.0022, t * 0.08) * TAU * 1.6;
      if (this.hover) { var dx = p.x - this.mx, dy = p.y - this.my, dd = dx * dx + dy * dy; if (dd < 30000) ang += (1 - dd / 30000) * Math.atan2(dy, dx) * 0.8; }
      if (this.swirl && this.swirl.s > 0.02) { var sx = p.x - this.swirl.x, sy = p.y - this.swirl.y, sd = Math.sqrt(sx * sx + sy * sy); if (sd < 320) ang = Math.atan2(sy, sx) + Math.PI / 2.4 * (1 - sd / 320) * this.swirl.s + ang * (1 - this.swirl.s); }
      var sp = 1.4 * k;
      var nx = p.x + Math.cos(ang) * sp, ny = p.y + Math.sin(ang) * sp;
      ctx.strokeStyle = "rgba(255,255,255," + p.a + ")";
      ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(nx, ny); ctx.stroke();
      p.x = nx; p.y = ny; p.life -= k;
      if (p.life < 0 || p.x < -5 || p.x > w + 5 || p.y < -5 || p.y > h + 5) { p.x = rand(0, w); p.y = rand(0, h); p.life = rand(80, 320); }
    }
  };

  /* =========================================================
     7. RIPPLE GRID — black ink dots on paper, rippling
     ========================================================= */
  var RippleGrid = inherit(function (c, o) { Scene.call(this, c, o); });
  RippleGrid.prototype.setup = function () {
    this.gap = this.w < 760 ? 22 : 28;
    this.ripples = []; this.nextR = 0;
  };
  RippleGrid.prototype.burst = function (x, y) { this.ripples.push({ x: x, y: y, r: 0, m: 2 }); };
  RippleGrid.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t, g = this.gap;
    ctx.clearRect(0, 0, w, h);
    if (t > this.nextR) { this.ripples.push({ x: rand(w * .1, w * .9), y: rand(h * .1, h * .9), r: 0 }); this.nextR = t + 2.2; }
    if (this.hover && (!this.lastHR || t - this.lastHR > 0.5)) { this.ripples.push({ x: this.mx, y: this.my, r: 0, m: 1 }); this.lastHR = t; }
    for (var q = this.ripples.length - 1; q >= 0; q--) { this.ripples[q].r += 3 * k; if (this.ripples[q].r > 700) this.ripples.splice(q, 1); }
    ctx.fillStyle = "#000";
    for (var y = g / 2; y < h; y += g) {
      for (var x = g / 2; x < w; x += g) {
        var s = 1.1, dx0 = 0, dy0 = 0;
        for (var i = 0; i < this.ripples.length; i++) {
          var rp = this.ripples[i], dx = x - rp.x, dy = y - rp.y, d = Math.sqrt(dx * dx + dy * dy);
          var band = 1 - Math.min(1, Math.abs(d - rp.r) / 46);
          if (band > 0) { var fall = (1 - rp.r / 700) * band * (rp.m || 1); s += fall * 2.6; if (d > 0) { dx0 += dx / d * fall * 5; dy0 += dy / d * fall * 5; } }
        }
        if (this.hover) { var mdx = x - this.mx, mdy = y - this.my, md = Math.sqrt(mdx * mdx + mdy * mdy); if (md < 140) s += (1 - md / 140) * 2.2; }
        ctx.globalAlpha = Math.min(0.85, 0.2 + (s - 1.1) * 0.22);
        ctx.beginPath(); ctx.arc(x + dx0, y + dy0, s, 0, TAU); ctx.fill();
      }
    }
    ctx.globalAlpha = 1;
  };

  /* =========================================================
     8. TUNNEL — warp through infinite frames
     ========================================================= */
  var Tunnel = inherit(function (c, o) { Scene.call(this, c, o); });
  Tunnel.prototype.setup = function () {
    this.frames = []; for (var i = 0; i < 26; i++) this.frames.push(i / 26);
    var n = Math.round(160 * this.density() + 40);
    this.stars = []; for (var j = 0; j < n; j++) this.stars.push({ a: rand(0, TAU), z: rand(0, 1), sp: rand(.4, 1) });
    this.ox = 0; this.oy = 0; this.zoff = 0; this.boost = 0;
  };
  Tunnel.prototype.burst = function () { this.boost = 1; };
  Tunnel.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    var tx = this.hover ? (this.mx - w / 2) * 0.12 : Math.sin(t * .4) * 20;
    var ty = this.hover ? (this.my - h / 2) * 0.12 : Math.cos(t * .3) * 14;
    this.ox += (tx - this.ox) * 0.05; this.oy += (ty - this.oy) * 0.05;
    var cx = w / 2 + this.ox, cy = h / 2 + this.oy;
    var maxS = Math.max(w, h) * 1.25;
    this.zoff += 0.00075 * k * (1 + this.boost * 9); this.boost *= Math.pow(0.965, k);
    for (var i = 0; i < this.frames.length; i++) {
      var z = (this.frames[i] + this.zoff) % 1;
      var e = Math.pow(z, 2.4);
      var size = 12 + e * maxS;
      var px = cx + (w / 2 - cx) * e, py = cy + (h / 2 - cy) * e;
      ctx.save(); ctx.translate(px, py); ctx.rotate(z * 0.9 + t * 0.05);
      ctx.strokeStyle = "rgba(255,255,255," + (Math.min(1, z * 1.6) * (1 - z) * 0.55) + ")";
      ctx.lineWidth = 0.6 + e * 1.4;
      var r = size * 0.18;
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(-size / 2, -size / 2 * 0.62, size, size * 0.62, r); else ctx.rect(-size / 2, -size / 2 * 0.62, size, size * 0.62);
      ctx.stroke();
      ctx.restore();
    }
    for (var j = 0; j < this.stars.length; j++) {
      var s = this.stars[j];
      s.z += 0.006 * s.sp * k * (1 + this.boost * 5); if (s.z > 1) { s.z = 0; s.a = rand(0, TAU); }
      var d0 = Math.pow(s.z, 2.2) * maxS * 0.6, d1 = Math.pow(Math.max(0, s.z - 0.04), 2.2) * maxS * 0.6;
      ctx.strokeStyle = "rgba(255,255,255," + (s.z * 0.7) + ")"; ctx.lineWidth = 0.6 + s.z;
      ctx.beginPath(); ctx.moveTo(cx + Math.cos(s.a) * d1, cy + Math.sin(s.a) * d1); ctx.lineTo(cx + Math.cos(s.a) * d0, cy + Math.sin(s.a) * d0); ctx.stroke();
    }
  };

  /* =========================================================
     9. ORBITS — gyroscope of light
     ========================================================= */
  var Orbits = inherit(function (c, o) { Scene.call(this, c, o); });
  Orbits.prototype.setup = function () {
    this.rings = [];
    for (var i = 0; i < 6; i++) this.rings.push({ tilt: rand(0.9, 1.35), rot: i * Math.PI / 6 + rand(-.1, .1), sp: rand(0.15, 0.4) * (i % 2 ? -1 : 1), r: 0.55 + i * 0.09, n: 90 });
    this.tx = 0; this.ty = 0; this.extra = 0; this.spin = 0;
  };
  Orbits.prototype.burst = function () { this.spin = 1; };
  Orbits.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    var mobile = w < 760;
    var cx = w * (mobile ? 0.5 : (this.opts.cx || 0.72)), cy = h * (mobile ? 0.32 : (this.opts.cy || 0.5));
    var R = Math.min(w, h) * (mobile ? 0.3 : 0.36);
    var gx = this.hover ? (this.mx / w - 0.5) * 0.6 : 0, gy = this.hover ? (this.my / h - 0.5) * 0.6 : 0;
    this.tx += (gx - this.tx) * 0.05; this.ty += (gy - this.ty) * 0.05;
    this.extra += 0.12 * this.spin * (k || 1); this.spin *= Math.pow(0.96, k || 1);
    // core
    var core = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.5);
    core.addColorStop(0, "rgba(255,255,255,.35)"); core.addColorStop(.3, "rgba(255,255,255,.06)"); core.addColorStop(1, "rgba(255,255,255,0)");
    ctx.fillStyle = core; ctx.beginPath(); ctx.arc(cx, cy, R * 0.5, 0, TAU); ctx.fill();
    ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(cx, cy, 3, 0, TAU); ctx.fill();
    for (var i = 0; i < this.rings.length; i++) {
      var rg = this.rings[i], rr = R * rg.r;
      var tilt = rg.tilt + this.ty, rot = rg.rot + this.tx + t * 0.05 + this.extra * (i % 2 ? -1 : 1);
      var ct = Math.cos(tilt), cr = Math.cos(rot), sr = Math.sin(rot);
      for (var j = 0; j < rg.n; j++) {
        var a = j / rg.n * TAU;
        var x = Math.cos(a) * rr, y = Math.sin(a) * rr * ct, z = Math.sin(a) * Math.sin(tilt);
        var X = x * cr - y * sr, Y = x * sr + y * cr;
        ctx.globalAlpha = 0.12 + (1 - z) * 0.18;
        ctx.fillRect(cx + X - 0.7, cy + Y - 0.7, 1.4, 1.4);
      }
      // moving bead + trail
      for (var b = 0; b < 14; b++) {
        var ab = t * rg.sp * 2 + i - b * 0.05;
        var bx = Math.cos(ab) * rr, by = Math.sin(ab) * rr * ct, bz = Math.sin(ab) * Math.sin(tilt);
        var BX = bx * cr - by * sr, BY = bx * sr + by * cr;
        ctx.globalAlpha = (1 - b / 14) * (0.5 + (1 - bz) * 0.25);
        var bs = (b === 0 ? 3.4 : 2.2) * (1 - b / 20);
        ctx.beginPath(); ctx.arc(cx + BX, cy + BY, bs, 0, TAU); ctx.fill();
      }
    }
    ctx.globalAlpha = 1;
  };

  /* =========================================================
     10. STARFIELD — quiet parallax night with shooting stars
     ========================================================= */
  var Starfield = inherit(function (c, o) { Scene.call(this, c, o); });
  Starfield.prototype.setup = function () {
    var n = Math.round(320 * this.density() + 60);
    this.stars = []; for (var i = 0; i < n; i++) this.stars.push({ x: rand(0, this.w), y: rand(0, this.h), z: rand(.1, 1), ph: rand(0, TAU) });
    this.shoot = null; this.nextShoot = 2;
    this.px = 0; this.py = 0;
  };
  Starfield.prototype.burst = function (x, y) { this.shoot = { x: x + 300, y: y - 150, l: 0 }; this.flash = 1; };
  Starfield.prototype.draw = function (k) {
    var ctx = this.ctx, w = this.w, h = this.h, t = this.t;
    ctx.clearRect(0, 0, w, h);
    var gx = this.hover ? (this.mx / w - .5) * 30 : 0, gy = this.hover ? (this.my / h - .5) * 30 : 0;
    this.px += (gx - this.px) * 0.04; this.py += (gy - this.py) * 0.04;
    ctx.fillStyle = "#fff";
    for (var i = 0; i < this.stars.length; i++) {
      var s = this.stars[i];
      s.x -= 0.05 * s.z * k; if (s.x < -2) s.x = w + 2;
      ctx.globalAlpha = Math.min(1, s.z * (0.45 + 0.55 * Math.sin(t * (1 + s.z) + s.ph)) * 0.9 + (this.flash || 0) * 0.5 * s.z);
      var sz = s.z * 1.6;
      ctx.fillRect(s.x + this.px * s.z, s.y + this.py * s.z, sz, sz);
    }
    this.flash = (this.flash || 0) * Math.pow(0.95, k);
    if (!this.shoot && t > this.nextShoot) { this.shoot = { x: rand(w * .2, w), y: rand(0, h * .4), l: 0 }; }
    if (this.shoot) {
      var sh = this.shoot; sh.l += 0.025 * k;
      var len = 140, x0 = sh.x - sh.l * 600, y0 = sh.y + sh.l * 300;
      var g = ctx.createLinearGradient(x0, y0, x0 + len, y0 - len / 2);
      g.addColorStop(0, "rgba(255,255,255,.9)"); g.addColorStop(1, "rgba(255,255,255,0)");
      ctx.globalAlpha = Math.max(0, 1 - sh.l); ctx.strokeStyle = g; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + len, y0 - len / 2); ctx.stroke();
      if (sh.l > 1) { this.shoot = null; this.nextShoot = t + rand(3, 7); }
    }
    ctx.globalAlpha = 1;
  };

  /* ---------- Registry & loop ---------- */
  var TYPES = {
    logo: LogoParticles, wave: DotWave, sphere: DotSphere, network: Network, hex: HexScan,
    flow: FlowField, ripple: RippleGrid, tunnel: Tunnel, orbits: Orbits, stars: Starfield
  };
  var scenes = [];

  function init() {
    var nodes = document.querySelectorAll("canvas[data-bg]");
    if (!nodes.length) return;
    var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var sc = en.target.__scene; if (!sc) return;
        sc.visible = en.isIntersecting;
        if (sc.visible && !sc.started) sc.resize();
      });
    }, { rootMargin: "120px 0px" }) : null;

    Array.prototype.forEach.call(nodes, function (cv) {
      var Type = TYPES[cv.getAttribute("data-bg")];
      if (!Type || !cv.getContext) return;
      var opts = {};
      ["cx", "cy", "r", "horizon", "cam", "count"].forEach(function (key) {
        var v = cv.getAttribute("data-" + key); if (v !== null) opts[key] = parseFloat(v);
      });
      var sc = new Type(cv, opts);
      cv.__scene = sc;
      scenes.push(sc);
      if (io) io.observe(cv); else { sc.visible = true; }
      sc.resize();
    });

    // Tap / click anywhere on an animated section to "play" with it
    document.addEventListener("click", function (e) {
      if (!e.isTrusted || e.target.closest("a,button,input,textarea,select,label,.hl-secure,.ai-flip,.bd-haptic,.form,.mega,.dock")) return;
      for (var i = 0; i < scenes.length; i++) {
        var sc = scenes[i]; if (!sc.visible || !sc.burst) continue;
        var r = sc.canvas.getBoundingClientRect();
        if (e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) {
          sc.burst(e.clientX - r.left, e.clientY - r.top);
          Haptics.fire([14, 40, 24], true);
          if (REDUCED) sc.frame(16);
          break;
        }
      }
    });

    var rT;
    window.addEventListener("resize", function () {
      clearTimeout(rT);
      rT = setTimeout(function () { scenes.forEach(function (s) { s.resize(); }); }, 150);
    });

    if (REDUCED) return; // static single frame only
    var last = performance.now();
    function loop(now) {
      var dt = Math.min(50, now - last); last = now;
      if (!document.hidden) {
        for (var i = 0; i < scenes.length; i++) if (scenes[i].visible && scenes[i].started) scenes[i].frame(dt);
      }
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
  window.BardiumBG = { scenes: scenes };
})();
