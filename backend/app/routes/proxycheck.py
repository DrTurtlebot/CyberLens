import traceback
import requests
from fastapi import APIRouter, Body, HTTPException
from app.core import settings
from app.common import utils
from app.common.models import RequestDataModel
import logfire

# Initialize FastAPI router with the specific prefix
router = APIRouter(prefix="/proxycheck")


# Function to handle the logic for querying ProxyCheck
async def proxycheck_function(input_data: RequestDataModel):
    with logfire.span("ProxyCheckFunction"):
        if settings.main.ENV_API_PROXYCHECK_URL != "":
            # Get the ProxyCheck API URL and API key from environment settings
            proxycheck_address = settings.main.ENV_API_PROXYCHECK_URL
            proxycheck_api_key = settings.main.ENV_API_PROXYCHECK_KEY

            # Convert input data to an IP address if necessary
            target_ip = utils.process_address_to_ip(input_data)

            # Compile the full API request URL
            full_address = (
                f"{proxycheck_address}{target_ip}?key={proxycheck_api_key}&vpn=1&asn=1"
            )

            # Make the request to ProxyCheck API and retrieve JSON data
            response = requests.get(full_address)
            return response.json()
        return {"InvalidAPIUrl": "Please check the API URL in the settings"}


# API endpoint to request data from ProxyCheck API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    """
    API route to handle requests for querying the ProxyCheck API.
    Accepts input data (IP address) and returns the fetched proxy check data.
    """
    try:
        # Use utility function to handle caching and avoid redundant API calls
        return await utils.fetch_data_api_with_cache(
            "ProxyCheck", input_data, proxycheck_function
        )
    except Exception:
        # Log the exception and raise an HTTPException with details
        logfire.error("{error}", error=traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "detail": {
                    "type": "internal_error_si",
                    "msg": "See Sys Admin >:(",
                    "info": "Did you provide a full address? 🤔 Example: http://www.example.com",
                }
            },
        )
