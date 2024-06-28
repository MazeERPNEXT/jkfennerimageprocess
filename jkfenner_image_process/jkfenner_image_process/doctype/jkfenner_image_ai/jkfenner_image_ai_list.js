frappe.listview_settings["JKFenner Image AI"] = {
    onload(listview) {
        listview.page.set_secondary_action(__("Data Import"), function() {
            location.href = "/app/data-import/new-data-import-1?reference_doctype=JKFenner Image AI&enable_autosave=false";
        });
    }
};
frappe.listview_settings['JKFenner Image AI'] = {
    hide_name_column: true,
}
// frappe.ui.form.on('JKFenner Image AI', {
//     refresh: function(frm) {
//         // Add custom button to apply the range filter
//         frm.add_custom_button(__('Filter by Length Range'), function() {
//             var dialog = new frappe.ui.Dialog({
//                 title: __('Filter by Length Range'),
//                 fields: [
//                     {
//                         fieldname: 'length',
//                         label: __('Minimum Length'),
//                         fieldtype: 'Float',
//                         reqd: 1  // Make this field mandatory
//                     },
//                     {
//                         fieldname: 'length',
//                         label: __('Maximum Length'),
//                         fieldtype: 'Float',
//                         reqd: 1  // Make this field mandatory
//                     }
//                 ],
//                 primary_action_label: __('Apply'),
//                 primary_action: function() {
//                     var values = dialog.get_values();
//                     if (values.length !== undefined && values.length !== undefined) {
//                         // Apply filter on the child table field based on the length range
//                         frm.set_query('length', function() {
//                             return {
//                                 filters: [
//                                     ['Product Dimensions', 'length_field', '>=', values.length],
//                                     ['Product Dimensions', 'length_field', '<=', values.length]
//                                 ]
//                             };
//                         });
//                         dialog.hide();
//                         frm.refresh_field('length');
//                     } else {
//                         frappe.msgprint(__('Please enter both minimum and maximum lengths.'));
//                     }
//                 }
//             });
//             dialog.show();
//         });
//     }
// });
