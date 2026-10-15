# Bardium website: step-by-step deployment guide (for beginners)

This guide takes you from "the files are in a folder" to "the new design is live on **https://bardium.in**".
Do each step in order and tick it off. Netlify and GitHub sometimes rename buttons slightly. If a label doesn't match exactly, look for the closest one.

---

## ✅ Part 0: What you have

The folder **`bardium-premium-website`** contains the whole website:

| File / folder | What it is |
|---|---|
| `index.html` | Home page |
| `services.html` | "What We Do" page |
| `work.html` | Our Work (case studies) |
| `security.html` | Security page |
| `contact.html` | Contact page with the form |
| `privacy.html` / `terms.html` | Privacy Policy and Terms & Conditions |
| `404.html` | "Page not found" page |
| `assets/css/style.css` | All the design (colours, fonts, layout, hover effects) |
| `assets/js/bg.js` | The 10 background animations |
| `assets/js/main.js` | Preloader, cursor, scroll effects, contact form |
| `assets/fonts/` | The fonts (stored inside the website, so there's no Google dependency) |
| `assets/img/` | Logo, favicon, social-share image |
| `_headers` | **Security headers** (HTTPS, CSP, anti-clickjacking). Netlify reads it automatically |
| `netlify.toml` | Tells Netlify there is **no build step**. It just publishes the folder |

There is **no npm, no React build and no `node_modules`**. It's pure HTML/CSS/JS, so the PowerShell/npm errors you had before can't happen.

---

## ✅ Part 1: Look at it on your computer (1 minute)

1. Open the folder `Bardium1 → bardium-premium-website`.
2. **Double-click `index.html`**. It opens in Chrome/Edge.
3. Click around: hover "What We Do" to see the mega menu, and scroll to see the animations.
4. To see the phone version, press **F12**, then click the 📱 phone icon (top-left of the panel) and choose "iPhone 12 Pro".

> The contact form only sends emails once the site is online (Part 4). That's normal.

---

## ✅ Part 2: Put the code on GitHub

### 2a. Create the repository
1. Go to **https://github.com** and sign in.
2. Top-right, click **`+`** → **New repository**.
3. **Repository name:** `bardium-website` (or any name you like).
4. Choose **Private** (recommended) or Public.
5. ⚠️ **Do NOT tick** "Add a README file", ".gitignore" or "license". Leave the repository empty.
6. Click the green **Create repository** button.
7. Copy the URL at the top (it looks like `https://github.com/YOUR-NAME/bardium-website`) and **send it to Claude**. Claude will push the code for you.

### 2b. (Only if you want to upload it yourself instead)
1. On the empty repository page, click the link **"uploading an existing file"**.
2. Open the `bardium-premium-website` folder, select **everything inside it** (Ctrl + A) and drag it into the browser window.
   - Make sure you drag the *contents*, so `index.html` sits at the top level of the repo and isn't inside another folder.
3. Wait for all files to finish uploading, then click **Commit changes** at the bottom.

---

## ✅ Part 3: Connect GitHub to Netlify (auto-deploy)

Your domain **bardium.in is already connected to your existing Netlify site**. The easiest path is to keep that site and point it at the new GitHub repo, so the domain and HTTPS stay as they are.

### Option A (recommended): reuse your existing Netlify site
1. Go to **https://app.netlify.com** and log in.
2. Click your existing site (the one showing `bardium.in`).
3. Left menu: **Site configuration** → **Build & deploy** → **Continuous deployment**.
4. Under **Repository**, click **Link repository** (or **Manage repository → Link to a different repository**).
5. Choose **GitHub**. If asked, click **Authorize Netlify** and allow access to the `bardium-website` repo.
6. Pick the **bardium-website** repository.
7. Build settings: fill them in exactly like this:
   - **Branch to deploy:** `main`
   - **Base directory:** *(leave empty)*
   - **Build command:** *(leave empty, and delete anything already there, e.g. `npm run build`)*
   - **Publish directory:** `.` *(just a dot; delete `build` if it's there)*
8. Click **Deploy** / **Save**.
9. Go to the **Deploys** tab. Within about 30 seconds you'll see **"Published"** in green.
10. Open **https://bardium.in** and press **Ctrl + F5** to hard-refresh. You should see the new black-and-white design. 🎉

### Option B: create a brand-new Netlify site
1. In Netlify, click **Add new site** → **Import an existing project** → **Deploy with GitHub**.
2. Pick `bardium-website`. Use the same build settings as step 7 above, then click **Deploy**.
3. You'll get a temporary address like `random-name-123.netlify.app`. Open it to check the site.
4. Move the domain over:
   - On the **old** site: **Domain management** → next to `bardium.in` click **Options → Remove domain** (do the same for `www.bardium.in`).
   - On the **new** site: **Domain management** → **Add a domain** → type `bardium.in` → **Verify** → **Add domain**.
5. If Netlify says **"Awaiting External DNS"**, go to **GoDaddy** → **My Products** → `bardium.in` → **DNS**:
   - **A** record, Name `@` → Value `75.2.60.5`
   - **CNAME** record, Name `www` → Value `your-new-site-name.netlify.app`
   - Click **Save**. DNS can take from 10 minutes up to a few hours.
6. Back in Netlify: **Domain management → HTTPS → Verify DNS configuration → Provision certificate**.

### Option C: no GitHub at all (quick manual upload)
1. In your Netlify site, open the **Deploys** tab.
2. Drag the whole `bardium-premium-website` folder onto the box that says **"Drag and drop your site output folder here"**.
3. Done. (You'll have to drag it again every time something changes.)

---

## ✅ Part 4: Check that everything works

1. **Website:** open https://bardium.in on your laptop **and** on your phone.
2. **Privacy & Terms:** scroll to the footer and click **Privacy Policy** and **Terms & Conditions**. Each opens its own page.
3. **Contact form:** go to Contact, send a test message, then check **info@bardium.in** (or your Gmail if it forwards).
   - The **first** time, Formspree may email you asking you to **confirm the form**. Click the link in that email.
   - In Formspree (https://formspree.io → your form → Settings), if "Restrict to domain" is on, add `bardium.in`.
4. **Security score:** go to **https://securityheaders.com**, type `bardium.in` and click **Scan**. You should see a top grade (A or A+), because the `_headers` file is working.
5. **Sharing preview:** paste `https://bardium.in` into WhatsApp. The black "Built to be remembered." card should appear (it can take a day for WhatsApp to refresh its cache).

---

## ✅ Part 5: Making changes later

Once GitHub + Netlify are connected, **every change you push to GitHub goes live automatically in about 30 seconds**.

- **Ask Claude:** tell Claude what to change (for example "add a Careers page") and it will edit the files and push them. Netlify publishes automatically.
- **On GitHub yourself:** open a file in the repo → click the ✏️ pencil → edit → **Commit changes**.
- **Contact details** are in the footer of every page and on `contact.html`.
- **Formspree form ID** is at the top of `assets/js/main.js` (`FORMSPREE_ID = "mdeozzlw"`).

---

## 🆘 If something goes wrong

| Problem | Fix |
|---|---|
| bardium.in still shows the old site | Press **Ctrl + F5**, or open it in an incognito window. Check the Netlify **Deploys** tab says *Published*. |
| Netlify deploy says "Build failed: npm…" | The build command isn't empty. Clear it and set Publish directory to `.` (see Part 3, step 7). |
| Page shows a white page / no styling | `index.html` must be at the **top level** of the GitHub repo, not inside another folder. |
| Contact form shows "Something went wrong" | Confirm the form in the Formspree email, and check the domain restriction in Formspree settings. |
| "Not secure" warning | Netlify → Domain management → HTTPS → **Verify DNS configuration**, then wait up to an hour. |
