// Copyright (c) 2023, muthukumarmazeworks and contributors
// For license information, please see license.txt

frappe.ui.form.on('JKFenner Image AI', {
	refresh: function (frm, cdt, cdn) {
		// frappe.call({
		// 	method: 'jkfenner_image_process.jkfenner_image_process.jkfenner_image_process.jkfenner_image_ai.get_timeline_html',
		// 	callback: function (res) {
		// 		var template = res.message;
		// 		frm.set_df_property('html_fieldname', 'options', frappe.render(template, { rows: [] }));
		// 		frm.refresh_field('html_fieldname');
		// 	}
		// });
	},
	onload: function (frm) {
		// Your onload logic here
	}
});

// frappe.ui.form.on('Target Doctype', 'refresh', function(frm, cdt, cdn){
// 	frappe.call({
// 	  'method': 'frappe.client.get_list',
// 	  'args': {
// 		'doctype': 'Source DocType',
// 		'columns': ['*']
// 		'filters': [['Source DocType', 'link_reference', '=', frm.doc.name]]
// 	  },
// 	  'callback': function(res){
// 		  var template = "<table><tbody>{% for (var row in rows) { %}<tr>{% for (var col in rows[row]) { %}<td>rows[row][col]</td>{% } %}</tr>{% } %}</tbody></table>",
// 		 frm.set_df_property('html_fieldname', 'options', frappe.render(template, {rows: res.message});
// 		 frm.refresh_field('html_fieldname');
// 	  }
// 	})
//  });
