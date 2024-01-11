frappe.ui.form.on('JKFenner Image AI', {
	onload: function (frm) {
		// Your onload logic here
		if(frm.preview_image_area == null)
		{ 
			frm.preview_image_area = $('<div class="preview-image row">').appendTo(
				frm.fields_dict.preview_image_html.wrapper
			);
		}	
	},
	get_image: function (frm) {

		if(!!frm.preview_image_area){
			let new_image_div = frm.doc.multiple_image_upload.map((file)=> {
				return `<div class="card col-2 ml-3 mr-3" style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s; width: 100%;border: 2px solid darkgray;border-top-left-radius: 10px;border-top-right-radius: 10px;height: 284px;" >   
				<img src="${!!file.images ? file.images : "/assets/jkfenner_image_process/images/sku_no_img.png"}"  alt="no-image" style="width:100%;border-top-left-radius: 10px;border-top-right-radius: 10px; position:relative; top:15px;height: 193px;object-fit: scale-down;">
				<div class="container" style="padding: 15px 16px;">
					<p>${!!file.images ? file.images.split('/').slice(-1).pop() : "No Image"}</p>    
				</div>
			</div>`
			});
			$(frm.preview_image_area).html(new_image_div);
		}

		// if (frm.doc.multiple_image_upload.length >= 1) {
		// 	frm.doc.multiple_image_upload.forEach(function (item) {
				
		// 		 `<img src="/assets/jkfenner_image_process/images/E70657-2.jpg " style="width: 95%; position: relative; left: 10px; top: 10px;"/>`
				
		// 		 frm.set_value(`<img src="/assets/jkfenner_image_process/images/E70657-2.jpg " style="width: 95%; position: relative; left: 10px; top: 10px;" />`)
		// 	});

		// 	frm.set_value(`<img src="/assets/jkfenner_image_process/images/E70657-2.jpg " style="width: 95%; position: relative; left: 10px; top: 10px;" />`);
		// } else {
		// 	frm.set_value(`<img src="/assets/jkfenner_image_process/images/sku_no_img.png " style="width: 95%; position: relative; left: 10px; top: 10px;" />`);
		// }


	},
	after_save: function (frm) {
		// Your custom logic when a row is removed from the payment_entry_child table
		console.log('removed');
		// Example: Update the image preview when a row is removed
		frm.trigger('get_image');
	},
	refresh: function (frm) {
		frm.trigger('get_image');
	}
});


frappe.ui.form.on('Multiple Image Upload', {
	multiple_image_upload_remove : function(frm){
		frm.trigger('get_image');		
	},
	multiple_image_upload_add : function(frm){
		frm.trigger('get_image');
	}
});