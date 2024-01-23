frappe.pages['ai-image-search'].on_page_load = function(wrapper) {
    new AiImageSearchPage(wrapper);
};

class AiImageSearchPage {
    constructor(wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'New Image Search',
            single_column: true
        });

        this.page.set_title('Image Search');

        // Render the template and append it to the page body
        $(frappe.render_template("ai_image_search", {})).appendTo(this.page.body);

        // Attach the function to the button click event using the class
        $('.navigate-details').on('click', () => this.navigateToAiImageDetails());
        $('.previewImage').on('change', (e) => this.previewImage(e)); // Use arrow function to retain 'this' context
        $('.navigate-button').on('click', () => {
            // Toggle the visibility of the target div
            
            this.pickMatchingImage()
        });

        // Dummy API data
        this.imageData = [
            { id: 1, src: '/assets/jkfenner_image_process/images/R7404808 W.jpg', title: 'Image 1' },
            { id: 2, src: '/assets/jkfenner_image_process/images/R7404808 W.jpg', title: 'Image 2' },
            { id: 3, src: '/assets/jkfenner_image_process/images/R7404808 W.jpg', title: 'Image 3' },
            // Add more image data as needed
        ];

        // Display dummy images on page load
        this.displayImages(this.imageData);
    }

    navigateToAiImageDetails() {
        // Navigate to the "ai-image-details" page
        frappe.set_route('Form', 'ai-image-details');
    }

    upload_file(file, callback) {
    
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();
            xhr.upload.addEventListener("loadstart", (e) => {
                file.uploading = true;
            });
            xhr.upload.addEventListener("progress", (e) => {
                if (e.lengthComputable) {
                    file.progress = e.loaded;
                    file.total = e.total;
                }
            });
            xhr.upload.addEventListener("load", (e) => {
                file.uploading = false;
                resolve();
            });
            xhr.addEventListener("error", (e) => {
                file.failed = true;
                reject();
            });
            xhr.onreadystatechange = () => {
                if (xhr.readyState == XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        file.request_succeeded = true;
                        let r = null;
                        let file_doc = null;
                        try {
                            r = JSON.parse(xhr.responseText);
                            if (r.message.doctype === "File") {
                                file_doc = r.message;
                            }
                        } catch (e) {
                            r = xhr.responseText;
                        }
    
                        file.doc = file_doc;
                        callback(file_doc)
                        //Handle Success
                    } else if (xhr.status === 403) {
                        file.failed = true;
                        let response = JSON.parse(xhr.responseText);
                        file.error_message = `Not permitted. ${response._error_message || ""}.`;
    
                        try {
                            // Append server messages which are useful hint for perm issues
                            let server_messages = JSON.parse(response._server_messages);
    
                            server_messages.forEach((m) => {
                                m = JSON.parse(m);
                                file.error_message += `\n ${m.message} `;
                            });
                        } catch (e) {
                            console.warning("Failed to parse server message", e);
                        }
                    } else if (xhr.status === 413) {
                        file.failed = true;
                        file.error_message = "Size exceeds the maximum allowed file size.";
                    } else {
                        file.failed = true;
                        file.error_message =
                            xhr.status === 0
                                ? "XMLHttpRequest Error"
                                : `${xhr.status} : ${xhr.statusText}`;
    
                        let error = null;
                        try {
                            error = JSON.parse(xhr.responseText);
                        } catch (e) {
                            // pass
                        }
                        frappe.request.cleanup({}, error);
                    }
                }
            };
            xhr.open("POST", "/api/method/upload_file", true);
            xhr.setRequestHeader("Accept", "application/json");
            xhr.setRequestHeader("X-Frappe-CSRF-Token", frappe.csrf_token);
    
            let form_data = new FormData();
            if (file.file_obj) {
                form_data.append("file", file.file_obj, file.name);
            }
            form_data.append("is_private", +file.private);
            
    
            if (file.file_url) {
                form_data.append("file_url", file.file_url);
            }
    
            if (file.file_name) {
                form_data.append("file_name", file.file_name);
            }
            if (file.library_file_name) {
                form_data.append("library_file_name", file.library_file_name);
            }
            
    
            if (file.optimize) {
                form_data.append("optimize", true);
            }
    
            xhr.send(form_data);
        }).then(function(res) {
            return res;
          });
    }

    async pickMatchingImage(){
        let fileInput = $('.previewImage').prop('files')[0];
        const getScore = async (fileResponse) => {
            let scores = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.guess_image',{
                image : fileResponse.name
            });
            let imageGrid = "";
            scores.images.forEach((image,_index) => {
                imageGrid += `<div class="col-4">
                <div class="card-image">
                   <div class="card-body-image" style="height: 440px;">
                      <h5 class="card-title-image">Matching Percentage: ${Math.round(scores.scores[_index]*100,2)}%</h5>
                      <div class="card-image-search"> <img style="height: 221px;object-fit: scale-down;" class="matchingimage w-100" id="matchingImage" src="${image}" alt="Matching Image"> </div>
                      <p>Struct dim Similarty Score: WIP</p>
                      <p>Image Similarty Score:  </p>
                      <p>ID A:WIP,ID B:WIP,ID C:WIP</p>
                      <button class="btn btn-primary btn-sm primary-action-image navigate-details">View Details</button> 
                   </div>
                </div>
             </div>`;
            })
            $('.preview-section').removeClass('hide');
            $('.preview-section').html('<div class="row">'+imageGrid+"</div>")
            
        };
        this.upload_file({'file_obj': fileInput, 'name':"TestImg.png","file_name":"TestImg.png"},getScore)
    }

    previewImage(event) {
        var input = event.target;
        var reader = new FileReader();
        var canvas = document.getElementById('canv1');
        var context = canvas.getContext('2d');

        reader.onload = function () {
            var img = new Image();
            img.onload = function () {
                // Clear the canvas
                context.clearRect(0, 0, canvas.width, canvas.height);

                // Set canvas dimensions to match the image
                canvas.width = img.width;
                canvas.height = img.height;

                // Draw the image on the canvas
                context.drawImage(img, 0, 0);

                // Convert the canvas content to an image data URL
                var imageDataURL = canvas.toDataURL();

                // Replace the content of the image tag with the data URL
                $('#uploaded-image').attr('src', imageDataURL);
            };
            img.src = reader.result;
        };

        // Read the selected file as a data URL
        reader.readAsDataURL(input.files[0]);
    }

    displayImages(images) {
        // Display images in a list or grid format
        var $imageList = $('.image-list');
        $imageList.empty();

        images.forEach((image) => {
            var $imageItem = $('<div class="image-item"></div>');
            var $image = $('<img src="' + image.src + '" alt="' + image.title + '">');
            var $title = $('<p>' + image.title + '</p>');

            $imageItem.append($image, $title);
            $imageList.append($imageItem);
        });
    }
}

$(document).ready(function () {
    // Initialize your page
    frappe.pages['ai-image-search'].on_page_load();
});