frappe.listview_settings["JKFenner Image AI"] = {
    onload(listview) {
		listview.page.set_secondary_action(__("Data Import"), function(){
			location.href="/app/data-import/new-data-import-1?reference_doctype=JKFenner Image AI&enable_autosave=false"
		});
	}
}