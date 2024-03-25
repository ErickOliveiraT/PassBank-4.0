import hashlib
import base64

def to_fernet_key(password: str):
    # Use a hashing function (SHA-256) to derive a 32-byte key
    hashed_key = hashlib.sha256(password.encode()).digest()
    # Return the base64 encoded key
    return base64.urlsafe_b64encode(hashed_key)

def md5(password: str):
    return hashlib.md5(password.encode()).hexdigest()