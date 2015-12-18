#----------------------------------------------------------------------
# functions selection
# Author : felixlechA.com | f.rault
# Date   : April 2015
# Ver    : 1.0
#----------------------------------------------------------------------

import maya.cmds as mc

#----------------------------------------------------------------------
def get_parent( in_obj ):
    '''
    Return the name of the direct parent

    :param in_obj : The object name whose return Parent name
    :type in_obj: string

    :return: the Parent object name
    :rtype: string
    '''
    # Get Parent
    parent_list = mc.listRelatives( in_obj, p=True, fullPath= True )

    if parent_list:
        parent_name = parent_list[0]
        return parent_name
    else:
        return None

#----------------------------------------------------------------------
def get_shapesType( in_obj, type= ['nurbsCurve'] ):
    '''
    Get the shapes of a given object

    :param in_obj : The object that give shapes
    :type in_obj: string

    :param type: Define the shape type to return
    :type type: list

    :return: A list of Shapes name
    :rtype: list
    '''
    # - Get All Shapes
    shape_list = mc.listRelatives( in_obj, s= True, fullPath= True )

    # - Filter shapes by type
    if shape_list:
        result= list()
        for shape in shape_list:
            if mc.nodeType( shape )in type:
                result.append( shape )
        return result
    else:
        return None

#----------------------------------------------------------------------
def get_jointHierarchy( in_joint ):
    '''
    Return a list of joints in Hierarchical order.
    Get all the child joints of a giving one

    :param in_joint: The name of the first joint
    :type in_joint: string

    :return: A list of Joint in Hierarchical order
    :rtype: list
    '''
    # Get children and load them in the lJnt list
    children_list = mc.listRelatives( in_joint, children=True, allDescendents=True, fullPath= True ) or list()
    children_list.reverse()

    child_joint_list = []
    for child in children_list:
        if mc.nodeType(child) == 'joint':
            child_joint_list.append( child )

    # Create a list to return
    result = list()
    if mc.nodeType(in_joint) == 'joint':
        result.append( in_joint )
    result.extend( child_joint_list )

    return result

#----------------------------------------------------------------------
def sort_objectByHierarchy( in_obj, order= 'dsc' ):
    '''
    Sort object_list object by place in hierarchy

    :param in_obj: List of object as longName
    :type in_obj: string

    order: 'dsc' or 'asc'
    '''
    # --- Sort object by hierarchy level
    # - Create dictionnary
    sort_dict= dict()

    upper_rank= 0
    for item in in_obj:
        # - Split longName
        rank= len(item.split('|'))

        # - Update upper_rank
        if rank > upper_rank:
            upper_rank= rank

        # - Create rank key if needs
        if not rank in sort_dict.keys():
            sort_dict[rank]= list()
        # - Add iterm to key
        sort_dict[rank].append( item )

    # --- Build a return list object by hierarchy
    result= list()
    # - Define how sort object
    # asc
    start= 0
    end= upper_rank + 1
    side= 1

    if order == 'dsc':
        start= upper_rank
        end= -1
        side= -1

    # - Build list
    for i in range( start, end, side):
        if i in sort_dict.keys():
            result.extend( sort_dict[i] )

    return result

#----------------------------------------------------------------------
def convert_face_to_edges( face ):
    '''
    For a given face return two uncontinus edges

    :param face: The full face name
    :type face: string
    '''
    #--- convert face to edges
    edges = mc.ls( mc.polyListComponentConversion( face, ff=True, te=True ), fl=True )

    #--- For 3edges Faces return the 2 first edges
    if len(edges) == 3:
        return [edges[0], edges[1]]

    #--- Create a vertex set with the first edge
    setEdgeA = set(mc.ls(mc.polyListComponentConversion(edges[0], fe=True, tv=True), fl=True))

    #--- Search an edge without commun vertex
    for i in range( 1, len(edges) ):
        setEdgeB = set(mc.ls(mc.polyListComponentConversion(edges[i], fe=True, tv=True), fl=True))
        if not setEdgeA & setEdgeB:
            #--- return uncontinus edges
            return [edges[0], edges[i]]