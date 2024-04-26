import frappe
import os
import sys
# from jkfennerai.inference import predict
from collections import OrderedDict
from jkfenner_image_process.jkfenner_image_process.ai import LoadJKFennerModel
import base64
import cv2
from io import BytesIO
from frappe import publish_progress
from time import sleep

@frappe.whitelist()
def guess_image(images, inner_diameter_1, inner_diameter_2, length, branched, dlsegment, threshold, similarity_score):
    images = images.split('~')
    _files = frappe.get_list("File", filters = {'name':["in", images]}, fields=["name"], pluck="name")
    inner_diameter_1 = float(inner_diameter_1) if inner_diameter_1 else None
    inner_diameter_2 = float(inner_diameter_2) if inner_diameter_2 else None
    length = int(length) if length else None
    is_branched_hose = True if branched == 'true' else False
    dl_segment = True if dlsegment == 'true' else False
    is_threshold = True if threshold == 'true' else False    
    # ai_responses = {
    #     "images": [
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/E72068/E72068-16.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70368/C70368-41.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/E71617/E71617-28.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70592/C70592-90.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70477/C70477-49.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/E71617/E71617-74.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/E72068/E72068-61.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70592/C70592-34.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70680/C70680-9.jpg",
    #         "/assets/jkfenner_image_process/images/machine_learning/augment_images/A70896/A70896-59.jpg"
    #     ],
    #     "scores": [
    #         "0.8233142",
    #         "0.7654208",
    #         "0.7642282",
    #         "0.7544414",
    #         "0.74282396",
    #         "0.742217",
    #         "0.73571",
    #         "0.7337779",
    #         "0.7235214",
    #         "0.7229657"
    #     ]
    # }

    
    ai_responses = {}

    imgs = [frappe.get_doc('File', _file) for _file in _files]
    img_paths = [file.get_full_path() for file in imgs]
    predictor = LoadJKFennerModel().predictor
    similarity_scores = []
    print(img_paths, dl_segment, is_threshold, 'branch' if is_branched_hose else 'single', inner_diameter_1, inner_diameter_2, length, 0,sep=" ----- ")
    similarity_images, foreground_img_list = predictor.run(img_paths, dl_segment, is_threshold, 'branch' if is_branched_hose else 'single', inner_diameter_1, inner_diameter_2, length, 200)
    base64_images = []
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 35]
    for foreground_img in foreground_img_list:
        is_success, buffer = cv2.imencode(".jpg", foreground_img, encode_param)
        if is_success:
            im = base64.b64encode(buffer)
            base64_images.append(im)
    similarity_images = dict(sorted(similarity_images.items(), key=lambda x: x[1], reverse=True))
    similarity_images = OrderedDict(similarity_images)
    similarity_images_with_path = []
    for similarity_image, score in similarity_images.items():
        image_parts = str(similarity_image).split('-')
        image_parts.pop()
        imagefolder = "-".join(image_parts)
        similarity_images_with_path.append("/assets/jkfenner_image_process/images/machine_learning/augment_images/{}/{}".format(imagefolder, similarity_image))
        similarity_scores.append(score)
    similarity_scores = [str(similarity_score) for similarity_score in similarity_scores]

    # Filter data based on similarity score
    filtered_data = [(image, score) for image, score in zip(similarity_images_with_path, similarity_scores) if float(score) >= float(similarity_score)]

    ai_responses["images"] = [data[0] for data in filtered_data]
    ai_responses["scores"] = [data[1] for data in filtered_data]
    ai_responses['foreground_images'] = base64_images
    
    predicted_images = ai_responses['images']
    docsinfo = [image.split('/')[-2] for image in predicted_images]
    docs = []
    for docinfo in docsinfo:
        try:
            docs.append(frappe.get_last_doc('JKFenner Image AI', filters=[["name","=",docinfo]]))
        except frappe.DoesNotExistError:
            docs.append(None)
    ai_responses["docs"] = docs

    try:
        # Store image URL
        image_doc = frappe.get_doc({
            'doctype': 'JKFenner Upload Image Stored',
            'upload_image': ','.join([ img.file_url for img in imgs]),
            'id_a1': inner_diameter_1,
            'id_a2': inner_diameter_2,
            'length': length,
            'branched': is_branched_hose,
            'dl_segment': dl_segment,
            'threshold': is_threshold,
            'current_datetime': frappe.utils.now_datetime()
        })
        
        image_doc.insert(ignore_permissions=True)
        foreground_img_doc_list = []
        for index, foreground_img in enumerate(ai_responses['foreground_images']):
            file = frappe.get_doc(
			{
				"doctype": "File",
				"file_name": image_doc.name+f"_foreground_image_{index}.jpg",
				"attached_to_doctype": image_doc.doctype,
				"attached_to_name": image_doc.name,
				"content": foreground_img,
				"decode": True,
			}
		    )
            file.save()
            foreground_img_doc_list.append(file.file_url)
        if foreground_img_doc_list:
            image_doc.foreground_image_url = ",".join(foreground_img_doc_list)
            image_doc.save()
        # Create records in child table for each document in ai_responses
        for index, image_url in enumerate(ai_responses["images"]):

            part_no = os.path.basename(os.path.dirname(image_url))
            part_no_with_hose = os.path.basename(image_url)
            part_no_with_hose = part_no_with_hose.split('-')[-1].split('.')[0]
            main_table_part_no = ai_responses["docs"][index]

            # Fetch the document from JKFenner Image AI table based on part_no
            jkfenner_image_ai_doc = None
            inner_diameter_1 = 0
            inner_diameter_2 = 0
            length = "None"
            thickness = "None"

            try:
                jkfenner_image_ai_doc = frappe.get_last_doc("JKFenner Image AI", {'part_no': part_no})
            except frappe.DoesNotExistError: 
                pass
            # Access product_dimensions child table and get inner_diameter_1 value
            # inner_diameter_1 = jkfenner_image_ai_doc.product_dimensions[part_no_with_hose].inner_diameter_1_mm if part_no_with_hose in jkfenner_image_ai_doc.product_dimensions else 0
            # inner_diameter_2 = jkfenner_image_ai_doc.product_dimensions[part_no_with_hose].inner_diameter_2_mm if part_no_with_hose in jkfenner_image_ai_doc.product_dimensions else 0
            if jkfenner_image_ai_doc:
                inner_diameter_1 = jkfenner_image_ai_doc.product_dimensions[0].inner_diameter_1_mm if jkfenner_image_ai_doc.product_dimensions else 0
                inner_diameter_2 = jkfenner_image_ai_doc.product_dimensions[0].inner_diameter_2_mm if jkfenner_image_ai_doc.product_dimensions else 0
                length = jkfenner_image_ai_doc.product_dimensions[0].length if jkfenner_image_ai_doc.product_dimensions else 0
                thickness = jkfenner_image_ai_doc.product_dimensions[0].thickness if jkfenner_image_ai_doc.product_dimensions else 0

            # Insert into the child table of JKFenner Upload Image Stored
            image_doc.append('matching_find_images', {
                'part_no': part_no,
                'image_url': image_url,
                'matching_percentage': float(ai_responses["scores"][index]) * 100,
                'id_a1': inner_diameter_1,
                'id_a2': inner_diameter_2,
                'length': length,
                'thickness': thickness,
                'idx': index+1,
                'inner_diameter_1': inner_diameter_1,
                'inner_diameter_2': inner_diameter_2,
                # Add other fields as needed
            })

        # Save the image_doc after inserting all child records
        image_doc.save()
        frappe.db.commit()
    
        return image_doc
    except Exception as e:
        return "Failed to store image: {0}".format(str(e))
