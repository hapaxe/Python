import maya.cmds as cmds

selection = cmds.ls(sl=True, fl=True)

for i, elt in enumerate(selection):
    cmds.polyNormalizeUV(selection[i], pa = 0)