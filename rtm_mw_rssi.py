#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
def main():                                                                       
  print('helo')
  TCP_IP_8 = '172.16.1.8'
  TCP_IP_9 = '172.16.1.9'
  TCP_IP_3 = '172.16.1.3'
  TCP_IP_10 = '172.16.1.10'
  TCP_IP_11 = '172.16.1.11'
  TCP_IP_12 = '172.16.1.12'
  TCP_PORT = 502
  data = [1,8,0]#,73,0,48,0,49,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet8 = rtm_mw.RTM_MW(data)
  Packet8.RetranNum =0
  Packet8.DestOne = [8,1,7]
  Packet8.DestTwo =  [3,0,0]
  Packet8.DestThree = [7,0,2]

  Packet9 = rtm_mw.RTM_MW(data)
  Packet9.RetranNum =0
  Packet9.DestOne = [9,1,7]
  Packet9.DestTwo =  [3,0,0]
  Packet9.DestThree = [7,0,2]

  Packet3 = rtm_mw.RTM_MW(data)
  Packet3.RetranNum =0
  Packet3.DestOne = [3,0,7]
  Packet3.DestTwo =  [3,0,0]
  Packet3.DestThree = [7,0,2]

  Packet12 = rtm_mw.RTM_MW(data)
  Packet12.RetranNum =0
  Packet12.DestOne = [12,1,7]
  Packet12.DestTwo =  [3,0,0]
  Packet12.DestThree = [7,0,2]

  Packet10 = rtm_mw.RTM_MW(data)
  Packet10.RetranNum =0
  Packet10.DestOne = [10,1,7]
  Packet10.DestTwo =  [3,0,0]
  Packet10.DestThree = [7,0,2]

  Packet11 = rtm_mw.RTM_MW(data)
  Packet11.RetranNum =0
  Packet11.DestOne = [11,1,7]
  Packet11.DestTwo =  [3,0,0]
  Packet11.DestThree = [7,0,2]

  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
#      Packet8.connect(TCP_IP_8, TCP_PORT)
      Packet9.connect(TCP_IP_9, TCP_PORT)
      Packet10.connect(TCP_IP_10, TCP_PORT)
#      Packet11.connect(TCP_IP_11, TCP_PORT)
      Packet12.connect(TCP_IP_12, TCP_PORT)
    elif ord(q)==115:#s
      try:
#        print('rtm 8')
#        Packet8.Send()
        print('rtm 9')
        Packet9.Send()
        print('rtm 10')
        Packet10.Send()
 #       print('rtm 11')
  #      Packet11.Send()
        print('rtm 12')
        Packet12.Send()

      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        try:
          Packet.Send()
          Packet_two.Send()
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
if __name__ == "__main__":
    main()

