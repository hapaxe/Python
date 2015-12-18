import maya.cmds as cmds

maSelection = cmds.ls(sl=True, fl=True)

longueur = len(maSelection)

i=0
while i < longueur:
    nameMult = "MULT_" + maSelection[i]
    myShader = cmds.shadingNode('multiplyDivide', n=nameMult, au=True)
    cmds.connectAttr(maSelection[i] + ".translate", nameMult + ".input1")
    cmds.setAttr(nameMult + ".input2", -1, -1, -1)
    cmds.connectAttr(nameMult + ".output", maSelection[i] + "_offset.translate")
    i+=1