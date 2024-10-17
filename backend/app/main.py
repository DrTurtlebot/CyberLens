# Standard Library Imports
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import os

# Third-Party Imports
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_429_TOO_MANY_REQUESTS
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from pydantic import IPvAnyAddress
import logfire

# Local Application Imports
from app.core import settings
from app.common import utils
from app.routes import (
    proxycheck,
    abuseipdb,
    virustotal,
    getcards,
    urlscan,
    summary,
    registrar,
    bug_report,
)

# Initialize Utils and Settings
logfire.configure(
    token=settings.main.LOGFIRE_TOKEN, send_to_logfire=settings.main.PRODUCTION
)
logfire.info("----------------")
logfire.info("Server Starting!")
logfire.notice("In Production?: {prod_status} ", prod_status=(settings.main.PRODUCTION))
utils.connect_to_db()

# Launch FastAPI App
app = FastAPI()
# logfire.instrument_fastapi(app)

# CORS Middleware
logfire.info("CORS Whitelist: {whitelist}", whitelist=settings.main.ENV_CORS_WHITELIST)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.main.ENV_CORS_WHITELIST,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# SlowAPI Rate Limiter Middleware
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_exception_handler(HTTP_429_TOO_MANY_REQUESTS, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Blocking IPs Settings
failed_attempts = {}
blocked_ips = {}
BLOCK_DURATION = timedelta(minutes=3)
BLOCK_THRESHOLD = 2


# Check if an IP is currently blocked
def is_blocked(ip: IPvAnyAddress) -> bool:
    block_info = blocked_ips.get(ip)
    if block_info:
        block_time, duration = block_info
        if datetime.now() >= block_time + duration:
            logfire.notice("RL: Unblocking IP: {ip}", ip=ip)
            del blocked_ips[ip]
            return False
        return True
    return False


# Block an IP for a defined duration
def block_ip(ip: IPvAnyAddress):
    blocked_ips[ip] = (datetime.now(), BLOCK_DURATION)


# Middleware to check if an IP is blocked
@app.middleware("http")
async def middleware_test(request: Request, call_next):
    client_ip = request.client.host
    if is_blocked(client_ip):
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Your IP has been blocked due to suspicious activity"},
        )
    return await call_next(request)


# Custom 404 Handler to block constant failed attempts
@app.exception_handler(HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, exc: HTTPException):
    client_ip = request.client.host
    failed_count = failed_attempts.get(client_ip, 0) + 1
    failed_attempts[client_ip] = failed_count
    # failed_attempts[client_ip] = 0 #Disables IP Banning
    if failed_count >= BLOCK_THRESHOLD:
        block_ip(client_ip)
        logfire.warning("RL: Blocking IP: {client_ip}", client_ip=client_ip)
        failed_attempts.pop(client_ip, None)
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Your IP has been blocked due to suspicious activity"},
        )
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"detail": "Not Found"},
    )


# Root Handler
@app.get("/")
def read_root():
    return {"root": "true"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logfire.notice("Starting up the application")
    yield
    logfire.notice("Shutting down the application")


# Include API Routers
app.include_router(proxycheck.router, prefix="/api")
app.include_router(abuseipdb.router, prefix="/api")
app.include_router(virustotal.router, prefix="/api")
app.include_router(getcards.router, prefix="/api")
app.include_router(urlscan.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(registrar.router, prefix="/api")
app.include_router(bug_report.router, prefix="/api")


# Start Server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=4000, reload=True)
