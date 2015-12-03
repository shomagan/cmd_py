#!/c/Python33/ python
import rtm_mw,sys,getopt
import msvcrt
def main():
  conf = {
          'ip_addr': '192.168.1.250',
          'port': 502,
          'data' : [2,74,0],
          'retrun_num': 0,
          'dest': [1,0,8],
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
  conf['dest'][2] = conf['chanel']
  Packet.DestOne = conf['dest']

  print(Packet)
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      Packet.connect(conf['ip_addr'], conf['port'])
    elif ord(q)==115:#s
      try:
        Packet.Send()
      except OSError:
        print ("Can't send tcp Packet")

if __name__ == '__main__':
  main()
