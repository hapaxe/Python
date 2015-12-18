#----------------------------------------------------------------------
# asset_importer importer
# Author : felixlechA.com | f.rault
# Date   : May 2015
# Decription : asset importer tool
#----------------------------------------------------------------------
import maya.cmds as mc
from functools import partial
import os

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AssetImporter():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'assetImporterTool_Window'
        self.tool_title= 'Asset Importer Tool'
        self.project_name= os.environ['CUBE_PROJECT_NAME']
        self.project_datas= os.environ['CUBE_PROJECT_DATAS']

        self.type_list= get_subdirectories( in_path=  self.project_datas + '\Asset' )
        self.asset_list= get_subdirectories( in_path=  '' )
        self.task_list= get_subdirectories( in_path=  '' )

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
        self.widgets['win'] = mc.window( self.tool_name, title= self.tool_title, sizeable= False , toolbox= True )

        self.widgets['win_col'] = mc.columnLayout( adj= True )
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, cll= False, bgc=[0.537, 0.590, 0.118], l= self.project_name, labelVisible= True, bv= False )

        # --- Type
        self.widgets['row_layout_type'] = mc.rowColumnLayout( nc = 2 , cw = [(1, 90), (2, 200)], columnOffset = [(1, 'both', 15), (2, 'both', 5)] )
        self.widgets['text_type'] = mc.text(l = 'Type', w = 95, h = 30, align = 'left' )
        self.widgets['menu_type'] = mc.optionMenu( w =  195, h = 30, cc= partial( self.menu_change, 'type' ) )
        for type in self.type_list:
            mc.menuItem( self.widgets['menu_type'], label = type )

        # --- Asset
        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_layout_asset'] = mc.rowColumnLayout(nc = 2, cw = [(1, 90), (2, 200)], columnOffset = [(1, 'both', 15), (2, 'both', 5)] )
        self.widgets['text_asset'] = mc.text(l = 'Asset', w = 95, h = 30, align = 'left' )
        self.widgets['menu_asset'] = mc.optionMenu( w =  195, h = 30, cc= partial( self.menu_change, 'asset' ) )
        for asset in self.asset_list:
            mc.menuItem( self.widgets['menu_asset'], label = asset )

        # --- Task
        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_layout_task'] = mc.rowColumnLayout(nc = 2, cw = [(1, 90), (2, 200)], columnOffset = [(1, 'both', 15), (2, 'both', 5)] )
        self.widgets['text_task'] = mc.text(l = 'Task', w = 95, h = 30, align = 'left' )
        self.widgets['menu_task'] = mc.optionMenu( w =  195, h = 30, cc= partial( self.menu_change, 'task' ) )
        for task in self.task_list:
            mc.menuItem( self.widgets['menu_task'], label = task )

        # --- nameSpace
        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['separator'] = mc.separator( style='in' )
        self.widgets['row_layout_nameSpace'] = mc.rowColumnLayout(nc = 2, cw = [(1, 140), (3, 150)], columnOffset = [(1, 'both', 15), (2, 'both', 0)] )
        self.widgets['checkBox_nameSpace'] = mc.checkBox( w = 135, h = 30, l = 'Force nameSpace', cc= partial( self.menu_change, 'checkBox_ns' ) )
        self.widgets['textField_nameSpace'] = mc.textField( w = 150, h = 30, en = False )

        # --- How Many
        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_layout_howMany'] = mc.rowColumnLayout( nc = 2, cw = [(1, 140), (2, 150)], columnOffset = [(1, 'both', 33), (2, 'both', 0)] )
        self.widgets['text_howMany'] = mc.text(l = 'How many import', w = 117, h = 30, align = 'left' )
        self.widgets['intField_howMany'] = mc.intField( w = 150, v = 1, min= 1 )

        # --- Process
        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['separator'] = mc.separator( style='in' )
        self.widgets['row_layout_process'] = mc.rowColumnLayout(nc = 2, cw = [(1, 65), (2, 225)] )
        self.widgets['win_bt_reset'] = mc.button( height= 50, label='Import', annotation= 'Import', c= partial( self.import_asset, 'local') )
        self.widgets['win_bt_launch'] = mc.button ( height= 50, label = 'Import as Reference', c= partial( self.import_asset, 'reference') )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def menu_change(self, input_name, *args ):

        type_item= mc.optionMenu( self.widgets['menu_type'], q = True, v = True )
        asset_item= mc.optionMenu( self.widgets['menu_asset'], q = True, v = True )

        if input_name == 'type':
            if not type_item == '---':
                self.asset_list= get_subdirectories( in_path=  self.project_datas + '\Asset\\'+ type_item )
                self.task_list= get_subdirectories( in_path=  self.project_datas + '\Asset\\'+ type_item +'\\'+ asset_item )
            else:
                self.asset_list= get_subdirectories( in_path=  '' )
                self.task_list= get_subdirectories( in_path=  '' )

        if input_name == 'asset':
            if not asset_item == '---':
                self.task_list= get_subdirectories( in_path=  self.project_datas + '\Asset\\'+ type_item +'\\'+ asset_item )
            else:
                self.task_list= get_subdirectories( in_path=  '' )

        self.refresh_UI()

    def refresh_UI(self, *args ):

        type_item= mc.optionMenu( self.widgets['menu_type'], q = True, v = True )
        asset_item= mc.optionMenu( self.widgets['menu_asset'], q = True, v = True )
        task_item= mc.optionMenu( self.widgets['menu_task'], q = True, v = True )
        checkBox_ns= mc.checkBox( self.widgets['checkBox_nameSpace'], q = True, v = True)

        # --- Type
        mc.deleteUI( self.widgets['menu_type'] )
        self.widgets['menu_type'] = mc.optionMenu( w =  195, h = 30, parent= self.widgets['row_layout_type'], cc= partial( self.menu_change, 'type' ) )
        task_ON= 1
        for i in range( 0, len(self.type_list), 1 ):
            if self.type_list[i] == type_item:
                task_ON= i
            mc.menuItem( self.widgets['menu_type'], label = self.type_list[i] )
        if type_item in self.type_list:
            mc.optionMenu( self.widgets['menu_type'], edit= True, select= task_ON+1 )

        # --- Asset
        mc.deleteUI( self.widgets['menu_asset'] )
        self.widgets['menu_asset'] = mc.optionMenu( w =  195, h = 30, parent= self.widgets['row_layout_asset'], cc= partial( self.menu_change, 'asset' ) )
        asset_ON= 1
        for i in range( 0, len(self.asset_list), 1 ):
            if self.asset_list[i] == asset_item:
                asset_ON= i
            mc.menuItem( self.widgets['menu_asset'], label = self.asset_list[i] )
        if asset_item in self.asset_list:
            mc.optionMenu( self.widgets['menu_asset'], edit= True, select= asset_ON+1 )

        # --- Task
        mc.deleteUI( self.widgets['menu_task'] )
        self.widgets['menu_task'] = mc.optionMenu( w =  195, h = 30, parent= self.widgets['row_layout_task'], cc= partial( self.menu_change, 'task' ) )
        task_ON= 1
        for i in range( 0, len(self.task_list), 1 ):
            if self.task_list[i] == task_item:
                task_ON= i
            mc.menuItem( self.widgets['menu_task'], label = self.task_list[i] )
        if task_item in self.task_list:
            mc.optionMenu( self.widgets['menu_task'], edit= True, select= task_ON+1 )

        # --- checkBox NS
        if checkBox_ns:
            mc.textField( self.widgets['textField_nameSpace'], edit= True, en= True )
        else:
            mc.textField( self.widgets['textField_nameSpace'], edit= True, en= False )

        ns= build_nameSpace( type= type_item, asset= asset_item )
        mc.textField( self.widgets['textField_nameSpace'], edit= True, tx= ns )

    def import_asset(self, mode, *args):

        # - Get datas from UI
        type_item= mc.optionMenu( self.widgets['menu_type'], q = True, v = True )
        asset_item= mc.optionMenu( self.widgets['menu_asset'], q = True, v = True )
        task_item= mc.optionMenu( self.widgets['menu_task'], q = True, v = True )
        namespace= mc.textField( self.widgets['textField_nameSpace'], q = True, tx = True)
        howMany= mc.intField( self.widgets['intField_howMany'], q = True, v = True)

        # - Build directory path
        full_path= self.project_datas + '\Asset\\'+ type_item +'\\'+ asset_item +'\\'+ task_item

        # - Build file name
        file_name= type_item.split('_')[0] +'_'+ asset_item.split('_')[0] +'_'+ task_item +'_'+ asset_item.split('_')[1] +'.ma'

        # - Get files in directory
        file_list = os.listdir( full_path )

        if file_name in file_list:
            for i in range( 0, howMany):
                if mode == 'reference':
                    mc.file( full_path +'\\'+ file_name, r= True, type = "mayaAscii", gl = True, loadReferenceDepth= "all", namespace= namespace, options = "v=0")
                elif mode == 'local':
                    if namespace == '':
                        mc.file( full_path +'\\'+ file_name, i= True, type = "mayaAscii", mergeNamespacesOnClash= False, gl = True, loadReferenceDepth= "all", rpr= '', options = "v=0")
                    else:
                        mc.file( full_path +'\\'+ file_name, i= True, type = "mayaAscii", gl = True, loadReferenceDepth= "all", namespace= namespace, options = "v=0")
        else:
            print 'no file found !'

#----------------------------------------------------------------------
def get_subdirectories( in_path ):
    '''
    Get the sub directory of a given path

    :param in_path: Path to get sub directory
    :type in_path: string

    :return: A list of sub directory order with '---' in first item
    :rtype: list
    '''
    sub_directory= list()
    if os.path.exists( in_path ):
        for item in os.listdir( in_path ):
            if os.path.isdir( os.path.join( in_path, item )):
                sub_directory.append( item )

    result= ['---']
    sort_sub_directory= sorted( sub_directory )
    result.extend( sort_sub_directory )

    return result

#----------------------------------------------------------------------
def build_nameSpace( type, asset ):

    # - Build base name
    if type == '---' or asset == '---':
        return ''

    base_name= type.split('_')[0] + '_' + asset.split('_')[0] + '_'

    # - Get All nameSpace in scene
    all_nameSpace= mc.namespaceInfo( ':', lon= True, recurse=True )

    nbr= 1
    numbering= ''
    for ns in all_nameSpace:
        numbering= ''
        # - Build Padding
        nbr_zero= 3 - len(str(nbr))
        for i in range( 0, nbr_zero):
            numbering += '0'
        numbering += str(nbr)

        # - Test ns Existing
        if not ns in ['UI', 'shared']:
            if mc.namespace( ex = base_name + numbering ):
                nbr += 1
            else:
                break

    return base_name + numbering