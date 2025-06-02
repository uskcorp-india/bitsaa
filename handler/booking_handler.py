import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.booking_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(booking: dict):
    booking_validator = validator.validate(booking)
    logger.info(f'booking details: {booking}')

    if 'errors' in booking_validator:
        return build_response(booking_validator['errors'],400)
    else:
        response = db.create_booking(booking)
        return build_response(response,'booking Created Successfully')

def find(booking_id: str):
    response = db.find_booking(booking_id)
    logger.info(response)
    return build_response(response,"booking Found Successfully")

def update(booking: dict):
    validated_booking = validator.validate(booking)
    logger.info(f'Updating booking details: {booking}')

    if 'errors' in validated_booking:
        return build_response(validated_booking['errors'], 400)
    else:
        response = db.update_booking(booking)
        return build_response(response, 'booking Updated Successfully')

def delete(booking_id:str):
    response=db.delete_booking(booking_id)
    logger.info(response)
    return build_response(response,message="booking deleted successfully")