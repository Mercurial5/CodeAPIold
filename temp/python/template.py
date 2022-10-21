import sys, os

exit = 1
quit = 1
os._exit = 1
sys.exit = 1
i = 0
for _ in range(%s):

    %s

    print('TestCase')
    i += 1
    if i == 0:
        1 / 0