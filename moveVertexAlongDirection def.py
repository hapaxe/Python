import maya.cmds as mc


def move():

    selection = mc.ls(sl=True, fl=True)

    distance = input()
    distance = str(distance)
    dist_list = []

    for i in selection:
        dist_list.append(distance)

    mc.moveVertexAlongDirection(selection, n=dist_list)