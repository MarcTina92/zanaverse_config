app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"


# Only keep what you truly need as fixtures (e.g., your theme)
fixtures = [
    {"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]},
]

after_install = "zanaverse_config.install.apply_branding"
after_migrate = "zanaverse_config.install.apply_branding"
