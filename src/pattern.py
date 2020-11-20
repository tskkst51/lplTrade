'''
Pattern module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pattern:
   def __init__(self, data):
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

      self.reversalPctTrigger = float(data['profileTradeData']['reversalPctTrigger'])

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHammer(self, bc, bar):
      # The distance from the lo to the close
      # is > the distance from the hi to the close
      
      b = bar - 1
      hi = bc[b][self.hi]
      lo = bc[b][self.lo]
      cl = bc[b][self.cl]
      op = bc[b][self.op]

      print ("Previous bar: " + str(b))
      print ("hi: " + str(hi))
      print ("lo: " + str(lo))
      print ("op: " + str(op))
      print ("cl: " + str(cl))

      # Add bar length > average to take action!!
      # Add vol > avg vol ??
      
      # Hammer: close > open, lo < open, hi > open
      if cl > op:
         if lo < op:
            if hi > op:
               print ("Hammer! close > open, lo < open, hi > open")
               return 1
            else:
               return 0
               
      loCl = round(lo - cl, 2)
      if loCl < 0:
         loCl = loCl * -1
         
      hiCl = round(hi - cl, 2)
      
      if hiCl < 0:
         hiCl = loCl * -1
         
      print ("loCl: hiCl: " + str(loCl) + " " + str(hiCl))
      print ("loCl - hiCl: " + str(loCl - hiCl))

      #if hiCl < loCl and hiCl != 0:
      if hiCl - loCl > 0 and hiCl != 0:
         pctMoved = 100.00 - round(loCl / hiCl, 2)
         print ("pctMoved: " + str(pctMoved))

         if pctMoved < self.reversalPctTrigger:
            # Hammer
            return 1
            
#      if cl < op:
#         # Inverted Hammer
#         return 0
#
#      # Hammer
#      if hiCl > loCl:
#         self.hammer = 1
#         return self.hammer
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInvHammer(self, bc, bar):

      # Look at previous bar
      b = bar - 1
      hi = bc[b][self.hi]
      lo = bc[b][self.lo]
      cl = bc[b][self.cl]
      op = bc[b][self.op]

      # Inv Hammer
      print ("Previous bar: " + str(bar))
      print ("hi: " + str(hi))
      print ("lo: " + str(lo))
      print ("op: " + str(op))
      print ("cl: " + str(cl))

      # Inv Hammer: hi > op, cl < op, lo < op
      if hi > op:
         if cl < op:
            if lo < op:
               print ("Inv Hammer: hi > op, cl < op, lo < op")
               return 1
            else:
               return 0
         
      loCl = round(lo - cl, 2)
      if loCl < 0:
         loCl = loCl * -1
         
      hiCl = round(hi - cl, 2)
      
      if hiCl < 0:
         hiCl = loCl * -1
         
      print ("loCl: hiCl: " + str(loCl) + " " + str(hiCl))
      print ("loCl - hiCl: " + str(loCl - hiCl))

      if loCl > hiCl:
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
