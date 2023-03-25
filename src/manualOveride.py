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
      
      self.path = manualOveridePath + "/" + sym + manualOverideEx

      try:
         # Open and truncate overide file
         with open(self.path, 'w') as mo:
            pass
      except OSError as e:
         print ("Can't open overide file for " + sym) 
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOverideValue(self):
   
      if os.stat(self.path).st_size >= 1:
         with open(self.path, 'r') as mo:
            readValue = mo.readlines()
            #print ("readValue " + str(readValue))
         
         if (isinstance(readValue, list)):
            orValue = readValue[0]
            
         for mode in self.overideModes:
            
            if orValue == mode:
               self.pathFD = open(self.path, 'w')
               return orValue
      
      return ""
# end ManualOveride
