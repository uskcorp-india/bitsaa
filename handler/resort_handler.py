import dynamodb.dynamodb_proxy as db
from constants.common import RESORT
from utils.logger_factory import get_logger
import validator.resort_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(resort_data: dict):
    resort_validator = validator.validate(resort_data)
    logger.info(f'resort details: {resort_data}')

    if 'errors' in resort_validator:
        return build_response(resort_validator['errors'],400)
    else:
        response = db.create_resort(resort_validator)
        return build_response(response,'resort Created Successfully')

def find(resort_id: str):
    response = db.find_resort(resort_id)
    logger.info(response)
    return build_response(response,"resort Found Successfully")

def find_all():
    response = db.find_all_resorts()
    logger.info(response)
    return build_response(response, f"{RESORT}'s retrieved successfully.")

def update(resort_id: str,resort: dict):
    validated_resort = validator.validate(resort)
    logger.info(f'Updating resort details: {resort}')

    if 'errors' in validated_resort:
        return build_response(validated_resort['errors'], 400)
    else:
        response = db.update_resort(resort_id,validated_resort)
        return build_response(response, 'resort Updated Successfully')

def delete(resort_id:str):
    response=db.delete_resort(resort_id)
    logger.info(response)
    return build_response(response,message="resort deleted successfully")