这是我为了自动地完成社团里**抽签并且发送邮件**的工作所开发出来的一个小工具。除了程序运行的文件之外，还需要其他外部文件：

1. **data.txt**：存储保底池的数据，每一项的格式为：`<wechat_id>` `<record>` `<name>` ，用制表符`\t`分隔；
2. **eamil.cfg**：发件箱的配置文件，一共需要四项，内容为：
	* sender_address:`xxx`
	* sender_password:`xxx`
	* smtp_server:`xxx`
	* smtp_port:`xxx`
3. **activity.txt**：活动信息文件，分为两个部分，第一部分是报名名单信息，每一项的格式为：`<wechat_id>` `<name>` `<group>` `<email_address>`，用制表符`\t`分隔；第二部分是活动信息，一共需要四项，内容为：
	* activity_time:`xxx`
	* TimeLimit:`xxx`
	* ChargeLink:`xxx`
	* N:`xxx`

`xxx`是需要填入的内容。