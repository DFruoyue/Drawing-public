class Member(object):
    def __init__(self, name:str, wechat_id:str = None, group:str = None, email_address:str = None, record:int = None, result:str = None) -> None:
        self.name:str = name
        self.wechat_id:str = wechat_id
        self.group:str = group
        self.email_address:str = email_address
        self.record:int = record
        self.result:str = result