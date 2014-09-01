#FS|7E 02 F0 10 00 46 53 A0 8F 03 00| 36 00 |E3 15 |43 04 7E 
#FR
import sys, os, threading, atexit,io,serial
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt as m
#def hextoascii():

def main():
  ser = serial.Serial(1)  # open first serial port
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
  ser.baudrate = 115200;
  ser.write("hello")      # write a string
  cmd_en = 0
  cmd_FS_stop = [0x7E,0x02,0xF0,0x10,0x00,0x46,0x53,0xA0,0x8F,0x03,0x00,0x36,0x00,0xE3,0x15]
  ChekSum = RTM64ChkSUM(cmd_FS_stop[1:] , len(cmd_FS_stop)-1)
  cmd_FS_stop.append(ChekSum&0xFF)
  cmd_FS_stop.append((ChekSum>>8)&0xFF)
  cmd_FS_stop.append(0x7E)
  cmd_FS_start = [0x7E,0x02,0xF0,0x10,0x00,0x46,0x53,0xA0,0x8F,0x03,0x00,0x36,0x00,0xE4,0x15]  
  ChekSum = RTM64ChkSUM(cmd_FS_start[1:] , len(cmd_FS_start)-1)
  cmd_FS_start.append(ChekSum&0xFF)
  cmd_FS_start.append((ChekSum>>8)&0xFF)
  cmd_FS_start.append(0x7e)
  cmd_FS_FullStop = [0x7E,0x02,0xF0,0x10,0x00,0x46,0x53,0xA0,0x8F,0x03,0x00,0x36,0x00,0xE0,0x15]  
  ChekSum = RTM64ChkSUM(cmd_FS_FullStop[1:] , len(cmd_FS_FullStop)-1)
  cmd_FS_FullStop.append(ChekSum&0xFF)
  cmd_FS_FullStop.append((ChekSum>>8)&0xFF)
  cmd_FS_FullStop.append(0x7e)
  cmd_FS_FullStart = [0x7E,0x02,0xF0,0x10,0x00,0x46,0x53,0xA0,0x8F,0x03,0x00,0x36,0x00,0xE2,0x15]  
  ChekSum = RTM64ChkSUM(cmd_FS_FullStart[1:] , len(cmd_FS_FullStart)-1)
  cmd_FS_FullStart.append(ChekSum&0xFF)
  cmd_FS_FullStart.append((ChekSum>>8)&0xFF)
  cmd_FS_FullStart.append(0x7e)
  cmd_FR_Conf = [0x7E,0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0xFE,0x00,0x01]  
  ChekSum = RTM64ChkSUM(cmd_FR_Conf[1:] , len(cmd_FR_Conf)-1)
  cmd_FR_Conf.append(ChekSum&0xFF)
  cmd_FR_Conf.append((ChekSum>>8)&0xFF)
  cmd_FR_Conf.append(0x7e)
  cmd_FR_2 = [0x7E,0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0x02,0x04,0x01]  
  ChekSum = RTM64ChkSUM(cmd_FR_2[1:] , len(cmd_FR_2)-1)
  cmd_FR_2.append(ChekSum&0xFF)
  cmd_FR_2.append((ChekSum>>8)&0xFF)
  cmd_FR_2.append(0x7e)
  cmd_FR_0 = [0x7E,0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0x00,0x04,0x01]  
  ChekSum = RTM64ChkSUM(cmd_FR_0[1:] , len(cmd_FR_0)-1)
  cmd_FR_0.append(ChekSum&0xFF)
  cmd_FR_0.append((ChekSum>>8)&0xFF)
  cmd_FR_0.append(0x7e)
  cmd_FR_T = [0x7E,0x02,0xF0,0x0F,0x00,0x46,0x52,0xA0,0x8F,0x03,0x00,0x03,0x00,0x04]  
  ChekSum = RTM64ChkSUM(cmd_FR_T[1:] , len(cmd_FR_T)-1)
  cmd_FR_T.append(ChekSum&0xFF)
  cmd_FR_T.append((ChekSum>>8)&0xFF)
  cmd_FR_T.append(0x7e)
  cmd_FS_IP = [0x7E,0x02,0xF0,0x10,0x00,0x46,0x53,0xA0,0x8F,0x03,0x00,0x08,0x00,0x01,0xEC]  #0xC0,0xA8]#
  ChekSum = RTM64ChkSUM(cmd_FS_IP[1:] , len(cmd_FS_IP)-1)
  cmd_FS_IP.append(ChekSum&0xFF)
  cmd_FS_IP.append((ChekSum>>8)&0xFF)
  cmd_FS_IP.append(0x7e)

  cmd_s = list(range(0,200))

  while 1:
    hello = ser.readline(ser.inWaiting())
    if (hello == '~'): 
      if (cmd_en == 0):
        cmd_en = 1
        count = 0
        cmd_s[count] = hello
        count = 1
      else: 
        cmd_s[count] = hello
        cmd_en = 0
        count += 1
        print_hex(char_to_int(cmd_s,count),count)
    elif (hello != ''):
      if (len(hello)>1):
        i=0
        while(i<len(hello)):
          cmd_s[count] = hello[i]
          i+=1
          if (count == len(cmd_s)-1): count =0
          else: count += 1  
      else:
        cmd_s[count] = hello
#        print(char_to_int(hello,1))
        if (count == len(cmd_s)-1): count =0
        else: count += 1  
    if m.kbhit() == 1:
      q = m.getche()
      if q == 'q':
        sys.exit(1)
      elif q=='f':
        temp_buff = int_to_char(cmd_FS_FullStart)
        print_hex (cmd_FS_FullStart,len(cmd_FS_FullStart))
        ser.write(temp_buff)
      elif q=='s':
        temp_buff = int_to_char(cmd_FS_FullStop)
        print (cmd_FS_FullStop)
        ser.write(temp_buff)
      elif q=='g':
        temp_buff = int_to_char(cmd_FS_start)
        print (cmd_FS_start)
        ser.write(temp_buff)
      elif q=='r':
        temp_buff = int_to_char(cmd_FR_Conf)
        print (cmd_FR_Conf)
        ser.write(temp_buff)
      elif q=='R':
        temp_buff = int_to_char(cmd_FR_2)
        print (cmd_FR_2)
        ser.write(temp_buff)
      elif q=='o':
        temp_buff = int_to_char(cmd_FR_0)
        print (cmd_FR_0)
        ser.write(temp_buff)
      elif q=='t':
        temp_buff = int_to_char(cmd_FR_T)
        print (cmd_FR_T)
        ser.write(temp_buff)
      elif q=='i':
        temp_buff = int_to_char(cmd_FS_IP)
        print (cmd_FS_IP)
        ser.write(temp_buff)
           
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
def char_to_int(cmd_x,lenth):
  """char to string array confersion"""
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i<lenth):
    cmd_r[i]=ord(cmd_x[i])
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
