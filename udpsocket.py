#!/c/Python33/ python
import sys
import msvcrt
import socket,_thread as thread, threading
def UdpList(sock):
  while(1):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print (data)

if __name__ == '__main__':


  UDP_IP = '172.16.1.4'
  UDP_PORT = 4000
  MESSAGE = "Hello,mega 03!"
  
  print ("UDP target IP:", UDP_IP)
  print ("UDP target port:", UDP_PORT)
  print (MESSAGE)
 
  sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
  sock.bind(("", UDP_PORT))

  thread.start_new_thread(UdpList, (sock,))
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      sys.exit(1)
    elif ord(q)==99:#c
      msg = bytes(MESSAGE,'utf-8')
      sock.sendto(msg, (UDP_IP, UDP_PORT))
