from asyncio import get_running_loop
from dataclasses import dataclass
from typing import Callable, Coroutine


@dataclass(eq=True, frozen=True)
class Job:
    func: Callable[..., Coroutine]
    delay: int


class Scheduler:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Scheduler, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self._jobs = set()

    def add_job(self, job: Job):
        self._jobs.add(job)

    def _run_job(self, func, delay, *args):
        current_loop = get_running_loop()
        current_loop.create_task(func(*args))
        current_loop.call_later(delay, self._run_job, func, delay, *args)

    def _run_all_jobs(self):
        for job in self._jobs:
            self._run_job(func=job.func, delay=job.delay)

    def run_jobs(self):
        loop = get_running_loop()
        loop.call_soon(self._run_all_jobs)


scheduler = Scheduler()


def recurring(every: int):
    """
    Decorate a coro function to call it every N seconds.

    :param every: number of seconds after which a task will be repeated
    """

    def decorated(func):

        new_job = Job(func=func, delay=every)

        scheduler.add_job(job=new_job)

        async def wrapper(*args):

            return await func(*args)

        return wrapper

    return decorated


def run_recurring_jobs():
    scheduler.run_jobs()


