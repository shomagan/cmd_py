#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
import time
from pymodbus.client.sync import ModbusTcpClient
import logging
if __name__ == '__main__':
  client = ModbusTcpClient('192.168.2.231',port=502)
  logging.basicConfig()
  log = logging.getLogger()
  log.setLevel(logging.DEBUG)
  while 1:
    temps  = client.read_holding_registers(0,4,unit=8) # address, count, slave address
    if temps:
      print (temps.registers)
    time.sleep(0.5)
    if(msvcrt.kbhit()):
      q = msvcrt.getch()
      print(ord(q))
      if ord(q) == 113:#q
        client.close()
        sys.exit(1)

