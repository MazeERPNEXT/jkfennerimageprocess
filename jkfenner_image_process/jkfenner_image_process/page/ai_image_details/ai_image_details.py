import frappe
from frappe.utils.pdf import get_pdf
from reportlab.pdfgen import canvas 
from PyPDF2 import PdfReader, PdfWriter, PageObject
import io  
from jinja2 import Environment, FileSystemLoader
from ..ai_image_search.ai_image_search import guess_image

@frappe.whitelist(allow_guest=True)
def get_image_ai_details(part_no):
    part_no =  frappe.form_dict.get('part_no')
    result = frappe.get_all('JKFenner Image AI', filters={'part_no': part_no})
    image_paths = []
    getAllValues = None
    if result:
        x = result[0].name 
        getAllValues = frappe.get_doc('JKFenner Image AI', x)
        if hasattr(getAllValues, 'multiple_image_upload'):
            image_paths = [ child_row.images for child_row in getAllValues.multiple_image_upload]
    image_html_content = """ 
                    <div>
                        <p style="text-align: center; font-size: 20px;">{{getAllValues.part_no}}</p>
                    </div>
                    <div class="slide-container">
                             {% for image_path in image_paths %}
                                <div class="slide fade">
                                    <h5 id="slider-value" class="card-title-viewimage">Matching Percentage: 90%</h5>
                                    <img class="details-image" id="slider-image" src="{{ image_path }}" alt="Image 1">
                                </div>
                            {% endfor %}
                        <a href="#" class="prev" title="Previous">&#10094;</a>
                        <a href="#" class="next" title="Next">&#10095;</a>
                    </div>
                    <table class="table table-bordered">
                        <caption class="captions-image">Generic Details</caption>
                        <tbody>
                            <tr>
                                <td scope="row">Domestic / Export</td>
                                <td>{{getAllValues.domestic__export}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Part No.</td>
                                <td>{{getAllValues.part_no}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Part Description</td>
                                <td>{{getAllValues.part_description}}</td>
                            </tr>
                            <tr>
                                <td scope="row">SAP Asset Code</td>
                                <td>{{getAllValues.sap_asset_code}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Type of Hose</td>
                                <td>{{getAllValues.type_of_hose}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Toolings Created on</td>
                                <td>{{getAllValues.toolings_created_on}}</td>
                            </tr>
                            <tr>
                                <td scope="row">EAN</td>
                                <td>{{getAllValues.ean}}</td>
                            </tr>
                            <tr>
                                <td scope="row">UPC</td>
                                <td>{{getAllValues.upc}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Customer 1 (Cross Ref)</td>
                                <td>{{getAllValues.customer_1_cross_ref}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Customer 2 (Cross Ref)</td>
                                <td>{{getAllValues.customer_2_cross_ref}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Customer 3,4,5 (Cross Ref)</td>
                                <td>{{getAllValues.customer_345_cross_ref}}</td>
                            </tr>
                        </tbody>
                    </table>
    
                    <table class="table table-bordered">
                        <caption class="captions-image">Application/Performance</caption>
                        <tbody>
                            <tr>
                                <td scope="row">Vehicle Model</td>
                                <td>{{getAllValues.vehicle_model}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Application (Radiator / Heater ) </td>
                                <td>{{getAllValues.application_radiator__heater_}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Vehicle manufacturer </td>
                                <td>{{getAllValues.vehicle_manufacturer}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Vehicle Make/Year</td>
                                <td>{{getAllValues.vehicle_makeyear}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Sub Application </td>
                                <td>{{getAllValues.sub_application}}</td>
                            </tr>
                        </tbody>
                    </table>
    
                    <table class="table table-bordered">
                        <caption class="captions-image">Dimensions</caption>
                        <tbody>
                            <tr>
                                <td scope="row">Inner Diameter A (MM)</td>
                                <td>{{getAllValues.inner_diameter_a_mm}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Inner Diameter B (MM)</td>
                                <td>{{getAllValues.inner_diameter_b_mm}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Thickness  </td>
                                <td>{{getAllValues.thickness}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Outer Diameter A (mm)</td>
                                <td>{{getAllValues.outer_diameter_a_mm}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Outer Diameter B (mm) </td>
                                <td>{{getAllValues.outer_diameter_b_mm}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Central axis length (mm)</td>
                                <td>{{getAllValues.central_axis_length_mm}}</td>
                            </tr>
                            <tr>
                                <td scope="row">Product weight (grams) </td>
                                <td>{{getAllValues.product_weight_grams}}</td>
                            </tr> 
                        </tbody>
                    </table>"""
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(image_html_content)
    rendered_content = template.render(part_no=part_no, image_paths=image_paths, getAllValues=getAllValues)
    print (image_paths)
    return rendered_content

@frappe.whitelist(allow_guest=True)
def generate_internal_pdf(part_no):
    part_no = frappe.form_dict.get('part_no')
    result = frappe.get_all('JKFenner Image AI', filters={'part_no': part_no})
    image_paths = []

    if result:
        x = result[0].name 
        getAllValues = frappe.get_doc('JKFenner Image AI', x)
    
        if hasattr(getAllValues, 'multiple_image_upload'):
            image_paths = [frappe.utils.get_url(child_row.images) for child_row in getAllValues.multiple_image_upload]
        # return image_paths
    html_content_internal = '''<div class="layout-main-section" id="element-to-print">
                            <div style="position: relative;">
                            <!-- Rest of your HTML content -->
                            <img style="width: 37%; height: auto" src="/assets/jkfenner_image_process/images/JK-finner.png">
                        </div>
                        {% for image_path in image_paths %}
                        <div>
                            <h5 id="slider-value" style="font-size:18px; text-align:center" class="card-title-viewimage">Matching Percentage: 90%</h5>
                            <img id="slider-image" style="width:100%" src="{{ image_path }}" alt="Image 1">
                        </div>
                        {% endfor %}
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
                            margin: 20px 0px;
                            border-collapse: collapse;
                            
                            ">
                        <caption class="captions-image"
                          style="
                            color: #ffffff !important;
                            text-align: left !important;
                            /* text-align: center; */
                            background: #008174 !important;
                            padding: 10px !important;
                            font-weight: 700 !important;
                            font-size: 20px !important;
                            border-top-left-radius: 10px !important;
                            border-top-right-radius: 10px !important;
                            caption-side: top !important;
                            border-collapse: collapse;" 
                        >
                            Generic Details
                        </caption>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Domestic / Export</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.domestic__export}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Part No.</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.part_no}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Part Description</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.part_description}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">SAP Asset Code</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.sap_asset_code}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Type of Hose</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.type_of_hose}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Toolings Created on</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.toolings_created_on}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">EAN</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.ean}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">UPC</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.upc}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 1 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.customer_1_cross_ref}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 2 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.customer_2_cross_ref}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 3,4,5 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.customer_345_cross_ref}}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
                            margin: 20px 0px;
                            border-collapse: collapse;">
                        <caption class="captions-image"
                          style="
                            color: #ffffff !important;
                            text-align: left !important;
                            /* text-align: center; */
                            background: #008174 !important;
                            padding: 10px !important;
                            font-weight: 700 !important;
                            font-size: 20px !important;
                            border-top-left-radius: 10px !important;
                            border-top-right-radius: 10px !important;
                            caption-side: top !important;
                            border-collapse: collapse;">
                            Application/Performance
                            </caption>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Model	</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_model}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Application (Radiator / Heater )</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.application_radiator__heater_}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle manufacturer</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_manufacturer}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Make/Year	</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_makeyear}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Sub Application</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.sub_application}}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
                            margin: 20px 0px;
                            border-collapse: collapse;
                            margin-top:10px">
                        <caption class="captions-image"
                          style="
                            color: #ffffff !important;
                            text-align: left !important;
                            /* text-align: center; */
                            background: #008174 !important;
                            padding: 10px !important;
                            font-weight: 700 !important;
                            font-size: 20px !important;
                            border-top-left-radius: 10px !important;
                            border-top-right-radius: 10px !important;
                            caption-side: top !important;
                            border-collapse: collapse;" 
                        >
                            Dimensions
                        </caption>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Inner Diameter A (MM)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.inner_diameter_a_mm}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Inner Diameter B (MM)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.inner_diameter_b_mm}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Thickness</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.thickness}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Outer Diameter A (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.outer_diameter_a_mm}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Outer Diameter B (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.outer_diameter_b_mm}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Central axis length (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.central_axis_length_mm}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Product weight (grams)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.product_weight_grams}}</td>
                            </tr>
                        </tbody>
                    </table>
                    
                </div>'''
    
   
     # Get the PDF buffer
    pdf_buffer = get_pdf(html_content_internal)

        # Add watermark to the PDF
    pdf_with_watermark, rendered_content = add_watermark(pdf_buffer, part_no, image_paths, getAllValues, html_content_internal)

        # Set response properties for downloading the PDF
    frappe.response.filename = "test_with_watermark.pdf"
    frappe.response.filecontent = pdf_with_watermark
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"

        # Render the HTML content (not being used in the current code)
    print(rendered_content)

def add_watermark(pdf_buffer, part_no, image_paths, getAllValues,html_content_internal):
    watermark_text = "Confidential - Internal Use Only"
    watermark_font_size = 64
    watermark_opacity = 0.3

    # Create a PDF reader
    pdf_reader = PdfReader(io.BytesIO(pdf_buffer))

    # Create a PDF writer
    pdf_writer = PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]

        # Create a buffer to store the modified page
        output_buffer = io.BytesIO()

        # Create a PDF canvas for the modified page
        pdf_canvas = canvas.Canvas(output_buffer, pagesize=(page.mediaBox.getWidth(), page.mediaBox.getHeight()))

        # Set font and size
        pdf_canvas.setFont("Helvetica", watermark_font_size)
        pdf_canvas.rotate(55)
        pdf_canvas.setFillAlpha(watermark_opacity)

        # Calculate center coordinates of the page
        center_x = page.mediaBox.getLowerRight_x() / 1.2
        center_y = page.mediaBox.getLowerRight_y() / 2

        # Draw the watermark text on the center of the page
        pdf_canvas.drawCentredString(center_x, center_y, watermark_text)

        # Save the canvas content to the buffer
        pdf_canvas.save()

        # Merge the original page with the modified page
        page.mergePage(PdfReader(io.BytesIO(output_buffer.getvalue())).getPage(0))

        # Add the modified page to the PDF writer
        pdf_writer.addPage(page)

    # Save the PDF with watermark to a buffer
    output_buffer = io.BytesIO()
    pdf_writer.write(output_buffer)
    output_buffer.seek(0)

    # Render HTML content (not being used in the current code)
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_content_internal)
    rendered_content = template.render(part_no=part_no, image_paths=image_paths, getAllValues=getAllValues)

    return output_buffer.read(), rendered_content






