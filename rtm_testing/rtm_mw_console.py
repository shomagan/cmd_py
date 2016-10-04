#!/c/Python33/ python
import rtm_mw,sys,getopt,serial
import _thread as thread
import msvcrt
def ComList(ser,a):
  while(1):
    hello = ser.read(1)
    if (hello != ''):
      a+=1
      #print(char_to_int(hello,len(hello)))
      error_log = open('recv_log.txt','a')
      if(ord(hello)==250):
        error_log.write ('\n')
      error_log.write (str(hello))
      error_log.close()
      print(hello,ord(hello))

def main():
  '''
  start d.bat
  rtm_mw_console.exe -n 3 -i 192.168.1.231 -a 7 -p 1 
  -n network waribale number
  -i ip address if use
  -a rtm_mw address
  -p comport

  '''
  conf = {
          'ip_addr': '192.168.1.250',
          'port': 502,
          'data' : [2,74,0],
          'retrun_num': 0,
          'dest': [1,0,8],
          'chanel': 8,
          'com_channel': 0,
         }
  print (sys.argv)
  try:
      opts, args = getopt.getopt(sys.argv[1:], "w:n:a:c:i:p:v", ['ip_addr', 'version'])
  except getopt.GetoptError as err:
      # print help information and exit:
      print(str(err)) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
  print(opts)
  for o, a in opts:
      if o == '-n':
          conf['data'][1] = eval(a)
          print(conf['data'])
      elif o == '-w':
          conf['data'][0] = 1
      elif o == '-a':
          conf['dest'][0] = eval(a)
      elif o == '-i' or o == '--ip_addr':
          print (a)
          conf['ip_addr'] = a
      elif o == '-p':
          conf['com_channel'] = eval(a)-1
#          print (a)
      elif o == '-v' or o == '--version':
          print('exit')
          sys.exit(0)
      else:
          assert False, "Unhandled option"

  print(conf)
  open_com_port =1
  try:
    ser = serial.Serial(conf['com_channel'])  # open first serial port
    ser.baudrate = 115200;
    print (ser.name)          # check which port was really used
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial.SerialException as e:
    open_com_port =0
    print("could not open port \n")

  Packet = rtm_mw.RTM_MW(conf['data'])
  Packet.RetranNum = conf['retrun_num']
  conf['dest'][2] = conf['chanel']
  Packet.DestOne = conf['dest']
  a=0
  if open_com_port:
    thread.start_new_thread(ComList, (ser,a))

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
    elif ord(q)==97:#a
      Packet.SendPacket(ser,0)


if __name__ == '__main__':
  main()
