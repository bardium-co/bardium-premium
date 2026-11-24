# Bardium website — notes for Claude

- Static site (HTML/CSS/JS), no build step on Netlify. Netlify auto-deploys every push to `main` → https://bardium.in
- **Pages are generated** by `_src/build.py` (header, mega menu, mobile dock, footer, all page content). Edit content there, run `python3 _src/build.py`, then commit the regenerated `.html` files. Don't hand-edit the `.html` files or the next build will overwrite them.
- Design system: `assets/css/style.css`. Animations: `assets/js/bg.js` (10 canvas scenes, touch/tilt/haptics). Interactions + contact form (Formspree `mdeozzlw`): `assets/js/main.js`.
- Security headers live in `_headers` (strict CSP: no inline scripts/styles, no external hosts except Formspree). Keep it that way.
- Owner preferences: premium black & white (CRED-like), no burger menu (desktop mega menu + mobile bottom dock), never show programming languages/tech stack, no stats/numbers, highlight "secured" wording, services are broad (any software/app), simple English.
- Before pushing: check every page on desktop, tablet and phone widths, with no console errors and no horizontal scroll.
- Bardium POS page (`pos.html`) is the exception to the black & white look: white & blue product theme from `assets/css/pos.css` (scoped to `body[data-page="pos"]`). At the owner's request it shows "Co-powered by Printel Business Solutions", 10,000+ customers and 16+ years of experience, and a "works with any POS device" hardware section.
