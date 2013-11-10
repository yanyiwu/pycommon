import sys
import os
import time
import smtplib
import logging
import socket
import fcntl
import struct
from email.mime.text import MIMEText
#from email.MIMEText import MIMEText

MAIL_HOST = "smtp.163.com"
MAIL_POSTFIX = "163.com"

TIME_SLEEP = 10


#get_ip_address('lo')
#get_ip_address('eth0')
def get_ip_address(ifname = "eth0"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def send_mail(user, passwd, to_list, sub, content):
    me = user + "<" + user + "@" + MAIL_POSTFIX + ">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(MAIL_HOST)
        s.login(user, passwd)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
    except Exception as err:
        logging.error("send mail failed. [%s]" %err)
        return False
    logging.info("send mail %s [%s] [%s]" %(to_list, sub, content))
    return True
        
def wait_process_exit(pattern):
    while True:
        ps_string = os.popen('ps aux | grep %s | grep -v grep' %pattern,'r').read()
        ps_strings = ps_string.strip().split('\n')
        if len(ps_strings) < 2:
            return
        else:
            time.sleep(TIME_SLEEP)

def run(pattern, user, passwd):
    SUBJECT = get_ip_address()
    CONTENT = "process quit , 88 "
    MAIL_TO_LIST = ["wuyanyi09@gmail.com"]
    wait_process_exit(pattern)
    send_mail(user, passwd, MAIL_TO_LIST, SUBJECT, CONTENT)
 
if __name__ == '__main__':
    logging.basicConfig(format = "[%(asctime)s] %(filename)s[line:%(lineno)d] : [%(levelname)s] %(message)s", level = logging.DEBUG)
    if len(sys.argv) < 4:
        print >> sys.stderr, "usage: %s <grep_pattern> <user> <passwd>" %sys.argv[0]
        exit(1)
    run(sys.argv[1], sys.argv[2], sys.argv[3])

