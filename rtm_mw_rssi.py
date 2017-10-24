#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
import time
def main():                                                                       
  print('helo')
  TCP_IP_95 = '172.16.1.95'
  TCP_IP_3 = '172.16.1.3'
  TCP_IP_4 = '172.16.1.4'
  TCP_IP_5 = '172.16.1.5'
  TCP_IP_6 = '172.16.1.6'
  TCP_IP_7 = '172.16.1.7'
  TCP_IP_8 = '172.16.1.8'
  TCP_IP_10 = '172.16.1.10'
  TCP_IP_11 = '172.16.1.11'
  TCP_IP_12 = '172.16.1.12'
  TCP_IP_94 = '172.16.1.94'
  TCP_IP_95 = '172.16.1.95'
  TCP_IP_96 = '172.16.1.96'
  TCP_IP_97 = '172.16.1.97'
  TCP_IP_98 = '172.16.1.98'
  TCP_IP_99 = '172.16.1.99'
  TCP_IP_100 = '172.16.1.100'
#  TCP_IP_95 = '172.24.131.95'
  TCP_IP_101 = '172.16.1.101'
  TCP_IP_102 = '172.16.1.102'
  TCP_IP_232 = '192.168.1.232'

  TCP_PORT = 502
  data = [1,8,0,0,0]#,73,0,48,0,49,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet3 = rtm_mw.RTM_MW(data)
  Packet3.RetranNum =0
  Packet3.DestOne = [3,0,7]

  Packet6 = rtm_mw.RTM_MW(data)
  Packet6.RetranNum =0
  Packet6.DestOne = [6,0,7]
  Packet7 = rtm_mw.RTM_MW(data)
  Packet7.RetranNum =0
  Packet7.DestOne = [7,0,7]
  Packet95 = rtm_mw.RTM_MW(data)
  Packet95.RetranNum =0
  Packet95.DestOne = [95,0,7]

  Packet98 = rtm_mw.RTM_MW(data)
  Packet98.RetranNum =0
  Packet98.DestOne = [98,0,7]

  Packet98 = rtm_mw.RTM_MW(data)
  Packet98.RetranNum =0
  Packet98.DestOne = [98,0,7]

  Packet94 = rtm_mw.RTM_MW(data)
  Packet94.RetranNum =0
  Packet94.DestOne = [94,0,7]

  Packet95 = rtm_mw.RTM_MW(data)
  Packet95.RetranNum =0
  Packet95.DestOne = [95,0,7]

  Packet96 = rtm_mw.RTM_MW(data)
  Packet96.RetranNum =0
  Packet96.DestOne = [96,0,7]

  Packet97 = rtm_mw.RTM_MW(data)
  Packet97.RetranNum =0
  Packet97.DestOne = [97,0,7]
  Packet99 = rtm_mw.RTM_MW(data)
  Packet99.RetranNum =0
  Packet99.DestOne = [99,0,7]
 
  Packet101 = rtm_mw.RTM_MW(data)
  Packet101.RetranNum =0
  Packet101.DestOne = [101,0,7]

  Packet100 = rtm_mw.RTM_MW(data)
  Packet100.RetranNum =0
  Packet100.DestOne = [100,0,7]

  Packet102 = rtm_mw.RTM_MW(data)
  Packet102.RetranNum =0
  Packet102.DestOne = [102,0,7]


  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
#      Packet8.connect(TCP_IP_8, TCP_PORT)
#      Packet93.connect(TCP_IP_93, TCP_PORT)
      Packet3.connect(TCP_IP_3, TCP_PORT)
#      Packet6.connect(TCP_IP_6, TCP_PORT)
#      Packet7.connect(TCP_IP_7, TCP_PORT)
#      Packet95.connect(TCP_IP_95, TCP_PORT)
#      Packet4.connect(TCP_IP_4, TCP_PORT)


    #  Packet232.connect(TCP_IP_232, TCP_PORT)

    elif ord(q)==115:#s
      try:
#        print('rtm 93')
#        Packet93.Send()
     #   print('rtm 3')
    #    Packet3.Send()
   #     print('rtm 4')
        Packet3.Send()
        print('rtm 3')         
 
 #       Packet6.Send()
  #      print('rtm 6')         
 #       Packet4.Send()
  #      print('rtm 94')         
  #      Packet7.Send()
   #     print('rtm 7')         
   #     Packet95.Send()
    #    print('rtm 95')         

 #       Packet95.Send()
  #      print('rtm 232')     `
   #     Packet232.Send()
#        print('rtm 3')
 #       Packet3.Send()

   #     print('rtm 5')
  #      Packet232.Send()


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

