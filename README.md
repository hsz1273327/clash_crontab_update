# clash_crontab_update

定时更新clash节点的程序.

## 默认行为

这个镜像会在每次定时任务启动时读取指定文件,以下这些字段如果文件中本身没有设置则会填入默认值

| 字段                  | 默认值       |
| --------------------- | ------------ |
| `mixed-port`          | 7890         |
| `redir-port`          | 7892         |
| `allow-lan`           | true         |
| `mode`                | Rule         |
| `log-level`           | silent       |
| `external-controller` | 0.0.0.0:9090 |
| `secret`              | ''           |

## 参数

可以通过环境变量设置参数

| 环境变量                                 | 用途                                                            | 是否必须 | 默认值        |
| ---------------------------------------- | --------------------------------------------------------------- | -------- | ------------- |
| `CLASH_CRONTAB_UPDATE_CLASH_URL`         | 指定梯子给的节点更新URL                                         | 是       | ---           |
| `CLASH_CRONTAB_UPDATE_CLASH_CONFIG_INIT` | 指定是否在程序启动时初始化配置文件,如果你已经有配置了就不用设置 | 否       | 否            |
| `CLASH_CRONTAB_UPDATE_CLASH_CONFIG_PATH` | 指定待更新节点的配置文件路径                                    | 否       | `/config.yml` |
| `CLASH_CRONTAB_UPDATE_UPDATE_PERIOD`     | 指定定时任务的执行时间,crontab语法                              | 否       | `0 4 * * *`   |

## 使用方式

参考如下`docker-compose`:

```yml
version: '2.4'
x-log: &default-log
    options:
        max-size: "10m"
        max-file: "3"
services:
    clash:
        image: dreamacro/clash:v1.18.0
        restart: unless-stopped
        mem_limit: 512m
        logging:
            <<: *default-log
        volumes:
            - /volume1/software/docker_deploy/clash/config.yaml:/root/.config/clash/config.yaml
        network_mode: "host"
        depends_on:
            - updater
    ui:
        image: haishanh/yacd:v0.3.8
        restart: unless-stopped
        logging:
            <<: *default-log
        environment:
            YACD_DEFAULT_BACKEND: http://<群晖机器的地址>:9090
        ports:
            - "9080:80"
        depends_on:
            - clash
    updater:
        image: hsz1273327/clash_crontab_update
        restart: unless-stopped
        logging:
            <<: *default-log
        environment:
            CLASH_CRONTAB_UPDATE_CLASH_URL: <梯子给的url>
            CLASH_CRONTAB_UPDATE_CLASH_CONFIG_INIT: True
        volumes:
            - <配置文件位置>:/config.yml
```