import sys
import re


class SpaceType:
    """ storage structure info"""
    def __init__(self):
        self.space_type = "input"
        self.num = 0
        self.var_array = {1: ["", "", "", ""], }

    def add_var(self, name, type_var, size, description):
        self.var_array[self.num] = [name, type_var, size, description]
        self.num += 1

    def del_var_info(self):
        self.num = 0
HTML_DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">'
HTML_NAME = '<html><head><title>OwnNetworkVariable</title>'
HTML_CHARSET = '<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">'
HTML_CONTENT = '<meta http-equiv="refresh" content="60">'
HTML_CONTENT_NAME = '<meta content="MSHTML 6.00.2900.3698" name="GENERATOR">'
HTML_STYLE = '<style></style><!-- saved from url=(0038)http://192.168.1.232/sp.shtml --></head>'
HTML_TABLE_OPEN = '<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'

def main():
    """build fb description """
    fb_name = open('fb_name.txt', 'w')
    html_describe = open('html_describe.html', 'w')
    html_describe.write(HTML_DOCTYPE)
    html_describe.write(HTML_NAME)
    html_describe.write(HTML_CHARSET)
    html_describe.write(HTML_CONTENT)
    html_describe.write(HTML_CONTENT_NAME)
    html_describe.write(HTML_STYLE)
    html_describe.write('<body>')
    fb_name.write('Number FB and Name\n')
    current = 0
    start_structure = 0
    while 1:
        current += 1
        if current == 101:
            html_describe.write('</body></html>')
            sys.exit(1)
        try:
            if current <= 9:
                fb_temp = open('FB/fb0000'+str(current)+'.h')
            elif current <= 99:
                fb_temp = open('FB/fb000'+str(current)+'.h')
            else:
                fb_temp = open('FB/fb00'+str(current)+'.h')
        except IOError:
            continue
        description_structure = SpaceType()
        line_number = 0
        for line_full in fb_temp:
            try:
                if line_number == 0:
                    fb_name.write(fb_temp.name+'\n')
                    if (len(line_full)) > 2 & (line_full[0] == '/') & (line_full[1] == '*'):
                        fb_name.write(line_full)
                    else:
                        fb_name.write("didn't find description")

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
                            #write struct type
                            fb_name.write(description_structure.space_type+'\n')
                            for j in range(description_structure.num):
                                fb_name.write(description_structure.var_array[j][0]+' '
                                              + description_structure.var_array[j][1])
                                if description_structure.var_array[j][2]:
                                    fb_name.write(description_structure.var_array[j][2]+' ')
                                if description_structure.var_array[j][3]:
                                    fb_name.write(description_structure.var_array[j][3]+' ')
                                fb_name.write('\n')
                        else:
                            fb_name.write("type_structure_error"+line)
                        start_structure = 0
                        description_structure.del_var_info()
                    else:
                        p_var = re.compile\
                            ('^\s*Register_type\s+(?P<name>[\w\d]+)\s*(?P<size>\[[\d\w]+\])?\s*;'
                             '\s*(//)?\s*(?P<type>[bit,int,uint,\d,/]*)\s*(?P<description>[\w\W]*$)')
                        l = p_var.match(line_full)
                        if l:
                            r = p_var.search(line_full)
                            description_structure.add_var(r.group('name'), r.group('type'),
                                                          r.group('size'), r.group('description'))
            except IndexError:
                break
            line_number += 1


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
