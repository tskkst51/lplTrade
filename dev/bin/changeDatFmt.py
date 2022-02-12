## Change directory date name from M D Y to Y M D
  
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def changeDateInFile():

   exitDir="exitResults"
   
   newStr = ""
   for path in os.listdir(exitDir):
      srcP = exitDir + "/" + path
      dstP = exitDir + "/" + path + "-n"
      with open(dstP, 'w') as dst:
         with open(srcP, 'r') as src:
            print (str(srcP))
            for l in src:
               if "2020" in l:
                  b, m, e = l.rpartition("2020")
               elif "2021" in l:
                  b, m, e = l.rpartition("2021")
               else:
                  continue
               yr = m
               mnth = b[0] + b[1]
               day = b[2] + b[3]
               newDate = yr + mnth + day
               print (l)
               print (newDate)
               lItems = l.split()
               print (str(lItems))
               lItems[0] = newDate
               print (str(lItems))
               for lItem in lItems:
                  newStr += lItem + " "
               newStr += "\n"
               print (newStr)
            dst.write(newStr)
            newStr = ""
         os.rename(dstP, srcP)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def changeDate():

   testDir="../lpltArchives"
   
   dirs = os.listdir(testDir)
   
   for d in dirs:
      print (str(d[0]), str(d[1]))
      if d[0] == '2' and d[1] == '0' and d[2] == '2' and d[3] == '0':
         print ("HERE")
         continue 
      if "2020" in d:
         b, m, e = d.rpartition("2020")
      elif "2021" in d:
         b, m, e = d.rpartition("2021")
      else:
         continue
         
      print (str(d))
      yr = m
      mnth = b[0] + b[1]
      day = b[2] + b[3]
      oldDate = testDir + "/" + d
      newDate = testDir + "/" + yr + mnth + day + e
      print (oldDate)
      print (newDate)
      os.rename(oldDate, newDate)
      
changeDate()

#changeDateInFile()

exit (0)