import frappe

def set_default_footer():
    """Set default email footer so new sites don't show 'Sent via ERPNext'."""
    try:
        frappe.db.set_single_value(
            "System Settings",
            "email_footer_address",
            "— Sent via Zanaverse ERP"
        )
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Zanaverse: set_default_footer failed")
