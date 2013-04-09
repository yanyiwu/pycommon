import datetime
import subprocess
import os
import pylogger 


class GarbageCleaner:
    def __init__(self):
        self.__list = list()
        self.stamp_map = dict()
        self.day_interval = 2
        pass
    
    def run(self):
        pass

    def add_file_path(self,file_path):
        self.__list.append(file_path)
        if file_path in self.stamp_map:
            pylogger.logger.critical('file path redup .')
        else:
            self.stamp_map[file_path] = datetime.datetime.now()
        pass

    def call_cleaner(self):
        now_t = datetime.datetime.now()

        clean_file_n = 0
        for file_path in self.__list:
            #if self.stamp_map[file_path] < day - datetime.timedelta( days = self.day_interval):
            if self.stamp_map[file_path] < now_t - datetime.timedelta( seconds = 5):
                self._remove(file_path)
                del self.stamp_map[file_path]
                clean_file_n += 1
            else:
                break
        
        self.__list = self.__list[clean_file_n:]
        pylogger.logger.debug('clean files sum[%s]' %clean_file_n)
        pass

    def _remove(self,file_path):
        if os.path.exists(file_path):
            cmd="/bin/rm %s" %(file_path)
            if subprocess.call(cmd,shell=True):
                pylogger.logger.critical('_clean %s failed!' %file_path)
            else:
                pylogger.logger.debug('_clean %s finished.' %file_path)
        else:
            pylogger.logger.error('file_path[%s] no exist' %file_path)




if __name__ == '__main__':
    a=datetime.date(2013,1,1)
    b=datetime.date(2013,5,1)
    print dir(datetime.timedelta)
    pass
