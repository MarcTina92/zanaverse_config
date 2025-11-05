import frappe

def _asbool(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return bool(v)
    if isinstance(v, str): return v.strip().lower() in {"1", "true", "yes", "on"}
    return False

def _set_single(dt, field, val):
    try:
        if not frappe.db.exists("DocType", dt):
            return
        doc = frappe.get_single(dt)
        if hasattr(doc, field) and getattr(doc, field) != val:
            setattr(doc, field, val)
            doc.save(ignore_permissions=True)
    except Exception:
        # be quiet on stacks where the doctype/field doesn’t exist
        pass

def _flip_flags(dt):
    if not frappe.db.table_exists(dt):
        return 0
    try:
        fns = {f.fieldname for f in frappe.get_meta(dt).fields}
    except Exception:
        return 0
    touched = 0
    for name in frappe.get_all(dt, pluck="name"):
        try:
            d = frappe.get_doc(dt, name)
            dirty = False
            for f in ("is_complete", "is_skipped", "is_dismissed", "disabled"):
                if f in fns and getattr(d, f, None) != 1:
                    setattr(d, f, 1); dirty = True
            for f in ("is_active", "show_onboarding", "enable_getting_started"):
                if f in fns and getattr(d, f, None) != 0:
                    setattr(d, f, 0); dirty = True
            if dirty:
                d.save(ignore_permissions=True); touched += 1
        except Exception:
            continue
    return touched

def _remove_help_links():
    # Navbar Settings (fields vary by version)
    try:
        if frappe.db.exists("DocType", "Navbar Settings"):
            ns = frappe.get_doc("Navbar Settings", "Navbar Settings")
            bad_labels = ("help", "docs", "documentation", "developer")
            bad_urls   = ("frappeframework.com", "frappe.io/docs", "/docs")
            def keep(items):
                out = []
                for i in (items or []):
                    label = (getattr(i, "label", "") or "").lower()
                    url   = (getattr(i, "url", "") or "").lower()
                    if any(w in label for w in bad_labels): continue
                    if any(w in url   for w in bad_urls):   continue
                    out.append(i)
                return out
            if hasattr(ns, "top_bar_items"): ns.top_bar_items = keep(ns.top_bar_items)
            if hasattr(ns, "footer_items"):  ns.footer_items  = keep(ns.footer_items)
            if hasattr(ns, "help_menu"):     ns.help_menu     = []
            ns.save(ignore_permissions=True)
    except Exception:
        pass

    # Portal Menu Item (schema differs across versions)
    try:
        if frappe.db.table_exists("Portal Menu Item"):
            meta = frappe.get_meta("Portal Menu Item")
            has_url   = any(f.fieldname == "url" for f in meta.fields)
            has_route = any(f.fieldname == "route" for f in meta.fields)
            fields = ["name", "title", "enabled"]
            if has_url:   fields.append("url")
            if has_route: fields.append("route")
            bad_words = ("help", "docs", "documentation", "developer")
            bad_urls  = ("frappeframework.com", "frappe.io/docs", "/docs")
            for r in frappe.get_all("Portal Menu Item", fields=fields):
                title = (r.get("title") or "").lower()
                link  = (r.get("url") or "") if has_url else ""
                link  = link or ((r.get("route") or "") if has_route else "")
                lwr   = (link or "").lower()
                if any(w in title for w in bad_words) or any(w in lwr for w in bad_urls):
                    try:
                        doc = frappe.get_doc("Portal Menu Item", r["name"])
                        doc.enabled = 0
                        doc.save(ignore_permissions=True)
                    except Exception:
                        continue
    except Exception:
        pass

def disable_onboarding_if_config():
    # explicit enable overrides the disable flag
    if _asbool(frappe.conf.get("zanaverse_enable_onboarding", 0)):
        return
    if not _asbool(frappe.conf.get("zanaverse_disable_onboarding", 1)):
        return

    # Global toggles (silently skip when absent)
    _set_single("Desk Settings",   "disable_onboarding", 1)
    _set_single("System Settings", "disable_onboarding", 1)
    _set_single("CRM Settings",    "show_onboarding", 0)
    _set_single("CRM Settings",    "enable_getting_started", 0)

    # Flip records that drive the right-side “Getting started” & tours
    for dt in ("Module Onboarding", "Onboarding", "App Tour"):
        _flip_flags(dt)

    # Scrub help/docs links so users don’t leak to stock sites
    _remove_help_links()

    # Make effects immediate
    frappe.clear_cache()
    frappe.db.commit()
