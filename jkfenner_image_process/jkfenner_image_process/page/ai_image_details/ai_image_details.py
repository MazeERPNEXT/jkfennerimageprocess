import frappe
from frappe.utils.pdf import get_pdf
 
@frappe.whitelist(allow_guest=True)
def generate_pdf():

    html_content = ''
    
 
    # Add items to PDF HTML
    html_content += '''<div class="layout-main-section" id="element-to-print">
                            <img style="width:37%; height:auto" src="/assets/jkfenner_image_process/images/JK-finner.png">
                        <div  >
                            <h5 id="slider-value" style="font-size:18px; text-align:center" class="card-title-viewimage">Matching Percentage: 90%</h5>
                            <img id="slider-image" style="width:100%" src="/assets/jkfenner_image_process/images/E70657-1.jpg" alt="Image 1">
                        </div>
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
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">Export</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Part No.</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">E72262</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Part Description</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">DAYCO CURVED RADIATOR HO</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">SAP Asset Code</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">72262</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Type of Hose</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">Branched</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Toolings Created on</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">22-12-2023</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">EAN</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">1840129806607</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">UPC</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">840129806608</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 1 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">67192</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 2 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">67193</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Customer 3,4,5 (Cross Ref)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">67194</td>
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
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">SUV300</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Application (Radiator / Heater )</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">Radiator</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle manufacturer</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">Mahindra</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Vehicle Make/Year	</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">2021</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Sub Application</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">Null</td>
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
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">20.0 / 23.0 / 26.0</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Inner Diameter B (MM)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">44.0 / 48.5</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Thickness</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">200</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Outer Diameter A (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">22.2 / 24.1 / 27.2</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Outer Diameter B (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">46.2 / 50.1</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Central axis length (mm)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">220 / 935 / 930 / 654 /920</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;" scope="row">Product weight (grams)</td>
                                <td style="border: 1px solid #23232457;width: 33%;padding: 0.5rem;border-collapse: collapse;">2.270</td>
                            </tr>
                        </tbody>
                    </table>
                    
                </div>'''
    
# Append the rendered HTML to the page body
    frappe.publish_realtime('html', html_content, user=frappe.session.user)
 
    pdf_content = get_pdf(html_content)
 
   
    frappe.response.filename = "test.pdf"
    frappe.response.filecontent = pdf_content
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"