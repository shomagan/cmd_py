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
      print(hello)
#      print(ord(hello))
def main():
  have_serial = 1
  try:
    ser = serial.Serial('COM6')
    ser.baudrate = 115200;
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
  count = 0
  send_request = 'Jalisco'
  if have_serial:
    thread.start_new_thread(ComList, (ser, ))

  while 1:
    q = msvcrt.getch()
    if ord(q) == 113:#q
      s.close()
      sys.exit(1)
    elif ord(q)==109:#m
      print (send_request)
      ser.write(send_request.encode('ascii'))

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
