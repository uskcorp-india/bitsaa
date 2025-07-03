import os
import hmac
import hashlib
import base64

def is_valid_tikkl_signature(signature: str, body: str | bytes, is_base64: bool) -> bool:
    secret = os.environ.get("TIKKL_SECRET")
    if not secret:
        print("Missing TIKKL_SECRET environment variable")
        return False

    if is_base64:
        if isinstance(body, str):
            try:
                body_bytes = base64.b64decode(body)
            except Exception as e:
                print("Base64 decoding error:", e)
                return False
        else:
            body_bytes = body
    else:
        body_bytes = body.encode("utf-8") if isinstance(body, str) else body

    computed_signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=body_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    print(f"Provided signature: {signature}")
    print(f"Computed signature: {computed_signature}")

    return hmac.compare_digest(signature, computed_signature)
