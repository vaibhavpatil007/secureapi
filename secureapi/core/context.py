class RequestContext:
    def __init__(self, user, resource, action, resource_id, tenant_id):
        self.user = user
        self.resource = resource
        self.action = action
        self.resource_id = resource_id
        self.tenant_id = tenant_id