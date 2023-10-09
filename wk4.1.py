import threading, queue

def thread_function(q):
    item = q.get()
    print(f'Thread: {item}')

def main():
	q = queue.Queue()

	q.put('one')
	q.put('two')
	q.put('three')

	# Create 3 threads - This is a list comprehension
	# Pass the queue as an argument to the threads
	threads = [threading.Thread(target=thread_function, args=(q, )) for _ in range(3)]

	# start all threads
	for i in range(3):
		threads[i].start()

	# Wait for them to finish
	for i in range(3):
		threads[i].join()

	print('All work completed')

if __name__ == '__main__':
	main()