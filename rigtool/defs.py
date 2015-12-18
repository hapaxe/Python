#----------------------------------------------------------------------
# rigtool defs
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from math import sqrt
import functions.selection as selection

#----------------------------------------------------------------------
def get_transform( in_obj, ws= True ):
    '''
    Get the transform of the input object and return this World Space Transforms

    :param in_obj: the object name whose return Transform info
    :type in_obj: string

    :return: The World Space Transform of given object
    :rtype: dictionnary
    '''

    dTrans = dict()

    if ws:
        dTrans['pos'] = mc.xform( in_obj, q=True, ws=True, t=True )
        dTrans['rot'] = mc.xform( in_obj, q=True, ws=True, ro=True )
        dTrans['scl'] = mc.xform( in_obj, q=True, s=True, r=True )
    else:
        dTrans['pos'] = mc.xform( in_obj, q=True, ws=False, t=True )
        dTrans['rot'] = mc.xform( in_obj, q=True, ws=False, ro=True )
        dTrans['scl'] = mc.xform( in_obj, q=True, s=True, r=True )

    return dTrans

#----------------------------------------------------------------------
def clean_jointOrient( in_joint, mode= 'transform' ):
    '''
    Clean the joint orient for the in Joint

    :param in_joint: the name of the joint
    :type in_joint: string

    :param mode: define where stack the rotation 'transform' or 'jointOrient'
    :type mode: string

    :return: none
    '''
    # - Check if joint was the last of the chain
    joint_x= False
    jnt_list= selection.get_jointHierarchy( in_joint )
    if len(jnt_list) == 1 and jnt_list[0] == in_joint:
        joint_x= True

    for Axis in ['X', 'Y', 'Z']:
        # - Get the rotation and rotation joint Orient
        if joint_x:
            rot = 0
            rot_jOrient = 0
        else:
            rot = mc.getAttr( in_joint+ '.rotate'+ Axis )
            rot_jOrient = mc.getAttr( in_joint+ '.jointOrient'+ Axis )

        # - Clean
        if mode == 'transform':
            mc.setAttr( in_joint+ '.jointOrient' + Axis, 0 )
            mc.setAttr( in_joint+ '.rotate' + Axis, rot + rot_jOrient )
        elif mode == 'jointOrient':
            mc.setAttr( in_joint+ '.jointOrient' + Axis, rot + rot_jOrient )
            mc.setAttr( in_joint+ '.rotate' + Axis, 0 )

#----------------------------------------------------------------------
def get_length_inbetween( obj1, obj2 ):
    '''
    Calculate the distance inbetween 2 objects

    :param obj1: the first object
    :type obj1: string

    :param obj2: the second object
    :type obj2: string

    :return: the length inbetween the two in objects
    :rtype: float
    '''
    if not mc.objExists(obj1) and not mc.objExists(obj2):
        return

    # Get the world space position
    t1= mc.xform( obj1, q=True, ws=True, t=True )
    t2= mc.xform( obj2, q=True, ws=True, t=True )

    # return the length
    return sqrt( (t1[0]-t2[0])**2 + (t1[1]-t2[1])**2 + (t1[2]-t2[2])**2 )

#----------------------------------------------------------------------
def create_group( name=None, parent=None, ws=False, lPos=[0,0,0], lRot=[0,0,0], lScl=[1,1,1] ):
    '''
    Create a Group

    :param name: The Joint Name
    :type name: string

    :param parent: The Parent name
    :type parent: string

    :param lPos: A three input list define the Translation
    :type lPos:  list

    :param lRot: A three input list define the Rotation
    :type lRot:  list

    :param lScl: A three input list define the Scale
    :type lScl:  list

    :return: the Group name
    :rtype: string
    '''
    # - Create Group
    group = mc.group( em=True )
    # - Place in WS
    mc.xform( group, ws=True, t=lPos, ro=lRot, s=lScl )
    # - Parent
    if parent:
        mc.parent( group, parent )
    # - Rename
    if name:
        group= mc.rename(group, name )

    return group
