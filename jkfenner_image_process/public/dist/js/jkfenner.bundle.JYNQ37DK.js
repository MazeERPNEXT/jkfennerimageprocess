(() => {
  // ../jkfenner_image_process/jkfenner_image_process/public/js/jkfenner_image_process.bundle.js
  var pos = 0;
  var totalSlides = $("#slider-wrap ul li").length;
  var sliderWidth = $("#slider-wrap").width();
  $(document).ready(function() {
    $("#slider-wrap ul#slider").width(sliderWidth * totalSlides);
    $("#next").click(function() {
      slideRight();
    });
    $("#previous").click(function() {
      slideLeft();
    });
    var autoSlider = setInterval(slideRight, 3e3);
    $.each($("#slider-wrap ul li"), function() {
      var c = $(this).attr("data-color");
      $(this).css("background", c);
      var li = document.createElement("li");
      $("#pagination-wrap ul").append(li);
    });
    countSlides();
    pagination();
    $("#slider-wrap").hover(function() {
      $(this).addClass("active");
      clearInterval(autoSlider);
    }, function() {
      $(this).removeClass("active");
      autoSlider = setInterval(slideRight, 3e3);
    });
  });
  function slideLeft() {
    pos--;
    if (pos == -1) {
      pos = totalSlides - 1;
    }
    $("#slider-wrap ul#slider").css("left", -(sliderWidth * pos));
    countSlides();
    pagination();
  }
  function slideRight() {
    pos++;
    if (pos == totalSlides) {
      pos = 0;
    }
    $("#slider-wrap ul#slider").css("left", -(sliderWidth * pos));
    countSlides();
    pagination();
  }
  function countSlides() {
    $("#counter").html(pos + 1 + " / " + totalSlides);
  }
  function pagination() {
    $("#pagination-wrap ul li").removeClass("active");
    $("#pagination-wrap ul li:eq(" + pos + ")").addClass("active");
  }
})();
//# sourceMappingURL=jkfenner.bundle.JYNQ37DK.js.map
