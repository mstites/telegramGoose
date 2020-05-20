import logging
import threading
import time
import time

def thread1():
    for i in range(1000):
        logging.info("1")
        time.sleep(1)

def thread2():
    for i in range(1000):
        logging.info("2")
        time.sleep(1)

def thread_function(name):
    while True:
        logging.info("Thread %s: starting", name)
        time.sleep(2)
        logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main    : create and start thread 1")
    t1 = threading.Thread(target=thread_function, args=(1,))
    t1.start()
    logging.info("Main    : create and start thread 2")
    t2 = threading.Thread(target=thread_function, args=(2,))
    t2.start()
    # threads = list()
    # for index in range(3):
    #     logging.info("Main    : create and start thread %d.", index)
    #     x = threading.Thread(target=thread_function, args=(index,))
    #     threads.append(x)
    #     x.start()
    #
    # for index, thread in enumerate(threads):
    #     logging.info("Main    : before joining thread %d.", index)
    #     thread.join()
    #     logging.info("Main    : thread %d done", index)
