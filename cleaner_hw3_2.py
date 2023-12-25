from multiprocessing import cpu_count, Pool, current_process
from time import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(num: int):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(i)
    logger.debug(f'In process {current_process()} factorizing {num}')
    return divisors


def factorize_parallel(nums: list[int]):
    with Pool(processes=num_cores) as pool:
        results = pool.map(factorize, nums)
        logger.debug(f'Results: {results}')
    return results


if __name__ == "__main__":
    list_numbers = [128, 255, 99999, 10651060]
    num_cores = cpu_count()
    print(f'{num_cores} cores')

    # Synchronous version
    sync_results = [factorize(num) for num in list_numbers]
    print("Synchronous results:", sync_results)

    # Parallel version
    start = time()
    parallel_results = factorize_parallel(list_numbers)
    finish = time()
    print("Parallel results:", parallel_results)

    assert parallel_results == sync_results

    print('Execution time: ', finish - start, ' sec')
