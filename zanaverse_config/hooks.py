# -*- coding: utf-8 -*-
app_name = "zanaverse_config"
app_title = "Zanaverse"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# Ship only what you need as fixtures (theme is fine)
fixtures = [{"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]}]

# Dynamic branding (via helpers below)
app_logo_url = "zanaverse_config.brand.app_logo_url"
brand_html   = "zanaverse_config.brand.brand_html"

# On fresh install / migrate, enforce branding (you already have these)
after_install = "zanaverse_config.install.apply_branding_first_time"
after_migrate = "zanaverse_config.install.apply_branding"

# Website context + Desk boot overrides
update_website_context = "zanaverse_config.brand.update_website_context"
boot_session = "zanaverse_config.brand.boot_session"  # <— authoritative title/logo at boot

# Fallbacks (used before dynamic hooks run)
website_context = {
    "brand_html": "Zanaverse",
    "favicon": "/assets/zanaverse_config/favicon.png",
    "splash_image": "/assets/zanaverse_config/logo.svg",
}

# Tiny client nudge for SPA routes / setup wizard (keeps things in sync)
# You can remove this later if you find boot_session alone is sufficient.

