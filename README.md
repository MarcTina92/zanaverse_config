# Zanaverse Config

Lightweight Frappe app to **seed and enforce branding** (logo, favicon, etc.) and expose them everywhere (Desk + Website/Login). Supports a **white-label switch** so client changes can stick when desired.

---

## What this app sets

By default, all of these point to **one canonical asset** in your app:

```
/assets/zanaverse_config/images/zv-logo.png?v=2
```

Fields it controls (in **Website Settings**):

* `app_logo`
* `footer_logo`
* `favicon`
* `banner_image`
* `splash_image`
* `brand_html` (fallback `<img>` for places that render raw HTML)

And Frappe hooks that read from Website Settings:

* `app_logo_url` → `zanaverse_config.brand.app_logo_url`
* `brand_html`   → `zanaverse_config.brand.brand_html`
* `update_website_context` → `zanaverse_config.brand.update_website_context`
  (ensures **Website/Login** uses your logo + favicon)

---

## Install

```bash
# from your bench root
bench get-app https://github.com/MarcTina92/zanaverse_config.git
bench --site <your-site> install-app zanaverse_config
```

> Replace `<your-site>` e.g. `dev-zanaschools.localhost`.

---

## First-run branding (LOCKED by default)

The app reads a site config flag:

* `zanaverse_branding_locked` (default **true**)

Behavior:

* **locked = true** → force Zanaverse branding on every run (overwrites values)
* **locked = false** → only **seed empty fields**; client changes will **stick**

### Commands

```bash
# Enforce Zanaverse branding (locked)
bench --site <your-site> set-config zanaverse_branding_locked true
bench --site <your-site> execute zanaverse_config.install.apply_branding
# => {"changed": true/false, "force": true}

# Allow client white-label changes to stick (unlocked)
bench --site <your-site> set-config zanaverse_branding_locked false
bench --site <your-site> execute zanaverse_config.install.apply_branding
# => {"changed": true/false, "force": false}
```

The same `apply_branding` also runs after installation and on migrate via hooks.

---

## Using ONE logo everywhere

1. Put your logo once in the app (no spaces in the filename):

```
apps/zanaverse_config/zanaverse_config/public/images/zv-logo.png
```

Then build:

```bash
bench build --app zanaverse_config
```

2. (Optional) If you want to change the default image later, replace that file and bump the cache buster (`?v=3`), then:

```bash
bench build --app zanaverse_config
bench --site <your-site> clear-website-cache
bench --site <your-site> clear-cache
```

> You can still point **Website Settings** fields to any path you want (e.g. `/files/...`). The hooks will read whatever is set there; the **lock** only controls whether we overwrite them.

---

## Quick verification

### Server-side (what the page renders)

```bash
# Favicon + login card logo should both reference your asset
curl -s http://<your-site>/login | tr -d '\n' | sed 's/></>\n</g' \
| grep -i 'rel="shortcut icon"\|class="app-logo"'
```

### In a Python console

```python
bench --site <your-site> console
>>> import frappe, zanaverse_config.brand as b, pprint
>>> pprint.pprint(frappe.get_hooks('app_logo_url'))
>>> pprint.pprint(frappe.get_hooks('brand_html'))
>>> pprint.pprint(frappe.get_hooks('update_website_context'))
>>> b.app_logo_url()
'/assets/zanaverse_config/images/zv-logo.png?v=2'
```

### On Desk (browser DevTools)

```js
frappe.boot?.app_logo_url
document.querySelector('.navbar .navbar-brand img')?.src
```

Both should include `/assets/zanaverse_config/images/zv-logo.png?v=2`.

---

## Troubleshooting

* **Login shows wrong favicon**
  Clear website cache and confirm `update_website_context` is registered:

  ```bash
  bench --site <your-site> clear-website-cache
  bench --site <your-site> console
  >>> import frappe; frappe.get_hooks('update_website_context')
  ['zanaverse_config.brand.update_website_context']
  ```

* **Logo still flips back to Frappe after logout**
  You likely have `zanaverse_branding_locked=true` and an old asset.
  Replace the file, bump `?v=` and rebuild/clear caches; or set `locked=false` for that client if you want their custom logo to stick.

* **I want this site to be white-label**
  Set `zanaverse_branding_locked=false` and run `apply_branding` once. From then on, the client can change logo via UI and it won’t be overwritten.

---

## What lives where (code map)

```
zanaverse_config/
 ├─ zanaverse_config/
 │   ├─ brand.py           # app_logo_url(), brand_html(), update_website_context()
 │   ├─ install.py         # asbool(), apply_branding(), apply_branding_first_time()
 │   ├─ hooks.py           # registers hooks + after_install/after_migrate
 │   └─ public/
 │       └─ images/
 │           └─ zv-logo.png   # your canonical logo asset
 └─ README.md
```

---

## Updating the branding image

1. Replace `public/images/zv-logo.png` with your new image (PNG/SVG both fine).
2. Bump the version query e.g. `?v=3` in `hooks.py` (if referenced there) and/or update Website Settings to the new `?v=`.
3. Rebuild and clear caches:

```bash
bench build --app zanaverse_config
bench --site <your-site> clear-website-cache
bench --site <your-site> clear-cache
```

---

## Uninstall / Reset (optional)

```bash
# Remove the app (keeps your site)
bench --site <your-site> uninstall-app zanaverse_config

# Manually clear Website Settings branding (if you want a clean slate)
bench --site <your-site> execute frappe.client.set_value --kwargs \
'{"doctype":"Website Settings","name":"Website Settings","fieldname":"app_logo","value":""}'
# (repeat for footer_logo, favicon, banner_image, splash_image, brand_html)
bench --site <your-site> clear-website-cache
```

---

## License

MIT © Zanaverse
