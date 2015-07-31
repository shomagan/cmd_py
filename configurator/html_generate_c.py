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
ITERABLE_TEMPLATE = '(while)|(for)|(if)|(else\s*if)|(switch)'
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
    comment = 0
    while 1:
        current += 1
        if current == 108:
            fb_html_describe.write('</table>'+'\n')
            fb_html_describe.write('</body></html>')
            sys.exit(1)
        try:
            if current <= 9:
                fb_temp = open('FB/fb0000'+str(current)+'.c')
            elif current <= 99:
                fb_temp = open('FB/fb000'+str(current)+'.c')
            else:
                fb_temp = open('FB/fb00'+str(current)+'.c')
        except IOError:
            continue
        fb_name.write(fb_temp.name+'\n')
        line_full = fb_temp.readline()
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

        find_iterable(fb_temp)



def find_iterable(fb_temp):
    line_full = fb_temp.readline()
    while line_full:
        if '//' in line_full:
            start = line_full.find('//')
            line_full = line_full[:start]
        if '/*' in line_full:
            comment = 1
        if comment:
            if '*/' in line_full:
                comment = 0
        else:
            if ITERABLE_TEMPLATE in line_full:

        line_full = fb_temp.readline()


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
