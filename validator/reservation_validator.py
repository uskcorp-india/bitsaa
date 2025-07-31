from schema import Schema, And, Optional, SchemaError
from utils.validator_utils import is_string_or_none, is_int_or_none


def validate(reservation: dict) -> dict:
    errors = []

    field_validators = {
        Optional('reservation_id'): And(is_string_or_none, len, error="Field 'reservation_id' should be a non-empty string"),
        Optional('resort'): And(dict, len, error="Field 'created_at' should be a non-empty string"),
        Optional('registration'): And(list, len, error="Field 'registration' should be a list"),
        Optional('status'): And(is_string_or_none, len, error="Field 'status' should be a non-empty string"),
        Optional('transaction_id'): And(is_string_or_none, len, error="Field 'id' should be a non-empty string"),
        Optional('created_at'): And(is_string_or_none, len, error="Field 'created_at' should be a non-empty string"),
        Optional('extra_bed'):And(bool, error="Field should be type of bool"),
        Optional('room_count'):And (is_int_or_none, error="Field 'room_count' should be a non-empty int"),
        Optional('check_in'):And(is_string_or_none, len, error="Field 'check_in' should be a non-empty string"),
        Optional('check_out'): And(is_string_or_none, len, error="Field 'check_out' should be a non-empty string"),
        Optional('total_cost'): And(is_string_or_none, len, error="Field 'total_cost' should be a non-empty string")

    }

    validated_reservation = {}
    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key

        if key_name in reservation:
            try:
                validated_reservation[key_name] = Schema(validator).validate(reservation[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")
    if errors:
        return {"errors": errors}
    return validated_reservation