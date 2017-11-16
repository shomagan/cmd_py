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
  
def arc_parse(packet):
  print(packet,'\n')

  if len(packet) == 54:
    print('len data packet 54 \n')
    big_to_little(packet)
    print(packet)
    otv_start = packet[0]
    print('otv start',otv_start,'\n')
    otv_end = packet[1]
    print('otv end',otv_end,'\n')
    start_time = packet[2]|(packet[3]<<8)|(packet[4]<<16)|(packet[5]<<24)
    print('start_time',start_time,'\n')
    flo32 = 0.0 
    value = packet[6]|(packet[7]<<8)|(packet[8]<<16)|(packet[9]<<24)
    flo32 = struct.pack('I',value)
    Summ_Mass_Liquid = struct.unpack('f',flo32)
    print("Summ_Mass_Liquid ",Summ_Mass_Liquid,'\n')
    value = packet[10]|(packet[11]<<8)|(packet[12]<<16)|(packet[13]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Liquid = struct.unpack('f',flo32)
    print("Mass_FlowRate_Liquid ",Mass_FlowRate_Liquid,'\n')
    value = packet[14]|(packet[15]<<8)|(packet[16]<<16)|(packet[17]<<24)
    flo32 = struct.pack('I',value)
    Volume_FlowRate_Gas = struct.unpack('f',flo32)
    print("Volume_FlowRate_Gas ",Volume_FlowRate_Gas,'\n')

    value = packet[18]|(packet[19]<<8)|(packet[20]<<16)|(packet[21]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Oil = struct.unpack('f',flo32)
    print("Mass_FlowRate_Oil ",Mass_FlowRate_Oil,'\n')

    value = packet[22]|(packet[23]<<8)|(packet[24]<<16)|(packet[25]<<24)
    flo32 = struct.pack('I',value)
    Mass_FlowRate_Water = struct.unpack('f',flo32)
    print("Mass_FlowRate_Water ",Mass_FlowRate_Water,'\n')

    value = packet[26]|(packet[27]<<8)
    flo32 = value/10000
    print("Sr_Density_Liquid ",flo32,'\n')

    value = packet[28]|(packet[29]<<8)
    flo32 = value/100
    print("Sr_Temperature_Liquid ",flo32,'\n')

    value = packet[30]|(packet[31]<<8)
    flo32 = value/10000
    print("Sr_Wm_Water ",flo32,'\n')

    value = packet[32]|(packet[33]<<8)
    flo32 = value/10000
    print("Density_Oil_Save ",flo32,'\n')

    value = packet[34]|(packet[35]<<8)
    flo32 = value/10000
    print("Density_Water_Save ",flo32,'\n')

    value = packet[36]|(packet[37]<<8)
    flo32 = value/10000
    print("Density_Liquid_Save ",flo32,'\n')

    value = packet[38]|(packet[39]<<8)
    flo32 = value/100
    print("Pc_Gas ",flo32,'\n')


    value = packet[40]|(packet[41]<<8)
    print("CntTime ",value,'\n')

    value = packet[42]|(packet[43]<<8)
    print("Sync_Liquid ",value,'\n')

    value = packet[44]|(packet[45]<<8)
    print("OtvNumber ",value,'\n')

    value = packet[46]|(packet[47]<<8)|(packet[48]<<16)|(packet[49]<<24)
    flo32 = struct.pack('I',value)
    Summ_Volume_Gas = struct.unpack('f',flo32)
    print("Summ_Volume_Gas ",Summ_Volume_Gas,'\n')

    value = packet[50]|(packet[51]<<8)|(packet[52]<<16)|(packet[53]<<24)
    flo32 = struct.pack('I',value)
    Volume_FlowRate_Liquid = struct.unpack('f',flo32)
    print("Volume_FlowRate_Liquid ",Volume_FlowRate_Liquid,'\n')


  else:
    print('len packet mismatch\n',len(packet))


  return 1

def ComList(ser):
  while(1):
    hello = ser.read(1)
    if (hello != ''):
      #print(char_to_int(hello,len(hello)))
      print(int.from_bytes(hello,byteorder='big'))
#      print(hex(ord(hello)))
def main():
  have_serial = 1
#  devpy.color_traceback()
#  log = devpy.autolog() # log is a regular stdlib logger object
#  log.info('Yes')
  try:
    ser = serial.Serial('COM9')
    ser.baudrate = 9600;
    print (ser.name)          # check which port was really used
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial.SerialException as e:
    have_serial = 0
    print("could not open port \n")
  hello = 'hello'
  mdbtcp = [0x00,0x03,0x00,0x00,0x00,0x04]#,6,3,0x00,0x3,0x00,1]#,0x04,0x04,0x21,0x05,0x00]
  mdb_address = 5
  mdb_command = 3
  start_address = 0
  reg_numm = 1
  data = [0x0001,0x0002,0x0003,0x0004,0x0005,0x0006,0x0007,0x0008,0x00009,0x0010,0x0011,0x0012,0x0013,0x0014]  #u16 format u16
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
#  print (RTM64ChkSUM(cmd_fs , 13))
#  print (0x02f6)
  TCP_IP = '172.16.1.3'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if have_serial:
    thread.start_new_thread(ComList, (ser, ))
    print ('tread is start')
  good_transaction = 0
  bad_transaction = 0
  print ('c - tcp connect\n'
         't - mdbtcp send(after connect)\n'
         'm - modbus RTU send over uart(open auto)\n')  
  arc_parse = 0
  itt=0
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
    elif ord(q)==114:#r
      mdbtcp_s = bytearray(mdbtcp[6:])
      crc = crc16(mdbtcp_s,len(mdbtcp_s))
      mdbtcp_s.append(crc&0xFF)
      mdbtcp_s.append((crc>>8)&0xFF)

      print(mdbtcp_s[0:])
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(5)
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      data_s =[]
      print(data)
      for i in range(0,len(data)):
        data_s.append(data[i])
#      arc_parse(data_s[9:])
      parse_mdb_response(data_s)
      print(data_s)
      print("lenght",len(data_s))
      print(time_pr,'ms')

    elif ord(q)==109:#m
      mdb_rtu = mdbtcp[6:]
      crc = crc16(mdb_rtu,len(mdb_rtu))
      mdb_rtu.append(crc&0xFF)
      mdb_rtu.append((crc>>8)&0xFF)
      print (mdb_rtu)

      if have_serial:
        ser.reset_input_buffer()
        ser.write(mdb_rtu)
        if arc_parse:
          ser.timeout = 0.4
          receive_buff = ser.read(59)
          buff_temp = [receive_buff[i] for i in range(3,57)]
#          arc_parse(buff_temp)

      
    elif ord(q)==99:#c
      s.connect((TCP_IP, TCP_PORT))
    elif ord(q)==116:#t
#      mdbtcp[0] =  random.randint(0, 255)
      mdbtcp_s = bytearray(mdbtcp[0:])
      print(mdbtcp[0:])
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(5)
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
          mdbtcp[8]= ((start_address>>8)&0xff)
          mdbtcp[9]= (start_address&0xff)
          mdbtcp_s = bytearray(mdbtcp[0:])
          print(mdbtcp[0:])
          s.send(mdbtcp_s)
          time_start=time.time()
          s.settimeout(4)
          data = s.recv(BUFFER_SIZE)
          good_transaction+=1
          time_pr=time.time() - time_start
          data_s =[]
          for i in range(0,len(data)):
            data_s.append(data[i])
          print(data_s)
          print("lenght",len(data_s))
          if data_s:
            if ChekErrorPacket(data_s):
              bad_transaction+=1
          print(time_pr,'ms')
          print('transaction number',good_transaction)
          print('error transaction number',bad_transaction)
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
