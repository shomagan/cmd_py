#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
if __name__ == '__main__':
  print('helo')
  TCP_IP = '192.168.1.233'
  TCP_PORT = 502
  data = [1,73,0]
  Packet = rtm_mw.RTM_MW(data)
  Packet.RetranNum =1
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
