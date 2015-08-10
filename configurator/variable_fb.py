import sys
import re


class SpaceType:
    """ storage structure info"""
    def __init__(self):
        self.space_type = "input"
        self.num = 0
        self.temp_array = {0: [" ", " ", " ", " "], }
        self.in_array = {0: [" ", " ", " ", " "], }
        self.var_array = {0: [" ", " ", " ", " "], }
        self.out_array = {0: [" ", " ", " ", " "], }

    def add_var(self, name, type_var, size, description):
        self.temp_array[self.num] = [name, type_var, size, description]
        self.num += 1

    def del_var_info(self):
        self.temp_array = {0: [" ", " ", " ", " "], }
        self.in_array = {0: [" ", " ", " ", " "], }
        self.var_array = {0: [" ", " ", " ", " "], }
        self.out_array = {0: [" ", " ", " ", " "], }


def find(numm):
    """build fb description """
    start_structure = 0
    try:
        if numm <= 9:
            fb_temp = open('FB/fb0000'+str(numm)+'.h')
        elif numm <= 99:
            fb_temp = open('FB/fb000'+str(numm)+'.h')
        else:
            fb_temp = open('FB/fb00'+str(numm)+'.h')
    except IOError:
        return
    description_structure = SpaceType()
    line_number = 0
    for line_full in fb_temp:
        try:
            if '//' in line_full:
                start = line_full.find('//')
                line = line_full[:start]
            else:
                line = line_full
            if start_structure == 0:
                p = re.compile('^\s*typedef\s*(volatile)?\s*struct\W')
                if p.match(line):
                    start_structure = 1
            else:
                if start_structure == 1 & ('}'in line):
                    p_type = re.compile('^\s*\}\s*((fb)|(FB))(?P<number>[\d]{5})_(?P<type>[\w]{2,3})_type')
                    structure_close = p_type.match(line)
                    if structure_close:
                        l = p_type.search(line)
                        description_structure.space_type = l.group('type')
                        if description_structure.space_type == 'IN':
                            for l in range(description_structure.num):
                                description_structure.in_array[l] = description_structure.temp_array[l]
                        elif description_structure.space_type == 'VAR':
                            for l in range(description_structure.num):
                                description_structure.var_array[l] = description_structure.temp_array[l]
                        elif description_structure.space_type == 'OUT':
                            for l in range(description_structure.num):
                                description_structure.out_array[l] = description_structure.temp_array[l]
                    start_structure = 0
                    description_structure.num = 0
                else:
                    p_var = re.compile('^\s*Register_type\s+(?P<name>[\w\d]+)\s*(?P<size>\[[\d\w]+\])?\s*;'
                                       '\s*(//)?\s*(?P<type>[bit,int,uint,\d,/]*)\s*(?P<description>[\w\W]*$)')
                    l = p_var.match(line_full)
                    if l:
                        r = p_var.search(line_full)
                        description_structure.add_var(r.group('name'), r.group('type'),
                                                      r.group('size'), r.group('description'))
        except IndexError:
            break
        line_number += 1
    return description_structure





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
