#!/c/Python33/ python
#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 10  01 02 56 03 7E 
#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 10 01 02 56 03 7E
#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 FE 00 32 73 04 7E 
#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 FE 00 32 73 04 7E 
#7E 03 F0 0E 00 56 4D A0 8F 03 70 05 00 4B 03 7E  
#7E 03 F0 0E 00 56 4D A0 8F 03 70 05 00 4B 03 7E 
#7E 02 F0 0C 00 56 4D A0 8F 03 00 D3 02 7E 

#7E 02 F0 0F 00 46 52 A0 8F 03 00 10 01 02 DE 02 7E 
#7E 02 F0 0F 00 46 52 A0 8F 03 00 28 01 02 F6 02 7E 

#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 03 03 00 01 00 01
import sys,getopt
import _thread as thread
import msvcrt
import socket
import time

mdbtcp = [0x01,0x09,0x03,0x04,0x05,0x06,0x04,0x04,0x00,0x00,0x00,0x03]

def main():

  '''
  start d.bat
  rtm_mw_console.exe -n 3 -i 192.168.1.231 -a 7 -p 1 
  -n network waribale number
  -i ip address if use
  -a rtm_mw address
  -p comport
  -r ind numm 
  '''
  conf = {
          'port': 502,
          'data' : [0x01,0x09,0x03,0x04,0x05,0x06,0x04,0x04,0x00,0x00,0x00,0x02],
          'ip_addr': '192.168.1.250'
         }
  print (sys.argv)
  try:
      opts, args = getopt.getopt(sys.argv[1:], "a:f:r:i:", ['ip_addr'])
  except getopt.GetoptError as err:
      # print help information and exit:
      print(str(err)) # will print something like "option -a not recognized"
      usage()
      sys.exit(2)
  print(opts)
  for o, a in opts:
      if o == '-a':
          conf['data'][6] = eval(a)
      elif o == '-f':
          conf['data'][7] = eval(a)
      elif o == '-r':
          conf['data'][8] = (eval(a)>>8)&0xff
          conf['data'][9] = eval(a)&0xff
      elif o == '-i' or o == '--ip_addr':
          print(conf['ip_addr'])
          print (a)
          conf['ip_addr'] = a
      else:
          assert False, "Unhandled option"

  print(conf)
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      s.connect((conf['ip_addr'], conf['port']))
    elif ord(q)==115:#s

      try:
        mdbtcp_s = bytearray(conf['data'][0:])
        print(conf['data'][0:])
        s.send(mdbtcp_s)
        time_start=time.time()
        s.settimeout(4)
        data = s.recv(BUFFER_SIZE)
        time_pr=time.time() - time_start
        data_s =[]
  #        print(data)
        for i in range(0,len(data)):
          data_s.append(data[i])
        print(data_s)
        print("lenght",len(data_s))
        print(time_pr,'ms')
      except OSError:
        print ("Can't send tcp Packet")


if __name__ == '__main__':
  main()
