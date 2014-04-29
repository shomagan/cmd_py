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
  ser.baudrate =115200
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
  Packet_class = Packet()
  packet = list(range(0,200))
  log = open('log.log','w')
  ptr_packet = 0
  time_packet = time.time()
  count = 0 
  while 1:
    hello = ser.readline(ser.inWaiting())
    if (((time.time()-time_packet)>1.0)and cmd_en):
      cmd_en=0
    if (hello == '~'): 
      if (cmd_en == 0):
        time_packet = time.time()
        cmd_en = 1
        count = 0
        packet[count] = hello
        count = 1
      else: 
        time_packet = time.time()
        packet[count] = hello
        cmd_en = 0
        count += 1
        ptr_packet+=1
        packet_temp = char_to_int(packet,count)
        print(time.time()-time_start)
        log.write(str(time.time()-time_start)+'\t')  
        Packet_class.parser(packet_temp,count,ptr_packet)
        Packet_class.packet_print(log)
        
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
#        sys.stderr.write(cmd_mdb)
class Packet:
  def __init__(self):
    self.number = 0
    self.comand = "ZZ"
    self.addres_size = 0
    self.lenght = 0
    self.addres = [0 for x in range(5)]
    self.CRC_in   = 0
    self.CHSUM_calc   = 0
    self.CRC_calc   = 0
    self.CRC_status   = "OK"    
  def parser(self,packet,lenght,number):
    self.number = number
    self.addres_size = packet[1]
    self.lenght = packet[3]
    self.comand = (chr(packet[5])+chr(packet[6]))
    for x in range(self.addres_size):
      self.addres[x] = (packet[x*2+8]<<8|packet[x*2+7])&0x0FFF 
    self.CRC_in = (packet[self.lenght]<<8|packet[self.lenght-1])
    self.CRC_calc = RTM64CRC16(packet[1:],self.lenght-1)
    self.CHSUM_calc   = RTM64ChkSUM(packet[1:],self.lenght-2)
    if (self.CRC_in==self.CRC_calc or self.CHSUM_calc==self.CRC_in):
      self.CRC_status   = "OK"    
    else:
      self.CRC_status   = "Err"    
  def packet_print(self,log):
    log.write ('number'+str(self.number)+'\t'+'comm'+str(self.comand))
    print ('number'+str(self.number)+'comm'+str(self.comand))
    for x in range(self.addres_size):
      log.write ('adress'+str(x)+'='+str(self.addres[x])+'\t')
      print ('adress'+str(x)+'='+str(self.addres[x])+'\t')
    log.write('CRC'+str(self.CRC_in)+'CRC_calc'+str(self.CRC_calc)+'checksumm'+str(self.CHSUM_calc)+str(self.CRC_status)+'\n')
    print('CRC'+str(self.CRC_in)+'CRC_calc'+str(self.CRC_calc)+'checksumm'+str(self.CHSUM_calc)+str(self.CRC_status)+'\n')

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
  """char to string array conversion"""
  i = 0
  cmd_r = ['~']
  while (i<len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i+=1
  return cmd_r[1:]
def char_to_int(cmd_x,lenth):
  """char to string array conversion"""
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
