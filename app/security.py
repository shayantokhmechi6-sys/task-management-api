from argon2 import PasswordHasher
from jose import jwt
from datetime import datetime, timedelta,timezone
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")
passwordhasher=PasswordHasher()

def hash_password(password):
    password_hash=passwordhasher.hash(password)
    return password_hash

def verify_password(password,password_hash):
    result=passwordhasher.verify(password_hash,password)
    return result


ALGORITHM = "HS256"


def create_access_token(user_id):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token