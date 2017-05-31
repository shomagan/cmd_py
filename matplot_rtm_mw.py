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
import seaborn
import struct
import rtm_mw

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
    TCP_IP_232 = '192.168.7.232'
    TCP_IP_3 = '172.16.1.3'
    TCP_PORT = 502
    BUFFER_SIZE = 1024

    data = [2,8,0]
    packet_232 = rtm_mw.RTM_MW(data)
    packet_232.RetranNum =0
    packet_232.DestOne = [3,0,7]

    packet_3 = rtm_mw.RTM_MW(data)
    packet_3.RetranNum =0
    packet_3.DestOne = [3,0,7]

    try:
        packet_232.connect(TCP_IP_232, TCP_PORT)
        packet_3.connect(TCP_IP_3, TCP_PORT)

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
            data_buf = packet_232.SendPacket(packet_232.s,1)
            if data_buf:
                print(data_buf)
                str_temp = packet_232.ChekPacket(data_buf)
                print(packet_232.DataInPacket)
                if len(packet_232.DataInPacket) != 5:
                    str_temp += 'DataInPacket_Error'
                if str_temp:
                    print(str_temp)
                    data_error += 1
                    error_log = open('error_log_TCP.txt', 'a')
                    error_log.write(str_temp+str(len(packet_232.DataInPacket))+time.asctime()+'\n')
                    error_log.close()
                else:
#                    ip_error_byte = str(packet.DataInPacket[5])+str(packet.DataInPacket[6]<<8)+str(packet.DataInPacket[7]<<16)+str(packet.DataInPacket[8]<<24)
 #                   raz_rezet_byte = packet.DataInPacket[1]|(packet.DataInPacket[2]<<8)|(packet.DataInPacket[3]<<16)|(packet.DataInPacket[4]<<24)
                    ip_error = packet_232.DataInPacket[1]
                    successful_packet += 1
            data_buf = packet_3.SendPacket(packet_3.s,1)
            if data_buf:
                str_temp = packet_3.ChekPacket(data_buf)
                if len(packet_3.DataInPacket) != 5:
                    str_temp += 'DataInPacket_Error'
                if str_temp:
                    print(str_temp)
                    data_error += 1
                    error_log = open('error_log_TCP.txt', 'a')
                    error_log.write(str_temp+str(packet_3.DataInPacket)+time.asctime()+str(len(packet_3.DataInPacket))+'\n')
                    error_log.close()
                else:
#                    ip_error_byte = str(packet.DataInPacket[5])+str(packet.DataInPacket[6]<<8)+str(packet.DataInPacket[7]<<16)+str(packet.DataInPacket[8]<<24)
 #                   raz_rezet_byte = packet.DataInPacket[1]|(packet.DataInPacket[2]<<8)|(packet.DataInPacket[3]<<16)|(packet.DataInPacket[4]<<24)
                    raz_rezet = packet_3.DataInPacket[1]
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
    raz_rezet_template = ' target = %.1f '
    ip_error_template = ' server = %.1f '
    raz_rezet_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    ip_error_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)

    ax.legend()
    ax.set_ylim(20, 100)
    ax.set_xlim(0, 100)
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
            xmax += 1
            xmin += 1
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
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=1000,init_func=init)
    plt.show()


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
