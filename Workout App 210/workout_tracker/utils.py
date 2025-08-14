import hashlib

def hash_password(p: str) -> str:
    """Return a sha256 hash for a plain-text password."""
    return hashlib.sha256(p.encode()).hexdigest()

