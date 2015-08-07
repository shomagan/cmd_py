#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
if __name__ == '__main__':
  print('helo')
  TCP_IP = '192.168.1.231'
  TCP_PORT = 502
  data = [2,160,0,161,0,162,0,163,0,164,0,165,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet = rtm_mw.RTM_MW(data)
  Packet.RetranNum =0
  Packet.DestOne = [3,0,7]
  Packet.DestTwo =  [8,0,7]
  Packet.DestThree = [200,0,5]

  print(Packet)
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      Packet.connect(TCP_IP, TCP_PORT)
    elif ord(q)==115:#s
      try:
        Packet.Send()
      except OSError:
        print ("Can't send tcp Packet")

