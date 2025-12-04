import re
from schema import Schema, And, Optional, SchemaError
from utils.validator_utils import is_string_or_none

def validate(registration: dict) -> dict:
    errors = []

    field_validators = {
        Optional('registration_no'): And(is_string_or_none, len, error="Field 'registration_no' should be a non-empty string"),
        Optional('reservation_id'): And(is_string_or_none, len, error="Field 'reservation_id' should be a non-empty string"),
        Optional('phone'): And(is_string_or_none, lambda s: s.isdigit() and len(s) == 10, error="Phone number must be a 10-digit number"),
        Optional('address'): And(is_string_or_none, len, error="Field 'address' should be a non-empty string"),
        Optional('aadhar'): And(is_string_or_none, len, error="Field 'aadhar' should be a non-empty string"),
        # Fields from Tikkl payload
        Optional('objectType'): And(is_string_or_none, len, error="Field 'objectType' should be a non-empty string"),
        Optional('ticket_id'): And(is_string_or_none, len, error="Field 'ticket_id' should be a non-empty string"),
        Optional('orderId'): And(is_string_or_none, len, error="Field 'orderId' should be a non-empty string"),
        Optional('orgName'): And(is_string_or_none, len, error="Field 'orgName' should be a non-empty string"),
        Optional('orgSubdomain'): And(is_string_or_none, len, error="Field 'orgSubdomain' should be a non-empty string"),
        Optional('campaignName'): And(is_string_or_none, len, error="Field 'campaignName' should be a non-empty string"),
        Optional('campaignUrl'): And(is_string_or_none, len, error="Field 'campaignUrl' should be a non-empty string"),
        Optional('orderUrl'): And(is_string_or_none, len, error="Field 'orderUrl' should be a non-empty string"),
        Optional('eventName'): And(is_string_or_none, len, error="Field 'eventName' should be a non-empty string"),
        Optional('orderTimeUtc'): And(is_string_or_none, len, error="Field 'orderTimeUtc' should be a non-empty string"),
        Optional('registrantName'): And(is_string_or_none, len, error="Field 'registrantName' should be a non-empty string"),
        Optional('registrantEmail'): And(is_string_or_none, lambda s: bool(re.match(
             r'^[a-zA-Z0-9][a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', s
        )), error="Invalid registrantEmail format"),
    }

    validated_registration = {}
    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key

        if key_name in registration:
            try:
                validated_registration[key_name] = Schema(validator).validate(registration[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")

    if errors:
        return {"errors": errors}
    return validated_registration
