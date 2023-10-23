from hashlib import sha256
import jwt
from datetime import datetime, timedelta
from django.conf import settings


def make_user_hash(usr: str, salt: str, pwd: str):
    hash_string = str(usr) + str(salt) + str(pwd)

    user_hash = sha256(hash_string.encode()).hexdigest()

    return user_hash


def generate_access(hash: str) -> str:
    payload = {
        'user_hash': hash,
        'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXP)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def generate_refresh(hash: str):
    payload = {
        'user_hash': hash,
        'exp': datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXP)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
