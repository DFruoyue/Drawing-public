from library import *
import sys

#是否进行测试
TEST = True
while True:
    x = input("是否进行测试? [y/n/q]: ")
    if x in ["y", "n", "q"]:
        match x:
            case 'y':   TEST = True
            case 'n':   TEST = False
            case 'q':
                print('退出程序')
                sys.exit()
        break
    else:
        print("无效输入.请输入 'y' for yes, 'n' for no, 或者 'q' to quit.")

#文件路径
applicants_file = 'setting/applicants.txt'
activity_config_file = 'setting/activity_config.json'
guarantee_data_file = 'setting/guarantee_data.json'
email_config_file = 'setting/email_config.json'

#初始化,读取配置文件
activity = Activity(activity_config_file, applicants_file)
guaranteed_pool = GuaranteedPool(guarantee_data_file)
email = Email(email_config_file)

#生成保底名单
activity.lucky_dogs = guaranteed_pool.get_Baildeout_list(activity.applicants)

#抽签
activity.draw()

#更新保底名单
guaranteed_pool.update(activity.lucky_dogs, activity.applicants)

#发送邮件,第二个参数表示是否是测试模式
email.send(activity,TEST)

#保存数据
activity.save_data()
activity.clear_activity_config()
guaranteed_pool.save_data(guarantee_data_file)