import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('Users')

async def register_user_in_db(data):
    user_id = str(uuid.uuid4())
    data['user_id'] = user_id
    user_table.put_item(Item=data)
    return {"user_id": user_id}
