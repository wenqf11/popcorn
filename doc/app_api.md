## 用户模块

### 用户登录

- 请求地址：http://domain.com/app/login/
- 请求方式：GET
- 请求参数：
	- **username**，`string`，用户名
	- **password**，`string`，密码
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：status返回用户是否登录成功，data返回token或错误信息
- json示例：

		{
			status: "ok",
			data: "joD932Lujdo2i"
		}
	或

		{
			status: "error",
			data: "user not exists"
		}

### 修改密码

- 请求地址：http://domain.com/app/password/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **password**，`string`，密码
	- **new_password**，`string`，新密码
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：status返回是否修改成功，失败则data返回错误信息
- json示例：

		{
			status: "ok",
			data: "password changed"
		}
	或

		{
			status: "error",
			data: "wrong password"
		}

### 获取用户信息

- 请求地址：http://domain.com/app/userinfo/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：该用户的用户信息
- json示例：

		{
			status: "ok",
			data: {
				username: "yl-1993",
				name: "杨磊",
				department: "空调组",
				state: "在岗",
				gender: "男",
				mobile: "18810651000",
				email: "yanglei11@mails.tsinghua.edu.cn",
				address: "紫荆1#404A",
				zipcode: "100084",
				birthday: "1993-05-28",
				id_card: "110104199305283421",
				card_type: "身份证",
				content: "what?",
				memo: "hahahahaha",
				contact: "某个人",
				contact_mobile: "13012348765",
				status: "审核通过",
				todo: 5
			}
		}

### 获取积分

- 请求地址：http://domain.com/app/score/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **year**，`int`，所要查询积分的年份，如2015
	- **month**，`int`，所要查询积分的月份，如5
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：该用户的积分
- json示例：

		{
			status: "ok",
			data: 10
		}
	或

		{
			status: "error",
			data: "score not exist for this user"
		}

### 获取积分排名

- 请求地址：http://domain.com/app/score/rank/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **year**，`int`，所要查询积分的年份，如2015
	- **month**，`int`，所要查询积分的月份，如5
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：所有用户在所查询月份的积分，返回结果按积分降序排列
- json示例：

		{
			status: "ok",
			data: [
				{ username: "hahehi", name: "zhangsan", score: 24 },
				{ username: "syb", name:"lisi", score: 23 },
				{ username: "yanglei", name:"wangwu", score: 10 }
			]
		}
	或

		{
			status: "ok",
			data: []
		}

### 抢彩蛋

- 请求地址：http://domain.com/app/egg/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：`bonus`为本次抢彩蛋的奖金，`probability`为中奖概率，`result`为是否中奖
- json示例：

		{
			status: "ok",
			data: {
				bonus: 20.0,
				probability: 0.1,
				result: true
			}
		}
	或

		{
			status: "ok",
			data: {
				bonus: 50.0,
				probability: 0.05,
				result: false
			}
		}

### 彩蛋信息查询

- 请求地址：http://domain.com/app/egg/info/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **date**，`string`，要查询的日期，如“2015-05-22”
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：`bonus`为当次抢彩蛋的奖金，`probability`为当日中奖概率，`result`为是否中奖
- json示例：

		{
			status: "ok",
			data: {
				bonus: 20.0,
				probability: 0.1,
				result: true
			}
		}
	或

		{
			status: "error",
			data: "element not exists"
		}

## 考勤模块

### 获取上下班数据

- 请求地址：http://domain.com/app/checkinfo/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **date**，`string`，要查询的日期，如“2015-05-22”
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：该日期该用户签到签退的时间，如果是晚班则签退日期是下一天
- json示例：

		{
			status: "ok",
			data: {
				checkin: "2015-05-13 08:32:59 北京市海淀区清华园1号",
				checkout: "2015-05-13 18:35:11 北京市海淀区清华园1号"
			}
		}
	或

		{
			status: "error",
			data: "work info not exist"
		}

### 更新上下班数据

- 请求地址：http://domain.com/app/check/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **date**，`string`，上下班日期，夜班的话以上班日期为准
	- **checkin**，`string`，上班时间以及地点
	- **checkout**，`string`，下班时间以及地点
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：是否签到成功
- json示例：

		{
			status: "ok",
			data: "check info update success"
		}
	或

		{
			status: "error",
			data: "check info existed"
		}

## 设备模块

### 获取所有设备简称

- 请求地址：http://domain.com/app/device/brief/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：所有设备的简称brief
- json示例：

		{
			status: "ok",
			data: ["ks304921", "kt931121", "dj239932", "gl991223"]
		}

### 获取设备信息

- 请求地址：http://domain.com/app/device/info/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **device_brief**，`string`，设备简称
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：所查询设备的基本信息
- json示例：

		{
			status: "ok",
			data: {
				id: 2,
				brief: "kz084732",
				name: "kz设备名称",
				producer: "HUAWEI",
				type: "kernel",
				serial: "10086-10000-4008823823",
				brand: "certain brand",
				model: "haha",
				bought_time: "2011-02-17",
				location: "c#210",
				memo: ""
			}
		}

## 抄表模块

### 获取当日巡视路线列表

- 请求地址：http://domain.com/app/route/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：该用户当日要巡视的所有路线
- json示例：

		{
			status: "ok",
			data: [
				{
					id: 1,					// 路线在数据库中的id
					name: "线路一",			// 路线名称
					start_time: "08:00",	// 路线起始巡视时间
					interval: 2,			// 巡视周期（小时）
					checked: 1				// 是否巡视完毕（未实现）
				},
				{
					id: 1,
					name: "线路一",
					start_time: "08:00",
					interval: 2,
					checked: 0
				},
				{
					id: 2,
					name: "线路二",
					start_time: "10:00",
					interval: 4,
					checked: 0
				},
			]
		}

### 获取路线上的设备列表

- 请求地址：http://domain.com/app/form/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **route_id**，`int`，要查询的路线id，获取此路线上的所有设备
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：指定id路线上的所有设备信息，抄表表单以表单项数组返回
- json示例：

		{
			status: "OK",
			data: [
				{
					id: 12,
					name: "kt094732",
					content: [
						{
							name: "设备状态",
							choice: true,
							choices: ["正常", "异常"],
							memo: "重要"
						},
						{
							name: "压力",
							choice: false,
							unit: "MPa",
							min: "12",
							max: "18",
							memo: "重要"
						}
					]
				},
				{
					id: 32,
					name: "ms383831",
					content: [
						{
							name: "设备状态",
							choice: true,
							choices: ["正常", "异常"],
							memo: "重要"
						}
					]
				}
			]
		}

## 保养模块

### 获取保养任务列表

- 请求地址：http://domain.com/app/maintain/list/1/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：获取到的保养任务列表，以数组形式返回
- json示例：

		{
			status: "ok",
			data: [
				{
					id: 24,
					title: "空调每月保养计划",
					device_name: "空调05",
					device_breif: "kt028462",
					creator: "张三",
					create_time: "2015-04-21 12:02:02",
					description: "积灰过多，需清灰",
					image: "http://domain.com/static/05.jpg",
					memo: "较重要，需优先处理",
					confirmed: false,
					note: ""
				},
				{
					id: 36,
					title: "锅炉每周保养计划",
					device_name: "锅炉2",
					device_breif: "gt135212",
					creator: "李四",
					create_time: "2015-05-04 21:06:01",
					description: "需进行某项操作",
					image: "http://domain.com/static/23.jpg",
					memo: "一般重要",
					confirmed: true,
					note: "保养还未结束，目前状况良好"
				}
			]
		}
	或

		{
			status: "ok",
			data: []
		}

### 确认接受保养任务

- 请求地址：http://domain.com/app/maintain/confirm/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要接受的保养任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：确认保养任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task confirmed"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

### 更新保养计划

- 请求地址：http://domain.com/app/maintain/update/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要更新的保养任务id
	- **note**，`string`，更新的保养记录
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：更新保养计划是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task updated"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

### 完成保养任务

- 请求地址：http://domain.com/app/maintain/submit/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要提交的保养任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：提交保养任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task submitted"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

## 维修模块

### 新建维修任务

- 请求地址：http://domain.com/app/maintain/add/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **device_brief**，`int`，设备简称
	- **title**，`string`，报修标题
	- **description**，`string`，情况描述
	- **image**，`string`，图片URL，先传好图片再新建报修
	- **memo**，`string`，备注
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：新建维修任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task added"
		}
	或

		{
			status: "error",
			data: "device not exist"
		}

### 获取维修任务列表

- 请求地址：http://domain.com/app/maintain/list/2/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：获取到的维修任务列表，以数组形式返回
- json示例：

		{
			status: "ok",
			data: [
				{
					id: 18,
					title: "空调04进风管报修",
					device_name: "空调04",
					device_brief: "kt273311",
					creator: "张三",
					create_time: "2015-04-21 12:02:02",
					description: "进风管损坏，需更换",
					image: "http://domain.com/static/12.jpg",
					memo: "需携带配件",
					confirmed: false,
					note: ""
				},
				{
					id: 20,
					title: "空调04损坏",
					device_name: "空调04",
					device_brief: "kt999283",
					creator: "李四",
					create_time: "2015-05-04 21:06:01",
					description: "空调损坏，原因不明",
					image: "http://domain.com/static/30.jpg",
					memo: "",
					confirmed: true,
					note: "初步检修完毕，等待下一步继续维修"
				}
			]
		}
	或

		{
			status: "ok",
			data: []
		}

### 确认接受维修任务

- 请求地址：http://domain.com/app/maintain/confirm/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要接受的维修任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：确认维修任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task confirmed"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

### 更新维修进度

- 请求地址：http://domain.com/app/maintain/update/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要更新的维修任务id
	- **note**，`string`，更新的维修记录
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：更新维修进度是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task updated"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

### 完成维修任务

- 请求地址：http://domain.com/app/maintain/submit/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **maintain_id**，`int`，要提交的维修任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：提交维修任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "maintain task submitted"
		}
	或

		{
			status: "error",
			data: "maintain task not exist"
		}

## 意见反馈模块

### 提交反馈意见

- 请求地址：http://domain.com/app/feedback/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **feedback**，`string`，用户的反馈意见
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：提交反馈意见是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "feedback created"
		}
	或

		{
			status: "error",
			data: "user not exists"
		}

