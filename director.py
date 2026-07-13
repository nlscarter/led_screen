#!/usr/bin/env python3

import os
import time

# Clear the terminal
os.system("clear")

print("###################")
print("#                 #")
print("#   Hello World   #")
print("#                 #")
print("###################")

# Keep the program running so the console stays visible
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass