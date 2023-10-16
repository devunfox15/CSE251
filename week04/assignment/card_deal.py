import time
import threading
import random


def friend(give_out_cards:threading.Semaphore, i_need_cards_sem:threading.Semaphore):
    for _ in range(15):
        give_out_cards.acquire()
        print("tick")
        time.sleep(.5)
        i_need_cards_sem.release()
        pass

def cards(give_out_cards:threading.Semaphore, i_need_cards_sem:threading.Semaphore):
    for _ in range(15):
        give_out_cards.acquire()
        print("tick")
        time.sleep(.5)
        i_need_cards_sem.release()
        pass

def main():
    give_out_cards = threading.Semaphore(0)
    i_need_cards_sem = threading.Semaphore(1)

    friend_thread = threading.Thread(target=clock_tick, args=(tick_pend, tock_pend))
    me_thread = threading.Thread(target=clock_tock, args=(tick_pend, tock_pend))

    tick_thread.start()
    tock_thread.start()
    tick_thread.join()
    tock_thread.join()

    
    pass



if __name__ == '__main__':
    main()
