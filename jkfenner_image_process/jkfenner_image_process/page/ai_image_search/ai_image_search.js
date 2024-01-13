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
            $('.preview-section').toggleClass('hide');
        });
    }

    navigateToAiImageDetails() {
        // Navigate to the "ai-image-details" page
        frappe.set_route('Form', 'ai-image-details');
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
}

$(document).ready(function () {
    // Initialize your page
    frappe.pages['ai-image-search'].on_page_load();
});