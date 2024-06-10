import frappe
from datetime import datetime
import os
import zipfile
from frappe.utils.file_manager import get_file
import shutil
import json
from frappe.utils.background_jobs import enqueue

def save_input_to_frappe(output_folder_path, frappe_folder_path="Home/Output CSV - AI Images Patch Processing"):
    output_folder_path_frappe_parent = frappe.get_doc("File", frappe_folder_path)

    files = os.listdir(output_folder_path)
    for file in files:
        file_path = os.path.join(output_folder_path, file)
        if os.path.isdir(file_path):
            folder_doc = frappe.new_doc("File")
            folder_doc.update({
                "file_name": file,
                "folder": output_folder_path_frappe_parent.name,
                "is_folder": True
            })
            folder_doc.insert(ignore_permissions=True)
            inner_files = os.listdir(file_path)
            for inner_file in inner_files:
                inner_file_path = os.path.join(file_path, inner_file)
                if os.path.isfile(inner_file_path):
                    with open(inner_file_path, 'rb') as f:  
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
                bytes_contents = f.read()
                file_doc = frappe.new_doc("File")
                file_doc.is_private = False
                file_doc.file_name = file
                file_doc.content = bytes_contents
                file_doc.save_file(ignore_existing_file_check=True, overwrite=True)
                file_doc.folder = output_folder_path_frappe_parent.name
                file_doc.insert()
    frappe.db.commit()

@frappe.whitelist()
def unzip(file_ids):
    file_ids = json.loads(file_ids)
    task_id = frappe.generate_hash(length=10)
    enqueue("jkfenner_image_process.jkfenner_image_process.input_zip.unzip_task", file_ids=file_ids, task_id=task_id)
    return task_id

def unzip_task(file_ids, task_id):
    temp_folder = "/tmp/ai_images"

    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
        os.chmod(temp_folder, 0o777)

    input_temp_folder_location = os.path.join(temp_folder, "zip_archive")
    if not os.path.exists(input_temp_folder_location):
        os.mkdir(input_temp_folder_location)
        os.chmod(input_temp_folder_location, 0o777)
    else:
        shutil.rmtree(input_temp_folder_location, True)

    os.mkdir(input_temp_folder_location)  # Ensure the directory is created
    os.chmod(input_temp_folder_location, 0o777)

    for file_id in file_ids:
        file_doc = frappe.get_doc("File", file_id)
        if not file_doc.is_folder and file_doc.file_url.endswith('.zip'):
            file_path = frappe.get_site_path("public", "files", file_doc.file_name)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    extracted_path = zip_ref.extract(member, input_temp_folder_location)
                    # Adjust the permission of the extracted file/directory
                    if os.path.isfile(extracted_path) or os.path.isdir(extracted_path):
                        os.chmod(extracted_path, 0o777)   
            file_doc.delete()
            
    save_input_to_frappe(input_temp_folder_location, "Home/Input Images - AI Images Batch Processing")
    return True
