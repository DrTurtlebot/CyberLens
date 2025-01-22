import os
import random
import traceback
from pydantic import AnyUrl
from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from openai import OpenAI
from app.core import settings
from app.common import utils
from app.routes import abuseipdb, proxycheck, virustotal, registrar
from app.common.models import RequestDataModel
import logfire

# Set up the router
router = APIRouter(prefix="/summary")


# Define the function to be used by the fetch_data_api_with_cache function
# check if data is in cache
async def summary_function(input_data: RequestDataModel):
    with logfire.span("SummaryFunction"):
        # Get the target IP and the AbuseIPDB API key and address
        # target_ip = utils.process_address_to_ip(input_data)
        input_data
        # This is really weirdly coded, but it works and still allows queing, todo fix later!
        tempdata = {}
        datatype = utils.check_data_type(input_data)
        if datatype in ["url", "ip"]:
            tempdata.update({"ABUSEIPDB": await abuseipdb.request_data(input_data)})
            tempdata.update({"PROXY": await proxycheck.request_data(input_data)})
            tempdata.update({"VIRUS": await virustotal.request_data(input_data)})
        if datatype in ["hash"]:
            tempdata.update({"VIRUS": await virustotal.request_data(input_data)})
        try:
            AnyUrl.validate(input_data)
            tempdata.update({"REGISTRAR": await registrar.request_data(input_data)})
        except Exception:
            tempdata.update({"REGISTRAR": {"error": "True"}})

        data = {}
        # set Summary Info
        # Get ABUSE IPDB Info
        if "ABUSEIPDB" in tempdata and "InvalidAPIUrl" not in tempdata["ABUSEIPDB"]:
            abuse_data = tempdata["ABUSEIPDB"].get("data", {})
            
            data.update({"Inputed_string": input_data})
            data.update({"Abuse_IP": abuse_data.get("ipAddress", "N/A")})
            data.update({"Abuse_Score": abuse_data.get("abuseConfidenceScore", "N/A")})
            data.update({"Abuse_CountryName": abuse_data.get("countryName", "N/A")})
            data.update({"Abuse_CountryCode": abuse_data.get("countryCode", "N/A")})
            data.update({"Abuse_ISP": abuse_data.get("isp", "Unknown")})
            data.update({"Abuse_Reports": abuse_data.get("totalReports", 0)})

            # Handle AbuseIPDB Reports Details
            reports = abuse_data.get("reports", [])
            if reports:
                # Randomly sample up to 10 reports
                random_reports = random.sample(reports, min(10, len(reports)))
                # Extract only the comments from the sampled reports
                comments = [report.get("comment", "") for report in random_reports]
                # Update the data dictionary with only the comments
                data.update({"Abuse_Reports_Comments": comments})

        # Get ProxyCheck Ip
        if "PROXY" in tempdata:
            proxy_keys = list(tempdata["PROXY"].keys())
            proxy_ip_key = next((key for key in proxy_keys if key != "status"), None)
            if "InvalidAPIUrl" not in tempdata["PROXY"]:
                proxy_data = tempdata["PROXY"].get(proxy_ip_key, {})
                print("running summary check for proxy")
                data.update({"Proxy_IP": proxy_ip_key})
                data.update({"Proxy_ISOCountry": proxy_data.get("isocode", "N/A")})  # Default to "N/A" if key doesn't exist
                data.update({"Proxy_Country": proxy_data.get("country", "N/A")})
                data.update({"Proxy_Proxy": proxy_data.get("proxy", "Unknown")})
                data.update({"Proxy_Type": proxy_data.get("type", "Unknown")})
                data.update({"Proxy_City": proxy_data.get("city", "Unknown")})
                data.update({"Proxy_Organ": proxy_data.get("organisation", "Unknown")})
                print(proxy_data)

        # Get Registrar Info
        # example registrar data {'domain': {'id': '3211695_DOMAIN_COM-VRSN', 'domain': 'epic.com', 'punycode': 'epic.com', 'name': 'epic', 'extension': 'com', 'whois_server': 'whois.godaddy.com', 'status': ['clientdeleteprohibited', 'clientrenewprohibited', 'clienttransferprohibited', 'clientupdateprohibited'], 'name_servers': ['dns-public-a.epic.com', 'dns-public-b.epic.com'], 'dnssec': True, 'created_date': '1990-08-23T04:00:00Z', 'created_date_in_time': '1990-08-23T04:00:00Z', 'updated_date': '2022-09-06T08:13:03Z', 'updated_date_in_time': '2022-09-06T08:13:03Z', 'expiration_date': '2025-09-18T11:59:59Z', 'expiration_date_in_time': '2025-09-18T11:59:59Z'}, 'registrar': {'id': '146', 'name': 'GoDaddy.com, LLC', 'phone': '480-624-2505', 'email': 'abuse@godaddy.com', 'referral_url': 'http://www.godaddy.com'}}
        if "REGISTRAR" in tempdata:
            if "InvalidAPIUrl" not in tempdata["REGISTRAR"]:
                try:
                    registrar_data = tempdata["REGISTRAR"]
                    
                    # Check for "error" key
                    if "error" in registrar_data:
                        data.update({"Registrar_Error": registrar_data.get("error", "Unknown")})
                    else:
                        # Use .get() to safely access nested keys
                        domain_info = registrar_data.get("domain", {})
                        registrar_info = registrar_data.get("registrar", {})

                        data.update({"Registrar_WHOIS": domain_info.get("whois_server", "N/A")})
                        data.update({"Registrar_Name": registrar_info.get("name", "Unknown")})
                        data.update({"Registrar_Created": domain_info.get("created_date", "N/A")})
                        data.update({"Registrar_Updated": domain_info.get("updated_date", "N/A")})
                        data.update({"Registrar_Expire": domain_info.get("expiration_date", "N/A")})

                        # Check for "registrant" key
                        data.update({"Registrar_Data_Found": "registrant" in registrar_data})
                except Exception as e:
                    data.update({"Registrar_Error": "True"})
        # Get VirusTotal Info
        # check if tempdata["VIRUS"] contains an element called error
        if "VIRUS" in tempdata:
            if "InvalidAPIUrl" not in tempdata["VIRUS"]:
                virus_data = tempdata["VIRUS"]

                # Check for "error" key
                if "error" in virus_data:
                    logfire.error(
                        "VirusTotal Error: {value}", value=virus_data.get("error", "Unknown")
                    )
                    data.update({"Virus_Error": virus_data.get("error", "Unknown")})
                else:
                    # Use .get() for safe key access
                    data.update({"Virus_Stats": virus_data.get("analysis_stats", {})})

                    # Handle "hash" data type
                    if "hash" in virus_data.get("data_type", ""):
                        attributes = virus_data.get("all", {}).get("attributes", {})
                        threat_classification = attributes.get(
                            "popular_threat_classification", {}
                        )

                        data.update({"Virus_Type": "Hash"})
                        data.update({"Virus_Name": attributes.get("meaningful_name", "N/A")})
                        data.update({"Virus_Magic": attributes.get("magic", "N/A")})
                        data.update(
                            {
                                "Virus_ThreatCategory": threat_classification.get(
                                    "popular_threat_category", "N/A"
                                )
                            }
                        )

        # Used if you just want to return an unformatted dict of the data collected, used for OpenAI
        return data


# Request Data from the Summary API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    try:
        """Get Summary Data"""

        return await utils.fetch_data_api_with_cache(
            "Summary", input_data, summary_function
        )

    except Exception:
        logfire.error("{error}", error=traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "detail": {
                    "type": "internal_error_si",
                    "msg": "See Sys Admin >:(",
                    "info": "did you give a full address? 🤔 http://www.website.com",
                }
            },
        )


# Function to draw the favicon and title on each page
def draw_header(canvas, doc):
    # Set up the document width and height
    width, height = A4

    # Title settings
    title_text = "CyberLens Analysis Report"
    title_font_size = 16
    title_width = canvas.stringWidth(title_text, "Helvetica-Bold", title_font_size)

    # Calculate x-position to center the title
    title_x = (width - title_width) / 2
    title_y = height - 50  # Y position of the title

    # Favicon settings
    favicon_path = "assets/favicon.png"
    favicon_width = 50
    favicon_height = 50

    # Calculate x-position for the favicon to align its center with the title
    favicon_x = title_x - (favicon_width / 2) - 60  # Adjust as needed for spacing
    favicon_y = title_y - 15  # Adjust the Y position to align visually with the title

    # Draw the favicon image
    canvas.drawImage(
        favicon_path,
        favicon_x,
        favicon_y,
        width=favicon_width,
        height=favicon_height,
        mask="auto",
    )

    # Draw the title
    canvas.setFont("Helvetica-Bold", title_font_size)
    canvas.drawString(title_x, title_y, title_text)


# Function to parse and format the response text
def parse_response_text(response_text, body_style, title_style):
    elements = []
    lines = response_text.split("\n")  # Split the text into lines

    for line in lines:
        line = line.strip()  # Remove leading and trailing spaces

        # Check if the line is a title
        if line.startswith("**") and line.endswith("**"):
            title = line.replace("**", "").strip()  # Remove ** and extra spaces
            elements.append(Paragraph(title, title_style))  # Add as a title paragraph
        elif line:  # Add normal paragraphs if not empty
            elements.append(Paragraph(line, body_style))

        elements.append(Spacer(1, 5))  # Add space between paragraphs

    return elements


# Function to delete all files in the reports folder, but not the folder itself
def delete_files(folder_path: str):
    try:
        # Iterate through each file in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if it is a file (not a subdirectory) and then delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        logfire.error(
            "Error deleting files in {folder_path}: {e}", folder_path=folder_path, e=e
        )


# Summary PDF generator
@router.post("/generate_report")
async def generate_report(input_data: str = Body(..., embed=False)):
    with logfire.span("GenerateReport"):
        try:
            # make sure the reports folder exists
            if not os.path.exists("reports"):
                logfire.info("Creating reports folder")
                os.makedirs("reports")
            logfire.info("Deleting old reports")
            delete_files("reports")  # Delete all files in the reports folder

            # Get a dict of the data collected
            temp_data = await summary_function(input_data)
            sanitised_data = (
                str(temp_data).replace("'", "").replace("{", "").replace("}", "")
            )  # Use this to reduce the token count

            # Beginning Prompt
            ai_prompt = """you are a report maker for a cyber security firm
            , Given the Following Data set, create a brief summary, 
            of the information provided. Please just use paragraphs. Follow this 
            style, Summary, Details, Other(If needed), Conclusion, and 
            Recommendations, All titles need to be returned back with this style **Title:** so that 
            I can understand the structure, and use /n for new lines. also a title must be on its own line, please be technical but also understandable by a client"""

            # Generate the response
            openai_client = OpenAI(api_key=settings.main.ENV_API_OPENAI_KEY)
            with logfire.span("AI Request Made..."):
                response = openai_client.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": ai_prompt},
                        {"role": "user", "content": sanitised_data},
                    ],
                )
                response_text = response.choices[0].message.content
            logfire.info("Response from OpenAI received")
            # Set up the PDF document
            file_name = f"reports/{hash(input_data)}-report.pdf"
            doc = SimpleDocTemplate(file_name, pagesize=A4)

            # Define styles
            styles = getSampleStyleSheet()
            body_style = styles["Normal"]
            body_style.fontSize = 12
            body_style.leading = 14  # Adjust line spacing if needed

            # Create elements to add to the document
            elements = []

            # Add Title
            title_style = ParagraphStyle(
                name="Title",
                parent=styles["Normal"],
                fontSize=14,
                leading=12,
                spaceAfter=6,
                textColor=colors.black,
                alignment=0,  # Center alignment for titles
            )

            # Add Disclaimer below the title
            disclaimer_style = ParagraphStyle(
                name="Disclaimer",
                fontSize=6,
                leading=8,
                alignment=1,  # Center alignment
                textColor=colors.black,
            )
            disclaimer_text = (
                "**DISCLAIMER:**\n This report was generated using AI models such as GPT-4o, and may not be 100% accurate. "
                "Please verify the information on cyberlens.online before taking any action. This report is also only generated using publicly available data "
                "and does not use any private client data. All sources of data are from APIs where the only input is input string given, e.g., IP or URL. "
                "CyberLens in its current state should NOT be used for any legal or commercial purposes. It is for educational purposes in its current state."
            )
            disclaimer_paragraph = Paragraph(disclaimer_text, disclaimer_style)
            elements.append(disclaimer_paragraph)
            elements.append(Spacer(1, 10))  # Add space after disclaimer

            # Parse and format the response text
            # Assuming parse_response_text is a function to format text based on response
            response_elements = parse_response_text(
                response_text, body_style, title_style
            )
            elements.extend(response_elements)

            # Create a frame for the main content area (leaving space for header/footer)
            frame = Frame(40, 40, A4[0] - 80, A4[1] - 120, id="main_frame")

            # Define a page template with a custom drawing function for the header
            template = PageTemplate(
                id="page_template", frames=[frame], onPage=draw_header
            )
            doc.addPageTemplates([template])

            # Build the document with the elements
            doc.build(elements)

            logfire.info(f"Report generated for: {input_data}")

            return FileResponse(
                path=file_name,
                filename="CyberLens_Report.pdf",
                media_type="application/pdf",
            )

        except Exception:
            logfire.error("{error}", error=traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail={
                    "detail": {
                        "type": "internal_error_si",
                        "msg": "See Sys Admin >:(",
                        "info": "Did you give a full address? 🤔 http://www.website.com",
                    }
                },
            )
