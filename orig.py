import maya.cmds as mc

def orig(node=['empty']):
    """
    Cree un group offset orig
    :param node: string : name of the node to offset
    :return: string : name of the orig
    """

    if node == ['empty']:
        node = mc.ls(sl=True)
    for object in node:
        orig = mc.group(em=True, name=object + '_orig')
        constraint = mc.parentConstraint(object, orig, mo=False)
        mc.delete(constraint)
        mc.parent(object, orig)
    return orig