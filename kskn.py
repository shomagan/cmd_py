#!/c/Python33/ python
"""
add addres property befor start program
"""
import sys, os, _thread as thread, threading,socket,atexit,io,serial,time

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt
#def hextoascii():
def ComList(ser,a):
  while(1):
    hello = ser.read(1)
    if (hello != ''):
      a+=1
      #print(char_to_int(hello,len(hello)))
      print(hello,ord(hello))

def main():
  ser = serial.Serial(1)  # open first serial port
  ser.baudrate = 9600;
  ser.stopbits = 2
  print (ser.name)          # check which port was really used
  try:
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial.SerialException as e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)
  hello = 'hello'
  TCP_IP = '192.168.1.242'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  MESSAGE = "Hello, World!"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  a = 0
  thread.start_new_thread(ComList, (ser,a ))
  print ('tread is start')
  data = [2,73,0,74,0,0,0]#,81,0,82,0,100,0]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
  data_p = [0x01,89,0]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
  MdbKskn = [0x01,0x03,0x00,0x02,0x00,0x04,0x00,0x00]
  Packet = RTM_MW(data)  
  Packet.Chan = 0x01

  while 1:
#    if msvcrt.kbhit():
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==119:#w
      ser.write(cmd)
    elif ord(q)==110:#n
      print(Cmd_NI)
      ser.write(Cmd_NI)
    elif ord(q)==114:#r
      print(cmd_FR_T)
      ser.write(cmd_FR_T)

    elif ord(q)==109:#m
      #mdb = int_to_char(cmd[-11:-3])
      mdb = cmd[-11:-3]
      print (cmd[-11:-3])
      ser.write(mdb)
    elif ord(q)==97:#a
      Packet.SendPacket(ser,0)
    elif ord(q)==43:#+
      data_p[1] += 1
      Packet_p = RTM_MW(data_p)  
      Packet_p.SendPacket(ser,0)

    elif ord(q)==99:#c
      try:
        s.connect((TCP_IP, TCP_PORT))
      except TimeoutError:
        print (time.asctime())
        print ("mega12 not TCP connected ")
        error_log = open('error_log.txt','a')
        error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
        error_log.close()
      except ConnectionAbortedError:
        print (time.asctime())
        print ("mega12 connect aborted TCP")
        error_log = open('error_log.txt','a')
        error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
        error_log.close()
        s.connect((TCP_IP, TCP_PORT))
    elif ord(q)==115:#s
      try:
        Packet.SendPacket(s,1)
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==104:#h
      data = [0x01]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
      for i in range(11):
        data.append(90+i)
        data.append(0)
      PacketAll = RTM_MW(data)
      PacketAll.SendPacket(ser,0)

    elif ord(q)==108:#l
      while(1):
        try:
          Packet.SendPacket(s,1)
        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
          except TimeoutError:
            print (time.asctime())
            print ("mega12 not TCP connected ")
            error_log = open('error_log.txt','a')
            error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
            error_log.close()
          except ConnectionAbortedError:
            print (time.asctime())
            print ("mega12 connect aborted TCP")
            error_log = open('error_log.txt','a')
            error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
            erro_log.close()
            s.connect((TCP_IP, TCP_PORT))
        print (time.asctime())
        time.sleep(0.1)
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)

    elif ord(q)==116:#t
      CRC = crc16(MdbKskn[0:6],6)
      MdbKskn[6]=(CRC&0xFF)
      MdbKskn[7]=((CRC>>8)&0xFF)
      print (MdbKskn[0:8])
      ser.write(MdbKskn)

    elif ord(q)==102:#f
      mdbtcp_s=bytearray(cmd_fr[0:])
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(4)
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      kerneltime = (data[9]<<8|data[10])/10
      print(data)
      print(time_pr,'ms')
  #        sys.stderr.write(cmd_mdb)
class RTM_MW(object):
  def __init__(self,Data):
    self.Kod = 250
    self.Len = [0x00,0x00]
    self.RetranNum = 1
    self.Flag = 0x02
    self.MyAdd = [7,0,0]
    self.Chan = 1
    self.MyAdd[2] = 0x01
    self.DestAdd = [12,0x0,0x00]
    self.DestAdd[2] = 5
#    self.DestAddEnd = [8,0,0x00]
    self.DestAddEnd = [0xeb,0x03,0]
#    self.DestAddEnd = [202,0x00,0]
    self.DestAddEnd[2] = 5
    self.Tranzaction  = 1
    self.PacketNumber = 1
    self.PacketItem   = 1
    self.Instruction  = 1
    self.Data=Data
    self.Errorcnt = 0
    self.OkReceptionCnt = 0

  def SendPacket(self,s,type):
    BUFFER_SIZE = 1024
    Packet = [self.Kod]
    Packet.append(self.Len[0])
    Packet.append(self.Len[1])
    Packet.append(self.RetranNum)
    Packet.append(self.Flag)
    Packet.append(self.MyAdd[0])
    Packet.append(self.MyAdd[1])
    Packet.append(self.MyAdd[2])
    Packet.append(self.DestAdd[0])
    Packet.append(self.DestAdd[1])
    Packet.append(self.DestAdd[2])
    Packet.append(self.DestAddEnd[0])
    Packet.append(self.DestAddEnd[1])
    Packet.append(self.DestAddEnd[2])
    Packet.append(self.Tranzaction)
    Packet.append(self.PacketNumber)
    Packet.append(self.PacketItem)
    for i in range(0,len(self.Data)):
      Packet.append(self.Data[i])
    lenght = len(Packet)
    lenght+=2
    self.Len[0] = lenght&0xFF 
    self.Len[1] = (lenght>>8)&0xFF
    Packet[1] = self.Len[0]
    Packet[2] = self.Len[1]
    CRC = RTM64CRC16(Packet, len(Packet))
    Packet.append(CRC&0xFF)
    Packet.append((CRC>>8)&0xFF)
    if (type == 1):
      Packet_str = bytearray(Packet[0:])
      print(Packet_str)
      time_start=time.time()
      s.send(Packet_str)
      s.settimeout(1)
#data = s.recvfrom(BUFFER_SIZE)
      try:
        data = s.recv(BUFFER_SIZE)
        self.OkReceptionCnt+=1
        time_pr=time.time() - time_start
  #    data = char_to_int(data_s,len(data_s))
        print (data,self.OkReceptionCnt)
        print(time_pr,'s')
        print(len(data))
      except socket.timeout:
        self.Errorcnt+=1
        print("TCP_RecvError",self.Errorcnt)
        print (time.asctime())
        error_log = open('error_log.txt','a')
        error_log.write ("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
        error_log.close()
    elif(type == 0):
      print(Packet)
      s.write(Packet)


    

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
    main()
