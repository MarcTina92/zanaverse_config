# -*- coding: utf-8 -*-
app_name = "zanaverse_config"
app_title = "Zanaverse"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# === Include your brand assets on Desk & Website ===
app_include_js = ["assets/zanaverse_config/js/brand.js"]
web_include_js = ["assets/zanaverse_config/js/brand.js"]
#app_include_css = ["assets/zanaverse_config/css/brand.css"]

# === Fixtures (standardise to `dt`, remove duplicates) ===
fixtures = [
    # Canonical sidebar (explicit names)
    {
        "doctype": "Workspace",
        "filters": [["name", "in", [
            "Zanaverse Home", "Home", "Admin", "Wiki", "Helpdesk", "Support",
            "ERPNext Settings", "ERPNext Integrations",
        ]]],
    },
    # Also include all workspaces in your app module (future Zana-specific pages)
    {"doctype": "Workspace", "filters": [["module", "=", "Zanaverse Config"]]},

    # Navbar / Themes / Dashboards / Onboarding / Translations / Email Templates
    {"doctype": "Navbar Settings"},
    {"doctype": "Website Theme", "filters": [["name", "like", "Zana%"]]},
    {"doctype": "Number Card", "filters": [["module", "=", "Zanaverse Config"]]},
    {"doctype": "Dashboard", "filters": [["module", "=", "Zanaverse Config"]]},
    {"doctype": "Dashboard Chart", "filters": [["module", "=", "Zanaverse Config"]]},
    {"doctype": "Onboarding Step", "filters": [["name", "like", "Zana %"]]},
    {"doctype": "Module Onboarding", "filters": [["name", "like", "Zana %"]]},
    {"doctype": "Translation", "filters": [["language", "=", "en"]]},
    {"doctype": "Email Template", "filters": [["name", "in", [
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


after_install = [
    "zanaverse_config.install.apply_branding_first_time",
    "zanaverse_config.install.apply_workspace_visibility_baseline",  # ← add this
]
after_migrate = [
    "zanaverse_config.install.apply_branding",
    "zanaverse_config.install.apply_email_footer",
    "zanaverse_config.install.apply_onboarding_whitelabel", 
    "zanaverse_config.install.ensure_whitelabel_baseline",
]

update_website_context = "zanaverse_config.brand.update_website_context"
boot_session = "zanaverse_config.brand.boot_session"

# Fallbacks while dynamic hooks run
website_context = {
    "brand_html": "Zanaverse",
    "favicon": "/assets/zanaverse_config/favicon.png",
    "splash_image": "/assets/zanaverse_config/logo.svg",
}
