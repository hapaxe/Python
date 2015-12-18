__author__ = 'm.lanton'
import maya.cmds as mc
import sandBox.m_lanton.ml_utilities as mlutilities

datas = {'count_b':0, 'count_s':0, 'count_w':0}


# create an orb ctrl
def create_orb(sca=[1.0, 1.0, 1.0], name='empty', *args):
    ctrl_shape = mc.circle(nr=[0, 1, 0])[0]

    circle_list = list()
    circle_list.append(mc.duplicate(rr=True)[0])
    mc.xform(ro=[90, 0, 0])

    circle_list.append(mc.duplicate(rr=True)[0])
    mc.xform(ro=[90, 90, 0])

    circle_list.append(mc.duplicate(rr=True)[0])
    mc.xform(ro=[90, 45, 0])

    circle_list.append(mc.duplicate(rr=True)[0])
    mc.xform(ro=[90, -45, 0])

    mc.select(circle_list)
    mc.makeIdentity(apply=True, t=True, r=True, s=True)
    mc.pickWalk(d='down')
    mc.select(ctrl_shape, tgl=True)
    mc.parent(r=True, s=True)
    mc.delete(circle_list)
    mc.xform(ctrl_shape, cp=True)

    if name != 'empty':
        ctrl_shape = mc.rename(ctrl_shape, name)
    mc.xform(ctrl_shape, s=sca)
    mc.makeIdentity(apply=True, s=True)

    return ctrl_shape


def create_deform(deform_type, axis, current_node):
    if deform_type == 'bend':
        deform = deform_type + str(datas['count_b'])
    if deform_type == 'squash':
        deform = deform_type + str(datas['count_s'])
    if deform_type == 'wave':
        deform = deform_type + str(datas['count_w'])
    mc.select(current_node)
    mc.nonLinear(typ=deform_type)
    deform_name = mc.rename(deform, current_node+ '_'+deform_type+'_'+axis)
    deform_handle = mc.rename(deform+'Handle', current_node+'_'+deform_type+'Handle'+axis)
    return [deform_name, deform_handle]


# create a wave deformer and the system to control it
def wave_for_each():
    """Create a wave deformer and controlers for every selected element"""

    # what's selected
    selection = mc.ls(sl=True)

    # for each selected node
    for node in selection:
        datas['count_w']+=1
        # get the name and the transforms
        node_name = node.split('|')[-1]
        pos = mc.xform(node, q=True, rp=True, ws=True)

        # def name of the new nodes
        ctrl_name = node_name + '_ctrl'
        wave_name = node_name + '_wave'
        wave_control = node_name + '_wave_ctrl'
        orb_name = node_name + '_orb'
        mover_name = node_name + '_mover'

        # calculate ctrl size
        #bbox
        bbox = mc.exactWorldBoundingBox(node, ignoreInvisible=True)
        bbox_size = [0, 0]
        bbox_size[0] = bbox[3] - bbox[0]
        bbox_size[1] = bbox[5] - bbox[2]
        bbox_size.sort()
        bbox_height = bbox[4] - bbox[1]

        ctrl_size = bbox_size[1] * 0.5

        # orb and mover
        orb_size = 5

        # create ctrl and place it
        mc.circle(name=wave_control, normal=(0, 1, 0), sections=8, radius=ctrl_size)
        zero_out_wave_ctrl = mlutilities.zero_out(wave_control)

        mlutilities.create_orb(sca=orb_size/2, name=orb_name)
        mc.spaceLocator(name=mover_name + 'loc', a=True, p=[0, 0, 0])
        mc.parent(mover_name + 'loc', orb_name)

        # create wave
        wavenode = create_deform('wave', '', node)
        print wavenode

        # creates wave hierarchy
        mc.parent(orb_name, wave_control)

        #color
        mlutilities.color([wave_control + 'Shape'], 'light_blue')
        mlutilities.color([orb_name], 'green')

        # bindPreMatrix
        #mc.connectAttr(wave_control + '.worldInverseMatrix', wave_name + '.bindPreMatrix')

        # ctrl placement
        mc.xform(zero_out_wave_ctrl, t=[pos[0], pos[1] + (bbox_height / 2), pos[2]])
        #mc.xform(zero_out_wave_ctrl, ro=rot)

        # parent to existing hierarchy        
        if mc.objExists(ctrl_name):
            mc.parent(zero_out_wave_ctrl, ctrl_name)
        elif mc.objExists('helper_ctrl'):
            mc.parent(zero_out_wave_ctrl, 'helper_ctrl')
        else:
            mc.parent(zero_out_wave_ctrl, 'walk_ctrl')