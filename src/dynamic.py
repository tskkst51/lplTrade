'''
dynamic module
'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Dynamic:
   def __init__(self, timeBar, path, dc):
   
      self.inRangeBars = 1
      
      self.initialTimeBar = timeBar
      
      assert(path)
      
      self.dcPath = path
      self.gpPath = path.replace(".dc", ".gp")
      
      self.inRangeBars = 1
      
      self.algoStr = ""
      
      if timeBar == 1:
         self.inRangeBars = 5
      elif timeBar == 2:
         self.inRangeBars = 4
      elif timeBar == 3:
         self.inRangeBars = 4
      elif timeBar == 4:
         self.inRangeBars = 2
      elif timeBar == 5:
         self.inRangeBars = 1

      self.bc = dc.readDailyBarChart(self.dcPath)
      self.gd = dc.readDailyGapData(self.gpPath)
      self.dc = dc

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getRangeBars(self):
      
      return self.inRangeBars
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def initAlgoStr(self, timeBar=1):

      self.algoStr = "TB" + str(timeBar) + "_"
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def appendAlgoStr(self, algoStr):

      self.algoStr += algoStr
            
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def endAlgoStr(self):

      self.algoStr += "DY"
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def isInitialAlgoStr(self):

      if self.algoStr == "":
         return 1
         
      return 0
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def setOpenCloseBars(self, currentPrice, timeBar):
   
      if self.isInitialAlgoStr():
         self.initAlgoStr()
         self.appendAlgoStr(self.getInitialOpenCloseBarAlgo(currentPrice))
         print ("self.algoStr " + self.algoStr)
         self.endAlgoStr()
         
         #self.setBeginDayOpenCloseBarAlgo(dc, bc, gd, currentPrice)
      else:
         self.initAlgoStr(timeBar)
         self.appendAlgoStr(self.getOpenCloseBarAlgo(currentPrice))
         self.endAlgoStr()

      print ("self.algoStr " + self.algoStr)

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getOpenCloseBarAlgo(self, currentPrice):
      pass
      
   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   def getInitialOpenCloseBarAlgo(self, currentPrice):
   
      print ("gd gapDatta " + str(self.gd))
      print ("bc gapDatta " + str(self.bc))
      
      avgPriceMove = self.gd[0]
      largestPriceMove = self.gd[1]
      dateLargestPriceMove = int(self.gd[3])
      
      #dailyData = sorted(dc.items(), key=lambda x: x[1], reverse=True)
      
      #lastDay = dailyData[len(dailyData) - 1]
      lastDay = len(self.bc) - 1
      lastDaysDate = self.bc[lastDay][8]
      
      directionGain = 0 # 0 == negative 1 == positive
      if currentPrice - self.bc[lastDay][3] > 0:
         directionGain = 1

      for day in self.bc:
         print ("dateLargestPriceMove " + str(dateLargestPriceMove))
         print ("day " + str(day))
         print ("date " + str(day[8]))
         if int(day[8]) == int(dateLargestPriceMove):
            print ("here ")
            hi = day[0]
            lo = day[1]
            op = day[2]
            cl = day[3]
            bl = day[5]

            # op > cl; prev day hi > lo
            # _|       |_
            #  |_     _|
            #  |       |

            # cl > op
           # algoStr += "OB1_CB3_OS3_CS1_"
            
            if op > cl:
               pctIntraMove = round(lo / hi, 2)
               pctDayaMove = round(cl / currentPrice, 2)
               self.appendAlgoStr("OB3_CB1_OS1_CS3_")
            else:
               pctIntraMove = round(hi / lo, 2)
               pctDayaMove = round(currentPrice / cl, 2)
               self.appendAlgoStr("OB1_CB3_OS3_CS1_")
               
            print ("algoStr " + str(self.algoStr))
            print ("pctDayaMove " + str(pctDayaMove))
            print ("pctIntraMove " + str(pctIntraMove))

            break

      print ("avgPriceMove " + str(avgPriceMove))
      print ("largestPriceMove " + str(largestPriceMove))
      #print ("len(dailyData) " + str(len(dailyData)))
      print ("dateLargestPriceMove " + str(dateLargestPriceMove))
      print ("lastDay " + str(lastDay))
      print ("lastDaysDate " + str(lastDaysDate))
      print ("directionGain " + str(directionGain))
      print ("currentPrice " + str(currentPrice))

      #avgPriceMove = self.getDAvgPriceMoveEquivToCurrent(self.gd)
      
      return self.algoStr
 

