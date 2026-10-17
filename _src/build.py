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
<link rel="stylesheet" href="{{P}}assets/css/style.css">
<script src="{{P}}assets/js/bg.js" defer></script>
<script src="{{P}}assets/js/main.js" defer></script>
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
            ("work", "work.html", "case", "Work"), ("security", "security.html", "shield", "Security"),
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

def cta_section(title_a="Let's build", title_b="something unforgettable.", canvas="tunnel"):
    return f'''
<section class="section cta fade-top" aria-label="Start a project">
  <canvas class="bg-canvas" data-bg="{canvas}" aria-hidden="true"></canvas>
  <div class="container cta__inner">
    <span class="eyebrow" data-reveal>Your move</span>
    <h2 class="display cta__title" data-split>{title_a}<br><span class="serif">{title_b}</span></h2>
    <p class="lead" data-reveal data-delay=".2">Tell us what you're imagining. A free discovery call, a fixed quote within 48 hours — and zero obligation.</p>
    <div class="btn-row" data-reveal data-delay=".3">{btn("Get a free quote", "{P}contact.html")}<a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener"><span class="btn__label"><span>Chat on WhatsApp</span><span aria-hidden="true">Chat on WhatsApp</span></span>{icon("wa", "btn__arrow btn__arrow--static")}</a></div>
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
  <div class="ui-top"><div class="ui-kicker">Doha Lounge · Seat 14A</div><div class="ui-title">Good evening.<br>Dine at leisure.</div><div class="ui-ar">قائمة الطعام</div></div>
  <div class="ui-status"><i class="on"></i><i class="on"></i><i class="on"></i><i></i></div>
  <div class="ui-tabs"><span class="ui-tab is-on">Mains</span><span class="ui-tab">Arabic</span><span class="ui-tab">Desserts</span></div>
  <div class="ui-list">
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Grilled Hammour</div><div class="ui-sub">Saffron rice · lemon butter</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Lamb Machboos</div><div class="ui-sub">Slow-cooked · Gulf spices</div></div><span class="ui-add">+</span></div>
    <div class="ui-item"><span class="ui-thumb"></span><div><div class="ui-name">Umm Ali</div><div class="ui-sub">Warm · pistachio · cream</div></div><span class="ui-add">+</span></div>
  </div>
  <div class="ui-cta"><span>Status · Preparing</span><span>●</span></div>
</div></div>'''

def chip_float(cls, ico, title, sub):
    return f'<div class="float-chip {cls}" aria-hidden="true"><span class="float-chip__ic">{icon(ico)}</span><span>{title}<small>{sub}</small></span></div>'

ABUDI_FEATURES = ["Scan a table QR — full menu in seconds", "Orders hit the kitchen instantly", "Staff dashboard to accept &amp; complete", "Automatic bills — print or on-screen", "Menu updates in seconds", "Works on any smartphone"]
LOUNGE_FEATURES = ["Bilingual menu — English &amp; Arabic", "Live Kitchen Order Tickets (KOT)", "Flight, seat &amp; name on every order", "Live status: accepted → served", "Guest feedback on the dashboard", "Secure per-staff login accounts"]

def work_card(kind, detailed=False):
    if kind == "abudi":
        visual = phone_abudi() + chip_float("float-chip--a", "bell", "New order · T07", "Sent to kitchen") + chip_float("float-chip--b", "bolt", "Order to kitchen", "Under 1 second")
        tag, title, lead = "QR Table Ordering System", "Abudi<br>Coffee Roasters", "A digital ordering system for a specialty coffee house. Guests scan a QR code at their table, browse the full menu on their phone and order in seconds — no waiting, no paper menus."
        feats = ABUDI_FEATURES
        chips = ["Faster service", "Zero paper menus", "Fewer errors", "Live kitchen"]
    else:
        visual = phone_lounge() + chip_float("float-chip--a", "lang", "English · العربية", "One-tap switch") + chip_float("float-chip--b", "lock", "Staff login", "Per-user accounts")
        tag, title, lead = "Luxury Lounge Ordering &amp; KOT", "Doha Airport<br>Lounge", "A premium bilingual ordering and kitchen management system for a luxury airport lounge in Doha. Guests order from their seat; staff run every ticket on a real-time kitchen screen."
        feats = LOUNGE_FEATURES
        chips = ["Luxury guest experience", "Arabic &amp; English", "Real-time KOT", "Per-staff accountability"]
    fl = "".join(f"<li>{f}</li>" for f in (feats if detailed else feats[:4]))
    ch = "".join(f'<span class="chip">{c}</span>' for c in chips)
    more = "" if detailed else f'<a class="link-arrow" href="{{P}}work.html#{kind}">Read the case study {icon("arrow")}</a>'
    extra_detail = ""
    if detailed:
        extra_detail = f'<div><p class="eyebrow">Results</p></div><div class="chips">{ch}</div>'
    return f'''<article class="work-card" id="{kind}" data-reveal>
  <div class="work-card__visual" data-cursor="Live">{visual}</div>
  <div class="work-card__body">
    <span class="work-card__tag"><span class="live-dot"></span> Live · {tag}</span>
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
    <p class="touch-hint" aria-hidden="true"><span class="touch-hint__dot"></span>Tap · drag · tilt to play</p>
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
      {work_card("lounge")}
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
      {work_card("lounge", True)}
      {NEXT_CARD}
    </div>
  </div>
</section>
{marquee(["Cafés", "Airport lounges", "Restaurants", "Startups", "Retail", "Enterprises"])}
{cta_section("Your story,", "built next.", "tunnel")}
'''
    page("work.html", "work", "Our Work — Live Projects &amp; Case Studies | Bardium",
         "Case studies from Bardium: a QR table ordering system for Abudi Coffee Roasters and a bilingual luxury lounge ordering and KOT system in Doha.", body)

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
    build_home(); build_services(); build_work(); build_security(); build_contact(); build_privacy(); build_terms(); build_404()
