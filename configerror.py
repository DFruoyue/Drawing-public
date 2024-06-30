#配置错误异常
class ConfigError(Exception):
    def __init__(self, message, code)->None:
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self)->None:
        return f"[ConfigError {self.code}]: {self.message}"