# zanaverse_config/install.py
import frappe

# ---------------------- small helpers ----------------------

def asbool(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return bool(v)
    if isinstance(v, str): return v.strip().lower() in {"1", "true", "yes", "on"}
    return False

def _logo_path() -> str:
    """Single source of truth for your logo everywhere."""
    return "/assets/zanaverse_config/images/zv-logo.png?v=2"

# ---------------------- workspace tagging ----------------------

# Add any baseline workspaces you always ship
CURATED_WORKSPACES = ["Home", "Zanaverse Home", "Admin"]

def _tag_workspace_module():
    """
    Ensure curated Workspaces have module='Zanaverse Config'.
    Idempotent: only writes when a value differs.
    Gracefully skips if 'module' field doesn't exist on this build.
    """
    updated = []
    if not frappe.db.table_exists("Workspace"):
        return updated

    meta = frappe.get_meta("Workspace")
    has_module_field = getattr(meta, "has_field", None) and meta.has_field("module")

    for name in CURATED_WORKSPACES:
        if not frappe.db.exists("Workspace", name):
            continue
        w = frappe.get_doc("Workspace", name)

        # ensure label/title are never empty (defensive)
        w.label = w.label or name
        w.title = w.title or w.label

        if has_module_field and getattr(w, "module", None) != "Zanaverse Config":
            w.module = "Zanaverse Config"
            w.save(ignore_permissions=True)
            updated.append(name)

    if updated:
        frappe.db.commit()
    return updated

# ---------------------- branding writer ----------------------

def _write_branding(*, force: bool) -> bool:
    """
    Write branding fields. If force=False, only seed when empty.
    Only touches Website Settings; keep this focused.
    """
    if not frappe.db.exists("Website Settings", "Website Settings"):
        return False

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

    # Only branding-related fields (tight, predictable)
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

# ---------------------- public entry points ----------------------

def apply_branding() -> dict:
    """
    Run on migrate (and manually). Enforce when locked; otherwise only seed empties.
    Also auto-tags curated Workspaces with module='Zanaverse Config' so
    your module-based fixtures pick them up.
    """
    locked = asbool((frappe.get_conf() or {}).get("zanaverse_branding_locked", True))
    changed = _write_branding(force=locked)
    ws_updated = _tag_workspace_module()
    return {"changed": changed, "force": locked, "workspaces": ws_updated}

def apply_branding_first_time() -> dict:
    """
    Run once after install to guarantee an initial Zanaverse brand,
    then mark a site flag so we don’t reseed unnecessarily.
    Always calls workspace tagging (idempotent).
    """
    conf = frappe.get_conf() or {}
    init_key = "zanaverse_branding_initialized"

    if asbool(conf.get(init_key)):
        ws_updated = _tag_workspace_module()
        return {"initialized": False, "changed": False, "force": False, "workspaces": ws_updated}

    changed = _write_branding(force=True)
    ws_updated = _tag_workspace_module()

    # Persist the initialization flag in site_config.json
    try:
        from frappe.installer import update_site_config
    except Exception:
        update_site_config = None

    if update_site_config:
        update_site_config(init_key, True)
    else:
        # Safe fallback: update in-memory conf (will persist when site config is next written)
        frappe.conf.update({init_key: True})

    return {"initialized": True, "changed": changed, "force": True, "workspaces": ws_updated}
