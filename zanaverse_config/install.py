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

# zanaverse_config/install.py
def _tag_workspace_module():
    """
    Ensure curated Workspaces have module='Zanaverse Config'.
    Idempotent and robust: will fall back to db.set_value if needed.
    """
    updated = []
    if not frappe.db.table_exists("Workspace"):
        return updated

    try:
        meta = frappe.get_meta("Workspace")
        # be defensive: treat as present unless we can prove otherwise
        has_module_field = True
        if getattr(meta, "has_field", None):
            has_module_field = meta.has_field("module")
    except Exception:
        has_module_field = True

    for name in CURATED_WORKSPACES:
        if not frappe.db.exists("Workspace", name):
            continue

        if has_module_field:
            current = frappe.get_value("Workspace", name, "module")
            if current != "Zanaverse Config":
                try:
                    # try the clean path first
                    w = frappe.get_doc("Workspace", name)
                    w.label = w.label or name
                    w.title = w.title or w.label
                    w.module = "Zanaverse Config"
                    w.save(ignore_permissions=True)
                except Exception:
                    # fall back to direct write if save path rejects it
                    frappe.db.set_value("Workspace", name, "module", "Zanaverse Config", update_modified=False)
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

def apply_email_footer(force=True):
    """Set a simple global email footer, but only on stacks that support it."""
    try:
        meta = frappe.get_meta("System Settings")
    except Exception:
        return {"changed": False, "skipped": True, "reason": "no System Settings meta"}

    # older/newer stacks may not have this field
    has_field = getattr(meta, "has_field", None)
    if has_field and not meta.has_field("email_footer"):
        return {"changed": False, "skipped": True, "reason": "email_footer field missing"}

    try:
        ss = frappe.get_single("System Settings")
    except Exception:
        return {"changed": False, "skipped": True, "reason": "cannot load System Settings"}

    if not hasattr(ss, "email_footer"):
        return {"changed": False, "skipped": True, "reason": "email_footer attr missing"}

    footer_html = """
    <div style="color:#6b7280;font-size:12px;line-height:1.6;margin-top:12px">
      <strong>Zanaverse</strong><br>
      <a href="https://zanaverse.io" style="color:#6b7280;text-decoration:underline">zanaverse.io</a>
    </div>
    """.strip()

    changed = False
    current = getattr(ss, "email_footer", None)
    if force or not current:
        if current != footer_html:
            ss.email_footer = footer_html
            changed = True

    if changed:
        ss.save(ignore_permissions=True)
        frappe.db.commit()
    return {"changed": changed, "skipped": False}

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
