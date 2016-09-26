__author__ = 'lantonm'
import maya.cmds as mc
from PySide.QtCore import *
from PySide.QtGui import *
import ml_file as ml_file
import orig
import PT_ui

folder_path = '/'.join(__file__.split('/')[:-1])

# -------------------------------------- EXPORT TEMPLATES ----------------------
# ------------------------------------------------------------------------------
class MPosTool(QDialog, PT_ui.Ui_MPosToolMainWindow):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setObjectName('m_pos_tool_ui')

        self.move_pB.clicked.connect(self.move_from_ui)
        self.move_even_pB.clicked.connect(self.move_even_from_ui)

    def get_data(self):
        """
        Get data from ui
        :return: [[attributes*], world_space, mirror, mirror_axis, behavior]
        :rtype: list
        """

        attributes = list()

        if self.tx_cB.isChecked():
            attributes.append('tx')
        if self.ty_cB.isChecked():
            attributes.append('ty')
        if self.tz_cB.isChecked():
            attributes.append('tz')
        if self.rx_cB.isChecked():
            attributes.append('rx')
        if self.ry_cB.isChecked():
            attributes.append('ry')
        if self.rz_cB.isChecked():
            attributes.append('rz')
        if self.sx_cB.isChecked():
            attributes.append('sx')
        if self.sy_cB.isChecked():
            attributes.append('sy')
        if self.sz_cB.isChecked():
            attributes.append('sz')

        world_space = self.ws_rB.isChecked()

        mirror = self.mirror_cB.isChecked()

        if self.mirror_x_rB.isChecked():
            mirror_axis = 'x'
        elif self.mirror_y_rB.isChecked():
            mirror_axis = 'y'
        else:
            mirror_axis = 'z'

        return [attributes, world_space, mirror, mirror_axis]

    def move_from_ui(self):
        """
        Use move function calling ui data
        :return:
        """
        data = self.get_data()

        selection = mc.ls(sl=True)

        self.move(selection, data[0], data[1], data[2], data[3])

    def move_even_from_ui(self):
        """
        Use move function calling ui data
        :return:
        """
        data = self.get_data()

        selection = mc.ls(sl=True)

        self.move_even(selection, data[0], data[1], data[2], data[3])

    @staticmethod
    def move_even(obj_list=[], attributes=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'],
                  world_space=True, mirror=False, mirror_axis='x'):
        """
        Call the move function by even
        :param obj_list: list of objects to move by pair
        :type obj_list: list

        :param attributes: list of attributes to move
        :type attributes: list

        :param world_space: world space by default, object space if False
        :type world_space: boolean

        :param mirror: mirror state
        :type mirror: boolean

        :param mirror_axis: mirror axis
        :type mirror_axis: str

        :return:
        """
        # UNDO : Open history chunk
        mc.undoInfo(openChunk=True)

        try:
            if len(obj_list) == 0:
                obj_list = mc.ls(sl=True, et='transform')

            for i, obj in enumerate(obj_list):
                if i % 2 == 0:
                    source = obj
                    target = obj_list[i + 1]
                print source, target

                MPosTool.move(source_target=[source, target],
                              attributes=attributes,
                              world_space=world_space,
                              mirror=mirror,
                              mirror_axis=mirror_axis)

        # UNDO : Close history chunk
        finally:
            mc.undoInfo(closeChunk=True)

    @staticmethod
    def move(source_target=[], attributes=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'],
             world_space=True, mirror=False, mirror_axis='x'):
        """
        :param source_target: couple source/target
        :type source_target: list

        :param attributes: list of attributes to move
        :type attributes: list

        :param world_space: world space by default, object space if False
        :type world_space: boolean

        :param mirror: mirror state
        :type mirror: boolean

        :param mirror_axis: mirror axis
        :type mirror_axis: str

        :return:
        """
        # UNDO : Open history chunk
        mc.undoInfo(openChunk=True)

        try:
            # Define couple source/target if not already defined
            if len(source_target) == 0:
                if len(mc.ls(sl=True)) > 1:
                    source_target = mc.ls(sl=True)[:2]
                else:
                    source_target = mc.ls(sl=True)

            # If no source and target given, or to get from selection : return
            if len(source_target) == 0:
                print "No source and no target, skipped."
                return
            # If only one object selected : mirror from its own coordinates
            elif len(source_target) == 1:
                source_target.append(source_target[0])
            else:
                source_target = source_target[:2]

            source = source_target[0]
            target = source_target[1]

            # Get initial transforms from source and target
            if world_space:
                source_translate = mc.xform(source, q=True, t=True, ws=True)
                source_rotate = mc.xform(source, q=True, ro=True, ws=True)
                source_scale = mc.xform(source, q=True, s=True, ws=True)

                target_translate = mc.xform(target, q=True, t=True, ws=True)
                target_rotate = mc.xform(target, q=True, ro=True, ws=True)
                target_scale = mc.xform(target, q=True, s=True, ws=True)
            else:
                source_translate = mc.xform(source, q=True, t=True, os=True)
                source_rotate = mc.xform(source, q=True, ro=True, os=True)
                source_scale = mc.xform(source, q=True, s=True, os=True)

                target_translate = mc.xform(target, q=True, t=True, os=True)
                target_rotate = mc.xform(target, q=True, ro=True, os=True)
                target_scale = mc.xform(target, q=True, s=True, os=True)

            # Defining mirror multiplier
            if mirror and mirror_axis == 'x':
                mir_val = [-1, 1, 1]
            elif mirror and mirror_axis == 'y':
                mir_val = [1, -1, 1]
            elif mirror and mirror_axis == 'z':
                mir_val = [1, 1, -1]
            else:
                mir_val = [1, 1, 1]

            print(source_translate, source_rotate, source_scale,
                  target_translate, target_rotate, target_scale)
            print mir_val

            translate = [0, 0, 0]
            rotate = [0, 0, 0]
            scale = [1, 1, 1]

            # Defining transforms
            # ------------------------------------------------------------------
            # TRANSLATE
            if 'tx' in attributes:
                translate[0] = source_translate[0] * mir_val[0]
            else:
                translate[0] = target_translate[0]

            if 'ty' in attributes:
                translate[1] = source_translate[1] * mir_val[1]
            else:
                translate[1] = target_translate[1]

            if 'tz' in attributes:
                translate[2] = source_translate[2] * mir_val[2]
            else:
                translate[2] = target_translate[2]
            # ------------------------------------------------------------------
            # ROTATE
            if 'rx' in attributes:
                # If mirror
                if mirror:
                    # If mirror X or Y
                    if mirror_axis == 'x' or mirror_axis == 'y':
                        rotate[0] = 180 - source_rotate[0]
                    # If mirror Z
                    else:
                        rotate[0] = -source_rotate[0]
                # If attribute BUT NOT mirror
                else:
                    rotate[0] = source_rotate[0]
            # If NOT attribute
            else:
                rotate[0] = target_rotate[0]

            if 'ry' in attributes:
                # If mirror
                if mirror:
                    # If mirror X or Y
                    if mirror_axis == 'x' or mirror_axis == 'y':
                        rotate[1] = source_rotate[1]
                    # If mirror Z
                    else:
                        rotate[1] = -source_rotate[1]
                # If attribute BUT NOT mirror
                else:
                    rotate[1] = source_rotate[1]
            # If NOT attribute
            else:
                rotate[1] = target_rotate[1]

            if 'rz' in attributes:
                # If mirror
                if mirror:
                    # If mirror X
                    if mirror_axis == 'x':
                        rotate[2] = 180 - source_rotate[2]
                    # If mirror Y
                    elif mirror_axis == 'y':
                        rotate[2] = -source_rotate[2]
                    # If mirror Z
                    else:
                        rotate[2] = source_rotate[2]
                # If attribute BUT NOT mirror
                else:
                    rotate[2] = source_rotate[2]
            # If NOT attribute
            else:
                rotate[2] = target_rotate[2]
            # ------------------------------------------------------------------
            # SCALE
            if 'sx' in attributes:
                scale[0] = source_scale[0] * mir_val[0]
            else:
                scale[0] = target_scale[0]

            if 'sy' in attributes:
                scale[1] = source_scale[1] * mir_val[1]
            else:
                scale[1] = target_scale[1]

            if 'sz' in attributes:
                scale[2] = source_scale[2] * mir_val[2]
            else:
                scale[2] = target_scale[2]

            # Normalize rotate values
            for i, value in enumerate(rotate):
                if value > 180:
                    rotate[i] -= 360
                elif value < -180:
                    rotate[i] += 360
                else:
                    rotate[i] = value

            # Move the target according to the new coordinates
            if world_space:
                print(source_translate, source_rotate, source_scale,
                      target_translate, target_rotate, target_scale, )
                mc.xform(target, t=translate, ws=True)
                mc.xform(target, ro=rotate, ws=True)
                mc.xform(target, s=scale, ws=True)
            else:
                print(source_translate, source_rotate, source_scale,
                      target_translate, target_rotate, target_scale, )
                mc.xform(target, t=translate, os=True)
                mc.xform(target, ro=rotate, os=True)
                mc.xform(target, s=scale, os=True)

        # UNDO : Close history chunk
        finally:
            mc.undoInfo(closeChunk=True)
