#select the objects you want to be replaced, the object you want to place after them, and run the script

import maya.cmds as mc

selection = mc.ls(sl=True, fl=True)
object_to_dup = selection[-1]
targets = selection[:-1]


for i, obj in enumerate(targets):
    nbr = str(i)
    dup = 'dup_' + object_to_dup + '_' + nbr
    mc.duplicate(object_to_dup, n=dup, ilf=True)
    attr1 = mc.getAttr(selection[i] + '.translateX')
    attr2 = mc.getAttr(selection[i] + '.translateY')
    attr3 = mc.getAttr(selection[i] + '.translateZ')
    attr4 = mc.getAttr(selection[i] + '.rotateX')
    attr5 = mc.getAttr(selection[i] + '.rotateY')
    attr6 = mc.getAttr(selection[i] + '.rotateZ')
    attr7 = mc.getAttr(selection[i] + '.scaleX')
    attr8 = mc.getAttr(selection[i] + '.scaleY')
    attr9 = mc.getAttr(selection[i] + '.scaleZ')
    mc.setAttr(dup + '.translateX', attr1)
    mc.setAttr(dup + '.translateX', attr1)
    mc.setAttr(dup + '.translateY', attr2)
    mc.setAttr(dup + '.translateZ', attr3)
    mc.setAttr(dup + '.rotateX', attr4)
    mc.setAttr(dup + '.rotateY', attr5)
    mc.setAttr(dup + '.rotateZ', attr6)
    mc.setAttr(dup + '.scaleX', attr7)
    mc.setAttr(dup + '.scaleY', attr8)
    mc.setAttr(dup + '.scaleZ', attr9)