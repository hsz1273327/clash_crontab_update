import os
from pathlib import Path
from functools import partial
from apscheduler.triggers.cron import CronTrigger
from schema_entry import EntryPoint
from pyloggerhelper import log
from crontaskscheduler import CronTaskScheduler
from tasks import update_nodes


class Application(EntryPoint):
    _name = "clash_crontab_update"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["clash_url"],
        "properties": {
            "app_version": {
                "type": "string",
                "title": "v",
                "description": "应用版本",
                "default": "0.0.0"
            },
            "app_name": {
                "type": "string",
                "title": "n",
                "description": "应用名",
                "default": "clash_crontab_update"
            },
            "log_level": {
                "type": "string",
                "title": "l",
                "description": "log等级",
                "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                "default": "DEBUG"
            },
            "update_period": {
                "type": "string",
                "description": "定时更新的间隔,使用crontab的格式,默认每天凌晨4点执行",
                "default": "0 4 * * *"
            },
            "clash_config_path": {
                "type": "string",
                "description": "待更新clash配置的位置",
                "default": "/config.yml"
            },
            "clash_url": {
                "type": "string",
                "description": "节点数据的url",
            },
            "clash_config_init": {
                "type": "boolean",
                "description": "是否在程序启动时初始化设置",
                "default": False
            }
        }
    }

    def do_main(self) -> None:
        log.initialize_for_app(
            app_name=self.config.get("app_name"),
            log_level=self.config.get("log_level")
        )
        log.info("获取任务配置", config=self.config)
        scheduler = CronTaskScheduler.create("blocking", logger=log)
        config_path = Path(self.config["clash_config_path"])
        clash_url = self.config["clash_url"]
        task = partial(update_nodes, config_path, clash_url)
        if self.config.get("clash_config_init"):
            task()
        scheduler.add_job(task, CronTrigger.from_crontab(self.config["update_period"]))
        log.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            log.info('crontab task stoped')
        except Exception as e:
            log.error("crontab task get error", err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
