from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, reservation:dict):
    reservation = reservation | build_record()
    reservation['status']= "pending"
    table = dynamodb.Table(common.RESERVATION)
    table.put_item(Item=reservation)
    logger.info("Created reservation successfully")
    return reservation

@with_connection
def find(dynamodb, reservation_id: str):
    table = dynamodb.Table(common.RESERVATION)
    response = table.get_item(Key={"id": reservation_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"reservation not found with ID: {reservation_id}")

@with_connection
def update(dynamodb,reservation_id, reservation: dict):
    table = dynamodb.Table(common.RESERVATION)
    update_fields = {k: v for k, v in reservation.items() if k != 'id'}
    update_expression = "SET "
    expression_attribute_names = {}
    expression_attribute_values = {}
    for key, value in update_fields.items():
        attribute_name = f"#{key}"
        expression_attribute_names[attribute_name] = key
        expression_attribute_values[f":{key}"] = value
        update_expression += f"{attribute_name} = :{key},"
    update_expression = update_expression.rstrip(", ")
    response = table.update_item(
        Key={"id": reservation_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression="attribute_exists(id)",
        ReturnValues="ALL_NEW"
    )

    logger.info(f"Updated resort with ID {reservation_id} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, reservation_id: str):
    table = dynamodb.Table(common.RESERVATION)
    table.delete_item(Key={"id": reservation_id})
    logger.info(f"Deleted {common.RESERVATION} successfully '{reservation_id}'")
    return {"action_type": f"{common.RESERVATION} deleted", "id": reservation_id}