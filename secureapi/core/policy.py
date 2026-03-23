import yaml

class PolicyLoader:
    def __init__(self, path="secureapi.yaml"):
        with open(path) as f:
            self.policies = yaml.safe_load(f)

    def __call__(self, resource, action):
        return self.policies.get(resource, {}).get(action, [])