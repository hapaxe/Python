__author__ = 'm.lanton'
from PySide.QtGui import *
from maya import OpenMayaUI
from shiboken import wrapInstance

import curveManager

reload(curveManager)


def main():
    # Close all windows
    global WIDGET_HOLDER

    try:
        WIDGET_HOLDER.close()
    except (AttributeError, NameError):
        pass
    # Get Pyside instance of Maya MainWindow
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    main_window = wrapInstance(long(ptr), QWidget)
    # New Window
    WIDGET_HOLDER = curveManager.CurveManager(parent=main_window)
    # Store to prevent garbage collection
    # Show
    WIDGET_HOLDER.show()