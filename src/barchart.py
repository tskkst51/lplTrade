'''
Barchart module
'''
class Barchart:
   def __init__(self):
      self.totGain = 0.0
      self.grandTotal = 0.0
      self.strAction = ""
      self.debugFlag = debugFlag
      self.verboseFlag = verboseFlag
      self.logPath = logPath
      self.debugPath = debugPath
      self.wins = 0
      self.losses = 0
      self.totalTrades = 0

   def loadBC(bc, path):
      ctr = 0
      with open(path, 'r') as bcData:
         for line in bcData:
            line = line.strip("\n")
            bar = line.split(",")
                        
            if ctr == 0:
               bc[ctr][0] = float(bar[0])
               bc[ctr][1] = float(bar[1])
               bc[ctr][2] = float(bar[2])
               bc[ctr][3] = float(bar[3])
               bc[ctr][4] = int(bar[4])
            else:
               bc.append(bar)
               bc[ctr][0] = float(bar[0])
               bc[ctr][1] = float(bar[1])
               bc[ctr][2] = float(bar[2])
               bc[ctr][3] = float(bar[3])
               bc[ctr][4] = int(bar[4])
            ctr += 1
            
      return ctr
      
   def unLoadBC(bc, path, i):
   
      with open(path, 'a+') as bcData:
         bcData.write('%s, ' % str(bc[i][0]))
         bcData.write('%s, ' % str(bc[i][1]))
         bcData.write('%s, ' % str(bc[i][2]))
         bcData.write('%s, ' % str(bc[i][3]))
         bcData.write('%s, ' % str(bc[i][4]))
         bcData.write('\'%s\'' % bc[i][5] + "\n")
         
      return 
            
# end Barchart
