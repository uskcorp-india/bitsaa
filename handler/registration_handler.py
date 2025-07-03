import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.registration_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)

def create(registration: dict):
    validated_registration = validator.validate(registration)
    print(f'registration details: {registration}')
    if 'errors' in validated_registration:
        return build_response(validated_registration['errors'],400)
    else:
        response = db.create_registration(validated_registration)
        return build_response(response,'registration Created Successfully')


def find(registration_id: str):
    response = db.find_registration(registration_id)
    if "Item" in response:
        if response['Item'].get('reservation_id'):
            logger.info(response)
            return build_response({}, "Registration already completed")
        return build_response(response['Item'],"registration Found Successfully")
    else:
        logger.info(response)
        return build_response({},"registration not Found")


def registration_exists(registration_id: str):
    response = db.registration_exists(registration_id)
    logger.info(response)
    return build_response(response,"registration Found Successfully")

def update(registration_id: str,registration: dict):
    validated_registration = validator.validate(registration)
    logger.info(f'Updating customer details: {registration}')

    if 'errors' in validated_registration:
        return build_response(validated_registration['errors'], 400)
    else:
        response = db.update_registration(registration_id,registration)
        return build_response(response, 'registration Updated Successfully')

def delete(registration_id:str):
    response=db.delete_registration(registration_id)
    logger.info(response)
    return build_response(response,message="registration deleted successfully")