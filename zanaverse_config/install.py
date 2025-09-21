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

# ---------------------- onboarding preference (Zana wins) ----------------------

def _is_zana(docname: str) -> bool:
    dn = (docname or "").strip().lower()
    return dn.startswith(("zana", "zanaverse"))

def apply_onboarding_whitelabel() -> dict:
    """
    Prefer Zana/Zanaverse Module Onboarding over stock ones.
    If a Zana variant exists for a module, mark all non-Zana as complete (hidden)
    and ensure the Zana one remains incomplete (visible).

    Idempotent and tolerant of schema differences across stacks.
    """
    if not frappe.db.table_exists("Module Onboarding"):
        return {"skipped": True, "reason": "no Module Onboarding table"}

    meta = frappe.get_meta("Module Onboarding")
    has_is_complete = getattr(meta, "has_field", None) and meta.has_field("is_complete")
    if not has_is_complete:
        return {"skipped": True, "reason": "field is_complete missing"}

    rows = frappe.get_all(
        "Module Onboarding",
        fields=["name", "module", "title", "is_complete"],
        order_by="module asc, modified desc",
    )

    by_module = {}
    for r in rows:
        by_module.setdefault(r.get("module") or "", []).append(r)

    changed = False
    toggled = {"enabled": [], "disabled": []}

    for module, docs in by_module.items():
        zana_docs = [d for d in docs if _is_zana(d.get("name") or d.get("title") or "")]
        if not zana_docs:
            continue

        preferred = zana_docs[0]

        if preferred.get("is_complete"):
            try:
                frappe.db.set_value(
                    "Module Onboarding", preferred["name"], "is_complete", 0, update_modified=False
                )
                toggled["enabled"].append(preferred["name"])
                changed = True
            except Exception:
                pass

        for d in docs:
            if d["name"] == preferred["name"]:
                continue
            if not _is_zana(d.get("name") or d.get("title") or ""):
                if not d.get("is_complete"):
                    try:
                        frappe.db.set_value(
                            "Module Onboarding", d["name"], "is_complete", 1, update_modified=False
                        )
                        toggled["disabled"].append(d["name"])
                        changed = True
                    except Exception:
                        pass

    if changed:
        frappe.db.commit()

    return {"changed": changed, **toggled}

# ---------------------- workspace tagging ----------------------

# Add any baseline workspaces you always ship
CURATED_WORKSPACES = [
    "Home",
    "Zanaverse Home",
    "Admin",
    "Wiki",
    "Support",   # corrected from "ZanaSupport"
]

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
                    w = frappe.get_doc("Workspace", name)
                    w.label = w.label or name
                    w.title = w.title or w.label
                    w.module = "Zanaverse Config"
                    w.save(ignore_permissions=True)
                except Exception:
                    frappe.db.set_value("Workspace", name, "module", "Zanaverse Config", update_modified=False)
                updated.append(name)

    if updated:
        frappe.db.commit()
    return updated

# ---------------------- baseline workspace visibility ----------------------

BASELINE_HIDE = {
    "Build", "Users", "Tools", "ERPNext Settings",
    "ERPNext Integrations", "Welcome Workspace",
}

def apply_workspace_visibility_baseline() -> dict:
    """
    One-time baseline: hide a small set of platform workspaces and unhide others.
    Idempotent (guarded by a site_config flag) and safe across schema variants.
    """
    if not frappe.db.table_exists("Workspace"):
        return {"skipped": True, "reason": "no Workspace doctype"}

    init_key = "zanaverse_workspace_baseline_applied"
    conf = frappe.get_conf() or {}
    if conf.get(init_key):
        return {"skipped": True, "reason": "already applied"}

    changed = False
    touched = {"hidden": [], "shown": []}

    for r in frappe.get_all("Workspace", fields=["name", "is_hidden"]):
        name = r["name"]
        try:
            if name in BASELINE_HIDE:
                frappe.db.set_value("Workspace", name, {"is_hidden": 1, "public": 1}, update_modified=False)
                touched["hidden"].append(name); changed = True
            else:
                if r.get("is_hidden"):
                    frappe.db.set_value("Workspace", name, {"is_hidden": 0, "public": 1}, update_modified=False)
                    touched["shown"].append(name); changed = True
        except Exception:
            pass

    if changed:
        frappe.db.commit()

    try:
        from frappe.installer import update_site_config
        update_site_config(init_key, True)
    except Exception:
        frappe.conf.update({init_key: True})

    return {"changed": changed, **touched}

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

# ---------------------- whitelabel invariants (self-healing) ----------------------

TRANSLATIONS = {
    ("en", "Helpdesk"): "ZanaHelpdesk",
    ("en", "Support"): "ZanaSupport",
    ("en", "ERPNext Settings"): "Zana Settings",
    ("en", "ERPNext Integrations"): "Zana Integrations",
}

WS_TARGETS = {
    "Zanaverse Home":        {"public": 1, "is_hidden": 0, "sequence_id": 1},
    "Home":                  {"public": 0, "is_hidden": 1, "sequence_id": 99},
    "Admin":                 {"public": 0, "is_hidden": 0, "sequence_id": 2},
    "Wiki":                  {"public": 1, "is_hidden": 0, "sequence_id": 3},
    "Helpdesk":              {"public": 1, "is_hidden": 0, "sequence_id": 4},
    "Support":               {"public": 1, "is_hidden": 0, "sequence_id": 5},
    "ERPNext Settings":      {"public": 0, "is_hidden": 0, "sequence_id": 30},
    "ERPNext Integrations":  {"public": 0, "is_hidden": 0, "sequence_id": 32},
}

ADMIN_WS = ("Admin", "ERPNext Settings", "ERPNext Integrations")

def _upsert_translation(lang: str, src: str, dst: str):
    """Idempotently set a translation and dedupe any duplicates."""
    if not frappe.db.table_exists("Translation"):
        return
    rows = frappe.get_all("Translation", filters={"language": lang, "source_text": src}, pluck="name")
    if rows:
        keep = rows[0]
        doc = frappe.get_doc("Translation", keep)
        if getattr(doc, "translated_text", None) != dst:
            doc.translated_text = dst
            doc.save()
        for name in rows[1:]:
            frappe.delete_doc("Translation", name)
    else:
        frappe.get_doc({
            "doctype": "Translation",
            "language": lang,
            "source_text": src,
            "translated_text": dst,
        }).insert(ignore_permissions=True)

def _set_ws(name: str, **vals):
    """Safely enforce workspace flags/order + admin role without revalidating links."""
    if not frappe.db.table_exists("Workspace") or not frappe.db.exists("Workspace", name):
        return

    # update simple flags without full doc save (avoids link validation)
    updatable = ("public", "is_hidden", "sequence_id")
    for k in updatable:
        if k in vals:
            try:
                frappe.db.set_value("Workspace", name, k, vals[k], update_modified=False)
            except Exception:
                pass

    # ensure System Manager role via child row insert (no parent save)
    if name in ADMIN_WS and frappe.db.table_exists("Workspace Role"):
        if not frappe.db.exists("Workspace Role", {"parent": name, "role": "System Manager"}):
            import uuid
            frappe.db.sql("""
                INSERT INTO `tabWorkspace Role`
                    (name, creation, modified, owner, docstatus,
                     parent, parenttype, parentfield, idx, role)
                VALUES
                    (%s, NOW(), NOW(), %s, 0,
                     %s, 'Workspace', 'roles', 1, %s)
            """, (str(uuid.uuid4()), "Administrator", name, "System Manager"))

def ensure_whitelabel_baseline() -> dict:
    """
    Enforce translations + canonical workspaces on every migrate.
    Safe to run repeatedly (idempotent). Keeps prod/dev/client stacks in sync.
    """
    for (lang, src), dst in TRANSLATIONS.items():
        _upsert_translation(lang, src, dst)

    for name, vals in WS_TARGETS.items():
        _set_ws(name, **vals)

    frappe.db.commit()
    return {"status": "ok", "translations": len(TRANSLATIONS), "workspaces": len(WS_TARGETS)}

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

    try:
        from frappe.installer import update_site_config
    except Exception:
        update_site_config = None

    if update_site_config:
        update_site_config(init_key, True)
    else:
        frappe.conf.update({init_key: True})

    return {"initialized": True, "changed": changed, "force": True, "workspaces": ws_updated}
