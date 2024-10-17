import traceback
import vt
import asyncio
from fastapi import APIRouter, Body, HTTPException
from app.core import settings
from app.common import utils
from app.common.models import RequestDataModel
import logfire

# Set up the router
router = APIRouter(prefix="/virustotal")


# VirusTotal function to handle the logic for querying VirusTotal
async def virus_total_function(input_data: RequestDataModel):
    virustotal_json = {}
    with logfire.span("VirusTotalFunction"):
        # Connect to VirusTotal API using the API key from settings
        if settings.main.ENV_API_VIRUSTOTAL_KEY != "":
            async with vt.Client(settings.main.ENV_API_VIRUSTOTAL_KEY) as client:
                data_type = utils.check_data_type(input_data)

                # If the input is a URL or IP, get the information
                if data_type == "url" or data_type == "ip":
                    try:
                        url = await client.get_object_async(
                            "/urls/{}", format(vt.url_id(input_data))
                        )
                    except vt.error.APIError:
                        logfire.notice("Url Needs Scanning First")
                        await client.scan_url_async(
                            str(input_data)
                        )  # Initiate the scan
                        asyncio.sleep(1)  # Wait for the scan to complete
                        url = await client.get_object_async(
                            "/urls/{}", format(vt.url_id(input_data))
                        )

                    # Unpack and format the data
                    virustotal_json.update(
                        {
                            "data_type": "web",
                            "raw_input": input_data,
                            "analysis_stats": url.last_analysis_stats,
                            "times_submitted": url.times_submitted,
                            "all": url.to_dict(),
                        }
                    )

                # If the input is a hash, get the hash data
                elif data_type == "hash":
                    logfire.info("Hash Data Requested")
                    hash_data = await client.get_object_async(f"/files/{input_data}")
                    virustotal_json.update(
                        {
                            "data_type": "hash",
                            "raw_input": input_data,
                            "analysis_stats": hash_data.last_analysis_stats,
                            "times_submitted": hash_data.times_submitted,
                            "all": hash_data.to_dict(),
                        }
                    )
            logfire.info("VirusTotal Data Retrieved")
            return virustotal_json
        return {"InvalidAPIUrl": "Please check the API URL in the settings"}


# API endpoint to request data from the VirusTotal API
@router.post("/request_data")
async def request_data(input_data: str = Body(..., embed=False)):
    try:
        return await utils.fetch_data_api_with_cache(
            "VirusTotal", input_data, virus_total_function
        )
    except Exception:
        logfire.error("{error}", error=traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "detail": {
                    "type": "internal_error_si",
                    "msg": "See Sys Admin >:(",
                    "info": "Did you provide a valid address? 🤔 Example: http://www.website.com",
                }
            },
        )
