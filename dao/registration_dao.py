import datetime
from dynamodb.connection import with_connection
from utils.logger_factory import get_logger
import constants.common as common
from utils.dao_utils import from_attributes_to_json

logger = get_logger(__name__)
@with_connection
def create(dynamodb, registration_data:dict):
    logger.info(f"response: {registration_data}")
    registration_data['id'] = registration_data['registration_no']
    registration_data['created_at'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    table = dynamodb.Table(common.REGISTRATION)
    table.put_item(Item=registration_data)
    logger.info("Created registration successfully")
    return registration_data

@with_connection
def find(dynamodb, registration_id: str):
    table = dynamodb.Table(common.REGISTRATION)
    response = table.get_item(Key={"id": registration_id})
    return from_attributes_to_json(response)

@with_connection
def registration_exists(dynamodb, registration_id: str) -> bool:
    table = dynamodb.Table(common.REGISTRATION)
    response = table.get_item(Key={"id": registration_id}, ProjectionExpression="id")
    return "Item" in response

@with_connection
def update(dynamodb,registration_id, registration_data: dict):
    table = dynamodb.Table(common.REGISTRATION)
    registration_data['updated_at'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    update_fields = {k: v for k, v in registration_data.items() if k != 'id'}
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
        Key={"id": registration_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )
    logger.info(f"Updated resort with ID {registration_id} successfully")
    return response.get("Attributes", {})

@with_connection
def delete(dynamodb, registration_id: str):
    table = dynamodb.Table(common.REGISTRATION)
    table.delete_item(Key={"id": registration_id})
    logger.info(f"Deleted {common.REGISTRATION} successfully '{registration_id}'")
    return {"action_type": f"{common.REGISTRATION} deleted", "id": registration_id}