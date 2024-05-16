frappe.pages['ai-image-search'].on_page_load = function (wrapper) {
    new AiImageSearchPage(wrapper);
};

let imageURL = '/assets/jkfenner_image_process/images/upload_image.png';
let taskID = Math.random().toString(36).substring(2);

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
            this.navigateToAiImageDetails(imageName, imagePercentage);
        });

        $('.previewImage').on('change', (e) => this.previewImage(e));

        $('.navigate-button').on('click', async () => {
            await this.pickMatchingImage($(this).data('action'));
            // await this.getStoredData();
        });
        $('.struct-button').on('click', async () => {
            await this.pickMatchingStruct($(this).data('action'));
            // await this.getStoredData();
        });

        $(document).ready(() => {
            $('.preview_search_image_aug').on('click', function () {
                var clickedImageSrc = $(this).attr('src');
                $('#uploaded-image').attr('src', clickedImageSrc);
            });

            $('.preview_seg_image').on('click', function () {
                var clickedImageSrc = $(this).attr('src');
                $('#uploaded-image').attr('src', clickedImageSrc);
            });

            $('.remove-icon').on('click', function () {
                // Find the parent container of the remove icon
                var parentContainer = $(this).closest('.image-container');

                // Set the src attribute of the image to the path of the default image
                parentContainer.find('img').attr('src', imageURL);
            });
            
            this.incrementQty = this.incrementQty.bind(this);
            this.decrementQty = this.decrementQty.bind(this);
             // Attach event listeners
                 this.attachTolleranceEventListeners();
        });
        // Add loader to the page
        this.loader = $('<div id="loader" class="loader"></div>').appendTo(this.page.body);
        // this.progress2 = $('<div class="container-progress"><div class="progress2 progress-moved"><div class="progress-bar2"><div class="progress-text">0%</div></div></div></div>').appendTo(this.page.body);
        frappe.socketio.task_subscribe(taskID);

       
    }

    attachTolleranceEventListeners() {
        // Attach event listeners to the buttons
        $('.qty-btn-plus').on('click', this.incrementQty);
        $('.qty-btn-minus').on('click', this.decrementQty);
    }
    
    incrementQty(event) {
        // Find the input field relative to the clicked button
        const $inputQty = $(event.target).closest('.qty-container').find('.input-qty');
        let currentValue = parseFloat($inputQty.val());
        $inputQty.val(currentValue + 1);
    }
    
    decrementQty(event) {
        // Find the input field relative to the clicked button
        const $inputQty = $(event.target).closest('.qty-container').find('.input-qty');
        let currentValue = parseFloat($inputQty.val());
        if (currentValue > 0) {
            $inputQty.val(currentValue - 1);
        }
    }   

    // Hide the loader after some time (for example, 3 seconds)
    // Adjust the time as needed
    navigateToAiImageDetails(part_no, Score, Image, childTable, parentTable) {
        const jsonString = JSON.stringify(Score, Image);
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
        }).then(function (res) {
            return res;
        });
    }
    showLoader() {
        this.loader.show();
    }
    hideLoader() {
        this.loader.hide();
    }
    
// Pick Matching Image
    async pickMatchingImage(action) { 
        this.showLoader();
        let fileInputs = $('.previewImage').prop('files');
        fileInputs = Array.from(fileInputs);
        // Clear previous search results 
        $('.preview-section').html('');
        const getScore = async (fileResponses) => {
          const bracnchedInput = $('#bracnchedInput').prop('checked');
          const dlsegmentInput = $('#dlsegmentInput').prop('checked');
          const thresholdInput = $('#thresholdInput').prop('checked');
          const thickness = 5;
      
          // Check if scores is undefined
          if (fileInputs.length == 0) {
            // Handle the case where scores is undefined, e.g., show an error message
            frappe.msgprint('Please Upload SKU Part.');
            this.hideProgress();
            return;
          }
          if (!thresholdInput && !dlsegmentInput) {
            // Show message if neither checkbox is checked
            frappe.msgprint('Please Check Threshold or DL Segment');
            this.hideProgress();
            return;
          }
          const totalFiles = fileResponses.length;
          let processedFiles = 0;
         // Function to update the loading percentage
         const updatePercentage = () => {
            const percentage = Math.round((processedFiles / totalFiles) * 100);
            this.updateProgressPercentage(percentage);
        };
        frappe.show_progress("Image Processing",15,100,"Started Processing (15%)")

          const response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.guess_image', {
            images: fileResponses.map(fr => fr.name).join('~'),
            branched: bracnchedInput,
            dlsegment: dlsegmentInput,
            threshold: thresholdInput,
            thickness: thickness,
            task_id : taskID
          });
      
          let imageGrid = "";
          const foreground_images = response.foreground_image_url.split(',') || [];
          foreground_images.forEach((fi, index) => {
              let image = $(".preview_seg_image")[index];
              if(!!image)
                  $(image).attr('src', fi);
          })
          response.matching_find_images.forEach((image, _index) => {
            let part_no = image.part_no && image.part_no ? image.part_no.name : '';
            let score = image.matching_percentage;
            const roundedPercentage = Math.round(image.matching_percentage);
            const roundedPercentageString = `Similarty Percentage: ${roundedPercentage}%`;
            const roundedSimilartyPercentage = `Image Similarty Score: ${roundedPercentage}%`;

            // Construct HTML for each image
            imageGrid += `
              <div class="col-lg-4 col-md-6 col-sm-6 mb-3">
                <div class="card-image">
                  <div id="image-details" class="card-body-image">
                    <h5 class="card-title-image">${roundedPercentageString}</h5>
                    <div class="card-image-search"> 
                      <img style="height: 221px; object-fit: scale-down;" class="matchingimage w-100" id="matchingImage"  src="${image.image_url}" alt="Matching Image">
                      <p style="text-align:center">${!!image ? image.part_no : "No Image"}</p> 
                    </div>
                    <div class="card-content">
                      <p>${roundedSimilartyPercentage}</p>
                      <p>ID A1: ${image.id_a1}, ID A2: ${image.id_a2 || 0}, Length: ${image.length || 0}, Thickness: ${image.thickness || 0}</p>
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
      
          $('.preview-section').removeClass('hide');
          $('.preview-section').html('<div class="row">' + imageGrid + "</div>");
      
          $('.navigate-details').on('click', (event) => {
            const imageName = $(event.target).data('image-name');
            const imagePercentage = $(event.target).data('image-percentage');
            const imagesPath = $(event.target).data('image-path');
            const childTable = $(event.target).data('child-name');
            const parentTable = $(event.target).data('parent-name');
            this.navigateToAiImageDetails(imageName, imagePercentage, imagesPath, childTable, parentTable);
          });
      
          this.hideLoader();
        };
      
        let fileResponses = []
        let filePromises = []
      
        fileInputs.forEach(fileInput => {
          const imageName = fileInput.name.split('.')[0];
          filePromises.push(this.upload_file({ 'file_obj': fileInput, 'name': "TestImg.png", "file_name": imageName }));
        });
        frappe.show_progress("Image Processing",5,100,"Uploading Images (5%)")
        fileResponses = await Promise.all(filePromises);
        getScore(fileResponses);
      }

// Structural dimensions
      async pickMatchingStruct(action) {
        this.showLoader();
        let fileInputs = $('.previewImage').prop('files');
        fileInputs = Array.from(fileInputs);
        // Clear previous search results
        $('.preview-section').html('');
        const getScore = async (fileResponses) => {
          const innerDiameter1MaxInput = $('#innerDiameter1MaxInput').val();
          const innerDiameter1MinInput = $('#innerDiameter1MinInput').val();
          const innerDiameter2MinInput = $('#innerDiameter2MinInput').val();
          const innerDiameter2MaxInput = $('#innerDiameter2MaxInput').val();
          const lengthInputMin = $('#lengthInputMin').val();
          const lengthInputMax = $('#lengthInputMax').val();
          const bracnchedInput = $('#bracnchedInput').prop('checked');
          const dlsegmentInput = $('#dlsegmentInput').prop('checked');
          const thresholdInput = $('#thresholdInput').prop('checked');
          const thickness = 5;
    
          frappe.show_progress("Image Processing",15,100,"Started Processing (15%)")
          const response = await frappe.xcall('jkfenner_image_process.jkfenner_image_process.page.ai_image_search.ai_image_search.guess_image', {
            images: fileResponses.map(fr => fr.name).join('~'),
            inner_diameter_1: innerDiameter1MinInput && action != 'without_struct' ? parseFloat(innerDiameter1MinInput) : '',
            inner_diameter_1_max: innerDiameter1MaxInput && action != 'without_struct' ? parseFloat(innerDiameter1MaxInput) : '',
            inner_diameter_2: innerDiameter2MinInput && action != 'without_struct' ? parseFloat(innerDiameter2MinInput) : '',
            inner_diameter_2_max: innerDiameter2MaxInput && action != 'without_struct' ? parseFloat(innerDiameter2MaxInput) : '',
            length: lengthInputMin && action != 'without_struct' ? parseFloat(lengthInputMin) : '',
            length_max: lengthInputMax && action != 'without_struct' ? parseFloat(lengthInputMax) : '',
            branched: bracnchedInput,
            dlsegment: dlsegmentInput,
            threshold: thresholdInput,
            thickness: thickness,
            // similarity_score: similarityScore,
            task_id: taskID
          });
      
          let imageGrid = "";
      
          response.matching_find_images.forEach((image, _index) => {
            let part_no = image.part_no && image.part_no ? image.part_no.name : '';
            let score = image.matching_percentage;
            const roundedPercentage = Math.round(image.matching_percentage);
            const roundedPercentageString = `Similarty Percentage: ${roundedPercentage}%`;
            const roundedSimilartyPercentage = `Image Similarty Score: ${roundedPercentage}%`;
      
            // Construct HTML for each image
            imageGrid += `
              <div class="col-lg-4 col-md-6 col-sm-6 mb-3">
                <div class="card-image">
                  <div id="image-details" class="card-body-image">
                    <h5 class="card-title-image">${roundedPercentageString}</h5>
                    <div class="card-image-search"> 
                      <img style="height: 221px; object-fit: scale-down;" class="matchingimage w-100" id="matchingImage"  src="${image.image_url}" alt="Matching Image">
                      <p style="text-align:center">${!!image ? image.part_no : "No Image"}</p> 
                    </div>
                    <div class="card-content">
                      <p>${roundedSimilartyPercentage}</p>
                      <p>ID A1: ${image.id_a1}, ID A2: ${image.id_a2 || 0}, Length: ${image.length || 0}, Thickness: ${image.thickness || 0}</p>
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
      
          $('.preview-section').removeClass('hide');
          $('.preview-section').html('<div class="row">' + imageGrid + "</div>");
      
          $('.navigate-details').on('click', (event) => {
            const imageName = $(event.target).data('image-name');
            const imagePercentage = $(event.target).data('image-percentage');
            const imagesPath = $(event.target).data('image-path');
            const childTable = $(event.target).data('child-name');
            const parentTable = $(event.target).data('parent-name');
            this.navigateToAiImageDetails(imageName, imagePercentage, imagesPath, childTable, parentTable);
          });
      
          this.hideLoader();
        };
      
        let fileResponses = []
        let filePromises = []
      
        fileInputs.forEach(fileInput => {
          const imageName = fileInput.name.split('.')[0];
          filePromises.push(this.upload_file({ 'file_obj': fileInput, 'name': "TestImg.png", "file_name": imageName }));
        });

        frappe.show_progress("Image Processing",5,100,"Uploading Images (5%)")
        
        fileResponses = await Promise.all(filePromises);
        getScore(fileResponses);
      }

  

    previewImage(event) {
        this.showLoader();
        var input = event.target;
        var files = input.files;
        var previewImageIds = ['uploaded-image_1', 'uploaded-image_2', 'uploaded-image_3']; // IDs of preview image elements

        $(".preview_seg_image").each(function(i, elem){    
            $(elem).attr('src', imageURL)
        });

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
$(document).ready(function() {
    // Function to clear structural dimensions inputs
    function clearStructuralInputs() {
        $('#innerDiameter1MinInput').val('');
        $('#innerDiameter2MinInput').val('');
        $('#lengthInputMin').val('');
        $('#innerDiameter1MaxInput').val('');
        $('#innerDiameter2MaxInput').val('');
        $('#lengthInputMax').val('');
    }

    // Event listener for image upload input change
    $('#finput').change(function() {
        clearStructuralInputs();
    });
});

$(document).ready(function () {
    // Initialize your page
    frappe.pages['ai-image-search'].on_page_load();
});
frappe.realtime.on('Image Processing', (msg) => {
    frappe.show_progress("Image Processing",msg.percentage,100, msg.message)
    if (msg.percentage >= 100) {
        setTimeout(()=>{
            frappe.hide_progress("Image Processing")
        }, 1000)
    }

});
var buttonPlus  = $(".qty-btn-plus");
var buttonMinus = $(".qty-btn-minus");

var incrementPlus = buttonPlus.click(function() {
  var $n = $(this)
  .parent(".qty-container")
  .find(".input-qty");
  $n.val(Number($n.val())+1 );
});

var incrementMinus = buttonMinus.click(function() {
  var $n = $(this)
  .parent(".qty-container")
  .find(".input-qty");
  var amount = Number($n.val());
  if (amount > 0) {
    $n.val(amount-1);
  }
});