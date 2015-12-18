from PySide import QtCore, QtGui
import sys, json, os
from PySide.QtCore import *
from PySide.QtGui import *
import maya.cmds as cmds

_WINDOW_TITLE = "Switch Reference"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(217, 153)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupbox_switch_references = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupbox_switch_references.setObjectName("groupbox_switch_references")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupbox_switch_references)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_helper = QtGui.QLabel(self.groupbox_switch_references)
        self.label_helper.setObjectName("label_helper")
        self.verticalLayout_3.addWidget(self.label_helper)
        self.layout_representation_options = QtGui.QHBoxLayout()
        self.layout_representation_options.setObjectName("layout_representation_options")
        self.label_representation_options = QtGui.QLabel(self.groupbox_switch_references)
        self.label_representation_options.setObjectName("label_representation_options")
        self.layout_representation_options.addWidget(self.label_representation_options)
        self.combo_representation_options = QtGui.QComboBox(self.groupbox_switch_references)
        self.combo_representation_options.setObjectName("combo_representation_options")
        self.combo_representation_options.addItem("")
        self.combo_representation_options.addItem("")
        self.combo_representation_options.addItem("")
        self.combo_representation_options.addItem("")
        self.layout_representation_options.addWidget(self.combo_representation_options)
        self.layout_representation_options.setStretch(1, 10)
        self.verticalLayout_3.addLayout(self.layout_representation_options)
        self.verticalLayout_2.addWidget(self.groupbox_switch_references)
        self.button_switch = QtGui.QPushButton(self.dockWidgetContents)
        self.button_switch.setObjectName("button_switch")
        self.verticalLayout_2.addWidget(self.button_switch)
        MainWindow.setWidget(self.dockWidgetContents)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DockWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.groupbox_switch_references.setTitle(QtGui.QApplication.translate("MainWindow", "Switch References", None, QtGui.QApplication.UnicodeUTF8))
        self.label_helper.setText(QtGui.QApplication.translate("MainWindow", "Select item and representation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_representation_options.setText(QtGui.QApplication.translate("MainWindow", "Representation :", None, QtGui.QApplication.UnicodeUTF8))
        self.combo_representation_options.setItemText(0, QtGui.QApplication.translate("MainWindow", "SetupLOD0", None, QtGui.QApplication.UnicodeUTF8))
        self.combo_representation_options.setItemText(1, QtGui.QApplication.translate("MainWindow", "SetupLOD1", None, QtGui.QApplication.UnicodeUTF8))
        self.combo_representation_options.setItemText(2, QtGui.QApplication.translate("MainWindow", "SetupLOD2", None, QtGui.QApplication.UnicodeUTF8))
        self.combo_representation_options.setItemText(3, QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.button_switch.setText(QtGui.QApplication.translate("MainWindow", "Switch", None, QtGui.QApplication.UnicodeUTF8))

class MainWindow(QDockWidget, Ui_MainWindow):

    def __init__(self, parent=None):
        # Init Superclass
        QDockWidget.__init__(self, parent)
        # Build UI
        self.setupUi(self)
        self.setWindowTitle(_WINDOW_TITLE)
        # Conect Signals
        self.button_switch.pressed.connect(self._run_pressed)

    def _get_params(self):
        # Gather Representation Parameters
        self.representation = self.combo_representation_options.currentText()

    def _run_pressed(self):
        # Get params
        self._get_params()
        
        switch_reference(path_to_switch=self.representation)

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
        main_window.setAllowedAreas(Qt.NoDockWidgetArea)
        main_window.setFloating(True)
        main_window.show()
    # If not Inside Maya
    except ImportError:
        # Verbose
        print "Outside MAYA !"


def switch_reference(path_to_switch):
    '''
    Get the selected object, query his reference node and his path,
    rebuild all representations path
    and switch
    '''
    # Get the selection
    selected_item = cmds.ls(sl=True)
    
    for each in selected_item:
        # Get the reference_node
        reference_node = cmds.referenceQuery( each, referenceNode=True )
        
        # Get the path of referenced node
        rn_path = cmds.referenceQuery( each, filename=True, unresolvedName=True)
        
        # Get active representation of reference
        split_rn_path = rn_path.split("/")
        active_representation = split_rn_path[-2]
        
        # Get path parts to rebuild
        path_parts = rn_path.split(active_representation)
        
        # Rebluid paths of setupLOD0, setupLOD1 and setupLOD2
        setupLOD0_str = "setupLOD0"
        setupLOD0_path = path_parts[0]+setupLOD0_str+path_parts[1]+setupLOD0_str+path_parts[2]
        
        setupLOD1_str = "setupLOD1"
        setupLOD1_path = path_parts[0]+setupLOD1_str+path_parts[1]+setupLOD1_str+path_parts[2]
        
        setupLOD2_str = "setupLOD2"
        setupLOD2_path = path_parts[0]+setupLOD2_str+path_parts[1]+setupLOD2_str+path_parts[2]


        if path_to_switch == "SetupLOD0":
            # Remove env var
            no_env_setupLOD0_path = setupLOD0_path.replace("$CUBE_PROJECT_DATAS", "P:/Stella_Serie/projet")
            # If {*} in path from reference editor
            if "}" in setupLOD0_path:
                split_setupLOD0_path = no_env_setupLOD0_path.split("{")
                good_setupLOD0_path = split_setupLOD0_path[0]
                if os.path.exists(good_setupLOD0_path):
                    # Switch to the representation intended
                    cmds.file(good_setupLOD0_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD0"
                else:
                    print reference_node + " dont have setupLOD0"
            else:
                if os.path.exists(no_env_setupLOD0_path):
                    # Switch to the representation intended
                    cmds.file(setupLOD0_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD0"
                else:
                    print reference_node + " dont have setupLOD0"


        if path_to_switch == "SetupLOD1":
            # Remove env var
            no_env_setupLOD1_path = setupLOD1_path.replace("$CUBE_PROJECT_DATAS", "P:/Stella_Serie/projet")
            # If {*} in path from reference editor
            if "}" in setupLOD1_path:
                split_setupLOD1_path = no_env_setupLOD1_path.split("{")
                good_setupLOD1_path = split_setupLOD1_path[0]
                if os.path.exists(good_setupLOD1_path):
                    # Switch to the representation intended
                    cmds.file(good_setupLOD1_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD1"
                else:
                    print reference_node + " dont have setupLOD1"
            else:
                if os.path.exists(no_env_setupLOD1_path):
                    # Switch to the representation intended
                    cmds.file(setupLOD1_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD1"
                else:
                    print reference_node + " dont have setupLOD1"

        if path_to_switch == "SetupLOD2":
            # Remove env var
            no_env_setupLOD2_path = setupLOD2_path.replace("$CUBE_PROJECT_DATAS", "P:/Stella_Serie/projet")
            # If {*} in path from reference editor
            if "}" in setupLOD2_path:
                split_setupLOD2_path = no_env_setupLOD2_path.split("{")
                good_setupLOD2_path = split_setupLOD2_path[0]
                if os.path.exists(good_setupLOD2_path):
                    # Switch to the representation intended
                    cmds.file(good_setupLOD2_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD2"
                else:
                    print reference_node + " dont have setupLOD2"
            else:
                if os.path.exists(no_env_setupLOD2_path):
                    # Switch to the representation intended
                    cmds.file(setupLOD2_path, type="mayaAscii",options="v=0",loadReference=reference_node)
                    print reference_node + " switched to setupLOD2"
                else:
                    print reference_node + " dont have setupLOD2"

        if path_to_switch == "None":
            # Unload reference
            cmds.file(unloadReference=reference_node)
