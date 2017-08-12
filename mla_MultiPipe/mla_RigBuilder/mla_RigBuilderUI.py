import mla_MultiPipe.mla_file_utils.mla_Multi_file_utils as file_utils
import mla_MultiPipe.mla_file_utils.mla_Multi_import_utils as import_utils
# import mla_file_utils.mla_path_utils as path_utils
import mla_GeneralPipe.mla_file_utils.mla_path_constructor_ui as pcui
from Qt import QtWidgets, QtCore, QtGui

reload(pcui)
reload(file_utils)
reload(import_utils)

application = import_utils.get_application()

dockable = import_utils.get_dockable_widget(application)


class RigBuilderUI(QtWidgets.QDialog, dockable):

    def __init__(self, parent=None):
        super(RigBuilderUI, self).__init__(parent=parent)

        self.setWindowTitle('Rig Builder UI')
        # Path constructor
        self.path_constructor = pcui.PathConstructorUI()
        # UI
        self.buildUI()

    def buildUI(self):
        pass
