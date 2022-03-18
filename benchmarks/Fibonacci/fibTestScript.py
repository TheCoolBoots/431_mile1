import os
import time

passes = 30
funInput = 38

i = 0
sum = 0
while i < passes:
    # start a timer
    start = time.time()

    # run the file with input
    os.system("echo " + str(funInput) + " | ./a.out")

    # end timer
    end = time.time()

    # add to overall time sum
    sum += (end - start)
    i += 1


# print the average time => time sum / # of passes
print("average runtime: " + str(sum / passes))