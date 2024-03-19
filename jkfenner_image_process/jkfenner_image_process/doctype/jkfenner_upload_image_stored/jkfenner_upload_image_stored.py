# Copyright (c) 2024, muthukumarmazeworks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now


class JKFennerUploadImageStored(Document):
	
    @staticmethod
    def clear_old_logs(days=2):
        records_to_delete = frappe.get_list("JKFenner Upload Image Stored",
                                            filters = {"modified" : ("<", Now() - Interval(days=days))},
                                            fields=["name","filr_url"])
        for record in records_to_delete:
             frappe.delete_doc("JKFenner Upload Image Stored", record["name"])

             if record["file_url"]:
                  file_name = record["file_url"].split("/")[-1]
                  file_doc = frappe.get_doc("File", {"file_name": file_name})
                  if file_doc:
                       frappe.delete_doc("File", file_doc.name)

@frappe.whitelist()
def clear_error_logs():
	"""Flush all Error Logs"""
	frappe.only_for("System Manager")
	frappe.db.truncate("JKFenner Upload Image Stored")