# 一个简单的数据库前后端项目

## 调试

* 安装 `pipenv` 和 `yarn` (包括最新版的 `nodejs`)
* cd 到 `./booom_db` 里面去
* 初次使用记得 `pipenv install` 安装虚拟环境
* `pipenv shell` 进入 `pipenv` 虚拟环境
* `./update_run.sh` 运行

## Dockerize

* Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
* Just execute `$ sudo docker-compose up` at the root directory of the project in the terminal.
* Enter `localhost://8080` in browser to explor the website.

> If you wanna fully rebuild the container, just type `$ sudo docker-compose up --build`

> BTW, `sudo` is optional.

## More infos to quickly start this prject

* Backend: [booom_db](./booom_db)
* Frontend: [db_frontend](./booom_db/db_frontend)

## 超级用户

> 用于管理其他用户

* 账号: admin
* 密码: admin666

## 测试用户

> 用于登录

* 账号: 17775110118
* 密码: 97294597

## 依赖

* Python 3.7
* Pipenv
* MongoDB
* yarn(optional)

## 感谢

* Django
* MongoDB
* mongoengine
* vue
* yarn
* vuetify
* filepone
* python & pipenv

## 运行本项目

```bash
$ ./start.sh
```

## 修改

如果做了修改, 请执行 booom\_db/update\_run.sh
