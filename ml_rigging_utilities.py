import maya.cmds as mc


def rivet(components=[]):
    """
    Create a rivet on an edge or a selection of edges.
    :param components: list of the component to rivet.
    :type components: list

    :return:
    """
    if not components:
        components = mc.ls(sl=True, fl=True)

    obj = components[0].split('.')
    edge1 = components[0].split('[')[-1].split(']')[0]

    if len(components) > 1 :
        edge2 = components[1].split('[')[-1].split(']')[0]
    elif len(components) == 1:
        cfme1 = mc.createNode('curveFromMeshEdge', n='rivetCurveFromMeshEdge##')
        mc.setAttr('%s.ihi' % cfme1, 1)
        mc.setAttr('%s.ei[0]' % cfme1, 1)
