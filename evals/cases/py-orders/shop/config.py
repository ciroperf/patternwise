class ConfigManager:
    _instance = None

    def __init__(self):
        self.settings = {"payments_enabled": True, "orders_count": 0, "currency": "EUR"}

    @staticmethod
    def get_instance():
        if ConfigManager._instance is None:
            ConfigManager._instance = ConfigManager()
        return ConfigManager._instance
