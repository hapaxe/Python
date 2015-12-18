__author__ = 'f.scaduto'

import sys
import json
from datetime import datetime
from PySide.QtCore import *
from PySide.QtGui import *
from main_window_ui import Ui_MainWindow

import definitions as sceneCheck_def
reload(sceneCheck_def)

_WINDOW_TITLE = "Scene batcher Tool V0.1"
_DEFAULT_ASSET_LIST = ['cube001', 'cube002']
_DEFAULT_CMDS_LIST = ['import maya.cmds as mc','mc.polyCube()','cube.test(*args)']

class MainWindow(QDockWidget, Ui_MainWindow):

    def __init__(self, parent=None):
        # Init Superclass
        QDockWidget.__init__(self, parent)
        # Build UI
        self.setupUi(self)
        self.setWindowTitle(_WINDOW_TITLE)
        self.textedit_asset_list.setPlainText(str(_DEFAULT_ASSET_LIST))
        self.textEdit_cmds.setPlainText(str(_DEFAULT_CMDS_LIST))
        # Members
        # Set Button Disabled
        self.button_batch.setEnabled(False)
        self.in_assets = _DEFAULT_ASSET_LIST
        self.cmds = _DEFAULT_CMDS_LIST
        # Conect Signals
        self.textedit_asset_list.textChanged.connect(self._assets_list_changed)
        self.textEdit_cmds.textChanged.connect(self._cmds_list_changed)
        self.button_dataCheck.pressed.connect(self._dataCheck)
        self.button_batch.pressed.connect(self._batch)

    def _assets_list_changed(self):
        # Get New Text
        new_assets_text = self.textedit_asset_list.toPlainText().replace('\'', '\"')
        # Try to load
        try:
            new_assets_content = json.loads(new_assets_text)
        except ValueError:
            new_assets_content = None
        # If List
        if isinstance(new_assets_content, list):
            # Set Member
            self.in_assets = new_assets_content
            # Set Button Enabled
            self.button_batch.setEnabled(True)
        # If not List
        else:
            # Set Button Disabled
            self.button_batch.setEnabled(False)

    def _cmds_list_changed(self):
        # Get New Text
        new_cmds_text = self.textEdit_cmds.toPlainText().replace('\'', '\"')
        # Try to load
        try:
            new_cmds_content = json.loads(new_cmds_text)
        except ValueError:
            new_cmds_content = None
        # If List
        if isinstance(new_cmds_content, list):
            # Set Member
            self.cmds = new_cmds_content
            # Set Button Enabled
            self.button_batch.setEnabled(True)
        # If not List
        else:
            # Set Button Disabled
            self.button_batch.setEnabled(False)

    def _get_params(self):
        # Gather Asset Parameters
        self.project = self.combo_project.currentText()[:3]
        # If Open Scene Publish
        if self.radio_openScene_publish.isChecked():
            self.open_type = 'publish'
        # If Open Scene Wip
        else:
            self.open_type = 'wip'
        # If Save Scene Publish
        if self.radio_saveScene_publish.isChecked():
            self.save_type = 'publish'
        # If Save Scene Wip
        else:
            self.save_type = 'wip'
        # Create a list to store tasks
        self.tasks=[]
        # If a checkBox is checked, append the task to list
        if self.checkBox_modeling.isChecked():
            self.tasks.append('modeling')
        if self.checkBox_setupLOD0.isChecked():
            self.tasks.append('setupLOD0')
        if self.checkBox_setupLOD1.isChecked():
            self.tasks.append('setupLOD1')
        if self.checkBox_setupLOD2.isChecked():
            self.tasks.append('setupLOD2')
        if self.checkBox_assemblyDef.isChecked():
            self.tasks.append('assemblyDef')
        if self.checkBox_set.isChecked():
            self.tasks.append('set')

    def _dataCheck(self):
        # Get current time
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Get all parameters
        self._get_params()
        # Print a log
        print('\n\n>>   ---------- Data check ----------')
        print('>>')
        print('>>   Time :                  '+time)
        print('>>')
        print('>>   Project :               '+self.project)
        print('>>   Open scene from :       '+self.open_type)
        print('>>   Save scene to :         '+self.save_type)
        print('>>   Task(s) to batch :      '+str(self.tasks))
        print('>>   Assets to batch :       '+str(self.in_assets))
        print('>>   Command(s) to batch :   '+str(self.cmds))
        print('\n')

    def _batch(self):
        # If not default assets text
        if not self.in_assets != _DEFAULT_ASSET_LIST:
            print('>>   Please insert assets list first.')
        else:
            # If not default cmds text
            if not self.cmds != _DEFAULT_CMDS_LIST:
                print('>>   Please insert commands list first.')
            else:
                # Get params
                self._get_params()
                sceneCheck_def.batch_scenes(in_assets=self.in_assets,
                                            project_id=self.project,
                                            tasks=self.tasks,
                                            scene_state=self.open_type,
                                            in_cmds=self.cmds,
                                            save_state=self.save_type)


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
