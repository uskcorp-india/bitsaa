import re
from schema import Schema, And, Optional, SchemaError
from utils.validator_utils import is_string_or_none
def validate(booking: dict) -> dict:
    errors = []

    field_validators = {
        'booking_id': And(is_string_or_none, len, error="Field 'bookingId' should be a non-empty string"),
        Optional('fullName'): And(is_string_or_none, len, error="Field 'fullName' should be a non-empty string"),
        Optional('phone'): And(is_string_or_none, len, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number"),
        Optional('email'): And(is_string_or_none, lambda s: bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9-]+\.(?:com|in|co\.in)$', s)),error="Invalid email format"),
        Optional('room'): And(is_string_or_none, len, error="Field 'roomId' should be a non-empty string"),
        Optional('booking_date'): And(is_string_or_none, len, error="Field 'bookingDate' should be a non-empty string"),
        Optional('check_in'): And(is_string_or_none, len, error="Field 'startTime' should be a non-empty string"),
        Optional('check_out'): And(is_string_or_none, len, error="Field 'endTime' should be a non-empty string"),
        Optional('status'): And(is_string_or_none, len, error="Field 'status' should be a non-empty string"),
        Optional('id'): And(is_string_or_none, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(is_string_or_none, len, error="Field 'created_at' should be a non-empty string"),
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