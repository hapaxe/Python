#----------------------------------------------------------------------
# functions connection
# Author : felixlechA.com | f.rault
# Date   : Janury 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc

#----------------------------------------------------------------------
def get_MessageConnection_Input( inObj, inAttr ):
    '''
    Return a string of the input object connected to a connection message,
    who have message attribut name as inAttr

    :param inObj: the object name
    :type inObj: string

    :param inAttr : the attribut name
    :type inAttr : string

    :return : an object name
    :rtype : string
    '''
    # Get the attribute type
    if mc.objExists( inObj +'.' + inAttr ):
        attrType = mc.getAttr( inObj +'.' + inAttr, type=True )
    else :
        return None

    # message attribute
    if attrType == 'message':
        l_Input = mc.listConnections( inObj +'.' + inAttr, s=True, d=False )
        if l_Input:
            return l_Input[0]
        else:
            return None

#----------------------------------------------------------------------
def get_MessageConnection_Ouput( inObj, inAttr ):
    '''
    Return a list of the output objects connected to a connection message,
    who have message attribut name as inAttr

    :param inObj: the object name
    :type inObj: string

    :param inAttr : the attribut name
    :type inAttr: string

    :return : a list of objects name
    :rtype : list
    '''
    l_connection = mc.listConnections( inObj + '.message', s=False, d=True, p=True) or list()

    l_Output = []
    for s_connection in l_connection:
        if s_connection.split('.')[-1] == inAttr:
            l_Output.append( s_connection.split('.')[0] )

    return l_Output

#----------------------------------------------------------------------
def get_node_connection( in_obj, in_attr, in_way ):
    '''
    For a given parameter on an object return the node name and shape name of the other side of the connection

    :param inObj: the object name
    :type inObj: string
    :param inAttr: the attribut name
    :type inAttr: string
    :param inWay: Define the way of connection 'in' / 'out'
    :type inWay: string
    :return: A list of string [0] was the node name [1] was the shape node name
    :rtype: list
    '''
    if in_way == 'in':
        s_source = True
        s_destination = False
    elif in_way == 'out':
        s_source = False
        s_destination = True
    else:
        return

    s_node = mc.listConnections( in_obj + '.' + in_attr, s=s_source, d=s_destination, p=False, scn=True)[0] or ''
    s_node_shape = mc.listConnections( in_obj + '.' + in_attr, s=s_source, d=s_destination, p=True, scn=True)[0].split('.')[0] or ''

    return [ s_node, s_node_shape ]

#----------------------------------------------------------------------
def connect_Attribute( source, target, attribute= ['translate', 'rotate']):
    '''
    Connect two object Attribut by Attibute.
    by default connect Translate and Rotate

    :param source: the name of the source object
    :type source: string
    :param target: the name of the target object
    :type target: string
    :param attribute: List of attibutes to connect
    :type attribute: list
    :return:
    '''
    if not source or not target:
        return

    # - Replace translate by translateX / Y / Z
    if 'translate' in attribute:
        attribute.remove('translate')
        attribute.extend( ['translateX', 'translateY', 'translateZ'] )
    # - Replace roate by rotateX / Y / Z
    if 'rotate' in attribute:
        attribute.remove('rotate')
        attribute.extend( ['rotateX', 'rotateY', 'rotateZ'] )
    # - Replace scale by scaleX / Y / Z
    if 'scale' in attribute:
        attribute.remove('scale')
        attribute.extend( ['scaleX', 'scaleY', 'scaleZ'] )

    # --- Loop on Attributes
    for attr in attribute:
        # - Check if Attributes exist on the two objects
        if not mc.objExists( source + '.' + attr ) or not mc.objExists( target + '.' + attr ):
            continue
        # - Check if connection is already done
        if not mc.isConnected( source + '.' + attr, target + '.' + attr ):
            # - Do connection
            mc.connectAttr( source + '.' + attr, target + '.' + attr, force= True )