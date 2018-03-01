#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
if __name__ == '__main__':
  print('helo')
  TCP_IP = '192.168.1.232'
  TCP_PORT = 502

#  data = [2,204,0,205,0,206,0,232,0,233,0,234,0,75,0]#,156,0,157,0,158,0,159,0,160,0,161,0,162,0,163,0]#,145,0,146,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  data = [2,44,0,43,0]
#  data = [1,161,0x0,162,0x0]#,156,0,157,0,158,0,159,0,160,0,161,0,162,0,163,0]#,145,0,146,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet_1 = rtm_mw.RTM_MW(data)
  Packet_1.RetranNum = 1
  Packet_1.DestOne = [3,0,7]
  Packet_1.DestTwo = [5,0,5]
  Packet_1.DestThree = [4,0,0]

  while 1:
    q = msvcrt.getch()
    global socket
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      socket = Packet_1.connect(TCP_IP, TCP_PORT)

    elif ord(q)==115:#s
      try:
#        Packet_1.SendPacket(socket)
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

