from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, booking_data:dict):
    booking_data = booking_data | build_record()
    table = dynamodb.Table(common.BOOKING)
    table.put_item(Item=booking_data)
    logger.info("Created booking successfully")
    return booking_data

@with_connection
def find(dynamodb, booking_id: str):
    table = dynamodb.Table(common.BOOKING)
    response = table.get_item(Key={"id": booking_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"User not found with ID: {booking_id}")

@with_connection
def update(dynamodb, booking_data: dict):
    table = dynamodb.Table(common.BOOKING)
    booking_data = booking_data | build_record()
    update_fields = {k: v for k, v in booking_data.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": booking_data["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated booking with ID {booking_data['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, booking_id: str):
    table = dynamodb.Table(common.BOOKING)
    table.delete_item(Key={"id": booking_id})
    logger.info(f"Deleted {common.BOOKING} successfully '{booking_id}'")
    return {"action_type": f"{common.BOOKING} deleted", "id": booking_id}