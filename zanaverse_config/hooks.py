app_name = "zanaverse_config"
app_title = "Zanaverse Config"
app_publisher = "Zanaverse"
app_description = "Branding and site-level settings (frappe-only)"
app_email = "info@marctinaconsultancy.com"
app_license = "mit"

fixtures = [
    {"dt": "Custom Field", "filters": [["dt","not in", [
        "Sales Invoice","Sales Order","Quotation","Delivery Note","Purchase Order","Purchase Invoice",
        "Purchase Receipt","Item","Customer","Supplier","POS Invoice","Pick List","Material Request",
        "Stock Entry","Stock Reconciliation","Job Card","Packed Item","Stock Entry Detail",
        "Stock Reconciliation Item","Item Barcode","Delivery Note Item","Purchase Receipt Item",
        "Purchase Invoice Item","Sales Invoice Item","POS Invoice Item","Supplier Quotation",
        "Student","Instructor","Course Schedule","Fee Structure"
    ]]]},
    {"dt": "Property Setter", "filters": [["doc_type","not in", [
        "Sales Invoice","Sales Order","Quotation","Delivery Note","Purchase Order","Purchase Invoice",
        "Purchase Receipt","Item","Customer","Supplier","POS Invoice","Pick List","Material Request",
        "Stock Entry","Stock Reconciliation","Job Card","Packed Item","Stock Entry Detail",
        "Stock Reconciliation Item","Item Barcode","Delivery Note Item","Purchase Receipt Item",
        "Purchase Invoice Item","Sales Invoice Item","POS Invoice Item","Supplier Quotation",
        "Student","Instructor","Course Schedule","Fee Structure"
    ]]]},
    {"dt": "Print Format", "filters": [["doc_type","not in", [
        "Sales Invoice","Sales Order","Quotation","Delivery Note","Purchase Order","Purchase Invoice",
        "Purchase Receipt","Item","Customer","Supplier","POS Invoice","Pick List","Material Request",
        "Stock Entry","Stock Reconciliation","Job Card","Packed Item","Stock Entry Detail",
        "Stock Reconciliation Item","Item Barcode","Delivery Note Item","Purchase Receipt Item",
        "Purchase Invoice Item","Sales Invoice Item","POS Invoice Item","Supplier Quotation",
        "Student","Instructor","Course Schedule","Fee Structure"
    ]]]},
    {"dt": "Website Settings"},
    {"dt": "Portal Settings"},
    {"dt": "Website Theme", "filters": [["name", "like", "Zana%"]]},
    {"dt": "Navbar Item", "filters": [["item_label", "like", "Zana%"]]},
    {"dt": "Letter Head", "filters": [["name", "like", "Zana%"]]},
    {"dt": "Web Page", "filters": [["name", "in", ["Home","home"]]]},
]
