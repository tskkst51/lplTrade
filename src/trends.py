'''
trends module
'''

import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Trends:
   def __init__(self):
   
      # Bar identifiers High, Low, Open, Close, Volume, Length, Date 
      
      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6 # Session Hi
      self.sL = 7 # Session Li
      self.dt = 8
      
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def init(self):
   
      # Short, mid, long, mega, future
      trends = [[0.0,0.0,0.0,0.0,0.0]]
   
      return trends

# end trends
