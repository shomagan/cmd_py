#FS|7E 02 F0 10 00 46 53 A0 8F 03 00| 36 00 |E3 15 |43 04 7E 
#FR
import sys, os, threading, atexit,io,serial,time
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt as m
#def hextoascii():

def main():
  time_start=time.time()
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
  cmd_en = 0
  packet = list(range(0,200))
  log = open('log.log','w')
  while 1:
    hello = ser.readline(ser.inWaiting())
    if (hello == '~'): 
      if (cmd_en == 0):
        cmd_en = 1
        count = 0
        packet[count] = hello
        count = 1
      else: 
        packet[count] = hello
        cmd_en = 0
        count += 1
        log.write (char_to_int(packet,count)+'\n')
        print_hex(char_to_int(packet,count),count)
    elif (hello != ''):
      if (len(hello)>1):
        i=0
        while(i<len(hello)):
          packet[count] = hello[i]
          i+=1
          if (count == len(packet)-1): count =0
          else: count += 1  
      else:
        packet[count] = hello
#        print(char_to_int(hello,1))
        if (count == len(packet)-1): count =0
        else: count += 1  
    if m.kbhit() == 1:
      q = m.getche()
      if q == 'q':
        log.close()
        sys.exit(1)
      elif q=='f':
        temp_buff = int_to_char(cmd_FS_FullStart)
        print_hex (cmd_FS_FullStart,len(cmd_FS_FullStart))
        ser.write(temp_buff)
#        sys.stderr.write(cmd_mdb)
class Packet:
  def __init__(self):
    self.number = 0
    self.comand = "ZZ"
    self.const = {}
    self.input_variable = {}
    self.var_variable   = {}
    self.out_variable   = {}    
  def new_var(self,name,address,type_v):
    if (type_v == 0):
      self.const[name] = address
    elif(type_v == 1):      
      self.input_variable[name] = address
    elif(type_v == 2):
      self.out_variable[name] = address
    else:
      self.var_variable[name] = address

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
