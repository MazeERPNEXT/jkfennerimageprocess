import frappe
import os
from jkfennerai.inference import predict


@frappe.whitelist(allow_guest=True)
def guess_image(image): 
    config_file_path = "/home/mazeworks/frappe-bench-lms/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig.cfg"
    _file = frappe.get_doc("File", {'name': image})
    img_path = _file.get_full_path()
    predictor = predict(config_file_path)
    similarity_scores, similarity_images, pad_img = predictor.run(img_path)
    similarity_images_with_path = []
    for similarity_image in similarity_images:
        imagefolder = str(similarity_image).split('-')[0]
        similarity_images_with_path.append("/assets/jkfenner_image_process/images/machine_learning/augment_images/{}/{}".format(imagefolder, similarity_image))
    similarity_scores = [str(similarity_score) for similarity_score in similarity_scores]
    return {
        'images': similarity_images_with_path,
        'scores': similarity_scores
    }