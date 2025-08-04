import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
pending_table = dynamodb.Table('pending_reservation')
reservation_table = dynamodb.Table('reservation')
resort_table = dynamodb.Table('resort')

TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def lambda_handler(event, context):
    now = datetime.now()
    expired_ids = []

    # 1. Scan pending reservations
    response = pending_table.scan()
    pending_items = response.get('Items', [])

    for item in pending_items:
        created_at_str = item.get('created_at')
        pending_id = item.get('id')

        if not created_at_str or not pending_id:
            continue  # Skip if essential data is missing

        try:
            created_at = datetime.strptime(created_at_str, TIME_FORMAT)
        except ValueError:
            print(f"[WARN] Invalid date format: {created_at_str}")
            continue

        # 2. Check if older than 10 minutes
        if (now - created_at).total_seconds() > 600:
            try:
                # 3. Fetch reservation by ID
                reservation = reservation_table.get_item(Key={'id': pending_id}).get('Item')
                if not reservation:
                    print(f"[WARN] Reservation not found for id: {pending_id}")
                    continue

                resort_info = reservation.get('resort', {})
                resort_id = resort_info.get('id')
                room_count = int(reservation.get('room_count', 1))

                if resort_id:
                    # 4. Update resort: release blocked room(s)
                    try:
                        resort_table.update_item(
                            Key={'id': resort_id},
                            UpdateExpression='SET blocked_rooms = blocked_rooms - :rooms, available = available + :rooms',
                            ExpressionAttributeValues={':rooms': room_count}
                        )
                        print(f"[OK] Unblocked {room_count} rooms for resort {resort_id}")
                    except Exception as e:
                        print(f"[ERR] Failed to update resort {resort_id}: {e}")

                # 5. Remove from pending_reservation
                pending_table.delete_item(Key={'id': pending_id})
                expired_ids.append(pending_id)

            except Exception as e:
                print(f"[ERROR] Failed processing {pending_id}: {e}")
                print({
                'message': f"Processed {len(expired_ids)} expired reservations",
                'expired_ids': expired_ids
            })

    return {
        'message': f"Processed {len(expired_ids)} expired reservations",
        'expired_ids': expired_ids
    }
