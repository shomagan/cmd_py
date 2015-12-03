import sys, os, _thread as thread, threading,socket,atexit,io,serial,time

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt

def main():
  TCP_IP = '172.16.1.9'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  MESSAGE = "Hello, World!"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  a = 0
  #thread.start_new_thread(ComList, (ser,a ))
  Packet = RTM_MW()
  while 1:
#    if msvcrt.kbhit():
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==99:#c
      try:
        s.connect((TCP_IP, TCP_PORT))
      except TimeoutError:
        print (time.asctime())
        print ("mega12 not TCP connected ")
        error_log = open('error_log_TCP.txt','a')
        error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
        error_log.close()
      except ConnectionAbortedError:
        print (time.asctime())
        print ("mega12 connect aborted TCP")
        error_log = open('error_log_TCP.txt','a')
        error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
        error_log.close()
        s.connect((TCP_IP, TCP_PORT))
    elif ord(q)==115:#s
      try:
        data_buf = Packet.SendPacket(s)
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      while(1):
        try:
          data_buf = Packet.SendPacket(s)
        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log_TCP.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
          except TimeoutError:
            print (time.asctime())
            print ("mega12 not TCP connected ")
            error_log = open('error_log_TCP.txt','a')
            error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
            error_log.close()
          except ConnectionAbortedError:
            print (time.asctime())
            print ("mega12 connect aborted TCP")
            error_log = open('error_log_TCP.txt','a')
            error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
            erro_log.close()
            s.connect((TCP_IP, TCP_PORT))
        print (time.asctime())
#        time.sleep(0.1)
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)

class RTM_MW(object):
  def __init__(self):
                            #                    command  &rotor    &mega1   &megafinaly modbuss
              #         0    1    2     3   4     5     6   7   8     9   10    11  12    13  14  15    16    17  18
                        #7E   02   F0   21   00   52   34   03   90   06   D1   00  00   00    00   85 FF DC FF 04 00 00 00 00 00 00 01 00 00 00 00 00 67 06 7E
    self.request_r4 = [0x7E,0x02,0xF0,0x21,0x00,0x52,0x34,0x03,0x90,0x09,0xD1,0x00,0x00,0x00,0x00,0x05,0x2D,0x1C,0x3C,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x95,0x03,0x7E]
    ChekSum = RTM64ChkSUM(self.request_r4[1:],len(self.request_r4)-4)
    self.request_r4[-3] = ChekSum&0xFF
    self.request_r4[-2] =(ChekSum>>8)&0xFF
#                     7E 02 F0 0C 00 52 34 06 51 03 00 DE 01 7E
    self.cmd_r4 = [0x7E,0x02,0xF0,0x0C,0x00,0x52,0x34,0x09,0x51,0x03,0x00,0xDE,0x01,0x7E]
    ChekSum = RTM64ChkSUM(self.cmd_r4[1:],len(self.cmd_r4)-4)
    self.cmd_r4[-3] = ChekSum&0xFF
    self.cmd_r4[-2] =(ChekSum>>8)&0xFF
    self.request_v4 = [0x7E,0x02,0xF0,0x52,0x00,0x56,0x34,0x03,0x90,0x09,0xD1,0x30,0x81,0x03,0x00,0x30,0x82,0x03,0x00,0x30,0x83,0x03,0x00,0x30,0x84,0x03,0x00,0x30,0x85,0x03,0x00,0x30,0x86,0x03,0x00,0x30,0x87,0x03,0x00,0x30,0x88,0x03,0x00,0x30,0x89,0x03,0x00,0x30,0x8A,0x03,0x00,0x30,0x8B,0x03,0x00,0x30,0x8C,0x03,0x00,0x30,0x8D,0x03,0x00,0x30,0x8E,0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x6E,0x0D,0x00,0x00,0x00,0x00,0xE9,0x0D,0x7E]
    ChekSum = RTM64ChkSUM(self.request_v4[1:],len(self.request_v4)-4)
    self.request_v4[-3] = ChekSum&0xFF
    self.request_v4[-2] =(ChekSum>>8)&0xFF
    self.cmd_v4 = [0x7E,0x02,0xF0,0x0C,0x00,0x56,0x34,0x09,0x51,0x03,0x00,0xE5,0x01,0x7E]
    ChekSum = RTM64ChkSUM(self.cmd_v4[1:],len(self.cmd_v4)-4)
    self.cmd_v4[-3] = ChekSum&0xFF
    self.cmd_v4[-2] =(ChekSum>>8)&0xFF

    self.OkReceptionCnt =0
    self.Errorcnt =0
  def SendPacket(self,s):
    BUFFER_SIZE = 1024
    data_s =[]
    
    Packet_str = bytearray(self.cmd_r4[0:])
    print(Packet_str)
    time_start=time.time()
    s.send(Packet_str)
    s.settimeout(5)
#data = s.recvfrom(BUFFER_SIZE)

     
    try:
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      print('time ms'+str(time_pr))
#    data = char_to_int(data_s,len(data_s))

      for i in range(0,len(data)):
        data_s.append(data[i])
 #     data_s = "".join(data)
      chek_sum = RTM64ChkSUM(data_s[1:],len(data_s)-4)
      chek_sum_recv = data_s[-3]|(data_s[-2]<<8)

      if ((self.request_r4[0] == data_s[0])&
         (self.request_r4[5] == data_s[5])&
         (self.request_r4[6] == data_s[6])&
         (self.request_r4[9] == data_s[9])&
         (chek_sum_recv == chek_sum)):
        self.OkReceptionCnt+=1
        print('good receive r4 packet')
      else:
        print('receive bad packet','\n',data_s,'\n',self.request_r4)
        error_log = open('error_log_TCP.txt','a')
        error_log.write ('receive bad packet'+'\n'+str(data_s)+'\n'+str(self.request_r4))
        error_log.close()

          
#      print (data_s,self.OkReceptionCnt)
#      print(time_pr,'s')
#      print(len(data))
    except socket.timeout:
      self.Errorcnt+=1
      print("TCP_RecvError",self.Errorcnt)
      print (time.asctime())
      error_log = open('error_log_TCP.txt','a')
      error_log.write ("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
      error_log.close()
    
#    time.sleep(5)
    data_s =[]
    Packet_st = bytearray(self.cmd_v4[0:])
    print(Packet_st)
    time_start=time.time()
    s.send(Packet_st)
    s.settimeout(5)
#data = s.recvfrom(BUFFER_SIZE)
    try:
      data = s.recv(BUFFER_SIZE)
      self.OkReceptionCnt+=1
      time_pr=time.time() - time_start
      print('time ms'+str(time_pr))
#    data = char_to_int(data_s,len(data_s))
      for i in range(0,len(data)):
        data_s.append(data[i])
 #     data_s = "".join(data)
      chek_sum = RTM64ChkSUM(data_s[1:],len(data_s)-4)
      chek_sum_recv = data_s[-3]|(data_s[-2]<<8)

      if ((self.request_v4[0] == data_s[0])&
         (self.request_v4[5] == data_s[5])&
         (self.request_v4[6] == data_s[6])&
         (self.request_v4[9] == data_s[9])&
         (chek_sum_recv == chek_sum)):
        self.OkReceptionCnt+=1
        print('good receive v4 packet')
      else:
        error_log = open('error_log_TCP.txt','a')
        error_log.write ('receive bad packet'+'\n'+str(data_s)+'\n'+str(self.request_r4))
        error_log.close()

        print('receive bad packet','\n',data_s,'\n',self.request_v4)
#      print (data_s,self.OkReceptionCnt)
#      print(time_pr,'s')
#      print(len(data))
    except socket.timeout:
      self.Errorcnt+=1
      print("TCP_RecvError",self.Errorcnt)
      print (time.asctime())
      error_log = open('error_log_TCP.txt','a')
      error_log.write ("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
      error_log.close()
    return data_s

    

def RTM64CRC16(pbuffer , Len):
  """CRC16 for RTM64"""
  CRC = 0x0000
  k = 0
  while (k < Len):
    CRC = (CRC^((pbuffer[k]<<8)&0xFFFF))
    k+=1
    i=8
    while (i):
      i-=1
      if (CRC & 0x8000): CRC = (((CRC<<1)&0xFFFF)^0x1021)
      else: CRC = ((CRC<<1)&0xFFFF)
  return CRC
def crc16(pck,len):
  """CRC16 for modbus"""
  CRC = 0xFFFF
  i = 0
  while ( i < len ):
    CRC ^= pck[i]
    i+=1
    j = 0 
    while ( j < 8):
       j+=1
       if ( (CRC & 0x0001) == 1 ): CRC = ((CRC >> 1)&0xFFFF) ^ 0xA001;
       else: CRC >>= 1;
  return (CRC&0xFFFF)
def RTM64ChkSUM(pbuffer,Len):
  """ CheckSum RTM64"""
  sum = 0
  i = 0
  while (i<Len):
    sum = sum + pbuffer[i]
    i+=1
  return sum
def int_to_char(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ['~']
  while (i<len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i+=1
  return cmd_r[1:]
def list_to_str(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ''
  while (i<len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i+=1
  return cmd_r
def str_to_int(cmd_x,lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i<lenth):
    cmd_r[i]=ord(cmd_x[i])
    i+=1
  return cmd_r

def char_to_int(cmd_x,lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i<lenth):
    cmd_r[i]=ord(str(cmd_x[i]))
    i+=1
  return cmd_r
def print_hex(cmd,lenth):
  i = 0
  hexf=[0 for x in range(lenth)]
  while (i<lenth):
    hexf[i] = (hex(cmd[i]))
    i+=1
  print (hexf)
if __name__ == "__main__":
  print ("told one things")
  main()
