"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists
import queue



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(filename: str, q: mp.Queue):
    with open(filename, "r") as file:
        for line in file:
            q.put(int(line.strip()))
    q.put("Finish")
    

# TODO create prime_process function
def prime_processes(q:mp.Queue, primes:list):
    while True:
        value = q.get()
        if value == "Finish":
            q.put("Finish")
            break
        if is_prime(value):
            primes.append(value)


def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')

def main():
    """Main function"""
    filename = 'data.txt'
    create_data_txt(filename)
    q = mp.Queue()
    log = Log(show_terminal=True)
    log.start_timer()

    # Create shared data structures
    primes = mp.Manager().list()

    # Create reading thread
    r_thread = threading.Thread(target=read_thread, args=(filename, q))

    # Create prime processes
    prime_process = [mp.Process(target=prime_processes, args=(q, primes)) for _ in range(PRIME_PROCESS_COUNT)]

    # Start them all
    r_thread.start()
    for p in prime_process:
        p.start()

    # Wait for them to complete
    r_thread.join()
    for p in prime_process:
        p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # Display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)

if __name__ == '__main__':
    main()
