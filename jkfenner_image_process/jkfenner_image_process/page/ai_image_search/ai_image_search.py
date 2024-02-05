import frappe
import os
# from jkfennerai.inference import predict



@frappe.whitelist(allow_guest=True)
def guess_image(image):
    ai_responses = {
        "images": [
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/E72068/E72068-16.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70368/C70368-41.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/E71617/E71617-28.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70592/C70592-90.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70477/C70477-49.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/E71617/E71617-74.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/E72068/E72068-61.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70592/C70592-34.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/C70680/C70680-9.jpg",
            "/assets/jkfenner_image_process/images/machine_learning/augment_images/A70896/A70896-59.jpg"
        ],
        "scores": [
            "0.8233142",
            "0.7654208",
            "0.7642282",
            "0.7544414",
            "0.74282396",
            "0.742217",
            "0.73571",
            "0.7337779",
            "0.7235214",
            "0.7229657"
        ]
    }
    # config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig.cfg"
    # _file = frappe.get_doc("File", {'name': image})
    # img_path = _file.get_full_path()
    # predictor = predict(config_file_path)
    # similarity_scores, similarity_images, pad_img = predictor.run(img_path)
    # similarity_images_with_path = []
    # for similarity_image in similarity_images:
    #     imagefolder = str(similarity_image).split('-')[0]
    #     similarity_images_with_path.append("/assets/jkfenner_image_process/images/machine_learning/augment_images/{}/{}".format(imagefolder, similarity_image))
    # similarity_scores = [str(similarity_score) for similarity_score in similarity_scores]
    # return {
    #     'images': similarity_images_with_path,
    #     'scores': similarity_scores
    # }
    # config_file_path = "/home/frappe/frappe-bench/apps/jkfenner_image_process/jkfenner_image_process/config/aiconfig.cfg"
    # _file = frappe.get_doc("File", {'name': image})
    # img_path = _file.get_full_path()
    # predictor = predict(config_file_path)
    # similarity_scores, similarity_images, pad_img = predictor.run(img_path)
    # similarity_images_with_path = []
    # for similarity_image in similarity_images:
    #     imagefolder = str(similarity_image).split('-')[0]
    #     similarity_images_with_path.append("/assets/jkfenner_image_process/images/machine_learning/augment_images/{}/{}".format(imagefolder, similarity_image))
    # similarity_scores = [str(similarity_score) for similarity_score in similarity_scores]
    # ai_responses = {
    #     'images': similarity_images_with_path,
    #     'scores': similarity_scores
    # }
    predicted_images = ai_responses['images']
    docsinfo = [ image.split('/')[-2] for image in predicted_images]
    docs = []
    for docinfo in docsinfo:
        try:
            docs.append(frappe.get_last_doc('JKFenner Image AI', filters=[["name","=",docinfo]]))
        except frappe.DoesNotExistError:
            docs.append(None)
    ai_responses["docs"] = docs
    return ai_responses