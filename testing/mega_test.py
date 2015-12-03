#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
import getopt
if __name__ == '__main__':
  '''test controller mega12'''
  conf = {
          'ip_addr': '192.168.1.218',
          'port': 502,
          'data' : [2,74,0],
          'retrun_num': 0,
          'dest': [218,0,8],
          'chanel': 8,
         }
  print (sys.argv)
  try:
      opts, args = getopt.getopt(sys.argv[1:], "w:r:a:c:i:v", ['ip_addr', 'version'])
  except getopt.GetoptError as err:
      # print help information and exit:
      print(str(err)) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
  print(opts)
  for o, a in opts:
      if o == '-r':
          conf['data'][1] = eval(a)
          print(conf['data'])
      elif o == '-w':
          conf['write'] = 1
      elif o == '-a':
          conf['dest'][0] = eval(a)
      elif o == '-i' or o == '--ip_addr':
          print (a)
          conf['ip_addr'] = a
      elif o == '-v' or o == '--version':
          print('exit')
          sys.exit(0)
      else:
          assert False, "Unhandled option"

  print(conf)

  Packet = rtm_mw.RTM_MW(conf['data'])
  Packet.RetranNum = conf['retrun_num']
  Packet.DestOne = conf['dest']
  Packet.DestTwo =  [13,0,2]
  Packet.DestThree = [200,0,5]

  print(Packet)
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      Packet.connect(conf['ip_addr'],conf['port'])
    elif ord(q)==115:#s
      try:
        Packet.Send()
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        try:
          Packet.Send()
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

