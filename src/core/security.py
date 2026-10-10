from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from core.config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": now,
            'token_type': 'bearer'
        })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> dict | None:
    try:
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return token
    except ExpiredSignatureError:
        return None
    except JWTError as e:
        return None