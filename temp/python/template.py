import sys, os

exit = 1
quit = 1
os._exit = 1
sys.exit = 1

try:

    for _ in range(%s):

        %s

        print('TestCase')

except EOFError:
    pass