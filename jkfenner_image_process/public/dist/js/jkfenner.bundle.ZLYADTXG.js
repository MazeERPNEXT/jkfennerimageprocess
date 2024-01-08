(() => {
  // ../jkfenner_image_process/jkfenner_image_process/public/js/jkfenner_image_process.bundle.js
  frappe.ui.form.on("jkfenner_image_ai", {
    refresh: function(frm) {
      let currentSlide = 0;
      const slides = document.querySelectorAll(".slide");
      const dots = document.querySelectorAll(".dot");
      const init = (n) => {
        slides.forEach((slide, index) => {
          slide.style.display = "none";
          dots.forEach((dot, index2) => {
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
        }, 5e3);
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
})();
//# sourceMappingURL=jkfenner.bundle.ZLYADTXG.js.map
