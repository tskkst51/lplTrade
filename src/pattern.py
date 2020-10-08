'''
Pattern module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pattern:
   def __init__(self):
      self.pattern = 0
      self.hammer = 1
      self.invHammer = 2
      self.hi = 0
      self.lo = 1
      self.op = 2
      self.cl = 3
      self.vl = 4
      self.bl = 5
      self.sH = 6
      self.sL = 7
      self.dt = 8

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHammer(self, bc, bar):
      # The distance from the lo to the close
      # is > the distance from the hi to the close
      
      b = bar - 1
      hi = bc[b][self.hi] * -1
      lo = bc[b][self.lo] * -1
      cl = bc[b][self.cl] * -1
      op = bc[b][self.op] * -1
      
      # Hammer
      if hi - cl > lo - cl:
         self.hammer = 1
         return self.hammer
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInvHammer(self, bc, bar):

      b = bar - 1
      hi = bc[b][self.hi] * -1
      lo = bc[b][self.lo] * -1
      cl = bc[b][self.cl] * -1
      op = bc[b][self.op] * -1

      # Inv Hammer
      if lo - cl > hi - cl:
         self.InvHammer = 1
         return self.InvHammer

      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Find the hi's/lows throughout the day to help with buy/sell decisions
   # A high would be a low bar followed by a high then followed by a low
   def FindHiPoints(self, bc, i):
            
      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def FindLoPoints(self, bc, i):
            
      return 0
            
            
# end Pattern
