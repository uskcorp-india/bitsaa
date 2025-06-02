import re
from schema import Schema, And, Optional, SchemaError
from utils.validator_utils import is_string_or_none
def validate(booking: dict) -> dict:
    errors = []

    field_validators = {
        Optional('firstname'): And(str, len, error="Field 'firstname' should be a non-empty string"),
        Optional('lastname'): And(is_string_or_none, len, error="Field 'lastname' should be a non-empty string"),
        Optional('phone'): And(is_string_or_none, len, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number"),
        Optional('email'): And(is_string_or_none, lambda s: bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9-]+\.(?:com|in|co\.in)$', s)),error="Invalid email format"),
        'booking_id': And(is_string_or_none, len, error="Field 'bookingId' should be a non-empty string"),
        Optional('user_id'): And(is_string_or_none, len, error="Field 'userId' should be a non-empty string"),
        Optional('member_id'): And(is_string_or_none, len, error="Field 'memberId' should be a non-empty string"),
        Optional('room_id'): And(is_string_or_none, len, error="Field 'roomId' should be a non-empty string"),
        Optional('booking_date'): And(is_string_or_none, len, error="Field 'bookingDate' should be a non-empty string"),
        Optional('start_time'): And(is_string_or_none, len, error="Field 'startTime' should be a non-empty string"),
        Optional('end_time'): And(is_string_or_none, len, error="Field 'endTime' should be a non-empty string"),
        Optional('purpose'): And(is_string_or_none, len, error="Field 'purpose' should be a non-empty string"),
        Optional('status'): And(is_string_or_none, len, error="Field 'status' should be a non-empty string"),
        Optional('id'): And(is_string_or_none, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(is_string_or_none, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(is_string_or_none, len, error="Field 'updated_at' should be a non-empty string"),
        Optional('address'): And(is_string_or_none, len, error="Field 'address' should be a non-empty string"),
        Optional('dob'): And(is_string_or_none, len, error="Field 'dob' should be a non-empty string"),
        Optional('gender'): And(is_string_or_none, len, error="Field 'gender' should be a non-empty string"),
        Optional('alias'): And(is_string_or_none, len, error="Field 'alias' should be a non-empty string"),
    }

    validated_booking = {}
    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key

        if key_name in booking:
            try:
                validated_booking[key_name] = Schema(validator).validate(booking[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")
    if errors:
        return {"errors": errors}
    return validated_booking