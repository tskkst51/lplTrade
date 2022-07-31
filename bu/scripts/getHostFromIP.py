import socket, sys             

if len(sys.argv) < 2:
   print ("Need file of IP's")
   exit (1)
   
with open(sys.argv[1], 'r') as ips:
   for i in ips:
      ip = i.strip("\n")
      try:
         print (str(socket.gethostbyaddr(ip)))  
      except socket.herror:
         continue

exit (0)