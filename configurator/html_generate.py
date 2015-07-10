import sys, os, atexit,io
#def hextoascii():

def main():
  fb_name = open('fb_name.txt','w')
  fb_dexcribe = open('fb_name.html','w')
  fb_name.write ('Number FB and Name\n')
  current = 0
  name = 0
  struct = 0
  while 1:
    struct_number = 0
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
    for linefull in fb_temp:
      try:
        if ((linefull[0] == '/') & (linefull[1] == '*')):
          fb_name.write (str(current)+' '+line)

        if('//' in linefull):
          start = linefull.find('//')
          line = linefull[:start]
        else:
          line = linefull
        if struct == 0:
          p_struct = re.compile('^\s*typedef\s*struct\W')
          if re.search(p_struct,line):
            struct = 1
            Space_Type[struct_number] = Space_Type()

        else :
          if (struct == 1 & ('}'in line)):
            p_type = re.compile('fb(?P<number>[\d]{5})\_(?P<type>[\w]{2;3})\_type')
            struct_close = p_type.match(line)
            if struct_close:
              l = p_type.search(line)
              Space_Type[struct_number].space_type = l.group('type')
              struct = 0
          else:
            p_type = re.compile('fb(?P<number>[\d]{5})\_(?P<type>[\w]{2;3})\_type')
            p_var = re.compile('^\s*Register\_type\s+(?P<name>[\w\d]+)\s*(\[(?P<size>[\d\w]+)\])?\s*\;')
	 Inputs[MaxInputs];
            SP_b.check(linefull)
            if SP_b.SizeArray:
              SP_b.save(OwnVariableFile,HtmlFile,HtmlDescribe,TagStructFile)
              SP_b.SP_Numm+=1

      except IndexError:break

class Space_Type:
  def __init__(self):
    self.space_type = "input"
    self.num = 0
    self.var_array = {1:"",}
  def add_var(self,line):
    self.var_array[self.num] = line
    self.num +=1


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
