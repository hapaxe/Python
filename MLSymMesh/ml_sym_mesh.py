__author__ = 'lantonm'
from PyQt4 import uic
import sip
from PyQt4 import QtGui, QtCore
import maya.OpenMayaUI as apiUI

import maya.api.OpenMaya as om2

import os
from pprint import pprint

folder_path = '/'.join(__file__.split('/')[:-1])
# ----------------------- BAKE FK CHAIN TO DYNAMIC ----------------------------
# -----------------------------------------------------------------------------
# If you put the .ui file for this example elsewhere, just change this path.
ml_sym_mesh_form, ml_sym_mesh_base = uic.loadUiType('%s/ml_sym_mesh.ui'
                                                    % folder_path)


def get_maya_window():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    :return: QtGui.QMainWindow instance of the top level Maya windows
    :rtype: QtGui.QMainWindow
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)


def ml_sym_mesh_ui():
    """
    Main proc for interface creation.
    """
    global win_templates
    try:
        win_templates.close()
    except:
        pass
    win_templates = MLSymMesh()

    win_templates.show()


class MLSymMesh(ml_sym_mesh_form, ml_sym_mesh_base):

    def __init__(self, parent=get_maya_window()):
        """
        Initialize the class and connect all the functions to the ui.

        :param parent: object to parent the window to
        :type parent: Qt object
        """
        super(MLSymMesh, self).__init__(parent)

        self.setupUi(self)
        self.setObjectName('mlSymMesh_UI')

        self.source_table = om2.MPointArray()
        self.target_table = om2.MPointArray()
        self.sel_vtces_idcs = om2.MIntArray()
        self.revert_value = 100

        self.get_source_pB.clicked.connect(self.get_source)
        self.get_target_pB.clicked.connect(self.get_target)
        self.revert_to_base_slider.valueChanged(self.get_revert_value)
        # self.revert_to_base_spinBox.valueChanged(self.get_revert_value)

        self.revert_to_base_pB(self.revert_selected_to_base)

    def get_source(self):
        self.source_table = self.get_selected_mesh_points()

    def get_target(self):
        self.target_table = self.get_selected_mesh_points()

    def get_revert_value(self):
        self.revert_value = self.revert_to_base_spinBox.value()

    @staticmethod
    def get_selected_mesh_points():
        selection_list = om2.MGlobal.getActiveSelectionList()

        # Get the dag path of the first item in the selection list
        obj_dag_path = selection_list.getDagPath(0)

        # Query vertex position
        # create a Mesh functionSet from our dag object
        mfn_object = om2.MFnMesh(obj_dag_path)

        points = mfn_object.getPoints(space=om2.MSpace.kObject)
        return obj_dag_path, points

    @staticmethod
    def revert_to_base(base_tbl, tgt_tbl, sel_vtcs_idcs, val, mesh_dag_path):
        print base_tbl

        destination_table = tgt_tbl

        tgt_mesh = om2.MFnMesh(mesh_dag_path)

        for i in range(base_tbl.__len__()):
            if i in sel_vtcs_idcs:
                destination_table[i] += ((tgt_tbl[i] - base_tbl[i]) * val / 100)
            else:
                pass

        tgt_mesh.setPoints(destination_table, om2.MSpace.kObject)


    @staticmethod
    def get_sel_vtces_idcs():

        sel = om2.MGlobal.getActiveSelectionList()

        mesh_path, o_components = sel.getComponent(0)

        fn_components = om2.MFnSingleIndexedComponent(o_components)
        selected_vertices_indices = fn_components.getElements()
