__author__ = 'm.lanton'
from PySide.QtGui import *
from maya import OpenMayaUI
from shiboken import wrapInstance

import Asset_Manager.AM as am

reload(am)


def main():
    # Close all windows

    global WIDGET_HOLDER
    #WIDGET_HOLDER = []

    try:
        WIDGET_HOLDER.close()
    except (AttributeError, NameError):
        pass
    # New Window
    WIDGET_HOLDER = am.AM_Class()
    # Store to prevent garbage collection
    # Show
    WIDGET_HOLDER.show()