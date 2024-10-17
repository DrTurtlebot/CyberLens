import asyncio
import traceback
import requests
import json
from fastapi import APIRouter, Body, HTTPException
from app.core import settings
from app.common import utils
from app.common.models import RequestDataModel
import logfire

# Initialize FastAPI router with the specific prefix
router = APIRouter(prefix="/urlscan")


# UrlScan function to handle the logic for querying the UrlScan API
async def urlscan_function(input_data: RequestDataModel):
    with logfire.span("UrlScanFunction"):
        if settings.main.ENV_API_URLSCAN_URL != "":
            # Get the UrlScan API URL and API key from environment settings
            urlscan_address = settings.main.ENV_API_URLSCAN_URL
            urlscan_key = settings.main.ENV_API_URLSCAN_KEY

            # Set headers and payload for the UrlScan request
            headers = {"API-Key": urlscan_key, "Content-Type": "application/json"}
            data = {"url": input_data, "visibility": "public"}

            # Send initial request to UrlScan API
            initial_response = requests.post(
                urlscan_address, headers=headers, data=json.dumps(data)
            ).json()

            # Check if the response contains the URL to poll for the scan result
            if not initial_response.get("status"):
                new_url_to_call = initial_response.get("api")

                # Wait for 8 seconds before polling the API
                await asyncio.sleep(8)
                attempts = 0
                max_attempts = 20

                # Poll the API until the scan result is available or the maximum attempts are reached
                while attempts < max_attempts:
                    attempts += 1
                    logfire.info(
                        "Attempt {attempts} to get the scan result", attempts=attempts
                    )
                    response = requests.get(new_url_to_call, headers=headers)

                    if response.status_code == 200:
                        data = response.json()
                        return data

                    # Wait 2 seconds before the next attempt
                    await asyncio.sleep(2)

                # If no result is available after max_attempts, raise a timeout error
                return TimeoutError(
                    "The request took too long to complete, please try again later"
                )

            # If the initial response indicates an error, raise an HTTPException
            else:
                logfire.error("The original request to the API was rejected")
                raise HTTPException(
                    status_code=400,
                    detail="The original request to the API was rejected",
                )
        return {"InvalidAPIUrl": "Please check the API URL in the settings"}


# API endpoint to request data from the UrlScan API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    try:
        # Use the caching function to avoid redundant API calls
        return await utils.fetch_data_api_with_cache(
            "UrlScan", input_data, urlscan_function
        )
    except Exception:
        # Log the exception and return an error response
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


# API endpoint to request screenshots from the UrlScan API result
@router.post("/screenshot")
async def request_screenshots(input_data: str = Body(..., embed=False)):
    result = await request_data(input_data)
    screenshot_url = result.get("task", {}).get("screenshotURL")

    # Prepare and return the data containing the screenshot URL
    data = {}
    if screenshot_url:
        data.update({"screenshot_url": screenshot_url})

    logfire.info("Screenshot URL retrieved")
    return data
