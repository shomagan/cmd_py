#!/c/Python33/ python
import rtm_mw,sys
import msvcrt
import time
import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

if __name__ == '__main__':
  import logging
  logging.basicConfig()
  log = logging.getLogger()
  log.setLevel(logging.DEBUG)
  client= ModbusClient(method = "rtu", port=1,stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200)

  #connect to the serial modbus server
  connection = client.connect()
  print (connection)

  while 1:
    response = client.read_input_registers(3, 4, unit=0x03) # address, count, slave address
    if response:
      print (response.registers)
    time.sleep(0.1)
    if(msvcrt.kbhit()):
      q = msvcrt.getch()
      print(ord(q))
      if ord(q) == 113:#q
        client.close()
        sys.exit(1)


#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from


#starting add, num of reg to read, slave unit.


