import dynamodb.dynamodb_proxy as db
from dao.resort_dao import decrement_blocked_room
from utils.email_utils import send_booking_confirmation_email
from utils.logger_factory import get_logger
import validator.confirm_validator as validator
from utils.response_utils import build_response
import hmac
import hashlib
import os

RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")
logger = get_logger(__name__)

def verify_razorpay_signature(order_id, payment_id, signature, secret):
    payload = f"{order_id}|{payment_id}"
    generated_signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated_signature, signature)


def create(reservation_id: str,confirm: dict):
    validated_reservation = validator.validate(confirm)
    logger.info(f'registration details: {confirm}')
    if 'errors' in validated_reservation:
        return build_response(validated_reservation['errors'], 400)
    else:
        confirm_details = confirm.get("confirm_details", {})
        order_id = confirm_details.get("order_id")
        payment_id = confirm_details.get("transaction_id")
        signature = confirm_details.get("signature")
        if not verify_razorpay_signature(order_id, payment_id, signature, RAZORPAY_SECRET):
            logger.info('registration details: Invalid Razorpay signature')
            return build_response( {}, "Invalid Razorpay signature")
        reservation = db.find_reservation(reservation_id)
        booking_room = int(reservation.get("room_count"))
        resort = db.find_resort(reservation['resort']['id'])
        available_rooms = int(resort['available'])
        if available_rooms < booking_room:
            return build_response(reservation, f"Only {available_rooms} rooms are available, but your trying to book {booking_room} room.")
        db.update_resort(reservation['resort']['id'], resort)
        decrement_blocked_room(reservation['resort']['id'], booking_room)
        reservation['status'] = "Confirm"
        reservation['transaction_id'] = confirm.get("confirm_details", {}).get("transaction_id")
        reservation['confirm_details'] = validated_reservation['confirm_details']
        send_booking_confirmation_email(reservation)
        db.update_reservation(reservation_id, reservation)
        for registration in reservation['registration']:
            registration = db.find_registration(registration['id'])
            registration['Item']['reservation_id'] = reservation_id
            db.update_registration(registration['Item']['id'], registration['Item'])
        db.delete_from_pending_reservation(reservation_id)
        return build_response(reservation, 'Registration Created Successfully')