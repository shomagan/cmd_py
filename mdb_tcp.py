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
def ComList(ser):
  while(1):
    hello = ser.read(1)
    if (hello != ''):
      #print(char_to_int(hello,len(hello)))
      print(ord(hello))
      print(hex(ord(hello)))
def main():
  have_serial = 1
  try:
    ser = serial.Serial('COM11')
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
  mdb_address = 3
  mdb_command = 3
  start_address = 653
  reg_numm = 2
  data = [3]
  mdbtcp.append(mdb_address)
  mdbtcp.append(mdb_command)
  mdbtcp.append((start_address>>8)&0xff)
  mdbtcp.append(start_address&0xff)
  if mdb_command == 3 or mdb_command == 4:
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
  TCP_IP = '172.16.1.5'
  TCP_PORT = 502
  BUFFER_SIZE = 1024
  MESSAGE = "Hello, World!"
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if have_serial:
    thread.start_new_thread(ComList, (ser, ))
  print ('tread is start')
  good_transaction = 0
  bad_transaction = 0
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
    elif ord(q)==110:#n
      for i in range(1,250):
        mdb_rtu = mdbtcp[6:]
        mdb_rtu[0] = i
        crc = crc16(mdb_rtu,len(mdb_rtu))
        mdb_rtu.append(crc&0xFF)
        mdb_rtu.append((crc>>8)&0xFF)
        print (mdb_rtu)
        ser.write(mdb_rtu)
        time.sleep(0.3)

    elif ord(q)==114:#r
      print(cmd_FR_T)
      ser.write(cmd_FR_T)
    elif ord(q)==109:#m
      mdb_rtu = mdbtcp[6:]
      crc = crc16(mdb_rtu,len(mdb_rtu))
      mdb_rtu.append(crc&0xFF)
      mdb_rtu.append((crc>>8)&0xFF)
      print (mdb_rtu)
      ser.write(mdb_rtu)
    elif ord(q)==99:#c
      s.connect((TCP_IP, TCP_PORT))
    elif ord(q)==116:#t
      mdbtcp_s = bytearray(mdbtcp[0:])
      print(mdbtcp[0:])
      s.send(mdbtcp_s)
      time_start=time.time()
      s.settimeout(4)
      data = s.recv(BUFFER_SIZE)
      time_pr=time.time() - time_start
      data_s =[]
#        print(data)
      for i in range(0,len(data)):
        data_s.append(data[i])
      parse_mdb_tcp_response(data_s)
      print(data_s)
      print("lenght",len(data_s))
      print(time_pr,'ms')

    elif ord(q)==108:#l
      while(1):
        try:
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
        time.sleep(0.05)
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
