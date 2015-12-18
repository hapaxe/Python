import maya.cmds as mc


# Utilise la sélection courrante pour sélectionner le plus haut parent.

selection = []
i=0
dico = {}
new_selection = []


for node in mc.ls( sl=True, l=True):
    node_name = '|' + node.split('|')[1]
    dico[node_name]= node_name
print i

for key in dico :
    new_selection.append(dico[key])
    

mc.select(new_selection)