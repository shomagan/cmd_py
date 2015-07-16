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

HTML_DOCTYPE = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">'
HTML_NAME = '<html><head><title>fb describe</title>'
HTML_CHARSET = '<meta charset="cp1251">'
HTML_CONTENT = '<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">'
HTML_CONTENT_NAME = '<meta content="MSHTML 6.00.2900.3698" name="GENERATOR">'
HTML_STYLE = '<style></style><!-- saved from url=(0038)http://192.168.1.232/sp.shtml --></head>'
HTML_TABLE_OPEN = '<table style="width: 961px; height: 30px;" border="1" cellpadding="1" cellspacing="1">'

def main():
    """build fb description """
    fb_name = open('fb_name.txt', 'w')
    fb_html_describe = open('html_describe.html', 'w')
    fb_html_describe.write(HTML_DOCTYPE)
    fb_html_describe.write(HTML_NAME)
    fb_html_describe.write(HTML_CHARSET)
    fb_html_describe.write(HTML_CONTENT)
    fb_html_describe.write(HTML_CONTENT_NAME)
    fb_html_describe.write(HTML_STYLE)
    fb_html_describe.write('<body>'+'\n')
    fb_name.write('Number FB and Name\n')
    current = 0
    start_structure = 0
    while 1:
        current += 1
        if current == 101:
            fb_html_describe.write('</table>'+'\n')
            fb_html_describe.write('</body></html>')
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
                        fb_html_describe.write('<table style="width: 961px; height: 30px;" '
                                               'border="1" cellspacing="1">'+'\n')
                        fb_html_describe.write('<tr>'+'\n')
                        fb_html_describe.write('<td style="font-weight:font-style:italic;font-family:Verdana;'
                                               'background-color:rgb(0,251,213);"><small><span style="color:black;">'+'\n')
                        fb_html_describe.write(fb_temp.name+line_full+'</span> </small></td>')
                        fb_html_describe.write('</tr>'+'\n')
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
                            if description_structure.space_type == 'IN':
                                for l in range(description_structure.num):
                                    description_structure.in_array[l] = description_structure.temp_array[l]
                            elif description_structure.space_type == 'VAR':
                                for l in range(description_structure.num):
                                    description_structure.var_array[l] = description_structure.temp_array[l]
                            elif description_structure.space_type == 'OUT':
                                for l in range(description_structure.num):
                                    description_structure.out_array[l] = description_structure.temp_array[l]
                            #write struct type
                            fb_name.write(description_structure.space_type+'\n')
                            for j in range(description_structure.num):
                                fb_name.write(description_structure.temp_array[j][0]+' '
                                              + description_structure.temp_array[j][1])
                                if description_structure.temp_array[j][2]:
                                    fb_name.write(description_structure.temp_array[j][2]+' ')
                                if description_structure.temp_array[j][3]:
                                    fb_name.write(description_structure.temp_array[j][3]+' ')
                                fb_name.write('\n')
                        else:
                            fb_name.write("type_structure_error"+line)
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
        lenght = len(description_structure.in_array)
        if len(description_structure.var_array) > lenght:
            lenght = len(description_structure.var_array)
        if len(description_structure.out_array) > lenght:
            lenght = len(description_structure.out_array)
        for i in range(lenght):
            fb_html_describe.write('<tr>'+'\n')
            fb_html_describe.write('<td ><small><span style="color:black;">'+'\n')
            if i < len(description_structure.in_array):
                if description_structure.in_array[i][0]:
                    fb_html_describe.write(description_structure.in_array[i][0]+' ')
                if description_structure.in_array[i][1]:
                    fb_html_describe.write(description_structure.in_array[i][1]+' ')
                if description_structure.in_array[i][2]:
                    fb_html_describe.write(description_structure.in_array[i][2]+' ')
                if description_structure.in_array[i][3]:
                    fb_html_describe.write(description_structure.in_array[i][3]+' ')

            fb_html_describe.write('</span> </small></td>')
            fb_html_describe.write('<td ><small><span style="color:black;">'+'\n')
            if i < len(description_structure.var_array):
                if description_structure.var_array[i][0]:
                    fb_html_describe.write(description_structure.var_array[i][0]+' ')
                if description_structure.var_array[i][1]:
                    fb_html_describe.write(description_structure.var_array[i][1]+' ')
                if description_structure.var_array[i][2]:
                    fb_html_describe.write(description_structure.var_array[i][2]+' ')
                if description_structure.var_array[i][3]:
                    fb_html_describe.write(description_structure.var_array[i][3]+' ')
            fb_html_describe.write('</span> </small></td>')
            fb_html_describe.write('<td ><small><span style="color:black;">'+'\n')
            if i < len(description_structure.out_array):
                if description_structure.out_array[i][0]:
                    fb_html_describe.write(description_structure.out_array[i][0]+' ')
                if description_structure.out_array[i][1]:
                    fb_html_describe.write(description_structure.out_array[i][1]+' ')
                if description_structure.out_array[i][2]:
                    fb_html_describe.write(description_structure.out_array[i][2]+' ')
                if description_structure.out_array[i][3]:
                    fb_html_describe.write(description_structure.out_array[i][3]+' ')
            fb_html_describe.write('</span> </small></td>')
            fb_html_describe.write('</tr>'+'\n')
        description_structure.del_var_info()




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
