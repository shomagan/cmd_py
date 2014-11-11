#!/c/Python33/ python
import sys, os, threading, atexit,io,time
import msvcrt as m
from struct import *
def main():
  time_start=time.time()
  Work = open ('sp.shtml','w')
  Struct = open ('struct.pat','w')
  TempC = open('ownvariablname.sh','r')
  TempHtml = open ('STM32F2x7ADC.shtml','r')
  #WorkHtml.write(TempHtml.readline())
  #WorkHtml.write(TempHtml.())
  for i in range(27):
    Work.writelines(TempHtml.readline())

  struct = 0
  start  = 0
  finish = 0
  first = 1
  cnt = 0
  for linefull in TempC:
    if('//' in linefull):
      start = linefull.find('//')
      line = linefull[:start]
    else:
      line = linefull
    if 'NetworkFlashVariable_t' in line:
      struct = 1
    if (struct == 1):
      if ('"'in line)&(first ==0):
        start = line.find('"')
        finish = line.find('"',start+1)
        name = line[start+1:finish]
        #Work.write('<span style="font-family: Verdana;"></span><span style="font-family: Verdana;"></span>'+'\n')
        Work.write('<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'+'\n')
        Work.write('<tbody>'+'\n')
        Work.write('<tr>'+'\n')
        Work.write('<td style="width: 100px;font-weight: bold; font-style: italic; font-family: Verdana; background-color: rgb(0, 251, 213);"><small><span style="color: black ;">'+'\n')
        Work.write(name+'\n')
        Work.write('</span> </small></td>'+'\n')
        Work.write('<td style="font-style: italic;font-family: Verdana;background-color: rgb(0, 251, 213);"><span style="color: black ;"><!--#'+str(cnt)+'--></span></td>'+'\n')
        Work.write('</tr>'+'\n')
        Work.write('</tbody>'+'\n')
        Work.write('</table>'+'\n')
        Struct.write ('"'+str(cnt)+'"'+','+'//'+name+'\n')
        cnt +=1
        first = 1
      if (('NULL'in line)|('MAC_ADD' in line))&(first ==1):
        first = 0
    if (struct == 1 & ('}'in line)):
        struct = 0
  for i in range(10):
    line = TempHtml.readline()
  for i in range(11):
    Work.writelines(TempHtml.readline())
  Struct.close()
  Work.close()
  TempC.close()
  TempHtml.close()
 
def find_name(number):
  fb_name = open('fb_name.txt','r')
  current = 0
  line = fb_name.readline()
  while 1:
    current+=1
    if current == 101:
      fb_name.close()
      return ('none_FB')

    line = fb_name.readline()
    try:
      cnt = 0
      for a in line:
        cnt +=1
        if a == ' ':
          break
      if (cnt == 2):
        fb_temp = int(line[0])
      elif(cnt == 3):
        fb_temp = int(line[0]+line[1])
      elif(cnt == 4):
        fb_temp = int(line[0]+line[1]+line[2])
      if (fb_temp == number):
        fb_name.close()
        return (line[cnt:])
    except IndexError:break
def write_property(FB_property,decompile):
  decompile.write (FB_property.name+'#'+str(FB_property.number)+'\n')
  if (len(FB_property.const)>0):
    for (key,value) in FB_property.const.items():
      decompile.write (key+'&'+str(value)+'\n')
  if (len(FB_property.input_variable)>0):
    for key in FB_property.input_variable:
      decompile.write (key+'&'+str(FB_property.input_variable[key])+'\n')
  if (len(FB_property.var_variable)>0):
    for key in FB_property.var_variable:
      decompile.write (key+'&'+str(FB_property.var_variable[key])+'\n')
  if (len(FB_property.out_variable)>0):
    for key in FB_property.out_variable:
      decompile.write (key+'&'+str(FB_property.out_variable[key])+'\n')

def fbparser(fb,len_fb):

  return array + len_fb
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
