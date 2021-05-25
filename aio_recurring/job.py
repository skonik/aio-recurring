from asyncio import get_running_loop


def reschedule_job(func, delay, *args):
    current_loop = get_running_loop()
    current_loop.create_task(func(*args,))
    current_loop.call_later(delay, reschedule_job, func, delay, *args)


jobs = dict()


def schedule_all_jobs():
    for _, value in jobs.items():
        reschedule_job(value['func'], delay=value['delay'])


def recurring(every: int):
    """
    Decorate a coro function to call it every N seconds.

    :param every: number of seconds after which a task will be repeated
    """

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
