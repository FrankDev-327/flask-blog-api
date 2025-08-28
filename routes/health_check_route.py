from flask_restful import Api
from controllers.health_check import HealthCheckController

def register_health_check_route(api: Api):
    api.add_resource(HealthCheckController, '/health-check', methods=['GET'], endpoint='health_check')
