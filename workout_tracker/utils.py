import hashlib

def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()

