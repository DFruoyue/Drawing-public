class Member(object):
    def __init__(self, name_or_member, wechat_id = None):
        if isinstance(name_or_member, Member):
            # 如果第一个参数是Member实例，复制其属性
            self._name = name_or_member._name
            self._wechat_id = name_or_member._wechat_id
        else:
            # 否则，按照name和wechat_id处理
            self._name = name_or_member
            self._wechat_id = wechat_id
    
    def __str__(self) -> str:
        return f'{self._wechat_id}:{self._name}'
    __repr__ = __str__
    def __eq__(self, other) -> bool:
        return self._wechat_id == other._wechat_id