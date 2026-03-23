from rest_framework.permissions import BasePermission
from secureapi.core.engine import SecureEngine
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine


class SecurePermission(BasePermission):
    def has_permission(self, request, view):
        return True  # allow, actual check in object level

    def has_object_permission(self, request, view, obj):
        engine = get_engine()

        resource = view.basename  # e.g., "form"
        action = self.map_method(request.method)

        context = RequestContext(
            user=request.user,
            resource=resource,
            action=action,
            resource_id=obj.id,
            tenant_id=self.get_tenant(request),
        )

        try:
            engine.authorize(context)
            return True
        except Exception as e:
            return False

    def map_method(self, method):
        return {
            "GET": "read",
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete",
        }.get(method, "read")

    def get_tenant(self, request):
        return request.headers.get("X-Tenant-ID")