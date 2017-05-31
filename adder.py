import sys
import struct
import time
import re

def CheckCRC(line):
  tmpcrc = 0x0000
  time_start = time.time()
  for i in range(len(line)):
    tmpcrc = ((tmpcrc >> 8) | (tmpcrc << 8))&0xffff
    tmpcrc ^= (int(line[i])&0x00ff)
    tmpcrc ^= ((tmpcrc & 0xff)>>4 &0xffff)
    tmpcrc ^= ((tmpcrc << 12) &0xffff)
    tmpcrc ^= (((tmpcrc & 0xff)<<5)&0xffff)

  print('checking crc time - ',time.time()- time_start)
  return tmpcrc;



file_in = open(sys.argv[1], 'rb')
file_without_crc = open('new'+'.fb32','wb')
file_crc = open('new'+'_crc.fb32','wb')

length = 0x00000000
input_file = file_in.read()
length |= len(input_file)

file_in.seek(0)
print('length output file - ',length)
output = struct.pack('>I', length)
output += input_file[-4:]
crc = CheckCRC(output)
file_crc.write(input_file[-4:])
file_without_crc.write(input_file)
print('crc = ',hex(crc))
file_crc.write(struct.pack('>H', crc))
file_without_crc.close()
file_crc.close()
file_in.close()

