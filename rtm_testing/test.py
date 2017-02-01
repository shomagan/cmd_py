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
import socket


try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import optparse

DEFAULT_PORT = "COM2"
DEFAULT_BAUDRATE = 115200
DEFAULT_RTS = None
DEFAULT_DTR = None
ADDRESS_MDB_SHIFT_REG = 154






def send_mdb_packet(mdb_packet,log,timeout=6,parse =0):
  global TCP_IP
  global TCP_PORT
  global s_socket

  try:
    packet_from = mdb_packet.send(s_socket,log,timeout=timeout,parse=parse)
  except OSError:
    print ("Can't send tcp Packet")
    error_log = open('error_log_rv.txt','a')
    error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
    error_log.close()
    try:
      s_socket.close()
      print('close tcp connection')
      socket_connect(s_socket, TCP_IP, TCP_PORT)
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
      socket_connect(s_socket, TCP_IP, TCP_PORT)
  return packet_from

def send_rtm_mw_packet(rtm_mw_packet,log,timeout=6):
  global TCP_IP
  global TCP_PORT
  global s_socket
  answer_cheked =0
  try:
    answer_cheked = rtm_mw_packet.Send(s_socket, timeout = timeout)
  except OSError:
    print ("Can't send tcp Packet")
    error_log = open('error_log_rv.txt','a')
    error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
    error_log.close()
    try:
      s_socket.close()
      print('close tcp connection')
      socket_connect(s_socket, TCP_IP, TCP_PORT)
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
      socket_connect(s_socket, TCP_IP, TCP_PORT)
  return answer_cheked

class Controller_info(object):
  ''' info about controller who will testing for'''
  def __init__(self,log,Packet): 
    self.mdb_address = 0
    self.rtm_address = 0
    self.mdb_shift = 0
    self.di_sost = 0
    self.do_sost = 0
    self.ai_sost = 0
    self.log= log
    self.rtm_mw_packet = Packet

  def __del__(self):
    print("controller info")

  def request_address_mdb_packet(self,mdb_packet):
    self.mdb_address = 0
    for i in range(2,6):
      mdb_packet.mdb_address = i
      mdb_packet.mdb_command = 3
      mdb_packet.mdb_start_address = 0
      mdb_packet.mdb_reg_numm = 2
      packet = send_mdb_packet(mdb_packet,self.log,timeout = 0.2)
      if len(packet) > 3:
        packet_dict = self.parse_mdb_response(packet[6:])
        if packet_dict['command'] == mdb_packet.mdb_command:
          print(packet_dict)
          if packet_dict['address'] == i:
            print('find mdb address')
            self.mdb_address = packet_dict['data'][1]
            if packet_dict['data'][1] == i:
              self.rtm_address = packet_dict['data'][0]
              print('mdb address = ',self.mdb_address,'\n')
            else:
              self.mdb_shift = 1
              print('but not match in packet',packet_dict['data'][1],'\n')
              print('most likely set mdb_shift regs in 0')
            break
        else:
          print ('not match mdb command','\n')
    return self.mdb_address 
  def write_regs_for_mdb(self,mdb_packet,mdb_start_address,data):
    mdb_packet.mdb_address = self.mdb_address
    if (len(data)>1):
      mdb_packet.mdb_command = 16
    else:
      mdb_packet.mdb_command = 6
    mdb_packet.mdb_start_address = mdb_start_address
    mdb_packet.mdb_reg_numm = len(data)
    mdb_packet.mdb_data = data
    packet = send_mdb_packet(mdb_packet,self.log,timeout=0.4,parse=1)
    succes =0
    if len(packet) > 3:
      packet_dict = self.parse_mdb_response(packet[6:])
      print('write mdb regs',packet_dict)
      if packet_dict['command'] == mdb_packet.mdb_command:
        if packet_dict['command'] == 16:
          if packet_dict['number_write_reg'] == len(data):
            succes =1
            print('write ',packet_dict['number_write_reg'],'regs','from address',mdb_packet.mdb_start_address,'\n')
        elif packet_dict['command'] == 6:
          if packet_dict['writes_regs_address'] == mdb_packet.mdb_start_address:
            succes =1
            print('write value ',packet_dict['reg_value'],'in address reg',mdb_packet.mdb_start_address,'\n')
    return succes
    

  def parse_mdb_response(self,packet):
    packet_dict = {'address':0,'command':0}
    if len(packet):
      packet_dict['address'] = packet[0]
      packet_dict['command'] = packet[1]      
    if packet[1] ==3 or packet[1]==4:
      packet_dict['data'] = []
      for i in range(packet[2]//2):
        reg_value = (packet[3+i*2]<<8)&0xff00
        reg_value |= (packet[3+i*2+1]&0x00ff)
        packet_dict['data'].append(reg_value)
    elif packet[1] ==16:
      address = (packet[2]<<8)&0xff00
      address |= (packet[3]&0x00ff)
      number_write_reg = (packet[4]<<8)&0xff00
      number_write_reg |= (packet[5]&0x00ff)
      packet_dict['number_write_reg'] = number_write_reg
    elif packet[1]==6:
      writes_regs_address = (packet[2]<<8)&0xff00
      writes_regs_address |= (packet[3]&0x00ff)
      packet_dict['writes_regs_address'] = writes_regs_address
      reg_value = (packet[4]<<8)&0xff00
      reg_value |= (packet[5]&0x00ff)
      packet_dict['reg_value'] = reg_value
    return packet_dict
    

def main():
  global TCP_IP
  TCP_IP = '192.168.2.205'
  global TCP_PORT
  TCP_PORT = 502
  global s_socket
  data = [2,3,0,1,0]#,73,0,48,0,49,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet = rtm_mw.RTM_MW(data)
  print('hello from ',TCP_IP,TCP_PORT)
  print(Packet)
  mdb_packet = mdb_tcp_request.Mdb()
  log = open('log_rv.txt','a')
  log.write ("mega12 test mdb retranslate"+time.asctime()+'\n')
  controller = Controller_info(log,Packet)

  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      log.close()
      del Packet
      del mdb_packet
      sys.exit(1)
    elif ord(q)==99:#c
      s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
      socket_connect(s_socket, TCP_IP, TCP_PORT)
    elif ord(q)==115:#s
      try:
        Packet.Send()
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        if controller.mdb_address == 0:
          if controller.request_address_mdb_packet(mdb_packet):
            print ('find it')
        if controller.rtm_address==0 and controller.mdb_shift == 1:
          data = [0x0000]
          controller.write_regs_for_mdb(mdb_packet,ADDRESS_MDB_SHIFT_REG-1,data)
          controller.request_address_mdb_packet(mdb_packet)

        print ('test immodule port')
        Packet.RetranNum = 1
        Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,7]
        Packet.DestTwo =  [3,0,0]
        cycle_rtm_send(30,Packet,controller,log)

        print ('test com1 port')
        Packet.RetranNum = 1
        Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,1]
        Packet.DestTwo =  [3,0,0]
        cycle_rtm_send(30,Packet,controller,log)

        print ('test com2 port')
        Packet.RetranNum = 1
        Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,5]
        Packet.DestTwo =  [3,0,0]
        cycle_rtm_send(30,Packet,controller,log)

        print ('test radio rfm23 port')
        Packet.RetranNum = 1
        Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,0]
        Packet.DestTwo =  [3,0,0]
        cycle_rtm_send(30,Packet,controller,log)

        if(msvcrt.kbhit()):
          log.close()
          del Packet
          del mdb_packet
          sys.exit(1)

    elif ord(q)==116:#t
      if controller.mdb_address == 0:
        if controller.request_address_mdb_packet(mdb_packet):
          print ('find it')
      if controller.rtm_address==0 and controller.mdb_shift == 1:
        '''it state sets if ADDRESS_MDB_SHIFT_REG is enabled'''
        data = [0x0000]
        controller.write_regs_for_mdb(mdb_packet,ADDRESS_MDB_SHIFT_REG-1,data)
        controller.request_address_mdb_packet(mdb_packet)
      print ('rtm_mw test immodule port')
      Packet.RetranNum = 1
      Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,7]
      Packet.DestTwo =  [5,0,0]
      cycle_rtm_send(10,Packet,controller,log)

      print ('rtm_mw test com1 port')
      Packet.RetranNum = 1
      Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,1]
      Packet.DestTwo =  [5,0,0]
      cycle_rtm_send(10,Packet,controller,log)

      print ('rtm_mw test com2 port')
      Packet.RetranNum = 1
      Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,5]
      Packet.DestTwo =  [5,0,0]
      cycle_rtm_send(10,Packet,controller,log)

#      print ('test radio rfm23 port')
#      Packet.RetranNum = 1
#      Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,0]
#      Packet.DestTwo =  [3,0,0]
#       cycle_rtm_send(30,Packet,controller,log)

      if(msvcrt.kbhit()):
        log.close()
        del Packet
        del mdb_packet
        sys.exit(1)

def cycle_rtm_send(cycle,Packet,controller,log,timeout=1):
  p = ''
  for i in range(cycle):
    Packet.RetranNum = 1
    Packet.DestOne = [controller.rtm_address&0xff,(controller.rtm_address>>8)&0xff,5]
    Packet.DestTwo =  [3,0,0]
    if (send_rtm_mw_packet(Packet,log,timeout=timeout)):
      p+='#'
    else:
      p+='*'
    progress(p)
    time.sleep(0.05)
    if(msvcrt.kbhit()):
      log.close()
      del Packet
      del mdb_packet
      sys.exit(1)
  end_progress(p)


def start_progress():
  sys.stdout.write('\r'+"/")
  sys.stdout.flush()
    

def progress(p):
  sys.stdout.write('\r'+"/"+p)
  sys.stdout.flush()


def end_progress(p):
  sys.stdout.write('\r'+"/"+p+'/'+'\n')
  sys.stdout.flush()


def socket_connect(s, TCP_IP, TCP_PORT):
  try:
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
    error_log.close()
    s.connect((TCP_IP, TCP_PORT))

if __name__ == '__main__':
    '''request modbus packet on com port or tcp connect
      options:
        -m modbus address
        -p port
        -b baud rate
    '''
    main()

