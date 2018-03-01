import sys
import struct
import time
import re

file_in = open(sys.argv[1], 'rb')
file_without_crc = open('w_' + sys.argv[1],'wb')
input_file = file_in.read()
input_file = input_file[4:-2]
file_without_crc.write(input_file)
file_without_crc.close()
file_in.close()

