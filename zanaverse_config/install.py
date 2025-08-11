# zanaverse_config/install.py
from __future__ import annotations

import frappe
from frappe.installer import update_site_config


def asbool(v) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        return v.strip().lower() in {"1", "true", "yes", "on"}
    return False


def apply_branding(force: bool | None = None):
    """
    Apply Zanaverse default branding to Website Settings.

    Behavior:
      - If `force` is True  -> always overwrite (SaaS/default).
      - If `force` is False -> only seed empty fields (client can customize).
      - If `force` is None  -> read site config key `zanaverse_branding_locked`
                               (defaults True) to decide.
    """
    ws = frappe.get_doc("Website Settings", "Website Settings")

    if force is None:
        locked = asbool(frappe.get_conf().get("zanaverse_branding_locked", True))
    else:
        locked = bool(force)

    changed = False

    def _set(field: str, value: str):
        nonlocal changed
        # If locked, always write. If unlocked, only seed when field is empty.
        current = ws.get(field)
        if locked or not current:
            if current != value:
                ws.set(field, value)
                changed = True

    # ---- Zanaverse defaults ----
    _set("app_name", "Zanaverse")
    _set("app_logo", "/assets/zanaverse_config/images/logo.svg?v=1")
    _set("footer_logo", "/assets/zanaverse_config/images/footer-logo.svg?v=1")
    _set("favicon", "/assets/zanaverse_config/images/favicon.png?v=4")
    _set("banner_image", "/assets/zanaverse_config/images/banner.png?v=1")
    _set(
        "brand_html",
        '<img src="/assets/zanaverse_config/images/logo.svg?v=1" '
        'alt="Zanaverse" style="height:22px;vertical-align:middle" />',
    )

    if changed:
        ws.save(ignore_permissions=True)
        frappe.db.commit()

    return {"changed": changed, "force": locked}


def apply_branding_first_time():
    """
    One-time brand enforcement on first install.
    Sets a site flag so subsequent installs/migrates don’t re-force unless
    `zanaverse_branding_locked` is True.
    """
    if asbool(frappe.get_conf().get("zanaverse_branding_initialized")):
        return {"initialized": True, "skipped": True}

    out = apply_branding(force=True)
    update_site_config("zanaverse_branding_initialized", True)
    return {"initialized": True, **(out or {})}
