# zanaverse_config/hooks.py
# -*- coding: utf-8 -*-
app_name = "zanaverse_config"
app_title = "Zanaverse"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# === Include your brand assets on Desk & Website ===
# Ensure these files actually exist in your built assets; otherwise comment them out.
app_include_js = ["assets/zanaverse_config/js/brand.js",    
 "assets/zanaverse_config/js/crm_kill_onboarding.js",
]
web_include_js = ["assets/zanaverse_config/js/brand.js"]
# app_include_css = ["assets/zanaverse_config/css/brand.css"]

# === Fixtures ===
fixtures = [
    {
        "doctype": "Workspace",
        "filters": [["name", "in", [
            "Zanaverse Home", "Home", "Admin", "Wiki", "Helpdesk", "Support",
            "ERPNext Settings", "ERPNext Integrations",
        ]]],
    },
    {"doctype": "Workspace", "filters": [["module", "=", "Zanaverse Config"]]},
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
        "Welcome - Zanaverse (Default)", 
    ]]]},
]

# === Dynamic branding: these must point to real callables ===
app_logo_url = "zanaverse_config.brand.app_logo_url"
brand_html   = "zanaverse_config.brand.brand_html"

# === Hooks ===
after_install = [
    "zanaverse_config.install.apply_branding_first_time",
    "zanaverse_config.install.apply_workspace_visibility_baseline",
    "zanaverse_config.brand.set_global_footer",          # <-- use brand.py
    "zanaverse_config.brand.apply_crm_brand", 
    "zanaverse_config.install.apply_welcome_template",
    "zanaverse_config.hardening.disable_onboarding_if_config",          # ← add
]
after_migrate = [
    "zanaverse_config.install.apply_branding",
    "zanaverse_config.install.apply_email_footer",
    "zanaverse_config.install.apply_onboarding_whitelabel",
    "zanaverse_config.install.ensure_whitelabel_baseline",
    "zanaverse_config.brand.enforce_global_footer",      # <-- use brand.py
    "zanaverse_config.brand.apply_crm_brand", 
    "zanaverse_config.install.apply_welcome_template",          # ← add
    "zanaverse_config.hardening.disable_onboarding_if_config",
]

update_website_context = "zanaverse_config.brand.update_website_context"
boot_session = "zanaverse_config.brand.boot_session"

website_context = {
    "brand_html": "Zanaverse",
    "favicon": "/assets/zanaverse_config/favicon.png",
    "splash_image": "/assets/zanaverse_config/logo.svg",
}

scheduler_events = {
    "daily": ["zanaverse_config.brand.enforce_global_footer",  # <-- use brand.py
    "zanaverse_config.brand.apply_crm_brand",] 
}
