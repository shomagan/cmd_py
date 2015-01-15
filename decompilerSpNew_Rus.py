#!/c/Python33/ python
import sys, os, threading, atexit,io,time,re
import msvcrt as m
from struct import *
def main():
  time_start=time.time()
  HtmlFile = open ('sp.shtml','w')
  TagStructFile = open ('struct.pat','w')      
  OwnVariableFile = open('ownvariablname.pat','w')
  Vars = open('../vars.h','r',encoding='cp1251',errors='ignore')
  TempHtml = open ('STM32F2x7ADC.shtml','r')
  struct = 0
  #WorkHtml.write(TempHtml.readline())
  #WorkHtml.write(TempHtml.())
  for i in range(27):
    HtmlFile.writelines(TempHtml.readline())
  OwnVariableFile.writelines('NetworkFlashVariable_t const NetworkFlashVariable[INTERNAL_VAR_NUM ]={'+'\n')
  for linefull in Vars:
#    line_x = Vars.readline()
    if('//' in linefull):
      start = linefull.find('//')
      line = linefull[:start]
    else:
      line = linefull
    p = re.compile('\WMyAdr\W')
#    print(re.search(p,line))
#    print(linefull)
    if re.search(p,line):
      struct = 1
      SP_b = SP()
    if (struct == 1):
    #  print(line_x)
      SP_b.check(linefull)
      SP_b.save(OwnVariableFile,HtmlFile,TagStructFile)
    if (struct == 1 & ('}'in line)):
        struct = 0
  OwnVariableFile.writelines('};')
  for i in range(10):
    line = TempHtml.readline()
  for i in range(11):
    HtmlFile.writelines(TempHtml.readline())
  TagStructFile.close()
  HtmlFile.close()
  OwnVariableFile.close()
  TempHtml.close()
  Vars.close()
  input ("exit")
class SP:
  def __init__(self):
    self.pDefault = "NULL"
    self.Name = "noname"
    self.InternalName = "noname"
    self.Type = "Kod"
    self.Ind =  0
    self.GuID = 0
    self.SizeArray = 0
    self.Flag = 0x00
    self.description = "//"
    self.opt = 0
  def check(self,line):
    self.SizeArray = 1
    w = re.compile('^\s*(?P<type>[\w\d]+)\s+(?P<name>[\w\d]+)\s*(\[(?P<size>[\d\w]+)\])?\s*\;\s*(?P<descript>\/\/[\w\W]*$)*',re.ASCII)
    test = w.match(line)
    if test:
      l = w.search(line)
      self.Name = '"'+l.group('name')+'"'
      self.InternalName ='"'+l.group('name')+'"'
      if(l.group('descript')):
        self.description = l.group('descript')
        print (l.group('descript'))
        n_t = re.compile('\"[\w\d\-\(\)\[\]]+\"')
        name_rs = n_t.search(self.description)
        if name_rs:
#          input (name_rs)
          self.Name = name_rs.group(0) 
      p = re.compile('v?[us]8',re.ASCII)

      m = p.match(l.group('type'))
      if m:
        self.Type = "KodInt8"
      else:
        p = re.compile('v?[us]16')
        m = p.match(l.group('type'))
        if m:
          self.Type = "KodInt16"
        else:
          p = re.compile("v?[us]32"
                         "|sCfgUpdateErrorFlags"
                         "|sKernelErrorFlags"
                         "|sKernelEventFlags" 
                         )
          m = p.match(l.group('type'))
          if m:
            self.Type = "KodInt32"
          else:
            p = re.compile('Int64U')
            m = p.match(l.group('type'))
            if m:
              self.Type = "KodInt32"
              self.SizeArray = 2
            else:
              p = re.compile('[^\W]Flo32\W')
              m = p.match(l.group('type'))
              if m:
                self.Type = "KodFloat32"
              else:
                self.Type = "Kod"
                self.SizeArray = 0
      if (l.group('size')):
        if(l.group('size')=="LenNumDI"):
          self.SizeArray = 18
        elif(l.group('size')=="ChanelCount"):
          self.SizeArray = 9
        else:
          self.SizeArray = int(l.group('size'))*self.SizeArray

    else:
#      print(line)
      self.SizeArray = 0
#    print(l.group('size'))
 #     print(self.SizeArray)

    self.Flag = 0x00

  def save(self,OwnVariableFile,HtmlFile,TagStructFile):
    if(self.SizeArray>0):
#      print(self.pDefault+','+self.Name+','+self.InternalName+','+self.Type+','+str(self.Ind)+','+str(self.GuID)+','+str(self.SizeArray)+','+str(self.Flag)+','+self.description+',')
#      print(self.pDefault+','+self.Name+','+self.InternalName+','+self.Type+','+str(self.Ind)+','+str(self.GuID)+','+str(self.SizeArray)+','+str(self.Flag)+','+self.description+',')
      OwnVariableFile.writelines(self.pDefault+','+self.Name+','+self.InternalName+','+self.Type+','+str(self.Ind)+','+str(int(self.GuID))+','+str(self.SizeArray)+','+str(self.Flag)+','+self.description+'\n')
      HtmlFile.write('<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'+'\n')
      HtmlFile.write('<tbody>'+'\n')
      HtmlFile.write('<tr>'+'\n')
      HtmlFile.write('<td style="width: 100px;font-weight: bold; font-style: italic; font-family: Verdana; background-color: rgb(0, 251, 213);"><small><span style="color: black ;">'+'\n')
      HtmlFile.write(self.Name+'\n')
      HtmlFile.write('</span> </small></td>'+'\n')
      HtmlFile.write('<td style="font-style: italic;font-family: Verdana;background-color: rgb(0, 251, 213);"><span style="color: black ;"><!--#'+str(self.Ind)+'--></span></td>'+'\n')
      HtmlFile.write('</tr>'+'\n')
      HtmlFile.write('</tbody>'+'\n')
      HtmlFile.write('</table>'+'\n')
      TagStructFile.write ('"'+str(self.Ind)+'"'+','+'//'+self.Name+'\n')
      self.Ind += 1
      if(self.Type =="KodInt8"):
        if(self.SizeArray==1):
          if (self.opt==0):
            self.GuID = self.GuID
            self.opt = 1
          else:
            self.GuID +=1
            self.opt = 0
        else:
          self.GuID = self.GuID + (self.SizeArray/2)
      if(self.Type =="KodInt16"):
        self.opt = 0
        self.GuID +=(self.SizeArray)
      if(self.Type =="KodInt32")|(self.Type =="KodFloat32"):
        self.opt = 0
        self.GuID +=(self.SizeArray*2)
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
