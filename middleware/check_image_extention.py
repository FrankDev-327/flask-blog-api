from functools import wraps
from flask import request, abort
from utils.helpers import Helper
from logger.logging import LoggerApp

helper = Helper()
LoggerApp = LoggerApp()
ALLOWED_EXTENSIONS = {"txt", "png", "gif", "jpg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_file_extension(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if request.method == "POST":
                if "file" not in request.files:
                    return func(*args, **kwargs)

            file = request.files["file"]
            if file.filename == "":
                abort(404, "File cannot be empty")
            if not allowed_file(file.filename):
                abort(404, "Format file not allowed")

        except AttributeError as arttError:
            abort(401, description=f"Format file not allowed: {arttError}")

        return func(*args, **kwargs)

    return wrapper
