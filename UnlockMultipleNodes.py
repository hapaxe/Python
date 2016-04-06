import maya.cmds as cmds

maSelection = cmds.ls(sl=True, fl=True)
i=0


while i<len(maSelection):
    cmds.lockNode(maSelection[i], l = False)
    i+=1