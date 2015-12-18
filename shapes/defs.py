#----------------------------------------------------------------------
# shapes defs
# Author : felixlechA.com | f.rault
# Date   : April 2015
# Decription : shapes commun definitions
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint
import functions.file_info as file_info
import functions.selection as selection
import rigtool.defs as rigtool_defs

import os
import json

#----------------------------------------------------------------------
def get_curve_datas( in_obj ):
    '''
     Get the datas of a given nurbsCurve to have ability to recreate on the way

    :param in_obj: Object name
    :type in_obj: string

    :return: Datas of the given curve
    :rtype: dictionnary
    '''
    # --- Get the first shape of in_obj
    if not in_obj:
        viewPrint( msg= 'Select a nurbsCurve object to get this construction infos', mode= 1 )
        return
    shapes= selection.get_shapesType( in_obj= in_obj, type= 'nurbsCurve' )

    if len( shapes ) > 0:
        shape= shapes[0]
    else:
        viewPrint( msg= ' > The given object have not nurbsCurve shape to give datas', mode= 3 )
        return

    # --- Get degree
    degree = mc.getAttr( shape +'.degree' )
    spans = mc.getAttr( shape +'.spans' )
    form= mc.getAttr( shape +'.form')

    if form:
        per= True
    else:
        per= False

    # --- Get point
    point= list()
    for i in range( spans + degree ):
        if not form:
            point_position= mc.xform('%s.cv[%d]' %(shape, i), q=True, t=True, ws=True)
        else:
            point_position= mc.xform('%s.cv[%d]' %(shape, i%spans), q=True, t=True, ws=True)
        # - Add to point list
        point.append( point_position )

    # --- Get knot
    node_cureveInfo= mc.createNode( 'curveInfo')
    mc.connectAttr( shape + '.worldSpace[0]', node_cureveInfo + '.inputCurve', f=True )
    knot= mc.getAttr( node_cureveInfo +'.knots' )[0]
    mc.delete( node_cureveInfo )

    # --- Create a dictionnary to return datas
    datas= dict()

    if '|' in in_obj:
        in_obj= in_onj.split('|')[-1]
    datas['name']= in_obj
    datas['degree']= degree
    datas['point']= point
    datas['knot']= knot
    datas['per']= per

    return datas

#----------------------------------------------------------------------
def write_shape_jsonFile( in_dict, edit= False ):

    # - Get Datas
    name= in_dict['name']

    # --- Build file path
    path_shape= file_info.get_BasePath( add_directory= ['config', 'shapes'], add_file=  name +'.json'  )

    # --- Check if directory exist
    if not os.path.exists( os.path.dirname( path_shape ) ):
        os.makedirs( os.path.dirname( path_shape ) )

    # - Write File
    # - Create json file
    if not os.path.isfile( path_shape ):
        with open( path_shape, 'w+') as file_json :
            json.dump( in_dict, file_json, sort_keys= True, separators= ( ',', ':' ) )

    # - Edit json file
    if os.path.isfile( path_shape ) and edit== True:
        with open( path_shape, 'w+') as file_json :
            json.dump( in_dict, file_json, sort_keys= True, separators= ( ',', ':' ) )
    else:
        print name +' : not editable'

#----------------------------------------------------------------------
def delete_shape_jsonFile( in_name ):
    '''
    Delete a shape json file description

    :param in_name: The shape file name to remove, whitout .json
    :return: string

    :return: None
    '''
    # --- Build file path
    path_shape= file_info.get_BasePath( add_directory= ['config', 'shapes'], add_file=  in_name +'.json'  )

    # if file exist, Remove the shape json file
    if os.path.isfile( path_shape ):
        os.remove( path_shape )
        print in_name +' : removed'

#----------------------------------------------------------------------
def get_availlable_shapes():
    '''
    Get the list of availlable shapes.

    :return: List of shape name
    :rtype: list
    '''

    # --- Build file path
    path= file_info.get_BasePath( add_directory= ['config', 'shapes'] )

    # - Get shapes jason files
    shape_list= list()
    if os.path.exists( path ):
        for json_file in os.listdir( path ):
            if json_file.endswith('.json' ):
                shape_list.append( json_file.split('.')[0] )

    # - Sort Asc shape list
    return sorted( shape_list )

#----------------------------------------------------------------------
def get_shape_datas_from_json( shape ):

    # --- Build file path
    path_shape= file_info.get_BasePath( add_directory= ['config', 'shapes'], add_file=  shape +'.json'  )

    if os.path.exists( path_shape ):
        with open( path_shape ) as json_file:
            return json.load( json_file )
    else:
        viewPrint( msg= shape +' is not availlable !', mode= 3 )
        return

#----------------------------------------------------------------------
def store_selected_ctrl_curve( edit= True ):
    '''
    Store selected nurbsCurve creation datas in json file

    :param edit: Define if update exist shape or not
    :type edit: boolean

    :return: none
    '''
    ctrls= mc.ls( sl= True )

    for ctrl in ctrls:
        write_shape_jsonFile( get_curve_datas( in_obj= ctrl ), edit= edit )

#----------------------------------------------------------------------
def add_shape( in_obj, shape= 'circle', size= 1, orient= 'X', mirror= [1,1,1], middle_jnt= True ):
    '''
    '''
    # --- Get shape datas
    shape_dict= get_shape_datas_from_json( shape )
    name= shape_dict['name']
    degree= shape_dict['degree']
    point= shape_dict['point']
    knot= shape_dict['knot']
    per= shape_dict['per']

    # - Check if object is a Transform or a joint
    if not mc.nodeType( in_obj ) in ['transform', 'joint']:
        return

    # --- Build new Shape
    curve_shape = mc.curve( d= degree, p= point, k= knot, per= per )
    # - Get Shape
    shape_obj= mc.listRelatives( curve_shape, s=True )[0]
    # - Parent new shape
    mc.parent( shape_obj, in_obj, s=True, r=True )
    # - Rename Shape
    name= in_obj.split('|')[-1]
    shape_obj= mc.rename( shape_obj, name + 'Shape')
    # - Remove empty transform
    mc.delete( curve_shape )

    # ---  edit curve
    # - Orient
    if orient == 'X' :
        mc.rotate(0, 0, -90, shape_obj+ '.cv[*]', r=True)
    if orient == 'Y' :
        mc.rotate(0, -90, 0, shape_obj+ '.cv[*]', r=True)
    if orient == 'Z' :
        mc.rotate(90, 0, 0, shape_obj+ '.cv[*]', r=True)

    # - Mirror
    mc.scale( mirror[0], mirror[1], mirror[2], shape_obj+ '.cv[*]', r=True)

    # - Size
    mc.scale( size, size, size, shape_obj+ '.cv[*]', r=True)

    # - Joints Offset Position
    if mc.nodeType( in_obj )== 'joint' and middle_jnt== True:
        children= selection.get_jointHierarchy( in_obj )
        if not len(children) >= 2:
            return
        # - Calcul offset for joint
        offset= rigtool_defs.get_length_inbetween( obj1= children[0], obj2= children[1] )/ 2

        if orient == 'X' :
            mc.move( offset, 0, 0, shape_obj+ '.cv[*]', os=True, r= True)
        if orient == 'Y' :
            mc.move( 0, offset, 0, shape_obj+ '.cv[*]', os=True, r= True)
        if orient == 'Z' :
            mc.move( 0, 0, offset, shape_obj+ '.cv[*]', os=True, r= True)

    # - Clean order Shapes
    move_shape( in_obj= in_obj, mode= 'top' )

#----------------------------------------------------------------------
def move_shape( in_obj, mode, shapes= list() ):
    '''
    Reorder Shapes

    :param in_obj: Object shapes to reorder
    :type in_obj: string

    :param mode: Define the mode to reorder
    :type mode: string

    :param shapes: Shapes to reorder
    :type shapes: list

    :return: none
    '''
    # - Get shapes if not define
    if len( shapes )== 0:
        shapes= selection.get_shapesType( in_obj, type= 'nurbsCurve' )

    # - Reorder
    if mode== 'up':
        mc.reorder( shapes, r= -1 )
    elif mode== 'dw':
        mc.reorder( shapes, r= 1 )
    elif mode== 'top':
        mc.reorder( shapes, f= True )
    elif mode== 'btm':
        mc.reorder( shapes, b= True )