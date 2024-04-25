# Copyright (c) 2024, muthukumarmazeworks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now
from datetime import datetime, timedelta


class JKFennerUploadImageStored(Document):
    
    @staticmethod
    def clear_old_logs(days=1):
        current_datetime = datetime.now()
        cutoff_date = current_datetime - timedelta(days=days)
        records_to_delete = frappe.get_list("JKFenner Upload Image Stored",
                                            filters={"creation": ("<", cutoff_date)},
                                            fields=["name", "upload_image", "foreground_image_url"])
        
        for record in records_to_delete:
            frappe.delete_doc("JKFenner Upload Image Stored", record["name"])

            # Delete associated files for upload_image
            if record["upload_image"]:
                file_urls = record["upload_image"].split(",")
                for file_url in file_urls:
                    file_name = file_url.strip()
                    try:
                         file_doc = frappe.get_doc("File", {"file_url": file_name})
                         if file_doc:
                              frappe.delete_doc("File", file_doc.name)
                    except:
                        pass

            # Delete associated files for foreground_image_url
            if record["foreground_image_url"]:
                file_urls = record["foreground_image_url"].split(",")
                for file_url in file_urls:
                    file_name = file_url.strip()
                    try:
                         file_doc = frappe.get_doc("File", {"file_url": file_name})
                         if file_doc:
                              frappe.delete_doc("File", file_doc.name)
                    except:
                        pass

        frappe.db.commit()

@frappe.whitelist()
def clear_error_logs():
    """Flush all Error Logs"""
    frappe.only_for("System Manager")
    frappe.db.truncate("JKFenner Upload Image Stored")

@frappe.whitelist()
def test_delete_record():
    JKFennerUploadImageStored.clear_old_logs()