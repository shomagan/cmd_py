__author__ = 'Руслан'
#!/c/Python33/ python
"""
add addres property befor start program
"""
import sys
import socket
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct

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
    raz_rezet = data_gen.raz_rezet
    ip_error = data_gen.ip_error
    TCP_IP = '172.16.1.4'
    TCP_PORT = 502
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = [2, 154, 0]
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
                if len(packet.DataInPacket) != 37:
                    str_temp += 'DataInPacket_Error'
                if str_temp:
                    print(str_temp)
                    data_error += 1
                    error_log = open('error_log_TCP.txt', 'a')
                    error_log.write(str_temp+str(packet.DataInPacket)+time.asctime()+'\n')
                    error_log.close()
                else:
                    ip_error = packet.DataInPacket[33]|(packet.DataInPacket[34]<<8)|(packet.DataInPacket[35]<<16)|(packet.DataInPacket[36]<<24)
                    raz_rezet = packet.DataInPacket[1]|(packet.DataInPacket[2]<<8)
                    
 #                   ip_error = struct.unpack('f',bytearray(packet.DataInPacket[5:9]))
  #                  raz_rezet = struct.unpack('f',bytearray(packet.DataInPacket[1:5]))
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
        yield t, raz_rezet, ip_error

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
    data_gen.raz_rezet = 0
    data_gen.ip_error = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False)
    line_raz_rezet, = ax.plot([], [],'bo', lw=2, label='successful packet')
    line_ip_err, = ax.plot([], [], lw=2, label='ip error')
    raz_rezet_template = ' input = %.1f '
    ip_error_template = ' output = %.1f '
    raz_rezet_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    ip_error_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)

    ax.legend()
    ax.set_ylim(0, 4100)
    ax.set_xlim(0, 5)
    ax.grid()
    xdata, y_rezet_data, y_ip_error_data = [], [], []
    def init():
        line_raz_rezet.set_data([], [])
        line_ip_err.set_data([], [])
        raz_rezet_text.set_text('')
        ip_error_text.set_text('')
        return line_raz_rezet, raz_rezet_text, line_ip_err, ip_error_text

    def run(data):
    # update the data
        t, y_rezet, y_ip_error = data
        xdata.append(t)
        y_rezet_data.append(y_rezet)
        y_ip_error_data.append(y_ip_error)
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
            xmax += 10
            ax.set_xlim(xmin, xmax)
            ax.figure.canvas.draw()
        ymin, ymax = ax.get_ylim()
        if (y_rezet >= ymax) | (y_ip_error >= ymax):
            ymax += 1000
            ax.set_ylim(ymin, ymax)
            ax.figure.canvas.draw()

        line_raz_rezet.set_data(xdata, y_rezet_data)
        line_ip_err.set_data(xdata, y_ip_error_data)
        raz_rezet_text.set_text(raz_rezet_template % y_rezet)
        ip_error_text.set_text(ip_error_template % y_ip_error)

        return line_raz_rezet, raz_rezet_text, line_ip_err, ip_error_text
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=100,init_func=init)
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
        self.DestAdd = [4, 0, 0x00]
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
