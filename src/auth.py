from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(plain: str):
    hash = ph.hash(plain)
    return hash


def verify_password(plain: str, hash: str):
    try:
        return ph.verify(hash, plain)
    except:
        return False
