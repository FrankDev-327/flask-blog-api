from base_resource import BaseResource
from services.role_service import RoleService

class RoleController(BaseResource):
    method_map = {
        'POST': 'assignRoToUser',
    }
    
    def __init__(self):
        super().__init__()
        self.role_service = RoleService()
        
    def assignRoToUser(self, roleBody):
        return self.role_service.assignRoToUser(roleBody)