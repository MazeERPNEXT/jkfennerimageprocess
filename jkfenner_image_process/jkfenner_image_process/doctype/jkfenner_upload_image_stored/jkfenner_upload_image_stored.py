# Copyright (c) 2024, muthukumarmazeworks and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class JKFennerUploadImageStored(Document):
	pass


# @frappe.whitelist()
# def store_image(image_url):
#     try:
#         image_doc = frappe.get_doc({
#             'doctype': 'JKFenner Upload Image Stored',
#             'upload_image': image_url,
#             'current_datetime': frappe.utils.now_datetime()
#         })
#         image_doc.insert(ignore_permissions=True)
#         frappe.db.commit()
#         return "Image stored successfully."
#     except Exception as e:
#         print(frappe.get_traceback(), "Error storing image")
#         return "Failed to store image: {0}".format(str(e))