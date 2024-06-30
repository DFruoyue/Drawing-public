from openpyxl import Workbook
import member as M
def export(members:list[M.Member], activity_time:str):#输出excle文件
    wb = Workbook()
    resultfile = wb.active
    resultfile['A1'] = activity_time + '活动名单'
    resultfile['B1'] = '邮件发送情况'
    i = 2
    for m in members:
        resultfile['A'+str(i)] = m.name
        resultfile['B'+str(i)] = m.result
        resultfile['C'+str(i)] = m.email_address
        resultfile['D'+str(i)] = m.group
        resultfile['E'+str(i)] = m.wechat_id
        i = i + 1
    wb.save('members in ' + activity_time + '.xlsx')
    print(activity_time + "活动名单保存成功:'members in " + activity_time + ".xlsx'")