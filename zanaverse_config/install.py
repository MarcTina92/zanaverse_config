import frappe

def _has_field(doctype: str, fieldname: str) -> bool:
    try:
        return frappe.get_meta(doctype).has_field(fieldname)
    except Exception:
        return False

def _set(ws, fieldname: str, value: str, force: bool = True):
    """Set a Website Settings field; respect 'force' or only fill if empty."""
    if _has_field("Website Settings", fieldname):
        if force or not ws.get(fieldname):
            ws.set(fieldname, value)

def apply_branding(force: bool = True):
    """Apply Zanaverse SaaS branding on every migrate."""
    ws = frappe.get_doc("Website Settings", "Website Settings")

    # core brand
    _set(ws, "app_name", "ZanaVerse", force=force)
    _set(ws, "app_logo", "/assets/zanaverse_config/images/logo.svg", force=force)
    _set(ws, "footer_logo", "/assets/zanaverse_config/images/footer-logo.svg", force=force)
    _set(ws, "favicon", "/assets/zanaverse_config/images/favicon.png?v=4", force=force)
    _set(ws, "banner_image", "/assets/zanaverse_config/images/banner.png", force=force)

    # navbar brand HTML (controls top-left brand in many themes)
    if _has_field("Website Settings", "brand_html"):
        brand_html = '<img src="/assets/zanaverse_config/images/logo.svg" alt="ZanaSchools" style="height:22px;vertical-align:middle">'
        if force or not ws.get("brand_html"):
            ws.brand_html = brand_html

    ws.save()
    frappe.db.commit()
