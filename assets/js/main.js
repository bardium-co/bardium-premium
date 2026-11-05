/* =========================================================
   BARDIUM — Interactions
   Preloader · header · reveals · scroll text · cursor ·
   magnetic buttons · counters · spotlight · contact form
   ========================================================= */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var FINE = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var FORMSPREE_ID = "mdeozzlw"; // https://formspree.io/f/mdeozzlw

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- Preloader ---------- */
  var pre = $(".preloader");
  function reveal() { document.body.classList.add("is-ready"); kickReveals(); }
  if (pre) {
    if (store("bd_seen") || REDUCED) {
      pre.classList.add("is-quick");
      setTimeout(reveal, 60);
    } else {
      store("bd_seen", "1");
      var done = false;
      var finish = function () {
        if (done) return; done = true;
        pre.classList.add("is-done");
        setTimeout(reveal, 250);
        setTimeout(function () { pre.style.display = "none"; }, 1200);
      };
      if (document.readyState === "complete") setTimeout(finish, 1600);
      else window.addEventListener("load", function () { setTimeout(finish, 1100); });
      setTimeout(finish, 3200); // never block longer than this
    }
  } else { reveal(); }

  /* ---------- Page transitions ---------- */
  var fader = $(".page-fade");
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a || !fader || REDUCED) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || a.target === "_blank" || a.hasAttribute("download") || /^(mailto:|tel:|https?:)/i.test(href) || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var norm = function (x) { return x.replace(/\/index\.html$/, "/").replace(/\.html$/, ""); };
    if (href.indexOf("#") > 0 && norm(a.pathname) === norm(location.pathname)) return;
    e.preventDefault();
    fader.classList.add("is-active");
    setTimeout(function () { location.href = a.href; }, 380);
  });
  window.addEventListener("pageshow", function (e) { if (fader) fader.classList.remove("is-active"); if (e.persisted) reveal(); });

  /* ---------- Header behaviour ---------- */
  var header = $(".header");
  var lastY = window.scrollY, ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("is-scrolled", y > 30);
      var megaOpen = header.querySelector(".nav__item--mega:hover");
      if (y > lastY && y > 400 && !megaOpen) header.classList.add("is-hidden");
      else if (y < lastY - 4 || y < 400) header.classList.remove("is-hidden");
    }
    lastY = y;
    scrub();
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });

  // mega menu background state
  $$(".nav__item--mega").forEach(function (item) {
    item.addEventListener("mouseenter", function () { header.classList.add("mega-open"); });
    item.addEventListener("mouseleave", function () { header.classList.remove("mega-open"); });
    item.addEventListener("focusin", function () { header.classList.add("mega-open"); });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) header.classList.remove("mega-open"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.activeElement && document.activeElement.closest(".nav__item--mega")) document.activeElement.blur();
  });

  /* ---------- Active nav ---------- */
  var page = document.body.getAttribute("data-page");
  $$("[data-nav]").forEach(function (a) { if (a.getAttribute("data-nav") === page) { a.classList.add("is-active"); a.setAttribute("aria-current", "page"); } });

  /* ---------- Split text into lines (by <br> / data-split) ---------- */
  $$("[data-split]").forEach(function (el) {
    var parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map(function (p, i) {
      return '<span class="split-line"><span>' + p.trim() + "</span></span>";
    }).join("");
    $$(".split-line > span", el).forEach(function (s, i) { s.style.transitionDelay = (i * 0.09 + (parseFloat(el.getAttribute("data-delay")) || 0)) + "s"; });
  });

  /* ---------- Reveal on scroll ---------- */
  var revealIO;
  function kickReveals() {
    var els = $$("[data-reveal],[data-split],.svc");
    if (!("IntersectionObserver" in window) || REDUCED) { els.forEach(function (el) { el.classList.add("is-in"); }); return; }
    if (revealIO) return;
    revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var el = en.target, d = parseFloat(el.getAttribute("data-delay")) || 0;
          if (el.hasAttribute("data-reveal")) el.style.transitionDelay = d + "s";
          el.classList.add("is-in");
          revealIO.unobserve(el);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    els.forEach(function (el) { revealIO.observe(el); });
  }

  /* ---------- Scroll-scrubbed manifesto text ---------- */
  var scrubEls = $$("[data-scrub]");
  scrubEls.forEach(function (el) {
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) frag.appendChild(document.createTextNode(w));
            else { var s = document.createElement("span"); s.className = "w"; s.textContent = w; frag.appendChild(s); }
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) {
          if (n.classList.contains("w-keep")) n.classList.add("w"); else walk(n);
        }
      });
    };
    walk(el);
    el.__words = $$(".w", el);
  });
  function scrub() {
    var vh = window.innerHeight;
    scrubEls.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = (vh * 0.85 - r.top) / (r.height + vh * 0.35);
      p = Math.max(0, Math.min(1, p));
      var n = Math.round(p * el.__words.length);
      el.__words.forEach(function (w, i) { w.classList.toggle("on", i < n); });
    });
  }
  scrub();

  /* ---------- Counters ---------- */
  var countIO = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target, end = parseFloat(el.getAttribute("data-count")), dec = (el.getAttribute("data-count").split(".")[1] || "").length;
      var t0 = performance.now(), dur = 1800;
      (function tick(now) {
        var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 4);
        el.textContent = (end * e).toFixed(dec);
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
      countIO.unobserve(el);
    });
  }, { threshold: 0.4 }) : null;
  $$("[data-count]").forEach(function (el) { if (countIO && !REDUCED) { el.textContent = "0"; countIO.observe(el); } });

  /* ---------- Haptics: switched off ---------- */
  function haptic() { /* haptics are switched off */ }

  /* ---------- "Secured" tooltip & AI→SI flip (tap on touch, hover on desktop) ---------- */
  $$(".hl-secure").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      var on = !el.classList.contains("is-tipped");
      $$(".hl-secure.is-tipped").forEach(function (o) { o.classList.remove("is-tipped"); });
      if (on) { el.classList.add("is-tipped"); haptic(12); clearTimeout(el.__t); el.__t = setTimeout(function () { el.classList.remove("is-tipped"); }, 2600); }
    });
  });
  $$(".ai-flip").forEach(function (el) {
    var toggle = function () { el.classList.toggle("is-flipped"); haptic([8, 30, 8]); };
    el.addEventListener("click", function (e) { e.preventDefault(); toggle(); });
    el.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); } });
    if (!FINE && "IntersectionObserver" in window) {
      var auto = null;
      new IntersectionObserver(function (en) {
        if (en[0].isIntersecting && !auto) auto = setInterval(function () { el.classList.toggle("is-flipped"); }, 2400);
        else if (!en[0].isIntersecting && auto) { clearInterval(auto); auto = null; }
      }, { threshold: 1 }).observe(el);
    }
  });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Contact form (Formspree) ---------- */
  var form = $("#contact-form");
  if (form) {
    var status = $(".form__status", form.parentNode), success = $(".form-success", form.parentNode);
    var btn = $("button[type=submit]", form);
    function setErr(name, msg) {
      var f = form.querySelector("[name='" + name + "']"); if (!f) return;
      var wrap = f.closest(".field"); wrap.classList.toggle("has-error", !!msg);
      var e = wrap.querySelector(".err"); if (e) e.textContent = msg || "";
    }
    function validate() {
      var ok = true, v = function (n) { return (form.elements[n] && form.elements[n].value || "").trim(); };
      setErr("name", ""); setErr("email", ""); setErr("message", "");
      if (v("name").length < 2) { setErr("name", "Please tell us your name."); ok = false; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v("email"))) { setErr("email", "Please enter a valid email address."); ok = false; }
      if (v("message").length < 10) { setErr("message", "A few words about your project, please (10+ characters)."); ok = false; }
      return ok;
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      if (form.elements._gotcha && form.elements._gotcha.value) return; // bot
      if (!validate()) return;
      btn.disabled = true;
      var lbl = btn.querySelectorAll(".btn__label span"); var orig = lbl[0].textContent; lbl.forEach(function (s) { s.textContent = "Sending…"; });
      var data = new FormData(form);
      fetch("https://formspree.io/f/" + FORMSPREE_ID, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("bad");
          form.style.display = "none";
          var nm = $(".js-name", success); if (nm) nm.textContent = (form.elements.name.value || "").split(" ")[0];
          success.classList.add("is-show");
          haptic([20, 60, 30]);
        })
        .catch(function () {
          status.textContent = "Something went wrong while sending. Please email us directly at info@bardium.in — we reply within 48 hours.";
          status.className = "form__status is-show is-error";
        })
        .then(function () { btn.disabled = false; lbl.forEach(function (s) { s.textContent = orig; }); });
    });
    $$("input, textarea", form).forEach(function (el) { el.addEventListener("input", function () { var w = el.closest(".field"); if (w) w.classList.remove("has-error"); }); });
  }
})();
