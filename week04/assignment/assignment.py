import time
import threading
import random
from datetime import datetime
from cse251 import *

# Global Constants - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50


class Car:
    def __init__(self):
        self.make = random.choice(['Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda'])
        self.model = random.choice(['A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round', 'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger', 'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX'])
        self.year = random.choice(range(1990, datetime.now().year))
        time.sleep(random.random() / SLEEP_REDUCE_FACTOR)

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')

class Queue251:
    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= MAX_QUEUE_SIZE
        self.items.append(item)

    def get(self):
        return self.items.pop(0)

class Factory(threading.Thread):
    def __init__(self, car_queue, dealer_semaphore, queue_lock):
        super().__init__()
        self.car_queue = car_queue
        self.dealer_semaphore = dealer_semaphore
        self.queue_lock = queue_lock

    def run(self):
        for i in range(CARS_TO_PRODUCE):
            car = Car()
            self.queue_lock.acquire()
            if len(self.car_queue.items) < MAX_QUEUE_SIZE:
                self.car_queue.put(car)
                self.dealer_semaphore.release()
            self.queue_lock.release()

class Dealer(threading.Thread):
    def __init__(self, car_queue, dealer_semaphore, queue_lock, queue_stats):
        super().__init__()
        self.car_queue = car_queue
        self.dealer_semaphore = dealer_semaphore
        self.queue_lock = queue_lock
        self.queue_stats = queue_stats

    def run(self):
        while True:
            self.dealer_semaphore.acquire()
            self.queue_lock.acquire()
            if len(self.car_queue.items) > 0:
                car = self.car_queue.get()
                self.queue_stats[len(self.car_queue.items)] += 1
            self.queue_lock.release()
            time.sleep(random.random() / SLEEP_REDUCE_FACTOR)

def main():
    log = Log(show_terminal=True)

    car_queue = Queue251()
    dealer_semaphore = threading.Semaphore(0)
    queue_lock = threading.Lock()
    queue_stats = [0] * MAX_QUEUE_SIZE

    factory = Factory(car_queue, dealer_semaphore, queue_lock)
    dealer = Dealer(car_queue, dealer_semaphore, queue_lock, queue_stats)

    log.start_timer()

    factory.start()
    dealer.start()

    factory.join()
    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')

if __name__ == '__main__':
    main()