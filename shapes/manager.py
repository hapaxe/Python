#----------------------------------------------------------------------
# shapes manager
# Author : felixlechA.com | f.rault
# Date   : April 2015
# Decription : The UI to manage shapes
#----------------------------------------------------------------------
import maya.cmds as mc
from functools import partial
import shapes.defs as shapes_defs
reload( shapes_defs )
import functions.selection as selection
reload( selection )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ShapeManager():
    def __init__( self ):
        '''
        init Class
        '''
        self.widgets = {} # Dictionnary who store the tool's UI
        self.shapes_list= shapes_defs.get_availlable_shapes()
        self.shapes_list.append( 'none' )
        self.datas= self.get_selection_datas()

    def UI( self, activeTab= 1, *args ):
        '''
        Create UI
        '''
        # --- Check existing Windows
        if mc.window('ShapeManager_Window', exists=True ):
            mc.deleteUI( 'ShapeManager_Window', window=True )

        # --- Create window
        self.widgets['win'] = mc.window('ShapeManager_Window', title='Shape Manager', w= 200, sizeable= False )

        # --- Create Tabs
        self.widgets['tabs'] = mc.tabLayout()

        # --- Tab : Create
        self.widgets['frame_create'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.281, 0.388, 0.478], l='shape settings', cll= False )

        self.widgets['column_create'] = mc.columnLayout( adjustableColumn=True, w=180 )

        self.widgets['menu_shape'] = mc.optionMenu( label=' Select Shape' )
        for shape_name in self.shapes_list:
            mc.menuItem( self.widgets['menu_shape'], label = shape_name )

        self.widgets['slider_size'] = mc.floatSliderGrp( label=' Size', field= True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=100.0, value= 1, precision= 3, columnAlign3= ['left', 'right', 'right'], columnWidth3= [65, 50, 20] )

        self.widgets['radio_orientation'] = mc.radioButtonGrp( label=' Orientation', labelArray3=['X', 'Y', 'Z'], select= 0, numberOfRadioButtons=3, columnWidth4= [65, 25, 25, 25 ], columnAlign4= ['left', 'right', 'right', 'right'] )

        self.widgets['row_col'] = mc.rowLayout(numberOfColumns= 4, columnAlign4=('left', 'right', 'right', 'right'), columnWidth4= [65, 27, 27, 27] )

        self.widgets['text_mirror'] = mc.text( ' Mirror' )
        self.widgets['cBox_mirror_X'] = mc.checkBox( label='X', v=False )
        self.widgets['cBox_mirror_Y'] = mc.checkBox( label='Y', v=False )
        self.widgets['cBox_mirror_Z'] = mc.checkBox( label='Z', v=False )

        mc.setParent( self.widgets['column_create'] )

        self.widgets['cBox_middle_jnt'] = mc.checkBox( label='Place in the middle of joints', v=True )

        self.widgets['cBox_remove_prev_shape'] = mc.checkBox( 'ui_remove_previous_shape', label='Remove previous Shapes', v=True )

        self.widgets['button_create'] = mc.button( label='Add Shape', command= self.launch, h=40, w=180 )


        # --- Tab : Edit
        mc.setParent( self.widgets['win'] )
        self.widgets['frame_edit'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.281, 0.388, 0.478], l='shape settings', cll= False )
        self.widgets['column_edit'] = mc.columnLayout( adjustableColumn=True, w=180 )

        self.widgets['row_col'] = mc.rowLayout(numberOfColumns= 2, columnAlign2=('left', 'right') )
        self.widgets['scroll_objects'] = mc.textScrollList( allowMultiSelection= True, append= self.datas.keys(), showIndexedItem= 1, font= 'fixedWidthFont', h= 100, w=90, sc= self.show_object_shapes )
        self.widgets['scroll_shapes'] = mc.textScrollList( allowMultiSelection= True, append= [], showIndexedItem= 1, font= 'fixedWidthFont', h= 100, w=90, sc= self.select_shape )

        mc.setParent( self.widgets['column_edit'] )
        self.widgets['button_refresh'] = mc.button( label='refresh', command= self.refresh_edit, h=20, w=180 )

        self.widgets['row_col'] = mc.rowLayout(numberOfColumns= 4, columnAlign4=('left', 'right', 'right', 'right'), columnWidth4= [65, 27, 27, 27] )

        self.widgets['text_mirror'] = mc.text( ' Mirror' )
        self.widgets['cBox_mirror_X_edit'] = mc.checkBox( label='X', v=False )
        self.widgets['cBox_mirror_Y_edit'] = mc.checkBox( label='Y', v=False )
        self.widgets['cBox_mirror_Z_edit'] = mc.checkBox( label='Z', v=False )

        mc.setParent( self.widgets['column_edit'] )
        self.widgets['button_edit_mirror'] = mc.button( label='Mirror Selected', command= self.launch_edit_mirror, h=40, w=180 )
        self.widgets['button_edit_remove'] = mc.button( label='Remove Selected', command= self.launch_edit_remove, h=30, w=180 )
        self.widgets['button_edit_copy'] = mc.button( label='Copy to Selected', command= self.launch_edit_copy, h=30, w=180 )

        # --- Tab : Manage
        mc.setParent( self.widgets['win'] )
        self.widgets['column_manage'] = mc.columnLayout( adjustableColumn=True, w=180 )

        self.widgets['frame_manage'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.281, 0.388, 0.478], l='Store Curve', cll= False )
        self.widgets['manage_win_col'] = mc.columnLayout( adjustableColumn=True, w=180 )

        self.widgets['cBox_store_manage'] = mc.checkBox( label='Edit previous Shapes', v=False, annotation= 'Overwrite existing shapes' )
        self.widgets['store_shape'] = mc.button( label='Store Selected', command= self.launch_store_curves, h=40, w=180 )

        mc.setParent( self.widgets['column_manage'] )
        self.widgets['frame_remove'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.281, 0.388, 0.478], l='Remove json file', cll= False )
        self.widgets['remove_win_col'] = mc.columnLayout( adjustableColumn=True, w=180 )

        self.widgets['remove_shape'] = mc.optionMenu( label=' Select Shape' )
        for shape_name in self.shapes_list:
            mc.menuItem( self.widgets['remove_shape'], label = shape_name )

        self.widgets['store_shape'] = mc.button( label='Remove', command= self.launch_remove_json, h=40, w=180 )


        mc.tabLayout( self.widgets['tabs'], edit=True, tabLabel=((self.widgets['frame_create'], 'Create'), ( self.widgets['frame_edit'], 'Edit'), ( self.widgets['column_manage'], 'Manage')), selectTabIndex= activeTab )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):
        '''
        '''
        # --- Get UI infos
        shape= mc.optionMenu( self.widgets['menu_shape'], q=True, v=True )
        size= mc.floatSliderGrp( self.widgets['slider_size'], q=True, v=True )
        orient= mc.radioButtonGrp( self.widgets['radio_orientation'], q=True, select= True )

        mirror_X= mc.checkBox( self.widgets['cBox_mirror_X'], q=True, v=True )
        mirror_Y= mc.checkBox( self.widgets['cBox_mirror_Y'], q=True, v=True )
        mirror_Z= mc.checkBox( self.widgets['cBox_mirror_Z'], q=True, v=True )

        middle_jnt= mc.checkBox( self.widgets['cBox_middle_jnt'], q=True, v=True )

        removePrevious= mc.checkBox( self.widgets['cBox_remove_prev_shape'], q=True, v=True )

        # - Set orient
        orientAxis = ['X', 'Y', 'Z']
        orient= orientAxis[ orient -1 ]

        # - Set mirror
        mirror= [1, 1, 1]
        if mirror_X:
            mirror[0]= -1
        if mirror_Y:
            mirror[1]= -1
        if mirror_Z:
            mirror[2]= -1

        # --- Get Selection
        sel= mc.ls( sl= True )

        # - If selection is empty create a new control
        if not sel:
            sel = [mc.group( em=True, name= shape + '_ctrl' )]

        for item in sel:
            # - Remove previous Shape if needs
            if removePrevious or shape== 'none':
                previous_shape= selection.get_shapesType( item, type= 'nurbsCurve' )
                if previous_shape:
                    mc.delete( previous_shape )

            # - Add new Shape
            if not shape== 'none':
                shapes_defs.add_shape( item, shape= shape, size= size, orient= orient, mirror= mirror, middle_jnt= middle_jnt )

        # --- reSelect previous Selection
        mc.select( sel )

    def launch_edit_mirror(self, *args):
        '''

        :param args:
        :return:
        '''
        mirror_X= mc.checkBox( self.widgets['cBox_mirror_X_edit'], q=True, v=True )
        mirror_Y= mc.checkBox( self.widgets['cBox_mirror_Y_edit'], q=True, v=True )
        mirror_Z= mc.checkBox( self.widgets['cBox_mirror_Z_edit'], q=True, v=True )

        shapes_selected = mc.textScrollList( self.widgets[ 'scroll_shapes' ], selectItem= True, q= True ) or list()

        # - Set mirror
        mirror= [1, 1, 1]
        if mirror_X:
            mirror[0]= -1
        if mirror_Y:
            mirror[1]= -1
        if mirror_Z:
            mirror[2]= -1

        # - Mirror
        for item in shapes_selected:
            mc.scale( mirror[0], mirror[1], mirror[2], item+ '.cv[*]', r=True)

    def launch_edit_remove(self, *args):
        '''

        :param args:
        :return:
        '''
        edit_shape_objects = mc.textScrollList( self.widgets[ 'scroll_objects' ], allItems= True, q= True ) or list()
        edit_shape_toRemove = mc.textScrollList( self.widgets[ 'scroll_shapes' ], selectItem= True, q= True ) or list()

        # - Delete shape
        for item in edit_shape_toRemove:
            mc.delete( item )

        self.refresh_edit( in_object= edit_shape_objects )

    def launch_store_curves(self, *args):
        '''

        :param args:
        :return:
        '''
        # --- Get UI infos
        edit= mc.checkBox( self.widgets['cBox_store_manage'], q=True, v=True )

        shapes_defs.store_selected_ctrl_curve( edit= edit )

        # - refresh UI
        self.shapes_list= shapes_defs.get_availlable_shapes()
        self.UI( activeTab= 3 )

    def launch_remove_json(self, *args):
        '''

        :param args:
        :return:
        '''
        # --- Get UI infos
        shape_toRemove= mc.optionMenu( self.widgets['remove_shape'], q=True, v=True )

        shapes_defs.delete_shape_jsonFile( in_name= shape_toRemove )

        # - refresh UI
        self.shapes_list= shapes_defs.get_availlable_shapes()
        self.UI( activeTab= 3 )

    def refresh_edit(self, in_object= None, *args):

        self.datas= self.get_selection_datas( in_object= in_object )
        self.UI( activeTab= 2 )

    def select_shape(self, *args):

        shapes_selected = mc.textScrollList( self.widgets[ 'scroll_shapes' ], selectItem= True, q= True ) or list()
        mc.select( shapes_selected )

    def get_selection_datas(self, in_object= None, *args):

        result= dict()

        if not in_object:
            in_object= mc.ls( sl=True, l= True )

        if in_object:
            for item in in_object:
                result[item]= selection.get_shapesType( item, type= 'nurbsCurve' ) or list()

        return result

    def show_object_shapes(self, *args):
        object_selected = mc.textScrollList( self.widgets[ 'scroll_objects' ], selectItem= True, q= True ) or list()

        shapes_to_show= list()
        for item in object_selected:
            shapes_to_show.extend( self.datas[item] )

        mc.textScrollList( self.widgets['scroll_shapes'], removeAll= True, edit= True)
        mc.textScrollList( self.widgets['scroll_shapes'], append= shapes_to_show, edit= True )

    def launch_edit_copy(self, *args):

        mirror_X= mc.checkBox( self.widgets['cBox_mirror_X_edit'], q=True, v=True )
        mirror_Y= mc.checkBox( self.widgets['cBox_mirror_Y_edit'], q=True, v=True )
        mirror_Z= mc.checkBox( self.widgets['cBox_mirror_Z_edit'], q=True, v=True )

        # - Set mirror
        mirror= [1, 1, 1]
        if mirror_X:
            mirror[0]= -1
        if mirror_Y:
            mirror[1]= -1
        if mirror_Z:
            mirror[2]= -1

        edit_shape_toCopy = mc.textScrollList( self.widgets[ 'scroll_shapes' ], selectItem= True, q= True ) or list()

        target= mc.ls( sl=True, l= True )[0]

        for item in edit_shape_toCopy:
            # - Get parent
            source= selection.get_parent( item )

            # - Create a TMP Group
            tmp_group = mc.group( em=True )

            # - parent Shape Temporary
            mc.parent( item, tmp_group, s=True, r=True )

            # - Duplicate Group
            tmp_group_twin= mc.duplicate( tmp_group )[0]

            # - Reparent Shape
            previous_shape = mc.listRelatives(tmp_group, s=True, fullPath= True)[0]
            mc.parent( previous_shape, source, s=True, r=True )

            # - Parent Shape to target
            duplicate_shape = mc.listRelatives(tmp_group_twin, s=True, fullPath= True)[0]
            mc.parent( duplicate_shape, target, s=True, r=True )
            # - Rename the duplicate Shape
            shape_list = mc.listRelatives(target, s=True, fullPath= True)
            for shape in shape_list:
                if mc.nodeType( shape ) == 'nurbsCurve':
                    duplicate_shape= shape

            shape_obj= mc.rename( duplicate_shape, target +'Shape')

            # - Clean
            mc.delete( [tmp_group, tmp_group_twin] )

            mc.scale( mirror[0], mirror[1], mirror[2], shape_obj+ '.cv[*]', r=True)
