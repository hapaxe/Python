from PySide2 import QtWidgets, QtCore, QtGui
import mla_path_utils as path_utils
from mla_UI_utils import mla_UI_utils
import mla_file_utils.mla_path_constructor_ui as pcui
import mla_file_utils.mla_file_utils as file_utils

mc = file_utils.import_if_available('maya.cmds')
mxs = file_utils.import_if_available('pymxs')

if mc:
    application = 'Maya'
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable
    dockable = file_utils.import_if_available('')
elif mxs:
    application = 'Max'
    from mla_UI_utils.mla_Max_UI_utils import MaxDockableWidget as dockable
    import MaxPlus
    dockable = file_utils.import_if_available('')



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
