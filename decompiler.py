"""
type 
---------------
bit 7 000 bit
bit 6 001 uit8
bit 5 010 uint16
      011 uint32
      100 float
      101 time
---------------
value
---------------
bit 2 0 variable
      1 array
---------------
destination
---------------
bit 1 00 const
bit 0 01 input
      10 output
      11 input_variable
"""
import sys, os, threading, atexit,io,time
import msvcrt as m
#def hextoascii():
type_variable = {'bit'     :0x00000000,
                 'uint8'   :0x00100000,
                 'uint16'  :0x01000000,
                 'uint32'  :0x01100000,
                 'float'   :0x10000000,
                 'time'    :0x10100000,
                 'variable':0x00000000,
                 'array'   :0x00000100,
                 'const'   :0x00000000,
                 'input'   :0x00000001,
                 'outpt'   :0x00000010,
                 'in_vb'   :0x00000011,
}
def main():
  time_start=time.time()
  fb_name = open('fb_name.txt','r')
  fb_namber_to_name = fb_name.readlines()
  fb32 = open ('debug.fb32','rb')
  fb32_b = fb32.read()
  fb32.close
  size_conf =((fb32_b[0])<<8)|((fb32_b[1]))
  size_im_conf = ((fb32_b[2])<<8)|((fb32_b[3]))
  im_conf = fb32_b[4:4+size_im_conf]
  size_fb_conf = ((fb32_b[4+size_im_conf])<<8)|((fb32_b[5+size_im_conf]))  
  fb_conf = fb32_b[6 + 1+ size_im_conf:6 + 1 + size_im_conf + size_fb_conf]
  im_conf_c = im_conf

  FB_pt = FB()
  pt_fb = 0
  pt_byte = 0
  pt_var = 0
  FB_array = [FB_pt]
  while (pt_byte < size_im_conf):
    if (FB_pt.number == 0):
      FB_pt.number = (im_conf_c[pt_byte]<<8)|(im_conf_c[pt_byte+1])
      FB_pt.name = find_name(FB_pt.number)
      pt_var = 0
      pt_byte += 2
    type_var = im_conf_c[pt_byte]
    pt_byte += 1
    if (type_var == 0xff):
      FB_array.append(FB_pt)
      FB_pt = FB()
      continue
    else:
      if ((type_var&0x03)==0):
        if (((type_var & 0xE0) == 0) | ((type_var & 0xE0) == 0x20)):
          FB_pt.new_var(str(pt_var)+'_const',im_conf_c[pt_byte],type_var&0x03)
          pt_byte +=1
        elif((type_var&0xE0 == 0x40)):
          FB_pt.new_var(str(pt_var)+'_const',im_conf_c[pt_byte]<<8|im_conf_c[pt_byte+1],type_var&0x03)
          pt_byte +=2
        elif((type_var&0xE0 == 0x60)):
          FB_pt.new_var(str(pt_var)+'_const',(im_conf_c[pt_byte]<<24)|(im_conf_c[pt_byte+1]<<16)|(im_conf_c[pt_byte+1]<<8)|(im_conf_c[pt_byte+1]),type_var&0x03)
          pt_byte +=4
        elif((type_var&0xE0 == 0x80)):
          float_temp = float((im_conf_c[pt_byte]<<24)|(im_conf_c[pt_byte+1]<<16)|(im_conf_c[pt_byte+1]<<8)|(im_conf_c[pt_byte+1]))
          FB_pt.new_var(str(pt_var)+'_const',float_temp,type_var&0x03)
          pt_byte +=4
        elif((type_var&0xE0 == 0xA0)):
          time_temp = ((im_conf_c[pt_byte]<<24)|(im_conf_c[pt_byte+1]<<16)|(im_conf_c[pt_byte+1]<<8)|(im_conf_c[pt_byte+1]))
          FB_pt.new_var(str(pt_var)+'_const',time_temp,type_var&0x03)
          pt_byte +=4
      elif((type_var&0x04)==0x04):
        size_array = im_conf_c[pt_byte]<<8|im_conf_c[pt_byte+1]
        pt_byte +=2
        addres_array = im_conf_c[pt_byte]<<8|im_conf_c[pt_byte+1]
        pt_byte +=2
        FB_pt.new_var(str(pt_var)+'_'+'array'+'_'+str(size_array),addres_array,type_var&0x03)
      else:
        addres_array = im_conf_c[pt_byte]<<8|im_conf_c[pt_byte+1]
        pt_byte +=2
        FB_pt.new_var(str(pt_var),addres_array,type_var&0x03)
    pt_var+=1
  pt_byte = 0
  fb_conf_c = fb_conf
  while (pt_byte < size_fb_conf):
    if (FB_pt.number == 0):
      FB_pt.number = (fb_conf_c[pt_byte]<<8)|(fb_conf_c[pt_byte+1])
      FB_pt.name = find_name(FB_pt.number)
      pt_var = 0
      pt_byte += 2
    type_var = fb_conf_c[pt_byte]
    pt_byte +=1
    if (type_var == 0xff):
      FB_array.append(FB_pt)
      FB_pt = FB()
      continue
    if ((type_var&0x03)==0):
      if (((type_var & 0xE0) == 0) | ((type_var & 0xE0) == 0x20)):
        FB_pt.new_var(str(pt_var)+'_const',fb_conf_c[pt_byte],type_var&0x03)
        pt_byte +=1
      elif((type_var&0xE0 == 0x40)):
        FB_pt.new_var(str(pt_var)+'_const',fb_conf_c[pt_byte]<<8|fb_conf_c[pt_byte+1],type_var&0x03)
        pt_byte +=2
      elif((type_var&0xE0 == 0x60)):
        FB_pt.new_var(str(pt_var)+'_const',(fb_conf_c[pt_byte]<<24)|(fb_conf_c[pt_byte+1]<<16)|(fb_conf_c[pt_byte+1]<<8)|(fb_conf_c[pt_byte+1]),type_var&0x03)
        pt_byte +=4
      elif((type_var&0xE0 == 0x80)):
        float_temp = float((fb_conf_c[pt_byte]<<24)|(fb_conf_c[pt_byte+1]<<16)|(fb_conf_c[pt_byte+1]<<8)|(fb_conf_c[pt_byte+1]))
        FB_pt.new_var(str(pt_var)+'_const',float_temp,type_var&0x03)
        pt_byte +=4
      elif((type_var&0xE0 == 0xA0)):
        time_temp = ((fb_conf_c[pt_byte]<<24)|(fb_conf_c[pt_byte+1]<<16)|(fb_conf_c[pt_byte+1]<<8)|(fb_conf_c[pt_byte+1]))
        FB_pt.new_var(str(pt_var)+'_const',time_temp,type_var&0x03)
        pt_byte +=4
    elif((type_var&0x04)==0x04):
      size_array = fb_conf_c[pt_byte]<<8|fb_conf_c[pt_byte+1]   
      pt_byte +=2
      addres_array = fb_conf_c[pt_byte]<<8|fb_conf_c[pt_byte+1]   
      pt_byte +=2
      FB_pt.new_var(str(pt_var)+'_'+'array'+'_'+str(size_array),addres_array,type_var&0x03)
    else:
      addres_array = fb_conf_c[pt_byte]<<8|fb_conf_c[pt_byte+1]         
      pt_byte +=2
      FB_pt.new_var(str(pt_var),addres_array,type_var&0x03)
    pt_var+=1
  print(len(FB_array))
  decompile = open('decompile.txt','w')
  i = 0
  while (i<len(FB_array)-1):
    write_property(FB_array[i+1],decompile)
    i+=1
  decompile.close()

#  print('configuration size',size_conf)
#  print('immanager size',size_im_conf)
#  print('fb size',size_fb_conf)
#  print(im_conf_c)
#  print(fb_conf_c)
  time_pr=time.time() - time_start
  print(time_pr)
#  print(im_two.input_variable,im_two.var_variable,im_two.out_variable) 
#  print(im_one.input_variable,im_one.var_variable,im_one.out_variable) 

class FB:
  def __init__(self):
    self.number = 0
    self.name = "noname"
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
