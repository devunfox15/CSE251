import time
import threading
import random

def my_thread_function(couch:threading.Semaphore):
    couch.acquire()
    time.sleep(.5)
    couch.release()
    print(f"{random.randint(0, 1000)}: Awake now")

def clock_tick(tick_pendulum:threading.Semaphore, tock_pendulum:threading.Semaphore):
    for _ in range(15):
        tock_pendulum.acquire()
        print("tick")
        time.sleep(.5)
        tick_pendulum.release()
    pass

def clock_tock(tick_pendulum:threading.Semaphore, tock_pendulum:threading.Semaphore):
    for _ in range(15):
        tick_pendulum.acquire()
        print("tock")
        time.sleep(.5)
        tock_pendulum.release()

    pass

def main():
    tick_pend = threading.Semaphore(0)
    tock_pend = threading.Semaphore(1)

    tick_thread = threading.Thread(target=clock_tick, args=(tick_pend, tock_pend))
    tock_thread = threading.Thread(target=clock_tock, args=(tick_pend, tock_pend))

    tick_thread.start()
    tock_thread.start()
    tick_thread.join()
    tock_thread.join()

    # couch = threading.Semaphore(3)
    # threads = [threading.Thread(target=my_thread_function, args=(couch,)) for _ in range(100)]
    # for t in threads:
    #     t.start()

    # for t in threads:
    #     t.join()
    
    pass



if __name__ == '__main__':
    main()


#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    def __init__(self, queue, semaphore, semaphore2, queue_stats):
        threading.Thread.__init__(self)
        self.queue = queue
        self.semaphore = semaphore
        self.semaphore2 = semaphore2  # Add a reference to the second semaphore
        self.queue_stats = queue_stats

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            car = Car()
            while self.queue.size() >= MAX_QUEUE_SIZE:
                pass  # Wait until the queue size is less than MAX_QUEUE_SIZE
            self.queue.put(car)
            self.semaphore2.release()
            # Collect queue size data
            self.update_queue_stats(self.queue, self.queue_stats)

    def update_queue_stats(self, queue, queue_stats):
        # This function is responsible for updating queue_stats
        size = queue.size()
        if size <= MAX_QUEUE_SIZE:
            queue_stats[size - 1] += 1  # Decrease by 1 to match index

class Dealer(threading.Thread):
    def __init__(self, queue, semaphore, semaphore2, queue_stats):
        threading.Thread.__init__(self)
        self.queue = queue
        self.semaphore = semaphore
        self.semaphore2 = semaphore2  # Add a reference to the second semaphore
        self.timeout = 1
        self.queue_stats = queue_stats

    def run(self):
        while True:
            if self.queue.size() > 0:
                car = self.queue.get()
                
                self.semaphore.release()
                # Simulate selling the car
                time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
                # Collect queue size data
                self.update_queue_stats(self.queue, self.queue_stats)
            else:
                time.sleep(self.timeout)  # Wait for a short period of time
                if not self.queue.size() > 0:
                    break

    def update_queue_stats(self, queue, queue_stats):
        # This function is responsible for updating queue_stats
        size = queue.size()
        if size <= MAX_QUEUE_SIZE:
            queue_stats[size - 1] += 1  # Decrease by 1 to match index
def main():
    log = Log(show_terminal=True)
    semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    semaphore2 = threading.Semaphore(MAX_QUEUE_SIZE)  # Define a second semaphore
    queue = Queue251()
    queue_stats = [0] * MAX_QUEUE_SIZE

    factory = Factory(queue, semaphore, semaphore2, queue_stats)  # Pass the second semaphore
    dealer = Dealer(queue, semaphore, semaphore2, queue_stats)   # Pass the second semaphore

    log.start_timer()

    factory.start()
    dealer.start()

    factory.join()
    dealer.join()

    log.stop_timer(f'All {CARS_TO_PRODUCE} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{CARS_TO_PRODUCE} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')

if __name__ == '__main__':
    main()