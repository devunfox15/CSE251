import time 
import threading


class ImportantStuff(threading.Thread):
    def _init_(self, num): # self is a way of saying this instance, you can add more parameters
       super()._init_() # must included
       self.num = num

    def run(self):
        print(f'I did my important work {self.num}')
        time.sleep(1)
        print(f'great sleeping {self.num}')



# def do_important_work(num:int, lock1:threading.Lock, lock2:threading.Lock):

#     lock1.acquire()
#     myList[0] = 10
#     print(f"this is really important work 1 {myList}")
#     time.sleep(1)
#     lock2.acquire()
#     print(f'I finished my important work {myList}')
#     lock1.release()
#     lock2.release()
    

# def do_important_work2(num:int, lock1:threading.Lock, lock2:threading.Lock):
#     lock2.acquire()
#     print(f'this is really important got lock 2')
#     myList[0] = 10
#     lock1.acquire()
#     print(f"this is really important work {myList}")
#     time.sleep(2)
#     print(f'I finished my important work {myList}')
#     lock2.release()
#     lock1.release()
    

myList = [1]
lock1 = threading.Lock()
lock2 = threading.Lock()


t1 = ImportantStuff(1, lock1)
t2 = ImportantStuff(2, lock2)

t1.start()
t2.start()
t1.join()
t2.join()