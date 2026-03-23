from fastapi import Depends, HTTPException
from secureapi.core.context import RequestContext
from secureapi.config.loader import get_engine


def secure_dependency(resource, action):
    def wrapper(user=Depends(get_current_user), tenant_id=None, resource_id=None):
        engine = get_engine()

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
            raise HTTPException(status_code=403, detail=str(e))

    return wrapper