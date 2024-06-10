import frappe
from datetime import datetime
import os


def save_output_to_frappe(output_folder_path, frappe_folder_path="Home/Output CSV - AI Images Patch Processing"):
	output_folder_path_frappe_parent = frappe.get_doc("File", frappe_folder_path)
	output_folder_path_frappe = frappe.new_doc("File")
	current_time = datetime.now()
	output_folder_path_frappe.update({
		"file_name": current_time.strftime("%Y%m%d_%H%M%S"),
		"folder": output_folder_path_frappe_parent.name,
		"is_folder": True
	})
	output_folder_path_frappe.insert(ignore_permissions=True)

	files = os.listdir(output_folder_path)
	for file in files:
		file_path = os.path.join(output_folder_path, file)
		if os.path.isdir(file_path):
			folder_doc = frappe.new_doc("File")
			folder_doc.update({
				"file_name": file,
				"folder": output_folder_path_frappe.name,
				"is_folder": True
			})
			folder_doc.insert(ignore_permissions=True)
			inner_files = os.listdir(file_path)
			for inner_file in inner_files:
				with open(os.path.join(file_path, inner_file), 'rb') as f:  
					bytes_contents = f.read()
					file_doc = frappe.new_doc("File")
					file_doc.is_private = False
					file_doc.file_name = inner_file
					file_doc.content = bytes_contents
					file_doc.save_file(ignore_existing_file_check=True, overwrite=True)
					file_doc.folder = folder_doc.name
					file_doc.insert()
		else:
			with open(file_path, 'rb') as f:  
				print(file_path)
				bytes_contents = f.read()
				file_doc = frappe.new_doc("File")
				file_doc.is_private = False
				file_doc.file_name = file
				file_doc.content = bytes_contents
				file_doc.save_file(ignore_existing_file_check=True, overwrite=True)
				file_doc.folder = output_folder_path_frappe.name
				file_doc.insert()
	frappe.db.commit()