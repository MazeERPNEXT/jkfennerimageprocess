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
            // $('.navigate-details').on('click', () => this.navigateToAiImageDetails());
            $('.navigate-details').on('click', (event) => {
                const imageName = $(event.target).data('image-name');
                const imagePercentage = $(event.target).data('image-percentage');
                this.navigateToAiImageDetails(imageName,imagePercentage);
            });
            $('.previewImage').on('change', (e) => this.previewImage(e)); // Use arrow function to retain 'this' context
            $('.navigate-button').on('click', async() => {
                await this.pickMatchingImage()
            });
            
        // Add loader to the page
        this.loader = $('<div id="loader" class="loader"></div>').appendTo(this.page.body);
        }
        
        navigateToAiImageDetails(part_no,Score,Image,childTable, parentTable) {
            const jsonString = JSON.stringify(Score, Image);
            console.log(childTable);
            const url = `/app/ai-image-details?part_no=${part_no}&matching_percentage=${Score}&image_url=${Image}&child_table=${childTable}&parent_table=${parentTable}`;
            console.log(url)
            window.open(url, '_blank');
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
            this.showLoader();
            let fileInput = $('.previewImage').prop('files')[0];
            const getScore = async (fileResponse) => {
                const inner_diameter_1 = 10; // Example value, replace with actual value
                const inner_diameter_2 = 20; // Example value, replace with actual value
                const length = 30; // Example value, replace with actual value
                const thickness = 5; // Example value, replace with actual value
  
                const response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.guess_image', {
                    image: fileResponse.name,
                    inner_diameter_1: inner_diameter_1,
                    inner_diameter_2: inner_diameter_2,
                    length: length,
                    thickness: thickness,
                });
                 console.log("response",response)
                // Check if scores is undefined
                if (!fileInput) {
                    // Handle the case where scores is undefined, e.g., show an error message
                    frappe.msgprint('Please Upload SKU Part.');
                    this.hideLoader();
                    return;
                    }

                // let imageName = scores.images[0];
                    
                    let imageGrid = "";
                    response.matching_find_images.slice(0, 3).forEach((image, _index) => {
                        // Extract data from the response
                        let part_no = image.part_no && image.part_no ? image.part_no.name : '';
                        let score = image.matching_percentage;
                        const roundedPercentage = Math.round(image.matching_percentage);
                        const roundedPercentageString = `Matching Percentage: ${roundedPercentage}%`;


                        // let innerDiameter1 = response.docs && response.docs[_index] && response.docs[_index].product_dimensions[0] ? response.docs[_index].product_dimensions[0].inner_diameter_1_mm : '0';
                        // let innerDiameter2 = response.docs && response.docs[_index] && response.docs[_index].product_dimensions[0] ? response.docs[_index].product_dimensions[0].inner_diameter_2_mm : '0';
                        // let length = response.docs && response.docs[_index] && response.docs[_index].product_dimensions[0] ? response.docs[_index].product_dimensions[0].length : '0';
                        // let thickness = response.docs && response.docs[_index] && response.docs[_index].product_dimensions[0] ? response.docs[_index].product_dimensions[0].thickness ?? 0 : '0';
        
                        // Construct HTML for each image
                        imageGrid += `<div class="col">
                                        <div class="card-image">
                                            <div id="image-details" class="card-body-image">
                                            <h5 class="card-title-image"> ${roundedPercentageString}</h5>
                                                <div class="card-image-search"> 
                                                <img style="height: 221px; object-fit: scale-down;" class="matchingimage w-100" id="matchingImage"  src="${image.image_url}" alt="Matching Image">
                                                <p  style="text-align:center">${!!image ? image.part_no : "No Image"}</p> 
                                            </div>
                                            <div class="card-content">
                                                <p>Image Similarty Score: ${image.matching_percentage}</p>
                                                <p>ID A1: ${image.id_a1}, ID A2: ${image.id_a2}, Length: ${image.length}, Thickness: ${image.thickness}</p>
                                                <button class="btn btn-primary btn-sm primary-action-image navigate-details" 
                                                    data-image-name="${image.part_no}" 
                                                    data-image-path="${image.image_url}" 
                                                    data-image-percentage="${roundedPercentage}" 
                                                    data-child-name="${image.name}"
                                                    data-parent-name="${response.name}">View Details</button>
                                            </div>
                                            </div>
                                        </div>
                                    </div>`;
                    });
        
                    // Display the constructed HTML
                    $('.preview-section').removeClass('hide');
                    $('.preview-section').html('<div class="row">' + imageGrid + "</div>");
        
                    // Attach event listener for details button
                    $('.navigate-details').on('click', (event) => {
                        const imageName = $(event.target).data('image-name');
                        const imagePercentage = $(event.target).data('image-percentage');
                        const imagesPath = $(event.target).data('image-path');
                        const childTable = $(event.target).data('child-name');
                        const parentTable = $(event.target).data('parent-name');
                        console.log(childTable) 
                        this.navigateToAiImageDetails(imageName, imagePercentage, imagesPath, childTable, parentTable);
                    });
                    this.hideLoader();                
                };
               this.upload_file({'file_obj': fileInput, 'name':"TestImg.png","file_name":"TestImg.png"},getScore)
            }

        showLoader() {
            this.loader.show();
        }
        hideLoader() {
            this.loader.hide();
        }

        previewImage(event) {
            // this.showLoader();
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
            // this.hideLoader();   
            // Read the selected file as a data URL
            reader.readAsDataURL(input.files[0]);
        }
        
    }
    $(document).ready(function () {
        // Initialize your page
        frappe.pages['ai-image-search'].on_page_load();
    });

    