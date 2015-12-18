#----------------------------------------------------------------------
# functions animation
# Author : felixlechA.com | f.rault
# Date   : Janury 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc

#----------------------------------------------------------------------
def bake_Objects( in_Obj_list, time= None, mergeAnim= False ):
    '''
    Bake given objects frame by frame in the scence current time range by default.

    :param in_Obj_list: List of objects name to bake
    :type in_Obj_list: list

    :param time: Define the time range
    :type time: (int, int)

    :param mergeAnim: If True merge Anim Layer
    :type mergeAnim: boolean
    '''

    # ---  filter list to bake
    l_obj = list(set( in_Obj_list )-set([None]))

    # --- Get current time
    i_time = mc.currentTime( q=True )

    # get time range
    if not time:
        time = (mc.playbackOptions(q=True, min=True), mc.playbackOptions(q=True, max=True))

    # Suspend refreshing
    mc.refresh( su=True )

    # --- Merge anim Layer
    if mergeAnim :
        # Get anim Layer
        all_layers = mc.ls(type = 'animLayer') or list()
        if len(all_layers) > 1:
            print '--> MERGE ANIM LAYER : ' + str( all_layers )
            mergeAnimLayers(items=all_layers)

    # Do Bake
    mc.bakeResults( l_obj, t=time, sampleBy=1 ,simulation=True , disableImplicitControl=True, preserveOutsideKeys=False, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation= True, controlPoints=False,shape=True)

    # Resume refreshing
    mc.refresh( su=False )

    # --- Set time at previous current time
    mc.currentTime( i_time )

#----------------------------------------------------------------------
def unbake_Objects( in_Obj_list ):
    '''
    Remove anim key on given objects

    :param in_Obj_list: List of objects name to unbake
    :type in_Obj_list: list
    '''
    # --- Get anim curve
    l_anim_curve = mc.listConnections( in_Obj_list, s= True, d= False, type ='animCurve' )
    if l_anim_curve:
        mc.delete( l_anim_curve )

#----------------------------------------------------------------------
def check_AnimKeys_inSet( inSet, remove_cstr= False ):
    '''
    Check if the objs in the inSET are animated or just posed

    :param inSet: Define the name of the SET to analyse
    :type inSet: string

    :return: True or False string who define if the inSET obj are animated or just posed
    :rtype: boolean
    '''
    # --- Get Controlers from SET
    if mc.objExists( inSet ):
        list_Ctrls= mc.sets( inSet, q=True )
    else:
        return False

    # --- Get start frame
    start_frame= mc.playbackOptions(q=True, min=True)

    # --- Check if key exist for Placement or for Anim
    animDelta= 0
    for ctrl in list_Ctrls:
        # --- Remove Cstr on Ctrl
        if remove_cstr == True:
            # - Create a list of Cstr to remove
            cstr_node = []

            # - Get ChannelBox Attributes
            attributes_chBox = mc.listAttr( ctrl, k=True ) or list()

            for attr in attributes_chBox:
                # - Pass Attr if not in channelBox
                if not attr in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']:
                    continue

                input = mc.listConnections( ctrl +'.' + attr, s=True, d=False )

                if input:
                    # - Check input node is a Cstr
                    if not mc.objectType( input[0] ) in ['pointConstraint', 'aimConstraint', 'orientConstraint', 'parentConstraint','scaleConstraint']:
                        continue

                    # - Add cstr if isn't already in
                    if not input[0] in cstr_node:
                        cstr_node.append( input[0] )

            # - Remove Constrain
            if cstr_node:
                mc.delete( cstr_node )

        # --- If no key exist on Ctrl
        if not mc.keyframe(ctrl, query=True, valueChange=True, timeChange=True):
            # - Set ket at the start frame
            mc.setKeyframe(ctrl, time= start_frame )

        # --- Get first and last key and check if we have many keys or only one
        first_key = mc.findKeyframe(ctrl, which='first')
        last_key = mc.findKeyframe(ctrl, which='last')

        # !!! - Check if keys have same value or not

        # --- Calculate delta inbetween keys to define if we have many keys
        animDelta += last_key - first_key

    if not animDelta == 0:
        return True
    else:
        return False
