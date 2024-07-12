class ConfigError(Exception):
    def __init__(self, message:str) -> None:
        self.message:str = message
    def __str__(self) -> str:
        return f'----------活动设置文件错误,错误信息:[{self.message}]----------'
    __repr__ = __str__