__author__ = 'f.scaduto'

import sys
import json
from PySide.QtCore import *
from PySide.QtGui import *
from main_window_ui import Ui_MainWindow
import assemblies
reload(assemblies)

_WINDOW_TITLE = "Assembly Tool"
_DEFAULT_LIST = ['cube001', 'anima_A', 'test002', 'test_A', 'test_B']

class MainWindow(QDockWidget, Ui_MainWindow):

    def __init__(self, parent=None):
        # Init Superclass
        QDockWidget.__init__(self, parent)
        # Build UI
        self.setupUi(self)
        self.setWindowTitle(_WINDOW_TITLE)
        self.textedit_asset_list.setPlainText(str(_DEFAULT_LIST))
        # Members
        self._is_manual = False
        self._is_auto = False
        self._is_batch = False
        # Conect Signals
        self.button_run.pressed.connect(self._run_pressed)
        self.groupbox_process_auto.toggled.connect(self._process_auto_toggled)
        self.groupbox_process_manual.toggled.connect(self._process_manual_toggled)
        self.radio_process_auto_batch.toggled.connect(self._batch_toggled)
        self.textedit_asset_list.textChanged.connect(self._list_changed)

    def update_ui(self):
        # Toggle Auto Enabled State
        self.groupbox_process_auto.setChecked(self._is_auto)
        # Toggle Manual Enabled State
        self.groupbox_process_manual.setChecked(self._is_manual)
        # Toggle Widgets Enabled State
        self.checkbox_process_auto_abc_anima.setEnabled(self._is_auto and self._is_batch)
        self.checkbox_process_auto_assembly_def.setEnabled(self._is_auto and self._is_batch)
        self.checkbox_process_auto_assembly_ref.setEnabled(self._is_auto and self._is_batch)
        self.checkbox_process_auto_modeling_anima.setEnabled(self._is_auto and self._is_batch)
        self.checkbox_process_auto_setuplod0.setEnabled(self._is_auto and self._is_batch)
        self.checkbox_process_auto_setuplod2.setEnabled(self._is_auto and self._is_batch)
        self.button_process_manual_abc_representation.pressed.connect(self._abc_representation_pressed)
        self.button_process_manual_add_tags.pressed.connect(self._add_tags_pressed)
        self.button_process_manual_setuplod0.pressed.connect(self._setuplod0_pressed)

    def _list_changed(self):
        # Get New Text
        new_text = self.textedit_asset_list.toPlainText().replace('\'', '\"')
        # Try to load
        try:
            new_content = json.loads(new_text)
        except ValueError:
            new_content = None
        # If List
        if isinstance(new_content, list):
            # Set Member
            self.asset_names = new_content
            # Set Button Enabled
            self.button_run.setEnabled(True)
        # If not List
        else:
            # Set Button Disabled
            self.button_run.setEnabled(False)

    def _batch_toggled(self, is_checked):
        # Toggle Widgets Enabled State
        self._is_batch = is_checked
        # Upadte UI
        self.update_ui()

    def _process_manual_toggled(self, is_checked):
        # Toggle Widgets Enabled State
        self._is_manual = is_checked
        self._is_auto = not is_checked
        # Upadte UI
        self.update_ui()

    def _process_auto_toggled(self, is_checked):
        # Toggle Widgets Enabled State
        self._is_manual = not is_checked
        self._is_auto = is_checked
        # Upadte UI
        self.update_ui()

    def _get_params(self):
        # Gather Asset Parameters
        self.asset_type_description = self.combo_asset_types.currentText()
        self.asset_type_undescore = self.combo_asset_types.currentText()[:3]
        # If Save Publish
        if self.radio_asset_save_publish.isChecked():
            self.save_type = 'publish'
        # If Save Wip
        else:
            self.save_type = 'wip'

    def _run_pressed(self):
        # If not default text
        if self.asset_names != _DEFAULT_LIST:
            # Get params
            self._get_params()
            # If Automatic
            if self.groupbox_process_auto.isChecked():
                # Batch
                if self.radio_process_auto_batch.isChecked():
                    # Modeling From Anima
                    if self.checkbox_process_auto_modeling_anima.isChecked():
                        # Process
                        assemblies.create_modeling(self.asset_names, self.save_type)
                    # Copy Anima Abc
                    if self.checkbox_process_auto_abc_anima.isChecked():
                        # Process
                        assemblies.copy_abc_modeling(self.asset_names, self.asset_type_undescore, self.asset_type_description)
                    # Setup Lod 0
                    if self.checkbox_process_auto_setuplod0.isChecked():
                        # Process
                        assemblies.create_setuplod0(self.asset_names, self.asset_type_undescore, self.asset_type_description, self.save_type)
                    # Setup Lod 2
                    if self.checkbox_process_auto_setuplod2.isChecked():
                        # Process
                        assemblies.create_setuplod2(self.asset_names, self.save_type)
                    # Assembly Def
                    if self.checkbox_process_auto_assembly_def.isChecked():
                        # Process
                        assemblies.create_assembly_def(self.asset_names, self.asset_type_undescore, self.asset_type_description, self.save_type)
                    # Assembly Ref
                    if self.checkbox_process_auto_assembly_ref.isChecked():
                        # Process
                        assemblies.create_assembly_ref(self.asset_names, self.asset_type_undescore, self.save_type)
                # Task
                elif self.radio_process_auto_add_tasks.isChecked():
                    # Process
                    assemblies.add_tasks_in_tube(self.asset_names)

    def _abc_representation_pressed(self):
        # Get params
        self._get_params()
        # Process
        assemblies.create_lods_abc(self.asset_type_undescore, self.asset_type_description)

    def _add_tags_pressed(self):
        # Get params
        self._get_params()
        # Process
        assemblies.add_cube_tag_manual()

    def _setuplod0_pressed(self):
        # Get params
        self._get_params()
        # Process
        assemblies.create_rig()

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