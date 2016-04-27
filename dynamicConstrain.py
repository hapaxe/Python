#Selectionnez votre controleur, entrez votre obj a contraindre, votre ct 1 (dyn), puis votre ct 2 (CTRL)(sans le nombre et entre apostrophes), puis le nombre d'iterations

import maya.cmds as mc

selection = mc.ls(sl=True, fl=True)

chain1 = input()
chainDyn = input()
chainCTRL = input()
longueur = input()
longueur = int(longueur)
i = 0
nameReverse = selection[0] + 'Reverse'
mc.shadingNode('reverse', asUtility=True, name = nameReverse)
mc.connectAttr(selection[0] + '.SWITCH', nameReverse + '.inputX')

while i < longueur:
   j = str(i)
   skChain = chain1 + j
   skChainDyn = chainDyn + j
   skChainCTRL = chainCTRL + j
   ctName = "chainConstrain" + j

   mc.parentConstraint( skChainDyn, skChainCTRL, skChain, name = ctName)
   mc.connectAttr(selection[0] + '.SWITCH', ctName + '.' + skChainDyn + 'W0')
   mc.connectAttr(nameReverse + '.outputX', ctName + '.' + skChainCTRL + 'W1')
   i += 1
