import smtplib
import ipgetter
import argparse
__description__ = 'email sender'

def main():
    parser = argparse.ArgumentParser(description=__description__)
    #parser.add_argument('-q', '--quiet', action='store_true',
     #                   help='quiet output')

    parser.add_argument('password')
    args = parser.parse_args()
    if args.password:
        fromaddr = 'shomagan@gmail.com'
        toaddrs  = 'shomagan@gmail.com'
        IP = ipgetter.myip()
        msg = IP
        username = 'shomagan@gmail.com'
        password = args.password
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

if __name__ == "__main__":
    main()
