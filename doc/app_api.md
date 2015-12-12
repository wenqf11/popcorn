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

### 上传用户头像

- 请求地址：http://domain.com/app/avatar/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **avatar**，`file`，用户头像的图像文件
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：是否上传成功
- json示例：

		{
			status: "ok",
			data: "avatar upload success"
		}
	或

		{
			status: "error",
			data: "avatar upload failed"
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
				avatar: "/media/user_avatar/syb1001/2015-07-27-14-09-12_test.jpg",
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

### 修改用户信息

- 请求地址：http://domain.com/app/userinfo/submit/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **name**，`string`，昵称
	- **gender**，`int`，性别，0表示女，1表示男
	- **mobile**，`string`，手机号
	- **email**，`string`，电子邮件
	- **address**，`string`，地址
	- **zipcode**，`string`，邮编
	- **birthday**，`string`，生日
	- **id_card**，`string`，身份证号
	- **memo**，`string`，备注
	- **contact**，`string`，紧急联系人
	- **contact_mobile**，`string`，联系人手机号
	- timestamp，`int`，时间戳，暂时没有用
- 备注：以上请求参数均为可选项，如果不对某一项进行修改请不要传该项，若传空项视为删除该项的值
- 返回结果：是否修改成功
- json示例：

		{
			status: "ok",
			data: "user info modified"
		}
	或

		{
			status: "error",
			data: "operation failed"
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

### 抽奖

- 请求地址：http://domain.com/app/egg/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：`bonus`为本次抽奖的奖金，`probability`为中奖概率，`result`为是否中奖
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

### 抽奖信息查询
- 请求地址：http://domain.com/app/egg/time/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：`bonus`为本次抽奖的奖金，`probability`为中奖概率，`start_time`抽奖开始时间， `end_time` 抽奖结束时间
- json示例：

		{
			status: "ok",
			data: {
				bonus: 20.0,
				probability: 0.1,
				start_time: 2:00
				end_time: 4:00
			}
		}
	或

		{
			status: "error",
			data: "bonus config does not found"
		}

### 中奖历史信息查询

- 请求地址：http://domain.com/app/egg/info/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **date**，`string`，要查询的日期，如“2015-05-22”
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：`bonus`为当次中奖的奖金，`probability`为当日中奖概率，`state`为中奖状态，0表示没中，1表示中了未领取，2表示已经领取奖励
- json示例：

		{
			status: "ok",
			data: {
				bonus: 20.0,
				probability: 0.1,
				state: 1
			}
		}
	或

		{
			status: "error",
			data: "element not exists"
		}

### 获取部门层级信息

- 请求地址：http://domain.com/app/class/tree/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：数据库中的部门层级树
- json示例：

		{
			status: "ok",
			data: {
				depth: 3
				root: {
					class_id: 1,
					name: "网电盈科",
					type: "公司",
					children: [
						{
							class_id: 2,
							name: "微谷项目部",
							type: "项目部",
							children: [
								{
									class_id: 4,
									name: "空调班组1",
									type: "班组"
								},
								{
									class_id: 5,
									name: "空调班组2",
									type: "班组"
								}
							]
						},
						{
							class_id: 3,
							name: "某项目部",
							type: "项目部"
						}
					]
				}
			}
		}
	或

		{
			status: "error",
			data: "illegal db data" // 数据库中不存在parentid为0的根节点
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

### 获取所有设备全称和简称

- 请求地址：http://domain.com/app/device/brief/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：所有设备的简称brief以及简称所对应全称的字典
- json示例：

		{
			status: "ok",
			data: {
				brief: ["ks304921", "kt931121", "dj239932"],
				dict: {
						ks304921: "冷水机001",
						kt931121: "空调机002"
						dj239932： "冷柜11"
					}
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

### 获取某个部门下的设备并按照设备类型分类

- 请求地址：http://domain.com/app/device/class/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **class_id**，`string`，部门id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：该部门管辖的、按照设备类型分好类的设备集合
- json示例：

		{
			status: "ok",
			data: [
				{
					type: "空调",
					devices: [
						{brief: "kt088233", name: "空调233"},
						{brief: "kt032764", name: "空调764"}
					]
				},
				{
					type: "锅炉",
					devices: [
						{brief: "gl387712", name: "锅炉12"}
					]
				}
			]
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
					end_time: "17:00",	    // 路线结束巡视时间
					interval: 2,			// 巡视周期（小时）
					checked: 1				// 是否巡视完毕（未实现）
				},
				{
					id: 1,
					name: "线路二",
					start_time: "08:00",
					end_time: "17:00",	  
					interval: 2,
					checked: 0
				},
				{
					id: 2,
					name: "线路三",
					start_time: "10:00",
					end_time: "17:00",	 
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
					name: "螺杆式风冷冷水机组",
					brief: "kt094732",
					content: [
						"冷供水温度  ℃": {
					        type": "integer",
					        id": 0,
					        default: "",
					        priority: "0",
					        hint:"正常值范围在7-12"
				    	},
				    	"冷供水压力  Mpa": {
					        type: "integer",
					        id: "1",
					        "default": "",
					        "priority": "1"
					    },
					]
				},
				{
					id: 32,
					name: "冷冻水泵",
					brief: "ms383831",
					content: [
						"水位": {
					        type: "integer",
					        id: "4",
					        default: "0",
					        priority: "4",
					        options: {
					            0: "偏高",
					            1: "中等",
					            2: "偏低"
					        }
					    }
					]
				}
			]
		}

### 提交抄表数据

- 请求地址：http://domain.com/app/meter/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **route_id**，`int`，抄表路线id，获取此路线上的所有设备
	- **brief**，`string`，设备简称
	- **content**，`string`，json格式的抄表数据
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：是否提交成功
- json示例：

		{
			status: "ok",
			data: "meter data submittid"
		}
	或

		{
			status: "error",
			data: "route not exists"
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
					assignor: "张三",
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
					assignor: "王五",
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
	- **image**， `File`， 图片
	- **description**，`string`，情况描述
	- **memo**，`string`，备注
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：新建维修任务是否成功，成功返回维修任务id（用于图片上传），失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: 12
		}
	或

		{
			status: "error",
			data: "device not exist"
		}

### 上传报修图像

- 请求地址：http://domain.com/app/maintain/image/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **id**，`int`，所要上传图片的维修任务id，新建维修任务时返回此id
	- **image**，`file`，报修图像文件
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：是否上传成功
- json示例：

		{
			status: "ok",
			data: "image upload success"
		}
	或

		{
			status: "error",
			data: "image upload failed"
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
					image: "http://domain.com/static/12.jpg", // 若未上传图片则为空字符串
					memo: "需携带配件",
					confirmed: false,
					note: ""
				},
				{
					id: 20,
					title: "空调04损坏",
					device_name: "无相关设备",
					device_brief: "无相关设备",
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


### 获取我的维修记录

- 请求地址：http://domain.com/app/maintain/record/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **start_date**，`string`，要查询的开始日期，如“2015-05-22”
	- **end_date**，`string`，要查询的结束日期，如“2015-12-12”
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：根据edit_datetime的起始和结束（包含起始和结束日期），也就是维修提交的时间来获取到的维修记录列表，以数组形式返回
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
					image: "http://domain.com/static/12.jpg", // 若未上传图片则为空字符串
					memo: "需携带配件",
					editor: "王五",
					edit_datime: "2015-05-22 12:02:02",
					is_audit: false,                      //是否审核确认
					note: "更换了进风管，修好了"
				},
				{
					id: 20,
					title: "空调04损坏",
					device_name: "无相关设备",
					device_brief: "无相关设备",
					creator: "李四",
					create_time: "2015-05-04 21:06:01",
					description: "空调损坏，原因不明",
					image: "http://domain.com/static/30.jpg",
					memo: "",
					editor: "李四",
					edit_datime: "2015-05-21 12:02:02",
					is_audit: true,						 //是否审核确认
					note: "初步检修完毕，等待下一步继续维修"
				}
			]
		}
	或

		{
			status: "ok",
			data: []
		}



## 任务模块

### 获取子任务列表

- 请求地址：http://domain.com/app/task/list/
- 请求方式：GET
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：获取到的子任务列表，以数组形式返回
- json示例：

		{
			status: "ok",
			data: [
				{
					id: 18,
					title: "子任务05",
					description: "子任务描述",
					super_title: "任务01",
					super_description: "任务描述",
					creator: "张三",
					create_time: "2015-04-21 12:02:02",
					memo: "需携带配件",
					confirmed: false,
					note: ""
				},
				{
					id: 20,
					title: "子任务01",
					description: "子任务描述",
					super_title: "任务03",
					super_description: "任务描述",
					creator: "李四",
					create_time: "2015-05-04 21:06:01",
					memo: "",
					confirmed: true,
					note: "初步进行完毕"
				}
			]
		}
	或

		{
			status: "ok",
			data: []
		}

### 确认接受子任务

- 请求地址：http://domain.com/app/task/confirm/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **task_id**，`int`，要接受的子任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：确认子任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "task confirmed"
		}
	或

		{
			status: "error",
			data: "taskitem not exist"
		}

### 更新子任务进度

- 请求地址：http://domain.com/app/task/update/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **task_id**，`int`，要更新的子任务id
	- **note**，`string`，更新的子任务记录
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：更新子任务进度是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "taskitem updated"
		}
	或

		{
			status: "error",
			data: "taskitem not exist"
		}

### 完成子任务

- 请求地址：http://domain.com/app/task/submit/
- 请求方式：POST
- 请求参数：
	- username，`string`，用户名
	- access_token，`string`，用户认证用的token
	- **task_id**，`int`，要提交的子任务id
	- timestamp，`int`，时间戳，暂时没有用
- 返回结果：提交子任务是否成功，失败则返回失败原因
- json示例：

		{
			status: "ok",
			data: "taskitem submitted"
		}
	或

		{
			status: "error",
			data: "taskitem not exist"
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

