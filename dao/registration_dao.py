from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, registration_data:dict):
    registration_data = registration_data | build_record()
    table = dynamodb.Table(common.REGISTRATION)
    table.put_item(Item=registration_data)
    logger.info("Created registration successfully")
    return registration_data

@with_connection
def find(dynamodb, registration_id: str):
    table = dynamodb.Table(common.REGISTRATION)
    response = table.get_item(Key={"id": registration_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"User not found with ID: {registration_id}")

@with_connection
def update(dynamodb, registration_data: dict):
    table = dynamodb.Table(common.REGISTRATION)
    registration_data = registration_data | build_record()
    update_fields = {k: v for k, v in registration_data.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": registration_data["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated registration with ID {registration_data['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, registration_id: str):
    table = dynamodb.Table(common.REGISTRATION)
    table.delete_item(Key={"id": registration_id})
    logger.info(f"Deleted {common.REGISTRATION} successfully '{registration_id}'")
    return {"action_type": f"{common.REGISTRATION} deleted", "id": registration_id}