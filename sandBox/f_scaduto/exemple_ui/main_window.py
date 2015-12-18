__author__ = 'f.scaduto'

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from main_window_ui import Ui_DockWidget # Ui_mainWindow

_WINDOW_TITLE = "exemple_ui"

class MainWindow(QDockWidget, Ui_DockWidget): # Ui_mainWindow

    def __init__(self, parent=None):
        # Init Superclass
        QDockWidget.__init__(self, parent)
        # Build UI
        self.setupUi(self)
        self.setWindowTitle(_WINDOW_TITLE)


def show_in_maya():
    # If Inside Maya
    try:
        # Get Maya Window
        import maya.OpenMayaUI as omui
        from shiboken import wrapInstance
        maya_window_ptr = omui.MQtUtil.mainWindow()
        maya_window = wrapInstance(long(maya_window_ptr), QMainWindow)
        # Instanciate Main Window
        main_window = MainWindow(parent=maya_window)
        # Show
        maya_window.addDockWidget(Qt.NoDockWidgetArea, main_window)
        main_window.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        main_window.setFloating(True)
        main_window.show()
    # If not Inside Maya
    except ImportError:
        # Verbose
        print "Outside MAYA !"

if __name__ == '__main__':
    # New App
    app = QApplication(sys.argv)
    # Instance MainWindow
    main_window = MainWindow()
    # Show
    main_window.show()
    # Exec
    sys.exit(app.exec_())
