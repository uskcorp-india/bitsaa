import boto3

dynamodb = boto3.resource('dynamodb')
room_table = dynamodb.Table('Rooms')

async def get_all_rooms_from_db():
    response = room_table.scan()
    return response.get('Items', [])
