#----------------------------------------------------------------------
# sceneCheck hotFix
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functions import animation, connection, general
reload( connection )

def update_dynamic_system():
    '''
    Update Dynamic System to fix some wird comportements
    - ON_OFF parameter will be unKeyable (non animation on it)
    - pairBlend rotInterpolation will be set to Quaternion to fix bakesd problems

    import sceneCheck.hotFix as hotFix
    reload( hotFix )
    hotFix.update_dynamic_system()

    :return: none
    '''
    # --- Get all dyn sys
    dynamic_system = mc.ls( type= 'hairSystem' )
    
    # - keep only valid Dyn System
    for item in dynamic_system:
        if not mc.objExists( item+ '.dynSystem' ) and not mc.objExists( item+ '.globalCtrl' ):
            dynamic_system.remove( item  )
    
    # - Get the Global_Ctrl
    global_ctrl_list= list()
    for item in dynamic_system:
        global_ctrl_list.append( connection.get_MessageConnection_Input( item, 'globalCtrl' ) )
    
    # - Get the dyn Joints
    dyn_joints_list = list()
    for item in global_ctrl_list:
        joint_list = connection.get_MessageConnection_Ouput( inObj= item, inAttr= 'dyn_jointDyn' )
        if joint_list:
            dyn_joints_list.extend( joint_list )
    
    # - Get associate pairBlend
    pairBlend_list= list()
    for item in dyn_joints_list:    
        node= connection.get_node_connection( in_obj= item, in_attr= 'rotateX', in_way= 'out' )[0]

        if node:
            if mc.nodeType( node ) == 'pairBlend':
                pairBlend_list.append( node )
    
    
    # --- Update System
    print '> Update Dynamic System :'
    # - Set ON_OFF attribut no Keyable
    nbr_fix= 0
    for item in global_ctrl_list:
        if not 'on_off' in mc.listAttr( item, cb= True ):
            mc.setAttr( item+ '.on_off', keyable= False ) # Be not keyable
            mc.setAttr( item+ '.on_off', channelBox= True ) # Display in channelBox
            nbr_fix += 1

    if nbr_fix == 0:
        print '+ Already done > Global_Ctrl dyn on_off set to unkayable'
    else:
        print str( nbr_fix )+ ' : Global_Ctrl dyn on_off parameter are now unkeyable'
    
    # - Set the Rot_Interpolation of pairBlend to Quaternion
    nbr_fix= 0
    for item in pairBlend_list:
        if not mc.getAttr( item+ '.rotInterpolation' ) == 1:
            mc.setAttr( item+ '.rotInterpolation', 1)
            nbr_fix += 1

    if nbr_fix == 0:
        print '+ Already done > pairBlend rotInterpoation are in Quaternion'
    else:
        print str(len( pairBlend_list ))+ ' : pairBlend rotInterpoation are in now Quaternion'

#----------------------------------------------------------------------
def fix_joint_scale_compensation():
    '''
    Fix the joint scale compensation
    replace scale inverseScale connection xyz by direct connection

    :return: none
    '''
    sel= mc.ls( type= 'joint' )

    slog= 'Fix joint scale compensation :'
    for item in sel:
        all_connection= mc.listConnections( item, source= True, destination= False, plugs= True, connections= True ) or list()

        if item + '.inverseScaleX' in all_connection and item + '.inverseScaleY' in all_connection and item + '.inverseScaleZ' in all_connection:
            plug_list= list( set( mc.listConnections( item, source= True, destination= False, plugs= False, connections= False )))

            for driver in plug_list:
                if driver + '.scaleX' in all_connection and driver + '.scaleY' in all_connection and driver + '.scaleZ' in all_connection:
                    mc.disconnectAttr( driver + '.scaleX', item + '.inverseScaleX' )
                    mc.disconnectAttr( driver + '.scaleY', item + '.inverseScaleY' )
                    mc.disconnectAttr( driver + '.scaleZ', item + '.inverseScaleZ' )

                    mc.connectAttr( driver + '.scale', item + '.inverseScale' )
                    slog += '\n . '+ item
                    break

    print slog

#----------------------------------------------------------------------
def clean_GeometryName_toExport( ):
    '''
    Assure Geometry name are unique, resolve noUnique name
    Assure Shape to Export name is Geo + Shape, resolve by rename intermediates if need

    :return: none
    '''
    print '\nGEOMETRY and SHAPE are OK ?'

    # - Get All Geo to Export
    if not mc.objExists( 'GEOMETRY_SET' ):
        print '!!! no GEOMETRY_SET to check found\n'
        return

    geometry= mc.sets( 'GEOMETRY_SET', q=True )
    s_log= ''

    for geo in geometry:
        # --- Fix Geo
        if '|' in geo:
            # - Get twin geo Name
            twin= mc.ls( geo.split('|')[-1] )
            for item in twin:
                # - Rename evil twin
                if not item == geo:
                    mc.rename( item, item.replace('|', '_') )

            # - replace geo longName by this shortName
            if len( mc.ls( geo.split('|')[-1] )) == 1:
                geo= geo.split('|')[-1]
                s_log+= '+ Fix geo : '+ geo +'\n'
            else:
                s_log+= '!!! error to rename ' + geo +'\n'
                continue

        # --- Fix Shape Name
        # - Get the Shape to export
        export_shape= mc.listRelatives( geo, s= True, noIntermediate= True )[0]

        # - Check Shape have the good name
        if not export_shape == geo +'Shape':
            # - Get intermediate Shape
            shapes = mc.listRelatives( geo, s=True, pa=True ) or list()

            # - Fix intermediate Shape name
            for shape in shapes:
                if mc.objExists(shape +'.intermediateObject') and not shape == export_shape:
                    mc.rename( shape, geo + 'Shape_Inter' )

            # - Rename to export Shape
            if not mc.objExists( geo + 'Shape' ):
                mc.rename( export_shape, geo + 'Shape' )
                s_log+= '+ Fix Shape : '+ geo + 'Shape\n'
            else:
                s_log+= '!!! error to rename ' + export_shape +'\n'

    # - Print Log
    if s_log == '':
        s_log= '+ YES !'
    print s_log