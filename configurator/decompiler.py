import sys, os, threading, atexit,io
import msvcrt as m
from struct import *
#def hextoascii():
class FB:
  def __init__(self):
    self.input_variable = {}
    self.var_variable   = {}
    self.out_variable   = {}    
  def new_var(self,name,address,type_v):
    if (type_v == 0):
      self.input_variable[name] = address
    elif(type_v == 1):      
      self.var_variable[name] = address
    else:self.out_variable[name] = address

def main():
  fb_name = open('fb_name.txt','r')
  fb_namber_to_name = fb_name.readlines()
  fb32 = open ('TESTING.fb32','rb')
  fb32_b = fb32.read()
  fb32.close
  size_conf =(ord(fb32_b[0])<<8)|(ord(fb32_b[1]))
  size_im_conf = (ord(fb32_b[2])<<8)|(ord(fb32_b[3]))
  im_conf = fb32_b[4:4+size_im_conf]
  size_fb_conf = (ord(fb32_b[4+size_im_conf])<<8)|(ord(fb32_b[5+size_im_conf]))  
  fb_conf = fb32_b[6 + 1+ size_im_conf:6 + 1 + size_im_conf + size_fb_conf]
  im_conf_c = str_to_c(im_conf,len(im_conf))
  fb_conf_c = str_to_c(fb_conf,len(fb_conf))
  print('configuration size',size_conf)
  print('immanager size',size_im_conf)
  print('fb size',size_fb_conf)
  print(im_conf_c)
  print(fb_conf_c)
  variable = {}
  fb_runtime = {}
  fb_immanager = {}
  im_one = FB()                
#  im_one.input_variable['null'] = 0
  im_one.new_var('ones',0x12,0)
  im_one.new_var('twels',0x2,2)
  im_two = FB()
  im_two.new_var('ones',0x66,0)
  im_two.new_var('twels',0x24,2)
  print(im_two.input_variable,im_two.var_variable,im_two.out_variable) 
  print(im_one.input_variable,im_one.var_variable,im_one.out_variable) 
#  decompiler(variable,fb_immanager,im_conf_c)
#  decompiler(variable,fb_runtime,fb_conf_c)  
#  print(fb32_b[1])

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
def str_to_c(cmd_x,lenth):
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
