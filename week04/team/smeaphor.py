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
