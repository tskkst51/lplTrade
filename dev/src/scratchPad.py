   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def exitWProfit(self, lastGain, posPrice):
      
      # Calculate if we should exit with profit
      
      # How close is the price to the min profit amount?
            
      pctNearTrgt = lastGain / self.getTargetProfit()

      self.lg.debug("exitWProfit: pctNearTrgt " + str(pctNearTrgt))

      triggerAmt = lastGain * self.inPosProfitPct

      self.lg.debug("exitWProfit: triggerAmt " + str(triggerAmt))
      
      if triggerAmt < posPrice:
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceTracking(self, action=0):
      
      self.lg.debug("In algorithmPriceTracking: " + str(action))

      # If in a position and in a profit, monitor it
      # Don't let a profit turn into a loss.
      
      if not self.inPosition():
         return 0
      
      #tGain = self.getTotalGain()
      tGain = self.totalGain
      
      # Do something different if this is the first position
      if tGain == 0.0 and self.numTrades < 1:
         return 0

      self.lg.debug("self.getCurrentLast(): " + str (self.getCurrentLast()))
      self.lg.debug("self.openPositionPrice: " + str (self.openPositionPrice))
      
      if self.getCurrentLast() < self.openPositionPrice:
         if tGain > 0:
            self.lg.debug("Position is losing money: ")
            self.lg.debug("-" + str(self.openPositionPrice - self.getCurrentLast()))
            if self.exitWProfit(tGain, self.openPositionPrice - self.getCurrentLast()):
               return 1
               
         if tGain < 0:
            self.lg.debug("Position is adding to the current loss: ")
            self.lg.debug(str(tGain) + " -" + str(self.openPositionPrice - self.getCurrentLast()))
      
      else:
         # In positive position let it ride
         self.lg.debug("Position is gaining profit. Let it ride: ")
         self.lg.debug(str(self.getCurrentLast() - self.openPositionPrice))
    
      return 0