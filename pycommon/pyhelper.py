import sys
#import pyconsole
import traceback
import pprint
import os

pyhelper_cmd_dict = {}
pyhelper_filekey = None
#pyhelper_terminal_size = pyconsole.get_terminal_size()
pyhelper_output_format = ""
#pyhelper_output_format = "ZH"

def get_output_env():
    global pyhelper_output_format
    if "PYHELPER_OUTPUT_FORMAT" in os.environ:
        pyhelper_output_format = os.environ["PYHELPER_OUTPUT_FORMAT"]

def pyhelper_add_helper(o):
    filekey = o.func_globals["__file__"]
    if type(o) == type(pyhelper_add_helper):
        res = o.func_code.co_name
        res += "("
        args = o.func_code.co_varnames[:o.func_code.co_argcount]
        dargs = o.func_defaults
        if not dargs:
            dargs = []
        argsl = len(args)
        dargsl = len(dargs)
        minus = argsl - dargsl
        for k in range(argsl):
            res += args[k]
            if k >= minus:
                dargk = dargs[k - minus]
                if type(dargk) == type(""):
                    dargk = '"%s"' % dargk
                res += "=%s" % dargk 
            res += ", "
        if res.endswith(", "):
            res = res[:-2]
        res += ")"
        if o.func_doc:
            res += "\n%s" % o.func_doc.lstrip("\n").rstrip()
        res += "\n"
        pyhelper_cmd_dict[filekey] = pyhelper_cmd_dict.get(filekey, {})
        pyhelper_cmd_dict[filekey][o.func_code.co_name] = (o, minus, argsl, res, o.func_globals)
    return o

def pyhelper_print_error_line(l):
    llen = len(l)
    olen = 15
    totallen = llen + olen * 2 + 2
    print "#" * totallen
    print "%s %s %s" % ("#" * olen, l ,"#" * olen)
    print "#" * totallen
    print 

def pyhelper_show_helper(key=None, index = 0):
    global pyhelper_filekey
    filekey = pyhelper_filekey
    this_cmd_dict = pyhelper_cmd_dict.get(filekey, {})
    candidate_keys = []
    if key and not (key in this_cmd_dict):
        pyhelper_print_error_line("Has No Func Named [%s]" % key)
        candidate_keys = [x for x in this_cmd_dict.keys() if key in x]
        key = None
    if index == 0:
        print "Usage:"
        print "%s FuncName FuncArg1 FuncArg2 ..." % sys.argv[0]
        print "The Following Help Will Print In Format:"
        print "FuncName(FuncArg1, ....)"
        print
        index += 1

    if key:
        print "[Function %s]:%s" % (index, this_cmd_dict[key][3])
        return

    if candidate_keys:
        for k in candidate_keys:
            pyhelper_show_helper(k, index)
            index += 1
        return 

    for k in sorted(this_cmd_dict.keys()):
        pyhelper_show_helper(k, index)
        index += 1

def pyhelper_main(zh=False):
    global pyhelper_filekey
    global pyhelper_output_format
    if zh:
        pyhelper_output_format = "ZH"
    get_output_env()
    pyhelper_filekey = traceback.extract_stack()[0][0]
    print pyhelper_filekey
    filekey = pyhelper_filekey
    this_cmd_dict = pyhelper_cmd_dict.get(filekey, {})
    #print this_cmd_dict
    if len(sys.argv) == 1:
        pyhelper_show_helper()
        return
    if not sys.argv[1] in this_cmd_dict:
        pyhelper_show_helper(sys.argv[1])
        return
    argnum = len(sys.argv) - 2
    ftuple = this_cmd_dict[sys.argv[1]]
    if argnum < ftuple[1] or argnum > ftuple[2]:
        pyhelper_print_error_line("Error Arg Nums , Need In [%s, %s], Input is %s" % (ftuple[1], ftuple[2], argnum))
        pyhelper_show_helper(sys.argv[1])
        return
    res = apply(ftuple[4].get(sys.argv[1], ftuple[0]), sys.argv[2:])
    if not res == None:
        if pyhelper_output_format.lower() == "json":
            import simplejson
            print simplejson.dumps(res, sort_keys=True, indent=2 * ' ', separators=(',',':'))
            return
        mprint = pprint
        if pyhelper_output_format.lower() == "zh":
            import zh_pprint
            mprint = zh_pprint
        mprint.pprint(res, width=100)
