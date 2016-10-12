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
import sys, os, _thread as thread, threading,socket,atexit,io,time

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt
BUFFER_SIZE = 1024
#def hextoascii():
def ComList(ser):
  while(1):
    hello = ser.read(1)
    if (hello != ''):
      #print(char_to_int(hello,len(hello)))
      print(ord(hello))
class Mdb(object):
  def __init__(self,
                mdb_address = 5,
                mdb_command = 3,
                mdb_start_address = 0,
                mdb_reg_numm = 4,
                mdb_data = [0x0005]):
    self.mdbtcp = [0x00,0x03,0x00,0x00,0x00,0x04]#,6,3,0x00,0x3,0x00,1]#,0x04,0x04,0x21,0x05,0x00]
    self.mdb_address = 5
    self.mdb_command = 3
    self.mdb_start_address = 0
    self.mdb_reg_numm = 4
    self.mdb_data = [0x0005]
    self.count = 0
    self.good_transaction = 0
    self.bad_transaction = 0

  def send(self,s_socket,log,timeout = 6,parse=0):
    mdbtcp = []
    mdbtcp = [self.mdbtcp[i] for i in range(len(self.mdbtcp)) ]
    mdbtcp.append(self.mdb_address)
    mdbtcp.append(self.mdb_command)
    mdbtcp.append((self.mdb_start_address>>8)&0xff)
    mdbtcp.append(self.mdb_start_address&0xff)
    if self.mdb_command == 3 or self.mdb_command == 4:
      mdbtcp.append((self.mdb_reg_numm>>8)&0xff)
      mdbtcp.append(self.mdb_reg_numm&0xff)
    elif self.mdb_command == 16:
      self.reg_numm = len(self.mdb_data)&0xffff
      self.reg_numm_bytes = self.mdb_reg_numm*2
      mdbtcp.append((self.mdb_reg_numm>>8)&0xff)
      mdbtcp.append(self.mdb_reg_numm&0xff)
      mdbtcp.append(self.mdb_reg_numm_bytes&0xff)
      for i in range(self.mdb_reg_numm):
        mdbtcp.append((self.mdb_data[i]>>8)&0xff)
        mdbtcp.append(self.mdb_data[i]&0xff)
    elif self.mdb_command == 6:
      mdbtcp.append((self.mdb_data[0]>>8)&0xff)
      mdbtcp.append(self.mdb_data[0]&0xff)
    else:
      log.write ('command not responde')
      print('command not responde')
    s = s_socket
    mdbtcp_s = bytearray(mdbtcp[0:])
    time_start=time.time()
    s.settimeout(timeout)
    s.send(mdbtcp_s)
    data_s =[]
    try:
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      for i in range(0,len(data)):
        data_s.append(data[i])
      if data_s:
        if parse:
          parse_mdb_tcp_response(data_s)
        log.write ('receive mb packet'+str(data_s) + '\n')

    except socket.timeout:

      print (time.asctime())
      error_log = open('error_log_rv.txt','a')
      error_log.write ("TCP_RecvError"+time.asctime()+'\n')
      error_log.close()
    return data_s


def parse_mdb_tcp_response(packet):
  parse_mdb_response(packet[6:])
  return


def parse_mdb_response(packet):
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

  
def ChekErrorPacket(data):
  if len(data)==9:
    print(data[-3:-1])
    if data[-2]==132:
      return 1
  return 0
  #        sys.stderr.write(cmd_mdb)
def RTM64CRC16(pbuffer , Len):
  """CRC16 for RTM64"""
  CRC = 0x0000
  k = 0
  while (k < Len):
    CRC = (CRC^(((pbuffer[k])<<8)&0xFFFF))
    k+=1
    i=8
    while (i):
      i-=1
      if (CRC & 0x8000): CRC = (((CRC<<1)&0xFFFF)^0x1021)
      else: CRC = ((CRC<<1)&0xFFFF)
  return CRC
def crc16(pck,lenght):
  """CRC16 for modbus"""
  CRC = 0xFFFF
  i = 0
  while ( i < lenght):
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
