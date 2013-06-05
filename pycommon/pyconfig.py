from pylogger import logger


_is_initted = False
g_config = {}

def _get_line():
    pass

def _strip_comments(line):
    if not line:
        return None
    pos = line.find("#")
    if -1 == pos:
        return line.strip()
    return line[:pos].strip()

def _split_key_value(line):
    line_segs = line.split("=")
    if 2 != len(line_segs):
        return None, None
    else:
        return line_segs[0].strip(), line_segs[1].strip()

def _display():
    for key in g_config:
        print "(%s, %s)" %(key, g_config[key])

def _init_config(filepath):
    global _is_initted
    global g_config
    if _is_initted:
        logger.critical("already initted.")
        return False
    try:
        fin = open(filepath, "r")
    except Exception as e:
        logger.critical("open file[%s] failed. error[%s]" %(filepath, e))
        return False
    for i, rawline in enumerate(fin):
        line = _strip_comments(rawline)
        if not line:
            continue
        key, value = _split_key_value(line)
        if key and key not in g_config:
            g_config[key] = value
        else:
            logger.critical("line %s: [%s] illegal or already configured before this line." %(i, line))
            return False

    _is_initted = True
    return True

if __name__ == "__main__":
    _init_config("1.conf")
    _display()
