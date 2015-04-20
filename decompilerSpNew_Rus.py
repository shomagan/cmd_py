#!/c/Python33/ python
import sys, os, threading, atexit,io,time,re
import fileinput
import msvcrt as m
from struct import *
def main():
  time_start=time.time()
  HtmlFile = open ('fs/sp.shtml','w')
  HtmlDescribe = open ('describe.html','w')
  TagStructFile = open ('struct.pat','w')
  OwnVariableFile = open('ownvariablname.pat','w')
  Vars = open('../vars.h','r',encoding='cp1251',errors='ignore')
  TempHtml = open ('STM32F2x7ADC.shtml','r')
  struct = 0
  #WorkHtml.write(TempHtml.readline())
  #WorkHtml.write(TempHtml.())
  for i in range(27):
    line = TempHtml.readline()
    HtmlFile.writelines(line)
#    HtmlDescribe.writelines(line)
  OwnVariableFile.writelines('NetworkFlashVariable_t const NetworkFlashVariable[INTERNAL_VAR_NUM ]={'+'\n')
  for linefull in Vars:
#    line_x = Vars.readline()
    if('//' in linefull):
      start = linefull.find('//')
      line = linefull[:start]
    else:
      line = linefull
    p = re.compile('\WMyAdr\W')
    if re.search(p,line):
      struct = 1
      SP_b = SP()
    if (struct == 1 & ('}'in line)):
        struct = 0
    if (struct == 1):
      SP_b.check(linefull)
      if SP_b.SizeArray:
        SP_b.save(OwnVariableFile,HtmlFile,HtmlDescribe,TagStructFile)
        SP_b.SP_Numm+=1

  print("first config variable "+str(SP_b.GuID))
  OwnVariableFile.writelines('};')
  for i in range(10):
    line = TempHtml.readline()
  for i in range(11):
    HtmlFile.writelines(TempHtml.readline())
    HtmlDescribe.writelines(TempHtml.readline())
  print("find " +str(SP_b.SP_Numm)+" own network variable")  
  OwnVariableFile.close()
  TagStructFile.close()
  HtmlFile.close()
#rewrite exist file with new network variable settings
  WriteExistFile()
  print ('start makefsdata.exe')
  os.system("C:/Work_MC/Mega11/mega12family_usercopy/inc/makefsdata.exe")
  HtmlDescribe.writelines(TempHtml.readline())

  TempHtml.close()
  Vars.close()
  input ("exit")
class SP:
  def __init__(self):
    self.pDefault = "NULL"
    self.Name = "noname"
    self.InternalName = "noname"
    self.Type = "Kod"
    self.Ind = 0
    self.GuID = 0
    self.SizeArray = 0
    self.Flag = 0x00
    self.description = "//"
    self.opt = 0
    self.SP_Numm = 0
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
        n_t = re.compile('\"[\w\d\-\(\)\[\]]+\"')
        name_rs = n_t.search(self.description)
        if name_rs:
          self.Name = name_rs.group(0) 
        n_t = re.compile('\&(?P<pDefault>[\w\d\-\(\)\[\]]+)\&')
        name_rs = n_t.search(self.description)
        if name_rs:
          self.pDefault = name_rs.group('pDefault')
        else:
          self.pDefault = "NULL"


      p = re.compile("v?[us]8"
                     "|uint8\_t",re.ASCII)

      m = p.match(l.group('type'))
      if m:
        self.Type = "KodInt8"
      else:
        p = re.compile("v?[us]16"
                        "|uint16\_t")
        m = p.match(l.group('type'))
        if m:
          self.Type = "KodInt16"
        else:
          p = re.compile("v?[us]32"
                         "|sCfgUpdateErrorFlags"
                         "|sKernelErrorFlags"
                         "|sKernelEventFlags" 
                         "|uint32\_t"
                         "|float"
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
                print ("unvalidate type for variable"+self.InternalName+"description "+self.description)
                self.Type = "Kod"
                self.SizeArray = 0
      if (l.group('size')):
        if(l.group('size')=="LenNumDI"):
          self.SizeArray = 18
        elif(l.group('size')=="ChanelCount"):
          self.SizeArray = 9
        elif(l.group('size')=="LOAD_BUFF_SIZE"):
          self.SizeArray = 512
        else:
          self.SizeArray = int(l.group('size'))*self.SizeArray
    else:
      self.SizeArray = 0

    self.Flag = 0x00

  def save(self,OwnVariableFile,HtmlFile,HtmlDescribe,TagStructFile):
    OwnVariableFile.writelines(self.pDefault+','+self.Name+','+self.InternalName+','+self.Type+','+str(self.Ind)+','+str(int(self.GuID))+','+str(self.SizeArray)+','+str(self.Flag)+','+self.description+'\n')
    HtmlFile.write('<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'+'\n')
    HtmlDescribe.write('<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'+'\n')
    HtmlFile.write('<tbody>'+'\n')
    HtmlDescribe.write('<tbody>'+'\n')
    HtmlFile.write('<tr>'+'\n')
    HtmlDescribe.write('<tr>'+'\n')
    HtmlFile.write('<td style="width: 100px;font-weight: bold; font-style: italic; font-family: Verdana; background-color: rgb(0, 251, 213);"><small><span style="color: black ;">'+'\n')
    HtmlDescribe.write('<td style="width: 5px;font-weight:bold; font-style: italic; font-family: Verdana; background-color: rgb(0, 251, 213);"><small><span style="color: black ;">'+'\n')
    HtmlFile.write(self.Name+'\n')
    HtmlDescribe.write(str(self.Ind)+'\n')
    HtmlDescribe.write('<td style="rgb(0, 251, 213);font-weight:bold;font-family: Verdana"><small><span style="color: black ;">'+'\n')
    HtmlDescribe.write(self.InternalName+'\t'+'Type = '+'\t'+self.Type+'\t'+'Size = '+'\t'+str(self.SizeArray)+'\t'+'Mdb_Addr = '+str(self.GuID) + '\t'+self.description+'\n')
    HtmlFile.write('</span> </small></td>'+'\n')
    HtmlFile.write('<td style="font-style: italic;font-family: Verdana;background-color: rgb(0, 251, 213);"><span style="color: black ;"><!--#'+str(self.Ind)+'--></span></td>'+'\n')
    HtmlFile.write('</tr>'+'\n')
    HtmlDescribe.write('</tr>'+'\n')
    HtmlFile.write('</tbody>'+'\n')
    HtmlDescribe.write('</tbody>'+'\n')
    HtmlFile.write('</table>'+'\n')
    HtmlDescribe.write('</table>'+'\n')
    TagStructFile.write ('    "'+str(self.Ind)+'"'+','+'//'+self.Name+'\n')
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
  def __del__(self):
    print("dlt SP")

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

def WriteExistFile():
  OwnVariableFile = open('ownvariablname.pat','r')
  replace = 0
  number = 0
  for line in fileinput.input('../ownvariablname.c', inplace=1):
    if "NetworkFlashVariable_t" in line:
      replace = 1
    if replace:
      cancel = re.compile('^\s*\}\;',re.ASCII)
      test = cancel.match(line)
      if test:
        replace = 0
        for own_line in OwnVariableFile:
          print(own_line,end='')
          number+=1
    else:
      print(line,end='')
  fileinput.close()
  if number:
    print ('replace '+str(number)+' string in file ../ownvariablname.c')
  else:
    print ("don't find NetworkFlashVariable_t struct in file ../ownvariablname.c")

  TagStructFile = open ('struct.pat','r')
  replace = 0
  number = 0
  for line in fileinput.input('../httpd_cgi_ssi.c', inplace=1):
    if "g_pcConfigSSITags[]" in line:
      replace = 1
      print(line+'{',end='')
    if replace:
      cancel = re.compile('^\s*\}\;',re.ASCII)
      test = cancel.match(line)
      if test:
        replace = 0
        for tag_line in TagStructFile:
          print(tag_line,end='')
          number+=1
        print(line,end='')
    else:
      print(line,end='')
  fileinput.close()
  if number:
    print ('replace '+str(number)+' string in file ../httpd_cgi_ssi.c')
  else:
    print ("don't find g_pcConfigSSITags struct in file ../httpd_cgi_ssi.c")


  

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
