import os
import jwt
from functools import wraps
from flask import request, abort
from utils.helpers import Helper
from logger.logging import LoggerApp
from services.token_service import TokenService
from datetime import datetime, timedelta, timezone

helper = Helper()
LoggerApp = LoggerApp()
tokenService = TokenService()


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, description="Missing or invalid token header")

        token = auth_header.split(" ")[1]
        existToken = tokenService.getTokenById(token)
        if not existToken:
            abort(401, description="Token not found")
        elif existToken.get("marked_as_used"):
            abort(401, description="Token has been marked as used in blacklist")

        try:
            payload = jwt.decode(
                existToken["token"],
                os.getenv("SECRET_KEY"),
                algorithms=["HS256"],
                options={"verify_exp": False},
            )
            request.user = payload
        except jwt.ExpiredSignatureError:
            LoggerApp.logErrorInfo({"errorMsg": "Token expired"})
            abort(401, description="Token expired")
        except jwt.InvalidTokenError:
            tokenService.createToken(token, marked_as_used=True)
            LoggerApp.logErrorInfo({"errorMsg": "Invalid token"})
            abort(401, description="Invalid token")

        return func(*args, **kwargs)

    return wrapper


def check_user_role(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if request.user["role"] != "admin":
                abort(403, description="User does not have the required role")
            return func(*args, **kwargs)
        except AttributeError:
            abort(401, description="Unauthorized: User information missing")

    return wrapper


def generateToken(userBody):
    try:
        user, _ = userBody
        payload = {
            "id": user["id"],
            "name": user["name"],
            "nick_name": user["nick_name"],
            "role": user["roles"],
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
        }
    except KeyError as e:
        LoggerApp.logErrorInfo({"tokenError": f"Missing key in userBody: {e}"})
        raise KeyError(f"Missing key in userBody: {e}")

    tokenGenerated = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    tokenService.createToken(tokenGenerated)
    return tokenGenerated
