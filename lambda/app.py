import os

from fastapi import FastAPI, Request
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
import json
from router.resort_router import router as resort_router
from router.reservation_router import router as reservation_router
from router.registration_router import router as registration_router
from router.confirm_router import router as confirm_router
from fastapi.responses import JSONResponse


from utils.logger_factory import get_logger

logger = get_logger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resort_router)
app.include_router(reservation_router)
app.include_router(registration_router)
app.include_router(confirm_router)

handler = Mangum(app)

@app.api_route("/{proxy_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def catch_all(request: Request, proxy_path: str):
    logger.info(proxy_path)
    logger.warning(f"Unhandled API Gateway request: {request.method} {request.url}")
    return {
        "status": False,
        "message": "Route not found",
        "status_code": 404,
        "data": None
    }

EXPECTED_API_KEY = "aB3!k9Lm@zR5qX7wP2eT8vY4dF6#rT1$gH5^VcL9mNpQ2rT8uLz#qW3eXpL9tR6yEwD2mX8qZsT8$mQ#vLp9ZdE7rT2yU5iO0jH7*qN3pVzL9tR6yEwD2mX8q"

@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    excluded_routes = []

    if request.url.path in excluded_routes:
        return await call_next(request)

    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != EXPECTED_API_KEY:
        logger.warning(f"Unauthorized request: Invalid or missing API key - {api_key}")
        return JSONResponse(
            status_code=403,
            content={
                "status": False,
                "message": "Forbidden: Invalid API Key",
                "status_code": 403,
                "data": None
            }
        )

    return await call_next(request)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event, indent=2)}")
    try:
        response = handler(event, context)
        logger.info(f"Raw response from Mangum: {json.dumps(response, indent=2)}")
        if not isinstance(response, dict):
            logger.warning("Response is not a dictionary, setting default empty response")
            response = {}
        body = response.get("body", "{}")
        logger.info(f"Raw response body: {body}")
        try:
            parsed_body = json.loads(body) if isinstance(body, str) else body
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON body: {str(e)}")
            parsed_body = {}
        status_code = response.get("statusCode", 500)
        logger.info(f"Extracted status code: {status_code}")
        if isinstance(parsed_body, dict):
            if "errors" in parsed_body:
                logger.info("Validation error detected")
                final_response = {
                    "status": False,
                    "message": "Validation Error",
                    "status_code": 422,
                    "data": parsed_body["errors"]
                }
                response["statusCode"] = 422
            else:
                final_response = {
                    "status": status_code < 400,
                    "message": parsed_body.get("message", "Success" if status_code < 400 else "Error"),
                    "status_code": status_code,
                    "data": parsed_body.get("data", [])
                }
        elif isinstance(parsed_body, list):
            extracted_message = next((item["message"] for item in parsed_body if isinstance(item, dict) and "message" in item), "Internal Server Error Occurred")
            filtered_data = [item for item in parsed_body if isinstance(item, dict) and "message" not in item]
            final_response = {
                "status": status_code < 400,
                "message": extracted_message,
                "status_code": status_code,
                "data": filtered_data
            }
        else:
            final_response = {
                "status": False,
                "message": "Internal Server Error",
                "status_code": 500,
                "data": []
            }
        logger.info(f"Formatted final response: {json.dumps(final_response, indent=2)}")
        response["body"] = json.dumps(final_response)
        return response
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": False,
                "message": "Internal Server Error",
                "status_code": 500,
                "data": []
            }),
            "headers": {"Content-Type": "application/json"}
        }
