import fileinput
class str_class(object):
  def __init__(self,clear_line,restline):
    self.clear_line = clear_line
    self.restline = restline

def find_comment(str_object):
    global comment
    if comment:
        start = str_object.restline.find('*/')
        if start ==-1:
            return str_object
        else:
            comment = 0
            if start < len(str_object.restline)-3:
                str_object.restline = str_object.restline[start+2:]
                find_comment(str_object)
            else:
                return str_object
    else: 
        start = str_object.restline.find('/*')
        if start == -1:
            str_object.clear_line = str_object.clear_line + str_object.restline
            return str_object
        else :
            if start > 0:
                str_object.clear_line = str_object.clear_line + str_object.restline[:start]
                str_object.restline = str_object.restline[start+2:]
            comment = 1
            start = str_object.restline.find('*/')
            if start ==-1:
                return str_object
            else:
                comment = 0
                if start < len(str_object.restline)-3:
                    str_object.restline = str_object.restline[start+2:]
                    find_comment(str_object)
                else:
                    return str_object

    
def find_type(file_fb_name):
    global comment
    comment = 0
    buff = ''
    for line in fileinput.input(file_fb_name, inplace=1):
        if '//' in line:
            start = line.find('//')
            line_temp = line[:start]
        else:
            line_temp = line
        clear_line = ''
        str_object = str_class(clear_line,line_temp)
        find_comment(str_object)
        if len(str_object.clear_line):
            if str_object.clear_line[-1] == line[-1]:
                buff = buff + str_object.clear_line
            else:
                buff = buff + str_object.clear_line+'\n'
        print(line,end='')
    print(buff)


def main():
     find_type("test-.c")
if __name__ == "__main__":
    'test reqursive find'
    main()
