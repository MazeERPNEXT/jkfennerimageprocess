import frappe
from frappe import DoesNotExistError, cstr, db , cint
from requests import get
import traceback
import time
import base64
import os
import shutil
from jkfenner_image_process.jkfenner_image_process.ai_patch import LoadJKFennerPatchModel
import configparser
from datetime import datetime

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("ai_patch_run", allow_site=True, max_size=500000000)


def is_job_running(job_name: str) -> bool:
	jobs = frappe.db.get_all("RQ Job", filters={"status": ["in", ["started", "queued"]]})
	for x in jobs:
		if x.job_name == job_name:
			return True
	return False


def run_mass_ai_prediction():
	job_name = "ai_patch_run"
	if not is_job_running(job_name):
		frappe.enqueue(
			method="jkfenner_image_process.mgmt_commands.run_mass_ai_prediction_job",
			queue="long",
			is_async=True,
			job_name=job_name,
			timeout="72000"
		)

def run_mass_ai_prediction_job():
	predictor = LoadJKFennerPatchModel().predictor
	test_images_frappe = frappe.get_doc("File", "Home/Input Images - AI Images Batch Processing")
	temp_folder = "/tmp/ai_images"
	shutil.rmtree(temp_folder, True)

	if (not os.path.exists(temp_folder)):
		os.mkdir(temp_folder)
		os.chmod(temp_folder, 0o777)

	test_images = os.path.join(temp_folder, "test_images")
	if (not os.path.exists(test_images)):
		os.mkdir(test_images)
		os.chmod(test_images, 0o777)
	image_files = test_images_frappe.get_successors()
	for image_file_name in image_files:
		image_file = frappe.get_doc("File", image_file_name)
		if image_file.is_folder:
			inner_folder_frappe = image_file
			inner_folder_url = os.path.join(test_images, image_file.file_name)
			if (not os.path.exists(inner_folder_url)):
				os.mkdir(inner_folder_url)
				os.chmod(inner_folder_url, 0o777)
			for inner_image_file_name in inner_folder_frappe.get_successors():
				inner_image_file = frappe.get_doc("File", inner_image_file_name)
				print(inner_image_file)
				if not inner_image_file.is_folder:
					file_content = inner_image_file.get_content()
					binary_file = open(os.path.join(inner_folder_url, inner_image_file.file_name), "wb")
					binary_file.write(file_content)
		else:
			file_content = image_file.get_content()
			binary_file = open(os.path.join(test_images, image_file.file_name), "wb")
			binary_file.write(file_content)
	single_augment_images_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/public/images/machine_learning/augment_images"
	branched_augment_images_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/public/images/machine_learning/augment_images"

	output_folder_path = os.path.join(temp_folder, "output_path")
	if (not os.path.exists(output_folder_path)):
		os.mkdir(output_folder_path)
		os.chmod(output_folder_path, 0o777)
	num_columns = 4
	num_rows = 5
	dl_segment = True
	threshold_segment = False
	hose_type = "single"

	predictor.run(test_images, single_augment_images_path, branched_augment_images_path, output_folder_path, 
			   		num_columns, num_rows, dl_segment, threshold_segment, hose_type, None,
					None, None, None, None, None)
	save_output_to_frappe(output_folder_path)


@frappe.whitelist()
def test_file():
	save_output_to_frappe('/tmp/ai_images/output_path')


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

	