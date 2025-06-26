import imaplib
import email
import os
import re
from email.header import decode_header
from email.utils import parseaddr

from handler.email_handler import send_confirmation_email
from handler.registration_handler import create, update, registration_exists

from utils.logger_factory import get_logger

logger = get_logger(__name__)

# Environment variables
IMAP_SERVER = os.environ["IMAP_SERVER"]
EMAIL_ACCOUNT = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
IMAP_PORT = int(os.environ.get("IMAP_PORT", 993))

NAME_PATTERN = r"Name[:-]?\s*([A-Za-z]+(?:[.\s][A-Za-z]+)*)"
REG_PATTERN = r"Registration\s*Number[:-]?\s*([\w-]+)"


def connect_to_mailbox():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")
    return mail


def fetch_unread_emails(mail):
    result, data = mail.search(None, "UNSEEN")
    if result != "OK":
        return []
    return data[0].split()


def parse_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset)
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset)


def extract_subject(msg):
    raw_subject = msg["Subject"]
    if raw_subject is None:
        return "(No Subject)"
    try:
        subject, encoding = decode_header(raw_subject)[0]
        if isinstance(subject, bytes):
            return subject.decode(encoding or "utf-8", errors="replace")
        return subject
    except Exception as e:
        print(f"Failed to decode subject: {e}")
        return "(Invalid Subject)"

def extract_sender_email(msg):
    from_header = msg.get("From")
    _, email_address = parseaddr(from_header)
    return email_address

def extract_name_and_registration(body):
    name = re.search(NAME_PATTERN, body, re.IGNORECASE)
    reg = re.search(REG_PATTERN, body, re.IGNORECASE)
    return (
        name.group(1).strip() if name else "Not found",
        reg.group(1).strip() if reg else "Not found"
    )


def process_email(mail, msg_num):
    result, msg_data = mail.fetch(msg_num, "(RFC822)")
    if result != "OK":
        print(f"Failed to fetch email {msg_num}")
        return

    msg = email.message_from_bytes(msg_data[0][1])
    subject = extract_subject(msg)
    body = parse_email_body(msg)
    sender_email = extract_sender_email(msg)
    name, reg = extract_name_and_registration(body)

    print(f"Email Subject: {subject}")
    print(f"Name: {name}")
    print(f"Registration Number: {reg}")
    registration = {
        "registration_no": reg,
        "fullName":name,
        "email":sender_email
    }

    print(f"registration: {registration}")
    if not registration_exists(registration['registration_no']):
        create(registration)
    else:
        update(registration['registration_no'],registration)
    send_confirmation_email(sender_email, name)
    mail.store(msg_num, '+FLAGS', '\\Seen')


def lambda_handler(event, context):
    try:
        mail = connect_to_mailbox()
        unread_msgs = fetch_unread_emails(mail)
        for msg_num in unread_msgs:
            process_email(mail, msg_num)
        mail.logout()
        print(f"{event}, {context}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise
