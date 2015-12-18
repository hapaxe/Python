__author__ = 'v.moriceau'

from maya import cmds
import common
import frustum

map(reload,[frustum, common])

def clean_containers():
    # Get All Containers
    containers = cmds.ls(type='container', long=True)
    # Each Container
    for container in containers:
        try:
            # Set blackBox to False
            cmds.setAttr(container + '.blackBox', False)
            # Verbose
            print 'Clean Containers : %s.blackBox set to False' % container
        except:
            # Verbose
            print 'Clean Containers : %s.blackBox is locked !' % container

def bake_visibility(nodes):
    # If Any node given
    if nodes:
        # Apply Bake
        _bake_geo_attr(nodes, 'visibility')

def bake_focal_length(nodes):
    # If Any node given
    if nodes:
        # Get Node's shapes
        nodes_shapes = []
        for node in nodes:
            shape = cmds.listRelatives(node, children=True, type='shape', fullPath=True)
            if shape:
                nodes_shapes.append(shape[0])
        # Apply Bake
        _bake_geo_attr(nodes_shapes, 'focalLength')

def frustum_cull(cam_name):
    # Get All Assemblies
    note_to_test = [transform for transform in cmds.ls(type='transform', long=True)
                    if cmds.nodeType(transform) == 'assemblyReference'
                    and not common.get_cube_tag(transform, 'lock_representation')]
    # Find What is not in cam frustum
    nodes_to_hide = frustum.cull(cam_name, note_to_test)
    # Each found
    for node_to_hide in nodes_to_hide:
        try:
            # Set Representatin to None
            cmds.assembly(node_to_hide, edit=True, active='')
        except ValueError:
            # Verbose
            print "Cleaning : '%s' Cannot be set to None, maybe a nested assembly already set to None" % node_to_hide
    # Return Culled Nodes
    return nodes_to_hide

def _bake_geo_attr(nodes, attribute_name):
    # Verbose
    print 'Cleaning : Baking \'%s\'' % attribute_name
    # Get Timeline info
    frame_in = int(cmds.playbackOptions(q=True, animationStartTime=True))
    frame_out = int(cmds.playbackOptions(q=True, animationEndTime=True))
    # Create a dict
    baked_attribute_values = dict()
    # Each Node wich has the attribute
    for node in nodes:
        # If Has Attribute
        if attribute_name in cmds.listAttr(node):
            # Prepare to store keys in dict
            baked_attribute_values[node] = dict()
    # Suspend Viewport refreshing
    cmds.refresh(su=True)
    # Get Attribute Info > store in dict
    for i in range(frame_in, frame_out, 1):
        # Set current time
        cmds.currentTime(i)
        # Each bakeable node
        for node in baked_attribute_values.keys():
            baked_attribute_values[node][i] = cmds.getAttr('%s.%s' % (node, attribute_name))
    # Resume Viewport refreshing
    cmds.refresh(su=False)
    # Break attribute Connection if needed
    for node in baked_attribute_values.keys():
        # Get Connection
        attribute_connection = cmds.listConnections('%s.%s' % (node, attribute_name), s=True, d=False, p=True, c=True)
        # If Exists
        if attribute_connection:
            # If Attribute Locked
            if cmds.getAttr('%s.%s' % (node, attribute_name), lock= True):
                # Unlock
                cmds.setAttr('%s.%s' % (node, attribute_name), lock= False)
            # Disconnect
            cmds.disconnectAttr(attribute_connection[1], '%s.%s' % (node, attribute_name))
        else:
            # Remove previous Keys
            cmds.cutKey(node, attribute=attribute_name, option="keys")
    # Key visibility based on previous analyse
    for i in range(frame_in, frame_out, 1):
        # Each Node
        for node in baked_attribute_values.keys():
            # Set Key
            cmds.setKeyframe(node, attribute=attribute_name, time=i, value=baked_attribute_values[node][i])
