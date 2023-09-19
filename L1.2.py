import time
import threading

class ImportantStuff(threading.Thread):
    def __init__(self, num, lock):
        super().__init__()
        self.num:int = num
        self.lock:threading.Lock = lock

    def run(self):
        self.lock.acquire()
        print(f"I did my important work {self.num}")
        time.sleep(1)
        self.lock.release()
        print(f"Great sleeping {self.num}")



def do_important_work(myList, lock1:threading.Lock, lock2:threading.Lock):
    lock1.acquire()
    print(f"This is really important got lock 1{myList}")
    time.sleep(1)
    lock2.acquire()
    myList[0] = 10
    do_important_work(myList, lock1, lock2)
    lock1.release()
    lock2.release()
    print(f"I finished my important work {myList}")

def do_important_work2(myList, lock1:threading.Lock, lock2:threading.Lock):
    lock2.acquire()
    print(f"This is really important got lock 2{myList}")
    time.sleep(1)
    lock1.acquire()
    myList[0] = 10
    # time.sleep(2)
    lock2.release()
    lock1.release()
    print(f"I finished my important work {myList}")

myList = [1]
lock1 = threading.Lock()
lock2 = threading.Lock()

# lock1.acquire()
t1 = ImportantStuff(1, lock1)
t2 = ImportantStuff(2, lock1)
# t2 = threading.Thread(target=do_important_work, args=(myList, lock1, lock2))
t1.start()
t2.start()
t1.join()
t2.join()
