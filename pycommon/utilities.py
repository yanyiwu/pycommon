import os
import time, datetime

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


def dicts_merge(*dicts):
    ret_dict = {}
    for _dict in dicts:
        for key in _dict:
            if key not in ret_dict:
                ret_dict[key] = _dict[key]
            else:
                if type(ret_dict[key]) == dict and type(_dict[key]) == dict:
                    ret_dict[key] = dicts_merge(ret_dict[key], _dict[key])
                else:
                    ret_dict[key] += _dict[key] # this += maybe throw exception
    return ret_dict

def str2datetime(tstr, pattern):
    t = time.strptime(tstr, pattern)
    return datetime.datetime(* t[:6])


if __name__ == "__main__":
    #print get_files(".", ".py")
    print dicts_merge({1:111}, {"h1":1,"h3":2,"h4":{"s1":1,"s2":2}},{"h1":2,"h3":3,"h4":{"s1":2, "s2":3,"s3":5}})
    print str2datetime("20130401", "%Y%m%d")
