import frappe
from datetime import datetime
import os
import zipfile
from frappe.utils.file_manager import get_file
import shutil
import json
from pathlib import Path
from frappe.utils.background_jobs import enqueue
from frappe.core.doctype.file import generate_file_name
from frappe.core.doctype.file.utils import get_content_hash

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
                    original_file_name = inner_file_path.split("/")[-1]
                    with open(inner_file_path, "rb") as f:
                        content_hash = get_content_hash(f.read())
                        file_name = generate_file_name(
                            name=original_file_name,
                            suffix=content_hash[-6:],
                            is_private=False,
                        )
                        public_file_path = Path(
                                            frappe.get_site_path("public", "files", file_name)
                                            )
                        shutil.copy(inner_file_path, public_file_path)
                        file_data = {
                            'name': frappe.generate_hash(length=10),
                            'file_name': file_name,
                            'file_url': os.path.join("/files", file_name),
                            'is_private': 0,
                            'content_hash': content_hash,
                            'file_size': os.path.getsize(public_file_path),
                            'folder': folder_doc.name,
                            'creation': datetime.now(),
                            'modified': datetime.now(),
                            'modified_by': 'Administrator',
                            'owner': 'Administrator',
                            'docstatus': 0,
                            'idx': 0,
                            'file_type': 'JPG',
                            'is_home_folder': 0,
                            'is_attachments_folder': 0,
                            'is_folder': 0,
                            'uploaded_to_dropbox': 0,
                            'uploaded_to_google_drive': 0
                        }
                        tab_file = frappe.qb.Table('tabFile')
                        insert_query = frappe.qb.into(tab_file)\
                            .insert(list(file_data.values()))\
                            .columns(tab_file.name, tab_file.file_name, tab_file.file_url,
                                     tab_file.is_private, tab_file.content_hash,
                                     tab_file.file_size, tab_file.folder,
                                     tab_file.creation, tab_file.modified,
                                     tab_file.modified_by, tab_file.owner,
                                     tab_file.docstatus, tab_file.idx,
                                     tab_file.file_type, tab_file.is_home_folder,
                                     tab_file.is_attachments_folder, tab_file.is_folder,
                                     tab_file.uploaded_to_dropbox, tab_file.uploaded_to_google_drive
                                     )
                        insert_query = insert_query.run()
        else:
            with open(file_path, 'rb') as f:  
                file_name = file_path.split("/")[-1]
                content_hash = get_content_hash(f.read())
                file_name = generate_file_name(
                    name=file_name,
                    suffix=content_hash[-6:],
                    is_private=False,
                )
                public_file_path = Path(
                                    frappe.get_site_path("public", "files", file_name)
                                    )
                shutil.copy(file_path, public_file_path)
                file_data = {
                    'name': frappe.generate_hash(length=10),
                    'file_name': original_file_name,
                    'file_url': os.path.join("public", "files", file_name),
                    'is_private': 0,  # Set to 1 if the file is private
                    'content_hash': content_hash,  # Calculate and insert the actual content hash if needed
                    'file_size': os.path.getsize(public_file_path),
                    'folder': folder_doc.name,
                    'creation': datetime.now(),
                    'modified': datetime.now(),
                    'modified_by': 'Administrator',
                    'owner': 'Administrator',
                    'docstatus': 0,
                    'idx': 0,
                    'file_type': 'JPG',
                    'is_home_folder': 0,
                    'is_attachments_folder': 0,
                    'is_folder': 0,
                    'uploaded_to_dropbox': 0,
                    'uploaded_to_google_drive': 0
                }
                tab_file = frappe.qb.Table('tabFile')
                insert_query = frappe.qb.into(tab_file)\
                    .insert(list(file_data.values()))\
                    .columns(tab_file.name, tab_file.file_name, tab_file.file_url,
                             tab_file.is_private, tab_file.content_hash,
                             tab_file.file_size, tab_file.folder,
                             tab_file.creation, tab_file.modified,
                             tab_file.modified_by, tab_file.owner,
                             tab_file.docstatus, tab_file.idx,
                             tab_file.file_type, tab_file.is_home_folder,
                             tab_file.is_attachments_folder, tab_file.is_folder,
                             tab_file.uploaded_to_dropbox, tab_file.uploaded_to_google_drive
                             )
                insert_query = insert_query.run()
    frappe.db.commit()

@frappe.whitelist()
def unzip(file_ids):
    file_ids = json.loads(file_ids)
    task_id = frappe.generate_hash(length=10)
    # enqueue("jkfenner_image_process.jkfenner_image_process.input_zip.unzip_task", file_ids=file_ids, task_id=task_id)
    unzip_task(file_ids, task_id)
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
            file_path = file_doc.get_full_path()
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    if member.filename.startswith("__MACOSX/"):
                        # skip directories and macos hidden directory
                        continue
                    extracted_path = zip_ref.extract(member, input_temp_folder_location)
                    # Adjust the permission of the extracted file/directory
                    if os.path.isfile(extracted_path) or os.path.isdir(extracted_path):
                        os.chmod(extracted_path, 0o777)   
            file_doc.delete(ignore_permissions=True)
            
    save_input_to_frappe(input_temp_folder_location, "Home/Input Images - AI Images Batch Processing")
    return True
