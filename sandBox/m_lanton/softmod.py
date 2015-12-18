__author__ = 'm.lanton'
import maya.cmds as mc
import sandBox.m_lanton.ml_utilities as mlutilities
reload(mlutilities)


#------------------------------------------
# create a softMod deformer and the system to control it
def softmod_for_each(size=1):
    """Create a softMod deformer and controlers for every selected element"""

    # what's selected
    selection = mc.ls(sl=True)

    # for each selected node
    for node in selection:

        # get the name and the transforms
        node_name = node.split('|')[-1]
        pos = mc.xform(node, q=True, rp=True, ws=True)

        # def name of the new nodes
        ctrl_name = node_name + '_ctrl'
        # softmod names
        soft_name = node_name + '_softMod'
        soft_control = node_name + '_softMod_ctrl'
        mover_name = node_name + '_mover_ctrl'

        if mc.objExists(soft_name):
            softmod_list = [softmod for softmod in mc.ls(et='softMod') if soft_name in softmod]

            number = str(len(softmod_list))
            soft_name = node_name + '_softMod_' + number
            soft_control = soft_name + '_ctrl'
            mover_name = node_name + '_mover' + number + '_ctrl'

        # calculate ctrl size
        #bbox
        bbox = mc.exactWorldBoundingBox(node, ignoreInvisible=True)
        bbox_size = [0, 0]
        bbox_size[0] = bbox[3] - bbox[0]
        bbox_size[1] = bbox[5] - bbox[2]
        bbox_size.sort()
        bbox_height = bbox[4] - bbox[1]

        ctrl_size = bbox_size[1] * 0.6

        if ctrl_size > 5.0:
            mover_size = 2.0
        else:
            mover_size = ctrl_size/2.0

        # create ctrl and place it
        mc.circle(name=soft_control, normal=(0, 1, 0), sections=8, radius=ctrl_size)
        #delete history
        mc.delete(soft_control, ch=True)
        zero_out_soft_ctrl = mlutilities.zero_out(soft_control)

        mover = mlutilities.create_ctrl(ctrl_type='simple_orb', name=mover_name, size=mover_size)

        mc.spaceLocator(name=mover_name + 'loc', a=True, p=[0, 0, 0])
        mc.parent(mover_name + 'loc', soft_control)

        # create softMod
        mc.softMod(node, n=soft_name, wn=(mover_name, mover_name))

        # creates softMod hierarchy
        mc.parent(mover[1], soft_control)

        # create/set/connect Attributes
        #visibility
        mc.connectAttr(mover_name + 'locShape.worldPosition', soft_name + '.falloffCenter')
        #size
        mc.addAttr(mover_name, at='float', k=True, h=False, ln='size', dv=5, min=0.001, max=50)
        mc.connectAttr(mover_name + '.size', soft_name + '.falloffRadius')
        #set display in channel box
        #mover
        mc.setAttr(mover_name + '.visibility', k=False, cb=False)
        #softMod ctrl
        mc.setAttr(soft_control + '.scaleX', k=False, cb=False)
        mc.setAttr(soft_control + '.scaleY', k=False, cb=False)
        mc.setAttr(soft_control + '.scaleZ', k=False, cb=False)
        mc.setAttr(soft_control + '.visibility', k=False, cb=False)
        #locator
        mc.setAttr(mover_name + 'loc.visibility', 0)

        #color
        mlutilities.color([soft_control + 'Shape'], 'cyan')
        mlutilities.color([mover_name + 'Shape'], 'dark_pink')

        # bindPreMatrix
        mc.connectAttr(soft_control + '.worldInverseMatrix', soft_name + '.bindPreMatrix')
        mc.connectAttr(node + '.worldMatrix[0]', soft_name + '.geomMatrix[0]', f=True)

        # ctrl placement
        mc.xform(zero_out_soft_ctrl, t=[pos[0], pos[1] + (bbox_height / 2), pos[2]])
        #mc.xform(zero_out_soft_ctrl, ro=rot)

        # parent to existing hierarchy        
        if mc.objExists(ctrl_name):
            mc.parent(zero_out_soft_ctrl, ctrl_name)
        elif mc.objExists('helper_ctrl'):
            mc.parent(zero_out_soft_ctrl, 'helper_ctrl')
        elif mc.objExists('walk_ctrl'):
            mc.parent(zero_out_soft_ctrl, 'walk_ctrl')
        else:
            pass

    mlutilities.rigset()