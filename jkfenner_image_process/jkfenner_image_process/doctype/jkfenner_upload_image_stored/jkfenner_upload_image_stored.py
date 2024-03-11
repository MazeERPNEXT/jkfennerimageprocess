# Copyright (c) 2024, muthukumarmazeworks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta


class JKFennerUploadImageStored(Document):
	pass
def delete_expired_data():
    # Define the date 2 days ago
    two_days_ago = datetime.now() - timedelta(days=2)
    
    # Query and delete the stored data older than two days
    frappe.db.sql("""DELETE FROM `tabJKFenner Upload Image Stored`
                     WHERE creation < %s""", two_days_ago)