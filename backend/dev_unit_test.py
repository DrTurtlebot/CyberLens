from app.routes.virustotal import virus_total_function
from app.routes.registrar import registrar_function
from app.routes.abuseipdb import abuseipdb_function
from app.routes.proxycheck import proxycheck_function
from app.routes.urlscan import urlscan_function
from app.routes.summary import summary_function


import app.core.settings as settings
import pytest_asyncio
import pytest
import asyncio
import logfire

logfire.configure(token=settings.main.LOGFIRE_TOKEN, send_to_logfire=False)


# Tests Route Functions
@pytest.mark.asyncio
async def test_virus_total_function():
    input_data = "https://www.google.com"
    result = await virus_total_function(input_data)

    assert result.get("raw_input") == input_data


@pytest.mark.asyncio
async def test_registrar_function():
    input_data = "https://www.google.com"
    result = await registrar_function(input_data)

    assert result.get("domain") is not None


@pytest.mark.asyncio
async def test_abuseipdb_ip_function():
    input_data = "https://www.google.com"
    result = await abuseipdb_function(input_data)

    assert result.get("data").get("ipAddress") is not None


@pytest.mark.asyncio
async def test_proxycheck_function():
    input_data = "https://www.google.com"
    result = await proxycheck_function(input_data)

    assert result.get("status") == "ok"


@pytest.mark.asyncio
async def test_urlscan_function():
    input_data = "https://www.microsoft.com"
    result = await urlscan_function(input_data)

    assert result.get("data") is not None
