from .Member import Member as M
from enum import Enum
import json
from datetime import datetime
import random
from openpyxl import Workbook
from .configerror import ConfigError
import sys
current_time= datetime.now().time()

class Result(Enum):
    Undefined = None
    Test = '测试中'
    Sent = '邮件发送成功'
    Failed = '邮件发送失败！'
    def __str__(self) -> str:
        return f'{self.value}'
    __repr__ = __str__

class Applicant(M):
    def __init__(self, name:str, wechat_id:str = None, group:str = None, email_address:str = None, result:Result = None) -> None:
        super().__init__(name, wechat_id)
        self._group:str = group
        self._email_address:str = email_address
        self._result:Result = result

class Activity(object):
    _activity_time:str = None
    _timeLimit:str = None
    _chargeLink:str = None
    _N:int = None
    _activity_config_file = None
    applicants:list[Applicant] = []
    lucky_dogs:list[Applicant] = []

    #初始化
    def __init__(self, activity_config_file:str, applicants_file:str) -> None:
        self._activity_config_file = activity_config_file
        self.__load_activity_config()
        self.__load_applicants(applicants_file)
    #私有方法
    #删除实例   

    #获取活动时间等信息
    def __load_activity_config(self) -> None:
        try:
            with open(self._activity_config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                self._activity_time = config_data.get('activity_time', None)
                self._timeLimit = config_data.get('timeLimit', None)
                self._chargeLink = config_data.get('chargeLink', None)
                self._N = config_data.get('N', None)
                if not config_data.get('Updated', None):
                    raise ConfigError(f"----------活动设置文件错误,错误信息:[未填写活动信息或者未更新Updated字段]----------")
        except ConfigError as e:
            print(e)
            sys.exit()
        except FileNotFoundError:
            print(f"----------活动设置文件错误,错误信息:[未找到'{self._activity_config_file}'文件]----------")
            sys.exit()
        except json.JSONDecodeError:
            print(f"----------活动设置文件错误,错误信息:['{self._activity_config_file}'文件内容违反Json规则]----------")
            sys.exit()
        except Exception as e:
            print(f"----------活动设置文件错误,错误信息:[未预测到的错误:{e}]----------")
            sys.exit()

    #获取申请人信息
    def __load_applicants(self, applicants_file:str) -> None:
        try:
            with open(applicants_file, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()
                for line in lines:
                    m = line.split('\t')
                    if not m[0] == None:
                        applicant = Applicant(name=m[1], wechat_id=m[0], group=m[2], email_address=m[3])
                        self.applicants.append(applicant)
        except FileNotFoundError:
            print(f"----------申请人文件错误,错误信息:[未找到'{applicants_file}'文件]----------")
        except Exception as e:
            print(f"----------申请人文件错误,错误信息:[未预测到的错误:{e}]----------")

    def __exportExcel(self):#输出excle文件
        wb = Workbook()
        resultfile = wb.active
        resultfile['A1'] = '活动名单'
        resultfile['B1'] = '邮件发送情况'
        resultfile['C1'] = '邮箱'
        resultfile['D1'] = '群来源'
        resultfile['E1'] = '微信号'
        columns = ['A', 'B', 'C', 'D', 'E']
        attributes = ['_name', '_result', '_email_address', '_group', '_wechat_id']
        for index, member in enumerate(self.lucky_dogs, start=2):
            for col, attr in zip(columns, attributes):
                resultfile[f'{col}{index}'] = getattr(member, attr)
        wb.save(self._activity_time + '活动名单.xlsx')
        print(self._activity_time + "活动名单保存成功:'" + self._activity_time + "活动名单.xlsx'")
    '''
        wb = Workbook()
        resultfile = wb.active
        resultfile['A1'] = activity_time + '活动名单'
        resultfile['B1'] = '邮件发送情况'
        resultfile['C1'] = '邮箱'
        resultfile['D1'] = '群来源'
        resultfile['E1'] = '微信号'
        columns = ['A', 'B', 'C', 'D', 'E']
        attributes = ['_name', '_result', '_email_address', '_group', '_wechat_id']
        for index, member in enumerate(members, start=2):
            for col, attr in zip(columns, attributes):
                resultfile[f'{col}{index}'] = getattr(member, attr)
        wb.save(activity_time + '活动名单.xlsx')
        print(activity_time + "活动名单保存成功:'" + activity_time + "活动名单.xlsx'")
    '''

    #公有方法
    #抽奖,并且更新申请人列表
    def draw(self) -> None:
        add_lucky_dogs = random.sample(self.applicants, self._N)    # 随机选择幸运者
        self.lucky_dogs.extend(add_lucky_dogs)
        for lucky_dog in add_lucky_dogs:
            self.applicants.remove(lucky_dog)  # 更新原始列表
    
    #保存数据
    def save_data(self) -> None:
        self.__exportExcel()
    
    #清空活动设置文件
    def clear_activity_config(self) -> None:
        try:
            with open(self._activity_config_file, 'w', encoding='utf-8') as file:
                data = {
                    'Updated':False,
                    'activity_time':'???',
                    'timeLimit':'???',
                    'chargeLink':'???',
                    'N':0
                }
                json.dump(data, file, ensure_ascii=False, indent=4)
                print('活动设置文件已清空')
        except Exception as e:
            print(f"----------活动设置文件错误,错误信息:[未预测到的错误:{e}]----------")

