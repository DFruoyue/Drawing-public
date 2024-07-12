from .Member import Member as M
import json
import datetime
class GuaranteedMember(M):
    def __init__(self, name_or_member, wechat_id:str = None, record:int = None) -> None:
        if isinstance(name_or_member, M):
            self._name = name_or_member._name
            self._wechat_id = name_or_member._wechat_id
            self._record = record
        else:
            self._name = name_or_member
            self._wechat_id = wechat_id
            self._record = record
    def __str__(self) -> str:
        return f'{self._wechat_id}:{self._name}'
    __repr__ = __str__

class GuaranteedPool(object):
    __members: dict[str, GuaranteedMember] = {}
    __last_modified_time = None
    #初始化
    def __init__(self,guarantee_data_file:str) -> None:
        self.__load_data(guarantee_data_file)

    #私有方法
    #加载数据
    def __load_data(self, guarantee_data_file:str) -> None:
        try:
            with open(guarantee_data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.__last_modified_time = data['last_modified_time']  # 获取并存储文件的最后修改时间
                for member_data in data['members']:
                    member = GuaranteedMember( 
                        name_or_member=member_data['name'],
                        wechat_id=member_data['wechat_id'],
                        record=member_data['record']
                    )
                    self.__members[member._wechat_id] = member
                print(f"保底数据来自于{str(self.__last_modified_time)}")
        except FileNotFoundError:
            print(f"File {guarantee_data_file} not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON.")

    #判断是否有该成员
    def __has_member(self, member:M) -> bool:
        return member._wechat_id in self.__members
    
    #判断该成员是否保底
    def __guarantee(self, member:M) -> bool:
        if not self.__has_member(member):
            return False
        return self.__members[member._wechat_id]._record == 2
    
    #添加记录次数
    def __add_record(self, memberToadd:M) -> None:
        if memberToadd._wechat_id in self.__members:
            self.__members[memberToadd._wechat_id]._record += 1
            self.__members[memberToadd._wechat_id]._name = memberToadd._name
        else:
            self.__members[memberToadd._wechat_id] = GuaranteedMember(memberToadd, record=1)
    
    #公有方法
    #保存数据
    def save_data(self, guarantee_data_file:str) -> None:
        data = {
            'last_modified_time':datetime.datetime.now().strftime('%Y年%m月%d日%H:%M:%S'), # 存储当前时间
            'members':[]
        }
        for member in self.__members.values():
            data['members'].append({
                'name':member._name,
                'wechat_id':member._wechat_id,
                'record':member._record,
            })
        with open(guarantee_data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    #产生保底名单type:list[M],并且更新申请人列表
    def get_Baildeout_list(self, applicants:list[M]) -> list[M]:
        bailout_list = []
        new_applicants = []
        for applicant in applicants:
            if self.__guarantee(applicant):
                bailout_list.append(applicant)
            else:
                new_applicants.append(applicant)
        applicants = new_applicants
        return bailout_list
    
    #更新保底名单
    def update(self, lucky_dogs:list[M], next_times:list[M]) -> None:
        for lucky_dog in lucky_dogs:
            if lucky_dog._wechat_id in self.__members:
                del self.__members[lucky_dog._wechat_id]
        for next_time in next_times:
            self.__add_record(next_time)