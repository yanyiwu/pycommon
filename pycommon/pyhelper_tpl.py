#import os,sys
#p = os.path
#sys.path.insert(0, p.abspath(p.join(p.dirname(p.abspath(p.expanduser(__file__))), "pycommon")))
#sys.path.insert(0, p.abspath(p.join(p.dirname(p.abspath(p.expanduser(__file__))), "../../pycommon")))

from pyhelper import pyhelper_add_helper,pyhelper_main

@pyhelper_add_helper
def A(a,b=1, c=""):
    """
    This Is The Help Of A
    Haha
    """
    print a,b
    #print sys.path
    pass

if __name__ == "__main__":
    pyhelper_main()
