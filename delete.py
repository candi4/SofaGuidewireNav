from threading import *

import time

import random

import queue

 

def producer(q):

    while True:

        item = random.randint(1, 25)

        print("Producer Producting Item: ", item)

        q.put(item)

        print("Producer Notification")
        time.sleep(0.5)


    

def consumer(q):

    while True:

        print("Consumer waiting ")

        print("Consumer consumed the item:", q.get())


    

q = queue.Queue()

t1 = Thread(target = consumer, args = (q,), daemon=True)

t1.start()

while True:

    item = random.randint(1, 25)

    print("Producer Producting Item: ", item)

    q.put(item)

    print("Producer Notification")
    time.sleep(0.5)

t2.start()

time.sleep(100)