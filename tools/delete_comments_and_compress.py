import re
import optparse

def remove_comment( text ) :
    def blot_out( strin ) :  # Return a string containing only the newline chars contained in strIn
        return ""# + ("\n" * strin.count('\n'))
    def replacer( match ) :
        s = match.group(0)
        if s.startswith('/'):  # Matched string is //...EOL or /*...*/  ==> Blot out all non-newline chars
            return blot_out(s)
        else:                  # Matched string is '...' or "..."  ==> Keep unchanged
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE)
    return re.sub(pattern, replacer, text)

def remove_empty_lines(text):
    pattern = re.compile(r'^\s*\n',re.DOTALL|re.MULTILINE)
    return re.sub(pattern, "", text)

def compress_if_else_statement(text):
    pattern_if = re.compile(r'if\s*(.+)\n\s*{',re.MULTILINE)
    pattern_else = re.compile(r'}\s*\n\s*else\s*\n\s*{',re.MULTILINE)
    first_step = re.sub(pattern_if, "if\g<1>{", text)
    second_step = re.sub(pattern_else, "}else{", first_step)
    return second_step


def main():
    parser = optparse.OptionParser(
            usage="",
            description=""
    )
    group = optparse.OptionGroup(parser, "Port settings")
    group.add_option("-f","--file",
                     dest="code_file",
                     action="store",
                     help="chose you file",
                     default='SwcFaultMgr_Common.c'
                     )
    parser.add_option_group(group)
    (options, args) = parser.parse_args()
    file_to_read = open(options.code_file,"r")
    base_file = file_to_read.read()
    file_to_write = open("RWD_"+options.code_file,"w")
    file_to_write_full = open("RWDF_"+options.code_file,"w")
    file_to_write.write(remove_comment(base_file))
    without_comment = remove_comment(base_file)
    without_comment = remove_empty_lines(without_comment)
    file_to_write_full.write(compress_if_else_statement(without_comment))
    file_to_read.close()
    file_to_write.close()
    file_to_write_full.close()
if __name__ == '__main__':
    ''' delete comments '''
    main()   
