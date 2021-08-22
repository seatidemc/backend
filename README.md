# backend

简体中文 | [English](./README.en.md)

这是 SEATiDE RESTful API 的后端部分，主要用于简化与阿里云 ECS 的相关交互，例如创建、开启、删除实例等，同时也用来拓展 SEATiDE 的相关 API 平台，比如提供用户注册和认证服务，同时存储用户数据（比如等级、MC 用户名）等用于将来可能的项目。

## 已完成的实现

### 阿里云 ECS 控制

使用阿里云 RAM 账户生成的 AccessKeyId 和 AccessKeySecret 来操控 ECS，所有的操作都会被写入数据库。所有对 `action` 接口的 *POST* 请求都需要一个管理员的登录凭证。

- *POST* `/api/ecs/v1/action` 使用 `type` 参数来指定操作类型
  - `delete` — 强制删除当前实例，不保存任何数据
  - `new` — 创建一个新的实例，然后分配 IP，然后启动它
  - `start` — 启动一个实例
  - `stop` — 停止一个实例
- *GET* `/api/ecs/v1/describe/:name`
  - `available` — 查看指定类型（在 `config.yml` 中配置）的 ECS 是否有库存
  - `instance` — 获取当前配置中的 ECS 的详细信息
  - `status` — 获取当前已创建的 ECS 的状态信息
  - `price` — 获取当前配置中的 ECS 的每小时估价（首小时）
  - `last-invoke` — （仅当 `deploy` 设置为 `true` 时）获取最近一次指令的执行结果

如果在 `config.yml` 中将 `deploy` 设定为 `true`，那么在实例被创建并启动以后，会自动执行位于 `src` 目录下的 `run.sh`，请确保此时该文件存在。**注：**在 `run.sh` 中不能使用 `~` 来代替 home 路径，否则会导致错误。

### 用户系统

对用户信息的增删改查，使用 `type` 参数来指定操作类型。所有对 `action` 接口的 *POST* 请求都需要一个管理员的登录凭证。

- *POST* `/api/user/v1/action`
  - `create` — 创建一个新的用户，必填三个参数：`username` 用户名、`password` 密码明文、`email` 电子邮箱
  - `get` — 获取某一用户的信息，不包括密码
  - `delete` — 删除某一用户
  - `alter` — 更改某用户的信息，使用**键—值**对来表示要更改的信息，不支持密码
  - `changepasswd` — 更改某用户的密码
- *POST* `/api/user/v1/auth`
  - `auth` — 使用用户名和密码获取一个 7 天有效期的登录凭证（token）
  - `check` — 检查登录凭证是否有效，失效或者过期

**注意：**必须在 `config.yml` 中的 `secret` 项填入一个随机的字符串才能正常生成 token。

## 部署

**需要 Python 3.8 以上版本和 MySQL 数据库**，低于 3.8（不包括）则无法运行。

1. 下载本项目

```sh
git clone https://github.com/seatidemc/backend.git
```

2. (*建议，选择性*) 创建虚拟环境

```sh
cd backend
python -m venv .
```

3. 安装依赖

```sh
pip install ./requirements.txt
cd src
unzip ./localdep.zip # 修改过的阿里云 ECS SDK
```

4. 初始化数据库。直接将 `.sql` 文件里的内容复制到 MySQL 窗口中执行即可。如果有任何问题发生，请先解决，不要继续。
5. 把 `config.example.yml` 重命名为 `config.yml`，然后修改内容。**请确保填写所有 `required` 项目。**

```sh
mv config.example.yml config.yml
vim config.yml
```

6. (*选择性*) 利用 `python` 来启动 API。可以在 `config.yml` 里面设置是否为 `production`（生产模式），如果是则会调用 `waitress` 在 `8080` 端口打开一个生产模式服务器，如果不是则会调用 `flask` 自身在 `5000` 端口打开一个测试服务器。

```sh
python ./app.py
```
