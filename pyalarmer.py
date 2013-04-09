#-*-coding:utf-8-*-
import commands
from pylogger import logger
class Alarmer:
    def __init__(self,**argv):
        self.__queue=[]
        self.THRESHOLD=1
        #self.__subject = argv['subject']
        if 'server' in argv:
            self.__server = argv['server']
        else:
            logger.critical('[server] error')
        if  'emailfrom' in argv:
            self.__from = argv['emailfrom']
        else:
            logger.critical('[emailfrom] error')
        if 'emailto' in argv:
            self.__to = argv['emailto']
        else:
            logger.critical('[emailto] error')
            

    def add(self,subject,content,attachment=None):
        self.__queue.append((subject,content,attachment))
        pass

    def call_alarmer(self):
        while len(self.__queue) >= self.THRESHOLD:
            self._send_mail()

    def _send_mail(self):
        (subject,content,attachments)=self.__queue.pop(0)
        content=content.replace('"','\'')

        send_cmd='./pycommon/send_mail/sendEmail -s "%s" -f "%s" -t "%s" -u "%s" -m "%s" -o message-charset="utf-8" ' %(self.__server,self.__from,self.__to,subject,content)
        if attachments:
            send_cmd += ' -a '
            for atta in attachments:
                send_cmd += ' "%s" ' %atta
        
        status,output=commands.getstatusoutput(send_cmd)
        if status:
            logger.error('_send_mail error:[%s]' %output)
        else:
            logger.info('_send_mail suceeded.')

