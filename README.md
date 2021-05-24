# aio-recurring
Recurring coroutines using asyncio

## Usage:

```python
import asyncio
from datetime import datetime

from aio_recurring.job import (
    recurring_job,
    run_recurring_jobs,
)


@recurring_job(every=5)
async def print_info_5():
    print(f"[{datetime.now()}] This coroutine is rescheduled every 5 seconds")


@recurring_job(every=10)
async def print_info_10():
    print(f"[{datetime.now()}] This coroutine is rescheduled every 10 seconds")


async def main():
    run_recurring_jobs()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

```