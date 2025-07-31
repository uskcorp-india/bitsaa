from schema import Schema, And, Optional, SchemaError
from utils.validator_utils import is_string_or_none

def validate(resort: dict) -> dict:
    errors = []

    field_validators = {
        Optional('id'): And(is_string_or_none, len, error="Field 'id' must be a non-empty string"),
        'name': And(is_string_or_none, len, error="Field 'name' must be a non-empty string"),
        'category': And(str, len, error="Field 'category' must be a non-empty string"),
        'available': And(int, lambda n: n > 0,error="Field 'available' must be a positive integer (rooms must be available)"),
        'price':And(int, error="Field 'maxPersonAllowed' must be a positive integer"),
        'maxPersonAllowed': And(int, lambda n: n > 0, error="Field 'maxPersonAllowed' must be a positive integer"),
    }
    validated_resort = {}
    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key

        if key_name in resort:
            try:
                validated_resort[key_name] = Schema(validator).validate(resort[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")
    if errors:
        return {"errors": errors}
    return validated_resort