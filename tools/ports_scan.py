import sys
import socket
from datetime import datetime
import logging
import _thread as thread
import time 

def tcp_ports(target, from_port, number_of_ports):
    for port in range(from_port,from_port + number_of_ports):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.05)
            # returns an error indicator
            result = s.connect_ex((target,port))
            if result == 0:
                print("Port {} is open".format(port))
                logging.info("Port {} is open".format(port))
            s.close()
            if port % 500 == 0:
                print("Scaned {} ports".format(port))
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            logging.info("\n Hostname Could Not Be Resolved !!!!")
            break
        except socket.error:
            print("\ Server not responding !!!!")
            logging.info("\ Server not responding !!!!")
            break

if __name__ == '__main__':
    # Defining a target
    if len(sys.argv) == 2:
        # translate hostname to IPv4
        target = socket.gethostbyname(sys.argv[1])
    else:
        print("Invalid amount of Argument")
    # Add Banner
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)
    logging.basicConfig(filename='ports.log', level=logging.DEBUG)
    logging.info('Ports')
    thread.start_new_thread(tcp_ports, (target, 0, 10000))
    thread.start_new_thread(tcp_ports, (target, 10000, 10000))
    thread.start_new_thread(tcp_ports, (target, 20000, 10000))
    thread.start_new_thread(tcp_ports, (target, 30000, 10000))
    thread.start_new_thread(tcp_ports, (target, 40000, 10000))
    thread.start_new_thread(tcp_ports, (target, 50000, 10000))
    thread.start_new_thread(tcp_ports, (target, 60000, 5535))
    while 1:
        try:
            time.sleep(0.3)
        except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            logging.info("\n Exiting Program !!!!")
            break

