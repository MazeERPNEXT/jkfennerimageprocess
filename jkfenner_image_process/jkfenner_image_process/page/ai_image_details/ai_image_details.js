frappe.pages['ai-image-details'].on_page_load = function(wrapper) {
	var partNo = frappe.utils.get_url_arg('part_no');
	var scores = frappe.utils.get_url_arg('matching_percentage');
	var image = frappe.utils.get_url_arg('image_url');
	var parent_ref = frappe.utils.get_url_arg('parent_table');
	var child_ref = frappe.utils.get_url_arg('child_table');

	$(document).on('click', '.navigation-button', (e) => {
		if ($(e.currentTarget).data('href') != "#")
			window.location.href = $(e.currentTarget).data('href')
	})

	console.log("🚀 ~ scores:", scores)

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'View Image Details',
		single_column: true
	});

	page.set_title('Result Details')
	let $btn = page.set_primary_action('Back To Search Image', function() {
		frappe.set_route("ai-image-search")
	});

	page.add_action_item('Export PDF For Internal', () => {
		window.open(`/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_internal_pdf?child_ref=${child_ref}&parent_ref=${parent_ref}`, '_blank');
	});
	page.add_action_item('Export PDF For Client', () => {
		window.open(`/api/method/jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.generate_client_pdf?child_ref=${child_ref}&parent_ref=${parent_ref}`, '_blank');
	});

	$(frappe.render_template("ai_image_details", {})).appendTo(page.body);

	frappe.call({
		method: 'jkfenner_image_process.jkfenner_image_process.page.ai_image_details.ai_image_details.get_image_ai_details',
		args: {
			'parent_ref': parent_ref,
			'child_ref': child_ref,
		},
		callback: function(response) {
			if (response) {
				var serverHtml = response.message;
				$('.layout-main-section').html('<div>' + serverHtml + "</div>");
				if ($('.table-bordered tbody tr').length === 0) {
					$('.table-bordered tbody').html('<tr><td colspan="2">None</td></tr>');
				}
			}
		}
	});

	frappe.ui.form.on('jkfenner_image_ai', {
		refresh: function(frm) {
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
		}
	});

	function updateKnowledgeDate() {
		frappe.call({
			method: 'frappe.client.get',
			args: {
				doctype: 'Application Settings',
				name: 'Application Settings' // Assuming you are using the name "Application Settings"
			},
			callback: function(r) {
				if (r.message) {
					let lastDataSetDate = r.message.last_data_set_date;
					if (lastDataSetDate) {
						let dateObj = new Date(lastDataSetDate);
						let day = String(dateObj.getDate()).padStart(2, '0');
						let monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
						let month = monthNames[dateObj.getMonth()];
						let year = dateObj.getFullYear();
						let formattedDate = `${day}-${month}-${year}`;
						document.getElementById('knowledge_tv').innerText = `Knowledge Cutoff Date: ${formattedDate}`;
					}
				}
			}
		});
	}

	updateKnowledgeDate();

	// Additional code for your slider functionality if needed
	// $(document).ready(function() {
	// 	var $sliderValue = $('#slider-value');
	// 	var $imageElement = $('#slider-image');
	// 	var $prevButton = $('.prev');
	// 	var $nextButton = $('.next');

	// 	var images = [
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-1.jpg", percentage: 90 },
	// 	  { url: "/assets/jkfenner_image_process/images/R7404808 W.jpg", percentage: 20 },
	// 	  { url: "/assets/jkfenner_image_process/images/R7404809 W.jpg", percentage: 30 },
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-6.jpg", percentage: 40 },
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-5.jpg", percentage: 50 },
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-4.jpg", percentage: 60 },
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-2.jpg", percentage: 70 },
	// 	  { url: "/assets/jkfenner_image_process/images/E70657-3.jpg", percentage: 80 },
	// 	];

	// 	var currentIndex = 0;

	// 	function updateSliderValue() {
	// 	  var currentImage = images[currentIndex];
	// 	  $sliderValue.text('Matching Percentage: ' + currentImage.percentage + '%');
	// 	  $imageElement.attr('src', currentImage.url);
	// 	}

	// 	// Set initial value
	// 	updateSliderValue();

	// 	$prevButton.on('click', function() {
	// 	  currentIndex = (currentIndex - 1 + images.length) % images.length;
	// 	  updateSliderValue();
	// 	});

	// 	$nextButton.on('click', function() {
	// 	  currentIndex = (currentIndex + 1) % images.length;
	// 	  updateSliderValue();
	// 	});
	// });
}
