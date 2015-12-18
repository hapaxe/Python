#----------------------------------------------------------------------
# rigtool orig
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint
import functions.selection as selection
import rigtool.defs as rigtool_defs

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Orig():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'origTool_Window'
        self.tool_title= 'orig settings'
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
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.37, 0.0, 0.0], l='', cll= False )

        self.widgets['suffix'] = mc.textFieldGrp( l=' Define suffix : ', cl2= [ 'left', 'right' ], cw2= [ 70, 70], text='orig', annotation= 'Define orig suffix name')
        self.widgets['comp_joint'] = mc.iconTextCheckBox( style='iconAndTextHorizontal', image1='rigTools_orig_jnt_no_comp.png', selectionImage= 'rigTools_orig_jnt_comp.png', label='Joint Scaling comp', value= False, annotation= 'Define if joint are scale compensate or not' )

        self.widgets['win_bt_launch'] = mc.button(l='Create orig', height= 30, c= self.launch )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):

        suffix = mc.textFieldGrp( self.widgets['suffix'], q=True, tx=True )
        comp_joint = mc.iconTextCheckBox( self.widgets['comp_joint'], q=True, v=True )

        on_selected( in_suffix= suffix, compensate_joint= comp_joint )

#----------------------------------------------------------------------
def on_selected( in_suffix= 'orig', compensate_joint= False ):
    '''

    :param in_suffix: Suffix add to in_obj name
    :type in_suffix: string

    :param compensate_joint: Define if joint are scale compensate or not
    :type compensate_joint: boolean

    :return: List of reset Group name
    :rtype: list
    '''
    # - Get current selection
    sel= mc.ls( sl= True, l= True )

    if not sel:
        viewPrint( msg= 'Select objects to add orig', mode= 1 )
        return

    # - Sort object by Hierarchy deeper rank
    obj_toRename= selection.sort_objectByHierarchy( in_obj= sel, order= 'dsc' )

    result= list()
    for item in obj_toRename:
        result.append( create( in_obj= item, in_suffix= in_suffix, compensate_joint= compensate_joint ) )

    return result


#----------------------------------------------------------------------
def create( in_obj, in_suffix= 'orig', compensate_joint= False ):
    '''
    Add a reset Grp parent of the inObj with the same WS position
    Compensate scaling for jnt object

    :param in_obj: the object name whose add a parent reset group
    :type in_obj: string

    :param in_suffix: Suffix add to in_obj name
    :type in_suffix: string

    :param compensate_joint: Define if joint are scale compensate or not
    :type compensate_joint: boolean

    :return: reset Group name
    :rtype: string
    '''
    # --- Define reset group Name
    name= in_obj.split('|')[-1]

    # - Replace suffix
    suffix_to_replace= [ 'Ctrl', 'ctrl', 'jnt' ]
    for suffix in suffix_to_replace:
        if in_obj.endswith( '_'+ suffix ):
            name= name.replace( '_'+ suffix, '' )

    # - Add suffix
    name= name + '_' + in_suffix

    # - Get parent
    parent= selection.get_parent( in_obj )
    # - Get WS transform
    dTrans= rigtool_defs.get_transform( in_obj )

    # --- Create group
    reset_grp= rigtool_defs.create_group( name= name, parent= parent, ws=True, lPos= dTrans['pos'], lRot= dTrans['rot'], lScl= dTrans['scl'] )

    # - Compensate joint Scaling
    comp_jnt= False
    if mc.nodeType( in_obj )== 'joint' and mc.nodeType( parent ) == 'joint' and compensate_joint == True:
        # - Get reset_grp Transform
        dT_grp = rigtool_defs.get_transform( reset_grp, ws= False )
        # - Reset Rotate
        mc.xform( reset_grp, ro= (0,0,0) )
        # - Set Rotate in jointOrient
        mc.setAttr( in_obj +'.jointOrient', dT_grp['rot'][0], dT_grp['rot'][1], dT_grp['rot'][2], type= 'double3')
        comp_jnt= True

    # - Parent
    obj= mc.parent( in_obj, reset_grp )[0]

    # - Compensate joint Scaling
    if comp_jnt == True:
        if not mc.isConnected( parent +'.scale', obj + '.inverseScale' ):
            mc.connectAttr( parent +'.scale', obj + '.inverseScale', f= True )

    return reset_grp