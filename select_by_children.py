import maya.cmds as mc


# Use current selection to select higher parent in hierarchy

selection = []
i = 0
dictionary = {}
new_selection = []


for node in mc.ls(sl=True, l=True):
    node_name = '|' + node.split('|')[1]
    dictionary[node_name] = node_name
print i

for key in dictionary:
    new_selection.append(dictionary[key])
    

mc.select(new_selection)