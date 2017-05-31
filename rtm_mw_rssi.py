#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
import time
def main():                                                                       
  print('helo')
  TCP_IP_7 = '172.16.1.7'
  TCP_IP_8 = '172.16.1.8'
  TCP_IP_9 = '172.16.1.9'
  TCP_IP_3 = '172.16.1.3'
  TCP_IP_4 = '172.16.1.4'
  TCP_IP_5 = '172.16.1.5'
  TCP_IP_10 = '172.16.1.10'
  TCP_IP_11 = '172.16.1.11'
  TCP_IP_12 = '172.16.1.12'
  TCP_IP_232 = '192.168.1.232'
  TCP_IP_93 = '172.24.130.93'
  TCP_IP_94 = '172.24.130.94'
  TCP_IP_95 = '172.16.1.95'

  TCP_PORT = 502
  data = [1,8,0,0,0]#,73,0,48,0,49,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet7 = rtm_mw.RTM_MW(data)
  Packet7.RetranNum =0
  Packet7.DestOne = [7,0,7]
  Packet7.DestTwo =  [3,0,0]
  Packet7.DestThree = [7,0,2]

  Packet8 = rtm_mw.RTM_MW(data)
  Packet8.RetranNum =0
  Packet8.DestOne = [8,1,7]

  Packet9 = rtm_mw.RTM_MW(data)
  Packet9.RetranNum =0
  Packet9.DestOne = [9,0,7]

  Packet3 = rtm_mw.RTM_MW(data)
  Packet3.RetranNum =0
  Packet3.DestOne = [3,0,7]

  Packet4 = rtm_mw.RTM_MW(data)
  Packet4.RetranNum =0
  Packet4.DestOne = [4,0,7]

  Packet5 = rtm_mw.RTM_MW(data)
  Packet5.RetranNum =0
  Packet5.DestOne = [5,0,7]

  Packet12 = rtm_mw.RTM_MW(data)
  Packet12.RetranNum =0
  Packet12.DestOne = [12,1,7]

  Packet10 = rtm_mw.RTM_MW(data)
  Packet10.RetranNum =0
  Packet10.DestOne = [10,0,7]

  Packet11 = rtm_mw.RTM_MW(data)
  Packet11.RetranNum =0
  Packet11.DestOne = [11,0,7]

  Packet232 = rtm_mw.RTM_MW(data)
  Packet232.RetranNum =0
  Packet232.DestOne = [3,0,7]

  Packet93 = rtm_mw.RTM_MW(data)
  Packet93.RetranNum =0
  Packet93.DestOne = [93,0,7]

  Packet94 = rtm_mw.RTM_MW(data)
  Packet94.RetranNum =0
  Packet94.DestOne = [94,0,7]

  Packet95 = rtm_mw.RTM_MW(data)
  Packet95.RetranNum =0
  Packet95.DestOne = [95,0,7]

  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
#      Packet8.connect(TCP_IP_8, TCP_PORT)
#      Packet93.connect(TCP_IP_93, TCP_PORT)
  #    Packet95.connect(TCP_IP_95, TCP_PORT)
  #    Packet232.connect(TCP_IP_232, TCP_PORT)
      Packet3.connect(TCP_IP_3, TCP_PORT)
  #    Packet4.connect(TCP_IP_4, TCP_PORT)
      Packet5.connect(TCP_IP_5, TCP_PORT)

    elif ord(q)==115:#s
      try:
#        print('rtm 93')
#        Packet93.Send()
     #   print('rtm 3')
    #    Packet3.Send()
   #     print('rtm 4')
  #      Packet4.Send()
#        print('rtm 95')         
 #       Packet95.Send()
  #      print('rtm 232')
   #     Packet232.Send()
        print('rtm 3')
        Packet3.Send()

        print('rtm 5')
        Packet5.Send()


      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        try:
          Packet93.Send()
          Packet94.Send()
          Packet95.Send()

        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log_rv.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            Packet93.close_tcp_connect()
            Packet94.close_tcp_connect()
            Packet95.close_tcp_connect()
            Packet93.connect(TCP_IP_93, TCP_PORT)
            Packet94.connect(TCP_IP_94, TCP_PORT)
            Packet95.connect(TCP_IP_95, TCP_PORT)

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
            Packet93.close_tcp_connect()
            Packet94.close_tcp_connect()
            Packet95.close_tcp_connect()
            Packet93.connect(TCP_IP_93, TCP_PORT)
            Packet94.connect(TCP_IP_94, TCP_PORT)
            Packet95.connect(TCP_IP_95, TCP_PORT)

        time.sleep(0.8)
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)
if __name__ == "__main__":
    main()

