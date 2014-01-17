#7E 03 F0 11 00 46 52 A0 8F 03 70 05 00 10 01 02 56 03 7E 
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
  ser.write("hello")      # write a string
  cmd_en = 0
#         0    1    2     3   4     5     6   7   8     9   10    11  12    13  14  15    16    17  18
  cmd = [0x7E,0x03,0xF0,0x16,0x03,0x46,0x52,0xA0,0x8F,0x03,0x70,0x05,0x00,0x20,0x04,0x00,0x00,0x00,0x04]
  CRC = crc16(cmd[-6:],6)
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
      elif q=='w':
#        cmd_VM_str =str(int(0x7E,16),int(0x02,16),int(0xF0,16),int(0x0C,16),int(0x00,16),int(0x56,16),int(0x4D,16),
#                      int(0xA0,16),int(0x8F,16),int(0x08,16),int(0x00,16),int(0xD3,16),int(0x02,16),int(0x7E,16))  
#        cmd_VM_str =chr(int(0x7E))+chr(int(0x02))+chr(int(0xF0))+chr(int(0x0C))+chr(int(0x00))+chr(int(0x56))+chr(int(0x4D))+chr(int(0xA0))+chr(int(0x8F))+chr(int(0x03))+chr(int(0x00))+chr(int(0xD3))+chr(int(0x02))+chr(int(0x7E))  
        cmd_mdb = int_to_char(cmd)
        ser.write(cmd_mdb)
      elif q=='m':
        mdb = int_to_char(cmd[-11:-3])
        print (cmd[-11:-3])
        ser.write(mdb)

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
