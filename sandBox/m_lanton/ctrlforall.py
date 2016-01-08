__author__ = 'm.lanton'
import maya.cmds as mc
import sandBox.m_lanton.ml_utilities as mlutilities


def ctrl_for_all(size='default', normal=(0, 1, 0)):
    selection = mc.ls(sl=True)

    for node in selection:
        node_name = node.split('|')[-1]

        pos = mc.xform(node, q=True, rp=True, ws=True)
        rot = mc.xform(node, q=True, ro=True, ws=True)
        sca = mc.xform(node, q=True, s=True)

        new_name = node_name + '_ctrl'

        bbox = mc.exactWorldBoundingBox(node, ignoreInvisible=True)
    
        # calculate ctrl size
        bbox_size = [0, 0]
        bbox_size[0] = bbox[3]-bbox[0]
        bbox_size[1] = bbox[5]-bbox[2]
        bbox_size.sort()
        ctrl_size = size
        if size == 'default':
            ctrl_size = bbox_size[1]*0.6/sca[0]


        # create circle and place it
        mc.circle(name=new_name, normal=normal, sections=8, radius=ctrl_size)
        mlutilities.color([new_name + 'Shape'], 'yellow')
        mc.addAttr(new_name, at='bool', k=True, h=False, ln='VISIBLE')
        mc.connectAttr(new_name+'.VISIBLE', node+'.visibility')
        mc.setAttr(new_name+'.VISIBLE', 1)
        mc.setAttr(new_name+'.visibility', k=False, cb=False)
        mc.makeIdentity(new_name, apply=True, s=True, r=True, t=True)
        mc.xform(new_name, t=pos)
        mc.xform(new_name, ro=rot)

        node_orig = mlutilities.orig(node=new_name)

        mc.parentConstraint('|'+node_orig+'|'+new_name, node)
        mc.scaleConstraint('|'+node_orig+'|'+new_name, node, mo=True)
        mc.delete(new_name, ch=True)

        # parent to existing hierarchy
        if mc.objExists('helper_ctrl'):
            mc.parent(node_orig, 'helper_ctrl')
        elif mc.objExists('walk_ctrl'):
            mc.parent(node_orig, 'walk_ctrl')
        else:
            pass

    # append ctrl to the existing rig set
    mlutilities.rigset()