import frappe
from frappe.utils.pdf import get_pdf
from reportlab.pdfgen import canvas 
from PyPDF2 import PdfReader, PdfWriter, PageObject
import io  
from jinja2 import Environment, FileSystemLoader
from ..ai_image_search.ai_image_search import guess_image
from urllib.parse import urljoin
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def get_image_ai_details(part_no, scores=None, image=""):
    part_no =  frappe.form_dict.get('part_no')
    result = frappe.get_all('JKFenner Image AI', filters={'part_no': part_no})
    image_paths = []
    product_dimensions = []
   

    getAllValues = None
    if result:
        x = result[0].name 
        getAllValues = frappe.get_doc('JKFenner Image AI', x)
        if hasattr(getAllValues, 'multiple_image_upload'):
            image_paths = [ child_row.images for child_row in getAllValues.multiple_image_upload]
        
        
        
        if hasattr(getAllValues, 'product_dimensions'):
            
            for child_row in getAllValues.product_dimensions:
                inner_diameter_1_mm = child_row.inner_diameter_1_mm
                inner_diameter_2_mm = child_row.inner_diameter_2_mm
                thickness = child_row.thickness
                length = child_row.length
                product_dimensions.append({
                    'inner_diameter_1_mm': inner_diameter_1_mm,
                    'inner_diameter_2_mm': inner_diameter_2_mm,
                    'thickness': thickness,
                    'length': length
                    })
            print(product_dimensions)    
    image_html_content = """ 
                    <div>
                        <p style="text-align: center; font-size: 20px;">{{getAllValues.part_no}}</p>
                    </div>
                    <div class="slide-container">
                          
                                <div class="slide fade">
                                    <h5 id="slider-value" class="card-title-viewimage">Matching Percentage: {{scores}}%</h5>
                                    <img class="details-image" id="slider-image" src="{{ image }}" alt="Image 1">
                                </div>
                            
                        <a href="#" class="prev" title="Previous">&#10094;</a>
                        <a href="#" class="next" title="Next">&#10095;</a>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
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
                        <div class="col-md-4">
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
                        <div class="col-md-4">
                            <table class="table table-bordered">
                                <caption class="captions-image">Product Dimensions</caption>
                                <tbody>
                                {% for product_dimension in product_dimensions %}
                                    <tr>
                                        <td scope="row">ID A1 (mm)</td>
                                        <td>{{ product_dimension.inner_diameter_1_mm }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">ID A2 (mm)</td>
                                        <td>{{ product_dimension.inner_diameter_2_mm }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Thickness </td>
                                        <td>{{ product_dimension.thickness }}</td>
                                    </tr>
                                    <tr>
                                        <td scope="row">Length (mm)</td>
                                        <td>{{ product_dimension.length }}</td>
                                    </tr>
                                {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                 """
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(image_html_content)
    rendered_content = template.render(part_no=part_no, image_paths=image_paths, product_dimensions=product_dimensions, getAllValues=getAllValues, scores=scores,image=image)
    print(image_paths,product_dimensions)
    return rendered_content

@frappe.whitelist(allow_guest=True)
def generate_internal_pdf(part_no, scores=None, image=""):
    part_no = frappe.form_dict.get('part_no')
    result = frappe.get_all('JKFenner Image AI', filters={'part_no': part_no})
    image_paths = []
    site_url = get_url()
    product_dimensions = []
    getAllValues = None
    
    if result:
        x = result[0].name
        getAllValues = frappe.get_doc('JKFenner Image AI', x)
    
        # if hasattr(getAllValues, 'multiple_image_upload'):
        #     image_paths = [urljoin(site_url, child_row.images) for child_row in getAllValues.multiple_image_upload]
        image_paths = [urljoin(site_url, image)]
        
        
        if hasattr(getAllValues, 'product_dimensions'):
            for child_row in getAllValues.product_dimensions:
                inner_diameter_1_mm = child_row.inner_diameter_1_mm
                inner_diameter_2_mm = child_row.inner_diameter_2_mm
                thickness = child_row.thickness
                length = child_row.length
                product_dimensions.append({
                    'inner_diameter_1_mm': inner_diameter_1_mm,
                    'inner_diameter_2_mm': inner_diameter_2_mm,
                    'thickness': thickness,
                    'length': length
                    })
    html_content_internal = ''' 
                        <style>
                                .table-bordered {
                                    border-collapse: collapse;
                                    width:80%;
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
                            </style>   
                            <div class="header" style="position: relative;width:100%;height: 4cm;background: #eee;display:flex; margin-top:-10px;bottom:10px;margin-bottom:10px">
                                <img style="width: 33%; height:150px;justify-content:center" src="{{ site_url }}/assets/jkfenner_image_process/images/JK-finner.png">
                            </div> 
                            <hr>   
                            {% for image_path in image_paths %}                      
                                <div >
                                    <img id="slider-image" style="width:25%;margin-left:200px;z-index:200; margin-top:0px;position:relative; bottom:20px height:240px" src="{{ image_path }}" alt="Image 1">
                                </div>
                            {% endfor %} 
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
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
                                <td " scope="row">Part No.</td>
                                <td ">{{getAllValues.part_no}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Customer</td>
                                <td ">{{getAllValues.customer}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Cross Ref.Part No 1</td>
                                <td ">{{getAllValues.cross_ref_part_no_1}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Cross Ref.Part No 2</td>
                                <td ">{{getAllValues.cross_ref_part_no_2}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Hose Type</td>
                                <td ">{{getAllValues.hose_type}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Development status</td>
                                <td ">{{getAllValues.development_status}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Export / Domestic AAM</td>
                                <td ">{{getAllValues.export__domestic_aam}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">Product SAP Code</td>
                                <td ">{{getAllValues.product_sap_code}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">EAN</td>
                                <td ">{{getAllValues.ean_no}}</td>
                            </tr>
                            <tr>
                                <td " scope="row">UPC</td>
                                <td ">{{getAllValues.upc_no}}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
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
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
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
                         Product Dimensions
                        </caption>
                        <tbody>
                        {% for product_dimension in product_dimensions %}
                            <tr>
                                <td  scope="row">ID A1 (mm)</td>
                                <td >{{ product_dimension.inner_diameter_1_mm }}</td>
                            </tr>
                            <tr>
                                <td  scope="row">ID A2 (mm)</td>
                                <td >{{ product_dimension.inner_diameter_2_mm }}</td>
                            </tr>
                            <tr>
                                <td  scope="row">Thickness</td>
                                <td >{{ product_dimension.thickness }}</td>
                            </tr>
                            <tr>
                                <td  scope="row">Length (mm)</td>
                                <td >{{ product_dimension.length }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                '''
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_content_internal)
    rendered_content = template.render(part_no=part_no, image_paths=image_paths,product_dimensions=product_dimensions, getAllValues=getAllValues, site_url=site_url, scores=scores, image=image)

    # file = open("/tmp/jkfenner.html", "w")
    # file.write(rendered_content)
    # file.close()
    
    # Get the PDF buffer
    pdf_buffer = get_pdf(rendered_content)

    # Add watermark to the PDF
    pdf_with_watermark = add_watermark(pdf_buffer, part_no, image_paths, getAllValues, html_content_internal)

        # Set response properties for downloading the PDF
    frappe.response.filename = "test_with_watermark.pdf"
    frappe.response.filecontent = pdf_with_watermark
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"

        # Render the HTML content (not being used in the current code)
    # print(rendered_content)

def add_watermark(pdf_buffer, part_no, image_paths, getAllValues,html_content_internal):
    watermark_text = "Confidential - Internal Use Only"
    watermark_font_size = 57
    watermark_opacity = 0.1

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
    # env = Environment(loader=FileSystemLoader("."))
    # template = env.from_string(html_content_internal)
    # rendered_content = template.render(part_no=part_no, image_paths=image_paths, getAllValues=getAllValues)

    return output_buffer.read() #, rendered_content



@frappe.whitelist(allow_guest=True)
def generate_client_pdf(part_no, scores=None, image=""):
    part_no = frappe.form_dict.get('part_no')
    result = frappe.get_all('JKFenner Image AI', filters={'part_no': part_no})
    image_paths = []
    site_url = get_url()
    product_dimensions = []
    getAllValues = None
    
    if result:
        x = result[0].name
        getAllValues = frappe.get_doc('JKFenner Image AI', x)
    
        # if hasattr(getAllValues, 'multiple_image_upload'):
        #     image_paths = [urljoin(site_url, child_row.images) for child_row in getAllValues.multiple_image_upload]
        image_paths = [urljoin(site_url, image)]
        
        if hasattr(getAllValues, 'product_dimensions'):
            for child_row in getAllValues.product_dimensions:
                inner_diameter_1_mm = child_row.inner_diameter_1_mm
                inner_diameter_2_mm = child_row.inner_diameter_2_mm
                thickness = child_row.thickness
                length = child_row.length
                product_dimensions.append({
                    'inner_diameter_1_mm': inner_diameter_1_mm,
                    'inner_diameter_2_mm': inner_diameter_2_mm,
                    'thickness': thickness,
                    'length': length
                    })
    html_content_client = '''
    <style>
                                .table-bordered {
                                    border-collapse: collapse;
                                    width:80%;
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
                            </style>
                         <div class="header" style="position: relative;width:100%;height: 4cm;background: #eee;display:flex; margin-top:-10px;bottom:10px;margin-bottom:10px">
                                <img style="width: 33%; height:150px;justify-content:center" src="{{ site_url }}/assets/jkfenner_image_process/images/JK-finner.png">
                            </div> 
                            <hr>  
                            {% for image_path in image_paths %}                      
                                <div >
                                    <img id="slider-image" style="width:25%;margin-left:200px;z-index:200; margin-top:0px;position:relative; bottom:20px height:240px" src="{{ image_path }}" alt="Image 1">
                                </div>
                            {% endfor %}  
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
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
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Part No.</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.part_no}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.customer}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Hose Type</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.hose_type}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Development status</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.development_status}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Export / Domestic AAM</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.export__domestic_aam}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Product SAP Code</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.product_sap_code}}</td>
                            </tr>
                            
                        </tbody>
                    </table>
                    <table class="table table-bordered" 
                            style="border: 1px solid #1819194f;
                            white-space: nowrap;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            font-size: inherit;
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
                            Product Application
                            </caption>
                        <tbody>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Manufacturer	</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_manufacturer}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Model</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_model}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Make Year	</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.vehicle_make_year}}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Hose Application</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{getAllValues.hose_application}}</td>
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
                          Product  Dimensions
                        </caption>
                        <tbody>
                            {% for product_dimension in product_dimensions %}
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">ID A1 (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{ product_dimension.inner_diameter_1_mm }}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">ID A2 (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{ product_dimension.inner_diameter_2_mm }}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Thickness</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{ product_dimension.thickness }}</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Length (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">{{ product_dimension.length }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    
                </div>'''
    env = Environment(loader=FileSystemLoader("."))
    template = env.from_string(html_content_client)
    rendered_content = template.render(part_no=part_no, image_paths=image_paths,product_dimensions=product_dimensions, getAllValues=getAllValues, site_url=site_url, scores=scores, image=image)

    # file = open("/tmp/jkfenner.html", "w")
    # file.write(rendered_content)
    # file.close()
    
    # Get the PDF buffer
    pdf_buffer_client = get_pdf(rendered_content)

        # Add watermark to the PDF
    pdf_with_watermark = add_watermark_client(pdf_buffer_client, part_no, image_paths, getAllValues, html_content_client)

        # Set response properties for downloading the PDF
    frappe.response.filename = "test_with_watermark.pdf"
    frappe.response.filecontent = pdf_with_watermark
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"

        # Render the HTML content (not being used in the current code)
    # print(rendered_content)

def add_watermark_client(pdf_buffer_client, part_no, image_paths, getAllValues,html_content_client):
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




