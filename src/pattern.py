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
   def isBarBeforeHammer(self, bc, candidateBar, hammerBar):
                     
      print ("hammer Candidate hi and bar " + str(self.ba.getSessionHiAndBar(bc, candidateBar)))
      print ("hammer bar " + str(self.ba.getSessionHiAndBar(bc, hammerBar)))

      print ("isSessionHi Candidate " + str(self.ba.isSessionHi(bc, candidateBar)))      
      print ("isSessionHi hammer " + str(self.ba.isSessionHi(bc, hammerBar)))
      print ("isSessionLo hammer " + str(self.ba.isSessionLo(bc, hammerBar)))
      
      sessionHi = 1
      notSessionLo = 0
      
      candidateSessionHi = self.ba.isSessionHi(bc, candidateBar)
      candidateSessionLo = self.ba.isSessionLo(bc, candidateBar)
      hammerSessionHi = self.ba.isSessionHi(bc, hammerBar)
      hammerSessionLo = self.ba.isSessionLo(bc, hammerBar)
      
      if hammerSessionHi == sessionHi and \
         hammerSessionLo == 0 and \
         bc[candidateBar][self.hi] < bc[hammerBar][self.hi] and \
         bc[candidateBar][self.lo] < bc[hammerBar][self.lo]:
         return 1
     
#      if hammerSessionHi == sessionHi and hammerSessionLo == notSessionLo:
#         if hammerSessionHi == sessionHi and candidateSessionHi == sessionHi:
#            return 1
      
      if bc[candidateBar][self.hi] < bc[hammerBar][self.hi] and \
         bc[candidateBar][self.lo] < bc[hammerBar][self.lo]:
         return 2
      
      if bc[hammerBar][self.hi] < bc[candidateBar][self.hi] and \
         bc[hammerBar][self.lo] < bc[candidateBar][self.lo] and \
         bc[hammerBar][self.cl] < bc[candidateBar][self.cl]:
         return 3

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBarBeforeInvHammer(self, bc, candidateBar, invHammerBar):
               
      print ("candidateSessionLo " + str(self.ba.getSessionLoAndBar(bc, candidateBar)))
      print ("invHammerSessionLo " + str(self.ba.getSessionLoAndBar(bc, invHammerBar)))

      print ("isSessionLo Candidate bar " + str(self.ba.isSessionLo(bc, candidateBar)))
      print ("isSessionLo invHammer bar " + str(self.ba.isSessionLo(bc, invHammerBar)))
      print ("isSessionHi invHammer bar " + str(self.ba.isSessionHi(bc, invHammerBar)))

      sessionLo = sessionHi = 1
      notSessionHi = notSessionLo = 0

      candidateSessionLo = self.ba.isSessionLo(bc, candidateBar)
      candidateSessionHi = self.ba.isSessionHi(bc, candidateBar)
      invHammerSessionLo = self.ba.isSessionLo(bc, invHammerBar)
      invHammerSessionHi = self.ba.isSessionHi(bc, invHammerBar)
      
      # Inverted hammer at the low
      if invHammerSessionLo == sessionLo and \
         invHammerSessionHi == 0 and \
         bc[candidateBar][self.hi] > bc[invHammerBar][self.hi] and \
         bc[candidateBar][self.lo] > bc[invHammerBar][self.lo]:
         return 1
         
#      if invHammerSessionLo == sessionLo and invHammerSessionHi == notSessionHi:
#         if invHammerSessionLo == sessionLo and candidateSessionLo == sessionLo: 
#            return 1

      # Inverted hammer between session lo and hi
      if bc[candidateBar][self.hi] > bc[invHammerBar][self.hi] and \
         bc[candidateBar][self.lo] > bc[invHammerBar][self.lo]:
         return 2
      
      # Reversal bar
      if bc[invHammerBar][self.hi] > bc[candidateBar][self.hi] and \
         bc[invHammerBar][self.lo] > bc[candidateBar][self.lo] and \
         bc[invHammerBar][self.cl] > bc[candidateBar][self.cl]:
         return 3
                  
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBarAfterInvHammerLower(self, bc, barAfterInvHammer, invHammerBar):
      
      if bc[barAfterInvHammer][self.lo] < bc[invHammerBar][self.lo] and \
         bc[barAfterInvHammer][self.hi] < bc[invHammerBar][self.hi]:
         print ("isBarAfterInvHammerLower 1 ")
         return 1
         
      return 0

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isBarAfterHammerHigher(self, bc, barAfterHammer, hammerBar):
      
      if bc[barAfterHammer][self.hi] > bc[hammerBar][self.hi]:
         print ("isBarAfterHammerHigher 1 ")
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

      #if hiCl < loCl and hiCl != 0:
#      if hiCl - loCl > 0:
#         if hiCl > opCl:
         #if opLo - opCl > 0:
         
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

      #       |
      #       |
      #    | _|_ |
      #    |  |  |
      #    |     |
      #       
      
      hammerCandidateBar = bar - 2
      hammerBar = bar - 1
      
      beginningOfBarAfterHammer = 1
      endOfBarAfterHammer = 2
      
      hammer = 1
      higherHammer = 2
      reversal = 3

      print ("isHammer: current bar: " + str(bar))
      print ("isHammer: hammerBar: " + str(hammerBar))
      print ("isHammer: hammerCandidateBar: " + str(hammerCandidateBar))
      
      if self.isBarHammer(bc, hammerBar):
         barType = self.isBarBeforeHammer(bc, hammerCandidateBar, hammerBar)
         if barType == hammer:
            return hammer
            
#         elif barType == higherHammer:
#            return higherHammer
#         elif barType == reversal:
#            return reversal

      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInvHammer(self, bc, bar):

      #    |     |   
      #    |  |  |
      #    | _|_ |
      #       |  
      #       |  
      #       |

      invHammerCandidateBar = bar - 2
      invHammerBar = bar - 1
      
      barType = 0
      invHammer = 1
      higherInvHammer = 2
      reversal = 3

      print ("isInvHammer: current bar: " + str(bar))
      print ("isInvHammer: invHammerBar: " + str(invHammerBar))
      print ("isInvHammer: invHammerCandidateBar: " + str(invHammerCandidateBar))
      
      if self.isBarInvHammer(bc, invHammerBar):
         barType = self.isBarBeforeInvHammer(bc, invHammerCandidateBar, invHammerBar)
         if barType == invHammer:
            return invHammer
            
#         elif barType == higherInvHammer:
#            return higherInvHammer
#         elif barType == reversal:
#            return reversal
               
      return 0
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isEncompassing(self, bc, bar):
   
      # encompassing bar +
      #       |
      #    |  |_
      #    |  |
      #    | _|
      #       |
      #
      # encompassing bar -
      #       |
      #    | _|
      #    |  |
      #    |  |_
      #       |
      
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
