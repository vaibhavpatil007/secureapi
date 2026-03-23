from secureapi.core.engine import SecureEngine
from secureapi.core.policy import PolicyLoader


_engine = None

def get_engine():
    global _engine

    if _engine is None:
        _engine = SecureEngine(
            policy_loader=PolicyLoader(),
            role_resolver=default_role_resolver,
            resource_resolver=default_resource_resolver,
        )

    return _engine