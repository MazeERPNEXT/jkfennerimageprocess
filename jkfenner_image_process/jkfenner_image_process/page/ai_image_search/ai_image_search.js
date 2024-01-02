frappe.pages['ai-image-search'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'New Image Search',
		single_column: true
	});

	page.set_title('JK Fenner Image Search')
	// let $btn = page.set_primary_action('Save', function() {
	// 	frm.save("Save", function(){
	// 		send_and_save_todo(frm.doc);
	// 	});
	// });

	$(frappe.render_template("ai_image_search", {})).appendTo(page.body);
	
};



