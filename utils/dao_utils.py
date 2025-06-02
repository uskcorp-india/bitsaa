from datetime import datetime
from dynamodb_json import json_util
from utils.utils import generate_uuid

def build_record():
    return {
        "id": generate_uuid(),
        "status": True,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

def from_attributes_to_json(attribute: dict):
    return json_util.loads(attribute)