import maya.cmds as cmds

selection = cmds.ls(sl=True, fl=True)
i=0
longueur = len(selection) - 1

while i<longueur:
    cmds.connectAttr(selection[-1] + ".translate", selection[i] + ".translate")
    i+=1