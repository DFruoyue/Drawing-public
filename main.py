import sys
import sendemail
import activityinformation as af
import guarantee
import copy
import random
import member as M
import exportexcel as ee

TEST = False
OVERFLOW = False
members:list[M.Member] = []                #参会者
remaining_registers:list[M.Member] = []    #剩余的候选者

#确定是否为测试模式
test = input('test mode?(y/n, q for quit):')
while True:
    if test == 'y':
        TEST = True
        break
    elif test == 'n':
        TEST = False
        break
    elif test == 'q':
        sys.exit()
    else:
        test = input('Wrong input.test mode?(y/n, q for quit):')

#获取信息
sec = sender_email_config = sendemail.EmailConfig()             #获取邮箱的配置信息
ai = activity_information = af.ActivityInformation()    #获取活动信息和参与者信息 
gpp = guaranteed_prize_pool = guarantee.import_guarantee()    #获取保底池信息

#先保底再抽签
if ai.N >= len(ai.registers):#如果报名人数小于可容纳人数，全中了
    for m in ai.registers:
        members = copy.deepcopy(ai.registers)      
else:
    for r in ai.registers:#优先录取已经有两次报名记录的同学
        if r.wechat_id in gpp and (gpp[r.wechat_id]).record == 2:
            members.append(r)
        else:
            remaining_registers.append(r)
    if ai.N < len(members):
        print('Warning:保底人数已经大于活动人数!生成保底名单,但是并未发送邮件')
        print(len(members))
        SEND = False
    else:
        for i in range(ai.N-len(members)):
            lucky_dog = remaining_registers.pop(random.randint(0,len(remaining_registers)-1))
            members.append(lucky_dog)

#更新保底池
for m in members:
    if m.wechat_id in gpp:
        gpp.pop(m.wechat_id)
for m in remaining_registers:
    if m.wechat_id in gpp:
        gpp[m.wechat_id].record += 1
        gpp[m.wechat_id].name = m.name
    else:
        gpp[m.wechat_id] = M.Member(m.name, m.wechat_id, record=1)

guaranteefile = open('data.txt', mode='w', encoding='utf-8')
#将最新的gpp写入data.txt文件中
for wechat_id in gpp:
    guaranteefile.write(wechat_id + '\t' + str(gpp[wechat_id].record) + '\t' + gpp[wechat_id].name + '\n')
guaranteefile.close()

#发送邮件
if TEST:
    for m in members:
        m.result = '测试,未发送'
elif OVERFLOW:
    for m in members:
        m.result = '保底人数已经大于活动人数!未发送邮件'
else:
    for m in members:
        m.result = sendemail.send_email(receiver = m, sender_email_config = sec, activity_information = ai)

#导出结果
ee.export(members = members, activity_time = ai.activity_time)