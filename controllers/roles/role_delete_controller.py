from base_resource import BaseResource
from services.role_service import RoleService
from middleware.check_token import require_token, check_user_role

class RoleDeleteController(BaseResource):
    method_map = { 'DELETE': 'removeRoleFromUser' }
    
    def __init__(self):
        super().__init__()
        self.role_service = RoleService()
        
    @require_token
    @check_user_role
    def removeRoleFromUser(self, roleBody):
        return self.role_service.removeRoleFromUser(roleBody)