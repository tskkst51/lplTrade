import os
f = open('txt.txt', 'a', os.O_NONBLOCK)
while 1:
        f.write('asd')
        f.flush()
