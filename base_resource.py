import inspect
from flask import request
from flask_restful import Resource

class BaseResource(Resource):
    """A Resource that routes HTTP verbs to custom-named handler methods."""
    
    method_map = {}  # override this in subclasses

    def dispatch_request(self, *args, **kwargs):
        # Get the name of the handler function from the method_map
        handler_name = self.method_map.get(request.method)
        if not handler_name:
            return {"message": "Method not allowed"}, 405

        handler_func = getattr(self, handler_name)

        # Handle POST and PUT requests with a JSON body
        if request.method in ["POST", "PUT"]:
            data = request.get_json(force=True, silent=True) or {}
            
            # Use inspect to get the parameter names of the handler function.
            # We exclude the 'self' parameter.
            param_names = [p.name for p in inspect.signature(handler_func).parameters.values() if p.name != 'self']
            
            # Find the first parameter that is not a URL parameter
            # (i.e., not already in kwargs). This parameter should receive the JSON body.
            body_param_name = None
            for name in param_names:
                if name not in kwargs:
                    body_param_name = name
                    break
            
            # If we found a parameter for the body, add the data to kwargs
            if body_param_name:
                kwargs[body_param_name] = data
            
            # Now call the handler function with all arguments as keyword arguments
            # to prevent positional argument conflicts.
            return handler_func(*args, **kwargs)

        # For GET/DELETE requests, just pass args and kwargs
        return handler_func(*args, **kwargs)