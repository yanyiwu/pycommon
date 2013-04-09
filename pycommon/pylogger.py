import logging
import logging.handlers
#import global_define
import os


logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
ch.setLevel(logging.INFO)

#log_dir=global_define.LOG_DIR
log_dir = 'log'
log_name = 'run.log'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
#fh=logging.handlers.TimedRotatingFileHandler(os.path.join(global_define.LOG_DIR,global_define.LOG_FILE_NAME),'d',1)
fh=logging.handlers.TimedRotatingFileHandler(os.path.join(log_dir,log_name),'d',1)
fh.setLevel(logging.DEBUG)
formatter=logging.Formatter("[%(asctime)s] %(filename)s[line:%(lineno)d] : [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
