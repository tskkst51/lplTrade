'''
Pattern module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Pattern:
  def __init__(self, data, ba, lg):
  
    self.ba = ba
    self.lg = lg
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
    
    if self.reversalPctTrigger == 0.0:
      self.reversalPctTrigger = 60.0
      
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
  def isPreviousBarLowLower(self, bc, prevBar, bar):
          
    if bc[prevBar][self.lo] < bc[bar][self.lo]:
      return 1
                
    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isPreviousBarHighLower(self, bc, prevBar, bar):

    print ("bc[prevBar][self.hi] " + str(bc[prevBar][self.hi]))
    print ("bc[bar][self.hi] " + str(bc[bar][self.hi]))

    if bc[prevBar][self.hi] < bc[bar][self.hi]:
      return 1
                
    return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isPreviousBarHighHigher(self, bc, prevBar, bar):

    print ("bc[prevBar][self.hi] " + str(bc[prevBar][self.hi]))
    print ("bc[bar][self.hi] " + str(bc[bar][self.hi]))

    if bc[prevBar][self.hi] > bc[bar][self.hi]:
      return 1
                
    return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isPreviousBarLowHigher(self, bc, prevBar, bar):

    print ("bc[prevBar][self.lo] " + str(bc[prevBar][self.lo]))
    print ("bc[bar][self.lo] " + str(bc[bar][self.lo]))

    if bc[prevBar][self.lo] > bc[bar][self.lo]:
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
  def isPreviousBarOpenHigherClose(self, bc, prevBar, bar):
   
    print ("bc[prevBar][self.op] " + str(bc[prevBar][self.op]))
    print ("bc[bar][self.cl] " + str(bc[bar][self.cl]))
      
    if bc[prevBar][self.op] > bc[bar][self.cl]:
      return 1
                
    return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isPreviousBarOpenLowerClose(self, bc, prevBar, bar):
          
    if bc[prevBar][self.op] < bc[bar][self.cl]:
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
    
    self.lg.debug ("Previous bar: " + str(bar))
    self.lg.debug ("hi: " + str(hi))
    self.lg.debug ("lo: " + str(lo))
    self.lg.debug ("op: " + str(op))
    self.lg.debug ("cl: " + str(cl))
          
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
      
    hiLo = hi - lo
    if hiLo < 0:
      hiLo = hiLo * -1
      
    self.lg.debug ("loCl: " + str(loCl))
    self.lg.debug ("hiCl: " + str(hiCl))
    self.lg.debug ("opCl: " + str(opCl))
    self.lg.debug ("opLo: " + str(opLo))
    self.lg.debug ("opHi: " + str(opHi))
    self.lg.debug ("hiLo: " + str(hiLo))
      
    if hi > op:
      if lo <= op:
        if opHi - opLo > 0:    
          if hiCl - loCl > 0:
            #pctMoved = 100.00 * round(loCl / hiCl, 2)
            pctMoved = 100.00 * round(hiCl / hiLo, 2)
            self.lg.debug ("pctMoved: " + str(pctMoved))
            self.lg.debug ("reversalPctTrigger: " + str(self.reversalPctTrigger))
      
            if pctMoved > self.reversalPctTrigger:
              self.lg.debug ("Hammer bar detected! pctMoved: " + str(pctMoved))
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
    
    self.lg.debug ("Previous bar: " + str(bar))
    self.lg.debug ("hi: " + str(hi))
    self.lg.debug ("lo: " + str(lo))
    self.lg.debug ("op: " + str(op))
    self.lg.debug ("cl: " + str(cl))
          
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
      
    loHi = lo - hi
    if loHi < 0:
      loHi = loHi * -1

    self.lg.debug ("loCl: " + str(loCl))
    self.lg.debug ("hiCl: " + str(hiCl))
    self.lg.debug ("opCl: " + str(opCl))
    self.lg.debug ("opLo: " + str(opLo))
    self.lg.debug ("loHi: " + str(loHi))
    
    if lo < op:
      if hi > op:
        if opLo - opHi > 0:    
          if loCl - hiCl > 0:
            #pctMoved = 100.00 * (hiCl / loCl)
            pctMoved = 100.00 * (loCl / loHi)
            self.lg.debug ("pctMoved: " + str(pctMoved))
            self.lg.debug ("reversalPctTrigger: " + str(self.reversalPctTrigger))
      
            if pctMoved > self.reversalPctTrigger:
              self.lg.debug ("invHammer bar detected! pctMoved: " + str(pctMoved))
              return 1
    return 0
    

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isHammer(self, bc, bar):

    # b-2 b-1 bar
    #      |
    #      |
    #   | _|_ |
    #   |  |  |
    #   |     |
    #         |
                
    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isBarHammer(bc, bar - 1):
      if self.isPreviousBarLower(bc, bar - 2, bar - 1):
        self.lg.debug ("isPreviousBarLower: " + str(self.isPreviousBarLower(bc, bar - 2, bar - 1)))
        if prevSessionBarHi and not prevSessionBarLo:
          self.lg.debug ("prevSessionBarHi: " + str(prevSessionBarHi))
          self.lg.debug ("prevSessionBarLo: " + str(prevSessionBarLo))
          return 1
    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isInvHammer(self, bc, bar):

    # b-2 b-1 bar
    #   |     |  
    #   |  |  |
    #   | _|_ |
    #      |  
    #      |  
    #      |

    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isBarInvHammer(bc, bar - 1):
      if self.isPreviousBarHigher(bc, bar - 2, bar - 1):
        if prevSessionBarLo and not prevSessionBarHi:
          return 1
    return 0
        
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isHammerInner(self, bc, bar):

    # |
    # |
    # |
    # | _|_ |
    # |  |  |
    #    |  |
    #     
    
    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isBarHammer(bc, bar - 1):
      if self.isPreviousBarLower(bc, bar - 2, bar - 1):
        if not prevSessionBarHi:
          return 1
    return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isInvHammerInner(self, bc, bar):

    # Inv Hammer in between session hi's and lo's
    #  |
    #  |     |  
    #  |  |  |
    #  | _|_ |
    #     |  
    #     |  
    #     |
    #     |
        
    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)
    
    if self.isBarInvHammer(bc, bar - 1):
      if self.isPreviousBarHigher(bc, bar - 2, bar - 1):
        if not prevSessionBarLo:
          return 1
    return 0
    
  # Previous reversals
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isHiReversalO(self, bc, bar):
    
    # reversal bar + must be done on the close
    # |
    # |
    # |     |_
    #   _|  |
    #    | _|
    #    |_ 

    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isPreviousBarOpenHigherClose(bc, bar - 1, bar):
      print ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar - 1, bar)))
	   
      if self.isPreviousBarLower(bc, bar - 1, bar):
        print ("isPreviousBarLower " + str(self.isPreviousBarLower(bc, bar - 1, bar)))
        if self.isPreviousBarOpenLower(bc, bar - 1, bar):
          print ("isPreviousBarOpenLower " + str(self.isPreviousBarOpenLower(bc, bar - 1, bar)))
          if self.isPreviousBarCloseLower(bc, bar - 1, bar):
            print ("isPreviousBarCloseLower " + str(self.isPreviousBarCloseLower(bc, bar - 1, bar)))
            if self.isPreviousBarLower(bc, bar - 2, bar - 1):
              print ("is Bar - 2 Lower " + str(self.isPreviousBarHigher(bc, bar - 2, bar - 1)))
              #if not prevSessionBarHi:
              return 1

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isLoReversalO(self, bc, bar):
    
    # reversal bar -
    #    |_  
    #    | _|
    # | _|  |
    # |  |  |_
    # |     |
    # |

    prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isPreviousBarOpenHigherClose(bc, bar - 1, bar):
      print ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar - 1, bar)))
       
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
  def isLoReversal(self, bc, bar):
    
    # reversal bar -
    #    |_  
    #    |  _|
    # | _|   |
    # |  |   |_
    # |      |
    # |

    #prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isPreviousBarOpenLowerClose(bc, bar - 1, bar - 1):
      self.lg.debug ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar - 1, bar - 1)))
      if self.isPreviousBarOpenHigherClose(bc, bar, bar):
        self.lg.debug ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar, bar)))
        if self.isPreviousBarLowLower(bc, bar - 2, bar - 1):
          self.lg.debug ("isPreviousBarLowLower " + str(self.isPreviousBarLowLower(bc, bar - 2, bar - 1)))
          if self.isPreviousBarHighLower(bc, bar - 2, bar - 1):
            self.lg.debug ("isPreviousBarLowHigher " + str(self.isPreviousBarLowHigher(bc, bar - 2, bar - 1)))
            if self.isPreviousBarCloseHigher(bc, bar - 1, bar):
              self.lg.debug ("isPreviousBarCloseHigher " + str(self.isPreviousBarCloseHigher(bc, bar - 1, bar)))
              return 1

    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isHiReversal(self, bc, bar):
    
    # reversal bar, must be done on the close
    # |
    # |
    # |    |_
    #  _|  |
    #   | _|
    #   |_ 

    #prevSessionBarLo, prevSessionBarHi = self.getSessionBar(bc, bar - 2)

    if self.isPreviousBarOpenHigherClose(bc, bar - 1, bar - 1):
      self.lg.debug ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar - 1, bar - 1)))
      if self.isPreviousBarOpenLowerClose(bc, bar, bar):
        self.lg.debug ("isPreviousBarOpenLowerClose " + str(self.isPreviousBarOpenLowerClose(bc, bar, bar)))
        if self.isPreviousBarHighHigher(bc, bar - 2, bar - 1):
          self.lg.debug ("isPreviousBarHighHigher " + str(self.isPreviousBarHighHigher(bc, bar - 2, bar - 1)))
          if self.isPreviousBarLowHigher(bc, bar - 2, bar - 1):
            self.lg.debug ("isPreviousBarLowHigher " + str(self.isPreviousBarLowHigher(bc, bar - 2, bar - 1)))
            if self.isPreviousBarCloseLower(bc, bar - 1, bar):
              self.lg.debug ("isPreviousBarCloseLower " + str(self.isPreviousBarCloseLower(bc, bar - 1, bar)))
              return 1
    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isEngulfing(self, bc, bar):
  
    # engulfing bar +
    #   |
    #   |  |
    #   |  |
    #   |  |
    #   |
    
    if self.isPreviousBarHighHigher(bc, bar - 1, bar):
      self.lg.debug ("isPreviousBarHighHigher " + str(self.isPreviousBarHighHigher(bc, bar - 1, bar)))
      if self.isPreviousBarLowLower(bc, bar - 1, bar):
        self.lg.debug ("isPreviousBarLowLower " + str(self.isPreviousBarLowLower(bc, bar - 1, bar)))
        return 1

    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isEncompassing(self, bc, bar):
  
    # encompassing bar +
    #      |
    #   |  |
    #   |  |
    #   |  |
    #      |
    
    if self.isPreviousBarHighLower(bc, bar - 1, bar):
      self.lg.debug ("isPreviousBarHighLower " + str(self.isPreviousBarHighLower(bc, bar - 1, bar)))
      if self.isPreviousBarLowHigher(bc, bar - 1, bar):
        self.lg.debug ("isPreviousBarLowHigher " + str(self.isPreviousBarLowHigher(bc, bar - 1, bar)))
        return 1

    return 0

  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isHiEncompassing(self, bc, bar):
  
    # encompassing bar +
    #      |
    #   |  |_
    #   |  |
    #   | _|
    #      |
    
    if self.isPreviousBarHighLower(bc, bar - 1, bar):
      self.lg.debug ("isPreviousBarHighLower " + str(self.isPreviousBarHighLower(bc, bar - 1, bar)))
      if self.isPreviousBarLowHigher(bc, bar - 1, bar):
        self.lg.debug ("isPreviousBarLowHigher " + str(self.isPreviousBarLowHigher(bc, bar - 1, bar)))
        if self.isPreviousBarOpenLowerClose(bc, bar, bar):
          self.lg.debug ("isPreviousBarOpenLowerClose " + str(self.isPreviousBarOpenLowerClose(bc, bar, bar)))
          return 1

    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def isLoEncompassing(self, bc, bar):
  
    # encompassing bar -
    #      |
    #   | _|
    #   |  |
    #   |  |_
    #      |
    
    if self.isPreviousBarHighLower(bc, bar - 1, bar):
      self.lg.debug ("isPreviousBarHighLower " + str(self.isPreviousBarHighLower(bc, bar - 1, bar)))
      if self.isPreviousBarLowHigher(bc, bar - 1, bar):
        self.lg.debug ("isPreviousBarLowHigher " + str(self.isPreviousBarLowHigher(bc, bar - 1, bar)))
        if self.isPreviousBarOpenHigherClose(bc, bar, bar):
          self.lg.debug ("isPreviousBarOpenHigherClose " + str(self.isPreviousBarOpenHigherClose(bc, bar, bar)))
          return 1

    return 0
    
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  # Find the hi's/lows throughout the day to help with buy/sell decisions
  # A high would be a low bar followed by a high then followed by a low
  def FindHiPoints(self, bc, i):
        
    pass
        
  #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  def FindLoPoints(self, bc, i):
        
    pass          
        
# end Pattern
