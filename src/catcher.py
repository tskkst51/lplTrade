import os
import signal
import sys
import time

def signal_handler(signal, frame):
  print ('catcher: signal %d received!') % signal
  raise Exception('catcher: i am done')

if hasattr(os.sys, 'winver'):
    signal.signal(signal.SIGBREAK, signal_handler)
else:
    signal.signal(signal.SIGTERM, signal_handler)

print ('catcher: started')
try:
    while(True):
        print ('catcher: sleeping...')
        time.sleep(1)
except Exception as ex:
    print (ex)
    sys.exit(0)
