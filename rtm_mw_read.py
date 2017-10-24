#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
if __name__ == '__main__':
  print('helo')
#  TCP_IP_1 = '172.16.1.3'
  TCP_IP_1 = '172.16.1.9'
  TCP_PORT = 502

  data = [1,1,0]#,156,0,157,0,158,0,159,0,160,0,161,0,162,0,163,0]#,145,0,146,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]

  Packet_1 = rtm_mw.RTM_MW(data)
  Packet_1.RetranNum = 0
  Packet_1.DestOne = [9,1,4]
  Packet_1.DestTwo = [3,0,5]
  Packet_1.DestThree = [4,0,0]

  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      Packet_1.connect(TCP_IP_1, TCP_PORT)

    elif ord(q)==115:#s
      try:
        Packet_1.Send()

      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        try:
          Packet_1.Send()
        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log_rv.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
          except TimeoutError:
            print (time.asctime())
            print ("mega12 not TCP connected ")
            error_log = open('error_log_rv.txt','a')
            error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
            error_log.close()
          except ConnectionAbortedError:
            print (time.asctime())
            print ("mega12 connect aborted TCP")
            error_log = open('error_log_rv.txt','a')
            error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
            erro_log.close()
            s.connect((TCP_IP, TCP_PORT))
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)

