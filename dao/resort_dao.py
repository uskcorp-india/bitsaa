from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
from utils.dao_utils import build_record
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, resort_data:dict):
    resort_data = resort_data | build_record()
    table = dynamodb.Table(common.RESORT)
    table.put_item(Item=resort_data)
    logger.info("Created resort successfully")
    return resort_data

@with_connection
def find(dynamodb, resort_id: str):
    table = dynamodb.Table(common.RESORT)
    response = table.get_item(Key={"id": resort_id})
    if "Item" in response:
        return from_attributes_to_json(response["Item"])
    else:
        raise ValueError(f"resort not found with ID: {resort_id}")

@with_connection
def find_all(dynamodb):
    table = dynamodb.Table(common.RESORT)
    response = table.scan()
    data = response.get("Items", [])
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response.get("Items", []))
    filtered_data = [resort for resort in data if resort.get("available", 0) > 0]
    return filtered_data

@with_connection
def update(dynamodb, resort_id: str, resort: dict):
    table = dynamodb.Table(common.RESORT)
    update_fields = {k: v for k, v in resort.items() if k != 'id'}
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
        Key={"id": resort_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression="attribute_exists(id)",
        ReturnValues="ALL_NEW"
    )

    logger.info(f"Updated resort with ID {resort_id} successfully")
    return response.get("Attributes", {})


@with_connection
def delete(dynamodb, resort_id: str):
    table = dynamodb.Table(common.RESORT)
    table.delete_item(Key={"id": resort_id})
    logger.info(f"Deleted {common.RESORT} successfully '{resort_id}'")
    return {"action_type": f"{common.RESORT} deleted", "id": resort_id}