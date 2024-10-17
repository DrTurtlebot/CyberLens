# Standard Library Imports
import socket
import re
from datetime import datetime, timedelta
import asyncio
import traceback

# Third-Party Imports
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logfire

# Local Application Imports
from app.common.models import AddressModel, RequestDataModel
from app.core import settings


# TODO, CHANGE THE MONGO TO MOTOR, THIS IS MASSIVE!
def connect_to_db():
    global mydb, mylock
    with logfire.span("Connecting to MongoDB.."):
        for attempts in range(10):
            try:
                logfire.info("Connecting...")
                if (
                    settings.main.ENV_MONGO_URI == "localhost:27017"
                    or settings.main.ENV_MONGO_URI == "mongo:27017"
                ):
                    logfire.notice("Detected Localhost, switching connection method")
                    mongo_client = MongoClient(settings.main.ENV_MONGO_URI, serverSelectionTimeoutMS=5000)  # fmt: skip
                else:
                    mongo_client = MongoClient(settings.main.ENV_MONGO_URI, server_api=ServerApi("1"), serverSelectionTimeoutMS=5000)  # fmt: skip
                mongo_client.admin.command("ping")
                logfire.notice("Connected to MongoDB")
                break
            except Exception:
                logfire.warn("Failed to connect to the database")
                logfire.error("{error}", error=traceback.format_exc())

            if attempts == 10:
                logfire.fatal("Failed to connect to the database after 10 attempts")
                raise ConnectionError("Failed to connect to the database")

            logfire.notice("Retrying connection...")

        mydb = mongo_client["cache"]
        mylock = mongo_client["lock"]

        # Clear Lock database of entries
        mylock["locks"].delete_many({})

        logfire.info("MongoDB Setup Complete")


def process_address_sanitise(address: AddressModel) -> str:
    try:
        # Strip the scheme and path from the address
        address = address.split("://")[-1].split("/")[0]
        return address
    except Exception as e:
        logfire.error("Failed to sanitize address: {e}", e=e)
        raise ValueError(f"Failed to sanitize address: {e}")


def process_address_to_ip(address: str) -> str:
    try:
        address = process_address_sanitise(address)
        resolved_ip = socket.gethostbyname(address)
        return resolved_ip
    except socket.gaierror as e:
        raise ValueError(f"Failed to resolve hostname: {e}")


def check_data_type(data: RequestDataModel) -> str:
    regex_url = r"^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/[^\s]*)?$"
    regex_ip = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    regex_hash = r"^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$"

    if re.match(regex_url, data):
        return "url"
    elif re.match(regex_ip, data):
        return "ip"
    elif re.match(regex_hash, data):
        return "hash"
    else:
        return "unknown"


def find_in_cache(api_name: str, input_data: RequestDataModel) -> dict:
    """
    Looks up data in the cache for the given API and input data.
    """
    mycol = mydb[api_name]
    mydoc = mycol.find_one({"_id": input_data})

    if mydoc:
        logfire.info(
            "{api_name} - {input_data}: Cache: Found In Cache",
            api_name=api_name,
            input_data=input_data,
        )
        return mydoc["data"]
    logfire.info(
        "{api_name} - {input_data}: Cache: Not Found, Beginning API Call",
        api_name=api_name,
        input_data=input_data,
    )
    return None


def save_to_cache(api_name: str, input_data: RequestDataModel, data: dict, ttl=14400):
    """
    Saves the given data to the cache with a TTL (Time-to-Live) value.
    """
    expiration_time = datetime.utcnow() + timedelta(seconds=ttl)
    mycol = mydb[api_name]
    mycol.create_index("expires_at", expireAfterSeconds=0)
    mycol.update_one(
        {"_id": input_data},
        {
            "$set": {
                "data": data,
                "timestamp": datetime.utcnow(),
                "expires_at": expiration_time,
            }
        },
        upsert=True,
    )


async def fetch_data_api_with_cache(
    api_name, input_data: RequestDataModel, api_function
):
    cached_data = find_in_cache(api_name, input_data)
    if cached_data:
        return cached_data

    lock = await acquire_mongo_lock(api_name, input_data)
    if lock is True:
        data = await api_function(input_data)
        save_to_cache(api_name, input_data, data)
        release_lock(api_name, input_data)
        return data
    else:
        return lock


async def acquire_mongo_lock(api_name, input_data: RequestDataModel, lock_timeout=30):
    mycol = mylock["locks"]
    full_lock_name = f"{api_name}-{input_data}"
    myquery = {"_id": full_lock_name}
    mydoc = mycol.find_one(myquery)

    if mydoc:
        attempts = 0
        while attempts < lock_timeout:
            mydoc = mycol.find_one(myquery)
            if not mydoc:
                return find_in_cache(api_name, input_data)

            attempts += 1
            await asyncio.sleep(0.3)

        logfire.error("Lock Timed Out waiting for cache")
        raise TimeoutError("Lock Timed Out waiting for cache")

    expiration_time = datetime.utcnow() + timedelta(seconds=45)
    mycol.create_index("expires_at", expireAfterSeconds=0)
    mycol.update_one(
        {"_id": full_lock_name},
        {"$set": {"timestamp": str(datetime.utcnow()), "expires_at": expiration_time}},
        upsert=True,
    )
    return True


def release_lock(api_name: str, input_data: RequestDataModel) -> bool:
    mycol = mylock["locks"]
    full_lock_name = f"{api_name}-{input_data}"
    mycol.delete_one({"_id": full_lock_name})
    return True


# Add the following function to utils.py


def save_to_bugs(report):
    """
    Save a bug report to the 'bugs' collection in MongoDB.
    """
    try:
        mycol = mydb["bugs"]  # Access the 'bugs' collection
        bug_data = {
            "name": report.name,
            "email": report.email,
            "url_or_ip": report.url_or_ip,
            "description": report.description,
            "timestamp": datetime.utcnow(),
        }

        # Insert the bug report into the database
        mycol.insert_one(bug_data)
        logfire.info("Bug report saved to MongoDB", bug_data=bug_data)

    except Exception as e:
        logfire.error("Error saving bug report to MongoDB: {e}", e=e)
        raise ValueError("Failed to save bug report to database")
