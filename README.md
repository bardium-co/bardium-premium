# bardium.in — "Built to be remembered."

Premium monochrome website for **Bardium**: pure HTML/CSS/JS, no build step.

- **Pages:** Home · What We Do · Our Work · Security · Contact · Privacy Policy · Terms & Conditions · 404
- **Animations:** 10 hand-built canvas backgrounds in `assets/js/bg.js` (logo particles, dot wave, dot sphere, secure network, hex scan, flow field, ripple grid, tunnel, orbits, starfield). They pause off-screen and respect "reduce motion".
- **Navigation:** inline nav with a "What We Do" mega menu on desktop and a bottom dock on mobile. No burger menu.
- **Security:** strict CSP, HSTS, X-Frame-Options and other headers in `_headers`; self-hosted fonts; no trackers.
- **Contact form:** Formspree (`assets/js/main.js` → `FORMSPREE_ID`).

## Run locally
Double-click `index.html`, or run `python -m http.server` in this folder and open http://localhost:8000.

## Deploy
Connected to Netlify. Every push to `main` goes live automatically. Full beginner guide: **[DEPLOY-GUIDE.md](DEPLOY-GUIDE.md)**.

## Add a new page
Copy `security.html`, rename it, change the `<title>`, the `data-page` on `<body>` and the content inside `<main>`, then add a link to it in the header nav, the mobile dock and the footer of each page.
