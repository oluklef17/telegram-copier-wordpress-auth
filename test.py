from queue import Queue

my_queue = Queue()

# Enqueue elements
my_queue.put(1)
my_queue.put(2)
my_queue.put(3)

# Dequeue elements
while not my_queue.empty():
    element = my_queue.get()
    print(f"Dequeued: {element}")
