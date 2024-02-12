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

	// Function to get images
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

	},
	after_save: function (frm) {
		// Your custom logic when a row is removed from the payment_entry_child table
		console.log('removed');
		// Example: Update the image preview when a row is removed
		frm.trigger('get_image');
	},
	refresh: function (frm) {
		frm.trigger('get_image');
		frm.trigger('hide_add_row');
    },

	

});

// frappe.ui.form.on('Product Dimensions', {
//     product_dimensions_add: function(frm, cdt, cdn) {
//         var selfTraining = locals[cdt][cdn];
//         let add_row = {
//             1: "HOSE A",
//             2: "HOSE B",
//             3: "HOSE C",
//             4: "HOSE D",
//             5: "HOSE E"
//         };

//         // Set value of "hoses"
//         frappe.model.set_value(cdt, cdn, "hoses", add_row[selfTraining.idx]);
// 		// frm.fields_dict['product_dimensions'].grid.cannot_add_rows = true;
//         // Trigger hide_add_row function after setting "hoses"
// 		var add_row_length = Object.keys(selfTraining).length;
// 		console.log(selfTraining);
//         var max_allowed_rows = 5; // You can change this value as needed
//         if (add_row_length >= max_allowed_rows) {
//             frm.fields_dict['product_dimensions'].grid.cannot_add_rows = true;
//         } else {
//             frm.fields_dict['product_dimensions'].grid.cannot_add_rows = false;
//         }
//         frm.trigger('hide_add_row');
//     },

//     hide_add_row: function(frm) {
//         var add_row_length = Object.keys(selfTraining).length;
// 		console.log(add_row_length);
//         var max_allowed_rows = 5; // You can change this value as needed
//         if (add_row_length >= max_allowed_rows) {
//             frm.fields_dict['product_dimensions'].grid.cannot_add_rows = true;
//         } else {
//             frm.fields_dict['product_dimensions'].grid.cannot_add_rows = false;
//         }
//     },
// });


frappe.ui.form.on('Product Dimensions', {
    product_dimensions_add: function(frm, cdt, cdn) {
        var selfTraining = locals[cdt][cdn];
        let add_row = {
            1: "HOSE A",
            2: "HOSE B",
            3: "HOSE C",
            4: "HOSE D",
            5: "HOSE E",
			6: "HOSE F",
        };
        frappe.model.set_value(cdt, cdn, "hoses", add_row[selfTraining.idx]);
        if (add_row[selfTraining.idx] === "HOSE E") {
            frm.fields_dict['product_dimensions'].grid.cannot_add_rows = true;
        }
    },

    refresh: function(frm) {
        frm.trigger('hide_add_row');
    },

    hide_add_row: function(frm) {
        if (frm.doc.product_dimensions_add == '') {
            frm.fields_dict['product_dimensions'].grid.cannot_add_rows = true;
        } else {
            frm.fields_dict['product_dimensions'].grid.cannot_add_rows = false;
        }
    },
});

// frappe.ui.form.on('Product Dimensions', {
// 	multiple_hoses_add : function(frm){
// 		frm.trigger('hoses');
// 	}
// });

frappe.ui.form.on('Multiple Image Upload', {
	multiple_image_upload_remove : function(frm){
		frm.trigger('get_image');		
	},
	multiple_image_upload_add : function(frm){
		frm.trigger('get_image');
	}
});

// Trigger 'add_units_to_field' function when inner_diameter_1 field changes
frappe.ui.form.on('Product Dimensions', {
    inner_diameter_1: function(frm, cdt, cdn) {
        add_units_to_field(frm, cdt, cdn);
    }
});

// Function to add units (mm) to the input field
function add_units_to_field(frm, cdt, cdn) {
    let child_row = locals[cdt][cdn];
    if (child_row.inner_diameter_1) {
        // Add units (mm) to the input field
        frappe.model.set_value(cdt, cdn, 'inner_diameter_1_with_units', child_row.inner_diameter_1 + ' mm');
    }
}