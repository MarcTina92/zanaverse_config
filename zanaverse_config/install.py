# zanaverse_config/install.py

import frappe

def apply_branding():
    # ---- per-site escape hatch ----
    # If this is set in site_config.json, we won't touch branding on this site.
    if frappe.conf.get("zanaverse_keep_custom_branding"):
        frappe.logger("zanaverse_config").info(
            "Branding skipped: zanaverse_keep_custom_branding=true"
        )
        return

    """Force Zanaverse branding on the site."""
    ws = frappe.get_doc("Website Settings", "Website Settings")

    _set(ws, "app_name", "Zanaverse", force=force)
    _set(ws, "app_logo", "/assets/zanaverse_config/images/logo.svg?v=1", force=force)
    _set(ws, "footer_logo", "/assets/zanaverse_config/images/footer-logo.svg?v=1", force=force)
    _set(ws, "favicon", "/assets/zanaverse_config/images/favicon.png?v=4", force=force)
    _set(ws, "banner_image", "/assets/zanaverse_config/images/banner.png?v=1", force=force)

    brand_html = (
        '<img src="/assets/zanaverse_config/images/logo.svg?v=1" '
        'alt="Zanaverse" style="height:22px;vertical-align:middle">'
    )
    _set(ws, "brand_html", brand_html, force=force)

    ws.save()
    frappe.db.commit()
