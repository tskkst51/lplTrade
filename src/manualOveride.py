'''
manualOveride module
'''

import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ManualOveride:
   def __init__(self, pfData, sym, rootPath):
   
      manualOveridePath = rootPath + "/manualOveride"
      manualOverideEx = ".mo"
      
      self.overideModes = pfData['overideModes'].split(',')
      self.doDoubleUp = pfData['doDoubleUp']
      self.path = manualOveridePath + "/" + sym + manualOverideEx

      print ("PATH " + self.path)
      print ("self.overideModes " + str(self.overideModes))
      
      if os.path.exists(self.path):
         os.unlink(self.path)
         
      try:
         # Open and truncate overide file
         with open(self.path, 'w') as mo:
            pass
      except OSError as e:
         print ("Can't open overide file for " + sym) 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOverideValue(self):
   
      try:
         if os.stat(self.path).st_size >= 1:
            with open(self.path, 'r') as mo:
               readValue = mo.readlines()
   
            print ("readValue " + str(readValue))
            
            if (isinstance(readValue, list)):
               orValue = readValue[0]
            print ("orValue " + str(orValue))
            for mode in self.overideModes:
               print ("mode " + str(mode))
               if orValue == mode:
                  self.pathFD = open(self.path, 'w')
                  return orValue
      except FileNotFoundError as e:
         pass
               
      return ""

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOverideAction(self, overideValue, inPosition):
   
      if overideValue == "openBuy":
         if not inPosition:
            return 1
            
      elif overideValue == "openSell":
         if not inPosition:
            return 2
            
      elif overideValue == "double":
         if inPosition and self.doDoubleUp:
            return 5

      elif overideValue == "close":
         if inPosition:
            return 6

      elif overideValue == "quit":
         if inPosition:
            return 7

      return 0
# end ManualOveride
