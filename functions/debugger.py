#----------------------------------------------------------------------
# functions debuger
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import sys

def list_python_path():
    '''
    Print the python path currently loaded

    :return: none
    '''
    for item in sys.path:
        print item