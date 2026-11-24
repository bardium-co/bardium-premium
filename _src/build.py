#!/usr/bin/env python3
"""Builds the static Bardium site pages from shared partials.

Edit content here, then run:  python _src/build.py
It rewrites every .html page in the repo root (header, footer and nav stay identical everywhere)."""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
LOGO = open(os.path.join(HERE, "logo-path.txt")).read().strip()
SITE = "https://bardium.in"
SLOGAN = "Built to be remembered."

# ---------------------------------------------------------------- icons
def ic(body, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'

I = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chev": '<path d="m6 9 6 6 6-6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "app": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 14h3M8 17h6"/>',
 "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM20 14v1M14 20h1M17 17h4v4h-4"/>',
 "cart": '<path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1"/><circle cx="18" cy="20" r="1"/>',
 "refresh": '<path d="M20 11a8 8 0 0 0-14.9-3M4 13a8 8 0 0 0 14.9 3"/><path d="M4 4v4h4M20 20v-4h-4"/>',
 "shield": '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.8 7.5 9 4.3-1.2 7.5-4.5 7.5-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.2"/>',
 "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
 "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
 "db": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
 "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.5 1.5A3.8 3.8 0 0 1 17.5 18z"/>',
 "backup": '<path d="M12 8v5l3 2"/><path d="M3.5 12a8.5 8.5 0 1 0 2.5-6"/><path d="M3 4v4h4"/>',
 "pulse": '<path d="M3 12h4l2-6 4 12 2-6h6"/>',
 "headers": '<path d="M4 6h16M4 12h10M4 18h7"/><circle cx="18" cy="17" r="3"/>',
 "check": '<path d="m5 12 5 5 9-10"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "home": '<path d="M4 11 12 4l8 7v8a1 1 0 0 1-1 1h-4v-6h-6v6H5a1 1 0 0 1-1-1z"/>',
 "grid": '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 "case": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 13h18"/>',
 "bolt": '<path d="M13 3 5 13h6l-1 8 8-10h-6z"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
 "wa": '<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-1.8-1.8l.8-1-1-2z"/>',
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v8h14v-8M12 8v12M12 8S10 3 7.5 4.5 9 8 12 8zm0 0s2-5 4.5-3.5S15 8 12 8z"/>',
 "doc": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "approve": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="m8 11 3 3 5-6M8 21h8"/>',
 "wrench": '<path d="M14.5 6.5a4 4 0 0 0 5 5L12 19a2.1 2.1 0 0 1-3-3z"/><path d="M14.5 6.5 17 4l3 3-2.5 2.5"/>',
 "lang": '<path d="M4 5h8M8 3v2M6 5c0 4 3 7 6 8M10 5c0 3-3 7-6 8"/><path d="m13 21 4-9 4 9M14.5 18h5"/>',
}
def icon(name, cls=""): return ic(I[name], cls)
ARROW = icon("arrow", "btn__arrow")
STAR = f'<svg class="marquee__star" viewBox="4 2 121 141" aria-hidden="true"><path fill="#fff" d="{LOGO}"/></svg>'

WA = "https://wa.me/919972782952?text=Hi%20Bardium%2C%20I%27d%20like%20to%20discuss%20a%20project."
def secure(word="secured", tip="HTTPS · Encrypted data · OWASP-aligned code"):
    return f'<span class="hl-secure" tabindex="0" data-tip="{tip}">{word}</span>'
def trust_row(cls=""):
    items = ["Free discovery call", "Fixed quote in 48h", "100% code ownership"]
    return f'<ul class="trust-row {cls}">' + "".join(f'<li>{icon("check")}{t}</li>' for t in items) + '</ul>'
SEC_CHIP = '<span class="chip chip--secure">' + icon("lock") + ' Secured by default</span>'

def btn(label, href, cls="", arrow=True, extra=""):
    a = ARROW if arrow else ""
    return f'<a class="btn {cls}" href="{href}"{extra}><span class="btn__label"><span>{label}</span><span aria-hidden="true">{label}</span></span>{a}</a>'

# ---------------------------------------------------------------- data
SERVICES = [
 ("web", "globe", "Website Design &amp; Development", "Bespoke, lightning-fast websites",
  "Bespoke, secured websites designed from a blank canvas and engineered for speed. Every pixel considered, every interaction intentional — built to turn visitors into clients.",
  ["Custom UI/UX design — no templates", "Responsive on every screen size", "SEO-ready structure &amp; Core Web Vitals", "Easy content management", "Analytics &amp; conversion tracking", "Launch, domain &amp; hosting setup"]),
 ("software", "code", "Custom Software Development", "Any software, for any business",
  "Software shaped around how your business actually works — not the other way round. Billing and POS, booking and ordering systems, inventory, CRM, ERP, HR and staff tools, automation — if your business needs it, we build it.",
  ["Built around your exact workflow", "Billing, POS &amp; inventory systems", "Booking, ordering &amp; scheduling", "CRM, ERP &amp; internal tools", "Automation of repetitive work", "Works online or offline"]),
 ("apps", "app", "Web &amp; Mobile Applications", "Apps for every screen",
  "Secured web and mobile applications that people love to use — customer apps, admin dashboards, client portals, marketplaces and SaaS platforms, built to scale as you grow.",
  ["Android, iOS &amp; web apps", "Secure login &amp; role-based access", "Real-time data &amp; notifications", "Admin dashboards &amp; reports", "Integrations with the tools you use", "Built to scale with your business"]),
 ("ecommerce", "cart", "E-Commerce", "Storefronts that sell",
  "Premium, secured online stores with seamless checkout and safe payments. From product catalogue to payment gateway to order management — designed to make buying effortless.",
  ["Product catalogue &amp; search", "Secure payment gateway integration", "Cart, checkout &amp; order tracking", "Inventory &amp; order dashboard", "WhatsApp &amp; email notifications", "Mobile-first shopping experience"]),
 ("revamp", "refresh", "Revamps &amp; Project Rescue", "Modernise or finish what was started",
  "Outdated website or an abandoned half-built project? We review everything, keep what works, rebuild what doesn't — and deliver a clean, modern, fully working product.",
  ["Full design &amp; quality audit", "Modern redesign without losing SEO", "Take over half-built projects", "Performance &amp; speed optimisation", "Bug fixing &amp; clean-up", "Clear timeline before we start"]),
 ("care", "shield", "Care, Security &amp; Maintenance", "We stay after launch",
  "We don't disappear after go-live. Security patches, updates, backups, uptime monitoring and content changes — handled quietly so you can focus on business.",
  ["Security updates &amp; patching", "Automated backups", "Uptime &amp; performance monitoring", "Content &amp; feature updates", "Priority support", "Monthly health report"]),
]
CAPABILITIES = ["Websites", "Custom software", "Mobile apps", "Web apps", "E-commerce", "Billing &amp; POS", "Booking systems", "Ordering systems", "CRM &amp; ERP", "Inventory", "Dashboards", "Client portals", "Automation", "AI integrations", "Landing pages", "Revamps"]

SECURITY = [
 ("lock", "HTTPS &amp; SSL everywhere", "Every site ships on HTTPS with modern TLS encryption and HSTS — so data between your visitors and your site can't be read or tampered with."),
 ("headers", "Hardened security headers", "Strict Content-Security-Policy, X-Frame-Options, Referrer-Policy and Permissions-Policy block clickjacking, injected scripts and data leaks."),
 ("code", "OWASP-aligned code", "We build against the OWASP Top 10 — input validation, output encoding and protection from XSS, injection and CSRF attacks."),
 ("key", "Secure authentication", "Hashed passwords, per-user accounts, role-based access and session protection. No shared logins — every action is accountable."),
 ("db", "Data protection", "We collect only what's needed, encrypt it in transit and store it with trusted providers that encrypt data at rest."),
 ("cloud", "Global CDN &amp; DDoS shielding", "Sites are deployed on enterprise-grade global edge networks with built-in DDoS mitigation and near-100% uptime."),
 ("backup", "Backups &amp; version control", "Every line of code lives in version control, with automated backups — so any change can be rolled back in minutes."),
 ("pulse", "Monitoring &amp; patching", "Dependencies are kept updated, vulnerabilities patched and uptime monitored — security is a process, not a one-time checkbox."),
]

PROCESS = [
 ("01", "Discover", "We listen first — your goals, audience and requirements — before anything is planned. Every project starts with listening, not assumptions."),
 ("02", "Design", "Wireframes, visual direction and a clear plan. You review and approve every screen before a single line of code is written."),
 ("03", "Engineer", "Clean, secure, scalable code — with regular previews so you can give feedback throughout the build."),
 ("04", "Launch &amp; care", "We launch, hand over full source code and documentation, and stay on for support, updates and security."),
]

# ---------------------------------------------------------------- partials
import hashlib
def V(rel):
    """Asset URL with a content hash, so browsers always load the latest file after a deploy."""
    with open(os.path.join(OUT, rel), "rb") as fh:
        return "{P}" + rel + "?v=" + hashlib.sha1(fh.read()).hexdigest()[:10]

def head(title, desc, path, extra=""):
    url = f"{SITE}/{path}" if path else SITE + "/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bardium">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{{P}}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{{P}}assets/img/apple-touch-icon.png">
<link rel="preload" href="{{P}}assets/fonts/outfit-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{P}}assets/fonts/instrument-serif-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{V("assets/css/style.css")}">
<script src="{V("assets/js/bg.js")}" defer></script>
<script src="{V("assets/js/main.js")}" defer></script>
{extra}</head>
'''

def mega():
    links = "".join(
        f'<a class="mega__link" href="{{P}}services.html#{s[0]}"><span class="mega__num">0{i+1}</span><span class="mega__title">{s[2]} {icon("arrow")}</span><span class="mega__desc">{s[3]}</span></a>'
        for i, s in enumerate(SERVICES))
    return f'''<div class="mega" role="region" aria-label="What we do">
  <div class="container mega__inner">
    <div class="mega__intro">
      <h3>Crafted,<br>end to end.</h3>
      <p>If it runs on a screen, we build it — and secure it. From the first sketch to years after launch.</p>
      <p><a class="link-arrow" href="{{P}}services.html">All services {icon("arrow")}</a></p>
    </div>
    <div class="mega__grid">{links}</div>
    <a class="mega__feature" href="{{P}}security.html">
      <img class="mega__feature-icon" src="{{P}}assets/img/logo-mark-white.svg" alt="" width="54" height="63">
      <h4>Secured by default</h4>
      <p>Every website and software we build is secured — HTTPS, encrypted data and OWASP-aligned code, at no extra cost.</p>
      <span class="link-arrow">Our security standard {icon("arrow")}</span>
    </a>
  </div>
</div>'''

def header(page):
    def nl(key, href, label):
        return f'<li class="nav__item"><a class="nav__link" data-nav="{key}" href="{href}">{label}</a></li>'
    dock = [("home", "index.html", "home", "Home"), ("services", "services.html", "grid", "Services"),
            ("work", "work.html", "case", "Work"), ("pos", "pos.html", "cart", "POS"), ("security", "security.html", "shield", "Security"),
            ("contact", "contact.html", "mail", "Contact")]
    dock_html = "".join(f'<a class="dock__link" data-nav="{k}" href="{{P}}{h}">{icon(i)}<span>{l}</span></a>' for k, h, i, l in dock)
    return f'''<body data-page="{page}">
<a class="skip-link" href="#main">Skip to content</a>
<div class="preloader" aria-hidden="true">
  <div class="preloader__inner">
    <svg class="preloader__mark" viewBox="4 2 121 141"><path d="{LOGO}"/></svg>
    <div class="preloader__word"><span>Bardium</span></div>
    <div class="preloader__bar"><i></i></div>
  </div>
</div>
<div class="page-fade" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"></div>
<div class="cursor-ring" aria-hidden="true"><span class="cursor-ring__label">View</span></div>

<header class="header">
  <div class="container header__inner">
    <a class="brand" href="{{P}}index.html" aria-label="Bardium — home">
      <img class="brand__mark" src="{{P}}assets/img/logo-mark-white.svg" alt="" width="30" height="35">
      <span class="brand__name">Bardium</span>
    </a>
    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">
        <li class="nav__item nav__item--mega">
          <a class="nav__link" data-nav="services" href="{{P}}services.html" aria-haspopup="true">What We Do {icon("chev", "nav__chev")}</a>
          {mega()}
        </li>
        {nl("work", "{P}work.html", "Our Work")}
        {nl("pos", "{P}pos.html", "Bardium POS")}
        {nl("security", "{P}security.html", "Security")}
        {nl("process", "{P}index.html#process", "How We Work")}
        {nl("contact", "{P}contact.html", "Contact")}
      </ul>
    </nav>
    <div class="header__cta">{btn("Get a free quote", "{P}contact.html", "btn--sm")}</div>
  </div>
</header>
<nav class="dock" aria-label="Mobile navigation">{dock_html}</nav>
'''

def footer():
    svc = "".join(f'<li><a href="{{P}}services.html#{s[0]}">{s[2].replace("Website Design &amp; Development","Website Design").replace("Custom Software Development","Custom Software")}</a></li>' for s in SERVICES)
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <a class="brand" href="{{P}}index.html" aria-label="Bardium — home">
          <img class="brand__mark" src="{{P}}assets/img/logo-mark-white.svg" alt="" width="38" height="44">
          <span class="brand__name">Bardium</span>
        </a>
        <p class="footer__slogan">Built to be <span class="serif">remembered.</span></p>
        <p>Premium, secured websites, software and applications — designed in India, built for the world.</p>
      </div>
      <div class="footer__col">
        <h4>What we do</h4>
        <ul>{svc}</ul>
      </div>
      <div class="footer__col">
        <h4>Company</h4>
        <ul>
          <li><a href="{{P}}work.html">Our Work</a></li>
          <li><a href="{{P}}pos.html">Bardium POS</a></li>
          <li><a href="{{P}}security.html">Security</a></li>
          <li><a href="{{P}}index.html#process">How We Work</a></li>
          <li><a href="{{P}}contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h4>Get in touch</h4>
        <ul>
          <li><a href="mailto:info@bardium.in">info@bardium.in</a></li>
          <li><a href="tel:+919972782952">+91 99727 82952</a></li>
          <li><a href="tel:+918147087749">+91 81470 87749</a></li>
          <li><a href="tel:+918861017667">+91 88610 17667</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer__giant" aria-hidden="true">Bardium</div>
  <div class="container">
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Bardium. All rights reserved. Built to be remembered.™</span>
      <div class="footer__legal">
        <a href="{{P}}privacy.html">Privacy Policy</a>
        <a href="{{P}}terms.html">Terms &amp; Conditions</a>
        <a href="{{P}}security.html">Security</a>
      </div>
    </div>
  </div>
</footer>
</body>
</html>
'''

def cta_section(title_a="Let's build", title_b="something unforgettable.", canvas="tunnel", lead="Tell us what you're imagining. A free discovery call, a fixed quote within 48 hours — and zero obligation.", primary=("Get a free quote", "{P}contact.html")):
    return f'''
<section class="section cta fade-top" aria-label="Start a project">
  <canvas class="bg-canvas" data-bg="{canvas}" aria-hidden="true"></canvas>
  <div class="container cta__inner">
    <span class="eyebrow" data-reveal>Your move</span>
    <h2 class="display cta__title" data-split>{title_a}<br><span class="serif">{title_b}</span></h2>
    <p class="lead" data-reveal data-delay=".2">{lead}</p>
    <div class="btn-row" data-reveal data-delay=".3">{btn(primary[0], primary[1])}<a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener"><span class="btn__label"><span>Chat on WhatsApp</span><span aria-hidden="true">Chat on WhatsApp</span></span>{icon("wa", "btn__arrow btn__arrow--static")}</a></div>
    {trust_row("trust-row--center")}
  </div>
</section>'''

def marquee(words, reverse=False):
    items = "".join(f'<span class="marquee__item">{w}{STAR}</span>' for w in words)
    r = " marquee--reverse" if reverse else ""
    return f'<div class="marquee{r}" aria-hidden="true"><div class="marquee__track"><div class="marquee__group">{items}</div><div class="marquee__group">{items}</div></div></div>'

def page(fname, page_key, title, desc, body, extra_head="", prefix=""):
    path = "" if fname == "index.html" else fname.replace(".html", "")
    doc = head(title, desc, path, extra_head) + header(page_key) + '<main id="main">' + body + "</main>" + footer()
    doc = doc.replace("{P}", prefix)
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(doc)
    print("wrote", fname, len(doc))

# ---------------------------------------------------------------- mockups
def phone_abudi():
    return f'''<div class="phone" aria-hidden="true"><div class="phone__screen"><span class="phone__notch"></span>
  <div class="ui-top"><div class="ui-kicker">Table 07 · Scan &amp; order</div><div class="ui-title">Abudi<br>Coffee Roasters</div></div>
  <div class="ui-tabs"><span class="ui-tab is-on">Coffee</span><span class="ui-tab">Cold</span><span class="ui-tab">Bakery</span></div>
  <div class="ui-list">
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Spanish Latte</div><div class="ui-sub">Double shot · condensed milk</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb ui-thumb--b"></span><div><div class="ui-name">V60 Pour Over</div><div class="ui-sub">Single origin · Ethiopia</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb ui-thumb--c"></span><div><div class="ui-name">Pistachio Croissant</div><div class="ui-sub">Baked fresh daily</div></div><span class="ui-add">+</span></div>
  </div>
  <div class="ui-cta"><span>Place order · 3 items</span><span>→</span></div>
</div></div>'''

def phone_lounge():
    return f'''<div class="phone phone--dark" aria-hidden="true"><div class="phone__screen"><span class="phone__notch"></span>
  <div class="ui-top"><div class="ui-kicker">Airport Lounge · Seat 14A</div><div class="ui-title">Good evening.<br>Dine at leisure.</div><div class="ui-ar">قائمة الطعام</div></div>
  <div class="ui-status"><i class="on"></i><i class="on"></i><i class="on"></i><i></i></div>
  <div class="ui-tabs"><span class="ui-tab is-on">Mains</span><span class="ui-tab">Arabic</span><span class="ui-tab">Desserts</span></div>
  <div class="ui-list">
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Grilled Hammour</div><div class="ui-sub">Saffron rice · lemon butter</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Lamb Machboos</div><div class="ui-sub">Slow-cooked · Gulf spices</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Umm Ali</div><div class="ui-sub">Warm · pistachio · cream</div></div><span class="ui-add">+</span></div>
  </div>
  <div class="ui-cta"><span>Status · Preparing</span><span>●</span></div>
</div></div>'''

# Airport lounge project on Home and Our Work. Never name Qatar, Doha or the lounge brand on the site.
SHOW_LOUNGE = True

SKYLINE_URL = "https://skyline-brief-web.onrender.com"

def phone_skyline():
    return '<div class="phone phone--shot" aria-hidden="true"><div class="phone__screen"><img src="{P}assets/img/skyline-brief-app.webp" alt="" width="390" height="844" loading="lazy" decoding="async"></div></div>'

MAHARAJA_URL = "https://maharajasharptools.in"
EXTERNAL = {"skyline": (SKYLINE_URL, "Skyline Brief"), "maharaja": (MAHARAJA_URL, "Maharaja Sharp Tools")}

def browser_maharaja():
    return '''<div class="browser" aria-hidden="true"><div class="browser__bar"><i></i><i></i><i></i><span>maharajasharptools.in</span></div><img class="browser__img" src="{P}assets/img/maharaja-sharp-tools-site.webp" alt="" width="1100" height="688" loading="lazy" decoding="async"></div>'''

def chip_float(cls, ico, title, sub):
    return f'<div class="float-chip {cls}" aria-hidden="true"><span class="float-chip__ic">{icon(ico)}</span><span>{title}<small>{sub}</small></span></div>'

ABUDI_FEATURES = ["Scan a table QR — full menu in seconds", "Orders hit the kitchen instantly", "Staff dashboard to accept &amp; complete", "Automatic bills — print or on-screen", "Menu updates in seconds", "Works on any smartphone"]
LOUNGE_FEATURES = ["Bilingual menu — English &amp; Arabic", "Live Kitchen Order Tickets (KOT)", "Flight, seat &amp; name on every order", "Live status: accepted → served", "Guest feedback on the dashboard", "Secure per-staff login accounts"]

SKYLINE_FEATURES = ["Every story checked against its original source", "Clear labels: confirmed, reported or community", "English &amp; Arabic, with full right-to-left layout", "Light and dark modes", "Alerts for the topics you follow", "Credit and a link to every original source"]

MAHARAJA_FEATURES = ["Full product catalogue, easy to browse", "Quote and WhatsApp buttons on every page", "Quick search to find any product", "Clean, professional look for a trade brand", "Works on any phone or computer", "Secured with HTTPS"]

def work_card(kind, detailed=False):
    if kind == "abudi":
        visual = phone_abudi() + chip_float("float-chip--a", "bell", "New order · T07", "Sent to kitchen") + chip_float("float-chip--b", "bolt", "Order to kitchen", "Under 1 second")
        tag, title, lead = "QR Table Ordering System", "Abudi<br>Coffee Roasters", "A digital ordering system for a specialty coffee house. Guests scan a QR code at their table, browse the full menu on their phone and order in seconds — no waiting, no paper menus."
        feats = ABUDI_FEATURES
        chips = ["Faster service", "Zero paper menus", "Fewer errors", "Live kitchen"]
    elif kind == "skyline":
        visual = phone_skyline() + chip_float("float-chip--a", "check", "Confirmed", "Sources checked") + chip_float("float-chip--b", "lang", "English · العربية", "One-tap switch")
        tag, title, lead = "AI News App · Dubai Real Estate", "Skyline<br>Brief", "A mobile app that brings trusted Dubai real estate news into one clean feed. Every fact is checked against the original source, every story shows how well it is sourced, and it reads beautifully in English and Arabic."
        feats = SKYLINE_FEATURES
        chips = ["AI-curated", "Verified sources", "Bilingual", "Secured from day one"]
    elif kind == "maharaja":
        visual = browser_maharaja() + chip_float("float-chip--a", "bell", "Get a quote", "One tap") + chip_float("float-chip--b", "lock", "Secured", "HTTPS everywhere")
        tag, title, lead = "Business Website · Cutting Tools", "Maharaja<br>Sharp Tools", "A clean, professional website for a Bengaluru supplier of precision cutting tools. Customers can browse the full range, then ask for a quote or message on WhatsApp in one tap."
        feats = MAHARAJA_FEATURES
        chips = ["Product catalogue", "Quote &amp; WhatsApp", "Mobile friendly", "Secured by default"]
    else:
        visual = phone_lounge() + chip_float("float-chip--a", "lang", "English · العربية", "One-tap switch") + chip_float("float-chip--b", "lock", "Staff login", "Per-user accounts")
        tag, title, lead = "Luxury Lounge Ordering &amp; KOT", "International<br>Airport Lounge", "A premium bilingual ordering and kitchen management system for a luxury lounge at a reputed international airport. Guests order from their seat; staff run every ticket on a real-time kitchen screen."
        feats = LOUNGE_FEATURES
        chips = ["Luxury guest experience", "Arabic &amp; English", "Real-time KOT", "Per-staff accountability"]
    fl = "".join(f"<li>{f}</li>" for f in (feats if detailed else feats[:4]))
    ch = "".join(f'<span class="chip">{c}</span>' for c in chips)
    more = "" if detailed else f'<a class="link-arrow" href="{{P}}work.html#{kind}">Read the case study {icon("arrow")}</a>'
    if kind in EXTERNAL:
        more = f'<a class="link-arrow" href="{EXTERNAL[kind][0]}" target="_blank" rel="noopener noreferrer">{"Visit the website" if kind == "maharaja" else "View the project"} {icon("arrow")}</a>'
    extra_detail = ""
    if detailed:
        extra_detail = f'<div><p class="eyebrow">Results</p></div><div class="chips">{ch}</div>'
    if kind in EXTERNAL:
        vis = f'<a class="work-card__visual" href="{EXTERNAL[kind][0]}" target="_blank" rel="noopener noreferrer" data-cursor="Open" aria-label="Open {EXTERNAL[kind][1]} (opens in a new tab)">{visual}</a>'
        tagline = f'<span class="work-card__tag">{"Live" if kind == "maharaja" else "Featured"} · {tag}</span>'
    else:
        vis = f'<div class="work-card__visual" data-cursor="Live">{visual}</div>'
        tagline = f'<span class="work-card__tag"><span class="live-dot"></span> Live · {tag}</span>'
    return f'''<article class="work-card" id="{kind}" data-reveal>
  {vis}
  <div class="work-card__body">
    {tagline}
    <h3>{title}</h3>
    <p>{lead}</p>
    <ul class="feature-list">{fl}</ul>
    <div class="chips">{SEC_CHIP}</div>
    {extra_detail}
    {more}
  </div>
</article>'''

NEXT_CARD = f'''<a class="next-card" href="{{P}}contact.html" data-reveal>
  <div><span class="eyebrow">Your project</span><h3>Could be next.</h3><p class="muted">A website, custom software or the app you keep thinking about — we're taking on new projects now.</p></div>
  <span class="round-arrow">{icon("arrow")}</span>
</a>'''

# ================================================================= HOME
def build_home():
    caps = "".join(f'<li>{c}</li>' for c in CAPABILITIES)
    sec = "".join(f'''<div class="sec-item" data-reveal data-delay="{(i%3)*0.08:.2f}"><div class="sec-item__icon">{icon(s[0])}</div><h3>{s[1]}</h3><p>{s[2]}</p></div>''' for i, s in enumerate(SECURITY[:6]))
    PROMS = [("gift", "Free discovery call", "Talk directly to the people who will build it. No sales scripts, no obligation."),
             ("doc", "Fixed quote in 48 hours", "A clear price and timeline before any work starts. No hidden costs. Ever."),
             ("lock", "Secured by default", "HTTPS, encrypted data and hardened, OWASP-aligned code on every build — at no extra cost."),
             ("code", "You own 100% of the code", "Full source code, designs and documentation are yours. No lock-in, no hostage situations."),
             ("approve", "You approve every step", "Every screen is signed off before code is written, with live previews throughout the build."),
             ("wrench", "30-day bug-fix warranty", "If anything we built misbehaves after launch, we fix it — free of charge.")]
    PROMISES = "".join(f'''<div class="promise-card{' promise-card--hl' if i == 2 else ''}" data-reveal data-delay="{(i%3)*0.08:.2f}"><span class="promise-card__n">0{i+1}</span><span class="promise-card__ic">{icon(ic_)}</span><h3>{t}</h3><p>{d}</p></div>''' for i, (ic_, t, d) in enumerate(PROMS))
    steps = "".join(f'''<div class="step" data-reveal data-delay="{i*0.1:.1f}"><div class="step__num">{n}</div><h3>{t}</h3><p>{d}</p></div>''' for i, (n, t, d) in enumerate(PROCESS))
    body = f'''
<section class="hero" aria-label="Introduction">
  <canvas class="bg-canvas" data-bg="logo" aria-hidden="true"></canvas>
  <div class="container">
    <div class="hero__content">
      <p class="eyebrow hero__eyebrow" data-reveal>Digital engineering studio</p>
      <h1 class="display h1 hero__title" data-split>Built to be<br><span class="serif">remembered.</span></h1>
      <p class="lead hero__sub" data-reveal data-delay=".25">We design and engineer premium, {secure()} websites, software and applications for brands that refuse to be ordinary.</p>
      <div class="btn-row" data-reveal data-delay=".35">{btn("Get a free quote", "contact.html")}{btn("See our work", "work.html", "btn--ghost")}</div>
      <div data-reveal data-delay=".45">{trust_row()}</div>
    </div>
  </div>
  <div class="hero__meta">
    <div class="container">
      <span class="scroll-cue"><span class="scroll-cue__line"></span>Scroll</span>
      <span class="avail"><span class="live-dot"></span>Booking new projects</span>
    </div>
  </div>
</section>

{marquee(["Secured websites", "Custom software", "Mobile apps", "Secured software", "E-commerce", "Secured by default"])}

<section class="section manifesto" aria-label="Manifesto">
  <canvas class="bg-canvas" data-bg="wave" data-horizon="0.78" data-cam="120" aria-hidden="true"></canvas>
  <div class="container">
    <p class="eyebrow" data-reveal>Our belief</p>
    <p class="manifesto__text" data-scrub>Most websites are forgotten in seconds. We build the ones people <span class="serif">remember</span> — fast, <span class="w-keep hl-secure" tabindex="0" data-tip="HTTPS · Encrypted data · OWASP-aligned code">secure</span>, meticulously crafted and <span class="w-keep ai-flip" tabindex="0" role="button" aria-label="AI — tap to flip"><span class="ai-flip__in"><span>AI</span><span>SI</span></span></span> engineered to perform from the very first click.</p>
    <div class="manifesto__sign" data-reveal><img src="assets/img/logo-mark-white.svg" alt="" width="22" height="26"> The Bardium standard</div>
  </div>
</section>

<section class="section crafted" id="services" aria-label="Services">
  <div class="container crafted__grid">
    <div class="crafted__text">
      <h2 class="display h2" data-split>Crafted,<br><span class="serif">end to end.</span></h2>
      <p class="lead" data-reveal data-delay=".15">Whatever you can imagine, we can build. Websites, custom software, web and mobile apps, online stores, booking and billing systems, dashboards and automation — for any business, in any industry.</p>
      <p class="crafted__sub" data-reveal data-delay=".2">One team takes your idea from the first sketch to launch — designing it, engineering it, keeping it {secure()} and looking after it for years to come. If it runs on a screen, Bardium builds it.</p>
      <ul class="caps" data-reveal data-delay=".25">{caps}<li class="caps__more">+ anything you imagine</li></ul>
      <div class="btn-row" data-reveal data-delay=".3">{btn("Tell us your idea", "contact.html")}{btn("Explore services", "services.html", "btn--ghost")}</div>
    </div>
    <div class="crafted__visual" data-reveal="fade"><canvas data-bg="sphere" data-r="0.34" aria-hidden="true"></canvas></div>
  </div>
</section>

<section class="section" id="work" aria-label="Selected work">
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>Selected work</p><h2 class="display h2" data-split>Live. Working.<br><span class="serif">Remembered.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">Real products, in production, used every day by real guests and real staff.</p>
    </div>
    <div class="work-list">
      {work_card("abudi")}
      {work_card("lounge") if SHOW_LOUNGE else ""}
      {work_card("skyline")}
      {work_card("maharaja")}
      {NEXT_CARD}
    </div>
  </div>
</section>

<section class="section promise fade-top" id="promise" aria-label="The Bardium promise">
  <canvas class="bg-canvas" data-bg="stars" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>The Bardium promise</p><h2 class="display h2" data-split>Zero risk.<br><span class="serif">Total confidence.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">Choosing who builds your website shouldn't feel like a gamble. So we take the risk off the table — and put it in writing.</p>
    </div>
    <div class="promise-grid">{PROMISES}</div>
    <div class="promise-cta" data-reveal>
      <div><p class="promise-cta__k">Ready when you are</p><p class="promise-cta__t">Your free discovery call is one click away.</p></div>
      <div class="btn-row">{btn("Claim your free call", "contact.html")}<a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener"><span class="btn__label"><span>WhatsApp us</span><span aria-hidden="true">WhatsApp us</span></span>{icon("wa", "btn__arrow btn__arrow--static")}</a></div>
    </div>
  </div>
</section>

<section class="section fade-top fade-bottom" id="security" aria-label="Security">
  <canvas class="bg-canvas" data-bg="hex" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>Security assurance</p><h2 class="display h2" data-split>Secured from<br><span class="serif">day one.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">Every website, web app and piece of software we deliver is {secure()} by default — HTTPS, encrypted data, hardened servers and OWASP-aligned code. Your business and your customers are protected from the very first line of code — not patched later.</p>
    </div>
    <div class="sec-grid">{sec}</div>
    <div class="sec-badges" data-reveal>
      <span class="sec-badge">{icon("lock")} HTTPS / TLS</span>
      <span class="sec-badge">{icon("shield")} OWASP Top 10</span>
      <span class="sec-badge">{icon("headers")} Strict CSP &amp; HSTS</span>
      <span class="sec-badge">{icon("backup")} Automated backups</span>
      <a class="sec-badge" href="security.html">Read our security standard {icon("arrow")}</a>
    </div>
  </div>
</section>

<section class="section section--paper" aria-label="Why Bardium">
  <canvas class="bg-canvas" data-bg="ripple" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>Why Bardium</p><h2 class="display h2" data-split>Obsessed with<br><span class="serif">the details.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">We are small by choice — so every project gets senior attention, honest timelines and craft you can feel.</p>
    </div>
    <div class="principles">
      <div class="principle" data-reveal><div class="principle__k">i.</div><h3>Design without templates</h3><p>Every layout is drawn for your brand alone. Nothing off-the-shelf, nothing you've seen before.</p></div>
      <div class="principle" data-reveal data-delay=".1"><div class="principle__k">ii.</div><h3>Engineering that lasts</h3><p>Clean, documented, scalable code — handed over to you in full, with no lock-in.</p></div>
      <div class="principle" data-reveal data-delay=".2"><div class="principle__k">iii.</div><h3>Partners after launch</h3><p>Updates, security and support for as long as you need us. We don't disappear.</p></div>
    </div>
  </div>
</section>

<section class="section" id="process" aria-label="How we work">
  <canvas class="bg-canvas" data-bg="flow" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>How we work</p><h2 class="display h2" data-split>From idea<br><span class="serif">to icon.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">Simple, transparent and built around your goals. Four steps. No surprises.</p>
    </div>
    <div class="process">{steps}</div>
  </div>
</section>
{cta_section()}
'''
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Bardium", "url": SITE, "logo": f"{SITE}/assets/img/apple-touch-icon.png",
           "slogan": SLOGAN, "email": "info@bardium.in",
           "contactPoint": [{"@type": "ContactPoint", "telephone": "+91-9972782952", "contactType": "sales", "areaServed": "Worldwide", "availableLanguage": ["English", "Hindi"]}]}
    ld = f'<script type="application/ld+json">{json.dumps(org)}</script>\n'
    page("index.html", "home", "Bardium — Built to be remembered. Premium websites &amp; web apps",
         "Bardium designs and engineers premium, secured websites, custom software, web and mobile apps and e-commerce for brands that refuse to be ordinary.", body, ld)

# ================================================================= SERVICES
def build_services():
    blocks = ""
    for i, s in enumerate(SERVICES):
        fl = "".join(f"<li>{f}</li>" for f in s[5])
        blocks += f'''<article class="svc" id="{s[0]}">
  <div class="svc__num" data-reveal>0{i+1} / 06</div>
  <h2 class="svc__title" data-reveal>{s[2]}<span class="serif">{s[3]}.</span></h2>
  <div class="svc__body" data-reveal data-delay=".1">
    <p>{s[4]}</p>
    <h4>What you get</h4>
    <ul class="feature-list">{fl}</ul>
    <div class="chips">{SEC_CHIP}</div>
  </div>
</article>'''
    body = f'''
<section class="page-hero" aria-label="Services">
  <canvas class="bg-canvas" data-bg="sphere" data-cx="0.76" data-r="0.32" aria-hidden="true"></canvas>
  <div class="container page-hero__content">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Services</span></nav>
    <h1 class="display h1" data-split>Crafted,<br><span class="serif">end to end.</span></h1>
    <p class="lead" data-reveal data-delay=".2">Whatever you need built — websites, software, apps and beyond. From the first sketch to years after launch — designed, engineered, {secure()} and cared for by Bardium.</p>
    <div data-reveal data-delay=".3">{trust_row()}</div>
  </div>
</section>
{marquee(["Design", "Develop", "Secured", "Launch", "Scale", "Care"], True)}
<section class="section section--tight" aria-label="Services">
  <div class="container">{blocks}
    <a class="next-card svc-more" href="contact.html" data-reveal>
      <div><span class="eyebrow">And much more</span><h3>Don't see it here?</h3><p class="muted">These are just a few examples. Any software, any app, any industry — if it runs on a screen, we build it. Tell us your idea.</p></div>
      <span class="round-arrow">{icon("arrow")}</span>
    </a>
  </div>
</section>

<section class="section" aria-label="How we engage">
  <canvas class="bg-canvas" data-bg="stars" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head section-head--center">
      <p class="eyebrow" data-reveal>How we engage</p>
      <h2 class="display h2" data-split>Choose your<br><span class="serif">pace.</span></h2>
      <p class="lead" data-reveal data-delay=".15">Clear scope, clear pricing, clear timelines. Pick the model that fits — every quote is tailored to your project.</p>
    </div>
    <div class="engage">
      <div class="engage-card" data-reveal><span class="engage-card__k">Model 01</span><h3>Project build</h3><p>A fixed-scope project — a new website, software or app — delivered end to end.</p><ul class="feature-list feature-list--single"><li>Fixed scope &amp; quote</li><li>Milestone-based delivery</li><li>Full source code handover</li></ul></div>
      <div class="engage-card engage-card--featured" data-reveal data-delay=".1"><span class="engage-card__k">Model 02 · Most chosen</span><h3>Build + care</h3><p>Your project built, then looked after — security, updates and support, every month.</p><ul class="feature-list feature-list--single"><li>Everything in Project build</li><li>Monthly security &amp; updates</li><li>Priority support line</li></ul></div>
      <div class="engage-card" data-reveal data-delay=".2"><span class="engage-card__k">Model 03</span><h3>Revamp sprint</h3><p>A focused sprint to redesign, speed up or finish an existing website or half-built project.</p><ul class="feature-list feature-list--single"><li>Audit in the first week</li><li>Keep SEO &amp; content</li><li>Fast, fixed timeline</li></ul></div>
    </div>
  </div>
</section>

{cta_section("Have something", "in mind?", "orbits")}
'''
    page("services.html", "services", "What We Do — Websites, Software, Apps &amp; E-Commerce | Bardium",
         "Bespoke website design, custom software, web and mobile applications, e-commerce, revamps and secured maintenance by Bardium — any software, for any business.", body)


# ================================================================= BARDIUM POS
POS_INV = "https://wa.me/919972782952?text=Hi%20Bardium%2C%20I%27d%20like%20early%20access%20to%20Bardium%20Invoice."
POS_DEMO = "https://wa.me/919972782952?text=Hi%20Bardium%2C%20I%27d%20like%20a%20free%20demo%20of%20Bardium%20POS."

# Extra line icons used only on the POS page
PI = {
 "store": '<path d="M3 9l1.5-5h15L21 9"/><path d="M4 9v11h16V9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20v-5h4v5"/>',
 "chef": '<path d="M6 14a4 4 0 0 1-.6-7.9A5 5 0 0 1 15 4.4a4 4 0 1 1 3 9.6"/><path d="M6 14h12v6H6z"/><path d="M6 17h12"/>',
 "coffee": '<path d="M17 8h1a3 3 0 0 1 0 6h-1"/><path d="M3 8h14v7a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M7 2v3M11 2v3"/>',
 "bolt2": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "cloudk": '<path d="M7 18a5 5 0 1 1 1-9.9A6 6 0 0 1 19.5 10 4 4 0 0 1 18 18z"/><path d="M10 14h4"/>',
 "cake": '<path d="M4 21h16v-8H4z"/><path d="M4 16c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 4 0"/><path d="M12 13V9M12 6a1.5 1.5 0 0 0 1.5-1.5C13.5 3 12 2 12 2s-1.5 1-1.5 2.5A1.5 1.5 0 0 0 12 6z"/>',
 "court": '<path d="M3 21V8l9-5 9 5v13"/><path d="M8 21v-7h8v7M3 21h18"/>',
 "grid4": '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
 "merge": '<path d="M8 3v6a4 4 0 0 0 4 4h0a4 4 0 0 1 4 4v4"/><path d="M16 3v6a4 4 0 0 1-4 4"/><path d="m5 6 3-3 3 3M13 6l3-3 3 3"/>',
 "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 "bike": '<circle cx="5.5" cy="17" r="3.5"/><circle cx="18.5" cy="17" r="3.5"/><path d="M8 17h6l-3-7h4l3.5 7M11 10l-2-4H6"/>',
 "bag": '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 "history": '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "toggle": '<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="16" cy="12" r="3"/>',
 "wifioff": '<path d="M2 2l20 20M8.5 16.1a5 5 0 0 1 7 0M5 12.6a10 10 0 0 1 5.2-2.7M16.8 10.1a10 10 0 0 1 2.2 2.5M2 8.8a15 15 0 0 1 4.2-2.6M10.7 5a15 15 0 0 1 11.3 3.8M12 20h.01"/>',
 "receipt": '<path d="M5 2v20l2.5-1.5L10 22l2-1.5 2 1.5 2.5-1.5L19 22V2l-2.5 1.5L14 2l-2 1.5L10 2 7.5 3.5z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 "support": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2" y="14" width="5" height="6" rx="2"/><rect x="17" y="14" width="5" height="6" rx="2"/><path d="M20 20a3 3 0 0 1-3 2h-3"/>',
 "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-1 2-2 0-1.5-1-1.6-1-3 0-1 .8-2 2-2h2a4 4 0 0 0 4-4 8 8 0 0 0-9-7z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10.5" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
 "rupee": '<path d="M6 4h12M6 9h12M14 20 7 13h3a4.5 4.5 0 0 0 0-9"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "plane": '<path d="M10.5 13.5 3 11l1.5-1.5 7.5 1L16 6a2 2 0 0 1 3 3l-4.5 4 1 7.5L14 22l-2.5-7.5z"/>',
 "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 "cloud": '<path d="M7 18a5 5 0 1 1 1-9.9A6 6 0 0 1 19.5 10 4 4 0 0 1 18 18z"/>',
}
def picon(name, cls=""): return ic(PI[name], cls) if name in PI else icon(name, cls)

POS_TYPES = [
 ("chef", "Fine dine", "Floors, table service and a calm kitchen."),
 ("coffee", "Cafés", "Quick counter billing and QR orders."),
 ("bolt2", "Quick service", "Fast take away and token-style flow."),
 ("cloudk", "Cloud kitchens", "Delivery orders, all in one inbox."),
 ("cake", "Bakeries &amp; sweets", "Simple counter sales, all day."),
 ("court", "Food courts", "Many counters, one clear view."),
]

POS_FEATURES = [
 ("toggle", "Menu on / off", "Sold out? Switch a dish off in one tap."),
 ("store", "Store open / close", "Open or close your outlet from anywhere."),
 ("chef", "Kitchen screen", "Live order tickets (KOT) for the kitchen."),
 ("bike", "Online orders", "Delivery orders land in one inbox."),
 ("bag", "Take away &amp; delivery", "Separate, simple flows for each."),
 ("calendar", "Advance orders", "Take orders for later, never forget one."),
 ("users", "Reservations &amp; waitlist", "Book tables and manage the queue."),
 ("merge", "Move &amp; merge tables", "Shift or join tables in seconds."),
 ("clock", "Staff clock-in", "Simple attendance for your team."),
 ("history", "Order history", "Find any old bill instantly."),
 ("chart", "Today at a glance", "Sales and orders for the day."),
 ("spark", "Guided setup", "A step-by-step guide to go live."),
]

POS_STEPS = [
 ("Free demo", "We show you Bardium POS working, on your phone or in your outlet."),
 ("Setup &amp; theme", "We add your menu, tables and floors, in your name and colours."),
 ("Train your team", "We train the counter, waiters and kitchen until they're confident."),
 ("Go live &amp; grow", "We stay with you for support, updates and loyalty offers."),
]

POS_SEC = [
 ("Your data stays separate", "Your menu, orders and customers are never mixed with anyone else's."),
 ("A login for every staff", "Each person signs in with their own login and sees only their part."),
 ("Encrypted connection", "Everything travels over HTTPS between your screens and the server."),
 ("Privacy done properly", "Customer sign-in, consent and data rules are handled with care."),
 ("Backups &amp; safe updates", "Your data is backed up and updates never stop your service."),
 ("Secured by default", "Security is part of Bardium POS from day one, at no extra cost."),
]

POS_FAQ = [
 ("Do I need internet to use Bardium POS?", "The Online edition needs internet so every screen stays in sync. If the counter goes offline, orders still reach the kitchen and billing continues when it reconnects. For places with weak internet, ask us about the Offline edition."),
 ("Can I run it on my phone?", "Yes. Owners and managers can see running tables, online orders and open or close the store from their phone. Waiters take orders on a phone too."),
 ("Will it look like my restaurant?", "Yes. Every restaurant gets its own name, colours and look, so your guests see your brand, not ours."),
 ("Who sets it up and trains my staff?", "We do. We add your menu, tables and floors, and train your counter, waiters and kitchen before you go live."),
 ("How much does Bardium POS cost?", "Our pricing is low and flexible. It depends on your outlet and the features you need, for both the Online and Offline editions. Book a free demo and we'll give you a clear quote, with no obligation."),
 ("Can I use Bardium POS outside India?", "Yes. Bardium POS is made in India and built for restaurants and cafés anywhere in the world."),
 ("How do guests pay?", "Guests and staff can pay by UPI, quickly and simply."),
 ("Is my data safe?", "Yes. Each restaurant's data is kept separate and secured, every staff member has their own login, and everything travels over an encrypted connection."),
]

STATUS = [("blank", "Blank"), ("running", "Running"), ("printed", "Bill printed"), ("waiting", "KOT / QR waiting"), ("hold", "On hold"), ("reserved", "Reserved")]

def build_pos():
    T = lambda s: s
    types = "".join(f'<article class="pz-type" data-reveal data-delay="{(i%3)*0.06:.2f}"><span class="pz-type__ic">{picon(k)}</span><h3>{t}</h3><p>{d}</p></article>' for i, (k, t, d) in enumerate(POS_TYPES))
    feats = "".join(f'<article class="pz-feat" data-reveal data-delay="{(i%4)*0.05:.2f}"><span class="pz-feat__ic">{picon(k)}</span><h3>{t}</h3><p>{d}</p></article>' for i, (k, t, d) in enumerate(POS_FEATURES))
    steps = "".join(f'<li class="pz-step" data-reveal data-delay="{i*0.08:.2f}"><span class="pz-step__n">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(POS_STEPS))
    secs = "".join(f'<li class="pz-sec" data-reveal><span class="pz-tick">{icon("check")}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for a, b in POS_SEC)
    faqs = "".join(f'<details class="pz-faq__item"{" open" if i == 0 else ""}><summary><span>{q}</span><span class="pz-faq__plus">{picon("plus")}</span></summary><p>{a}</p></details>' for i, (q, a) in enumerate(POS_FAQ))
    legend = "".join(f'<li><span class="pz-dot pz-dot--{k}"></span>{l}</li>' for k, l in STATUS)
    def ticks(items): return "".join(f'<li><span class="pz-tick pz-tick--sm">{icon("check")}</span>{x}</li>' for x in items)
    img = lambda src, alt, w, h, cls="": f'<img class="{cls}" src="{{P}}assets/img/pos/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    body = f'''
<div class="pos-page">

<section class="pz-hero" aria-label="Bardium POS">
  <div class="pz-wrap pz-hero__grid">
    <div class="pz-hero__copy">
      <p class="pz-pill" data-reveal><span class="pz-pill__dot"></span> Bardium POS · Made in India, used worldwide</p>
      <h1 class="pz-h1" data-reveal data-delay=".05">Run your whole restaurant from <span class="pz-hl">one screen.</span></h1>
      <p class="pz-lead" data-reveal data-delay=".12">Billing, tables, kitchen, QR orders, delivery and take away, all in one simple, {secure()} system. Made in India for restaurants and cafés around the world, and themed to look like yours.</p>
      <div class="pz-btns" data-reveal data-delay=".18">
        <a class="pz-btn pz-btn--primary" href="{POS_DEMO}" target="_blank" rel="noopener">Book a free demo {icon("arrow")}</a>
        <a class="pz-btn pz-btn--ghost" href="#features">See all features</a>
      </div>
      <ul class="pz-checks" data-reveal data-delay=".24">{ticks(["Works online &amp; offline", "Low, flexible pricing", "Works on any POS device", "Secured by default"])}</ul>
      <p class="pz-copower" data-reveal data-delay=".3"><span class="pz-copower__ic">{picon("spark")}</span>Co-powered by <b>Printel Business Solutions</b></p>
    </div>
    <div class="pz-hero__visual" data-reveal data-delay=".1">
      <div class="pz-browser">
        <div class="pz-browser__bar"><i></i><i></i><i></i><span>Bardium POS · Billing</span></div>
        {img("pos-counter.webp", "Bardium POS table view on the counter computer", 1342, 842)}
      </div>
      <div class="pz-phone">{img("pos-owner-phone.webp", "Bardium POS owner view on a phone", 392, 851)}</div>
      <div class="pz-float pz-float--a"><span class="pz-float__ic pz-float__ic--amber">{picon("bike")}</span><div><b>New online order</b><span>Table 9 · QR</span></div></div>
      <div class="pz-float pz-float--b"><span class="pz-float__ic pz-float__ic--green">{icon("check")}</span><div><b>Paid by UPI</b><span>Table 14 · bill closed</span></div></div>
      <div class="pz-float pz-float--c"><span class="pz-float__ic pz-float__ic--blue">{picon("chef")}</span><div><b>KOT sent</b><span>to the kitchen</span></div></div>
    </div>
  </div>
</section>

<section class="pz-strip" aria-label="Highlights">
  <div class="pz-wrap pz-strip__row">
    <div class="pz-strip__item">{picon("receipt")}<span>Fast billing</span></div>
    <div class="pz-strip__item">{picon("grid4")}<span>Live table view</span></div>
    <div class="pz-strip__item">{picon("chef")}<span>Kitchen tickets</span></div>
    <div class="pz-strip__item">{icon("qr")}<span>QR ordering</span></div>
    <div class="pz-strip__item">{picon("cloud")}<span>Online &amp; offline</span></div>
    <div class="pz-strip__item">{picon("tag")}<span>Low, flexible pricing</span></div>
  </div>
</section>

<section class="pz-partner" aria-label="Co-powered by Printel Business Solutions">
  <div class="pz-wrap">
    <div class="pz-partner__card" data-reveal>
      <div class="pz-partner__copy">
        <p class="pz-kicker">Our partner</p>
        <h2 class="pz-h3">Bardium POS, <span class="pz-hl">co-powered by Printel Business Solutions.</span></h2>
        <p>Bardium's modern, secured software, backed by Printel's long experience in billing and POS for businesses across India.</p>
      </div>
      <div class="pz-partner__stats">
        <div class="pz-stat"><b>10,000+</b><span>Customers</span></div>
        <div class="pz-stat"><b>16+</b><span>Years of experience</span></div>
      </div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Who it is for">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker" data-reveal>Made for every kind of food business</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">One POS. <span class="pz-hl">Any outlet.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Whether you run a busy restaurant or a small café counter, in India or anywhere in the world, Bardium POS fits the way you serve.</p>
    </div>
    <div class="pz-types">{types}</div>
  </div>
</section>

<section class="pz-sec-wrap pz-sec-wrap--tint" id="features" aria-label="Table view">
  <div class="pz-wrap pz-row">
    <div class="pz-row__copy">
      <p class="pz-kicker" data-reveal>Live table view</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Every table, <span class="pz-hl">at a glance.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">See which tables are running, which bills are printed and which orders are waiting, floor by floor, in clear colours.</p>
      <ul class="pz-legend" data-reveal data-delay=".14">{legend}</ul>
      <ul class="pz-list" data-reveal data-delay=".18">{ticks(["Floors like A/C, Non A/C, Rooftop and Family room", "Running time and bill amount on every table", "Move or merge tables in seconds", "Table reservations and a waitlist"])}</ul>
    </div>
    <div class="pz-row__media" data-reveal data-delay=".1">
      <div class="pz-shot">{img("pos-tables.webp", "Colour-coded table view in Bardium POS", 1342, 450)}</div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Kitchen and orders">
  <div class="pz-wrap pz-row pz-row--flip">
    <div class="pz-row__copy">
      <p class="pz-kicker" data-reveal>Orders &amp; kitchen</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">From table to kitchen, <span class="pz-hl">instantly.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Waiter orders, QR orders and online orders go straight to the kitchen as live tickets. Delivery and take away have their own simple flow.</p>
      <div class="pz-note" data-reveal data-delay=".14"><span class="pz-note__ic">{picon("wifioff")}</span><div><b>Counter offline? Service goes on.</b><p>If the counter computer loses connection, orders still reach the kitchen. Billing simply waits for the counter to come back.</p></div></div>
      <ul class="pz-list" data-reveal data-delay=".18">{ticks(["Live kitchen order tickets (KOT)", "Online orders waiting, clearly flagged", "Delivery, take away and advance orders", "Menu on / off when a dish runs out"])}</ul>
    </div>
    <div class="pz-row__media" data-reveal data-delay=".1">
      <div class="pz-shot">{img("pos-topbar.webp", "Bardium POS top bar with kitchen, online orders and an offline alert", 1342, 160)}</div>
      <div class="pz-kot">
        <div class="pz-kot__card"><div class="pz-kot__h"><b>KOT · Table 9</b><span>Dine in</span></div><ul><li><span>2 ×</span> Masala Dosa</li><li><span>1 ×</span> Filter Coffee</li><li><span>1 ×</span> Paneer Tikka <em>less spicy</em></li></ul><div class="pz-kot__f pz-kot__f--amber">Preparing</div></div>
        <div class="pz-kot__card"><div class="pz-kot__h"><b>KOT · Online</b><span>Delivery</span></div><ul><li><span>2 ×</span> Veg Biryani</li><li><span>1 ×</span> Brownie</li></ul><div class="pz-kot__f pz-kot__f--green">Ready</div></div>
        <div class="pz-kot__card"><div class="pz-kot__h"><b>KOT · Table 14</b><span>QR order</span></div><ul><li><span>1 ×</span> Cold Coffee</li><li><span>2 ×</span> Samosa</li></ul><div class="pz-kot__f pz-kot__f--blue">New</div></div>
      </div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap pz-sec-wrap--tint" aria-label="Owner app">
  <div class="pz-wrap pz-row">
    <div class="pz-row__copy">
      <p class="pz-kicker" data-reveal>Owner view</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Your restaurant, <span class="pz-hl">in your pocket.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Not at the outlet? Open Bardium POS on your phone and see everything that's happening, live.</p>
      <ul class="pz-list" data-reveal data-delay=".14">{ticks(["Open or close your store with one switch", "See running and free tables live", "Online orders waiting, right on your phone", "Staff clock-in and day timer"])}</ul>
    </div>
    <div class="pz-row__media pz-row__media--phone" data-reveal data-delay=".1">
      <div class="pz-phone pz-phone--solo">{img("pos-owner-phone.webp", "Owner view of Bardium POS on a phone", 392, 851)}</div>
      <div class="pz-badge pz-badge--a">{picon("toggle")} Store open</div>
      <div class="pz-badge pz-badge--b">{picon("bike")} 2 online orders</div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Hardware">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker" data-reveal>Hardware</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Works with <span class="pz-hl">any POS device.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Use Bardium POS on the hardware you already have, or let us help you choose the right setup for your outlet.</p>
    </div>
    <div class="pz-hw">
      <article class="pz-hw__card" data-reveal><div class="pz-hw__img">{img("hw-terminal.webp", "Touch screen POS terminal", 640, 640)}</div><h3>Touch POS terminals</h3><p>Fast billing on a counter touch screen.</p></article>
      <article class="pz-hw__card" data-reveal data-delay=".06"><div class="pz-hw__img">{img("hw-printer.webp", "Thermal receipt printer", 640, 640)}</div><h3>Receipt &amp; KOT printers</h3><p>Print bills and kitchen tickets.</p></article>
      <article class="pz-hw__card" data-reveal data-delay=".12"><div class="pz-hw__img">{img("hw-handheld.webp", "Handheld Android POS device", 640, 640)}</div><h3>Handheld POS</h3><p>Take orders and bill right at the table.</p></article>
      <article class="pz-hw__card" data-reveal data-delay=".18"><div class="pz-hw__img">{img("hw-kiosk.webp", "Self-order kiosk", 640, 640)}</div><h3>Self-order kiosks</h3><p>Let guests order and pay on their own.</p></article>
    </div>
    <ul class="pz-hw__also" data-reveal>{ticks(["Windows PCs &amp; laptops", "Android phones &amp; tablets", "Kitchen display screens", "Cash drawers &amp; barcode scanners"])}</ul>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="All features">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker" data-reveal>And so much more</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Everything you need. <span class="pz-hl">Nothing you don't.</span></h2>
    </div>
    <div class="pz-feats">{feats}</div>
  </div>
</section>

<section class="pz-sec-wrap pz-sec-wrap--tint" aria-label="Editions">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker" data-reveal>Online &amp; offline</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Online or offline. <span class="pz-hl">Your choice.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Bardium POS comes in two full editions. Run it in the cloud with every screen in sync, or offline on your counter when the internet can't be trusted.</p>
    </div>
    <div class="pz-eds">
      <article class="pz-ed pz-ed--main" data-reveal>
        <span class="pz-ed__tag">Online edition</span>
        <h3>Cloud POS</h3>
        <p>Counter, waiter phones, kitchen and guest QR all stay in sync over the internet.</p>
        <ul class="pz-list pz-list--light">{ticks(["Your own name, colours and look", "QR ordering and waiter phones", "Owner view on your phone", "Updates and support from Bardium"])}</ul>
        <a class="pz-btn pz-btn--white" href="{POS_DEMO}" target="_blank" rel="noopener">Book a free demo {icon("arrow")}</a>
      </article>
      <article class="pz-ed pz-ed--dark" data-reveal data-delay=".08">
        <span class="pz-ed__tag">Offline edition</span>
        <h3>Counter POS</h3>
        <p>For counters that must keep billing without the internet. Runs on a Windows computer.</p>
        <ul class="pz-list pz-list--light">{ticks(["Works without internet", "Runs on your counter computer", "Bills and kitchen tickets, always on", "Simple licence-key activation"])}</ul>
        <a class="pz-btn pz-btn--white" href="{POS_DEMO}" target="_blank" rel="noopener">Book a free demo {icon("arrow")}</a>
      </article>
    </div>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Pricing">
  <div class="pz-wrap">
    <div class="pz-price" data-reveal>
      <div class="pz-price__copy">
        <span class="pz-price__tag">{picon("tag")} Pricing</span>
        <h2 class="pz-h2 pz-h2--light">Low, flexible pricing.</h2>
        <p>Premium software shouldn't cost a fortune. Bardium POS is priced to fit your outlet, whether it's one café counter or a growing chain.</p>
        <div class="pz-btns"><a class="pz-btn pz-btn--white" href="{POS_DEMO}" target="_blank" rel="noopener">Get your price {icon("arrow")}</a></div>
      </div>
      <ul class="pz-price__pts">
        <li><span class="pz-price__ic">{picon("tag")}</span><div><b>Low cost</b><p>Priced for real businesses, not just big chains.</p></div></li>
        <li><span class="pz-price__ic">{picon("grid4")}</span><div><b>Flexible plans</b><p>Pay for the features and outlets you need.</p></div></li>
        <li><span class="pz-price__ic">{picon("cloud")}</span><div><b>Online or offline</b><p>Both editions, priced for your setup.</p></div></li>
        <li><span class="pz-price__ic">{icon("check")}</span><div><b>Clear quote</b><p>A free demo and a clear price before you decide.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="pz-sec-wrap pz-sec-wrap--tint" aria-label="Trusted worldwide">
  <div class="pz-wrap pz-trust pz-trust--one">
    <article class="pz-trust__card" data-reveal><span class="pz-trust__ic">{icon("globe")}</span><div><h3>Made in India. Used worldwide.</h3><p>Built in India for restaurants and cafés everywhere, with the same care, speed and security wherever you are.</p></div></article>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Bardium Invoice">
  <div class="pz-wrap">
    <div class="pz-inv" data-reveal>
      <div class="pz-inv__copy">
        <span class="pz-soon"><span class="pz-soon__dot"></span> Coming very soon</span>
        <h2 class="pz-h2">Bardium <span class="pz-hl">Invoice.</span></h2>
        <p class="pz-sub">Simple, {secure()} billing and invoicing for every kind of business, not just restaurants. From the team behind Bardium POS.</p>
        <ul class="pz-list">{ticks(["Create clean, professional invoices in seconds", "Keep track of who has paid and who hasn't", "Your business name and logo on every bill", "Works hand in hand with Bardium POS"])}</ul>
        <div class="pz-btns"><a class="pz-btn pz-btn--primary" href="{POS_INV}" target="_blank" rel="noopener">Get early access {icon("arrow")}</a></div>
      </div>
      <div class="pz-inv__visual" aria-hidden="true">
        <div class="pz-bill">
          <div class="pz-bill__top"><div class="pz-bill__brand"><span class="pz-bill__logo">YB</span><div><b>Your Business</b><span>Tax invoice</span></div></div><span class="pz-bill__paid">Paid</span></div>
          <div class="pz-bill__meta"><div><span>Billed to</span><b>Customer name</b></div><div><span>Date</span><b>Today</b></div></div>
          <div class="pz-bill__rows">
            <div class="pz-bill__row pz-bill__row--h"><span>Item</span><span>Qty</span><span>Amount</span></div>
            <div class="pz-bill__row"><span>Product one</span><span>2</span><span>₹ ——</span></div>
            <div class="pz-bill__row"><span>Product two</span><span>1</span><span>₹ ——</span></div>
            <div class="pz-bill__row"><span>Service</span><span>1</span><span>₹ ——</span></div>
          </div>
          <div class="pz-bill__total"><span>Total</span><b>₹ ——</b></div>
          <div class="pz-bill__actions"><span>{icon("doc")} Download</span><span>{icon("wa")} Share</span></div>
        </div>
        <div class="pz-bill pz-bill--back"></div>
      </div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Getting started">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker" data-reveal>Getting started</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Live in <span class="pz-hl">four simple steps.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">We handle the setup, the look and the training. You keep serving your guests.</p>
    </div>
    <ol class="pz-steps">{steps}</ol>
  </div>
</section>

<section class="pz-sec-wrap pz-navy" aria-label="Security">
  <div class="pz-wrap">
    <div class="pz-head pz-head--center">
      <p class="pz-kicker pz-kicker--light" data-reveal>Security &amp; privacy</p>
      <h2 class="pz-h2 pz-h2--light" data-reveal data-delay=".05">Your business, <span class="pz-hl pz-hl--light">secured.</span></h2>
    </div>
    <ul class="pz-secs">{secs}</ul>
  </div>
</section>

<section class="pz-sec-wrap" aria-label="Support">
  <div class="pz-wrap">
    <div class="pz-support" data-reveal>
      <span class="pz-support__ic">{picon("support")}</span>
      <div class="pz-support__copy">
        <h2 class="pz-h3">Real people. <span class="pz-hl">Real support.</span></h2>
        <p>Stuck during a rush? Call us. We help you on the phone, on WhatsApp or at your outlet.</p>
      </div>
      <div class="pz-support__act">
        <a class="pz-support__num" href="tel:+919972782952">{icon("phone")} +91 99727 82952</a>
        <a class="pz-btn pz-btn--ghost pz-btn--sm" href="{POS_DEMO}" target="_blank" rel="noopener">{icon("wa")} WhatsApp us</a>
      </div>
    </div>
  </div>
</section>

<section class="pz-sec-wrap pz-sec-wrap--tint" aria-label="Questions">
  <div class="pz-wrap pz-faq">
    <div class="pz-faq__head">
      <p class="pz-kicker" data-reveal>Questions</p>
      <h2 class="pz-h2" data-reveal data-delay=".05">Good to <span class="pz-hl">know.</span></h2>
      <p class="pz-sub" data-reveal data-delay=".1">Have another question? Call or message us any time.</p>
    </div>
    <div class="pz-faq__list" data-reveal data-delay=".1">{faqs}</div>
  </div>
</section>

<section class="pz-cta" aria-label="Book a demo">
  <div class="pz-wrap pz-cta__inner">
    <h2 class="pz-h2 pz-h2--light" data-reveal>See Bardium POS in <span class="pz-serif">your</span> restaurant.</h2>
    <p data-reveal data-delay=".08">Book a free demo. We'll show you how it looks and works with your own menu. No pressure.</p>
    <div class="pz-btns pz-btns--center" data-reveal data-delay=".14">
      <a class="pz-btn pz-btn--white" href="{POS_DEMO}" target="_blank" rel="noopener">Book a free demo {icon("arrow")}</a>
      <a class="pz-btn pz-btn--outline-light" href="tel:+919972782952">{icon("phone")} Call us</a>
    </div>
  </div>
</section>

</div>
'''
    page("pos.html", "pos", "Bardium POS — Secured Restaurant &amp; Café POS Software | Bardium",
         "Bardium POS, co-powered by Printel Business Solutions, is a secured restaurant and café POS, made in India and used worldwide, with online and offline editions, low and flexible pricing, and support for any POS device: billing, live table view, kitchen tickets, QR ordering, online orders, UPI payments and an owner view on your phone, themed to your brand.",
         body, extra_head=f'<link rel="stylesheet" href="{V("assets/css/pos.css")}">\n')


# ================================================================= WORK
def build_work():
    body = f'''
<section class="page-hero" aria-label="Our work">
  <canvas class="bg-canvas" data-bg="wave" data-horizon="0.74" data-cam="120" aria-hidden="true"></canvas>
  <div class="container page-hero__content">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Our work</span></nav>
    <p class="eyebrow" data-reveal>Selected work</p>
    <h1 class="display h1" data-split>Live. Working.<br><span class="serif">Remembered.</span></h1>
    <p class="lead" data-reveal data-delay=".2">Products in production — used every day by real guests and real staff. Here's what we've delivered.</p>
  </div>
</section>
<section class="section section--tight" aria-label="Case studies">
  <div class="container">
    <div class="work-list">
      {work_card("abudi", True)}
      {work_card("lounge", True) if SHOW_LOUNGE else ""}
      {work_card("skyline", True)}
      {work_card("maharaja", True)}
      {NEXT_CARD}
    </div>
  </div>
</section>
{marquee(["Cafés", "Restaurants", "Startups", "Retail", "Enterprises"])}
{cta_section("Your story,", "built next.", "tunnel")}
'''
    page("work.html", "work", "Our Work — Live Projects &amp; Case Studies | Bardium",
         "Case studies from Bardium: a QR table ordering system for Abudi Coffee Roasters, a business website for Maharaja Sharp Tools, and Skyline Brief, an AI news app for Dubai real estate.", body)

# ================================================================= SECURITY
def build_security():
    sec = "".join(f'''<div class="sec-item" data-reveal data-delay="{(i%3)*0.08:.2f}"><div class="sec-item__icon">{icon(s[0])}</div><h3>{s[1]}</h3><p>{s[2]}</p></div>''' for i, s in enumerate(SECURITY))
    checks = [
        ("HTTPS enforced", "Valid SSL certificate, HTTP→HTTPS redirect and HSTS."),
        ("Security headers verified", "CSP, X-Frame-Options, nosniff, Referrer &amp; Permissions policies."),
        ("Forms protected", "Validation, spam honeypots and rate-limited third-party handlers."),
        ("No secrets in code", "API keys and credentials kept in secure environment settings."),
        ("Dependencies audited", "Packages scanned and updated before go-live."),
        ("Access reviewed", "Least-privilege accounts for every admin and staff user."),
        ("Backups in place", "Version control and a tested rollback path."),
        ("Performance &amp; uptime", "Speed tested and monitoring switched on at launch."),
    ]
    cl = "".join(f'<li data-reveal><span class="tick">{icon("check")}</span><div><strong>{a}</strong><span class="d">{b}</span></div></li>' for a, b in checks)
    body = f'''
<section class="page-hero" aria-label="Security">
  <canvas class="bg-canvas" data-bg="network" aria-hidden="true"></canvas>
  <div class="container page-hero__content">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Security</span></nav>
    <p class="eyebrow" data-reveal>Security assurance</p>
    <h1 class="display h1" data-split>Security,<br><span class="serif">built in.</span></h1>
    <p class="lead" data-reveal data-delay=".2">Every website, app and piece of software we deliver is {secure()} from the very first line of code — not patched later. And we keep it protected long after launch.</p>
  </div>
</section>
<section class="section section--tight" aria-label="Security pillars">
  <div class="container">
    <div class="section-head section-head--split">
      <div><p class="eyebrow" data-reveal>Eight pillars</p><h2 class="display h2" data-split>How we protect<br><span class="serif">what matters.</span></h2></div>
      <p class="lead" data-reveal data-delay=".15">The same standard applies to every project — from a five-page website to a live software platform serving hundreds of users.</p>
    </div>
    <div class="sec-grid sec-grid--4">{sec}</div>
  </div>
</section>
<section class="section fade-top fade-bottom" aria-label="Launch checklist">
  <canvas class="bg-canvas" data-bg="hex" aria-hidden="true"></canvas>
  <div class="container">
    <div class="section-head">
      <p class="eyebrow" data-reveal>Before every launch</p>
      <h2 class="display h2" data-split>The Bardium<br><span class="serif">launch checklist.</span></h2>
    </div>
    <ul class="checklist">{cl}</ul>
    <div class="legal__callout" data-reveal>
      <p class="eyebrow">Practising what we preach</p>
      <p class="muted">This very website runs on HTTPS with a strict Content-Security-Policy, HSTS, clickjacking protection and no third-party trackers.</p>
    </div>
  </div>
</section>
{cta_section("Build it", "safe. Build it right.", "orbits")}
'''
    page("security.html", "security", "Security — Secure by Design | Bardium",
         "How Bardium secures every website and web app: HTTPS and HSTS, strict security headers, OWASP-aligned code, secure authentication, backups and monitoring.", body)

# ================================================================= CONTACT
def build_contact():
    opts = "".join(f"<option>{s[2]}</option>" for s in SERVICES) + "<option>Something else</option>"
    body = f'''
<section class="page-hero page-hero--short" aria-label="Contact">
  <canvas class="bg-canvas" data-bg="orbits" data-cx="0.8" aria-hidden="true"></canvas>
  <div class="container page-hero__content">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Contact</span></nav>
    <p class="eyebrow" data-reveal>Free discovery call · Fixed quote in 48h</p>
    <h1 class="display h1" data-split>Let's talk<br><span class="serif">big ideas.</span></h1>
  </div>
</section>
<section class="section section--tight" aria-label="Contact form">
  <div class="container contact-grid">
    <div>
      <p class="lead" data-reveal>Have a website, software or app in mind — or a project stuck halfway? Tell us. We reply within 48 hours with ideas, a timeline and a clear quote.</p>
      <div class="contact-info" data-reveal data-delay=".1">
        <div class="contact-row"><span class="contact-row__ic contact-row__ic--solid">{icon("wa")}</span><div><small>Fastest reply</small><a href="{WA}" target="_blank" rel="noopener">Chat on WhatsApp →</a></div></div>
        <div class="contact-row"><span class="contact-row__ic">{icon("mail")}</span><div><small>Email</small><a href="mailto:info@bardium.in">info@bardium.in</a></div></div>
        <div class="contact-row"><span class="contact-row__ic">{icon("phone")}</span><div><small>Call</small><div class="phones"><a href="tel:+919972782952">+91 99727 82952</a><a href="tel:+918147087749">+91 81470 87749</a><a href="tel:+918861017667">+91 88610 17667</a></div></div></div>
        <div class="contact-row"><span class="contact-row__ic">{icon("clock")}</span><div><small>Response time</small><span class="v">Within 48 hours</span></div></div>
        <div class="contact-row"><span class="contact-row__ic">{icon("pin")}</span><div><small>Location</small><span class="v">India · Serving clients worldwide</span></div></div>
      </div>
      <div class="next-steps" data-reveal data-delay=".15">
        <p class="eyebrow">What happens next</p>
        <ol>
          <li><span>01</span><div><strong>We reply within 48 hours</strong>A real person reads your message — no bots, no auto-sales.</div></li>
          <li><span>02</span><div><strong>Free discovery call</strong>We understand your goals and suggest the smartest way to reach them.</div></li>
          <li><span>03</span><div><strong>Fixed quote &amp; timeline</strong>A clear price before any work starts. You decide — zero obligation.</div></li>
        </ol>
      </div>
    </div>
    <div class="form" data-reveal data-delay=".15">
      <form id="contact-form" action="https://formspree.io/f/mdeozzlw" method="POST" novalidate>
        <div class="form__grid">
          <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="Rahul Sharma" required maxlength="100"><span class="err" role="alert"></span></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@company.com" required maxlength="150"><span class="err" role="alert"></span></div>
          <div class="field"><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+91" maxlength="20"></div>
          <div class="field"><label for="f-service">Service</label><select id="f-service" name="service"><option value="">Select a service</option>{opts}</select></div>
          <div class="field field--full"><label for="f-msg">Tell us about your project</label><textarea id="f-msg" name="message" placeholder="Goals, timeline, budget range, links…" required maxlength="4000"></textarea><span class="err" role="alert"></span></div>
          <div class="hp" aria-hidden="true"><label for="f-gotcha">Leave this empty</label><input id="f-gotcha" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
          <input type="hidden" name="_subject" value="New project enquiry — bardium.in">
        </div>
        <div class="form__foot">
          <p class="form__note">{icon("lock")} Your details are {secure("encrypted", "Sent over HTTPS · Never shared or sold")} and never shared. See our <a href="privacy.html">Privacy Policy</a>.</p>
          <button class="btn" type="submit"><span class="btn__label"><span>Get my free quote</span><span aria-hidden="true">Get my free quote</span></span>{ARROW}</button>
        </div>
      </form>
      <div class="form__status" role="status" aria-live="polite"></div>
      <div class="form-success" role="status" aria-live="polite">
        <span class="form-success__ic">{icon("check")}</span>
        <h3>Message received</h3>
        <p>Thank you<span class="js-name"></span> — we'll get back to you within 48 hours. Something remarkable starts here.</p>
        {btn("Back to home", "index.html", "btn--ghost")}
      </div>
    </div>
  </div>
</section>
'''
    body = body.replace('Thank you<span class="js-name"></span>', 'Thank you, <span class="js-name">friend</span>')
    page("contact.html", "contact", "Contact — Start a Project | Bardium",
         "Start a project with Bardium. Email info@bardium.in or call +91 99727 82952. We reply within 48 hours with ideas, a timeline and a clear quote.", body)

# ================================================================= LEGAL
def legal_page(fname, key, title, h1a, h1b, desc, sections, intro):
    toc = "".join(f'<a href="#{sid}">{i+1}. {t}</a>' for i, (sid, t, _) in enumerate(sections))
    secs = "".join(f'<h2 id="{sid}">{i+1}. {t}</h2>{c}' for i, (sid, t, c) in enumerate(sections))
    body = f'''
<section class="page-hero page-hero--short" aria-label="{h1a} {h1b}">
  <canvas class="bg-canvas" data-bg="stars" aria-hidden="true"></canvas>
  <div class="container page-hero__content">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>{h1a} {h1b}</span></nav>
    <p class="eyebrow" data-reveal>Legal</p>
    <h1 class="display h1" data-split>{h1a}<br><span class="serif">{h1b}</span></h1>
    <div class="legal__meta" data-reveal data-delay=".2"><span class="chip">Effective 15 October 2026</span><span class="chip">Last updated 15 October 2026</span></div>
  </div>
</section>
<section class="section section--tight" aria-label="{title}">
  <div class="container legal">
    <nav class="legal__toc" aria-label="On this page">{toc}</nav>
    <article class="legal__body">
      <p>{intro}</p>
      <div class="legal__callout"><p class="muted">Questions about this page? Write to <a href="mailto:info@bardium.in">info@bardium.in</a> — a real person will reply within 48 hours.</p></div>
      <div class="legal__spacer"></div>
      {secs}
    </article>
  </div>
</section>
'''
    page(fname, key, title, desc, body)

def build_privacy():
    S = [
     ("who", "Who we are", "<p>Bardium (“Bardium”, “we”, “us”) is a web design and development studio based in India, operating the website <a href=\"https://bardium.in\">bardium.in</a>. This Privacy Policy explains what personal information we collect through this website, why we collect it, and how we protect it.</p>"),
     ("collect", "Information we collect", "<h3>Information you give us</h3><p>When you use our contact form or email us, we collect the details you choose to share:</p><ul><li>Your name and email address</li><li>Your phone number (optional)</li><li>The service you are interested in and your project message</li></ul><h3>Information collected automatically</h3><p>Like most websites, our hosting provider automatically records basic technical data when you visit — such as your IP address, browser type, device type, pages requested and the date and time of the visit. This is used only for security, abuse prevention and keeping the site running.</p>"),
     ("use", "How we use your information", "<ul><li>To reply to your enquiry and prepare proposals or quotes</li><li>To deliver, manage and support projects you engage us for</li><li>To keep our website secure and prevent spam or abuse</li><li>To meet legal, tax and accounting obligations</li></ul><p>We do <strong>not</strong> sell, rent or trade your personal information, and we do not use it for third-party advertising.</p>"),
     ("cookies", "Cookies &amp; local storage", "<p>This website does not use advertising or tracking cookies. We use your browser’s session storage only to remember that the opening animation has already been shown during your visit — it contains no personal information and is cleared when you close the tab.</p>"),
     ("third", "Third-party services", "<p>We rely on a small number of trusted providers to run this website:</p><ul><li><strong>Formspree</strong> — processes contact-form submissions and delivers them to our inbox.</li><li><strong>Website hosting &amp; CDN</strong> (e.g. Netlify) — serves the website and keeps security logs.</li><li><strong>Email provider</strong> — receives and stores our business email.</li></ul><p>Each provider processes data under its own privacy policy and only for the purpose of providing its service to us.</p>"),
     ("retention", "How long we keep data", "<p>We keep enquiry details for as long as needed to respond and, if we work together, for the length of the project and any period required by law (for example, for invoicing and tax records). Enquiries that do not lead to a project are deleted within 24 months, or sooner on request.</p>"),
     ("security", "How we protect your data", "<p>This website is served exclusively over HTTPS with modern TLS encryption, HSTS and a strict Content-Security-Policy. Access to enquiries is limited to Bardium team members who need it. No method of transmission over the internet is 100% secure, but we take reasonable and appropriate measures to protect your information. Read more on our <a href=\"security.html\">Security page</a>.</p>"),
     ("rights", "Your rights", "<p>Subject to applicable law — including India’s Digital Personal Data Protection Act, 2023 — you may:</p><ul><li>Ask what personal data we hold about you</li><li>Ask us to correct or update it</li><li>Ask us to delete it</li><li>Withdraw consent for future communications</li><li>Raise a grievance about how your data is handled</li></ul><p>To exercise any of these rights, email <a href=\"mailto:info@bardium.in\">info@bardium.in</a>. We will respond within 30 days.</p>"),
     ("transfers", "International transfers", "<p>Some of our service providers may store or process data outside India. Where this happens, we rely on providers that apply strong security and contractual safeguards to protect your information.</p>"),
     ("children", "Children", "<p>This website is intended for businesses and adults. We do not knowingly collect personal information from anyone under 18. If you believe a child has sent us personal data, contact us and we will delete it.</p>"),
     ("changes", "Changes to this policy", "<p>We may update this policy from time to time. The “Last updated” date at the top of this page shows when it was last changed. Significant changes will be highlighted on this page.</p>"),
     ("contact", "Contact &amp; grievances", "<p>For any privacy question, request or complaint, contact our Grievance Officer:</p><p><strong>Bardium</strong><br>Email: <a href=\"mailto:info@bardium.in\">info@bardium.in</a><br>Phone: <a href=\"tel:+919972782952\">+91 99727 82952</a></p>"),
    ]
    legal_page("privacy.html", "privacy", "Privacy Policy | Bardium", "Privacy", "policy.",
               "How Bardium collects, uses and protects personal information shared through bardium.in.", S,
               "Your trust matters to us. This policy explains, in plain language, what information we collect when you visit bardium.in or contact us, and exactly how we look after it.")

def build_terms():
    S = [
     ("accept", "Acceptance of terms", "<p>By accessing <a href=\"https://bardium.in\">bardium.in</a> or engaging Bardium (“Bardium”, “we”, “us”) for any service, you (“Client”, “you”) agree to these Terms &amp; Conditions. If you do not agree, please do not use this website or our services.</p>"),
     ("services", "Our services", "<p>Bardium provides website design and development, web application development, QR ordering and restaurant technology, e-commerce development, website revamps, project completion, and maintenance and security services. The exact scope, deliverables, timeline and price of each project are set out in a written proposal or quotation agreed with you.</p>"),
     ("quotes", "Proposals &amp; quotations", "<p>Quotations are valid for 30 days from the date issued unless stated otherwise. Work begins once you accept the proposal in writing (email is sufficient) and any agreed advance payment is received. Requests outside the agreed scope will be quoted separately before any additional work begins.</p>"),
     ("payment", "Payments", "<ul><li>Payments follow the schedule in your proposal — typically an advance to begin, with the balance on milestones or before launch.</li><li>Invoices are payable within 7 days unless agreed otherwise.</li><li>We may pause work on overdue accounts until payment is received.</li><li>Advance payments cover work already scheduled and are non-refundable once work has started, except where required by law.</li><li>Third-party costs (domains, hosting, paid plugins, payment-gateway fees) are billed at actuals or paid directly by you.</li></ul>"),
     ("client", "Client responsibilities", "<p>You agree to provide content, feedback, approvals and access (such as domain or hosting credentials) in a timely manner. Delays in providing these may move the delivery date. You confirm that all content you supply — text, images, logos and data — is owned by you or properly licensed, and does not infringe anyone else’s rights.</p>"),
     ("revisions", "Revisions &amp; approvals", "<p>Each proposal includes a defined number of revision rounds. Additional revisions, or changes after a stage has been approved, may be charged separately. Your written approval of a design or build stage confirms it is complete.</p>"),
     ("ip", "Intellectual property", "<ul><li>On receipt of full payment, ownership of the final custom deliverables created specifically for you — including source code and designs — transfers to you.</li><li>Bardium retains ownership of its pre-existing tools, frameworks, libraries and know-how, and grants you a perpetual licence to use them as part of your deliverables.</li><li>Open-source and third-party components remain subject to their own licences.</li><li>Unless you ask us not to in writing, we may display the completed work in our portfolio and marketing.</li></ul>"),
     ("confidential", "Confidentiality", "<p>Both parties agree to keep confidential any non-public business, technical or financial information shared during a project, and to use it only for the purpose of that project. This obligation continues after the project ends.</p>"),
     ("warranty", "Support &amp; warranty", "<p>We fix defects in our own work reported within 30 days of launch at no extra cost. This does not cover issues caused by changes made by others, third-party services, hosting outages, or new feature requests. Ongoing support, updates and security maintenance are available under a separate care plan.</p>"),
     ("liability", "Limitation of liability", "<p>We take great care in our work, but websites depend on third-party systems we do not control. To the maximum extent permitted by law, Bardium is not liable for indirect, incidental or consequential losses — including loss of profit, data or business — and our total liability for any claim is limited to the amount you paid for the specific service giving rise to the claim.</p>"),
     ("termination", "Termination", "<p>Either party may end a project with written notice if the other materially breaches these terms and does not fix the breach within 14 days. On termination, you pay for all work completed up to that date, and we will hand over completed work once payment is settled.</p>"),
     ("website", "Use of this website", "<p>The content of this website — including text, design, graphics, animations, the Bardium name, logo and slogan — belongs to Bardium and may not be copied or reused without our written permission. You agree not to misuse the website, attempt to gain unauthorised access, or interfere with its security or operation.</p>"),
     ("law", "Governing law", "<p>These terms are governed by the laws of India. Any dispute will first be discussed in good faith; if it cannot be resolved, it shall be subject to the exclusive jurisdiction of the courts in Karnataka, India.</p>"),
     ("changes", "Changes to these terms", "<p>We may update these terms from time to time. The version published on this page at the time you accept a proposal applies to that project.</p>"),
     ("contact", "Contact", "<p>Questions about these terms? Email <a href=\"mailto:info@bardium.in\">info@bardium.in</a> or call <a href=\"tel:+919972782952\">+91 99727 82952</a>.</p>"),
    ]
    legal_page("terms.html", "terms", "Terms &amp; Conditions | Bardium", "Terms &amp;", "conditions.",
               "The terms and conditions for using bardium.in and engaging Bardium for website, web app and digital services.", S,
               "These terms set out how we work together — clearly and fairly. Please read them before engaging Bardium for a project or using this website.")

def build_404():
    body = f'''
<section class="nf" aria-label="Page not found">
  <canvas class="bg-canvas" data-bg="stars" aria-hidden="true"></canvas>
  <div class="container">
    <div class="nf__code" data-reveal>404</div>
    <h1 class="display h3" data-split>Lost in<br><span class="serif">space.</span></h1>
    <p class="lead" data-reveal data-delay=".2">The page you're looking for doesn't exist — but something remarkable is just one click away.</p>
    <div class="btn-row nf__btns" data-reveal data-delay=".3">{btn("Back to home", "/")}{btn("Contact us", "/contact.html", "btn--ghost")}</div>
  </div>
</section>'''
    page("404.html", "404", "Page not found | Bardium", "The page you are looking for could not be found.", body, prefix="/")

if __name__ == "__main__":
    build_home(); build_services(); build_work(); build_pos(); build_security(); build_contact(); build_privacy(); build_terms(); build_404()
