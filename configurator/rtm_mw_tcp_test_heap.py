#!/c/Python33/ python
"""
add addres property befor start program
"""
import sys
import socket
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None
import msvcrt


def data_gen():
    t = data_gen.t
    time_start = data_gen.time_start
    data_error = data_gen.data_error
    successful_packet = data_gen.successful_packet
    connection_error = data_gen.connection_error
    reset = data_gen.reset
    avail = data_gen.avail
    used = data_gen.used
    max_used = data_gen.max_used

    TCP_IP = '192.168.1.232'
    TCP_PORT = 502
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = [2,75,0,135,0,136,0,137,0]
    packet = RTM_MW(data)
    packet.Chan = 0x01
    try:
        s.connect((TCP_IP, TCP_PORT))
    except TimeoutError:
        print(time.asctime())
        print("mega12 not TCP connected ")
        connection_error += 1
        error_log = open('error_log_TCP.txt', 'a')
        error_log.write("mega12 not TCP connected "+time.asctime()+'\n')
        error_log.close()
    except ConnectionAbortedError:
        print(time.asctime())
        print("mega12 connect aborted TCP")
        connection_error += 1
        error_log = open('error_log_TCP.txt', 'a')
        error_log.write("mega12 connect aborted TCP"+time.asctime()+'\n')
        error_log.close()
        s.connect((TCP_IP, TCP_PORT))
    while 1:
        try:
            data_buf = packet.send_packet(s, 1)
            if data_buf:
                str_temp = packet.chek_packet(data_buf)
                reset  = packet.DataInPacket[1] | (packet.DataInPacket[2]<<8)
                avail = packet.DataInPacket[3] | (packet.DataInPacket[4]<<8)
                used = packet.DataInPacket[5] | (packet.DataInPacket[6]<<8)
                max_used = packet.DataInPacket[7] | (packet.DataInPacket[8]<<8)
                if len(packet.DataInPacket) != 5:
                    str_temp += 'DataInPacket_Error'
                if str_temp:
                    print(str_temp)
                    data_error += 1
                    error_log = open('error_log_TCP.txt', 'a')
                    error_log.write(str_temp+str(packet.DataInPacket)+time.asctime()+'\n')
                    error_log.close()
                else:
                    successful_packet += 1
        except OSError:
            print("Can't send tcp Packet")
            connection_error += 1
            error_log = open('error_log_TCP.txt', 'a')
            error_log.write("mega12 connect aborted TCP"+time.asctime()+'\n')
            error_log.close()
            try:
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
            except TimeoutError:
                print(time.asctime())
                print("mega12 not TCP connected ")
                error_log = open('error_log_TCP.txt','a')
                error_log.write("mega12 not TCP connected "+time.asctime()+'\n')
                error_log.close()
            except ConnectionAbortedError:
                print(time.asctime())
                print("mega12 connect aborted TCP")
                error_log = open('error_log_TCP.txt','a')
                error_log.write("mega12 connect aborted TCP"+time.asctime()+'\n')
                error_log.close()
                s.connect((TCP_IP, TCP_PORT))

        print(time.asctime())
        if msvcrt.kbhit():
            q = msvcrt.getch()
            print(ord(q))
            if ord(q) == 113:#q
                s.close()
                sys.exit(1)
        t = time.time() - time_start
        yield t, reset, avail, used, max_used,


def main():
    font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }
    data_gen.time_start = time.time()
    data_gen.t = 0
    data_gen.data_error = 0
    data_gen.successful_packet = 0
    data_gen.connection_error = 0
    data_gen.reset = 0
    data_gen.avail = 0
    data_gen.used = 0
    data_gen.max_used = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False)
    #fig, ax = plt.subplots()

    line_reset, = ax.plot([], [], lw=2, label='reset')
    line_avail, = ax.plot([], [], lw=2, label='availble memory for lwip')
    line_used, = ax.plot([], [], lw=2, label='used memory')
    line_max_used, = ax.plot([], [], lw=2, label='max used memory')
    reset_template = ' reset = %.1f '
    avail_template = ' avail = %.1f '
    used_template = ' used = %.1f '
    max_used_template = ' max_used = %.1f '

    reset_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    avail_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)
    used_text = ax.text(0.05, 0.7, '', transform=ax.transAxes)
    max_used_text = ax.text(0.05, 0.6, '', transform=ax.transAxes)

    ax.legend()
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 5)
    ax.grid()
    xdata, ydata, y1data, y2data, y3data  = [], [], [], [], []
    def init():
        line_reset.set_data([], [])
        line_avail.set_data([], [])
        line_used.set_data([], [])
        line_max_used.set_data([], [])
        reset_text.set_text('')
        avail_text.set_text('')
        used_text.set_text('')
        max_used_text.set_text('')
        return line_reset, line_avail, line_used, line_max_used,\
               reset_text, avail_text, used_text, max_used_text

    def run(data):
    # update the data
        t, y, y1, y2, y3 = data
        xdata.append(t)
        ydata.append(y)
        y1data.append(y1)
        y2data.append(y2)
        y3data.append(y3)
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
            xmax *= 2
            ax.set_xlim(xmin, xmax)
            ax.figure.canvas.draw()
        ymin, ymax = ax.get_ylim()
        if (y >= ymax) | (y1 >= ymax) | (y2 >= ymax) | (y3 >= ymax):
            ymax *= 2
            ax.set_ylim(ymin, ymax)
            ax.figure.canvas.draw()

        line_reset.set_data(xdata, ydata)
        line_avail.set_data(xdata, y1data)
        line_used.set_data(xdata, y2data)
        line_max_used.set_data(xdata, y3data)
        reset_text.set_text(reset_template % y)
        avail_text.set_text(avail_template % y1)
        used_text.set_text(used_template % y2)
        max_used_text.set_text(max_used_template % y3)
        return line_reset, line_avail, line_used, line_max_used,\
               reset_text, avail_text, used_text, max_used_text

    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1000,init_func=init)
    plt.show()



class RTM_MW(object):
    def __init__(self, Data):
        self.Kod = 250
        self.Len = [0x00,0x00]
        self.RetranNum = 0
        self.Flag = 0x00
        self.MyAdd = [7,0,0]
        self.Chan = 1
        self.MyAdd[2] = 0x01
        self.DestAdd = [3, 0, 0x00]
        self.DestAdd[2] = 2
        self.Tranzaction  = 0xe4
        self.PacketNumber = 1
        self.PacketItem   = 1
        self.Instruction  = 1
        self.Data=Data
        self.Errorcnt = 0
        self.OkReceptionCnt = 0

    def send_packet(self, s, type):
        BUFFER_SIZE = 1024
        Packet = [self.Kod]
        Packet.append(self.Len[0])
        Packet.append(self.Len[1])
        Packet.append(self.RetranNum)
        Packet.append(self.Flag)
        Packet.append(self.MyAdd[0])
        Packet.append(self.MyAdd[1])
        Packet.append(self.MyAdd[2])
        Packet.append(self.DestAdd[0])
        Packet.append(self.DestAdd[1])
        Packet.append(self.DestAdd[2])
        Packet.append(self.Tranzaction)
        Packet.append(self.PacketNumber)
        Packet.append(self.PacketItem)
        for i in range(0, len(self.Data)):
          Packet.append(self.Data[i])
        lenght = len(Packet)
        lenght += 2
        self.Len[0] = lenght & 0xFF
        self.Len[1] = (lenght >> 8) & 0xFF
        Packet[1] = self.Len[0]
        Packet[2] = self.Len[1]
        CRC = RTM64CRC16(Packet, len(Packet))
        Packet.append(CRC & 0xFF)
        Packet.append((CRC >> 8) & 0xFF)
        data_s = []
        if type == 1:
            Packet_str = bytearray(Packet[0:])
            print(Packet_str)
            time_start = time.time()
            s.send(Packet_str)
            s.settimeout(1)
            try:
                data = s.recv(BUFFER_SIZE)
                self.OkReceptionCnt += 1
                time_pr=time.time() - time_start
                for i in range(0, len(data)):
                    data_s.append(data[i])
                print(data_s, self.OkReceptionCnt)
                print(time_pr, 's')
                print(len(data))
            except socket.timeout:
                self.Errorcnt += 1
                print("TCP_RecvError", self.Errorcnt)
                print(time.asctime())
                error_log = open('error_log_TCP.txt', 'a')
                error_log.write("TCP_RecvError"+time.asctime()+str(self.Errorcnt)+'\n')
                error_log.close()
        elif type == 0:
            print(Packet)
            send_log = open('send_log.txt', 'a')
            send_log.write(str(Packet))
            send_log.close()
            s.write(Packet)
        return data_s

    def chek_packet(self, data):
        str_buf = ''
        [250, 19, 0, 0, 3, 7, 0, 1, 5, 0, 130, 228, 1, 1, 2, 5, 0, 8, 19]
        i = 0
        if data[i] != self.Kod:
            str_buf = 'Kod_error'+'\t'
        i += 1
        lenght = data[i] | data[i+1] << 8
        i += 2
        if lenght != len(data):
            str_buf+='lenght_Error'+'\t'
        i += 1#retrannum
        i += 1#flag
        if self.MyAdd[0] != data[i] or self.MyAdd[1] != data[i+1] or self.MyAdd[2] != data[i+2]:
            str_buf += 'MyAddr_Error'+'\t'
        i += 3
        if self.DestAdd[0] != data[i] or self.DestAdd[1]!= data[i+1] or (self.DestAdd[2] | 0x80) != data[i+2]:
            str_buf += 'DestAddr_Error'+'\t'
        i += 3
        if self.Tranzaction != data[i]:
            str_buf+='Tranzaction_Error'+'\t'
        i += 1
        if self.PacketNumber != data[i]:
            str_buf += 'PacketNumber_Error'+'\t'
        i += 1
        if self.PacketItem != data[i]:
            str_buf += 'PacketItem_Error'+'\t'
        i += 1
        self.DataInPacket = data[i:len(data)-2]
        i += len(self.DataInPacket)
        CRC = RTM64CRC16(data, len(data)-2)
        CRCin = data[i] | data[i+1] << 8
        if CRC != (CRCin):
            str_buf += 'CRC_Error'
        return str_buf
    
    

    

def RTM64CRC16(pbuffer , Len):
  """CRC16 for RTM64"""
  CRC = 0x0000
  k = 0
  while (k < Len):
    CRC = (CRC^((pbuffer[k]<<8)&0xFFFF))
    k+=1
    i=8
    while (i):
      i-=1
      if (CRC & 0x8000): CRC = (((CRC<<1)&0xFFFF)^0x1021)
      else: CRC = ((CRC<<1)&0xFFFF)
  return CRC
def crc16(pck,len):
  """CRC16 for modbus"""
  CRC = 0xFFFF
  i = 0
  while ( i < len ):
    CRC ^= pck[i]
    i+=1
    j = 0 
    while ( j < 8):
       j+=1
       if ( (CRC & 0x0001) == 1 ): CRC = ((CRC >> 1)&0xFFFF) ^ 0xA001;
       else: CRC >>= 1;
  return (CRC&0xFFFF)
def RTM64ChkSUM(pbuffer,Len):
  """ CheckSum RTM64"""
  sum = 0
  i = 0
  while (i<Len):
    sum = sum + pbuffer[i]
    i+=1
  return sum
def int_to_char(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ['~']
  while (i<len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i+=1
  return cmd_r[1:]
def list_to_str(cmd_x):
  """char to string array confersion"""
  i = 0
  cmd_r = ''
  while (i<len(cmd_x)):
    cmd_r += chr(int(cmd_x[i]))
    i+=1
  return cmd_r
def str_to_int(cmd_x,lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i<lenth):
    cmd_r[i]=ord(cmd_x[i])
    i+=1
  return cmd_r

def char_to_int(cmd_x,lenth):
  i = 0
  cmd_r = [0 for x in range(lenth)]
  while (i<lenth):
    cmd_r[i]=ord(str(cmd_x[i]))
    i+=1
  return cmd_r
def print_hex(cmd,lenth):
  i = 0
  hexf=[0 for x in range(lenth)]
  while (i<lenth):
    hexf[i] = (hex(cmd[i]))
    i+=1
  print (hexf)
if __name__ == "__main__":
  print ("told one things")
  main()
