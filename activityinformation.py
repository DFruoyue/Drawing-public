import sys
import configerror  as cfg
import member as M

class ActivityInformation(object):
    def __init__(self) -> None:
        try:
            with open('activity.txt', 'r', encoding='utf-8') as activityconfigfile:
                activityconfig = {}#四个活动信息
                lines = activityconfigfile.read().splitlines()
                for i in range(4):
                    line = lines.pop()
                    if ':' in line:
                        key,value = line.split(':',1)
                        activityconfig[key] = value
                if 'activity_time' in activityconfig:
                    self.activity_time = activityconfig['activity_time']
                else:
                    raise cfg.ConfigError('activity_time未配置',1)
                if 'TimeLimit' in activityconfig:
                    self.timeLimit = activityconfig['timeLtimit']
                else:
                    raise cfg.ConfigError('timeLimit未配置',2)
                if 'ChargeLink' in activityconfig:
                    self.chargeLink = activityconfig['chargeLink']
                else:
                    raise cfg.ConfigError('chargeLink未配置',3)
                if 'N' in activityconfig:
                    self.N = int(activityconfig['N'])
                else:
                    raise cfg.ConfigError('N未配置',4)
                #载入注册着信息
                self.registers:list[M.Member] = []
                for line in lines:
                    m = line.split('\t')
                    if not m[0] == None:
                        member = M.Member(name=m[1])
                        member.wechat_id = m[0]
                        member.group = m[2]
                        member.email_address = m[3]
                        self.registers.append(member)

        except cfg.ConfigError as e:
            print(e)
            sys.exit()
        except:
            print('\'activity.cfg\'文件打开失败')
            sys.exit()