import os

def get_files(dir_path, suffixes = ""):
    ret_list = []
    for root, dirs, files in os.walk(dir_path):
        for fpath in files:
            if fpath.endswith(suffixes):
                ret_list.append(os.path.join(root, fpath))
    return ret_list


def dump(file_content, file_path):
    _dir = os.path.dirname(file_path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(file_path, 'w') as fout:
        fout.write(file_content)

def flatten_list(in_list):
    out_list = list()
    for item in in_list:
        if(isinstance(item,(list,tuple))):
            out_list += flatten_list(item)
        else:
            out_list.append(item)
    return out_list

def get_relative_path(abspath, absprefix):
    plen = len(absprefix)
    if(plen < len(abspath) and abspath[0:plen] == absprefix):
        ret = abspath[plen:]
        if(ret[0]=='/'):
            return ret[1:]
        else:
            return ret
    else:
        return None

if __name__ == "__main__":
    print get_files(".", ".py")
