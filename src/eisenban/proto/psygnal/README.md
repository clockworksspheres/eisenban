
Looking at the possibility of using psygnal in threading commands...

Not likely practical...

# is there any indication inside a python threading.Thread that a thread is complete?

Python Thread Completion Indication

In Python, a threading.Thread object does not inherently provide an indication that a thread is complete. However, you can check if a thread is still running using the is_alive() method. For example:

if my_thread.is_alive():
    print("Thread is still running")
else:
    print("Thread has completed")
 

This method returns True if the thread is still running and False if it has finished execution or was never started.

Additionally, you can use the join() method to wait for the thread to complete before continuing with the rest of your program. This method will block the calling thread until the thread whose join() method is called has finished execution.

For instance:

my_thread.start()
my_thread.join()  # Waits for the thread to complete
print("Thread has completed")
 

If you need to perform actions after the thread has completed, you can use the join() method to ensure that your program waits for the thread to finish before proceeding.

It's worth noting that if a thread is set as a daemon thread (using daemon=True), it will automatically terminate when the main program ends, and you do not need to explicitly manage its completion.

🌐
realpython.com
An Intro to Threading in Python – Real Python
🌐
stackoverflow.com
multithreading - Python: is thread still running - Stack Overflow
🌐
docs.python.org
threading — Thread-based parallelism
can you get line by line output in threading.thread

If you want to get line-by-line output from a thread in Python, you can use standard output (print statements) or a shared data structure like a queue to capture the output. Here are two common approaches:
1. Using Print Statements

You can simply use print statements within the thread to output line-by-line data. This is straightforward but may not be suitable for more complex or concurrent scenarios.

import threading
import time

def my_thread_function():
    for i in range(5):
        print(f"Line {i}")
        time.sleep(1)

# Create and start the thread
thread = threading.Thread(target=my_thread_function)
thread.start()

# Wait for the thread to complete
thread.join()
 

2. Using a Queue

A more robust approach is to use a queue.Queue to capture the output from the thread and then process it in the main thread. This ensures that the output is captured and can be handled in a controlled manner.

import threading
import time
import queue

def my_thread_function(output_queue):
    for i in range(5):
        output_queue.put(f"Line {i}")
        time.sleep(1)

# Create a queue to hold the output
output_queue = queue.Queue()

# Create and start the thread
thread = threading.Thread(target=my_thread_function, args=(output_queue,))
thread.start()

# Process the queue in the main thread
while thread.is_alive() or not output_queue.empty():
    try:
        line = output_queue.get(timeout=0.1)
        print(line)
    except queue.Empty:
        continue

# Wait for the thread to complete
thread.join()
 

Explanation:

    Using Print Statements:

        Simple and easy to implement.

        Output is directly printed to the console.

        Not suitable for complex or concurrent scenarios where you need to capture and process the output in a controlled manner.

    Using a Queue:

        More robust and suitable for complex scenarios.

        Captures the output in a queue, allowing you to process it in the main thread.

        Ensures that the output is handled in a controlled and thread-safe manner.

Choose the approach that best fits your needs based on the complexity and requirements of your application.
AI-generated answer. Please verify critical facts. 


# NOTES: 

 * possibly catching on RE expressions and signaling on those, 

 * or signaling on line by line -

 * or using queue's and signaling on stuff coming out of queue's... 

 * better to come out of the threading class itself I think...

 * slot can thread.join() for faster processing??

 * also can send signals to other classes with or without data or pointers to data that processing is complete... 

 -----


