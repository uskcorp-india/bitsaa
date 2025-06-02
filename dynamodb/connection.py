from utils.utils import build_response
from utils.utils import get_logger
import boto3

logger = get_logger(__name__)

REGION = 'ap-south-1'
DYNAMODB = 'dynamodb'

def get_connection():
    return boto3.resource(DYNAMODB, region_name=REGION)

def with_connection(func):
    """Decorator to handle DynamoDB connection lifecycle."""

    def wrapper(*args, **kwargs):
        dynamodb = None
        try:
            dynamodb = get_connection()
            return func(dynamodb, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {e}")
            return build_response(500, {"error": str(e)})
        finally:
            if dynamodb and hasattr(dynamodb, 'close'):
                dynamodb.close()

    return wrapper
