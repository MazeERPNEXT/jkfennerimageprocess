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
}