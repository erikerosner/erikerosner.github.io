# Launching ErikRosner.com — step by step

A click-by-click guide for putting this site live on GitHub Pages at **erikrosner.com**, written for a first launch. Do the parts in order, and don't skip the checks: each one tells you the step worked before you move on.

**Time:** about an hour of clicking, plus waiting for DNS. That's usually 10–60 minutes, but it can take up to a day.

**Safety net:** Webflow keeps serving the current site until Part 5, and you can undo Part 5 in two minutes (see "Undo" at the end). Your email (Google Workspace) is never touched.

---

## Before you start

You need:

- [ ] A **GitHub account**. If you don't have one, go to https://github.com/signup. The **username** you pick appears in a temporary web address (`username.github.io`), so choose something professional, e.g. `erikrosner` if it's free.
- [ ] Your **GoDaddy** login. erikrosner.com is registered at GoDaddy, and its DNS is managed there.
- [ ] Your **Webflow** login (only needed at the very end, days later).
- [ ] The **GitHub Desktop** app (free; installed in Part 1).

Your GitHub username is **erikrosner**. It is already filled in everywhere below (it was checked on Nov 10, 2026: the account exists and `erikrosner.github.io` is free to use as the repository name).


### Write down what's there now (your backup)

These are erikrosner.com's current public DNS records, looked up on Nov 9 and rechecked on Nov 10, 2026 (unchanged). You'll replace only the two marked **change**:

| Type | Name | Value | What it is | In this launch |
|---|---|---|---|---|
| A | `@` | `198.202.211.1` | Webflow (the current site) | **change** |
| CNAME | `www` | `cdn.webflow.com` | Webflow (www) | **change** |
| MX | `@` | `aspmx.l.google.com` + 4 `alt…` servers | Your email (Google) | **don't touch** |
| TXT | `@` | `v=spf1 a mx ptr include:secureserver.net ~all` | Email security | **don't touch** |
| TXT | `@` | `google-site-verification=…` | Google ownership | **don't touch** |
| TXT | `@` | `proxy-ssl.webflow.com` | Old Webflow setting | leave until Webflow is retired |

Before Part 5, also take a screenshot of GoDaddy's DNS page. It's your record of exactly how things were.

---

## Part 1 — Final check, and turn the folder into a repository

### 1.1 Run the final check

1. Open **Terminal** (press `⌘ Space`, type `Terminal`, press Return).
2. Paste this line and press Return:
   ```bash
   cd "/Users/erikrosner/Library/CloudStorage/Dropbox/2 AREAS/PORTFOLIO/PORTFOLIO-WEBSITE"
   ```
3. Paste this and press Return:
   ```bash
   python3 scripts/build.py
   ```
4. ✅ **Check:** the output ends with `0 error(s)` and `Built _site/ with 6 files`. If you see `ERROR:` lines, stop and fix those first. The same check runs on GitHub, and an error there would stop the launch.

### 1.2 Install and set up GitHub Desktop

1. Go to https://desktop.github.com and click **Download for macOS**.
2. Open the downloaded file. Drag **GitHub Desktop** into **Applications** if asked, then open it.
3. Click **Sign in to GitHub.com**. Your browser opens. Sign in, then click **Authorize desktop**, then **Open GitHub Desktop** if the browser asks.
4. In GitHub Desktop, open the menu **GitHub Desktop → Settings… → Git**:
   - **Name:** `Erik Rosner`
   - **Email:** pick the address ending in **`@users.noreply.github.com`** from the dropdown. The repository will be public, and this keeps your personal email out of it.
   - **Default branch name for new repositories:** make sure it says **`main`**. The launch automation only runs on `main`.
   - Click **Save**.

### 1.3 Turn the website folder into a repository

1. In GitHub Desktop: menu **File → Add Local Repository…**
2. Click **Choose…**, go to `Dropbox › 2 AREAS › PORTFOLIO`, select the **PORTFOLIO-WEBSITE** folder, and click **Add Repository**. (Desktop may show **Add repository** instead; same thing.)
3. Desktop says *"This directory does not appear to be a Git repository."* Click the blue link **create a repository** in that message.
4. In the **Create a New Repository** window:
   - **Name:** leave as `PORTFOLIO-WEBSITE` (this local name doesn't matter).
   - **Local Path:** leave as is (it should end in `/PORTFOLIO`).
   - **Initialize this repository with a README:** leave **unchecked**. You already have a README.
   - **Git Ignore:** **None**. **License:** **None**.
   - Click **Create Repository**.

### 1.4 Check exactly what will be published

The repository will be **public**, so everything committed can be read by anyone.

1. Click the **History** tab (top of the left column). Click the first entry, **Initial commit**.
   - If History is empty and the files are listed under **Changes** instead, type `Initial commit` in the **Summary** box at the bottom left, then click **Commit to main**.
2. ✅ **Check:** the commit lists these **14 files**, and nothing else. GitHub Desktop may also add a small `.gitattributes` file, which is fine.
   ```
   .github/workflows/deploy.yml
   .gitignore
   DEPLOY.md
   README.md
   assets/favicon.svg
   assets/phosphor-icons.svg
   index.html
   scripts/build.py
   scripts/check.py
   scripts/sitedata.py
   scripts/type_scale.py
   scripts/update_icons.py
   themes.csv
   tokens.css
   ```
   The `.gitignore` file keeps out `_archive/`, `REFERENCE-IMAGES/`, `mockup.png`, `_site/` and `.claude/`. If any of those appear, **stop** and don't publish. Ask for help instead.
3. ✅ **Check:** the toolbar's middle button says **Current Branch: main**.

> **Dropbox note:** the repository lives inside Dropbox. That's fine for one computer. Avoid editing the site on two computers at the same time, so Dropbox doesn't create "conflicted copy" files inside the hidden `.git` folder.

---

## Part 2 — Put it on GitHub

### 2.1 Publish

1. In GitHub Desktop, click **Publish repository** (top right).
2. In the window (tab **GitHub.com**):
   - **Name:** `erikrosner.github.io`, with your username exactly, all lowercase.
   - **Description:** optional, e.g. `ErikRosner.com`.
   - **Keep this code private:** **UNCHECK this.** Free GitHub accounts can only publish public repositories as websites.
   - **Organization:** None.
   - Click **Publish Repository**.
3. ✅ **Check:** menu **Repository → View on GitHub** opens the repository in your browser, and the file list matches 1.4.

### 2.2 Expect one red ✗. It's normal

Publishing makes GitHub try to launch the site right away, before Pages is switched on. In the browser, click the **Actions** tab: you'll see a run called **Deploy ErikRosner.com** with a **red ✗**. That's expected; Part 3 fixes it.

---

## Part 3 — Switch on GitHub Pages and launch the test site

### 3.1 Switch Pages to "GitHub Actions"

1. In your repository on github.com, click **Settings** (the last tab, with a gear icon).
2. In the left sidebar, under **Code and automation**, click **Pages**.
3. Under **Build and deployment → Source**, open the dropdown and choose **GitHub Actions**. It saves by itself; there's no Save button.

### 3.2 Run the launch again

1. Click the **Actions** tab.
2. In the left list, click **Deploy ErikRosner.com**.
3. On the right, click the **Run workflow** button, keep **Branch: main**, and click the green **Run workflow**.
   - Or open the red run and click **Re-run jobs → Re-run all jobs**.
4. Wait about a minute and refresh. ✅ **Check:** the new run has a **green ✓**.
   - Click the run: under **build-and-deploy** you'll see a link like `https://erikrosner.github.io/`.
   - If it's red, click it, then click the step with the ✗ and read the message. A failure in **Check and stage site** shows the same `ERROR:` text as step 1.1.

### 3.3 Test the site at its temporary address

Open `https://erikrosner.github.io/` and check:

- [ ] The page appears in a random color theme with the name in its font.
- [ ] Clicking **the name** or **the clue icon** steps through themes. Click around 26 times to see them all, including Seattle in Modak.
- [ ] Hovering the icon shows the clue to its right. The icon and clue drift toward the pointer and spring back.
- [ ] The pixel cursor appears and tilts when you move the mouse sideways. It becomes a hand over links.
- [ ] Every link opens in a **new tab**. The email is plain text (not a link).
- [ ] On your phone, the page reads as one column. Tapping the name changes the theme.

If all of that works, the site itself is done. The rest is pointing your domain at it.

---

## Part 4 — Tell GitHub about erikrosner.com (nothing changes for visitors yet)

### 4.1 Verify that you own the domain (recommended, 5 minutes)

This stops anyone else from ever attaching erikrosner.com to their own GitHub site.

1. On github.com, click your **profile photo** (top right) → **Settings**.
2. In the left sidebar, under **Code, planning, and automation**, click **Pages**.
3. Click **Add a domain**, type `erikrosner.com`, and click **Add domain**.
4. GitHub shows a **TXT record** to create, with a name like `_github-pages-challenge-erikrosner` and a long code as its value. **Keep this tab open.** You'll add the record in step 5.4, then come back here and click **Verify**.

### 4.2 Add the custom domain to the site

1. Go back to your **repository → Settings → Pages**.
2. Under **Custom domain**, type `erikrosner.com` (no `www`, no `https://`) and click **Save**.
3. GitHub starts a **DNS check** that will fail or stay "in progress" for now. That's expected until Part 5 is done. **Enforce HTTPS** stays greyed out for now.

> You don't need a `CNAME` file. When a site is published with GitHub Actions, as this one is, GitHub stores the domain in this setting.

---

## Part 5 — Point erikrosner.com to GitHub (GoDaddy DNS)

Pick a quiet time: for up to an hour, some visitors may see the old site or a certificate warning while things switch over.

### 5.1 Open GoDaddy's DNS page

1. Go to https://www.godaddy.com and click **Sign In** (top right).
2. Go to **My Products** (or your name → **My Products**). Under **Domains**, find **erikrosner.com** and click **DNS**, or **Manage DNS**.
   - Or open the domain, then click the **DNS** tab, then **DNS Records**.
3. Take a **screenshot** of the whole records table. That's your backup.

> GoDaddy's labels change from time to time. You're looking for a table of records with **Type / Name / Data (Value) / TTL** columns, a **pencil** (edit) and **trash** (delete) icon on each row, and an **Add New Record** button.

### 5.2 Replace the main address (`@`) with GitHub's four addresses

1. Find the row **Type A, Name `@`, Data `198.202.211.1`** (Webflow). Click the **pencil**, change Data to `185.199.108.153`, and click **Save**.
2. Click **Add New Record** three times, once for each of the remaining addresses:

   | Type | Name | Value | TTL |
   |---|---|---|---|
   | A | `@` | `185.199.109.153` | default (1 hour) |
   | A | `@` | `185.199.110.153` | default |
   | A | `@` | `185.199.111.153` | default |

   Click **Save** after each one.
3. ✅ **Check:** there are now exactly **four** A records on `@`, ending in `108.153`, `109.153`, `110.153` and `111.153`. Nothing should still say `198.202.211.1`.

*(Optional, for newer IPv6 networks: add four records of type **AAAA**, Name `@`, with Values `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153` and `2606:50c0:8003::153`. The site works fine without them.)*

### 5.3 Point `www` to GitHub

1. Find the row **Type CNAME, Name `www`, Data `cdn.webflow.com`**. Click the **pencil**.
2. Change Data to `erikrosner.github.io` (no `https://`, no slash) and click **Save**.

### 5.4 Add GitHub's ownership record (from step 4.1)

1. Click **Add New Record**: **Type TXT**. Paste **Name** from GitHub (`_github-pages-challenge-erikrosner`; GoDaddy adds `.erikrosner.com` by itself) and paste **Value** from GitHub. Click **Save**.
2. Back in the GitHub tab from 4.1, click **Verify**. If it says the record isn't found yet, wait 10 minutes and click **Verify** again.

### 5.5 Don't touch

- The five **MX** records (`aspmx.l.google.com` …). They are your email.
- The **TXT** records starting `v=spf1` and `google-site-verification`.
- Anything named `_domainconnect`, or any record you don't recognize.
- If GoDaddy has **Forwarding** set up for the domain (a separate section on the domain page), turn it off only if it forwards erikrosner.com or www somewhere. Otherwise leave it alone.

### 5.6 Wait, then check that it's switched

In Terminal, paste:
```bash
dig +short erikrosner.com
```
✅ **Done when** it prints the four `185.199.10x.153` addresses. Before then it still prints `198.202.211.1`; wait 10 minutes and try again.

Then:
```bash
dig +short www.erikrosner.com
```
✅ **Done when** the first line is `erikrosner.github.io.`

(Or check from anywhere at https://www.whatsmydns.net: type `erikrosner.com` and choose **A**.)

---

## Finish — HTTPS, final test, and retiring Webflow

### Turn on HTTPS

1. Open **repository → Settings → Pages**. Under Custom domain it should now say **DNS check successful**. If not, click **Check again** after a few minutes.
2. GitHub then issues a free security certificate, which takes from a few minutes to about an hour. When the **Enforce HTTPS** checkbox becomes clickable, **tick it**.
   - Still greyed out after 24 hours? Delete the custom domain (empty the box and click **Save**), wait a minute, type `erikrosner.com` again and click **Save**.

### Final test

- [ ] `https://erikrosner.com` shows the new site with a padlock in the address bar.
- [ ] `http://erikrosner.com` and `https://www.erikrosner.com` both end up at `https://erikrosner.com`.
- [ ] Repeat the checklist from 3.3 once, on desktop and phone.
- [ ] Send yourself a test email at hi@erikrosner.com to confirm email still works. It should, since nothing email-related changed.

### Retire Webflow (wait about a week)

Give it a week of the new site running well, so you can still undo if needed. Then:

1. In **Webflow**, open the old site → **Site settings → Publishing** (or **Hosting**). Under custom domains, **remove** `erikrosner.com` and `www.erikrosner.com`.
2. In Webflow's **billing / plans** for that site, cancel the site plan so you stop paying for hosting.
3. Back in GoDaddy DNS, you can now **delete** the TXT record `proxy-ssl.webflow.com`.

---

## Undo (if something goes wrong in Part 5)

Webflow is still running until you retire it, so you can switch back in GoDaddy:

1. Edit one `@` **A** record back to `198.202.211.1`, and delete the other three GitHub A records (and any AAAA records you added).
2. Edit the `www` **CNAME** back to `cdn.webflow.com`.
3. Within about an hour, visitors see the Webflow site again.

---

## Updating the site later

1. Edit the files (for example a clue in `themes.csv`). If you changed an icon, run `python3 scripts/update_icons.py`.
2. Run `python3 scripts/build.py` and make sure it shows `0 error(s)`.
3. Open **GitHub Desktop**. Your changed files appear under **Changes**. Type a short **Summary** (e.g. `New Seattle clue`), click **Commit to main**, then click **Push origin** (top right).
4. GitHub launches the update automatically. Check the **Actions** tab for the green ✓. The live site updates about a minute later, so refresh with `⌘ Shift R`.

If a check fails on GitHub, the run turns red and **the live site stays as it was**. Nothing broken ever goes live.

---

## If something looks wrong

| What you see | What to do |
|---|---|
| Actions run is red at **Configure Pages** | Part 3.1 isn't done: set Source to **GitHub Actions**, then re-run (3.2). |
| Actions run is red at **Check and stage site** | Click it and read the `ERROR:` lines. Fix them locally, check with step 1.1, then commit and push. |
| `erikrosner.github.io` shows **404** | Wait 2 minutes after a green run. Check the repository name is exactly `erikrosner.github.io` and that it's **public**. |
| Page loads but has no colors or clues | Hard refresh (`⌘ Shift R`). Check that `themes.csv` was committed (step 1.4). |
| erikrosner.com still shows Webflow | DNS hasn't switched yet. Run the `dig` check (5.6), and confirm no `198.202.211.1` A record is left in GoDaddy. |
| Browser says "Your connection is not private" | The certificate isn't ready yet. Wait up to an hour after **DNS check successful**, then tick **Enforce HTTPS**. |
| Email stopped working | Something changed the MX records. Restore them from your screenshot (5.1). |
