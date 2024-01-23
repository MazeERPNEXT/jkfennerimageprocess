frappe.pages['ai-image-details'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'View Image Details',
		single_column: true
	});

	page.set_title('Result Details')
	let $btn = page.set_primary_action('Back To Search Image', function() {
		frappe.set_route("ai-image-search")
	});
   
	function createPDF() {
		var element = document.getElementById('element-to-print');
		
		// Find the button with the 'html2PdfConverter' class
		var button = document.querySelector('.html2PdfConverter');
	
		html2pdf(element, {
			margin: 1,
			padding: 0,
			filename: 'myfile.pdf',
			image: { type: 'jpeg', quality: 1 },
			html2canvas: { scale: 2, logging: true },
			jsPDF: { unit: 'in', format: 'A2', orientation: 'P' },
			// You can use the 'button' variable to access the button element
			button: button
		});
	}
   // Add Export button
    let $btnExport = page.set_secondary_action(__('Export as PDF'), function() {
        // Call a function to export the content as PDF
        createPDF();
    });
    function exportAsPDF() {
		// You can customize this logic based on your requirements
		var doc = new jsPDF();
		
		// Add content to the PDF
		doc.text('Image Details', 20, 10);
		doc.text('---------------------', 20, 20);
		
		// Add image
		var img = new Image();
		img.src = $('#slider-image').attr('src'); // Get the source of the image
		doc.addImage(img, 'JPEG', 20, 30, 160, 120); // You may need to adjust the dimensions
		
		// Add other details
		doc.text('Matching Percentage: ' + $('#slider-value').text(), 20, 160);
		
		// Save the PDF
		doc.save('image_details.pdf');
	}
	$(frappe.render_template("ai_image_details", {})).appendTo(page.body);
	frappe.ui.form.on('jkfenner_image_ai', {
		refresh: function(frm) {
			// Your Frappe method initialization code here
	
			let currentSlide = 0;
			const slides = document.querySelectorAll(".slide");
			const dots = document.querySelectorAll('.dot');
	
			const init = (n) => {
				slides.forEach((slide, index) => {
					slide.style.display = "none";
					dots.forEach((dot, index) => {
						dot.classList.remove("active");
					});
				});
				slides[n].style.display = "block";
				dots[n].classList.add("active");
			};
	
			frappe.dom.ready(() => {
				init(currentSlide);
	
				const next = () => {
					currentSlide >= slides.length - 1 ? currentSlide = 0 : currentSlide++;
					init(currentSlide);
				};
	
				const prev = () => {
					currentSlide <= 0 ? currentSlide = slides.length - 1 : currentSlide--;
					init(currentSlide);
				};
	
				frappe.ui.add_button(__("Next"), () => {
					next();
				});
	
				frappe.ui.add_button(__("Prev"), () => {
					prev();
				});
	
				setInterval(() => {
					next();
				}, 5000);
	
				dots.forEach((dot, i) => {
					dot.addEventListener("click", () => {
						console.log(currentSlide);
						init(i);
						currentSlide = i;
					});
				});
			});
		}
	});	

	$(document).ready(function() {
		var $sliderValue = $('#slider-value');
		var $imageElement = $('#slider-image');
		var $prevButton = $('.prev');
		var $nextButton = $('.next');
  
		var images = [
		  { url: "/assets/jkfenner_image_process/images/E70657-1.jpg", percentage: 90 },
		  { url: "/assets/jkfenner_image_process/images/R7404808 W.jpg", percentage: 20 },
		  { url: "/assets/jkfenner_image_process/images/R7404809 W.jpg", percentage: 30 },
		  { url: "/assets/jkfenner_image_process/images/E70657-6.jpg", percentage: 40 },
		  { url: "/assets/jkfenner_image_process/images/E70657-5.jpg", percentage: 50 },
		  { url: "/assets/jkfenner_image_process/images/E70657-4.jpg", percentage: 60 },
		  { url: "/assets/jkfenner_image_process/images/E70657-2.jpg", percentage: 70 },
		  { url: "/assets/jkfenner_image_process/images/E70657-3.jpg", percentage: 80 },
		  
		  // Add more image URLs and percentages as needed
		];
  
		var currentIndex = 0;
  
		function updateSliderValue() {
		  var currentImage = images[currentIndex];
		  $sliderValue.text('Matching Percentage: ' + currentImage.percentage + '%');
		  $imageElement.attr('src', currentImage.url);
		}
  
		// Set initial value
		updateSliderValue();
  
		$prevButton.on('click', function() {
		  currentIndex = (currentIndex - 1 + images.length) % images.length;
		  updateSliderValue();
		});
  
		$nextButton.on('click', function() {
		  currentIndex = (currentIndex + 1) % images.length;
		  updateSliderValue();
		});
	  });
}