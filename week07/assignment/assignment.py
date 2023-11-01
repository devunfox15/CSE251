"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Devun Durst>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

After Careful consideration I uses 10 pools because overall on my pc 
it had the fastest speed of completeing all of the 4034 task
then any other amounts of pools on my computer. 


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    global result_primes
    result = is_prime(value)
    if result == True:
       return ( f'{value} is prime')
    else:
       return (f'{value} is not prime')

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    global result_words
    found = False
    with open('words.txt','r') as file:
        for line in file:
            if word in line:
                found = True
                break
    if found: 
        return(f'{word} Found')
    else:
        return(f'{word} not found *****')

def task_upper(text:str):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    global result_upper
    uppercase = text.upper()
    return (f'{text} ==> {uppercase}')

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    global result_sums
    
    total = sum(range(start_value, end_value + 1))
    return (f'sum of {start_value:,} to {end_value:,} = {total:,}')
def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    global result_names
    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()
        name = data.get("name","Name not found")
        return (f'{url} has name {name}')
    else:
        return (f'{url} had an error receiving the information')


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool = mp.Pool(10)  # five pools
    # pool_primes = mp.Pool(5)
    # pool_words = mp.Pool(5)
    # pool_upper = mp.Pool(5)
    # pool_sums = mp.Pool(5)
    # pool_name = mp.Pool(17)


    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
       # Define callback functions for each task type
        def callback_prime(result):
            result_primes.append(result)
        
        def callback_word(result):
            result_words.append(result)
        
        def callback_upper(result):
            result_upper.append(result)
        
        def callback_sum(result):
            result_sums.append(result)
        
        def callback_name(result):
            result_names.append(result)
        
        if task_type == TYPE_PRIME:
            pool.apply_async(task_prime, args=(task['value'],), callback=callback_prime)
        elif task_type == TYPE_WORD:
            pool.apply_async(task_word, args=(task['word'],), callback=callback_word)
        elif task_type == TYPE_UPPER:
            pool.apply_async(task_upper, args=(task['text'],), callback=callback_upper)
        elif task_type == TYPE_SUM:
            pool.apply_async(task_sum, args=(task['start'], task['end']), callback=callback_sum)
        elif task_type == TYPE_NAME:
            pool.apply_async(task_name, args=(task['url'],), callback=callback_name)

    # Close the pool to signal that no more tasks will be added
    pool.close()

    # Wait for all tasks to complete
    pool.join()



    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
