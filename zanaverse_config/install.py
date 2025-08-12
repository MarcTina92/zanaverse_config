# zanaverse_config/install.py
import frappe

def asbool(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return bool(v)
    if isinstance(v, str): return v.strip().lower() in {"1", "true", "yes", "on"}
    return False

def _logo_path() -> str:
    # Single source of truth for your logo everywhere
    return "/assets/zanaverse_config/images/zv-logo.png?v=2"

def _write_branding(*, force: bool) -> bool:
    """Write branding fields. If force=False, only seed when empty."""
    ws = frappe.get_doc("Website Settings", "Website Settings")
    changed = False

    def _set(field: str, value: str):
        nonlocal changed
        if force or not ws.get(field):
            if ws.get(field) != value:
                ws.set(field, value)
                changed = True

    logo = _logo_path()
    brand_html = f'<img src="{logo}" alt="Zanaverse" style="height:22px;vertical-align:middle">'

    # Keep this list tight: only Website Settings branding-related fields
    _set("app_logo", logo)
    _set("footer_logo", logo)
    _set("favicon", logo)
    _set("banner_image", logo)
    _set("splash_image", logo)
    _set("brand_html", brand_html)

    if changed:
        ws.save(ignore_permissions=True)
        frappe.db.commit()
    return changed

def apply_branding() -> dict:
    """Run on migrate (and manually). Enforce when locked; otherwise only seed empties."""
    locked = asbool(frappe.get_conf().get("zanaverse_branding_locked", True))
    changed = _write_branding(force=locked)
    return {"changed": changed, "force": locked}

def apply_branding_first_time() -> dict:
    """
    Run once after install to guarantee an initial Zanaverse brand.
    Marks a site flag so we don’t reseed again unnecessarily.
    """
    conf = frappe.get_conf() or {}
    init_key = "zanaverse_branding_initialized"
    if asbool(conf.get(init_key)):
        return {"initialized": False, "changed": False, "force": False}

    changed = _write_branding(force=True)

    # Persist the initialization flag in site_config.json
    try:
        from frappe.installer import update_site_config
    except Exception:
        update_site_config = None
    if update_site_config:
        update_site_config(init_key, True)
    else:
        # Safe fallback: write directly if needed
        frappe.conf.update({init_key: True})

    return {"initialized": True, "changed": changed, "force": True}
