#!/c/Python33/ python
import sys
import os
import _thread as thread
import threading
import socket
import atexit
import io
import serial
import time
import struct
import random
import msvcrt

"""
FB_MODBUS_Buffer[0] = IN->MODBUS_Addr.Data.uint8;     
FB_MODBUS_Buffer[1] = IN->MODBUS_Func.Data.uint8;     
FB_MODBUS_Buffer[2] = IN->RegAddr.Data.uint16 >> 8;   
FB_MODBUS_Buffer[3] = IN->RegAddr.Data.uint16 & 0xFF; 
FB_MODBUS_Buffer[4] = IN->RegNum.Data.uint16 >> 8;    
FB_MODBUS_Buffer[5] = IN->RegNum.Data.uint16 & 0xFF;  
CRC = crc16(FB_MODBUS_Buffer, LengthPak-2);
FB_MODBUS_Buffer[LengthPak-2] = (char)CRC;
FB_MODBUS_Buffer[LengthPak-1] = (char)(CRC>>8);
"""
"""
add addres property befor start program
"""

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


def udp_list(sock):
    while 1:
        data, address = sock.recvfrom(1024)
        print(address)
        print(data, len(data))
        data_s = []
        for i in range(0, len(data)):
            data_s.append(data[i])
        print(data_s)


def big_to_little(packet):
    for i in range(len(packet)//2):
        temp = packet[2*i]
        packet[2*i] = packet[2*i+1]
        packet[2*i+1] = temp


def com_list(ser):
    while 1:
        hello = ser.read(1)
        if hello != '':
            print(int.from_bytes(hello, byteorder='big'))


def main():
    have_serial = 1
    try:
        port_name = 'COM3'
        ser = serial.Serial(port_name)
        ser.baudrate = 115200
        print(ser.name)          # check which port was really used
        sys.stderr.write('--- Miniterm on %s: %d,%s,%s,%s ---\n' % (
            ser.portstr,
            ser.baudrate,
            ser.bytesize,
            ser.parity,
            ser.stopbits,
        ))
    except serial.SerialException as e:
        have_serial = 0
        print("could not open port ", port_name, "\n")
    mdb_tcp = [0x00, 0x03, 0x00, 0x00, 0x00, 0x04] #,6,3,0x00,0x3,0x00,1]#,0x04,0x04,0x21,0x05,0x00]
    mdb_address = 3
    mdb_command = 3
    start_address = 0
    reg_num = 8
    value = struct.unpack('<I', struct.pack('<f', 57.5))
    data = [(value[0] >> 8) & 0xff, value[0] & 0xff, (value[0] >> 24) & 0xff,
            (value[0] >> 16) & 0xff]
    value = struct.unpack('<I', struct.pack('<f', 58.5))
    data.append((value[0] >> 8) & 0xff)
    data.append((value[0]) & 0xff)
    data.append((value[0] >> 24) & 0xff)
    data.append((value[0] >> 16) & 0xff)
    mdb_tcp.append(mdb_address)
    mdb_tcp.append(mdb_command)
    mdb_tcp.append((start_address >> 8) & 0xff)
    mdb_tcp.append(start_address & 0xff)
    if mdb_command == 3 or mdb_command == 4 or mdb_command == 1:
        mdb_tcp.append((reg_num >> 8) & 0xff)
        mdb_tcp.append(reg_num & 0xff)
    elif mdb_command == 16:
        reg_num_bytes = len(data) & 0xffff
        reg_num = reg_num_bytes >> 1
        mdb_tcp.append((reg_num >> 8) & 0xff)
        mdb_tcp.append(reg_num & 0xff)
        mdb_tcp.append(reg_num_bytes & 0xff)
        for i in range(reg_num_bytes):
            mdb_tcp.append(data[i] & 0xff)

    elif mdb_command == 6:
        mdb_tcp.append(data[0] & 0xff)
        mdb_tcp.append(data[1] & 0xff)
    else:
        print('command not responde')
    print(mdb_tcp)

    ip_address = '192.168.1.232'
    tcp_port = 502
    udp_port = 7
    udp_port_self = 7
    buffer_size = 1512
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if have_serial:
        thread.start_new_thread(com_list, (ser, ))
        print('tread is start')
    good_transaction = 0
    bad_transaction = 0
    print('c - tcp connect\n'
          't - mdbtcp send(after connect)\n'
          'm - modbus RTU send over uart(open auto)\n'
          'u - modbus RTU send over udp(open auto)\n')
    arc_parse = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", udp_port_self))
    thread.start_new_thread(udp_list, (sock,))
    while 1:
        q = msvcrt.getch()
        print(q)
        if ord(q) == 113: #q
            s.close()
            sys.exit(1)
        elif ord(q) == 119: #w
            print(mdbwrite)
            ser.write(mdbwrite)
        elif ord(q) == 114: #r
            mdb_tcp_temp = bytearray(mdb_tcp[6:])
            crc = crc16(mdb_tcp_temp, len(mdb_tcp_temp))
            mdb_tcp_temp.append(crc & 0xFF)
            mdb_tcp_temp.append((crc >> 8) & 0xFF)
            print(mdb_tcp_temp[0:])
            s.send(mdb_tcp_temp)
            time_start = time.time()
            s.settimeout(5)
            data = s.recv(buffer_size)
            time_pr = time.time() - time_start
            data_s = []
            print(data)
            for i in range(0, len(data)):
                data_s.append(data[i])
            parse_mdb_response(data_s)
            print(data_s)
            print("length", len(data_s))
            print(time_pr, 'ms')

        elif ord(q) == 109: #m
            mdb_rtu = mdb_tcp[6:]
            crc = crc16(mdb_rtu, len(mdb_rtu))
            mdb_rtu.append(crc & 0xFF)
            mdb_rtu.append((crc >> 8) & 0xFF)
            print(mdb_rtu)

            if have_serial:
                ser.reset_input_buffer()
                ser.write(mdb_rtu)
        elif ord(q) == 117: #u
            mdb_rtu = mdb_tcp[6:]
            crc = crc16(mdb_rtu, len(mdb_rtu))
            mdb_rtu.append(crc & 0xFF)
            mdb_rtu.append((crc >> 8) & 0xFF)
            print(mdb_rtu)
            packet_str = bytearray(mdb_rtu[0:])
            sock.sendto(packet_str, (ip_address, udp_port))
        elif ord(q) == 99: #c
            s.connect((ip_address, tcp_port))
        elif ord(q) == 116: #t
            mdb_tcp_temp = bytearray(mdb_tcp[0:])
            print(mdb_tcp[0:])
            s.send(mdb_tcp_temp)
            time_start = time.time()
            s.settimeout(5)
            data = s.recv(buffer_size)
            time_pr = time.time() - time_start
            data_s = []
            print(data)
            for i in range(0, len(data)):
                data_s.append(data[i])
            parse_mdb_tcp_response(data_s)
            print(data_s)
            print("length", len(data_s))
            print(time_pr, 'ms')
        elif ord(q) == 108:#l
            while 1:
                mdb_rtu = mdb_tcp[6:]
                crc = crc16(mdb_rtu, len(mdb_rtu))                                                                                    
                mdb_rtu.append(crc & 0xFF)
                mdb_rtu.append((crc >> 8) & 0xFF)
                print(mdb_rtu)
                packet_str = bytearray(mdb_rtu[0:])
                sock.sendto(packet_str, (ip_address, udp_port))
                time.sleep(0.2)
                if msvcrt.kbhit():
                    q = msvcrt.getch()
                    print(ord(q))
                    if ord(q) == 113:#q
                        s.close()
                        sys.exit(1)


def parse_mdb_tcp_response(packet):
    parse_mdb_response(packet[6:])
    return


def parse_mdb_response(packet):
    print('address', packet[0], 'hex', hex(packet[0]))
    print('command', packet[1], 'hex', hex(packet[1]))
    if packet[1] == 3 or packet[1]== 4:
        print('response byte', packet[2], hex(packet[2]))
        for i in range(packet[2]//2):
            data = (packet[3+i*2] << 8) & 0xff00
            data |= (packet[3+i*2+1] & 0x00ff)
            print('data of regs', i, '= ', data, 'hex', hex(data))
    elif packet[1] == 16:
        address = (packet[2] << 8) & 0xff00
        address |= (packet[3] & 0x00ff)
        print('start address', address, 'hex', hex(address))
        number_write_reg = (packet[4] << 8) & 0xff00
        number_write_reg |= (packet[5] & 0x00ff)
        print('number_write_reg', number_write_reg, 'hex', hex(number_write_reg))

    elif packet[1] == 6:
        address = (packet[2] << 8) & 0xff00
        address |= (packet[3] & 0x00ff)
        print('start address', address, 'hex', hex(address))
        reg_value = (packet[4] << 8) & 0xff00
        reg_value |= (packet[5] & 0x00ff)
        print('reg_value', reg_value, 'hex', hex(reg_value))
    return

  
def check_error_packet(data):
    if len(data) == 9:
        print(data[-3:-1])
        if data[-2] == 132:
            return 1
    return 0


def rtm64_crc(pbuffer, length):
    """CRC16 for RTM64"""
    crc = 0x0000
    k = 0
    while k < length:
        crc = (crc ^ (((pbuffer[k]) << 8) & 0xFFFF))
        k += 1
        i = 8
        while i:
            i -= 1
            if crc & 0x8000:
                crc = (((crc << 1) & 0xFFFF) ^ 0x1021)
            else:
                crc = ((crc << 1) & 0xFFFF)
    return crc


def crc16(pck, length):
    """CRC16 for modbus"""
    crc = 0xFFFF
    i = 0
    while i < length:
        crc ^= pck[i]
        i += 1
        j = 0
        while j < 8:
            j += 1
            if (crc & 0x0001) == 1:
                crc = ((crc >> 1) & 0xFFFF) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def rtm64_check_sum(buffer, length):
    """ CheckSum RTM64"""
    sum = 0
    i = 0
    while i < length:
        sum = sum + buffer[i]
        i += 1
    return sum


def int_to_char(cmd_x):
    """char to string array confersion"""
    i = 0
    cmd_r = ['~']
    while i < len(cmd_x):
        cmd_r += chr(int(cmd_x[i]))
        i += 1
    return cmd_r[1:]


def char_to_int(cmd_x, length):
    i = 0
    cmd_r = [0 for x in range(length)]
    while i < length:
        cmd_r[i] = ord(str(cmd_x[i]))
        i += 1
    return cmd_r


def print_hex(cmd, length):
    hex = [0 for i in range(length)]
    i = 0
    while i < length:
        hex[i] = (hex(cmd[i]))
        i += 1
    print(hex)


if __name__ == "__main__":
    main()
