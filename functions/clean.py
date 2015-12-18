#----------------------------------------------------------------------
# functions clean
# Author : felixlechA.com | f.rault
# Date   : february 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint

#----------------------------------------------------------------------
def nameSpace_removeAll( mode= 'command' ):
    '''
    Remove all nameSpace in current scene

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    # --- Get all assembly in current scene
    assembly_all = mc.ls( type= 'assemblyReference' ) or list()

    # --- Get assembly nameSpace
    ns_to_skip = ['UI','shared']

    for ass in assembly_all:
        ass_ns= mc.getAttr( ass + '.repNamespace' )

        if not ass_ns in ns_to_skip:
            ns_to_skip.append( ass_ns )

    # --- Get All NameSpace
    nameSpace= mc.namespaceInfo( ':', lon= True, recurse=True )
    nameSpace.reverse()

    # --- Delete NameSpace
    nbr = 0
    for ns in nameSpace:
        if not ns.split(':')[-1] in ns_to_skip:
            mc.namespace( removeNamespace= ns, mergeNamespaceWithParent = True)
            nbr = nbr + 1

    if nbr:
        logMsg = str(nbr) +' nameSpace have been Removed'
    else:
        logMsg = 'no nameSpace to delete'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def unknowNodes_remove( mode= 'command' ):
    '''
    Remove unknow noReferenced nodes

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    # --- Get unknow node
    unknown_node = mc.ls( type= [ 'unknown', 'unknownDag', 'unknownTransform'] )

    # --- Delete only noReferenced node
    delete_node= list()
    for node in unknown_node:
        if mc.objExists( node ):
            if not mc.referenceQuery( node, isNodeReferenced= True ):
                delete_node.append( node )
                mc.delete( node )

    if delete_node:
        logMsg = str(len(delete_node)) +' Unknow node deleted :' + ' '.join(delete_node)
    else:
        logMsg = 'no Unknow node to delete'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def unused_animCurve_remove( mode= 'command' ):
    '''
    Remove unused noReferenced animCurves

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    # --- Get animCurves node
    keys_node = mc.ls( type= 'animCurve' ) or list()

    # --- Delete only noReferenced animCurves node
    delete_node= list()
    for key_node in keys_node:
        connections = mc.listConnections( key_node + '.output', s=False, d= True, plugs= True ) or list()
        if not mc.referenceQuery( key_node, isNodeReferenced= True ) and len(connections) == 0:
            delete_node.append( key_node )
            mc.delete( key_node )

    if delete_node:
        logMsg = str(len(delete_node)) +' animCurve nodes deleted'
    else:
        logMsg = 'no animCurve nodes to delete'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def unused_hyperView_remove( mode= 'command' ):
    '''
    Remove unused hyperView, hyperLayout

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    # --- Get all hyperView in current scene
    hyperViewNodes = mc.ls(type=['hyperView']) or list()

    # - Calculate how mutch hyperView we have
    hyperView_nbr = len(hyperViewNodes)

    # --- Remove hyperView
    if hyperViewNodes:
        mc.delete( hyperViewNodes )
        hyperView = mc.ls(type=['hyperView']) or list()
        logMsg =  str( hyperView_nbr - len(hyperView))+ ' hyperView remove'
        print hyperView
    else:
        logMsg =  'no hyperView to delete found'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def useless_scriptNode_remove( mode= 'command' ):
    '''
    Remove useless scriptNodes

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    # --- Get all scriptNode in current scene
    scriptNodes = mc.ls(type='script') or list()

    # - Calculate how mutch scriptNode we have
    scriptNodes_nbr = len(scriptNodes)

    # - Keep the sceneConfigurationScriptNode node
    if 'sceneConfigurationScriptNode' in scriptNodes:
        scriptNodes.remove('sceneConfigurationScriptNode')

    # --- Remove useless scriptNode
    if scriptNodes:
        mc.delete( scriptNodes )
        scriptNodes = mc.ls(type='script') or list()
        logMsg =  str( scriptNodes_nbr - len(scriptNodes))+ ' scriptNode remove'
    else:
        logMsg =  'no scriptNode to delete found'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def fosterParent_remove( mode= 'command' ):
    '''
    Remove all fosterParent in scene

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    fosterParent = mc.ls( type='fosterParent' ) or list()

    if fosterParent:
        for foster in fosterParent:
            mc.lockNode( foster, lock=False )
            mc.delete( foster )
        logMsg =  str(len(fosterParent))+ ' fosterParent remove'
    else:
        logMsg =  'no fosterParent to remove'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def ghostMesh_remove( mode= 'command' ):
    '''
    Remove all mesh intermediate shape connected to nothing

    :param mode: Define if command is launch by 'menu' or by 'command'
    :type mode: string

    :return: none
    '''
    allShape= mc.ls( type= 'mesh', intermediateObjects= True  )

    ghostShape= list()
    for item in allShape:
        link= mc.listConnections( item )
        if not link:
            ghostShape.append( item )

    if ghostShape:
        mc.delete( ghostShape )
        logMsg =  str(len(ghostShape))+ ' ghostShape remove'
    else:
        logMsg =  'no ghostMesh to remove'

    if mode == 'menu':
        viewPrint( msg= logMsg, mode=1 )
    else:
        print logMsg

#----------------------------------------------------------------------
def channelBox_inputHistory( obj_list= None, hide_shape= False ):
    '''
    Clean ChannelBox Input History deformer list

    :param obj_list: List of object to clean
    :type obj_list: list

    :return: none
    '''
    # --- Get selection
    if not obj_list:
        obj_list= mc.ls( sl= True ) or list()

    if len(obj_list) == 0:
        print 'Select some object to Clean'
        return

    log_dict= dict()
    for item in obj_list:
        log_dict[item]= list()
        # --- Get Construction History
        history_nodes = mc.listHistory( item )

        # - Remove Self
        if history_nodes.count( item ):
            history_nodes.remove( item )

        # --- Skip Node Types
        to_skip= list()
        to_skip.extend( ['groupId','shadingEngine','transform', 'groupParts', 'unitConversion'] )
        # - Skip deformer
        to_skip.extend( [ 'skinCluster', 'wrap', 'nonLinear', 'cluster', 'softMod', 'ffd', 'jiggle', 'wire', 'sculpt', 'blendShape' ] )
        to_skip.extend( [ 'deformBend', 'clusterHandle', 'softModHandle' ] )
        # - Add radialBlendShape if plugin is loaded
        if mc.pluginInfo('radialBlendShape', q=True, l=True):
            to_skip.extend( [ 'radialBlendShape' ] )
        # - Skip tweak
        to_skip.extend( [ 'tweak' ] )
        # - Skip Shape
        if not hide_shape:
            to_skip.extend( ['locator', 'mesh', 'nurbsCurve'] )

        # - Clean history list
        ignore_nodes= mc.ls( history_nodes, type= to_skip )
        history_nodes= list(set( history_nodes )-set( ignore_nodes ))

        # - Hide Input ChannelBox visibility
        for node in history_nodes:
            if mc.getAttr( node + '.ihi') != 0:
                mc.setAttr( node + '.ihi', 0)
                log_dict[item].append( node )

    # Refresh selection to update channelBox
    mc.select( clear= True )
    mc.select( obj_list )

    logMsg = '-----\nClean channelBox input History :\n\n'

    for key in log_dict.keys():
        logMsg += key + ' :\n'
        if len( log_dict[key] ):
            logMsg += '  '+ str(log_dict[key]) +'\n'
        else:
            logMsg += '  nothink to clean\n'
    logMsg += '\n-----'

    print logMsg