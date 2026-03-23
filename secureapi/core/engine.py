class SecureEngine:
    def __init__(self, policy_loader, role_resolver, resource_resolver):
        self.policy_loader = policy_loader
        self.role_resolver = role_resolver
        self.resource_resolver = resource_resolver

    def authorize(self, context):
        user = context.user
        resource = context.resource
        action = context.action
        resource_id = context.resource_id
        tenant_id = context.tenant_id

        # Step 1: Get role
        role = self.role_resolver(user, tenant_id)

        # Step 2: Get policy
        allowed_roles = self.policy_loader(resource, action)

        if role not in allowed_roles:
            raise Exception(f"Role '{role}' not allowed")

        # Step 3: Fetch object
        obj = self.resource_resolver(resource, resource_id)

        # Step 4: Tenant check
        if hasattr(obj, "tenant_id") and obj.tenant_id != tenant_id:
            raise Exception("Cross-tenant access denied")

        # Step 5: Ownership check
        if "owner" in allowed_roles:
            if hasattr(obj, "created_by_id"):
                if obj.created_by_id != user.id and role != "admin":
                    raise Exception("Not owner")

        return True