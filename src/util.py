# lplTrade and company
# Let's trade some assets
#

#import krakenex
#from pykrakenapi import KrakenAPI
#import pusher
#from pusher import Pusher

import sys
import os
import io
import json

if __name__ == "__main__":
   pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Util():
   def __init__(self):
      
      self.rw = 1
   
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def writePath(self, path, line):

      with open(path, 'a+') as f:
         f.write ('%s' % str(line) + "\n")
         f.flush()
