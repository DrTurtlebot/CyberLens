from fastapi import APIRouter, Body
from app.core import settings
from app.common import utils
import traceback
import logfire

# Assuming your settings are imported from a config module

# Initialize FastAPI router with the specific prefix
router = APIRouter(prefix="/getcards")


@router.post("/request_data")
async def get_cards(input_data: str = Body(..., embed=False)):
    logfire.info("=====================================")
    logfire.info("User Requested Card Data for: {input_data}", input_data=input_data)
    with logfire.span("GetCardsFunction"):
        """
        API route to handle user requests for card data.
        Determines the type of input (IP, URL, or hash) and returns relevant card data.
        It is done like this to check if all apis are setup. 
        """
        try:
            # Determine the type of input data
            datatype = utils.check_data_type(input_data)

            # Initialize an empty list for cards
            card_list = ["Summary"]  # Summary is always added

            # Process based on the data type
            if datatype in ["url", "ip"]:
                # This is called as it will verify if a url is a legitimate url by calling the DNS resolver for it. If the URL is not legitimate (leads no where) then it will trigger an exception, which returns a 'NotRecognised' response.
                utils.process_address_to_ip(input_data)

                # Conditionally add cards based on settings and availability
                if settings.main.ENV_API_ABUSEIPDB_URL != "":
                    card_list.append("AbuseIPDB")

                if settings.main.ENV_API_PROXYCHECK_URL != "":
                    card_list.append("ProxyCheck")

                if settings.main.ENV_API_VIRUSTOTAL_KEY != "":
                    card_list.append("VirusTotal")

                if datatype == "url" and settings.main.ENV_API_URLSCAN_URL != "":
                    card_list.append("UrlScanScreenshot")

                if datatype == "url" and settings.main.ENV_API_WHODAT_URL != "":
                    card_list.append("Registrar")

            elif datatype == "hash":
                # For hash types, only VirusTotal is checked
                if settings.main.ENV_API_VIRUSTOTAL_KEY != "":
                    card_list.append("VirusTotal")

            else:
                card_list = ["NotRecognised"]

            return card_list

        except Exception:
            # Handle errors and return a 'NotRecognised' response
            logfire.error(traceback.format_exc())
            return ["NotRecognised"]
