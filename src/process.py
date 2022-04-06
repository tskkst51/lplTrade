'''
process module
'''

import subprocess
from multiprocessing import Process

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Process:
   def __init__(self):
   
      self.wp = os.getcwd()
      self.home = os.getenv(HOME)
      
      self.py = "python3"
      self.lplt = "bin/lpltL.py"
      
      self.pfC = self.home + "/profiles/et.json"
      self.pfP = self.wp + "/profiles/active.json"
      
      cmd="${py3} ${wp}/bin/lpltl.py -c $HOME/profiles/et.json -p ${wp}/test/${day}/profiles/active.json -w test/${day} -o -d -s $stock > $outFile"
      
      
#      q = Queue.Queue()
#      
#       t = threading.Thread(target=get_url, args = (q,u))
#       t.daemon = True
#       t.start()
#      
#      s = q.get()
#      print s

   def spawn(stock):
     
#      cmd = [self.py, self.lplt, \
#         "-c " + self.pfC, "-p " + self.pfP, "-d -s " + stock, shell=True, check=True, text=True, stdout=PIPE, stderr=STDOUT]
      
      print ("cmd " + str(cmd))
      
   def launch(self, stocks):
         
      for stock in stocks:
         p = Process(target=spawn, args=(stock,))
         p.start()

      print ("cmd " + cmd)
      
#      proc = subprocess.run(cmd)
#      
#      CompletedProcess(args=['ls', '-l'], returncode=0)
