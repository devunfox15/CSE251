"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json
from cse251 import *

RETRIEVE_THREADS = 38
NO_MORE_VALUES = 'No more'

def retrieve_thread(q, log):
    """ Process values from the data_queue """
    while True:
        url = q.get()
        if url == NO_MORE_VALUES:
            break
        log.write(requests.get(url).json()['name'])

        pass


def file_reader(q, log):
    """ This thread reads the data file and places the values in the data_queue """
    with open("urls.txt", "r") as file:
        for line in file:
            q.put(line.strip())
    log.write('Finished reading file')
    for _ in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)

def main():
    log = Log(show_terminal=True)
    q = queue.Queue()
    
    # Create the threads
    file_t = threading.Thread(target=file_reader, args=(q, log))
    threads = [threading.Thread(target=retrieve_thread, args=(q, log)) for _ in range(RETRIEVE_THREADS)]

    log.start_timer()
    
    # Start the retrieve_threads first, then file_reader
    for t in threads:
        t.start()
    
    file_t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    file_t.join()

    log.stop_timer('Time to process all URLs')

if __name__ == '__main__':
    main()