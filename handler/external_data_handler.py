import logging
from datetime import datetime
from typing import Optional
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tikkl-webhook")

MONGO_URI = "mongodb+srv://bgmcommunications_db_user:BGM%402026@bgm2026.4pu4sjb.mongodb.net/?retryWrites=true&w=majority&appName=bgm2026"

_client: Optional[MongoClient] = None
_db = None

def connect_to_mongo():
    global _client, _db
    if _client is None:
        masked = MONGO_URI.replace(
            MONGO_URI[MONGO_URI.find("//")+2:MONGO_URI.find("@")], "****:****"
        ) if "@" in MONGO_URI else "(undefined)"
        logger.info(f"[MongoDB] Using URI: {masked}")
        _client = MongoClient(MONGO_URI, maxPoolSize=5, serverSelectionTimeoutMS=5000)
        _db = _client['bgm_referral']
        logger.info("[MongoDB] Connected successfully!")
    return _db

def insert_to_mongo(ticket_data: dict):
    db = connect_to_mongo()
    tickets = db["tickets"]
    ticket_data["created_at"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ticket_id = ticket_data.get("id") or ticket_data.get("ticket_id")
    if not ticket_id:
        ticket_id = f"auto-{int(datetime.now().timestamp())}"
        ticket_data["id"] = ticket_id
    tickets.update_one(
        {"id": ticket_id},
        {"$set": ticket_data},
        upsert=True
    )
    logger.info(f"Ticket {ticket_id} saved in MongoDB")
    return ticket_data
