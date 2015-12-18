__author__ = 'm.lanton'
import maya.cmds as mc


def create_arm():
    selection = mc.ls(sl=True)

    if len(selection) == 1:
        position = mc.xform(selection[0], q=True, t=True)
    loc1 = mc.spaceLocator(n=selection[0]+'_loc_shoulder')
    loc2 = mc.spaceLocator(n=selection[0]+'_loc_wrist')
    mc.xform(loc2, t=[10, 0, 0])
    mc.aimConstraint(loc2, loc1, aim=[1, 0, 0])
    mc.aimConstraint(loc1, loc2, aim=[1, 0, 0])
    mc.select(loc1, loc2)
    group = mc.group(n='guide_group')
    mc.xform(group, t=position)