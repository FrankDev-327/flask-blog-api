import os
from jwt import (JWT)
from functools import wraps
from flask import request, abort
from jwt.utils import get_int_from_datetime
from datetime import datetime, timedelta, timezone

instance = JWT()

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, description="Missing or invalid token header")

        token = auth_header.split(" ")[1]

        try:
            payload = instance.decode(token, os.getenv('SECRET_KEY'), do_time_check=True, )
            request.user = payload
        except instance.ExpiredSignatureError:
            abort(401, description="Token expired")
        except instance.InvalidTokenError:
            abort(401, description="Invalid token")

        return func(*args, **kwargs)
    return wrapper

def generateToken(userBody):
    token = {
        'name':userBody['name'],
        'nick_name':userBody['nick_name'],
        'id':userBody['id'],
        'iat': get_int_from_datetime(datetime.now(timezone.utc)),
        'exp' : get_int_from_datetime(
            datetime.now(timezone.utc) + timedelta(hours=1)
        ),
    }
    
    return instance.encode(token, os.getenv('SECRET_KEY'),)