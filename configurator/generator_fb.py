import sys
import re
import matplotlib.pyplot as plt
import networkx as nx
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
ITERABLE_TEMPLATE = '^\s*((while)|(for)|(if)|(else\s*(if)*)|(switch))'
ANYTHING_TEMPLATE = '\s*[\d\w]'
class GraphType:
    """Position control"""
    def __init__(self):
        self.current_position = [0, 0]
        self.position = {}
        self.label_position = {}

    def node(self, label):
        self.current_position[1] -= 0.5
        label = str(self.current_position[1])+label
        self.position[label] = (self.current_position[0], self.current_position[1])
    def label(self, label):
        self.current_position[1] -= 0.5
        label = str(self.current_position[1])+label
        self.label_position[label] = (self.current_position[0], self.current_position[1])

    def clear(self):
        self.current_position = [0, 0]
        self.position = {}

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
    start_structure = 0
    comment = 0
    G = nx.MultiGraph()
    graph = GraphType()

    while 1:
        current += 1
        graph.clear()
        G.clear()
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
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)
                    G.add_nodes_from(graph.position.keys())
                    size = abs(graph.current_position[1])
                    plt.figure(figsize=(size, size))
                    nx.draw_networkx_nodes(G, graph.position, node_size=500, node_color='w')
                    max_position_x = 0
                    for key in graph.position:
                        if graph.position[key][0] > max_position_x:
                            max_position_x = graph.position[key][0]
                        graph.position[key] = (graph.position[key][0], graph.position[key][1]+0.3)
                    nx.draw_networkx_labels(G, graph.position, font_family='sans-serif')
                    max_position_y = abs(graph.current_position[1])
                    variable = variable_fb.find(current)
                    graph.clear()
                    G.clear()
                    dY = max_position_y/len(variable.in_array)
                    if dY < 1:
                        dY = 1
                    graph.current_position[0] = 0

                    for key in variable.in_array:
                        graph.current_position[1] -= dY
                        graph.node(variable.in_array[key][0])
                    G.add_nodes_from(graph.position.keys())
                    nx.draw_networkx_nodes(G, graph.position, node_size=500, node_color='w')
                    nx.draw_networkx_labels(G, graph.position, font_family='sans-serif')
                    plt.axis('off')
                    plt.savefig(name+".rw") # save as png
                elif function_name_r in line_full:
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)





def find_iterable(fb_temp, fb_html_describe, line_current, graph):
    graph.current_position[0] += 1
    fb_html_describe.write('<tr><td valign=TOP>'+'\n')
    fb_html_describe.write('<table border=1 cellspacing=0 cellpadding=8 >'+'\n')
    fb_html_describe.write('<tr>'+'\n')
    fb_html_describe.write('<td style="font-weight:font-style:italic;font-family:Verdana;>'
                           '<small><span style="color:black;">'+'\n')
    fb_html_describe.write(line_current+'</span> </small></td>')
    fb_html_describe.write('</tr>'+'\n')
    graph.node(line_current)
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
                graph.current_position[0] -= 1
                close_space(fb_html_describe)
                if '{' in line_full:
                    find_iterable(fb_temp, fb_html_describe, line_full, graph)
                return
            iterable_type = re.compile(ITERABLE_TEMPLATE)
            start_place = iterable_type.match(line_full)
            if start_place:
                condition = line_full
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
                                graph.current_position[0] -= 1
                                return
                            elif ones_condition:
                                graph.current_position[0] += 1
                                graph.current_position[1] -= 0.5
                                graph.node(condition)
                                graph.current_position[0] -= 1
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
