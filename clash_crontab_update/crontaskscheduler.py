import functools
from typing import Dict, Any, Callable
from pytz import timezone
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyproxypattern import Proxy
locale = timezone('Asia/Shanghai')


class CronTaskScheduler(Proxy):
    @classmethod
    def create(clz, scheduler_type: str = "background", gconfig: Dict[str, Any] = {}, **options: Any) -> "CronTaskScheduler":
        """初始化."""
        schedulers = {
            "background": BackgroundScheduler,
            "blocking": BlockingScheduler,
            "aio": AsyncIOScheduler
        }
        return CronTaskScheduler(schedulers.get(scheduler_type, BackgroundScheduler)(gconfig=gconfig, **options))

    def _instance_check(self, instance: Any) -> bool:
        return isinstance(instance, BaseScheduler)

    def regist_job(self, ct: CronTrigger) -> Callable[[Callable[[], None]], Callable[[], None]]:
        def decorate(func: Callable[[], None]) -> Callable[[], None]:
            @functools.wraps(func)
            def warp() -> None:
                if self.instance:
                    self.instance.add_job(func, ct)
                else:
                    self._callbacks.append(lambda instance: instance.add_job(func, ct))
                return func()
            return warp
        return decorate
