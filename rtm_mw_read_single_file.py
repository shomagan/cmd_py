#!/c/Python33/ python
import sys
import msvcrt
import os
import _thread as thread, threading,socket,atexit,io,serial,time
import struct
KodBit =  0x00
KodInt8 = 0x20
KodInt16 =  0x40
KodInt32 =  0x60
KodFloat32 =  0x80
KodTime32 = 0xA0
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

sended = 0
reconect = 0
def main():
  print('helo')
  TCP_IP_1 = '172.16.1.3'
  TCP_PORT = 502
  data = [1,143,0]#,145,0,146,0]#141,0,142,0,143,0,140,0,139,0,138,0,137,0,136,0]#,152,0,150,0]#103,0,104,105,0,106,0,107,0,108,0,109,0,110,0,111,0,112,0,113,0,114,0,115,0,116,0,117,0]#,116,0,117,0]
  Packet_1 = RTM_MW(data)
  Packet_1.RetranNum = 0
  Packet_1.DestOne = [3,0,4]
  Packet_1.DestTwo = [3,0,5]
  Packet_1.DestThree = [4,0,0]
  global sended
  global reconect
  sended = reconect= 0
  while 1:
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      del Packet
      sys.exit(1)
    elif ord(q)==99:#c
      Packet_1.connect(TCP_IP_1, TCP_PORT)
    elif ord(q)==115:#s
      try:
        Packet_1.Send(1)
        Packet_1.Send(2)
      except OSError:
        print ("Can't send tcp Packet")
    elif ord(q)==108:#l
      Packet_1.Send(1)
      while(1):
        try:
          Packet_1.Send(2)
        except OSError:
          print ("Can't send tcp Packet")
          error_log = open('error_log_rv.txt','a')
          error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
          error_log.close()
          try:
            Packet_1.s.close()
            reconect+=1
            Packet_1.connect(TCP_IP_1, TCP_PORT)
            Packet_1.Send(1)
          except TimeoutError:
            print(time.asctime())
            print("mega12 not TCP connected ")
            error_log = open('error_log_rv.txt','a')
            error_log.write ("mega12 not TCP connected "+time.asctime()+'\n')
            error_log.close()
          except ConnectionAbortedError:
            print(time.asctime())
            print("mega12 connect aborted TCP")
            error_log = open('error_log_rv.txt','a')
            error_log.write ("mega12 connect aborted TCP"+time.asctime()+'\n')
            erro_log.close()
            reconect+=1
            Packet_1.s.close()
            Packet_1.connect(TCP_IP_1, TCP_PORT)
            Packet_1.Send(1)
        time.sleep(0.250)
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)

          
        '''  sys.stdout.write('\r'+"\\")
          sys.stdout.write(str(data_s)+'\n')
          sys.stdout.write("lenght"+str(len(data_s))+'\n')
          sys.stdout.write(str(time_pr)+'ms'+'\n')
          sys.stdout.write('transaction sum'+str(good_transaction)+'\n')
          sys.stdout.write('error transaction sum'+str(bad_transaction)+'\n')
        '''

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


class RTM_MW(object):
  def __init__(self,Data):
    self.Kod = 250
    self.Len = [0x00,0x00]
    self.RetranNum =0
    self.Flag = 0x0
    self.MyAdd = [7,0,2]
    self.DestOne = [3,0,5]
    self.DestTwo =  [13,0,7]
    self.DestThree = [200,0,5]
    self.DestFor = [200,0,5]
    self.TranzactionSend  = 52
    self.PacketNumber = 1
    self.PacketItem   = 1
    self.Data=Data
    if self.Data:
      self.Instruction = self.Data[0]
      self.Ind = []
      self.IndNum = 0
      for i in range(0,(len(self.Data)-1)>>1):
        self.IndNum +=1 
        self.Ind.append(self.Data[2*i+1]|(self.Data[2*i+2]<<8))
    self.IndRecv = 0
    self.Type = [0x00 for x in range(200)]
    self.GUID = 0x0000
    self.LenName = 0x00
    self.Name = []
    self.LenIntName = 0x00
    self.IntName = []
    self.ArraySize = [0x00000 for x in range(200)]
    self.Value = []
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
        if (self.RetranNum > 2):
          Packet.append(self.DestFor[0])
          Packet.append(self.DestFor[1])
          Packet.append(self.DestFor[2])

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
    data_s =[]
    if (type == 1):
      Packet_str = bytearray(Packet[0:])
      time_start=time.time()
      self.s.send(Packet_str)
      self.s.settimeout(4)
      try:
        data = self.s.recv(BUFFER_SIZE)
        self.OkReceptionCnt+=1
        time_pr=time.time() - time_start
        for i in range(0,len(data)):
          data_s.append(data[i])
        if data_s:
          self.ChekPacket(data_s)
          if self.CheckCRC:
            if (len(self.DataInPacket)>1):
              self.HandPacket(self.DataInPacket)
            else:
              print("not empty packet")
            print(data_s)
          else:
            print('CRC_ERROR')
            error_log = open('error_log_rv.txt','a')
            error_log.write ("CRC_ERROR"+time.asctime()+str(self.Errorcnt)+'\n')
            error_log.close()
        
      except socket.timeout:
        self.Errorcnt+=1
        print("TCP_RecvError",self.Errorcnt)
        print (time.asctime())
        error_log = open('error_log_rv.txt','a')
        error_log.write ("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
        error_log.close()
    elif(type == 0):
      error_log = open('error_log_rv.txt','a')
      error_log.write (str(Packet))
      error_log.close()
      ser.write(Packet)
    return (data_s)
  def HandPacket(self,DataVal):
    if DataVal:
      os.system('cls' if os.name == 'nt' else 'clear')
      if self.Instruction == 1:
        k = 1
        for i in range(0,self.IndNum):
          self.IndRecv = DataVal[k]|(DataVal[1+k]<<8)
          if (self.IndRecv!=self.Ind[i]):
            break
          else:
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
                if self.Type[i] == KodBit:
                  self.Value[x] = DataVal[k]&0x01
                else:
                  self.Value[x] |= DataVal[k]<<(8*y)
                #print(x,k)
                k +=1
            print("Value = ",(self.Value))
            self.FlagRecv = DataVal[k]
            k+=1
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
      elif self.Instruction == 2:
        global sended
        global reconect
        k = 1
        flo32 = [0.0 for x in range(self.IndNum)]
        for i in range(0,self.IndNum):
          self.Value = [0 for x in range(self.ArraySize[i])]
          for x in range (0,self.ArraySize[i]):
            for y in range (0,ValType[self.Type[i]]):
              if self.Type[i] == KodBit:
                self.Value[x] = DataVal[k]&0x01
              else:
                self.Value[x] |= DataVal[k]<<(8*y)
              k +=1
            if self.Type[i] == KodFloat32:
              flo32[x] = struct.pack('I',self.Value[x])
          if self.Type[i] == KodFloat32:
            print("Value = ",struct.unpack('f',flo32[0]))
          else:
#            bar = (self.Value[0] - 800)/(4036 - 800)
#            bar = bar*6
#            print("pressure bar = ",bar)
            print("Value = ",self.Value,'hex',hex(self.Value[0]))

          print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        sended+=1
        print ("Sended packet=", sended)
        print ("reconect number=", reconect)
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
  def close_tcp_connect(self):
      self.s.close()


  def ChekPacket(self,data):
    str_buf = ''
    [250, 19, 0, 0, 3, 7, 0, 1, 5, 0, 130, 228, 1, 1, 2, 5, 0, 8, 19]
    i = 0
    self.CheckCRC = 0

    if (data[i] != self.Kod):
      str_buf = 'Kod_error'+'\t'
    else:
      i +=1
      if (len(data)>3):
        lenght = data[i]|data[i+1]<<8
      else:
        lenhgt = 0
      i +=2
      if (lenght!= len(data)):
        str_buf+='lenght_Error'+'\t'
      else:
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
            if(self.RetranNum > 2):
              if (self.DestFor[0] !=data[i] or self.DestFor[1]!=data[i+1] or (self.DestFor[2]|0x80)!=data[i+2]):
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
  def Send(self,instruction):
    self.Data[0] = instruction
    self.Instruction  = instruction
    self.SendPacket(self.s,1);

if __name__ == "__main__":
    main()


