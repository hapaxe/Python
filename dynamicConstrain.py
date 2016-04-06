#Selectionnez votre controleur, entrez votre obj a contraindre, votre ct 1 (dyn), puis votre ct 2 (CTRL)(sans le nombre et entre apostrophes), puis le nombre d'iterations

import maya.cmds as cmds

selection = cmds.ls(sl=True, fl=True)

chaine1 = input()
chaineDyn = input()
chaineCTRL = input()
longueur = input()
longueur = int(longueur)
i=0
nameReverse = selection[0] + 'Reverse'
cmds.shadingNode('reverse', asUtility=True, name = nameReverse)
cmds.connectAttr(selection[0] + '.SWITCH', nameReverse + '.inputX')

while i < longueur :
   j = str(i)
   skChaine = chaine1 + j
   skChaineDyn = chaineDyn + j
   skChaineCTRL = chaineCTRL + j
   ctName = "chainConstrain" + j

   cmds.parentConstraint( skChaineDyn, skChaineCTRL, skChaine, name = ctName)
   cmds.connectAttr(selection[0] + '.SWITCH', ctName + '.' + skChaineDyn + 'W0')
   cmds.connectAttr(nameReverse + '.outputX', ctName + '.' + skChaineCTRL + 'W1')
   i+=1