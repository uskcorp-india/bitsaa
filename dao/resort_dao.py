from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, resort_id:dict):
    resort_id = resort_id | build_record()
    table = dynamodb.Table(common.RESORT)
    table.put_item(Item=resort_id)
    logger.info("Created resort successfully")
    return resort_id

@with_connection
def find(dynamodb, resort_id: str):
    table = dynamodb.Table(common.RESORT)
    response = table.get_item(Key={"id": resort_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"resort not found with ID: {resort_id}")

@with_connection
def update(dynamodb, resort: dict):
    table = dynamodb.Table(common.RESORT)
    resort = resort | build_record()
    update_fields = {k: v for k, v in resort.items() if k != 'id'}
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in update_fields)
    expr_attr_values = {f":{k}": v for k, v in update_fields.items()}
    expr_attr_names = {f"#{k}": k for k in update_fields}

    response = table.update_item(
        Key={"id": resort["id"]},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_attr_names,
        ExpressionAttributeValues=expr_attr_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated resort with ID {resort['id']} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, resort_id: str):
    table = dynamodb.Table(common.resort)
    table.delete_item(Key={"id": resort_id})
    logger.info(f"Deleted {common.RESORT} successfully '{resort_id}'")
    return {"action_type": f"{common.RESORT} deleted", "id": resort_id}