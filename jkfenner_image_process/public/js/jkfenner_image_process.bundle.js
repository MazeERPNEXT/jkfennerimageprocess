frappe.listview_settings['File']={
	before_render: function () {

		if(cur_list.$delete_folder_button == undefined){
			let cur_page = cur_list.page;

		cur_list.$delete_folder_button = cur_page
			.add_button(__("Delete Folders"), () => {
				let checkedItems = cur_list.get_checked_items();
				let fileIDs = checkedItems.map(c => c.name);
				let deleteFiles = async (fileIDs) => {
					let response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.delete_folders', {folder_ids: fileIDs})
					cur_list.refresh();
				}
				deleteFiles(fileIDs);
			})
			.hide();
		
		cur_list.$delete_files_button = cur_page
			.add_button(__("Delete Files"), () => {
				let checkedItems = cur_list.get_checked_items();
				let fileIDs = checkedItems.map(c => c.name);
				let deleteFiles = async (fileIDs) => {
					let actions_menu_items = cur_list.get_actions_menu_items();
					let delete_action = actions_menu_items[actions_menu_items.length - 1].action;
					delete_action();
				}
				deleteFiles(fileIDs);
			})
			.hide();

		cur_list.toggle_folder_delete_buttons = () => {
			const hide_delete_btn = !(cur_list.$checks && cur_list.$checks.length > 0);
			cur_list.$delete_folder_button.toggle(!hide_delete_btn);
			cur_list.$delete_files_button.toggle(!hide_delete_btn);
		}
		old_on_row_checked = cur_list.on_row_checked
		cur_list.on_row_checked = () => {
			old_on_row_checked.apply(cur_list)
			cur_list.toggle_folder_delete_buttons();
		}
		}
	}
}
