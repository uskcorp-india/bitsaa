import dynamodb.dynamodb_proxy as db
from utils.logger_factory import get_logger
import validator.confirm_validator as validator
from utils.response_utils import build_response

logger = get_logger(__name__)


def create(reservation_id: str,confirm: dict):
    validated_reservation = validator.validate(confirm)
    logger.info(f'registration details: {confirm}')
    if 'errors' in validated_reservation:
        return build_response(validated_reservation['errors'], 400)
    else:
        reservation = db.find_reservation(reservation_id)

        resort = db.find_resort(reservation['resort']['id'])
        available_rooms = int(resort['available'])
        if available_rooms < 1:
            return build_response(reservation, f"Only {available_rooms} rooms are available, but you'registration trying to book 1 room.")
        resort['available'] = available_rooms - 1
        db.update_resort(reservation['resort']['id'], resort)

        reservation['status'] = "Confirm"
        reservation['transaction_id'] = confirm.get("confirm_details", {}).get("transaction_id")
        reservation['confirm_details'] = validated_reservation['confirm_details']
        db.update_reservation(reservation_id, reservation)

        for registration in reservation['registration']:
            registration = db.find_registration(registration['registration_id'])
            registration['Item']['reservation_id'] = reservation_id
            db.update_registration(registration['Item']['id'], registration['Item'])

        return build_response(reservation, 'registration Created Successfully')
