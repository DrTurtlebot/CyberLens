import requests
import traceback
from fastapi import APIRouter, Body, HTTPException
from pydantic import AnyUrl
from app.core import settings
from app.common import utils
import logfire

# Initialize FastAPI router with the specific prefix
router = APIRouter(prefix="/registrar")


# Function to handle the logic for querying the registrar (Whodat)
async def registrar_function(input_data: AnyUrl):
    with logfire.span("RegistrarFunction"):
        # Sanitize input by removing 'www.' and prefix subdomains
        input_data = utils.process_address_sanitise(input_data).replace("www.", "")

        whodat_address = settings.main.ENV_API_WHODAT_URL
        check_address = f"{whodat_address}{input_data}"
        # Make initial request to the Whodat API
        response = requests.get(check_address)
        # If the response status is 500, retry with the root domain
        if response.status_code == 500:
            root_domain = ".".join(input_data.split(".")[-2:])
            check_address = f"{whodat_address}{root_domain}"
            response = requests.get(check_address)
            response = response.json()
        else:
            logfire.error("{error}", error=traceback.format_exc())
            #print("Response is not JSON.. possibly a html response from server if the API is down")
            response = None

        return response


# API endpoint to request data from the registrar API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    """
    API route to handle requests for querying registrar data.
    Accepts input data (domain name) and returns the fetched registrar data.
    """
    try:
        # Use utility function to handle caching and avoid redundant API calls
        return await utils.fetch_data_api_with_cache(
            "Registrar", input_data, registrar_function
        )
    except Exception as e:
        # Log the exception and raise an HTTPException with details
        logfire.error("{error}", error=traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "detail": {
                    "type": "internal_error_si",
                    "msg": "See Sys Admin >:(",
                    "info": "Did you provide a full address? 🤔 Example: http://www.website.com",
                }
            },
        )
