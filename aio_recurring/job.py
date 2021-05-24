import asyncio
from asyncio import get_running_loop
from datetime import datetime


def reschedule_job(func, delay, *args):
    current_loop = get_running_loop()
    current_loop.create_task(func(*args,))
    current_loop.call_later(delay, reschedule_job, func, delay, *args)


jobs = dict()


def schedule_all_jobs():
    for _, value in jobs.items():
        reschedule_job(value['func'], delay=value['delay'])


def recurring_job(every: int):

    def decorated(func):

        jobs[func.__name__] = {
            'func': func,
            'delay': every,

        }

        async def wrapper(*args):

            return await func(*args)

        return wrapper

    return decorated


def run_recurring_jobs():
    loop = get_running_loop()
    loop.call_soon(schedule_all_jobs)


async def main():
    run_recurring_jobs()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()


@recurring_job(every=1)
async def print_hello():
    print("HELo!: ")
    print(datetime.now())
    print('\n')