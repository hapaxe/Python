import maya.cmds as cmds

maSelection = cmds.ls(sl=True, fl=True)
i=0


while i<len(maSelection):
    monAttr = maSelection[i] + '.en_occlusion'
    cmds.setAttr(monAttr, 1)
    i+=1