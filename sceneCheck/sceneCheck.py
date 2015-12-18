#----------------------------------------------------------------------
# sceneCheck sceneCheck
# Author : felixlechA.com | f.rault
# Date   : February 2015
# Decription : Check scene and do things
#----------------------------------------------------------------------
import maya.cmds as mc
import functions.animation as animation
reload( animation )

import os

#----------------------------------------------------------------------
def get_AssemblyInfo():
    '''
    For the current scene build and return a dictionnary contain all assembly info

    :return: A dictionnary of all assembly info
    :rtype: dictionnary
    '''
    # --- Create an empty dictionnary
    info_dict = dict()

    # --- Get all assembly in current scene
    assembly_all = mc.ls( type= 'assemblyReference' ) or list()

    # --- Loop on Assembly
    for item in assembly_all:
        # --- TYPE
        # - Get Type
        if mc.objExists( item + '.cube_type' ):
            type= mc.getAttr( item + '.cube_type' )
        else:
            type= 'UFO'

        # - Create/Check key : Type
        if not  type in info_dict.keys():
            info_dict[ type ]= {}

        # - Create a key for item
        info_dict[ type ][ item ] = {}

        # --- Populate item info
        if mc.objExists( item + '.repNamespace' ):
            nameSpace= mc.getAttr( item + '.repNamespace' )
            info_dict[ type ][ item ][ 'NameSpace' ] = nameSpace
        info_dict[ type ][ item ][ 'State' ] = mc.assembly( item, activeLabel= True, query= True )
        info_dict[ type ][ item ][ 'Path' ] = mc.getAttr( item + '.definition' )
        if mc.objExists( item + '.cube_name' ):
            info_dict[ type ][ item ][ 'CubeName' ] = mc.getAttr( item + '.cube_name' )

        # --- Get the master_ctrl
        if info_dict[ type ][ item ][ 'State' ] in [ 'setupLOD0', 'setupLOD2' ] and mc.objExists( nameSpace +':master_ctrl' ):
            info_dict[ type ][ item ][ 'MasterCtrl' ] = nameSpace +':master_ctrl'

    return info_dict

#----------------------------------------------------------------------
def get_AssemblyToSwitchAsRef( info_dict, force_state= None, force_setup_state= False ):
    '''
    From the info_dict build and return a dictionnary contain all assembly to switch as ref info

    :param info_dict:
    :type info_dict: dictionnary

    :param force_state: Name of state to force if file corresponding exist
    :type force_state: string

    :param force_setup_state: For clean export assembly force to switch all setup state to Ref
    :type force_setup_state: boolean

    :return: A dictionnary of assembly to switch as ref info
    :rtype: dictionnary
    '''
    # --- Create an empty dictionnary
    toSwitch_dict = dict()

    # --- Loop
    for type in info_dict.keys():
        for item in info_dict[type].keys():
            # --- Props, Characters and Camera
            if type in ['PR', 'CH', 'CM', 'FX']:
                # --- Process only Assembly on setupLOD 0 or 2 state
                if info_dict[ type ][ item ]['State'] in ['setupLOD0', 'setupLOD1', 'setupLOD2']:
                    assembly_parent= mc.listRelatives( item, parent= True, fullPath= True )[0]

                    # --- Define the Root grp
                    assembly_root= ''
                    for root in ['BG_ROOT', 'PR_ROOT', 'CH_ROOT', 'CM_ROOT', 'FX_ROOT', 'AM_ROOT', 'GD_ROOT', 'LT_ROOT', 'MT_ROOT']:
                        if root in assembly_parent:
                            assembly_root= root
                            continue

                    # --- For Assembly in Assembly we need to rebuild the complet nameSpace
                    if len( item.split(':') ) > 1:
                        preNS= item.split(':')[:-1]
                        assembly_complet_NS= ':'.join(preNS)+':'+info_dict[type][item]['NameSpace']
                    else:
                        assembly_complet_NS= info_dict[type][item]['NameSpace']

                    # --- Define if Assembly was Animated or just Posed
                    assembly_isAnimated= animation.check_AnimKeys_inSet( inSet= assembly_complet_NS +':RIG_SET', remove_cstr= True )

                    # --- Get Controlers from SET
                    list_Ctrls= list()
                    if mc.objExists( assembly_complet_NS +':RIG_SET' ):
                        list_Ctrls= mc.sets( assembly_complet_NS +':RIG_SET', q=True )

                    # --- BG Props to Switch
                    if assembly_root == 'PR_ROOT' or type in ['CH', 'CM', 'FX'] or assembly_root == 'BG_ROOT' and assembly_isAnimated or assembly_root == 'BG_ROOT' and force_setup_state and info_dict[ type ][ item ]['State'] in ['setupLOD1', 'setupLOD2']:
                        # Assembly name to switch
                        toSwitch_dict[item] = dict()

                        # old Assembly futur
                        if assembly_root == 'BG_ROOT':
                            toSwitch_dict[item]['AssemblyFutur'] = 'switch'
                            toSwitch_dict[item]['AssemblyTranslate'] = mc.xform( item, q=True, ws=True, t=True )
                            toSwitch_dict[item]['AssemblyRotate'] = mc.xform( item, q=True, ws=True, ro=True )
                            toSwitch_dict[item]['AssemblyScale'] = mc.xform( item, q=True, s=True, r=True )
                        else:
                            toSwitch_dict[item]['AssemblyFutur'] = 'remove'

                        # For 'PR' force parent to 'PR_ROOT'
                        if type == 'PR':
                            assembly_root = 'PR_ROOT'
                        # reParent Ref to parent
                        toSwitch_dict[item]['Parent'] = assembly_root
                        # NameSpace Assembly
                        toSwitch_dict[item]['AssemblyNameSpace'] = assembly_complet_NS
                        # State
                        state = info_dict[type][item]['State']
                        toSwitch_dict[item]['State'] = state
                        # The Anim Ctrls to get anim/pose and reApply
                        if list_Ctrls:
                            toSwitch_dict[item]['Controler'] = list_Ctrls
                        # Path
                        assembly_path= info_dict[type][item]['Path']
                        toSwitch_dict[item]['AssemblyPath'] = assembly_path
                        # Build Ref path
                        path_list= assembly_path.split('/')
                        path= path_list[:-2]

                        # Force setupLOD2 if possible
                        if force_state:
                            path_setupLOD2= path
                            path_setupLOD2.append( force_state )
                            path_setupLOD2.append( path_list[-1].replace( 'assemblyDef', force_state ) )
                            path_setupLOD2_full= '/'.join( path_setupLOD2 )

                            if os.path.isfile( path_setupLOD2_full ):
                                toSwitch_dict[item]['State'] = force_state
                                toSwitch_dict[item]['Path'] = path_setupLOD2_full
                                continue

                        # If force_state don't exist set the current state path
                        path.append( state )
                        path.append( path_list[-1].replace( 'assemblyDef', state ) )
                        toSwitch_dict[item]['Path'] = '/'.join( path )

    # Return Assembly to Switch
    return toSwitch_dict

#----------------------------------------------------------------------
def duplicate_animCurve( toSwitch_dict ):
    '''
    Duplicate the anim Curve of controlers define in toSwitch_dict Dictionnary

    :param toSwitch_dict: Contain toSwitch as ref infos
    :type toSwitch_dict: dictionnary

    :return: None
    '''
    # --- Get ctrls
    controlers = list()
    for item in toSwitch_dict.keys():
        if 'Controler' in toSwitch_dict[item].keys():
            controlers.extend( toSwitch_dict[item]['Controler'] )
        else:
            print '! '+ item +' have no Controlers list in RIG_SET'

    # --- Duplicate AnimCurve for each Controler
    for ctrl in controlers:
        anim_keys= list()

        # --- Get camera Shape
        if 'cam' in ctrl:
            cam_Shape= mc.listRelatives( ctrl, s= True )
            if mc.nodeType( cam_Shape ) == 'camera':
                anim_keys.extend( mc.listConnections( cam_Shape , s=True, d=False, type='animCurve') or list() )

        # --- Get animation Keys
        anim_keys.extend( mc.listConnections( ctrl , s=True, d=False, type='animCurve') or list() )

        # --- For each key Duplicate with a specific name
        for key in anim_keys:
            # For each key get the Attribut associate and build an unique name based on
            key_name= mc.listConnections( key + '.output', s=False, d= True, plugs= True )[0].replace(':', '_0_').replace('.', '_Attr_')
            # Duplicate the key
            mc.duplicate( key, name= 'TO_DELETE_'+ key_name )

#----------------------------------------------------------------------
def switch_assembly_to_ref( toSwitch_dict ):
    '''
    Switch Assembly to Reference file

    :param toSwitch_dict: Contain toSwitch as ref infos
    :type toSwitch_dict: dictionnary

    :return ctrls_dict: Contain NameSpace Assembly Ref, list of Reference Controls
    :rtype: dictionnary
    '''
    # Create an empty dictionnary
    ctrls_dict = dict()

    # --- Switch Assembly to Ref
    for item in toSwitch_dict.keys():

        # --- Deal with old Assembly
        if toSwitch_dict[item]['AssemblyFutur'] == 'switch':
            # - switch to None
            mc.assembly( item, edit= True, active= '' )
        elif toSwitch_dict[item]['AssemblyFutur'] == 'remove':
            # - remove Assembly
            mc.delete( item )

        item_ns = item
        if ':' in item:
            item_ns = item.replace(':', '_')

        # --- Import corresponding Ref
        ref_path= toSwitch_dict[item]['Path']
        ns_before= set( mc.namespaceInfo( ':', listOnlyNamespaces= True, recurse= True )) # get NS before import
        ref_file= mc.file( ref_path, reference=True, type='mayaAscii', namespace= item_ns )
        ns_after= set( mc.namespaceInfo( ':', listOnlyNamespaces= True, recurse= True )) # get NS After import

        # --- Get new NameSpace
        ref_ns= list(ns_after - ns_before)[0]
        split_ns = ref_ns.split(':')
        if len(split_ns) > 1:
            ref_ns = split_ns[0]

        # --- Deal with Reference PR from Assembly BG
        if toSwitch_dict[item]['AssemblyFutur'] == 'switch':
            Ass_pos= toSwitch_dict[item]['AssemblyTranslate']
            Ass_rot= toSwitch_dict[item]['AssemblyRotate']
            Ass_scl= toSwitch_dict[item]['AssemblyScale']

            if mc.objExists( ref_ns + ':RIG' ):
                mc.xform( ref_ns + ':RIG', ws= True, t= Ass_pos, ro= Ass_rot, s= Ass_scl )

        # --- Get Root Grp
        ref_master_ctrl = None
        if mc.objExists( ref_ns +':Global_SRT' ):
            ref_master_ctrl = ref_ns +':Global_SRT'
        elif mc.objExists( ref_ns +':master_ctrl' ):
            ref_master_ctrl = ref_ns +':master_ctrl'

        if ref_master_ctrl:
            ref_master_ctrl_long= mc.ls( ref_master_ctrl, long= True )[0]
            # Get the reference Group root
            ref_to_parent = ref_master_ctrl_long.split('|')[1]

            # - Parent Reference to Root Grp
            ref_parent= toSwitch_dict[item]['Parent']

            if mc.objExists( ref_parent ):
                mc.parent( ref_to_parent, ref_parent )

        # --- Get Reference Controlers from SET
        list_Ctrls= list()
        if mc.objExists( ref_ns +':RIG_SET' ):
            list_Ctrls= mc.sets( ref_ns +':RIG_SET', q=True )

        ctrls_dict[item]= dict()
        ctrls_dict[item]['AssemblyNameSpace'] = toSwitch_dict[item]['AssemblyNameSpace']
        ctrls_dict[item]['Controls'] = list_Ctrls

    return ctrls_dict

#----------------------------------------------------------------------
def reconnect_animCurve( ctrls_dict ):
    '''
    Reconnect animation Curve to ctrls

    :param ctrls_dict: Contain NameSpace Assembly Ref, list of Reference Controls
    :type ctrls_dict: dictionnary

    :return: None
    '''
    for item in ctrls_dict.keys():
        assembly_NS = ctrls_dict[item]['AssemblyNameSpace']
        ctrls = ctrls_dict[item]['Controls']

        for ctrl in ctrls:
            key_name = 'TO_DELETE_'+ assembly_NS +'_0_'+ ctrl.split(':')[-1]
            key_name = key_name.replace(':', '_0_')

            animCurves= mc.ls( key_name+ '_Attr_*', type= 'animCurve' )

            for animCurve in animCurves:
                mc.copyKey( animCurve )
                mc.pasteKey( ctrl, at= animCurve.split('_Attr_')[-1] )

#----------------------------------------------------------------------
def set_firstKey( ctrls_dict ):
    '''
    Set First Key on all given controls

    :param ctrls_dict: Contain NameSpace Assembly Ref, list of Reference Controls
    :type ctrls_dict: dictionnary

    :return: None
    '''
    # --- Get start frame
    start_frame= mc.playbackOptions(q=True, min=True)

    for item in ctrls_dict.keys():
        assembly_NS = ctrls_dict[item]['AssemblyNameSpace']
        ctrls = ctrls_dict[item]['Controls']

        # Filter only Character and Props
        if assembly_NS.startswith('CH_' ) or assembly_NS.startswith('PR_' ):
            mc.setKeyframe( ctrls, time= start_frame )

#----------------------------------------------------------------------
def extraClean():
    '''
    do an extra Clean on current scene

    :return: None
    '''
    # - Check Camera NameSpace
    if mc.objExists( 'CM_ROOT' ):
        # - Get CM_ROOT children
        children= mc.listRelatives( 'CM_ROOT', children= True )

        for child in children:
            # Run only on Camera Ref
            if mc.objExists( child +'.cube_type' ):
                if mc.getAttr( child +'.cube_type' ) == 'CM':
                    # Get current nameSpace
                    nameSpace_cam= child.split(':')[0]
                    part= nameSpace_cam.split('_')
                    # Check the nameSpace start
                    if not part[0] == ('CM'):
                        # reBuild the right nameSpace
                        newNameSpace = 'CM'
                        for i in range( 1, len(part)):
                            newNameSpace += '_' + part[i]

                        # - Rename Camera nameSpace
                        mc.namespace( rename= [nameSpace_cam, newNameSpace] )
                        logMsg_CM = '+ Camera nameSpace renamed'
                    else:
                        logMsg_CM = '. Camera nameSpace was ok'

                    print logMsg_CM

    # - Remove Cam Animatique if exist
    logMsg_GD = '. Animatique Camera already remove'
    if mc.objExists( 'GD_ROOT' ):
        # - Get root Grp
        root_group = mc.listRelatives( 'GD_ROOT', p=True )
        if root_group:
            root_group= root_group[0]
            root_group_split=  root_group.split('_')
            if len(root_group_split) == 3:
                animatique_cam = mc.ls( 'cam_animatique_'+ root_group_split[0]+ '_' +root_group_split[2] + '*' ) or list()
                if animatique_cam:
                    for item in animatique_cam:
                        if mc.objExists( item ):
                            if mc.objectType( item ) == 'camera':
                                camera_to_delete = mc.listRelatives( item, p=True, fullPath= True )[0]
                                if root_group in camera_to_delete and 'GD_ROOT' in camera_to_delete:
                                    mc.delete( camera_to_delete )
                                    logMsg_GD = '+ Animatique Camera remove'

    print logMsg_GD
