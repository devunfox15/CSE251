"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: <Your name>

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
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

        # Display the car that has was just created in the terminal
        # self.display()  # you may want to remove to debug
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    def __init__(self, barrier, car_queue, sem_factory, sem_dealer, dealer_stats, factory_id, dealer_count, factory_stats):
        super().__init__()
        self.car_queue = car_queue
        self.barrier = barrier
        self.sem_factory = sem_factory
        self.sem_dealer = sem_dealer
        self.dealer_stats = dealer_stats
        self.factory_id = factory_id
        self.dealer_count = dealer_count
        self.factory_stats = factory_stats
        self.cars_to_produce = random.randint(200, 300)

    def run(self):
        for _ in range(self.cars_to_produce):
            self.sem_factory.acquire()
            car = Car()
            self.car_queue.put(car)
            self.sem_dealer.release()
        i = self.barrier.wait()
        if i == 0:  
            for i in range(self.dealer_count):
                self.sem_dealer.release()
                self.car_queue.put("finished")

class Dealer(threading.Thread):
    def __init__(self, car_queue, sem_factory, sem_dealer, dealer_stats, dealer_index, total_cars):
        super().__init__()
        
        self.car_queue = car_queue
        self.sem_factory = sem_factory
        self.sem_dealer = sem_dealer
        self.dealer_stats = dealer_stats
        self.dealer_index = dealer_index
        self.total_cars = total_cars

    def run(self):
    
        while True:
            self.sem_dealer.acquire()
            car = self.car_queue.get()
            if car == "finished":
                break
            self.dealer_stats[self.dealer_index] += 1
            self.sem_factory.release()
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # Create semaphore(s) if needed
    sem_factory = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_dealer = threading.Semaphore(0)
    
    # Create queue
    car_queue = Queue251()
    
    # Create lock(s) if needed
    lock = threading.Lock()
    
    # Create barrier
    barrier = threading.Barrier(factory_count)

    # This is used to track the number of cars received by each dealer
    dealer_stats = list([0] * dealer_count)
    factory_stats = list([0]* factory_count)
    total_cars = 0  # Initialize the total number of cars
    
    total_cars_per_factory = []

    # Create your factories and dealerships
    
    factories = []  # Initialize an empty list for factory threads
    for factory_id in range(factory_count):
        factory = Factory(barrier, car_queue, sem_factory, sem_dealer, dealer_stats, factory_id, dealer_count, factory_stats)
        factories.append(factory)


    for cars in total_cars_per_factory:
        total_cars += cars

    dealers = [Dealer(car_queue, sem_factory, sem_dealer, dealer_stats, i, total_cars) for i in range(dealer_count)]

    log.start_timer()

    # Start all factories
    for factory in factories:
        factory.start()

    # Start all dealerships
    for dealer in dealers:
        dealer.start()

    # Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()

    for dealer in dealers:
        dealer.join()

      

    max_queue_size = car_queue.get_max_size()  # Get the max queue size

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    # collect this information after the factories are finished.
    factory_stats = [factory.cars_to_produce for factory in factories]
    
    return run_time, max_queue_size, dealer_stats, factory_stats  # Return the values


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)