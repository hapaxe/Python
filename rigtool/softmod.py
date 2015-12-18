#----------------------------------------------------------------------
# rigtool softmod
# Author : felixlechA.com | f.rault
# Date   : April 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint
import functions.selection as selection
import shapes.defs as shapes_defs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SoftMod():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'softModTool_Window'
        self.tool_title= 'softMod settings'
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
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.0, 0.333, 0.37], l='', cll= False )

        self.widgets['extra_name'] = mc.textFieldGrp( l='Extra name : ', cl2= [ 'left', 'right' ], cw2= [ 65, 75], text='', annotation= 'Define softMod extra name')
        self.widgets['multi_deformer'] = mc.iconTextCheckBox( style='iconAndTextHorizontal', image1='rigTools_softMod_one.png', selectionImage= 'rigTools_softMod_multi.png', label='Multi deformer', value= False, annotation= 'Define if create one for all, or one for each' )

        self.widgets['win_bt_launch'] = mc.button(l='Create softMod', height= 30, c= self.launch )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):

        extra_name = mc.textFieldGrp( self.widgets['extra_name'], q=True, tx=True )
        multi_deformer = mc.iconTextCheckBox( self.widgets['multi_deformer'], q=True, v=True )

        create( extra_name= extra_name, multi_deformer= multi_deformer )

#----------------------------------------------------------------------
def create( extra_name= '', multi_deformer= False ):
    '''
    Create softMod deformer on selected object

    :param extra_name: Define base name
    :type extra_name: string

    :param multi_deformer: Define if create one for all, or one for each
    :type multi_deformer: boolean

    :return: List of created softMod deformer
    :rtype: list
    '''
    # --- Get current selection
    sel= mc.ls( sl = True ) or list()

    if not sel:
        viewPrint( msg= 'Select Geometry to add softMod deformer', mode= 1 )
        return

    # - Filter sel to keep only valid objects
    obj_to_deform= list()
    for item in sel:
        if selection.get_shapesType( item, type= ['mesh', 'nurbsSurface', 'nurbsCurve', 'lattice'] ):
            obj_to_deform.append( item )

    # - Skip deformer creation if no object valid found
    if not obj_to_deform:
        viewPrint( msg= 'No valid object found in selection', mode= 1 )
        return

    # --- Launch Build
    result= list()
    if not multi_deformer:
        result.append( build_softmod( in_obj= obj_to_deform, extra_name= extra_name ))
    else:
        for item in obj_to_deform:
            result.append( build_softmod( in_obj= item, extra_name= extra_name, multi_deformer= True ))

    return result

#----------------------------------------------------------------------
def build_softmod( in_obj, extra_name, multi_deformer= False ):
    '''

    :param in_obj: List of object to deform
    :type in_obj: list

    :param extra_name:
    :type extra_name: string

    :param multi_deformer: Define if based name, or named with in_obj name
    :type multi_deformer: boolean

    :return: Deformer name
    :rtype: string
    '''
    # - Build name
    name = 'SoftMod'
    if multi_deformer:
        name= in_obj +'_'+ name
    if extra_name:
        name= extra_name +'_'+ name

    # --- Create SoftMod
    tmp = mc.softMod( in_obj, n= name )
    deform = tmp[0]
    handle = tmp[1]

    # - Add an orig
    sOrig = mc.group(em=True, n= deform +'_orig' )

    # - Add a root
    sRoot = mc.group(em=True, p=sOrig, n= deform +'_root' )
    shapes_defs.add_shape( sRoot, shape= 'circle_wired', size= 0.4, orient= 'X', mirror= [1,1,1], middle_jnt= True )

    # - Add ctrl
    ctrl = mc.group(em=True, p=sRoot, n= deform +'_ctrl' )
    shapes_defs.add_shape( ctrl, shape= 'circle_low', size= 0.3, orient= 'X', mirror= [1,1,1], middle_jnt= True )

    # - Change softMod handle
    mc.softMod( deform, e=True, wn=(ctrl, ctrl))

    # --- Add attributes
    # ---
    mc.addAttr( ctrl, ln='extra', at='enum', en='---')
    mc.setAttr( ctrl +'.extra', k=False, cb=True)

    # - falloffMode
    mc.addAttr( ctrl, ln='mode', at='enum', en='Volume:Surface')
    mc.setAttr( ctrl +'.mode', k=False, cb=True)
    mc.connectAttr( ctrl +'.mode', deform +'.falloffMode', f=True)

    # - falloffRadius
    mc.addAttr( ctrl, ln='smRadius', at='float', min=0.0, dv=.5)
    mc.setAttr( ctrl +'.smRadius', e=True, k=True)
    mc.connectAttr( ctrl +'.smRadius', deform +'.falloffRadius', f=True)

    # - offset
    mc.addAttr( ctrl, ln='offset', at='short', min=0, max=1)
    mc.setAttr( ctrl +'.offset', e=True, k=False, cb=True)

    smOffset = mc.spaceLocator( n= deform +'_offset')[0]
    mc.parent( smOffset, sRoot, r=True)
    mc.connectAttr( ctrl +'.offset', smOffset +'.v')
    mc.setAttr( smOffset +'Shape.localScale', .2, .2, .2)

    # - Connect softMod falloff center
    mc.connectAttr( smOffset +'.worldPosition', deform +'.falloffCenter', f=True)

    # - Connect BPM
    mc.connectAttr( ctrl +'.parentInverseMatrix', deform +'.bindPreMatrix', f=True)

    # - Clean Rig
    smShape  = mc.listConnections( deform, s=True, d=False, p=True, type='softModHandle')[0].rpartition('.')[0]
    mc.setAttr( smShape +'.v', 0)

    # --- Clean
    mc.setAttr( sRoot + '.visibility', k= False )
    mc.setAttr( ctrl + '.visibility', k= False )

    # - Offset locator
    mc.setAttr( smOffset + '.visibility', k= False )
    mc.setAttr( smOffset + 'Shape.ihi', 0)

    # - Remove unless handle
    mc.delete( handle )

    return deform
