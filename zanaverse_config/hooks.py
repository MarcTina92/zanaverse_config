# -*- coding: utf-8 -*-
app_name = "zanaverse_config"
app_title = "Zanaverse"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# === Include your brand assets on Desk & Website ===
app_include_js = ["assets/zanaverse_config/js/brand.js"]
#app_include_css = ["assets/zanaverse_config/css/brand.css"]

# === Fixtures (standardise to `dt`, remove duplicates) ===
fixtures = [
    {"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Zanaverse Config"]]},
    {"dt": "Workspace", "filters": [["name", "=", "Home"]]},
    {"dt": "Navbar Settings"},
    {"dt": "Website Settings"},
    {"dt": "Number Card", "filters": [["module", "=", "Zanaverse Config"]]},
    {"dt": "Dashboard", "filters": [["module", "=", "Zanaverse Config"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Zanaverse Config"]]},
        # 👇 Add these so white-labeled onboarding gets exported
    {"dt": "Onboarding Step"},
    {"dt": "Module Onboarding"},

    # Translations: grab all your EN overrides (non-contributed)
    {"dt": "Translation", "filters": [["language", "=", "en"]]},
    # Email templates you care about
    {"dt": "Email Template", "filters": [["name", "in", [
        "Exit Questionnaire Notification",
        "Interview Feedback Reminder",
        "Interview Reminder",
        "Leave Status Notification",
        "Leave Approval Notification",
    ]]]},
]

# === Dynamic branding (you already had these) ===
app_logo_url = "zanaverse_config.brand.app_logo_url"
brand_html   = "zanaverse_config.brand.brand_html"

after_install = "zanaverse_config.install.apply_branding_first_time"
after_migrate = [
    "zanaverse_config.install.apply_branding",
    "zanaverse_config.install.apply_email_footer",
]

update_website_context = "zanaverse_config.brand.update_website_context"
boot_session = "zanaverse_config.brand.boot_session"

# Fallbacks while dynamic hooks run
website_context = {
    "brand_html": "Zanaverse",
    "favicon": "/assets/zanaverse_config/favicon.png",
    "splash_image": "/assets/zanaverse_config/logo.svg",
}
