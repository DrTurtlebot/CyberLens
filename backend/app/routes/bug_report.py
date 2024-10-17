import requests
import traceback
import logfire
from fastapi import APIRouter, HTTPException, Request
from app.core import settings
from app.common.models import RequestDataModel
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from datetime import datetime

# Initialize FastAPI router
router = APIRouter(prefix="/bug-report")

# MongoDB connection for saving bugs
client = MongoClient(settings.main.ENV_MONGO_URI)
bug_db = client["bug_reports"]  # Create a new database for bug reports if not existing
bug_collection = bug_db["bugs"]  # This will be the collection where bugs are saved


# Define a Pydantic model to validate incoming bug report data
class BugReport(BaseModel):
    name: str = None
    email: str = None
    url_or_ip: str = None
    description: str


# Function to save the bug report to MongoDB
def save_to_bugs(bug_data: dict):
    try:
        bug_data["timestamp"] = datetime.utcnow()  # Add a timestamp to the report
        result = bug_collection.insert_one(
            bug_data
        )  # Insert the bug report into the bugs collection
        logfire.info("Bug report saved to MongoDB", bug_id=str(result.inserted_id))
    except Exception as e:
        logfire.error(
            "Error saving bug report to MongoDB", error=traceback.format_exc()
        )
        raise HTTPException(
            status_code=500, detail="Error saving the bug report to the database."
        )


# API endpoint to handle bug reports
@router.post("/report")
async def submit_bug_report(request: Request, report: BugReport):
    try:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 1024 * 1024:  # limit to 1MB
            raise HTTPException(status_code=413, detail="Payload too large")
        # Convert the Pydantic BugReport model to a dictionary
        bug_data = report.dict()

        # Log the incoming bug report (you can modify this to save to a database, etc.)
        logfire.info("New Bug Report!", report=bug_data)

        # Save the bug report to the bugs collection in MongoDB
        save_to_bugs(bug_data)

        return {"message": "Bug report submitted successfully!"}
    except Exception:
        logfire.error("Error handling bug report", error=traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "detail": {
                    "type": "internal_error_si",
                    "msg": "An error occurred while processing the bug report.",
                    "info": "Please contact the system administrator.",
                }
            },
        )
