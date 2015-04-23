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
import struct

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
      error_log = open('recv_log.txt','a')
      if(ord(hello)==250):
        error_log.write ('\n')
      error_log.write (str(hello))
      error_log.close()
      print(hello,ord(hello))

KodBit =	0x00
KodInt8 =	0x20
KodInt16 =	0x40
KodInt32 =	0x60
KodFloat32 =	0x80
KodTime32 =	0xA0
ValTypeName = {KodBit:"KodBit",
           KodInt8 :"KodInt8",
           KodInt16 :"KodInt16",
           KodInt32 :"KodInt32",
           KodFloat32 :"KodFloat32",
           KodTime32 :"KodTime32"
}
ValType = {KodBit:1,
           KodInt8 :1,
           KodInt16 :2,
           KodInt32 :4,
           KodFloat32 :4,
           KodTime32 :4
}

def main():
  ser = serial.Serial(1)  # open first serial port
  ser.baudrate = 115200;
  print (ser.name)          # check which port was really used
  try:
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial0.SerialException as e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)
  hello = 'hello'

  ser.write(serial.to_bytes([4]))
  cmd_en = 0  #                    command  &rotor    &mega1   &megafinaly modbuss
#         0    1    2     3   4     5     6   7   8     9   10    11  12    13  14  15    16    17  18
  cmd = [0x7E,0x03,0xF0,0x16,0x02,0x46,0x52,0xA0,0x8F,0x03,0x70,0x21,0x02,0x03,0x03,0x00,0x80,0x00,0x01]
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
  TCP_IP = '192.168.1.242'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  MESSAGE = "Hello, World!"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  a = 0
  thread.start_new_thread(ComList, (ser,a ))
  print ('tread is start')
  data = [2,37,0]#,81,0,82,0,100,0]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
  data_p = [1,0,1]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
  Packet = RTM_MW(data)  

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
      if Packet:
        del(Packet)
 
    elif ord(q)==97:#a
      Packet.SendPacket(ser,0)
    elif ord(q)==43:#+
      data_p[1] += 1
      Packet_p = RTM_MW(data_p)
      Packet_p.connect(TCP_IP, TCP_PORT)
      try:
        Packet_p.SendPacket(ser,1)
      except OSError:
        print ("Can't send tcp Packet")

    elif ord(q)==99:#c
      Packet.connect(TCP_IP, TCP_PORT)
    elif ord(q)==115:#s
      try:
        Packet.Send()
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
          Packet.SendPacket(ser,1)
        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log_rv.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            erro_log.close()
            s.connect((TCP_IP, TCP_PORT))
        print (time.asctime())
        time.sleep(0.02)
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
  def __init__(self,Data):
    self.Kod = 250
    self.Len = [0x00,0x00]
    self.RetranNum =0
    self.Flag = 0x0
    self.MyAdd = [7,0,0]
    self.MyAdd[2] = 0x02
    self.DestOne = [8,0,2]
    self.DestTwo =  [200,0,2]
    self.DestThree = [200,0,5]

    self.TranzactionSend  = 1
    self.PacketNumber = 1
    self.PacketItem   = 1
    self.Instruction  = 1
    self.Data=Data
    if self.Data:
      self.Instruction = self.Data[0]
      self.Ind = []
      self.IndNum = 0
      for i in range(0,(len(self.Data)-1)>>1):
        self.IndNum +=1 
        self.Ind.append(self.Data[2*i+1]|(self.Data[2*i+2]<<8))
    self.IndRecv = 0
    self.Type = [0x00 for x in range(64)]
    self.GUID = 0x0000
    self.LenName = 0x00
    self.Name = []
    self.LenIntName = 0x00
    self.IntName = []
    self.ArraySize = [0x00000 for x in range(64)]
    self.Value = []
    self.Flag = 0    
    self.Errorcnt = 0
    self.OkReceptionCnt = 0
    self.CheckCRC = 0
  def __del__(self):
    if self.s:
      self.s.close()
    print("dlt packet")
  def SendPacket(self,ser,type):
    BUFFER_SIZE = 1024
    Packet = [self.Kod]
    Packet.append(self.Len[0])
    Packet.append(self.Len[1])
    Packet.append(self.RetranNum)
    Packet.append(self.Flag)
    Packet.append(self.MyAdd[0])
    Packet.append(self.MyAdd[1])
    Packet.append(self.MyAdd[2])
    Packet.append(self.DestOne[0])
    Packet.append(self.DestOne[1])
    Packet.append(self.DestOne[2])
    if (self.RetranNum > 0):
      Packet.append(self.DestTwo[0])
      Packet.append(self.DestTwo[1])
      Packet.append(self.DestTwo[2])
      if (self.RetranNum > 1):
        Packet.append(self.DestThree[0])
        Packet.append(self.DestThree[1])
        Packet.append(self.DestThree[2])

    Packet.append(self.TranzactionSend)

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
      self.s.send(Packet_str)
      error_log = open('error_log_rv.txt','a')
      error_log.write (str(Packet_str))
      error_log.close()


      self.s.settimeout(2)
#data = s.recvfrom(BUFFER_SIZE)
      try:
        data = self.s.recv(BUFFER_SIZE)
        self.OkReceptionCnt+=1
        time_pr=time.time() - time_start
#        data = char_to_int(data,len(data))
        data_s =[]
        print(data)
        for i in range(0,len(data)):
          data_s.append(data[i])
        print(data_s,self.OkReceptionCnt)
        if data_s:
          self.ChekPacket(data_s)
          if self.CheckCRC:
            if (len(self.DataInPacket)>1):
              self.HandPacket(self.DataInPacket)
            else:
              print ("empty packet")
          else:
            print('CRC_ERROR')
            error_log = open('error_log_rv.txt','a')
            error_log.write ("CRC_ERROR"+time.asctime()+str(self.Errorcnt)+'\n')
            error_log.close()

        print(time_pr,'s')
        print(len(data))
      except socket.timeout:
        self.Errorcnt+=1
        print("TCP_RecvError",self.Errorcnt)
        print (time.asctime())
        error_log = open('error_log_rv.txt','a')
        error_log.write ("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
        error_log.close()
    elif(type == 0):
      print(Packet)
      ser.write(Packet)
  def HandPacket(self,DataVal):
    if DataVal:
      if self.Instruction == 1:
        k = 1
#        print(DataVal)
        for i in range(0,self.IndNum):
          self.IndRecv = DataVal[k]|(DataVal[1+k]<<8)
          k+=2
          print("IndexRecv = ",self.IndRecv,"IndWrite = ",self.Ind[i])
          self.Type[i] = DataVal[k]
          k+=1
          print("Valtype = ",ValTypeName[self.Type[i]])
          self.GUID = DataVal[k]|(DataVal[k+1]<<8)
          k+=2
          print("GUID = ",self.GUID)
          self.LenName = DataVal[k]
          k+=1
          self.Name = DataVal[k:k+self.LenName] 
          Name = ''
          for l in range(self.LenName):
            Name+=(chr(self.Name[l]))
          #Name = ascii(self.Name)
          k +=self.LenName
          print ("Name = ",Name.encode('cp1252'))
          self.LenIntName = DataVal[k]
          k+=1
          self.IntName = DataVal[k:k+self.LenIntName]
          k +=self.LenIntName
          InName = ''
          for l in range(self.LenIntName):
            InName+=(chr(self.IntName[l]))

          print("IntName = ",InName.encode('cp1252'))
          self.ArraySize[i] = DataVal[k]|(DataVal[k+1]<<8)
          k+=2
          print ("ArraySize = ",self.ArraySize[i])
          self.Value = [0 for x in range(self.ArraySize[i])]
          for x in range (0,self.ArraySize[i]):
            for y in range (0,ValType[self.Type[i]]):
              self.Value[x] |= DataVal[k]<<(8*y)
              #print(x,k)
              k +=1
          print("Value = ",self.Value)
          self.FlagRecv = DataVal[k]
          k+=1
          print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
      elif self.Instruction == 2:
        k = 1
        flo32 = [0.0 for x in range(self.IndNum)]
        for i in range(0,self.IndNum):
          self.Value = [0 for x in range(self.ArraySize[i])]
          for x in range (0,self.ArraySize[i]):
            for y in range (0,ValType[self.Type[i]]):
              self.Value[x] |= DataVal[k]<<(8*y)
              k +=1
            if self.Type[i] == KodFloat32:
              flo32[x] = struct.pack('I',self.Value[x])
          if self.Type[i] == KodFloat32:
            print("Value = ",struct.unpack('f',flo32[0]))
          else:
            print("Value = ",self.Value)
          print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
  def connect(self,TCP_IP, TCP_PORT):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
      self.s.connect((TCP_IP, TCP_PORT))
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
      self.s.connect((TCP_IP, TCP_PORT))

  def ChekPacket(self,data):
    str_buf = ''
    [250, 19, 0, 0, 3, 7, 0, 1, 5, 0, 130, 228, 1, 1, 2, 5, 0, 8, 19]
    i = 0
    if (data[i] != self.Kod):
      str_buf = 'Kod_error'+'\t'
    i +=1
    lenght = data[i]|data[i+1]<<8
    i +=2
    if (lenght!= len(data)):
      str_buf+='lenght_Error'+'\t'
    i +=1#retrannum
    i +=1#flag
    if (self.MyAdd[0] !=data[i] or self.MyAdd[1]!=data[i+1] or self.MyAdd[2]!=data[i+2]):
      str_buf+='MyAddr_Error'+'\t'
    i +=3
    if (self.DestOne[0] !=data[i] or self.DestOne[1]!=data[i+1] or (self.DestOne[2]|0x80)!=data[i+2]):
      str_buf+='DestAddr_Error'+'\t'
    i +=3
    if (self.RetranNum > 0):
      if (self.DestTwo[0] !=data[i] or self.DestTwo[1]!=data[i+1] or (self.DestTwo[2]|0x80)!=data[i+2]):
        str_buf+='DestAddr_Error'+'\t'
      i +=3
      if(self.RetranNum > 1):
        if (self.DestThree[0] !=data[i] or self.DestThree[1]!=data[i+1] or (self.DestThree[2]|0x80)!=data[i+2]):
          str_buf+='DestAddr_Error'+'\t'
        i +=3


    if (self.TranzactionSend != data[i]):
      str_buf+='TranzactionSend_Error'+'\t'
    i +=1
    self.PacketNumberRecv = data[i]
    if (self.PacketNumber != data[i]):
      str_buf+='PacketNumber_Error'+'\t'
    i +=1
    self.PacketItemRecv = data[i] 
    if (self.PacketItem != data[i]):
      str_buf+='PacketItem_Error'+'\t'
    i +=1
    self.DataInPacket = data[i:len(data)-2]
    i += len(self.DataInPacket)
    CRC = RTM64CRC16(data, len(data)-2)
    CRCin = data[i]|data[i+1]<<8
    if(CRC != (CRCin)):
      str_buf+='CRC_Error'
      self.CheckCRC = 0
    else:
      self.CheckCRC = 1
    return str_buf
  def Send(self):
    self.Data[0] = 1
    self.Instruction  = 1
    self.SendPacket(self.s,1);
#    time.sleep(3)
    self.Data[0] = 2
    self.Instruction  = 2
    self.SendPacket(self.s,1);
    

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
