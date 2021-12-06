from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from asyncio.tasks import ALL_COMPLETED
from utility import changeIP

def f(i, res, executor, second_futures):
    print(f"Processing {i}")
    res.append(i)
    if i == 5:
        changeIP()

    return res, i

futures = []
second_futures = []

def done_callback(future):
    res, i = future.result()
    print(f"Callback prcessing {i}")
    if i % 2 == 0:
        res.append(i * 100)

res = []
with ThreadPoolExecutor() as executor:
    for i in range(10):
        futures.append(
            executor.submit(f, i, res, executor, second_futures)
        )
        futures[-1].add_done_callback(done_callback)

# r = as_completed(futures)

print(res)