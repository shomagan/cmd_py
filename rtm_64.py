# 7E 13 F0 1E 00 52 46 A0 8F 05 60 04 00 07 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 90 12 7E
"""
add addres property befor start program
"""
import sys, os, _thread as thread, threading, socket, atexit, io, serial, time
import struct

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt


def com_list(ser, a):
    while (1):
        hello = ser.read(1)
        if hello != '':
            a += 1
            error_log = open('recv_log.txt', 'a')
            if ord(hello) == 250:
                error_log.write('\n')
            error_log.write(str(hello))
            error_log.close()
            print(hello, ord(hello))


KodBit = 0x00
KodInt8 = 0x20
KodInt16 = 0x40
KodInt32 = 0x60
KodFloat32 = 0x80
KodTime32 = 0xA0
ValTypeName = {KodBit: "KodBit",
               KodInt8: "KodInt8",
               KodInt16: "KodInt16",
               KodInt32: "KodInt32",
               KodFloat32: "KodFloat32",
               KodTime32: "KodTime32"
}
ValType = {KodBit: 1,
           KodInt8: 1,
           KodInt16: 2,
           KodInt32: 4,
           KodFloat32: 4,
           KodTime32: 4
}


def main():
    ser = serial.Serial("COM2")  # open first serial port
    ser.baudrate = 115200
    print(ser.name)  # check which port was really used
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
    hello = 'hello'
    ser.write(serial.to_bytes([4]))
    TCP_IP = '192.168.1.232'
    TCP_PORT = 502
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World!"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a = 0
    thread.start_new_thread(com_list, (ser, a))
    print('tread is start')
    data = [2, 38,
            0]  # ,81,0,82,0,100,0]#,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
    data_p = [1, 0,
              1]  # ,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b]#,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00,0x0b,0x00]
    Packet = Rtm64()
    while 1:
        # if msvcrt.kbhit():
        q = msvcrt.getch()
        print(ord(q))
        if ord(q) == 113:  # q
            s.close()
            sys.exit(1)
        elif ord(q) == 97:  # a
            Packet.SendPacket(ser, 0)
        elif ord(q) == 99:  # c
            Packet.connect(TCP_IP, TCP_PORT)
        elif ord(q) == 115:  # s
            try:
                Packet.SendPacket(ser, 1)
            except OSError:
                print("Can't send tcp Packet")
        elif ord(q) == 108:  # l
            while (1):
                try:
                  Packet.SendPacket(ser, 1)
                except OSError:
                  print("Can't send tcp Packet")
                  error_log = open('error_log_rv.txt', 'a')
                  error_log.write("mega12 connect aborted TCP" + time.asctime() + '\n')
                  error_log.close()
                  try:
                    Packet.s.close()
                    Packet.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    Packet.s.connect((TCP_IP, TCP_PORT))
                  except TimeoutError:
                    print(time.asctime())
                    print("mega12 not TCP connected ")
                    error_log = open('error_log_rv.txt', 'a')
                    error_log.write("mega12 not TCP connected " + time.asctime() + '\n')
                    error_log.close()
                  except ConnectionAbortedError:
                    print(time.asctime())
                    print("mega12 connect aborted TCP")
                    error_log = open('error_log_rv.txt', 'a')
                    error_log.write("mega12 connect aborted TCP" + time.asctime() + '\n')
                    error_log.close()
                    s.connect((TCP_IP, TCP_PORT))
                print(time.asctime())
                time.sleep(0.02)
                if (msvcrt.kbhit()):
                  q = msvcrt.getch()
                  print(ord(q))
                  if ord(q) == 113:  #q
                    s.close()
                    sys.exit(1)


class Rtm64(object):
  def __init__(self):
    # 7E 03 F0 11 00 46 52 A0 8F 08 20 07 04 FE 00 32 2E 04 7E
    self.kod = 0x7e
    self.service_one = 0x03
    self.service_two = 0xF0
    self.len = 0x11
    self.flag = 0x00
    self.command = [0x46, 0x52]
    self.address = [[0xA0, 0x8f], [0x03, 0x20], [0x08, 0x20]]
    self.value = [0xFE, 0x00, 0x32]
    self.crc = 0x0000
    self.error_cnt = 0
    self.OkReceptionCnt = 0
  def __del__(self):
    if self.s:
      self.s.close()
    print("dlt packet")

  def SendPacket(self, ser, type):
    BUFFER_SIZE = 1024
    packet = [self.kod]
    packet.append(self.service_one)
    packet.append(self.service_two)
    packet.append(self.len)
    packet.append(self.flag)
    packet.append(self.command[0])
    packet.append(self.command[1])
    packet.append(self.address[0][0])
    packet.append(self.address[0][1])
    packet.append(self.address[1][0])
    packet.append(self.address[1][1])
    packet.append(self.address[2][0])
    packet.append(self.address[2][1])
    packet.append(self.value[0])
    packet.append(self.value[1])
    packet.append(self.value[2])
    self.len = len(packet) + 1
    packet[3] = self.len
    chek_sum = RTM64ChkSUM(packet[1:], len(packet) - 1)
    packet.append(chek_sum & 0xFF)
    packet.append((chek_sum >> 8) & 0xFF)
    packet.append(self.kod)
    if type == 1:
      packet_str = bytearray(packet[0:])
      print(packet_str)
      time_start = time.time()
      self.s.send(packet_str)
      self.s.settimeout(2)
      try:
        data = self.s.recv(BUFFER_SIZE)
        self.OkReceptionCnt += 1
        time_pr = time.time() - time_start
        data_s = []
        for i in range(0, len(data)):
          data_s.append(data[i])
        print(data_s, self.OkReceptionCnt)
        print(time_pr, 's')
        print(len(data))
      except socket.timeout:
        self.error_cnt += 1
        print("TCP_RecvError", self.error_cnt)
        print(time.asctime())
        error_log = open('error_log_rv.txt', 'a')
        error_log.write("TCP_ReceiveError" + time.asctime() + str(self.error_cnt) + '\n')
        error_log.close()
    elif (type == 0):
      print(packet)
      ser.write(packet)

  def connect(self, TCP_IP, TCP_PORT):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.s.connect((TCP_IP, TCP_PORT))
    except TimeoutError:
      print(time.asctime())
      print("mega12 not TCP connected ")
      error_log = open('error_log_rv.txt', 'a')
      error_log.write("mega12 not TCP connected " + time.asctime() + '\n')
      error_log.close()
    except ConnectionAbortedError:
      print(time.asctime())
      print("mega12 connect aborted TCP")
      error_log = open('error_log_rv.txt', 'a')
      error_log.write("mega12 connect aborted TCP" + time.asctime() + '\n')
      error_log.close()
      self.s.connect((TCP_IP, TCP_PORT))


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


def crc16(pck, len):
  """CRC16 for modbus"""
  CRC = 0xFFFF
  i = 0
  while ( i < len ):
    CRC ^= pck[i]
    i += 1
    j = 0
    while ( j < 8):
      j += 1
      if ( (CRC & 0x0001) == 1 ):
        CRC = ((CRC >> 1) & 0xFFFF) ^ 0xA001;
      else:
        CRC >>= 1;
  return (CRC & 0xFFFF)


def RTM64ChkSUM(pbuffer, Len):
  """ CheckSum RTM64"""
  sum = 0
  i = 0
  while (i < Len):
    sum = sum + pbuffer[i]
    i += 1
  return sum


def int_to_char(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ['~']
  while (i < len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i += 1
  return cmd_r[1:]


def list_to_str(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ''
  while (i < len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i += 1
  return cmd_r


def str_to_int(cmd_x, lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i < lenth):
    cmd_r[i] = ord(cmd_x[i])
    i += 1
  return cmd_r


def char_to_int(cmd_x, lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i < lenth):
    cmd_r[i] = ord(str(cmd_x[i]))
    i += 1
  return cmd_r


def print_hex(cmd, lenth):
  i = 0
  hexf = [0 for x in range(lenth)]
  while (i < lenth):
    hexf[i] = (hex(cmd[i]))
    i += 1
  print(hexf)


if __name__ == "__main__":
    main()
