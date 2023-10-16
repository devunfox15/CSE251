import multiprocessing 
import multiprocessing.connection
import time

def sender(conn:multiprocessing.connection.Connection): 
    """ function to send messages to other end of pipe """
    conn.send('Hello')
    conn.send('World')
    print(f'sender Received: {conn.recv()}')
    print(f'sender Received: {conn.recv()}')
    time.sleep(7.5)
    conn.send('DONE')
    conn.close() 			# Close this connection when done

def receiver(conn:multiprocessing.connection.Connection): 
    """ function to print the messages received from other end of pipe  """
    # conn.send('Hello')
    # conn.send('World')
    print(f'reciever Received: {conn.recv()}')
    print(f'reciever Received: {conn.recv()}')
    while not conn.poll(5):
        print('waiting for more data')
    print(f'reciever Received: {conn.poll()}')
    time.sleep(.5)
    # print(f'reciever Received: {conn.poll()}')

if __name__ == "__main__": 

    # creating a pipe 
    parent_conn, child_conn = multiprocessing.Pipe() 

    # creating new processes 
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,)) 
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,)) 

    # running processes 
    p1.start() 
    p2.start() 

    # wait until processes finish 
    p1.join() 
    p2.join() 