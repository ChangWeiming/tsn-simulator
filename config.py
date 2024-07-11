import json

class Config:
    def __init__(self, config_path) -> None:
        f = open(config_path)
        s = f.read()
        configs = json.loads(s)
        f.close()
        self.config_map = configs
    def get_config_map(self):
        return self.config_map
    
    def get_value_with_default(self, key, default_val):
        if key not in self.config_map:
            return default_val
        return self.config_map[key]

    def get(self, key):
        return self.config_map[key]