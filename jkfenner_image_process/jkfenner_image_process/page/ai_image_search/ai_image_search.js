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
        $('.navigate-button').on('click', () => this.navigateToAiImageDetails());
		$('.previewImage').on('click', () => this.previewImage());
    }

    navigateToAiImageDetails() {
        // Navigate to the "ai-image-details" page
        frappe.set_route('Form', 'ai-image-details');
    }

	previewImage(imagePath) {
		console.log("previewImage");
					// var canvas = document.getElementById('canv1');
					// var context = canvas.getContext('2d');
					
					// Clear the canvas and set the text
					// context.clearRect(0, 0, canvas.width, canvas.height);
					// context.fillText('Hello, World!', 10, 50);
				
					// // Convert the canvas content to an image data URL
					// var imageDataURL = canvas.toDataURL('/assets/jkfenner_image_process/images/jk_fenner_background.png');
				
					// // Replace the content of the image tag with the data URL
					// $('#canv1').attr('src', imageDataURL);

		var myImg = new Image();
		myImg.onload = function() {
		context.drawImage(myImg, 0,0);
		myImg.style.maxWidth = '50px';
		document.getElementById('preview-image').appendChild(myImg);
		};
		// myImg.src = '/assets/jkfenner_image_process/images/E70657-1.jpg';
		// myImg.maxWidth = '50px';
		myImg.src = imagePath;
		$("#preview-image").html(myImg)
	}
}

