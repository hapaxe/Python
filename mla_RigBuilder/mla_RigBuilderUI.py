from Qt import QtWidgets, QtCore, QtGui
# import mla_file_utils.mla_path_utils as path_utils
import mla_UI_utils.mla_UI_utils as ui_utils
import mla_file_utils.mla_path_constructor_ui as pcui
import mla_file_utils.mla_file_utils as file_utils
import mla_file_utils.mla_import_utils as import_utils
reload(pcui)
reload(file_utils)
reload(import_utils)

application, mc, api = import_utils.import_from_application()

dockable = import_utils.get_dockable_widget(application)


class RigBuilderUI(dockable, QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(RigBuilderUI, self).__init__(parent=parent)

        self.setWindowTitle('Rig Builder UI')
        # Path constructor
        self.path_constructor = pcui.PathConstructorUI()
        # UI
        self.buildUI()

    def buildUI(self):
        pass
