import hashlib
import uuid
import json
from decimal import Decimal
from utils.logger_factory import get_logger

class IntConvertor(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)


def generate_uuid():
    """
    Generate a random 16-character UUID.

    Returns:
        str: A 16-character UUID string.
    """
    return str(uuid.uuid4())


def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'Application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=IntConvertor)
    get_logger(__name__).info(json.loads(response['body']))
    return response

def hash_value(value):
    return hashlib.sha256(value.encode()).hexdigest()

def convert_float_to_decimal(data):
    if isinstance(data, dict):
        return {k: convert_float_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_float_to_decimal(item) for item in data]
    elif isinstance(data, float):
        return Decimal(str(data))
    else:
        return data
