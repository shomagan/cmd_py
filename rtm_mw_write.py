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
"""
FB_MODBUS_Buffer[0] = IN->MODBUS_Addr.Data.uint8;     
FB_MODBUS_Buffer[1] = IN->MODBUS_Func.Data.uint8;     
FB_MODBUS_Buffer[2] = IN->RegAddr.Data.uint16 >> 8;   
FB_MODBUS_Buffer[3] = IN->RegAddr.Data.uint16 & 0xFF; 
FB_MODBUS_Buffer[4] = IN->RegNum.Data.uint16 >> 8;    
FB_MODBUS_Buffer[5] = IN->RegNum.Data.uint16 & 0xFF;  
CRC = crc16(FB_MODBUS_Buffer, LengthPak-2);
FB_MODBUS_Buffer[LengthPak-2] = (char)CRC;
FB_MODBUS_Buffer[LengthPak-1] = (char)(CRC>>8);
"""
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
  try:
    ser = serial.Serial('COM6')  # open first serial port
    ser.baudrate = 9600;
    print (ser.name)          # check which port was really used

    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
    ser.write(serial.to_bytes([4]))
    a = 0
    if(ser):
      thread.start_new_thread(ComList, (ser,a ))

  except serial.SerialException as e:
    sys.stderr.write("could not open port ")

  hello = 'hello'




  cmd_en = 0  #                    command  &rotor    &mega1   &megafinaly modbuss
#         0    1    2     3   4     5     6   7   8     9   10    11  12    13  14  15    16    17  18
  cmd = [0x7E,0x03,0xF0,0x16,0x02,0x46,0x52,0xA0,0x8F,0x03,0x70,0x21,0x02,0x05,0x03,0x00,0x00,0x00,0x01]
#  cmd = [0x7E,0x02,0xF0,0x14,0x02,0x46,0x52,0x03,0x70,0x21,0x02,0x03,0x03,0x00,0x1E,0x00,0x01]
  Cmd_NI =   [0x7E,0x02,0xF0,0x0F,0x00,0x4E,0x49,0xA0,0x8F,0x03,0x00,0x01,0x00,0x06]
  mdbtcp = [0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x03,0x00,0x80,0x00,0x06]
  cmd_FR_T = [0x7E,0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0x03,0x00,0x04]  
  ChekSum = RTM64ChkSUM(cmd_FR_T[1:] , len(cmd_FR_T)-1)
  cmd_FR_T.append(ChekSum&0xFF)
  cmd_FR_T.append((ChekSum>>8)&0xFF)
  cmd_FR_T.append(0x7e)
  ChekSum = RTM64ChkSUM(Cmd_NI[1:] , len(Cmd_NI)-1)
  Cmd_NI.append(ChekSum&0xFF)
  Cmd_NI.append((ChekSum>>8)&0xFF)
  Cmd_NI.append(0x7E)

#            7E 03   F0   16   00    4D  42    E8   83   B5  7F    21   02   01   03   00  01    00    01 D5 CA FF 05 7E
  CRC = crc16(cmd[-6:],6)
  Buff= [0x7E, 0x02, 0xF0, 0x0C, 0x00, 0x56, 0x4D, 0x03, 0x80, 0x05, 0x00 ]
  ChekSum = RTM64ChkSUM(Buff[1:] , len(Buff)-1)
  Buff.append(ChekSum&0xFF)
  Buff.append((ChekSum>>8)&0xFF)
  print_hex (Buff,len(Buff))
  cmd.append(CRC&0xFF)
  cmd.append((CRC>>8)&0xFF)
  ChekSum = RTM64ChkSUM(cmd[1:] , len(cmd)-1)
  cmd.append(ChekSum&0xFF)
  cmd.append((ChekSum>>8)&0xFF)
  cmd.append(0x7E)
  print_hex (cmd,len(cmd))
#  print (int_to_char(cmd))
  cmd_fr =[0x03,0xF0,0x11,0x00,0x46,0x52,0xA0,0x8F,0x03,0x70,0x05,0x00,0x10,0x01,0x02]
  cmd_vm = [0x02,0xF0,0x0C,0x00,0x56,0x4D,0xA0,0x8F,0x03,0x00]
  cmd_four = [0xAE,0x08,0x18,0x28]
  cmd_fs = [0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0x28,0x01,0x02]
  cmd_s = [0 for x in range(100)]
  count = 0
#  print (RTM64ChkSUM(cmd_fs , 13))
#  print (0x02f6)
  TCP_IP = '192.168.2.237'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  MESSAGE = "Hello, World!"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  crc = [2,230]
  crc = [146,141]
  sp_write = [19,0,0xb4,0x14]
  data = [2,6,0,19,0]#,81,0,82,0,100,0]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
  data_w = [3,6,0,crc[0],crc[1]]+sp_write
  Packet = RTM_MW(data,RetranNum = 0,Chan = 4,DestAdd1 = 3,Chan1 = 4,DestAdd2 = 3,Chan2 = 5)
  Packet.Chan = 0x01

  while 1:
#    if msvcrt.kbhit():
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==119:#w
      Packet_w = RTM_MW(data_w,RetranNum = 0,Chan = 4,DestAdd1 = 3,Chan1 = 4,DestAdd2 = 3,Chan2 = 5)
      Packet_w.SendPacket(s,1)
      del(Packet_w)
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
      try:
        Packet_p.SendPacket(s,1)
      except OSError:
        print ("Can't send tcp Packet")

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
      mdbtcp_s=bytearray(mdbtcp[0:])
      print(mdbtcp_s)
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(4)
      data = s.recv(BUFFER_SIZE)
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
  def __init__(self,Data,RetranNum = 0,Chan = 8,DestAdd1 = 3,Chan1 = 1,DestAdd2 = 4,Chan2 = 5):
    self.Kod = 250
    self.Len = [0x00,0x00]
    self.RetranNum = RetranNum
    self.Flag = 0x02
    self.MyAdd = [8,0,Chan]
    self.DestAdd = [DestAdd1&0xff,((DestAdd1>>8)&0xff),Chan1]
    self.DestAddEnd = [DestAdd2&0xff,((DestAdd2>>8)&0xff),Chan2]
#    self.DestAddEnd = [0xeb,0x03,0]
#    self.DestAddEnd = [202,0x00,0]
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
    if self.RetranNum==1:
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
      print(Packet)
      Packet_str = bytearray(Packet[0:])
      time_start=time.time()
      s.send(Packet_str)
      s.settimeout(1)
#data = s.recvfrom(BUFFER_SIZE)
      try:
        data = s.recv(BUFFER_SIZE)
        self.OkReceptionCnt+=1
        time_pr=time.time() - time_start
#        data = char_to_int(data,len(data))
        data_s =[]
        for i in range(0,len(data)):
          data_s.append(data[i])
        print(data_s,self.OkReceptionCnt)
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
