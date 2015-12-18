#selectionnez vos objets à remplacer, puis lancer le script, entrez le nom de l'objet qui remplace avec des  apostrophes :''

import maya.cmds as cmds
import random as ran

selection = cmds.ls(sl=True, fl=True)
objetADup = input()
cmds.select(objetADup)

i=0
while i<len(selection):
	nbr = str(i)
	dup = 'dup_' + objetADup + '_' + nbr
	cmds.duplicate(objetADup, n = dup, ilf = True)
	attr1 = cmds.getAttr(selection[i] + '.translateX')
	attr2 = cmds.getAttr(selection[i] + '.translateY')
	attr3 = cmds.getAttr(selection[i] + '.translateZ')
	attr4 = cmds.getAttr(selection[i] + '.rotateX')
	attr5 = cmds.getAttr(selection[i] + '.rotateY')
	attr6 = cmds.getAttr(selection[i] + '.rotateZ')
	attr7 = cmds.getAttr(selection[i] + '.scaleX')
	attr8 = cmds.getAttr(selection[i] + '.scaleY')
	attr9 = cmds.getAttr(selection[i] + '.scaleZ')
	cmds.setAttr(dup + '.translateX', attr1)
	cmds.setAttr(dup + '.translateX', attr1)
	cmds.setAttr(dup + '.translateY', attr2)
	cmds.setAttr(dup + '.translateZ', attr3)
	cmds.setAttr(dup + '.rotateX', attr4)
	cmds.setAttr(dup + '.rotateY', attr5)
	cmds.setAttr(dup + '.rotateZ', attr6)
	cmds.setAttr(dup + '.scaleX', attr7)
	cmds.setAttr(dup + '.scaleY', attr8)
	cmds.setAttr(dup + '.scaleZ', attr9)
	#cmds.delete(selection[i])
	i+=1