# Copyright (c) 2023, muthukumarmazeworks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JKFennerImageAI(Document):
	pass

@frappe.whitelist()
def get_hose_by_id(row_id):
    hoses = ['HOSE A', 'HOSE B', 'HOSE C', 'HOSE D', 'HOSE E']  # Add more hoses as needed
    hose_index = int(row_id) - 1
    if hose_index < len(hoses):
        return hoses[hose_index]
    else:
        return None
    
# def set_default_values(doc, method):
#     if not doc.product_dimensions_section:
#         return
#     for row in doc.product_dimensions_section:
#         # Set default value for inner_diameter_1_with_units if inner_diameter_1 is present
#         if row.inner_diameter_1 and not row.inner_diameter_1_with_units:
#             row.inner_diameter_1_with_units = f"{row.inner_diameter_1} mm"

# # Hook the function to the after_insert event
# def register_hook():
#     frappe.get_doc('JKfennerImageProcess.JKFennerImageAI.JKFennerImageAI').add_after_insert(set_default_values)

# # Call the function to register the hook
# register_hook()