__author__ = 'Martin'
import maya.cmds as mc
# import sys
# import os
import maya.cmds as mc
from PySide.QtCore import *
from PySide.QtGui import *
import ml_file as ml_file
import orig
import CM

PROJECT_PATH = 'E:/development/Python/'
ROOT_PATH = 'ml_curve_manager/'


# ----------------------------------------------------------------
class Proc (QDialog, CM.Ui_Dialog):
    def __init__(self, parent=None):
        #QDialog.__init__(self, parent)
        #self.setupUi(self)
        pass

    """def curve_manager_ui():
        # initialize values
        widgets['curve_type'] = 'circle'
        widgets['curve_name'] = 'ctrl'
        widgets['orientation'] = [0, 0, 0]
        widgets['mirror'] = [0, 0, 0]

        if mc.window('CurveManager_Window', exists=True):
            mc.deleteUI('CurveManager_Window', window=True)
        if mc.dockControl('CurveManager', exists=True):
            mc.deleteUI('CurveManager')

        # --- Create window-------------------------------------------------------------------------------------------------
        widgets['window'] = mc.window('CurveManager_Window')
        # formlayout and tabs
        widgets['form'] = mc.formLayout()
        widgets['tabs'] = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        mc.formLayout(widgets['form'], edit=True, attachForm=((widgets['tabs'], 'top', 0),
                                                              (widgets['tabs'], 'left', 0),
                                                              (widgets['tabs'], 'bottom', 0),
                                                              (widgets['tabs'], 'right', 0)))

        # creation tab------------------------------------------------------------------------------------------------------
        widgets['creation_layout'] = mc.rowColumnLayout(parent=widgets['tabs'], w=300)
        # creation options
        # line 1 : name/curve_name
        widgets['nameField'] = mc.textFieldGrp('ui_nameField', label=' Name', text='', columnAlign2=['left', 'left'],
                                               columnWidth2=[75, 225])
        # line 2 : list/curve_type
        widgets['curve_list'] = mc.optionMenuGrp('ui_curve_list', label=' Curve', columnAlign2=['left', 'left'],
                                                 columnWidth2=[75, 225], adjustableColumn2=2,
                                                 parent=widgets['creation_layout'])
        # line 3 : orientation
        widgets['orientation_menu'] = mc.radioButtonGrp('ui_orientation_menu', label=' Orientation',
                                                        labelArray3=['X', 'Y', 'Z'], select=2, numberOfRadioButtons=3,
                                                        columnWidth4=[75, 75, 75, 75],
                                                        columnAlign4=['left', 'left', 'left', 'left'])
        # line 4 : mirroring
        widgets['mirror_menu'] = mc.checkBoxGrp('ui_mirror_menu', label=' Mirror', numberOfCheckBoxes=3, label1='X',
                                                label2='Y', label3='Z', columnWidth4=[75, 75, 75, 75],
                                                columnAlign4=['left', 'left', 'left', 'left'])
        # line 5 : creation button
        widgets['creation_button'] = mc.button(label='Creation')
        # line 6 : remove shape option (edition mode only)
        widgets['remove_shape'] = mc.checkBoxGrp('remove_shape', label=' Remove Shape', numberOfCheckBoxes=1,
                                                 columnWidth2=[75, 75], columnAlign2=['left', 'left'])
        # line 7 : edition button
        widgets['edition_button'] = mc.button(label='Edition')

        # managing_layout tab-----------------------------------------------------------------------------------------------
        widgets['managing_layout'] = mc.rowColumnLayout(numberOfColumns=2, parent=widgets['tabs'])

        mc.tabLayout(widgets['tabs'], edit=True, tabLabel=((widgets['creation_layout'], 'creation/edition'),
                                                           (widgets['managing_layout'], 'managing')))

        widgets['allowedAreas'] = ['right', 'left']
        widgets['dock'] = mc.dockControl('CurveManager',
                                         area='left', content=widgets['window'], allowedArea=widgets['allowedAreas'], w=320)

        mc.showWindow(widgets['dock'])"""

    # ------------------------------------------------------------------------------------------------------------------
    def get_ui_datas(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def save_curve():
        # get selection
        selection = mc.ls(sl=True)
        # get the name of the curve
        curve_type = selection[0]
        # get the name of the curve
        curve_shape_name = mc.listRelatives(curve_type, s=True)[0]

        # get the degree, spans and calculate the numbers of CV of the curve
        curve_degree = mc.getAttr(curve_shape_name + '.degree')
        curve_span = mc.getAttr(curve_shape_name + '.spans')
        cv_number = curve_degree + curve_span

        # create a curveInfo node and connect it to the curve
        curve_info = mc.createNode('curveInfo', n=curve_type + '_curveInfo')  # curveInfo node creation
        mc.connectAttr(curve_type + '.worldSpace', curve_info + '.inputCurve')

        # get the knots of the curve
        knots = mc.getAttr(curve_info+'.knots')[0]

        # create an empty list for the coordinates of the points of the curve
        points = list()
        # fill the list of points coordinates
        for i in range(0, cv_number):
            point = mc.getAttr(curve_info+'.controlPoints['+str(i)+']')
            points.append(point[0])

        curve_dict = {'degree': curve_degree, 'points': points, 'knots': knots}

        ml_file.FileSystem.save_to_json(curve_dict, PROJECT_PATH+ROOT_PATH+'curve_dictionaries'+curve_type+'.json')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_curve(curve_type='circle', name='ctrl'):
        curve_dict = ml_file.FileSystem.load_from_json(PROJECT_PATH+ROOT_PATH+'curve_dictionaries'+curve_type+'.json')
        degree = curve_dict['degree']
        points = curve_dict['points']
        knots = curve_dict['knots']

        mc.curve(n=name, d=degree, p=points, k=knots)
        return name

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def curve_placement():

        selection = mc.ls(sl=True)
        i = 0

        for node in selection:
            # init infos
            curve_name += '_'+str(i)
            translation = mc.xform(node, q=True, translation=True, a=True)
            rotation = mc.xform(node, q=True, rotation=True, a=True)
            rotation = (rotation[0]+orientation[0], rotation[1]+orientation[1], rotation[2]+orientation[2])
            # create the curve
            ctrl = CM.Proc.create_curve(curve_type=curve_type, name=curve_name)
            # place the curve
            # scale
            mc.xform(ctrl, scale=mirror)
            mc.makeIdentity(ctrl, s=True, apply=True)
            # translate
            mc.xform(ctrl, translation=translation)
            # rotate
            mc.xform(ctrl, rotation=rotation)

            orig.orig(ctrl)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def modify_curve_shape(target='None', source='None', delete=True, add=False):
        """

        :param source: transform of the shape you want to assign (str)
        :param target: transform of the shape you want to modify (str)
        :param delete: specify if the original source shape must be kept or not (bool)
        :param add: specify if the source shape must replace the target shape or be added (bool)
        :return: transform of the modified shape (str)
        """

        # --- Get selection
        selection = mc.ls(sl=True)

        # --- Modify target and source if none provided
        if target == 'None':
            target = selection[0]
        if target == 'None' and source == 'None':
            source = selection[1]
        elif source == 'None':
            source = selection[0]
        else:
            pass

        # --- Duplicate if you don't want to delete the original source
        if not delete:
            source = mc.duplicate(source)

        # --- Get the shapes paths
        source_shape = mc.listRelatives(source, c=True, s=True, f=True)
        target_shape = mc.listRelatives(target, c=True, s=True, f=True)
        target_shape_short = mc.listRelatives(target, c=True, s=True)

        # --- Reparent the source shape to the target transform
        new_shape_name = mc.parent(source_shape, target, s=True, add=True)
        # --- Delete the source transform
        mc.delete(source)
        # --- If not add, delete the target shape
        if not add:
            mc.delete(target_shape)

        mc.rename(new_shape_name, target_shape_short)
