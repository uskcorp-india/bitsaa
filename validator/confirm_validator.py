from schema import Schema, And, Optional, SchemaError

def validate(confirm: dict) -> dict:
    errors = []

    field_validators = {
        Optional('confirm_details'):And(dict)
    }
    validated_registration = {}

    for key, validator in field_validators.items():
        key_name = key.schema if isinstance(key, Optional) else key
        if key_name in confirm:
            try:
                validated_registration[key_name] = Schema(validator).validate(confirm[key_name])
            except SchemaError as e:
                errors.append(str(e))
        else:
            if not isinstance(key, Optional):
                errors.append(f"Missing required field: {key_name}")
    if errors:
        return {"errors": errors}
    return validated_registration