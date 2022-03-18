import os
import time


# start a timer
start = time.time()


# run the file with input
os.system("./a.out")


# how do we do command line input?
os.system("3")

# end timer
end = time.time()

# print the difference
print(str(end - start))