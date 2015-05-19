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

## 考勤模块

### 获取上下班数据
### 更新上下班数据

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
	- timestamp，`int`，时间戳，暂时没有用
	- **route_id**，`int`，要查询的路线id，获取此路线上的所有设备
- 返回结果：指定id路线上的所有设备信息（包括json格式的抄表表单）
- json示例：

		{
			status: "OK",
			data: [
				{
					id: 12,
					name: "kt094732",
					content: "{data: 1}"
				},
				{
					id: 32,
					name: "ms383831",
					content: "{data: 1}"
				}
			]
		}

## 维修模块

### 获取维修任务列表
### 更新维修结果
### 新建维修任务

## 保养模块

### 获取保养任务列表
### 更新保养计划

