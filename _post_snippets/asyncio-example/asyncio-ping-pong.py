import asyncio
import time

# msg = "ping"

# async def main():
#     # print('Hello ...')
#     # await asyncio.sleep(1)
#     # print('... World!')
#     for i in range(10):
#         await ping()
#         pong()

# async def ping():
#     asyncio.sleep(1)
#     print(msg)

# async def pong():
#     msg = "pong"
#     print(msg)
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(
        say_after(3, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

# Python 3.7+
asyncio.run(main())
