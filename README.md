这是我为了自动地完成社团里**抽签并且发送邮件**的工作所开发出来的一个小工具。除了程序运行的文件之外，还需要其他外部文件：

1. **guarantee_data.json**：存储保底池的数据，包含两个项：
	* `"last_modified_time": "xxxx年xx月xx日xx:xx:xx"`
	* `"members":[{"name":"xxx","wechat_id":"xxx","record":n},...]`
2. **eamil.cfg**：发件箱的配置文件，一共需要四项，内容为：
	* `"sender_address":"xxx"`
	* `"sender_password":"xxx"`
	* `"smtp_server":"xxx"`
	* `"smtp_port":"xxx"`
3. **activity_config.json**：活动信息，一共需要四项，内容为：
	* `"Updated":true`			(bool)
	* `"activity_time":"xxx"`	(str)
	* `"TimeLimit":"xxx"`		(str)
	* `"ChargeLink":"xxx"`		(str)
	* `"N":n`					(int)
4. **applicants.txt**：报名名单，直接从excel表复制过来就好。每一项的格式为：`<wechat_id>` `<name>` `<group>` `<email_address>`，用制表符`\t`分隔。