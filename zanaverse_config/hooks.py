# -*- coding: utf-8 -*-
app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# Optional fixtures (keep only what you truly need)
fixtures = [{"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]}]

# Desk branding resolves dynamically from Website Settings (works for white-label)
app_logo_url = "zanaverse_config.brand.app_logo_url"
brand_html   = "zanaverse_config.brand.brand_html"

# Seed/enforce at install & after migrate
after_install = "zanaverse_config.install.apply_branding_first_time"
after_migrate = "zanaverse_config.install.apply_branding"


# Website pages (login, forgot, message, error...)
update_website_context = "zanaverse_config.brand.update_website_context"
