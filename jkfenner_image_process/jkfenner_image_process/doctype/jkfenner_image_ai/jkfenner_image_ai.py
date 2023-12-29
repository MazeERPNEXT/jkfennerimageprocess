# Copyright (c) 2023, muthukumarmazeworks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JKFennerImageAI(Document):
	pass
# @frappe.whitelist()
# def get_timeline_html():
# 	html_content = """
# 		<!DOCTYPE html>
# 		<html>
# 		<head>
# 		<!-- Add your meta tags, styles, and other head elements here -->
# 		<meta name="viewport" content="width=device-width, initial-scale=1">
# 		<style>
# 			.slideshow-container {
# 			max-width: 1000px;
# 			position: relative;
# 			margin: auto;
# 			}

# 			.prev, .next {
# 			cursor: pointer;
# 			position: absolute;
# 			top: 50%;
# 			width: auto;
# 			padding: 16px;
# 			margin-top: -22px;
# 			color: white;
# 			font-weight: bold;
# 			font-size: 18px;
# 			transition: 0.6s ease;
# 			border-radius: 0 3px 3px 0;
# 			user-select: none;
# 			}

# 			.next {
# 			right: 0;
# 			border-radius: 3px 0 0 3px;
# 			}

# 			.prev:hover, .next:hover {
# 			background-color: rgba(0,0,0,0.8);
# 			}
# 			.text {
# 			color: #f2f2f2;
# 			font-size: 15px;
# 			padding: 8px 12px;
# 			position: absolute;
# 			bottom: 8px;
# 			width: 100%;
# 			text-align: center;
# 			}

# 			.numbertext {
# 			color: #f2f2f2;
# 			font-size: 12px;
# 			padding: 8px 12px;
# 			position: absolute;
# 			top: 0;
# 			}

# 			.dot {
# 			cursor: pointer;
# 			height: 15px;
# 			width: 15px;
# 			margin: 0 2px;
# 			background-color: #bbb;
# 			border-radius: 50%;
# 			display: inline-block;
# 			transition: background-color 0.6s ease;
# 			}

# 			.active, .dot:hover {
# 			background-color: #717171;
# 			}

# 			.fade {
# 			animation-name: fade;
# 			animation-duration: 1.5s;
# 			}

# 			@keyframes fade {
# 			from {opacity: .4} 
# 			to {opacity: 1}
# 			}

# 			@media only screen and (max-width: 300px) {
# 			.prev, .next,.text {font-size: 11px}
# 			}
# 			</style>
# 		</head>
# 		<body>
# 		<div class="slideshow-container">
# 			<div class="mySlides fade">
# 			<div class="numbertext">1 / 3</div>
# 			<img src="img_nature_wide.jpg" style="width:100%">
# 			<div class="text">Caption Text</div>
# 			</div>

# 			<div class="mySlides fade">
# 			<div class="numbertext">2 / 3</div>
# 			<img src="img_snow_wide.jpg" style="width:100%">
# 			<div class="text">Caption Two</div>
# 			</div>

# 			<div class="mySlides fade">
# 			<div class="numbertext">3 / 3</div>
# 			<img src="img_mountains_wide.jpg" style="width:100%">
# 			<div class="text">Caption Three</div>
# 			</div>

# 			<a class="prev" onclick="plusSlides(-1)">❮</a>
# 			<a class="next" onclick="plusSlides(1)">❯</a>

# 			</div>
# 			<br>
# 			<div style="text-align:center">
# 				<span class="dot" onclick="currentSlide(1)"></span> 
# 				<span class="dot" onclick="currentSlide(2)"></span> 
# 				<span class="dot" onclick="currentSlide(3)"></span> 
# 			</div>

# 		<script>
# 		let slideIndex = 1;
# 		showSlides(slideIndex);

# 		function plusSlides(n) {
# 		showSlides(slideIndex += n);
# 		}

# 		function currentSlide(n) {
# 		showSlides(slideIndex = n);
# 		}

# 		function showSlides(n) {
# 		let i;
# 		let slides = document.getElementsByClassName("mySlides");
# 		let dots = document.getElementsByClassName("dot");
# 		if (n > slides.length) {slideIndex = 1}    
# 		if (n < 1) {slideIndex = slides.length}
# 		for (i = 0; i < slides.length; i++) {
# 			slides[i].style.display = "none";  
# 		}
# 		for (i = 0; i < dots.length; i++) {
# 			dots[i].className = dots[i].className.replace(" active", "");
# 		}
# 		slides[slideIndex-1].style.display = "block";  
# 		dots[slideIndex-1].className += " active";
# 		}
# 		</script>

# 		</body>
# 		</html>
# 		"""
# 	return html_content