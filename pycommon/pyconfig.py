from pylogger import logger

class Config:
    def __init__(self):
        self._is_initted = False
        self._config = {}
        pass

    def _strip_comments(self, line):
        if not line:
            return None
        pos = line.find("#")
        if -1 == pos:
            return line.strip()
        return line[:pos].strip()

    def _split_key_value(self, line):
        line_segs = line.split("=")
        if 2 != len(line_segs):
            return None, None
        else:
            return line_segs[0].strip(), line_segs[1].strip()

    def display(self):
        for key in self._config:
            print "(%s, %s)" %(key, self._config[key])

    def init(self, filepath):
        if self._is_initted:
            logger.critical("already initted.")
            return False
        try:
            fin = open(filepath, "r")
        except Exception as e:
            logger.critical("open file[%s] failed. error[%s]" %(filepath, e))
            return False
        for i, rawline in enumerate(fin):
            line = self._strip_comments(rawline)
            if not line:
                continue
            key, value = self._split_key_value(line)
            if key and key not in self._config:
                self._config[key] = value
            else:
                logger.critical("line %s: [%s] illegal or already configured before this line." %(i, line))
                return False

        self._is_initted = True
        return True

    def get(self, key):
        if not self._is_initted:
            logger.critical("config not initted.")
            return None
        if key in self._config:
            return self._config[key]
        else:
            logger.error("key[%s] is not in config" %key)
            return None


if __name__ == "__main__":
    config = Config()
    config.init("1.conf")
    config.display()
    print config.get("a")
