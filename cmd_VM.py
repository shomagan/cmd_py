#7E 02 F0 0C 00 56 4D A0 8F 03 00 D3 02 7E 
import sys, os, threading, atexit,io,serial
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt as m
#def hextoascii():

def main():
  ser = serial.Serial(1)  # open first serial port
  print (ser.name)          # check which port was really used
  try:
    sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
      ser.portstr,
      ser.baudrate,
      ser.bytesize,
      ser.parity,
      ser.stopbits,
    ))
  except serial.SerialException as e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)
  ser.write("hello")      # write a string
  cmd_en = 0
  while 1:
    hello = ser.readline(ser.inWaiting())
    if (hello == '~'): 
      if (cmd_en == 0):
        cmd_en = 1
        cmd = hello
      else: 
        cmd += hello
        cmd_en = 0
        print(cmd)
    elif (hello != ''):
      cmd += hello  
    if m.kbhit() == 1:
      q = m.getche()
      if q == 'q':
        sys.exit(1)
      elif q=='w':
#        cmd_VM_str =str(int(0x7E,16),int(0x02,16),int(0xF0,16),int(0x0C,16),int(0x00,16),int(0x56,16),int(0x4D,16),
#                      int(0xA0,16),int(0x8F,16),int(0x08,16),int(0x00,16),int(0xD3,16),int(0x02,16),int(0x7E,16))  
        cmd_VM_str =chr(int(0x7E))+chr(int(0x02))+chr(int(0xF0))+chr(int(0x0C))+chr(int(0x00))+chr(int(0x56))+chr(int(0x4D))+chr(int(0xA0))+chr(int(0x8F))+chr(int(0x03))+chr(int(0x00))+chr(int(0xD3))+chr(int(0x02))+chr(int(0x7E))  
        ser.write(cmd_VM_str)
        sys.stderr.write(cmd_VM_str)
if __name__ == "__main__":
    main()