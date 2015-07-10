import sys, os, threading, atexit,io
import msvcrt as m
#def hextoascii():

def main():
  fb_name = open('fb_name.txt','w')
  fb_name.write ('Number FB and Name\n')
  current = 0
  while 1:
    current+=1
    if current == 101: sys.exit(1)
    try:
      if (current <= 9):
        fb_temp = open('FB/fb0000'+str(current)+'.h')
      elif (current <= 99):
        fb_temp = open('FB/fb000'+str(current)+'.h')
      else:
        fb_temp = open('FB/fb00'+str(current)+'.h')
    except IOError: continue
    line = fb_temp.readline()
    while 1:
      try:
        if ((line[0] == '/') & (line[1] == '*')):
          fb_name.write (str(current)+' '+line)
          break
        else:line = fb_temp.readline()
      except IndexError:break
    if m.kbhit() == 1:
      q = m.getche()
      if q == 'q':
        sys.exit(1)
        fb_name.close()
      elif q=='w':
        sys.exit(1)
        fb_name.close()
      elif q=='m':
        sys.exit(1)
        fb_name.close()
      elif q=='h':
        sys.exit(1)
        fb_name.close()

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
