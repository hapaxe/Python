__author__ = 'f.scaduto'

import sys
import json
from PySide.QtCore import *
from PySide.QtGui import *
from bonusTool_window_ui import Ui_MainWindow
import assemblies
reload(assemblies)

_WINDOW_TITLE = "Assembly Bonus Tool"
_DEFAULT_LIST_CUBE_NAME = ["cube001"]
_DEFAULT_LIST_ASSEMBLY_NAME = ["PR_cube001_MODEL_001"]

class MainWindow(QDockWidget, Ui_MainWindow):

    def __init__(self, parent=None):
        # Init Superclass
        QDockWidget.__init__(self, parent)
        # Build UI
        self.setupUi(self)
        self.setWindowTitle(_WINDOW_TITLE)
        self.textedit_insert_cube_name.setPlainText(str(_DEFAULT_LIST_CUBE_NAME))
        self.textedit_insert_assembly_source_name.setPlainText(str(_DEFAULT_LIST_ASSEMBLY_NAME))
        # Conect Signals
        self.textedit_insert_cube_name.textChanged.connect(self._list_cube_name_changed)
        self.textedit_insert_assembly_source_name.textChanged.connect(self._list_assembly_name_changed)
        self.button_replace_assemblies_datas.pressed.connect(self._replace_assembly_data)
        self.button_replace_selected_object_to_assembly.pressed.connect(self._replace_object_to_assembly)
        self.button_convert_to_gpucache.pressed.connect(self._convert_to_gpucache_pressed)
        self.button_convert_to_geometry.pressed.connect(self._convert_to_geometry_pressed)
        # Set Button Disabled
        self.button_replace_assemblies_datas.setEnabled(False)
        self.button_replace_selected_object_to_assembly.setEnabled(False)

    def _list_cube_name_changed(self):
        # Get New Text
        new_text = self.textedit_insert_cube_name.toPlainText().replace('\'', '\"')
        # Try to load
        try:
            new_content = json.loads(new_text)
        except ValueError:
            new_content = None
        # If List
        if isinstance(new_content, list):
            # Set Member
            self.cube_name = new_content
            # Set Button Enabled
            self.button_replace_assemblies_datas.setEnabled(True)
        # If not List
        else:
            # Set Button Disabled
            self.button_replace_assemblies_datas.setEnabled(False)

    def _list_assembly_name_changed(self):
        # Get New Text
        new_text = self.textedit_insert_assembly_source_name.toPlainText().replace('\'', '\"')
        # Try to load
        try:
            new_content = json.loads(new_text)
        except ValueError:
            new_content = None
        # If List
        if isinstance(new_content, list):
            # Set Member
            self.assembly_name = new_content
            # Set Button Enabled
            self.button_replace_selected_object_to_assembly.setEnabled(True)
        # If not List
        else:
            # Set Button Disabled
            self.button_replace_selected_object_to_assembly.setEnabled(False)

    
    def _replace_assembly_data(self):
        # If not default text
        if self.cube_name != _DEFAULT_LIST_CUBE_NAME:
            assemblies.replace_selected_assemblies_data(cube_name=self.cube_name)

    def _replace_object_to_assembly(self):
        # If not default text
        if self.assembly_name != _DEFAULT_LIST_ASSEMBLY_NAME:
            assemblies.replace_selected_by_assemblies(assembly_to_deploy=self.assembly_name)

    def _convert_to_gpucache_pressed(self):
        # Process
        assemblies.convert_assembly_to(representation="gpuCache")

    def _convert_to_geometry_pressed(self):
        # Process
        assemblies.convert_assembly_to(representation="geometry")

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