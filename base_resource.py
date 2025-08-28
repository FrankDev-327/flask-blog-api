from flask import request
from flask_restful import Resource

class BaseResource(Resource):
    """A Resource that routes HTTP verbs to custom-named handler methods."""
    
    method_map = {}  # override this in subclasses

    def dispatch_request(self, *args, **kwargs):
        handler = self.method_map.get(request.method)
        if not handler:
            return {"message": "Method not allowed"}, 405

        # If POST or PUT, grab JSON body and pass it explicitly
        if request.method in ["POST", "PUT"]:
            data = request.get_json(force=True, silent=True) or {}
            return getattr(self, handler)(data, *args, **kwargs)

        # For GET/DELETE, just pass args
        return getattr(self, handler)(*args, **kwargs)