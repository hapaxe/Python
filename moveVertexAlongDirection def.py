import maya.cmds as cmds

maSelection = cmds.ls(sl=True, fl=True)

distance = input()
distance = str(distance)
longueur = len(maSelection)
maListe = []

i=0
while i < longueur:
    maListe.append(distance)
    i+=1
    
print(maListe)

cmds.moveVertexAlongDirection(maSelection, n = maListe)