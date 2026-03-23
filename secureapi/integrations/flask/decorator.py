from functools import wraps
from flask import request, jsonify
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine


def secure_endpoint(resource, action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            engine = get_engine()

            user = request.user
            tenant_id = request.headers.get("X-Tenant-ID")
            resource_id = kwargs.get(f"{resource}_id")

            context = RequestContext(
                user=user,
                resource=resource,
                action=action,
                resource_id=resource_id,
                tenant_id=tenant_id,
            )

            try:
                engine.authorize(context)
            except Exception as e:
                return jsonify({"error": str(e)}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator