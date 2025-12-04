import csv

import boto3

# DynamoDB table
TABLE_NAME = "registration"
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table(TABLE_NAME)

# CSV file path
csv_file = "data.csv"

# Static fields
STATIC_FIELDS = {
    "campaignName": "BITSAA Global Meet 2026",
    "campaignUrl": "https://tikkl.com/bgm/c/bgm26-hyd",
    "eventName": "BITSAA Global Meet 2026",
    "objectType": "ticket",
    "orgName": "BITSAA Global Meet",
    "orgSubdomain": "bgm",
}

# Base order URL
BASE_ORDER_URL = "https://tikkl.com/a/bgm/c/4326/participation/"

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [header.strip().replace('\ufeff', '') for header in reader.fieldnames]
    for row in reader:
        order_id = row["orderId"]  # get orderId from CSV
        print(order_id)
        print(row["date_time"])

        # Build item for DynamoDB
        item = {
            "id": row["id"],
            "registration_no": row["id"],
            "registrantName": row["first_name"] +" "+ row["last_name"],
            "registrantEmail": row["Email"],
            "orderId": order_id,
            "created_at" : row["date_time"],
            "orderTimeUtc": row["date_time"],
            "orderUrl": f"{BASE_ORDER_URL}{order_id}",
            **STATIC_FIELDS,
        }

        table.put_item(Item=item)

print("Data uploaded successfully!")
