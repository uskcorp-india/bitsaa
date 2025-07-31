import dynamodb.dynamodb_proxy as db
from utils.email_utils import send_booking_confirmation_email
from utils.logger_factory import get_logger
import validator.reservation_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(reservation: dict):
    reservation_validator = validator.validate(reservation)
    logger.info(f'reservation details: {reservation}')
    if 'errors' in reservation_validator:
        return build_response(reservation_validator['errors'],400)
    else:
        reservation_data = db.create_reservation(reservation_validator)
        if reservation_data['success']:
            send_booking_confirmation_email(reservation_validator.get('data')[0])
        return build_response(reservation_data,'reservation Created Successfully')

def find(reservation_id: str):
    response = db.find_reservation(reservation_id)
    logger.info(response)
    return build_response(response,"reservation Found Successfully")

def update(reservation_id,reservation: dict):
    validated_reservation = validator.validate(reservation)
    logger.info(f'Updating reservation details: {reservation}')

    if 'errors' in validated_reservation:
        return build_response(validated_reservation['errors'], 400)
    else:
        response = db.update_reservation(reservation_id,validated_reservation)
        return build_response(response, 'reservation Updated Successfully')

def delete(reservation_id:str):
    response=db.delete_reservation(reservation_id)
    logger.info(response)
    return build_response(response,message="reservation deleted successfully")