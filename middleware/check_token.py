import os
import jwt
from functools import wraps
from flask import request, abort
from logger.logging import LoggerApp
from datetime import datetime, timedelta, timezone

LoggerApp = LoggerApp()

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, description="Missing or invalid token header")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), do_time_check=True, algorithms=['HS256'])
            request.user = payload
        except jwt.ExpiredSignatureError:
            LoggerApp.logErrorInfo({'errorMsg': 'Token expired'})
            abort(401, description="Token expired")
        except jwt.InvalidTokenError:
            LoggerApp.logErrorInfo({'errorMsg': 'Invalid token'})
            abort(401, description="Invalid token")

        return func(*args, **kwargs)
    return wrapper

def generateToken(userBody):
    try:
        payload = {
            "id": userBody["id"],
            "name": userBody["name"],
            "nick_name": userBody["nick_name"],
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())
        }
    except KeyError as e:
        LoggerApp.logErrorInfo({'errorMsg': f"Missing key in userBody: {e}"})
        raise KeyError(f"Missing key in userBody: {e}")
    
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')