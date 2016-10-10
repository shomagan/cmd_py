try:
    import msvcrt
    PLATFORM = "win"
except ImportError:
    PLATFORM = "unix"
    import tty
    import termios
    from select import select
import rtm_mw
import mdb_tcp_request 
import sys
import time


try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import optparse

DEFAULT_PORT = "COM2"
DEFAULT_BAUDRATE = 115200
DEFAULT_RTS = None
DEFAULT_DTR = None


def send_mdb_packet(mdb_packet,log,rtm_mw_packet,timeout=6):
  global TCP_IP
  global TCP_PORT
  global s_socket

  try:
    mdb_packet.send(s_socket,log,timeout = timeout)
  except OSError:
    print ("Can't send tcp Packet")
    error_log = open('error_log_rv.txt','a')
    error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
    error_log.close()
    try:
      s_socket.close()
      print('close tcp connection')
      s_socket = rtm_mw_packet.connect(TCP_IP, TCP_PORT)
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
      s_socket = rtm_mw_packet.connect(TCP_IP, TCP_PORT)


def send_rtm_mw_packet(rtm_mw_packet,log,timeout=6):
  global TCP_IP
  global TCP_PORT
  global s_socket

  try:
    rtm_mw_packet.Send(timeout = timeout)
  except OSError:
    print ("Can't send tcp Packet")
    error_log = open('error_log_rv.txt','a')
    error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
    error_log.close()
    try:
      s_socket.close()
      print('close tcp connection')
      s_socket=rtm_mw_packet.connect(TCP_IP, TCP_PORT)
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
      s_socket=rtm_mw_packet.connect(TCP_IP, TCP_PORT)

class Controller_info(object):
  def __init__(self): 
    self.address = 0
    self.di_sost = 0
    self.do_sost = 0
    self.ai_sost = 0
  def __del__(self):
    print("controller info")
  def request_address()
    for i in range(250):
      send_mdb_packet(mdb_packet,log,Packet)      
  def parse_mdb_response(packet):
    packet_dict = {'address':0,'command':0}
    if len(packet):
      packet_dict.
      
    print('address', packet[0], 'hex', hex(packet[0]))
    print('command', packet[1], 'hex', hex(packet[1]))
    if packet[1] ==3 or packet[1]==4:
      print('response byte', packet[2], hex(packet[2]))
      for i in range(packet[2]//2):
        data = (packet[3+i*2]<<8)&0xff00
        data |= (packet[3+i*2+1]&0x00ff)
        print('data of regs', i, '= ', data, 'hex', hex(data))
    elif packet[1] ==16:
      address = (packet[2]<<8)&0xff00
      address |= (packet[3]&0x00ff)
      print('start address', address, 'hex', hex(address))
      number_write_reg = (packet[4]<<8)&0xff00
      number_write_reg |= (packet[5]&0x00ff)
      print('number_write_reg', number_write_reg, 'hex', hex(number_write_reg))

    elif packet[1]==6:
      address = (packet[2]<<8)&0xff00
      address |= (packet[3]&0x00ff)
      print('start address', address, 'hex', hex(address))
      reg_value = (packet[4]<<8)&0xff00
      reg_value |= (packet[5]&0x00ff)
      print('reg_value', reg_value, 'hex', hex(reg_value))
    return
    

def main():
  global TCP_IP
  TCP_IP = '192.168.2.205'
  global TCP_PORT
  TCP_PORT = 502
  global s_socket
  data = [2,3,0,1,0]#,73,0,48,0,49,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet = rtm_mw.RTM_MW(data)
  print('helo from ',TCP_IP,TCP_PORT)
  print(Packet)
  mdb_packet = mdb_tcp_request.Mdb()
  log = open('log_rv.txt','a')
  log.write ("mega12 test mdb retranslate"+time.asctime()+'\n')
  controller = Controller_info()

  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      log.close()
      del Packet
      del mdb_packet
      sys.exit(1)
    elif ord(q)==99:#c
      s_socket = Packet.connect(TCP_IP, TCP_PORT)
    elif ord(q)==115:#s
      try:
        Packet.Send()
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        mdb_packet.mdb_address = 4
        for i in range(15):
          send_mdb_packet(mdb_packet,log,Packet)
          time.sleep(0.2)
          if(msvcrt.kbhit()):
            log.close()
            del Packet
            del mdb_packet
            sys.exit(1)
        for i in range(15):
          Packet.RetranNum = 0
          Packet.DestOne = [4,0,4]
          time.sleep(0.3)
          send_rtm_mw_packet(Packet,log)
          time.sleep(0.2)
          if(msvcrt.kbhit()):
            log.close()
            del Packet
            del mdb_packet
            sys.exit(1)
        for i in range(15):
          Packet.RetranNum = 1
          Packet.DestOne = [4,0,7]
          Packet.DestTwo =  [3,0,0]
          send_rtm_mw_packet(Packet,log)
          time.sleep(0.2)
          if(msvcrt.kbhit()):
            log.close()
            del Packet
            del mdb_packet
            sys.exit(1)


        if(msvcrt.kbhit()):
          log.close()
          del Packet
          del mdb_packet
          sys.exit(1)
    elif ord(q)==116:#t
      mdb_packet.mdb_address = 4
      for i in range(15):
        send_mdb_packet(mdb_packet,log,Packet)
        time.sleep(0.2)
        if(msvcrt.kbhit()):
          log.close()
          del Packet
          del mdb_packet
          sys.exit(1)
      for i in range(15):
        Packet.RetranNum = 0
        Packet.DestOne = [4,0,4]
        time.sleep(0.3)
        send_rtm_mw_packet(Packet,log)
        time.sleep(0.2)
        if(msvcrt.kbhit()):
          log.close()
          del Packet
          del mdb_packet
          sys.exit(1)
      for i in range(15):
        Packet.RetranNum = 1
        Packet.DestOne = [4,0,7]
        Packet.DestTwo =  [3,0,0]
        send_rtm_mw_packet(Packet,log)
        time.sleep(0.2)
        if(msvcrt.kbhit()):
          log.close()
          del Packet
          del mdb_packet
          sys.exit(1)


      if(msvcrt.kbhit()):
        log.close()
        del Packet
        del mdb_packet
        sys.exit(1)


if __name__ == '__main__':
    '''request modbus packet on com port or tcp connect
      options:
        -m modbus address
        -p port
        -b baud rate
    '''
    main()

