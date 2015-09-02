import sys
import re
import variable_fb

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
ITERABLE_TEMPLATE = '^\s*(\})?\s*((while)|(for)|(if)|(else\s*(if)*)|(switch))'

ANYTHING_TEMPLATE = '\s*[\d\w]'
class GraphType:
    """Position control"""
    def __init__(self):
        self.current_position = [80, 0]
        self.position = []
        self.links = []
        self.node_number = 0

    def add_node(self, label):
        #ITERABLE_TEMPLATE_FULl = '^\s*(?P<operator>((while)|(for)|(if)|(else\s*(if)*)|(switch))\s*[\w\W]*)?$'
        label = label.replace("\n", "")
        label = label.replace("\\", "")
        label = label.replace("\t", "")
        if "if" in label:
            self.position.append((label, self.current_position[0], self.current_position[1], self.node_number, 1))
        elif "else" in label:
            self.position.append((label, self.current_position[0], self.current_position[1], self.node_number, 2))
        elif "for" in label:
            self.position.append((label, self.current_position[0], self.current_position[1], self.node_number, 3))
        elif "while" in label:
            self.position.append((label, self.current_position[0], self.current_position[1], self.node_number, 4))
        self.node_number += 1
        self.current_position[1] += 20
    def add_var(self, label):
        self.position.append((label, self.current_position[0], self.current_position[1], self.node_number, 5))
        self.node_number += 1
        self.current_position[1] += 20
    def add_link(self, node1, node2):
        self.links.append((node1, node2))
    def label(self, label):
        label = label.replace("\n", "")
        label = label.replace("\\", "")
        label = label.replace("\t", "")
        self.position.append((label, self.current_position[0], self.current_position[1], self.node_number,8))
        self.node_number += 1
        self.current_position[1] += 20
    def clear(self):
        self.current_position = [0, 0]
        self.position = []
        self.links = []
        self.node_number = 0

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
    current = 65
    comment = 0
    graph = GraphType()

    while 1:
        current += 1
        graph.clear()
        if current == 69:
            fb_html_describe.write('</table>'+'\n')
            fb_html_describe.write('</body></html>')
            fb_html_describe.write('</tr>'+'\n')
            fb_html_describe.write('</td>'+'\n')
            sys.exit(1)
        try:
            if current <= 9:
                name = 'fb0000'+str(current)
                fb_temp = open('FB/' + name + '.c')
            elif current <= 99:
                name = 'fb000'+str(current)
                fb_temp = open('FB/'+name + '.c')
            else:
                name = 'fb00'+str(current)
                fb_temp = open('FB/'+name + '.c')
        except IOError:
            continue
        fb_name.write(fb_temp.name+'\n')
        line_full = fb_temp.readline()
        if (len(line_full)) > 2 & (line_full[0] == '/') & (line_full[1] == '*'):
            fb_html_describe.write('<table border=1 cellspacing=0 cellpadding=0>'+'\n')
            fb_html_describe.write('<tr>'+'\n')
            fb_html_describe.write('<td style="font-weight:font-style:italic;font-family:Verdana;>'
                                   '<small><span style="color:black;">'+'\n')
            fb_html_describe.write(fb_temp.name+line_full+'</span> </small></td>')
            fb_html_describe.write('</tr>'+'\n')
            fb_html_describe.write('<tr><td valign=TOP>'+'\n')
            fb_name.write(line_full)
        else:
            fb_name.write("didn't find description")
        for line_full in fb_temp:
            if '//' in line_full:
                start = line_full.find('//')
                line_full = line_full[:start]
            if '/*' in line_full:
                comment = 1
            if comment:
                if '*/' in line_full:
                    comment = 0
            else:
                function_name = name + '_exec'
                function_name_r = name.upper() + '_exec'
                if function_name in line_full:
                    graph.current_position[1] = 20
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)
                    max_position_x = 0
                    max_position_y = graph.current_position[1]
                    json_file = open(name+'.json', 'w')
                    json_file.write('{"nodes":[')
                    variable = variable_fb.find(current)
                    dY = max_position_y/len(variable.in_array)
                    if dY < 1:
                        dY = 1
                    graph.current_position[0] = 40
                    graph.current_position[1] = 40
                    for key in variable.in_array:
                        graph.current_position[1] += dY
                        graph.add_var(variable.in_array[key][0])
                        add_links(variable.in_array[key][0], graph, len(graph.position))
                    for i in range(len(graph.position)):
                        json_file.write('{"name":'+'"'+graph.position[i][0]+'"'+',"group":'+str(graph.position[i][4])+',"x":'+str(graph.position[i][1])+
                                        ',"y":'+str(graph.position[i][2])+',"pos":'+str(graph.position[i][3])+'},\n')
                    json_file.write('{"name":"close","group":8,"x":0,"y":'+str(max_position_y)+'}],\n"links":[')
                    for i in range(len(graph.links)):
                        json_file.write('{"source":'+str(graph.links[i][0])+',"target":'+str(graph.links[i][1])+','+'"value":1},\n')
                    graph.clear()
                    json_file.write('{"source":1,"target":0,"value":1}\n]}')
                    # {"source":1,"target":0,"value":1},
                    json_file.close()
                elif function_name_r in line_full:
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)





def find_iterable(fb_temp, fb_html_describe, line_current, graph):
    graph.current_position[0] += 40
    fb_html_describe.write('<tr><td valign=TOP>'+'\n')
    fb_html_describe.write('<table border=1 cellspacing=0 cellpadding=8 >'+'\n')
    fb_html_describe.write('<tr>'+'\n')
    fb_html_describe.write('<td style="font-weight:font-style:italic;font-family:Verdana;>'
                           '<small><span style="color:black;">'+'\n')
    fb_html_describe.write(line_current+'</span> </small></td>')
    fb_html_describe.write('</tr>'+'\n')
    graph.add_node(line_current)
    if '{' in line_current:
        start_c = line_current.find("{")
        find_c = line_current.find("}", start_c)
        if find_c != -1:
            graph.current_position[0] -= 40
            close_space(fb_html_describe)
            return
    comment = 0
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
            if '}' in line_full:
                start_c = line_full.find("{")
                if start_c != -1:
                    find_c = line_full.find("}", 0, start_c)
                    if find_c != -1:
                        graph.current_position[0] -= 40
                        close_space(fb_html_describe)
                    else:
                        find_iterable(fb_temp, fb_html_describe, line_full, graph)
                        line_full = fb_temp.readline()
                else:
                    graph.current_position[0] -= 40
                    close_space(fb_html_describe)
                    return


            iterable_type = re.compile(ITERABLE_TEMPLATE)
            start_place = iterable_type.match(line_full)
            if start_place:
                number_hooks = find_condition_hooks(line_full)
                condition = line_full
                if number_hooks != 0:
                    line_full = fb_temp.readline()
                    number_hooks += find_condition_hooks(line_full)
                    condition += line_full
                    if number_hooks != 0:
                        line_full = fb_temp.readline()
                        number_hooks += find_condition_hooks(line_full)
                        condition += line_full
                if '{' in line_full:
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)
                else:
                    while 1:
                        line_full = fb_temp.readline()
                        anything = re.compile(ANYTHING_TEMPLATE)
                        if '//' in line_full:
                            start = line_full.find('//')
                            line_full = line_full[:start]
                        if '/*' in line_full:
                            comment = 1
                        if comment:
                            if '*/' in line_full:
                                comment = 0
                        else:
                            ones_condition = anything.match(line_full)
                            if '{' in line_full:
                                find_iterable(fb_temp, fb_html_describe,  condition, graph)
                                break
                            elif '}' in line_full:
                                close_space(fb_html_describe)
                                graph.current_position[0] -= 40
                                return
                            elif ones_condition:
                                graph.current_position[0] += 40
                                graph.current_position[1] += 20
                                graph.add_node(condition)
                                graph.current_position[0] -= 40
                                fb_html_describe.write('<tr><td valign=TOP>'+'\n')
                                fb_html_describe.write('<table border=1 cellspacing=0 cellpadding=8 >'+'\n')
                                fb_html_describe.write('<tr>'+'\n')
                                fb_html_describe.write('<td style="font-weight:font-style:italic;font-family:Verdana;>'
                                                       '<small><span style="color:black;">'+'\n')
                                fb_html_describe.write(condition+'</span> </small></td>')
                                fb_html_describe.write('</tr>'+'\n')
                                close_space(fb_html_describe)
                                break
            graph.label(line_full)
        line_full = fb_temp.readline()


def close_space(fb_html_describe):
    fb_html_describe.write('</table>'+'\n')
    fb_html_describe.write('</td>'+'\n')
    fb_html_describe.write('</tr>'+'\n')


def find_condition_hooks(line):
    pattern_open = re.compile("\(")
    pattern_close = re.compile("\)")
    open_num = len(pattern_open.findall(line))
    close_num = len(pattern_close.findall(line))
    return open_num - close_num


def add_links(name, graph, length):
    for i in range(length):
        node = 'IN->'+name
        if node in graph.position[i][0]:
            graph.add_link((length-1), graph.position[i][3])



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
