from base_resource import BaseResource

class HealthCheckController(BaseResource):
    method_map = {
        'GET': 'healthCheck',
    }
    
    def __init__(self):
        super().__init__()
        
    def healthCheck(self):
        return {"message": "OK"}, 200  