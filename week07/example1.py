# Example using pool apply_asyc()

import multiprocessing as mp 

from cse251 import *

def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    return total
    
if __name__ == "__main__":
    log = Log(filename_log='apply_async.log', show_terminal=True)
    log.start_timer()
    pool = mp.Pool(4)
    print("creative pool")
    results = [pool.apply_async(sum_all_values, args=(x,)) for x in range(10000, 10000 + 10)]
    print("results are created and everything is lanched")
    # do something else

    # collect all of the results into a list
    output = [p.get() for p in results]
    log.stop_timer('Finished: ')
    print(output)
