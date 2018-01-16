#!/c/Python33/ python
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
import random

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt
#def hextoascii():
def big_to_little(packet):
  for i in range(len(packet)//2):
    temp = packet[2*i]
    packet[2*i] = packet[2*i+1]
    packet[2*i+1] = temp
  

def main():
  have_serial = 1
#  devpy.color_traceback()
#  log = devpy.autolog() # log is a regular stdlib logger object
#  log.info('Yes')
  hello = 'hello'
  mdbtcp = [0x00,0x03,0x00,0x00,0x00,0x04]#,6,3,0x00,0x3,0x00,1]#,0x04,0x04,0x21,0x05,0x00]
  mdb_address = 3
  mdb_command = 3
  start_address = 0
  reg_numm = 2
  data = [0x000f,0x000f]  #u16 format u16
  mdbtcp.append(mdb_address)
  mdbtcp.append(mdb_command)
  mdbtcp.append((start_address>>8)&0xff)
  mdbtcp.append(start_address&0xff)
  if mdb_command == 3 or mdb_command == 4 or mdb_command == 1:
    mdbtcp.append((reg_numm>>8)&0xff)
    mdbtcp.append(reg_numm&0xff)
  elif mdb_command == 16:
    reg_numm = len(data)&0xffff
    reg_numm_bytes = reg_numm*2
    mdbtcp.append((reg_numm>>8)&0xff)
    mdbtcp.append(reg_numm&0xff)
    mdbtcp.append(reg_numm_bytes&0xff)
    for i in range(reg_numm):
      mdbtcp.append((data[i]>>8)&0xff)
      mdbtcp.append(data[i]&0xff)

  elif mdb_command == 6:
    mdbtcp.append((data[0]>>8)&0xff)
    mdbtcp.append(data[0]&0xff)
  else:
    print('command not responde')
  print(mdbtcp)

  count = 0
  TCP_IP = '172.16.1.3'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  good_transaction = 0
  bad_transaction = 0
  itt=0

  print ('c - tcp connect\n'
         't - mdbtcp send(after connect)\n'
         'm - modbus RTU send over uart(open auto)\n')  
  while 1:
#    if msvcrt.kbhit():
    q = msvcrt.getch()
    print(ord(q))
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==119:#w
      print(mdbwrite)
      ser.write(mdbwrite)
    elif ord(q)==99:#c
      s.connect((TCP_IP, TCP_PORT))
    elif ord(q)==116:#t
#      mdbtcp[0] =  random.randint(0, 255)
      mdbtcp_s = bytearray(mdbtcp[0:])
      print(mdbtcp[0:])
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(7)
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      data_s =[]
      print(data)
      for i in range(0,len(data)):
        data_s.append(data[i])
#      arc_parse(data_s[9:])
      parse_mdb_tcp_response(data_s)
      print(data_s)
      print("lenght",len(data_s))
      print(time_pr,'ms')

    elif ord(q)==108:#l
      while(1):
        try:
          mdbtcp_s = bytearray(mdbtcp[0:])
          sys.stdout.write(str(mdbtcp[0:]))
          s.send(mdbtcp_s)
          time_start=time.time()
          s.settimeout(4)
          data = s.recv(BUFFER_SIZE)
          good_transaction+=1
          time_pr=time.time() - time_start
          data_s =[]
          for i in range(0,len(data)):
            data_s.append(data[i])
          if data_s:
            if ChekErrorPacket(data_s):
              bad_transaction+=1
          os.system('cls' if os.name == 'nt' else 'clear')
          sys.stdout.write('\r'+"\\")
          sys.stdout.write(str(data_s)+'\n')
          sys.stdout.write("lenght"+str(len(data_s))+'\n')
          sys.stdout.write(str(time_pr)+'ms'+'\n')
          sys.stdout.write('transaction sum'+str(good_transaction)+'\n')
          sys.stdout.write('error transaction sum'+str(bad_transaction)+'\n')

        except OSError:
          bad_transaction+=1
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
        time.sleep(0.2)
        if(msvcrt.kbhit()):
          q = msvcrt.getch()
          print(ord(q))
          if ord(q) == 113:#q
            s.close()
            sys.exit(1)
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
