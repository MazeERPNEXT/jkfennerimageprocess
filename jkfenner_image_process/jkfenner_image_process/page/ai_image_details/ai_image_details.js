frappe.pages['ai-image-details'].on_page_load = function(wrapper) {
	var partNo = frappe.utils.get_url_arg('part_no');
	console.log(partNo,'dddd')
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'View Image Details',
		single_column: true
	});
	
	
	
	page.set_title('Result Details')
	let $btn = page.set_primary_action('Back To Search Image', function() {
		// window.history.go(-1)
		frappe.set_route("ai-image-search")
	});
   
	
   // Add Export button PDF
    // let $btnExport = page.set_secondary_action(__('Export PDF For Internal '), function() {
   	// 	method : window.open("/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_internal_pdf" , '_blank');
    // });

	page.add_action_item('Export PDF For Internal', () => {
		window.open(`/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_internal_pdf?part_no=${partNo}`, '_blank');
	});
	// page.add_action_item('Export PDF For Client', () => {
	// 	window.open("/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_client_pdf" , '_blank');
	// });

	// let $btnExportClient = page.set_inner_button(__('Export PDF For Client'), function() {
	// 	method : window.open("/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_client_pdf" , '_blank');
    // });
   
	$(frappe.render_template("ai_image_details", {})).appendTo(page.body);

	
		frappe.call({
			method: 'jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.get_image_ai_details',
			args: {
				part_no: partNo  // Pass the actual part_no here
			},
		
			callback: function(response) {
				// console.log(response.message)
				if (response) {
					// Access server-side data in the response
					var serverHtml = response.message;
					$('.layout-main-section').html('<div>'+serverHtml+"</div>")
					  
					// Add the slideshow script dynamically to the DOM
					var script = document.createElement('script');
					script.innerHTML = `
						var slideIndex = 0;
						showSlides();
		
						function showSlides() {
							var slides = document.getElementsByClassName("slide");
							for (var i = 0; i < slides.length; i++) {
								slides[i].style.display = "none";
							}
							slideIndex++;
							if (slideIndex > slides.length) {
								slideIndex = 1;
							}
							slides[slideIndex - 1].style.display = "block";
							setTimeout(showSlides, 8000); // Change slide every 8 seconds (adjust as needed)
						}
		
						document.querySelector('.prev').addEventListener('click', function() {
							slideIndex--;
							if (slideIndex < 1) {
								slideIndex = slides.length;
							}
							showSlides();
						});
		
						document.querySelector('.next').addEventListener('click', function() {
							slideIndex++;
							if (slideIndex > slides.length) {
								slideIndex = 1;
							}
							showSlides();
						});
					`;
					document.head.appendChild(script);
				}
			}
		});
	

	

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
						// console.log(currentSlide);
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