import CRCCCITT


def main():
  buff = [0x11,0x03,0x00,0x01]
  crc = RTM64CRC16(buff, 4)
  print(hex(crc))
  crc_CCITT = CRCCCITT.CRCCCITT()
  temp_buff = bytearray(buff[0:]) 
  print(temp_buff)
  crc = crc_CCITT.calculate(temp_buff)
  print(hex(crc))
  
def RTM64CRC16(pbuffer, Len):
  """CRC16 for RTM64"""
  CRC = 0x0000
  k = 0
  while (k < Len):
    CRC = (CRC ^ ((pbuffer[k] << 8) & 0xFFFF))
    k += 1
    i = 8
    while (i):
      i -= 1
      if (CRC & 0x8000):
        CRC = (((CRC << 1) & 0xFFFF) ^ 0x1021)
      else:
        CRC = ((CRC << 1) & 0xFFFF)
  return CRC
if __name__=="__main__":
  main()