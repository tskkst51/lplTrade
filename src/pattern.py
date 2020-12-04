'''
Pattern module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pattern:
   def __init__(self, data, ba):
   
      self.ba = ba
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
   def getSessionBar(self, bc, bar):

      # return bar's session hi and lo
      return self.ba.isSessionLo(bc, bar), self.ba.isSessionHi(bc, bar)
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarHigher(self, bc, prevBar, bar):
               
      if bc[prevBar][self.hi] > bc[bar][self.hi] and \
         bc[prevBar][self.lo] > bc[bar][self.lo]:
         return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarOpenLower(self, bc, prevBar, bar):
               
      if bc[prevBar][self.op] < bc[bar][self.op]:
         return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarCloseHigher(self, bc, prevBar, bar):
               
      if bc[prevBar][self.cl] > bc[bar][self.cl]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarLower(self, bc, prevBar, bar):
               
      if bc[prevBar][self.hi] < bc[bar][self.hi] and \
         bc[prevBar][self.lo] < bc[bar][self.lo]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarOpenHigher(self, bc, prevBar, bar):
               
      if bc[prevBar][self.op] > bc[bar][self.op]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarCloseLower(self, bc, prevBar, bar):
               
      if bc[prevBar][self.cl] < bc[bar][self.cl]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarOpenCloseLower(self, bc, prevBar, bar):
               
      if bc[prevBar][self.op] < bc[bar][self.op] and \
         bc[prevBar][self.cl] < bc[bar][self.cl]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isPreviousBarOpenCloseHigher(self, bc, prevBar, bar):
               
      if bc[prevBar][self.op] > bc[bar][self.op] and \
         bc[prevBar][self.cl] > bc[bar][self.cl]:
            return 1
                        
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBarHammer(self, bc, bar):
   
      # The distance from the lo to the close
      # is > the distance from the hi to the close
      
      # Look at previous bar
      hi = bc[bar][self.hi]
      lo = bc[bar][self.lo]
      cl = bc[bar][self.cl]
      op = bc[bar][self.op]

      potentialHammer = 0
      
      print ("Previous bar: " + str(bar))
      print ("hi: " + str(hi))
      print ("lo: " + str(lo))
      print ("op: " + str(op))
      print ("cl: " + str(cl))
               
      loCl = lo - cl
      if loCl < 0:
         loCl = loCl * -1
         
      hiCl = hi - cl
      if hiCl < 0:
         hiCl = loCl * -1
         
      opCl = op - cl
      if opCl < 0:
         opCl = opCl * -1
         
      opLo = op - lo
      if opLo < 0:
         opLo = opLo * -1
         
      opHi = op - hi
      if opHi < 0:
         opHi = opHi * -1
         
      print ("loCl: " + str(loCl))
      print ("hiCl: " + str(hiCl))
      print ("opCl: " + str(opCl))
      print ("opLo: " + str(opLo))
      print ("opHi: " + str(opHi))
         
      if hi > op:
         if lo < op:
            if opHi - opLo > 0:      
               if hiCl - loCl > 0:
                  pctMoved = 100.00 - round(loCl / hiCl, 2)
                  print ("pctMoved: " + str(pctMoved))
                  print ("reversalPctTrigger: " + str(self.reversalPctTrigger))
         
                  if pctMoved > self.reversalPctTrigger:
                     print ("Hammer bar detected! pctMoved: " + str(pctMoved))
                     return 1
         
      return 0
      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBarInvHammer(self, bc, bar):
   
      # The distance from the lo to the close
      # is > the distance from the hi to the close
      
      # Look at previous bar
      hi = bc[bar][self.hi]
      lo = bc[bar][self.lo]
      cl = bc[bar][self.cl]
      op = bc[bar][self.op]

      potentialInvHammer = 0
      
      print ("Previous bar: " + str(bar))
      print ("hi: " + str(hi))
      print ("lo: " + str(lo))
      print ("op: " + str(op))
      print ("cl: " + str(cl))
               
      loCl = lo - cl
      if loCl < 0:
         loCl = loCl * -1
         
      hiCl = hi - cl
      if hiCl < 0:
         hiCl = loCl * -1
         
      opCl = op - cl
      if opCl < 0:
         opCl = opCl * -1

      opLo = op - lo
      if opLo < 0:
         opLo = opLo * -1

      opHi = op - hi
      if opHi < 0:
         opHi = opHi * -1
         
      print ("loCl: " + str(loCl))
      print ("hiCl: " + str(hiCl))
      print ("opCl: " + str(opCl))
      print ("opLo: " + str(opLo))
      print ("opHi: " + str(opHi))
      
      if lo < op:
         if hi > op:
            if opLo - opHi > 0:      
               if loCl - hiCl > 0:
                  pctMoved = 100.00 - (hiCl / loCl)
                  print ("pctMoved: " + str(pctMoved))
                  print ("reversalPctTrigger: " + str(self.reversalPctTrigger))
         
                  if pctMoved > self.reversalPctTrigger:
                     print ("invHammer bar detected! pctMoved: " + str(pctMoved))
                     return 1
         
      return 0
      

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHammer(self, bc, bar):

      #  b-2 b-1 bar
      #       |
      #       |
      #    | _|_ |
      #    |  |  |
      #    |     |
      #       
                        
      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

      if self.isBarHammer(bc, bar - 1):
         if self.isPreviousBarLower(bc, bar - 2, bar - 1):
            print ("isPreviousBarLower: " + str(self.isPreviousBarLower(bc, bar - 2, bar - 1)))
            if prevSessionBarHi and not prevSessionBarLo:
               print ("prevSessionBarHi: " + str(prevSessionBarHi))
               print ("prevSessionBarLo: " + str(prevSessionBarLo))
               return 1

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInvHammer(self, bc, bar):

      #  b-2 b-1 bar
      #    |     |   
      #    |  |  |
      #    | _|_ |
      #       |  
      #       |  
      #       |

      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

      if self.isBarInvHammer(bc, bar - 1):
         if self.isPreviousBarHigher(bc, bar - 2, bar - 1):
            if prevSessionBarLo and not prevSessionBarHi:
               return 1
               
      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHammerInner(self, bc, bar):

      # |
      #       |
      #       |
      #    | _|_ |
      #    |  |  |
      #    |     |
      #       
      #             |
      
      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

      if self.isBarHammer(bc, bar - 1):
         if self.isPreviousBarLower(bc, bar - 2, bar - 1):
            if not prevSessionBarHi:
               return 1
               
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInvHammerInner(self, bc, bar):

      # Inv Hammer in between session hi's and lo's
      # |
      #    |     |   
      #    |  |  |
      #    | _|_ |
      #       |  
      #       |  
      #       |
      #            |
            
      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)
      
      if self.isBarInvHammer(bc, bar - 1):
         if self.isPreviousBarHigher(bc, bar - 2, bar - 1):
            if not prevSessionBarLo:
               return 1
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHiReversal(self, bc, bar):
      
      # reversal bar + must be done on the close
      # |
      # |
      # |     |_
      #   _|  |
      #    | _|
      #    |_ 

      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

      if self.isPreviousBarLower(bc, bar - 1, bar):
         print ("isPreviousBarLower " + str(self.isPreviousBarLower(bc, bar - 1, bar)))
         if self.isPreviousBarOpenLower(bc, bar - 1, bar):
            print ("isPreviousBarOpenLower " + str(self.isPreviousBarOpenLower(bc, bar - 1, bar)))
            if self.isPreviousBarCloseLower(bc, bar - 1, bar):
               print ("isPreviousBarCloseLower " + str(self.isPreviousBarCloseLower(bc, bar - 1, bar)))
               if self.isPreviousBarHigher(bc, bar - 2, bar - 1):
                  print ("is Bar - 2 Higher " + str(self.isPreviousBarHigher(bc, bar - 2, bar - 1)))
                  #if not prevSessionBarHi:
                  return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLoReversal(self, bc, bar):
      
      # reversal bar -
      #    |_  
      #    | _|
      # | _|  |
      # |  |  |_
      # |     |
      # |

      prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

      if self.isPreviousBarHigher(bc, bar - 1, bar):
         print ("isPreviousBarHigher " + str(self.isPreviousBarHigher(bc, bar - 1, bar)))
         if self.isPreviousBarOpenLower(bc, bar - 1, bar):
            print ("isPreviousBarOpenLower " + str(self.isPreviousBarOpenLower(bc, bar - 1, bar)))
            if self.isPreviousBarCloseHigher(bc, bar - 1, bar):
               print ("isPreviousBarCloseHigher " + str(self.isPreviousBarCloseHigher(bc, bar - 1, bar)))
               if self.isPreviousBarLower(bc, bar - 2, bar - 1):
                  print ("is Bar - 2 Lower " + str(self.isPreviousBarLower(bc, bar - 2, bar - 1)))
                  #if not prevSessionBarLo:
                  return 1

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isHiEncompassing(self, bc, bar):
   
      # encompassing bar +
      #       |
      #    |  |_
      #    |  |
      #    | _|
      #       |
      
      pass
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isLoEncompassing(self, bc, bar):
   
      # encompassing bar -
      #       |
      #    | _|
      #    |  |
      #    |  |_
      #       |
      
      pass
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   # Find the hi's/lows throughout the day to help with buy/sell decisions
   # A high would be a low bar followed by a high then followed by a low
   def FindHiPoints(self, bc, i):
            
      pass
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def FindLoPoints(self, bc, i):
            
      pass              
            
# end Pattern
