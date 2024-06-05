import frappe
from frappe.utils.pdf import get_pdf
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter, PageObject
import io  
from jinja2 import Environment, FileSystemLoader
from ..ai_image_search.ai_image_search import guess_image
from urllib.parse import urljoin
from frappe.utils import get_url
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_image_ai_details(parent_ref=None, child_ref=None):
    image_paths = []
    matching_find_images = []
    site_url = get_url() 
    upload_image_doc = frappe.get_doc('JKFenner Image Details Stored', child_ref)
    next_image_doc = None
    previous_image_doc = None
    app_settings = frappe.get_doc("Application Settings", "Application Settings")
    last_data_set_date_str = app_settings.get("last_data_set_date")
    last_data_set_date = datetime.strptime(last_data_set_date_str, "%Y-%m-%d")
    formatted_last_data_set_date = last_data_set_date.strftime("%d-%b-%Y")
    try:
        previous_image_doc = frappe.get_last_doc('JKFenner Image Details Stored',filters=[['idx','=',upload_image_doc.idx-1], ["parent","=",parent_ref], ['idx','<',4]], order_by="idx asc")
    except frappe.DoesNotExistError:
        pass
    try:
        next_image_doc = frappe.get_last_doc('JKFenner Image Details Stored',filters=[['idx','=',upload_image_doc.idx+1], ["parent","=",parent_ref], ['idx','<',4]], order_by="idx asc")
    except frappe.DoesNotExistError:
        pass
    getAllValues = frappe.get_doc('JKFenner Image AI', upload_image_doc.part_no)
    
    if hasattr(getAllValues, 'multiple_image_upload'):
        image_paths = [ child_row.images for child_row in getAllValues.multiple_image_upload]
    image_html_content = """ 
                    <div>
                       
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <p style="text-align: center; font-size: 20px;">{{getAllValues.part_no}}</p>
                            <div class="slide-container">
                                <div class="slide fade">
                                    <h5 id="slider-value" class="card-title-viewimage">Matching Percentage: {{upload_image_doc.matching_percentage}}%</h5>
                                    <img class="details-image" id="slider-image" src="{{ upload_image_doc.image_url }}" alt="Image 1">
                                </div>
                                <a href="#" data-href="{{ site_url +'/app/ai-image-details?child_table='+ previous_image_doc.name + "&parent_table="+ previous_image_doc.parent if previous_image_doc else "#" }}" class="prev navigation-button" title="Previous">&#10094;</a><button>
                                <a href="#" data-href="{{ site_url + '/app/ai-image-details?child_table='+ next_image_doc.name + "&parent_table="+ next_image_doc.parent if next_image_doc else "#" }}" class="next navigation-button" title="Next">&#10095;</a>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <table class="table table-bordered">
                                <caption class="captions-image">Generic Details</caption>
                                <tbody>
                                    <tr>
                                        <td scope="row">Part No.</td>
                                        <td>{{getAllValues.part_no}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Customer</td>
                                        <td>{{getAllValues.customer}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Cross Ref.Part No 1</td>
                                        <td>{{getAllValues.cross_ref_part_no_1}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Cross Ref.Part No 2</td>
                                        <td>{{getAllValues.cross_ref_part_no_2}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Hose Type</td>
                                        <td>{{getAllValues.hose_type}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Development status</td>
                                        <td>{{getAllValues.development_status}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Export / Domestic AAM</td>
                                        <td>{{getAllValues.export__domestic_aam}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Product SAP Code</td>
                                        <td>{{getAllValues.product_sap_code}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">EAN</td>
                                        <td>{{getAllValues.ean_no}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">UPC</td>
                                        <td>{{getAllValues.upc_no}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <table class="table table-bordered">
                                <caption class="captions-image">Product Application</caption>
                                <tbody>
                                    <tr>
                                        <td scope="row">Vehicle Manufacturer</td>
                                        <td>{{getAllValues.vehicle_manufacturer}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Vehicle Model</td>
                                        <td>{{getAllValues.vehicle_model}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Vehicle Make Year</td>
                                        <td>{{getAllValues.vehicle_make_year}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Hose Application</td>
                                        <td>{{getAllValues.hose_application}}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Sub Application </td>
                                        <td>{{getAllValues.sub_application}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="col-md-6">
                            <table class="table table-bordered">
                                <caption class="captions-image">Product Dimensions</caption>
                                <tbody>
                                    <tr>
                                        <td scope="row">ID A1 (mm)</td>
                                        <td>{{ upload_image_doc.id_a1 }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">ID A2 (mm)</td>
                                        <td>{{ upload_image_doc.id_a2 }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Thickness </td>
                                        <td>{{ upload_image_doc.thickness }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Length (mm)</td>
                                        <td>{{ upload_image_doc.length }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="disclimar" style="border: 1px solid lightgray;border-radius: 5px;padding: 11px;background-color: #d3d3d329;">
                            <p><b style="color:blue">AI-Generated Content: </b> The responses you receive are produced by an AI system based on the information available up to <span id="knowledge_tv">Knowledge Cutoff Date: {{ formatted_last_data_set_date }}</span>. This system is designed to provide reasonably accurate and relevant information, but it may not always reflect the most accurate match and specific nuances of your situation.</p>
                            <p><b style="color:blue">Verification Recommended: </b> We recommend verifying any critical information, design or advice provided by the AI with additional reliable sources. Please consult with a human expert if you have any specific concerns or require professional guidance.</p>
                            <p><b style="color:blue">Continuous Improvement: </b>AI systems are continually improving, and we welcome your feedback to enhance the quality and accuracy of the responses. If you encounter any issues or inaccuracies, please let us know.</p>
                        </div>
                    </div>
                 """
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(image_html_content)
    rendered_content = template.render(getAllValues=getAllValues, previous_image_doc=previous_image_doc, next_image_doc = next_image_doc, upload_image_doc = upload_image_doc, site_url=site_url)
    print(image_paths,matching_find_images)
    return rendered_content

@frappe.whitelist(allow_guest=True)
def generate_internal_pdf(parent_ref=None, child_ref=None):
    image_paths = []
    matching_find_images = []
    site_url = get_url()
    upload_image_doc = frappe.get_doc('JKFenner Image Details Stored', child_ref)
        
    getAllValues = frappe.get_doc('JKFenner Image AI', upload_image_doc.part_no)
    
    if hasattr(getAllValues, 'multiple_image_upload'):
        image_paths = [ child_row.images for child_row in getAllValues.multiple_image_upload]
    html_content_internal = ''' 
                        <style>
                                
                                .table-bordered {
                                    border-collapse: collapse;
                                    width:95%;
                                    margin-left:20px;
                                    margin-bottom:20px;
                                }
                                .table-bordered th,
                                .table-bordered td {
                                    border: 2px solid #dddddd;
                                    padding: 8px;
                                    text-align: left;
                                    border-right-color: #dddddd;
                                    border-right-width: medium;
                                }
                                .table-bordered th {
                                    background-color: #f2f2f2;
                                }
                                .grid-container{
                                    display: flex;
                                    column-gap:0px;
                                    grid-template-columns: auto auto;
                                    width:100%
                                }
                                .grid-item{
                                    padding: 10px;
                                    width:100%;
                                }
                                .disclimar{
                                    border: 1px solid lightgray;
                                    border-radius: 5px;
                                    padding: 11px;
                                    background-color: #d3d3d329;
                                }
                                .disclimar p b {
                                    color: blue;
                                }
                            </style>   
                            <div class="header" style="position: relative;width:100%;height: 4cm;background: #eee;display:flex; margin-top:-10px;bottom:10px;margin-bottom:10px">
                                <img style="width: 33%; height:150px;justify-content:center;" src="{{ site_url }}/assets/jkfenner_image_process/images/JK-finner.png">
                            </div> 
                            <hr>  
                                <div>
                                    <img id="slider-image" style="width:41%;margin-left:200px;z-index:200; margin-top:0px;margin-bottom:20px;position:relative; bottom:20px height:240px" src="{{ upload_image_doc.image_url }}" alt="Image 1">
                                </div>
                               <div class="grid-container">
                               <div class="grid-item">
                                    <table class="table table-bordered">
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
                                                <td>Part No.</td>
                                                <td>{{getAllValues.part_no}}</td>
                                            </tr>
                                            <tr>
                                                <td>Customer</td>
                                                <td>{{getAllValues.customer}}</td>
                                            </tr>
                                            <tr>
                                                <td>Cross Ref.Part No 1</td>
                                                <td>{{getAllValues.cross_ref_part_no_1}}</td>
                                            </tr>
                                            <tr>
                                                <td >Cross Ref.Part No 2</td>
                                                <td>{{getAllValues.cross_ref_part_no_2}}</td>
                                            </tr>
                                            <tr>
                                                <td>Hose Type</td>
                                                <td>{{getAllValues.hose_type}}</td>
                                            </tr>
                                            <tr>
                                                <td>Development status</td>
                                                <td>{{getAllValues.development_status}}</td>
                                            </tr>
                                            <tr>
                                                <td>Export / Domestic AAM</td>
                                                <td>{{getAllValues.export__domestic_aam}}</td>
                                            </tr>
                                            <tr>
                                                <td>Product SAP Code</td>
                                                <td>{{getAllValues.product_sap_code}}</td>
                                            </tr>
                                            <tr>
                                                <td>EAN</td>
                                                <td>{{getAllValues.ean_no}}</td>
                                            </tr>
                                            <tr>
                                                <td>UPC</td>
                                                <td>{{getAllValues.upc_no}}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                               <div class="grid-item">
                               <table class="table table-bordered grid-item" style="width:50% !importent">
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
                                        Product Application
                                            </caption>
                                        <tbody>
                                            <tr>
                                                <td  scope="row">Vehicle Manufacturer	</td>
                                                <td >{{getAllValues.vehicle_manufacturer}}</td>
                                            </tr>
                                            <tr>
                                                <td  scope="row">Vehicle Model</td>
                                                <td >{{getAllValues.vehicle_model}}</td>
                                            </tr>
                                            <tr>
                                                <td  scope="row">Vehicle Make Year	</td>
                                                <td >{{getAllValues.vehicle_make_year}}</td>
                                            </tr>
                                            <tr>
                                                <td  scope="row">Hose Application</td>
                                                <td >{{getAllValues.hose_application}}</td>
                                            </tr>
                                            <tr>
                                                <td  scope="row">Sub Application</td>
                                                <td >{{getAllValues.sub_application}}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    </br>
                                    <table class="table table-bordered">
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
                                Product Dimensions
                                </caption>
                                <tbody>
                                    <tr>
                                        <td scope="row">ID A1 (mm)</td>
                                        <td>{{ upload_image_doc.id_a1 }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">ID A2 (mm)</td>
                                        <td>{{ upload_image_doc.id_a2 }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Thickness </td>
                                        <td>{{ upload_image_doc.thickness }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Length (mm)</td>
                                        <td>{{ upload_image_doc.length }}</td>
                                    </tr>
                                </tbody>
                            </table> 
                                 </div>
                                </div>  

                             
                            <div class="disclimar">
                                <p><b>AI-Generated Content: </b> The responses you receive are produced by an AI system based on the information available up to [Knowledge Cutoff Date: Month, Year]. This system is designed to provide reasonably accurate and relevant information, but it may not always reflect the most accurate match and specific nuances of your situation.</p>
                                <p><b>Verification Recommended: </b> We recommend verifying any critical information, design or advice provided by the AI with additional reliable sources. Please consult with a human expert if you have any specific concerns or require professional guidance.</p>
                                <p><b>Continuous Improvement: </b>AI systems are continually improving, and we welcome your feedback to enhance the quality and accuracy of the responses. If you encounter any issues or inaccuracies, please let us know.</p>
                            </div> 
                '''
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_content_internal)
    rendered_content = template.render(getAllValues=getAllValues, site_url=site_url,upload_image_doc = upload_image_doc,)

    # file = open("/tmp/jkfenner.html", "w")
    # file.write(rendered_content)
    # file.close()
    
    # Get the PDF buffer
    pdf_buffer = get_pdf(rendered_content)

    # Add watermark to the PDF
    pdf_with_watermark = add_watermark(pdf_buffer, getAllValues,site_url,upload_image_doc, html_content_internal)

        # Set response properties for downloading the PDF
    frappe.response.filename = "test_with_watermark.pdf"
    frappe.response.filecontent = pdf_with_watermark
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"

        # Render the HTML content (not being used in the current code)
    # print(rendered_content)

def add_watermark(pdf_buffer,getAllValues,site_url,upload_image_doc,html_content_internal,):
    watermark_text = "Confidential - Internal Use Only"
    watermark_font_size = 57
    watermark_opacity = 0.1
    page_layout =[]
    # Create a PDF reader
    pdf_reader = PdfReader(io.BytesIO(pdf_buffer))

    # Create a PDF writer
    pdf_writer = PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]

        # Create a buffer to store the modified page
        output_buffer = io.BytesIO()

        # Create a PDF canvas for the modified page
        pdf_canvas = canvas.Canvas(output_buffer, pagesize=letter)

        if page_layout == '/TwoColumn':
     

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
    # env = Environment(loader=FileSystemLoader("."))
    # template = env.from_string(html_content_internal)
    # rendered_content = template.render(part_no=part_no, image_paths=image_paths, getAllValues=getAllValues)

    return output_buffer.read() #, rendered_content



@frappe.whitelist(allow_guest=True)
def generate_client_pdf(parent_ref=None, child_ref=None):
    image_paths = []
    matching_find_images = []
    site_url = get_url()
    upload_image_doc = frappe.get_doc('JKFenner Image Details Stored', child_ref)
        
    getAllValues = frappe.get_doc('JKFenner Image AI', upload_image_doc.part_no)
    
    if hasattr(getAllValues, 'multiple_image_upload'):
        image_paths = [ child_row.images for child_row in getAllValues.multiple_image_upload]

    html_content_client = '''
                             <style>
                                
                                .table-bordered {
                                    border-collapse: collapse;
                                    width:95%;
                                    margin-left:20px;
                                    margin-bottom:20px;
                                }
                                .table-bordered th,
                                .table-bordered td {
                                    border: 2px solid #dddddd;
                                    padding: 8px;
                                    text-align: left;
                                    border-right-color: #dddddd;
                                    border-right-width: medium;
                                }
                                .table-bordered th {
                                    background-color: #f2f2f2;
                                }
                                .grid-container{
                                    display: flex;
                                    column-gap:0px;
                                    grid-template-columns: auto auto;
                                    width:100%
                                }
                                .grid-item{
                                    padding: 10px;
                                    width:100%;
                                }
                            </style>
                         <div class="header" style="position: relative;width:100%;height: 4cm;background: #eee;display:flex; margin-top:-10px;bottom:10px;margin-bottom:10px">
                                <img style="width: 33%; height:150px;justify-content:center" src="{{ site_url }}/assets/jkfenner_image_process/images/JK-finner.png">
                            </div> 
                            <hr>  
                                <div >
                                    <img id="slider-image" style="width:41%;margin-left:200px;z-index:200; margin-top:0px;position:relative; bottom:20px height:240px" src="{{ upload_image_doc.image_url }}" alt="Image 1">
                                </div>
                            <div class="grid-container">
                               <div class="grid-item">
                                <table class="table table-bordered">
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
                                        <td>Part No.</td>
                                        <td>{{getAllValues.part_no}}</td>
                                    </tr>
                                    <tr>
                                        <td>Customer</td>
                                        <td>{{getAllValues.customer}}</td>
                                    </tr>
                                    <tr>
                                        <td>Hose Type</td>
                                        <td>{{getAllValues.hose_type}}</td>
                                    </tr>
                                    <tr>
                                        <td>Development status</td>
                                        <td>{{getAllValues.development_status}}</td>
                                    </tr>
                                    <tr>
                                        <td>Export / Domestic AAM</td>
                                        <td>{{getAllValues.export__domestic_aam}}</td>
                                    </tr>
                                    <tr>
                                        <td>Product SAP Code</td>
                                        <td>{{getAllValues.product_sap_code}}</td>
                                    </tr>
                                    
                                </tbody>
                            </table>
                            </div>
                               <div class="grid-item">
                               <table class="table table-bordered grid-item" style="width:50% !importent">
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
                                    Product Application
                                    </caption>
                                <tbody>
                                    <tr>
                                        <td>Vehicle Manufacturer	</td>
                                        <td>{{getAllValues.vehicle_manufacturer}}</td>
                                    </tr>
                                    <tr>
                                        <td>Vehicle Model</td>
                                        <td>{{getAllValues.vehicle_model}}</td>
                                    </tr>
                                    <tr>
                                        <td>Vehicle Make Year	</td>
                                        <td>{{getAllValues.vehicle_make_year}}</td>
                                    </tr>
                                    <tr>
                                        <td>Hose Application</td>
                                        <td>{{getAllValues.hose_application}}</td>
                                    </tr>
                                    <tr>
                                        <td>Sub Application</td>
                                        <td>{{getAllValues.sub_application}}</td>
                                    </tr>
                                </tbody>
                            </table>
                           </div>
                                </div> 
                    <table class="table table-bordered" >
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
                          Product  Dimensions
                        </caption>
                        <tbody>
                            <tr>
                                <td>ID A1 (mm)</td>
                                <td>{{ upload_image_doc.id_a1 }}</td>
                            </tr>
                            <tr>
                                <td>ID A2 (mm)</td>
                                <td>{{ upload_image_doc.id_a2 }}</td>
                            </tr>
                            <tr>
                                <td>Thickness </td>
                                <td>{{ upload_image_doc.thickness }}</td>
                            </tr>
                            <tr>
                                <td>Length (mm)</td>
                                <td>{{ upload_image_doc.length }}</td>
                            </tr>
                        </tbody>
                    </table> '''
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_content_client)
    rendered_content = template.render(getAllValues=getAllValues, site_url=site_url,upload_image_doc = upload_image_doc,)

    # file = open("/tmp/jkfenner.html", "w")
    # file.write(rendered_content)
    # file.close()
    
    # Get the PDF buffer
    pdf_buffer_client = get_pdf(rendered_content)

        # Add watermark to the PDF
    pdf_with_watermark = add_watermark_client(pdf_buffer_client, getAllValues,site_url,upload_image_doc, html_content_client)

        # Set response properties for downloading the PDF
    frappe.response.filename = "test_with_watermark.pdf"
    frappe.response.filecontent = pdf_with_watermark
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"

        # Render the HTML content (not being used in the current code)
    # print(rendered_content)

def add_watermark_client(pdf_buffer_client, getAllValues, site_url, upload_image_doc,html_content_client):
    watermark_text_client = "Confidential"
    watermark_font_size = 100
    watermark_opacity = 0.1

    # Create a PDF reader
    pdf_reader = PdfReader(io.BytesIO(pdf_buffer_client))

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
        pdf_canvas.drawCentredString(center_x, center_y, watermark_text_client)

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
    # env = Environment(loader=FileSystemLoader("."))
    # template = env.from_string(html_content_client)
    # rendered_content = template.render(part_no=part_no, image_paths=image_paths, getAllValues=getAllValues)

    return output_buffer.read() #, rendered_content




