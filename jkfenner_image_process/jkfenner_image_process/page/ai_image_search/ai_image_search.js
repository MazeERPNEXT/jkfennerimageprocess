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

            $('.navigate-details').on('click', (event) => {
                const imageName = $(event.target).data('image-name');
                const imagePercentage = $(event.target).data('image-percentage');
                this.navigateToAiImageDetails(imageName,imagePercentage);
            });
            $('.previewImage').on('change', (e) => this.previewImage(e)); 
            
            $('.navigate-button').on('click', async() => {
                await this.pickMatchingImage($(this).data('action'));
                // await this.getStoredData();
            });

            // $('.stored-dimensions').on('click', async() => {
            //     await this.getStoredData()
            // });
            $(document).ready(function() {
                $('.preview_search_image_aug').on('click', function() {
                    var clickedImageSrc = $(this).attr('src');
                    $('#uploaded-image').attr('src', clickedImageSrc);
                });
            });
            $(document).ready(function() {
                $('.remove-icon').on('click', function() {
                    // Find the parent container of the remove icon
                    var parentContainer = $(this).closest('.image-container');
                    
                    // Set the src attribute of the image to the path of the default image
                    parentContainer.find('img').attr('src', '/assets/jkfenner_image_process/images/upload_image.png');
                });
            });
        // Add loader to the page
        this.loader = $('<div id="loader" class="loader"></div>').appendTo(this.page.body);
    
        }
        // Hide the loader after some time (for example, 3 seconds)
        // Adjust the time as needed
        navigateToAiImageDetails(part_no,Score,Image,childTable, parentTable) {
            const jsonString = JSON.stringify(Score, Image);
            console.log(childTable);
            const url = `/app/ai-image-details?part_no=${part_no}&matching_percentage=${Score}&image_url=${Image}&child_table=${childTable}&parent_table=${parentTable}`;
            window.open(url, '_blank');
        }
        

        upload_file(file) {
        
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
                            resolve(file_doc);
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
                            reject(403)
                        } else if (xhr.status === 413) {
                            file.failed = true;
                            file.error_message = "Size exceeds the maximum allowed file size.";
                            reject(413)
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
                            reject(error)
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
        
        
        // async getStoredData(){
        //     this.showLoader();
        //     let fileInput = $('.previewImage').prop('files')[0];
        //     const getScore = async (fileResponse) => {
        //         const innerDiameter1 = parseFloat($('#innerDiameter1Input').val());
        //         const innerDiameter2 = parseFloat($('#innerDiameter2Input').val());
        //         const length = parseFloat($('#lengthInput').val());
        //         const thickness = 5;
  
        //         const response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.guess_image', {
        //             image: fileResponse.name,
        //             inner_diameter_1: innerDiameter1,
        //             inner_diameter_2: innerDiameter2,
        //             length: length,
        //             thickness: thickness,
        //         });
        //          console.log("response",response)
        //             this.hideLoader();                
        //         };
        //         this.upload_file({'file_obj': fileInput, 'name': "TestImg.png", "file_name": "TestImg.png"}, getScore);
        //     }
       
        async pickMatchingImage(action){
            this.showLoader();
            let fileInputs = $('.previewImage').prop('files');
            fileInputs = Array.from(fileInputs);
            // Clear previous search results
            $('.preview-section').html('');
            const getScore = async (fileResponses) => {
                const innerDiameter1Input = $('#innerDiameter1Input').val();
                const innerDiameter2Input = $('#innerDiameter2Input').val();
                const lengthInput = $('#lengthInput').val();
                const bracnchedInput = $('#bracnchedInput').prop('checked');
                const darkBackgroundInput = $('#darkBackgroundInput').prop('checked');
                const withConnectorInput = $('#withConnectorInput').prop('checked');        
                const thickness = 5;
                const response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.guess_image', {
                    // images: JSON.stringify([fileResponse.name]), 
                    images : fileResponses.map(fr => fr.name).join('~'),
                    inner_diameter_1: innerDiameter1Input && action != 'without_struct' ? parseFloat(innerDiameter1Input) : '',
                    inner_diameter_2: innerDiameter2Input && action != 'without_struct' ? parseFloat(innerDiameter2Input) : '',
                    length: lengthInput && action != 'without_struct' ? parseFloat(lengthInput) : '',
                    branched: bracnchedInput,
                    dark_background: darkBackgroundInput,
                    with_connector: withConnectorInput,
                    thickness: thickness,
                });

                // Check if scores is undefined
                if (fileInputs.length == 0) {
                    // Handle the case where scores is undefined, e.g., show an error message
                    frappe.msgprint('Please Upload SKU Part.');
                    this.hideLoader();
                    return;
                }
                    let imageGrid = "";
                    //.slice(0, 3)
                    response.matching_find_images.forEach((image, _index) => {
                        // Extract data from the response
                        let part_no = image.part_no && image.part_no ? image.part_no.name : '';
                        let score = image.matching_percentage;
                        const roundedPercentage = Math.round(image.matching_percentage);
                        const roundedPercentageString = `Matching Percentage: ${roundedPercentage}%`;

                        // Construct HTML for each image
                            imageGrid += `
                                    <div class="col-lg-4 col-md-6 col-sm-6 mb-3">
                                        <div class="card-image">
                                            <div id="image-details" class="card-body-image">
                                            <h5 class="card-title-image"> ${roundedPercentageString}</h5>
                                                <div class="card-image-search"> 
                                                <img style="height: 221px; object-fit: scale-down;" class="matchingimage w-100" id="matchingImage"  src="${image.image_url}" alt="Matching Image">
                                                <p  style="text-align:center">${!!image ? image.part_no : "No Image"}</p> 
                                            </div>
                                            <div class="card-content">
                                                <p>Image Similarty Score: ${image.matching_percentage}</p>
                                                <p>ID A1: ${image.id_a1}, ID A2: ${image.id_a2 || 0 }, Length: ${image.length || 0 }, Thickness: ${image.thickness || 0 }</p>
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
                let fileResponses = []
                let filePromises = []
                fileInputs.forEach(fileInput =>{
                    const imageName = fileInput.name.split('.')[0];
                    filePromises.push(this.upload_file({'file_obj': fileInput, 'name': "TestImg.png", "file_name": imageName}));
                });
                fileResponses = await Promise.all(filePromises);
                getScore(fileResponses);
            }

        showLoader() {
            this.loader.show();
        }
        hideLoader() {
            this.loader.hide();
        }

        previewImage(event) {
            this.showLoader();
            var input = event.target;
            var files = input.files;
            var previewImageIds = ['uploaded-image_1', 'uploaded-image_2', 'uploaded-image_3']; // IDs of preview image elements
        
            for (let i = 0; i < files.length; i++) {
                var file = files[i];
                var reader = new FileReader(); // FileReader object to read the file
        
                reader.onload = (function (index) {
                    return function (event) {
                        var img = new Image();
                        img.onload = function () {
                            // Set the src attribute of the corresponding img tag
                            document.getElementById(previewImageIds[index]).src = event.target.result;
                             // Remove the image icon
                            document.getElementById(previewImageIds[index]).classList.remove('icon-image');
                        };
                        img.src = event.target.result;
                    };
                })(i);
                // Read the selected file as a data URL
                reader.readAsDataURL(file);
            }
        
            this.hideLoader();
        }
    }
    $(document).ready(function () {
        // Initialize your page
        frappe.pages['ai-image-search'].on_page_load();
    });

    