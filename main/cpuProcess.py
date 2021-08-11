# !/usr/bin/env python3
""" Threads that waste CPU cycles """

import os
import threading


# a simple function that wastes CPU cycles forever
def cpu_waster():
    while True:
        pass


# display information about this process
print('n   Process ID: ', os.getpid())
print('Thread Count: ', threading.active_count())
for thread in threading.enumerate():
    print(thread)

for i in range(4):
    threading.Thread(target=cpu_waster).start()

# display information about this process
print('n  Process ID: ', os.getpid())
print('Thread Count: ', threading.active_count())
for thread in threading.enumerate():
    print(thread)