from functools import wraps
from flask import request, abort
from utils.helpers import Helper
from logger.logging import LoggerApp

helper = Helper()
LoggerApp = LoggerApp()


def check_file_extension(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("hereeeeeeeeeeeee")
        try:
            if request.method == "POST":
                if "file" not in request.files:
                    return func(*args, **kwargs)

            file = request.files["file"]
            if file.filename == "":
                abort(404, "File cannot be empty")
            if not helper.allowed_file(file.filename):
                abort(404, "Format file not allowed")

            return func(*args, **kwargs)
        except AttributeError as arttError:
            abort(401, description=f"Unauthorized: User information missing: {arttError}")

    return wrapper
