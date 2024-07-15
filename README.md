这是我为了自动地完成社团里**抽签并且发送邮件**的工作所开发出来的一个小工具。除了程序运行的文件之外，还需要其他外部文件，并且存储在`setting` 文件夹下，即根目录下的包含关系为：

```
root/
	library/...
	setting/
		guarantee_data.json
		email_config.json
		activity_config.json
		applicants.txt
	ConvertToJson(guarantee).py
	main.py
```

setting中四个外部文件的内容如下：

1. `guarantee_data.json`存储保底池的数据

  ```json
  {
  	"last_modified_time": "2024年07月12日17:05:41",
  	"members": [
  		{
  			"name": "xxx",
  			"wechat_id": "vx_114514",
  			"record": 1
  		},
      ...
  	]
  }
  ```
2. `eamil_config.json`发件箱的配置文件

  ```json
  {
  	"smtp_server": "example.123.com",
  	"smtp_port": 000,
  	"sender_address": "DFruoyue@example.com",
  	"sender_password": "ABCDEFG"
  }
  ```
3. `activity_config.json`活动信息

  ```json
  {
  	"Updated": false,
  	"activity_time": "x年x月x日x时",
  	"timeLimit": "x年x月x日x时",
  	"chargeLink": "http://chargeLink.example",
  	"N": 0
  }
  ```

  注意此处`Updated`项用于确保该文件是已经填写了的——只有当该项为`true`时程序才能运行，并且每次运行都会将该项复位为`false`，填写后需要手动置为`true`。
4. `applicants.txt`报名名单，直接从excel表复制过来。
	`<wechat_id>` `<name>` `<group>` `<email_address>`
	用制表符`\t`分隔。

	```
	vx_id	name	group	email
	```