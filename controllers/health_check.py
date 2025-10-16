from flask_restful import Resource


class HealthCheckController(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        return {"message": "OK"}, 200