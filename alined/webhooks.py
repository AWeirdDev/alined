import base64
import hmac
import hashlib


def verify_signature(channel_secret: str, body: bytes, signature: str) -> bool:
    # Create a new hash
    hsh = hmac.new(channel_secret.encode("utf-8"), body, hashlib.sha256).digest()

    # Verify the hash
    return signature.encode("utf-8") == base64.b64encode(hsh)
