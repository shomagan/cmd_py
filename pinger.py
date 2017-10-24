from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command


def main():
    pinged=[]
    for i in range(256):
        host = "192.168.1." + str(i)
        if ping(host):
            pinged.append(host) 
    for i in range(host):
        print(host+' ')
    
            


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that some hosts may not respond to a ping request even if the host name is valid.
    """

    # Ping parameters as function of OS
    parameters = "-n 2" if system_name().lower()=="windows" else "-c 1"

    # Pinging
    return system_call("ping " + parameters + " " + host + " -w 100") == 0        

if __name__=="__main__":
    main()