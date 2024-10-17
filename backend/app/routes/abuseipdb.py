import requests
import traceback
from fastapi import APIRouter, Body, HTTPException
from app.core import settings
from app.common import utils
from app.common.models import RequestDataModel
import logfire

# Initialize FastAPI router with the specific prefix
router = APIRouter(prefix="/abuseipdb")


# Function to handle the logic for querying AbuseIPDB
async def abuseipdb_function(input_data: RequestDataModel):
    with logfire.span("AbuseIPDBFunction"):
        if settings.main.ENV_API_ABUSEIPDB_URL != "":
            # Convert input data to an IP address if necessary
            target_ip = utils.process_address_to_ip(input_data)

            # Retrieve AbuseIPDB API credentials from environment settings
            abuseipdb_url = settings.main.ENV_API_ABUSEIPDB_URL
            abuseipdb_api_key = settings.main.ENV_API_ABUSEIPDB_KEY

            # Set request parameters
            params = {
                "ipAddress": target_ip,
                "maxAgeInDays": "30",  # Retrieve reports up to 30 days old
                "verbose": "false",  # Set to 'true' for detailed reports
            }

            # Set request headers, including the API key
            headers = {"Key": abuseipdb_api_key, "Accept": "application/json"}

            # Make the request to AbuseIPDB API
            response = requests.get(abuseipdb_url, params=params, headers=headers)

            # Parse the response JSON data
            return response.json()
        return {"InvalidAPIUrl": "Please check the API URL in the settings"}


# API endpoint to request data from AbuseIPDB API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    try:
        # Use utility function to handle caching and prevent redundant API calls
        return await utils.fetch_data_api_with_cache(
            "AbuseIPDB", input_data, abuseipdb_function
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
                    "info": "Did you provide a valid address? 🤔 Example: http://www.example.com",
                }
            },
        )
