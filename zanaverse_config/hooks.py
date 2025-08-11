app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

# Only depends on Frappe
required_apps = ["frappe"]

# Branding-only fixtures
fixtures = [
    {"dt": "Website Settings"},
    {"dt": "Portal Settings"},
    {"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]},
    {"dt": "Navbar Item",  "filters": [["item_label", "like", "Zana%"]]},
    {"dt": "Letter Head",  "filters": [["name", "like", "Zana%"]]},
    {"dt": "Web Page",     "filters": [["name", "in", ["Home","home"]]]},
]

# Optional: make portal default_role safe if role exists
after_install = "zanaverse_config.install.after_install"
after_migrate = "zanaverse_config.install.after_migrate"
