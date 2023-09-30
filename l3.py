import os
import time
import multiprocessing as mp

def func(name):
    time.sleep(0.5)
    print(f'{name}, {os.getpid()}')

if __name__ == '__main__':

    names = ['John', 'Mary', 'April', 'Murry', 'George','John', 'Mary', 'April', 'Murry', 'George',
             'John', 'Mary', 'April', 'Murry', 'George','John', 'Mary', 'April', 'Murry', 'George',
             'John', 'Mary', 'April', 'Murry', 'George','John', 'Mary', 'April', 'Murry', 'George']

    # Create a pool of 2 processes
    with mp.Pool(8) as p: #the variable 8 changes the amout of threads that you want to do. 
        # map those 2 process to the function func()
        # Python will call the function func() alternating items in the names list.
        # the two processes will run in parallel
        p.map(func, names)