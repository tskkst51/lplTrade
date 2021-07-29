   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def algorithmPriceTracking(self, action=0):
      
      self.lg.debug("In algorithmPriceTracking: " + str(action))

      # If in a position and in a profit, monitor it
      # Don't let a profit turn into a loss.
      
