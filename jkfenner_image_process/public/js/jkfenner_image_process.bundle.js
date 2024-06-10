frappe.listview_settings['File'] = {
    before_render: function () {
        if (cur_list.$delete_folder_button == undefined) {
            let cur_page = cur_list.page;

            cur_list.$delete_folder_button = cur_page
                .add_button(__("Delete Folders"), () => {
                    let checkedItems = cur_list.get_checked_items();
                    let fileIDs = checkedItems.map(c => c.name);
                    let deleteFiles = async (fileIDs) => {
                        frappe.confirm(
                            __('Are you sure you want to delete the selected folders?'),
                            async () => {
                                frappe.show_progress(__('Deleting Folders...'), 1000, 1000, null, true);
                                let response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.delete_folders', { folder_ids: fileIDs });
                                frappe.hide_progress();
                                if (response) {
                                    frappe.msgprint(__('Folders deleted successfully.'));
                                    cur_list.refresh();
                                }
                                location.reload();
                            }
                        );   
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

            cur_list.$unzip_file = cur_page
                .add_button(__("Unzip and move to batch"), () => {
                    let checkedItems = cur_list.get_checked_items();
                    let fileIDs = checkedItems.map(c => c.name);
                    let unzipFile = async (fileIDs) => {
                        frappe.confirm(
                            __('Are you sure you want to unzip the selected files?'),
                            async () => {
                                frappe.show_progress(__('Unzipping files...'), 100, 100, null, true);
                                let response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.input_zip.unzip', { file_ids: JSON.stringify(fileIDs) });
                                frappe.hide_progress();
                                if (response) {
                                    frappe.msgprint(__('Files unzipped successfully.'));
                                    // Remove the files from the list view
                                    for (let id of fileIDs) {
                                        cur_list.data.some((file, index) => {
                                            if (file.name === id) {
                                                cur_list.data.splice(index, 1);
                                                return true; // break out of the loop
                                            }
                                        });
                                    }
                                    cur_list.render();
                                }
                                location.reload();
                            }
                        );
                    }
                    unzipFile(fileIDs);
                })
                .hide();

            cur_list.toggle_folder_delete_buttons = () => {
                const hide_delete_btn = !(cur_list.$checks && cur_list.$checks.length > 0);
                cur_list.$delete_folder_button.toggle(!hide_delete_btn);
                cur_list.$delete_files_button.toggle(!hide_delete_btn);
                cur_list.$unzip_file.toggle(!hide_delete_btn);
            }

            let old_on_row_checked = cur_list.on_row_checked;
            cur_list.on_row_checked = () => {
                old_on_row_checked.apply(cur_list);
                cur_list.toggle_folder_delete_buttons();
            }
        }
    }
}
