import frappe
import os
from jkfennerai.inference import predict
from collections import OrderedDict



@frappe.whitelist()
def guess_image(images,inner_diameter_1,inner_diameter_2,length,branched,dark_background,with_connector):
    images = images.split('~')
    _files = frappe.get_list("File", filters = {'name':["in", images]}, fields=["name"], pluck="name")
    is_branched_hose = True if branched == 'true' else False
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
    if not is_branched_hose:
        if inner_diameter_1 and inner_diameter_2 and length:
            config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig_with_struct.cfg"
        else:
            config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig.cfg"
    else:
        if inner_diameter_1 and inner_diameter_2 and length:
            config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig_branch_with_struct.cfg"
        else:
            config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig_branch.cfg"
    print(config_file_path)
    imgs = [frappe.get_doc('File', _file) for _file in _files]
    img_paths = [file.get_full_path() for file in imgs]
    predictor = predict(config_file_path)
    similarity_scores = []
    similarity_images = predictor.run(img_paths,inner_diameter_1, inner_diameter_2, length)
    similarity_images = dict(sorted(similarity_images.items(), key=lambda x: x[1], reverse=True))
    similarity_images = OrderedDict(similarity_images)
    print(similarity_scores, similarity_images)
    similarity_images_with_path = []
    for similarity_image, score in similarity_images.items():
        imagefolder = str(similarity_image).split('-')[0]
        similarity_images_with_path.append("/assets/jkfenner_image_process/images/machine_learning/augment_images/{}/{}".format(imagefolder, similarity_image))
        similarity_scores.append(score)
    similarity_scores = [str(similarity_score) for similarity_score in similarity_scores]

    ai_responses["images"] = similarity_images_with_path
    ai_responses["scores"] = similarity_scores
    
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
            'dark_background': True if dark_background == 'true' else False,
            'with_connector': True if with_connector == 'true' else False,
            'current_datetime': frappe.utils.now_datetime()
        })
        
        image_doc.insert(ignore_permissions=True)
        print(image_doc)
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
        # print(image_detail)
        return image_doc
    except Exception as e:
        print(frappe.get_traceback(), "Error storing image")
        return "Failed to store image: {0}".format(str(e))