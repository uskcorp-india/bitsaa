import re
from schema import Schema, And, Optional, SchemaError

def validate(booking: dict) -> dict:
    errors = []

    field_validators = {
        'firstname': And(str, len, error="Field 'firstname' should be a non-empty string"),
        'lastname': And(str, len, error="Field 'lastname' should be a non-empty string"),
        'phone': And(str, len, lambda s: len(s) == 10 and s.isdigit(), error="Phone number must be a 10-digit number"),
        'email': And(str, lambda s: bool(re.match(r'^[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9-]+\.(?:com|in|co\.in)$', s)),error="Invalid email format"),
        Optional('booking_id'): And(str, len, error="Field 'bookingId' should be a non-empty string"),
        Optional('userId'): And(str, len, error="Field 'userId' should be a non-empty string"),
        Optional('memberId'): And(str, len, error="Field 'memberId' should be a non-empty string"),
        Optional('roomId'): And(str, len, error="Field 'roomId' should be a non-empty string"),
        Optional('bookingDate'): And(str, len, error="Field 'bookingDate' should be a non-empty string"),
        Optional('startTime'): And(str, len, error="Field 'startTime' should be a non-empty string"),
        Optional('endTime'): And(str, len, error="Field 'endTime' should be a non-empty string"),
        Optional('purpose'): And(str, len, error="Field 'purpose' should be a non-empty string"),
        Optional('status'): And(str, len, error="Field 'status' should be a non-empty string"),
        Optional('id'): And(str, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(str, len, error="Field 'created_at' should be a non-empty string"),
        Optional('updated_at'): And(str, len, error="Field 'updated_at' should be a non-empty string"),
        Optional('address'): And(str, len, error="Field 'address' should be a non-empty string"),
        Optional('dob'): And(str, len, error="Field 'dob' should be a non-empty string"),
        Optional('gender'): And(str, len, error="Field 'gender' should be a non-empty string"),
        Optional('alias'): And(str, len, error="Field 'alias' should be a non-empty string"),
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