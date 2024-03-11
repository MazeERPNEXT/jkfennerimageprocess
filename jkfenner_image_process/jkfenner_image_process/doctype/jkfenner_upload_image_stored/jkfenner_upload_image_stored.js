// Copyright (c) 2024, muthukumarmazeworks and contributors
// For license information, please see license.txt

frappe.ui.form.on("JKFenner Upload Image Stored", {
    refresh(frm) {
        // Check and delete records older than 2 days
        deleteOldRecords();
    }
});

function deleteOldRecords() {
    frappe.db.delete('JKFenner Upload Image Stored', {
        filters: {
            creation: ['<=', frappe.datetime.add_days(frappe.datetime.now_datetime(), -2)]
        }
    })
    .then(() => {
        console.log('Old records deleted successfully.');
    })
    .catch(err => {
        console.error('Error deleting old records:', err);
    });
}
