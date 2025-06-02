from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, reservation_id_data:dict):
    reservation_id_data = reservation_id_data | build_record()
    table = dynamodb.Table(common.RESERVATION)
    table.put_item(Item=reservation_id_data)
    logger.info("Created booking successfully")
    return reservation_id_data

@with_connection
def find(dynamodb, reservation_id: str):
    table = dynamodb.Table(common.RESERVATION)
    response = table.get_item(Key={"id": reservation_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"User not found with ID: {reservation_id}")

@with_connection
def update(dynamodb, reservation: dict):
    table = dynamodb.Table(common.RESERVATION)
    reservation = reservation | build_record()
    update_fields = {k: v for k, v in reservation.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": reservation["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated reservation with ID {reservation['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, reservation_id: str):
    table = dynamodb.Table(common.RESERVATION)
    table.delete_item(Key={"id": reservation_id})
    logger.info(f"Deleted {common.RESERVATION} successfully '{reservation_id}'")
    return {"action_type": f"{common.RESERVATION} deleted", "id": reservation_id}