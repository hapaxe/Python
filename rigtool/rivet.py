#----------------------------------------------------------------------
# rigtool rivet
# Author : felixlechA.com | f.rault
# Date   : April 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
import re
from functions.general import viewPrint
import functions.selection as selection

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Rivet():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'rivetTool_Window'
        self.tool_title= 'rivet settings'
        self.widgets = {} # Dictionnary who store the tool's UI

        # - Build window
        self.UI()

    #----------------------------------------------------------------------
    def UI( self, *args ):
        '''
        The UI
        '''
        # --- Check existing Windows
        if mc.window( self.tool_name, exists=True ):
            mc.deleteUI( self.tool_name, window=True )

        # --- Create window
        self.widgets['win'] = mc.window( self.tool_name, title= self.tool_title, w= 150, sizeable= False, toolbox= True )

        self.widgets['win_col'] = mc.columnLayout( adj= True )
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.00, 0.36, 0.047], l='', cll= False )

        self.widgets['extra_name'] = mc.textFieldGrp( l=' Extra name : ', cl2= [ 'left', 'right' ], cw2= [ 65, 75], text='', annotation= 'Define rivet extra name')
        self.widgets['orient'] = mc.iconTextCheckBox( style='iconAndTextHorizontal', image1='rigTools_rivet_position.png', selectionImage= 'rigTools_rivet_oriented.png', label='Surface oriented', value= True, annotation= 'Define if rivet follow surface orientation' )

        self.widgets['win_bt_launch'] = mc.button(l='Create rivet', height= 30, c= self.launch )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):

        extra_name = mc.textFieldGrp( self.widgets['extra_name'], q=True, tx=True )
        orient = mc.iconTextCheckBox( self.widgets['orient'], q=True, v=True )

        create( extra_name= extra_name, orient= orient )

#----------------------------------------------------------------------
def create( extra_name= '', orient= True ):
    '''
    Create rivets on each selected faces or inbetween two given edges

    :param extra_name: Define the base name
    :type extra_name: string

    :param orient: Define if rivet follow surface orientation
    :type orient: boolean

    :return: List of created rivet
    :rtype: list
    '''

    # --- Get subComponent Selection
    sel = mc.ls( sl=True )

    if not sel:
        viewPrint( msg= 'Select Faces or 2 Edges to build rivet', mode= 1 )
        return

    # --- keep only edges and faces
    edges = mc.filterExpand( sel, sm=32) or list()
    faces = mc.filterExpand( sel, sm=34) or list()

    # --- Build an edges list
    edge_list= list()
    if len(edges) == 2 :
        edge_list.extend( edges )
    elif faces :
        for face in faces:
            # - Get edges for each selected faces
            edges = selection.convert_face_to_edges( face )
            edge_list.extend( edges )
    else:
        viewPrint( msg= 'Select Faces or 2 Edges to build rivet', mode= 1 )
        return

    # --- Launch Build
    result= list()
    for i in range( 0, len(edge_list), 2):
        result.append( build_rivet( edgeA= edge_list[i], edgeB= edge_list[i+1], extra_name= extra_name, orient= orient) )

    return result

#----------------------------------------------------------------------
def create_loft_surface( edgeA, edgeB, name ):
    '''
    Create a loft surface inbetween the two given edges

    :param edgeA: The full edge name
    :type edgeA: string

    :param edgeB: The full edge name
    :type edgeB: string

    :param name: Define the rivet name
    :type name: string

    :return: The loft surface name
    :rtype: string
    '''
    # ---  init
    objA = edgeA.split('.')[0]
    objB = edgeB.split('.')[0]

    # ---  Create nodes
    nodes= list()
    node_edgeA= mc.createNode('curveFromMeshEdge', n= '%s_%s_Crv1' %(name, objA))
    nodes.append( node_edgeA )
    node_edgeB= mc.createNode('curveFromMeshEdge', n= '%s_%s_Crv2' %(name, objB))
    nodes.append( node_edgeB )
    node_loft= mc.createNode('loft', n= name + '_loft' )
    nodes.append( node_loft )

    # --- Set Nodes Connections
    # - Crv 1
    mc.setAttr( node_edgeA + '.ei[0]', int(re.findall('\d+', edgeA)[-1]) )
    mc.connectAttr( objA + '.w', node_edgeA + '.im', f= True )

    # - Crv 2
    mc.setAttr( node_edgeB + '.ei[0]', int(re.findall('\d+', edgeB)[-1]) )
    mc.connectAttr( objB + '.w', node_edgeB + '.im', f= True )

    # - Loft
    mc.setAttr( node_loft + '.ic', size= 2 )
    mc.setAttr( node_loft + '.u', True )
    mc.setAttr( node_loft + '.rsn', True )
    mc.connectAttr( node_edgeA + '.oc', node_loft + '.ic[0]', f=True )
    mc.connectAttr( node_edgeB + '.oc', node_loft + '.ic[1]', f=True )

    # - Historical intereset
    for node in nodes :
        mc.setAttr( node + '.ihi', 0)

    return node_loft

#----------------------------------------------------------------------
def attach_obj_on_surface( obj, surface, U= 0.5, V= 0.5, orient= True ):
    '''
    Attach an object to a given surface using pointOnSurfaceInfo

    :param obj: The object name to attach to the given surface
    :type obj: string

    :param surface: The surface who attach object
    :type surface: string

    :param U: The default U value of the pointOnSurfaceInfo
    :type U: float

    :param V: The default V value of the pointOnSurfaceInfo
    :type V: float

    :return: The pointOnSurfaceInfo node name
    :rtype: string
    '''
    nodes= list()

    # - Point on surface info
    node_pointOnSurfaceInfo= mc.createNode('pointOnSurfaceInfo', n= obj + '_pointOnSurfaceInfo')
    nodes.append( node_pointOnSurfaceInfo )
    mc.setAttr( node_pointOnSurfaceInfo + '.turnOnPercentage', True)
    mc.setAttr( node_pointOnSurfaceInfo + '.parameterU', U)
    mc.setAttr( node_pointOnSurfaceInfo + '.parameterV', V)

    # - Connect surface to pointOnSurfaceInfo
    if mc.nodeType( surface ) == 'loft':
        mc.connectAttr( surface + '.os', node_pointOnSurfaceInfo + '.is', f=True)
    else:
        surface= selection.get_shapesType( in_obj= surface, type= 'nurbsCurve' )[0]
        mc.connectAttr( surface + '.worldSpace[0]', node_pointOnSurfaceInfo + '.is', f=True)

    # --- Drive obj Translate
    mc.connectAttr( node_pointOnSurfaceInfo + '.positionX', obj + '.translateX' )
    mc.connectAttr( node_pointOnSurfaceInfo + '.positionY', obj + '.translateY' )
    mc.connectAttr( node_pointOnSurfaceInfo + '.positionZ', obj + '.translateZ' )


    if orient:
        # - Create node
        node_rotateHelper= mc.createNode('rotateHelper', n= obj + '_rotateHelper')
        nodes.append( node_rotateHelper )
        node_decomposeMatrix= mc.createNode('decomposeMatrix', n= obj + '_decomposeMatrix')
        nodes.append( node_decomposeMatrix )

        # - Get Rotate
        mc.connectAttr( node_pointOnSurfaceInfo + '.normal', node_rotateHelper + '.up' )
        mc.connectAttr( node_pointOnSurfaceInfo + '.tangentV', node_rotateHelper + '.forward' )
        mc.connectAttr( node_rotateHelper + '.rotateMatrix', node_decomposeMatrix + '.inputMatrix' )

        mc.connectAttr( node_decomposeMatrix + '.outputRotateX', obj + '.rotateX' )
        mc.connectAttr( node_decomposeMatrix + '.outputRotateY', obj + '.rotateY' )
        mc.connectAttr( node_decomposeMatrix + '.outputRotateZ', obj + '.rotateZ' )

    # --- Historical intereset
    for node in nodes :
        mc.setAttr( node + '.ihi', 0)

    return node_pointOnSurfaceInfo

#----------------------------------------------------------------------
def build_rivet( edgeA, edgeB, extra_name, orient= True ):
    '''
    Build a rivet between two given edges
    Edges can be from different mesh

    :param edgeA: The full edge name
    :type edgeA: string

    :param edgeB: The full edge name
    :type edgeB: string

    :param extra_name: Define the base name
    :type extra_name: string

    :param orient: Define if rivet follow surface orientation
    :type orient: boolean

    :return: The created rivet name
    :rtype: string
    '''
        # - Build name
    name = 'rivet'
    if extra_name:
        name= extra_name +'_'+ name

    # --- Create Locator Rivet
    rivet = mc.spaceLocator( n=name )[0]
    # - Add posU and posV attributes
    mc.addAttr( rivet, ln='posU', at='float', min=.0, max=1.0, dv=.5, k=True )
    mc.addAttr( rivet, ln='posV', at='float', min=.0, max=1.0, dv=.5, k=True )

    # - Create Loft surface
    loft= create_loft_surface( name= rivet, edgeA= edgeA, edgeB= edgeB )

    # - Attach rivet to loft
    node_pointOnSurfaceInfo= attach_obj_on_surface( obj= rivet, surface= loft, U= 0.5, V= 0.5, orient= orient )

    # - Drive U and V parameter of the pointOnSurfaceInfo
    mc.connectAttr( rivet + '.posU', node_pointOnSurfaceInfo + '.parameterU', f=True)
    mc.connectAttr( rivet + '.posV', node_pointOnSurfaceInfo + '.parameterV', f=True)

    # --- Historical intereset
    mc.setAttr( rivet + 'Shape.ihi', 0)

    # --- Clean
    for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility'] :
        mc.setAttr( rivet + '.'+ attr, k= False )

    for axis in ['X', 'Y', 'Z'] :
        mc.setAttr( rivet +'Shape.localPosition'+ axis, k= False, cb= False)

    return rivet
