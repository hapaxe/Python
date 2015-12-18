#----------------------------------------------------------------------
# dynamicSystem Manager
# Author : felixlechA.com | r.rault
# Date   : December 2014
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functools import partial
from functions import animation, connection, general

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DynamicSystemManager():
    '''
    Tool to Manage Dynamic System create with the Dynamic System Creator
    '''
    
    def __init__( self ):
        '''
        init Class
        '''
        self.widgets = {} # Dictionnary who store the tool's UI
        self.datas = self.get_dynamic_system_datas() # Dictionnary who store the current scene dynSystem datas

    #----------------------------------------------------------------------
    def UI( self, *args ):
        '''
        The dynamic System Manager UI
        '''
        # --- Check existing Windows
        if mc.window('DynamicSystemManager_Window', exists=True ):
            mc.deleteUI( 'DynamicSystemManager_Window', window=True )
    
        # --- Create window
        self.widgets['win'] = mc.window('DynamicSystemManager_Window', title='Dynamic System Manager', w= 450 )

        self.widgets['win_col'] = mc.columnLayout( adj= True )
        self.widgets['win_bt_refresh'] = mc.button(l='Update Datas from Scene', height= 25, c= self.update_datas_UI )
        
        # --- SELECTION
        self.widgets['SELECT_row'] = mc.rowLayout( numberOfColumns=2, rowAttach= [ (1, 'top', 0), (2, 'top', 0) ], adj= 2)

        self.widgets['NS_col'] = mc.columnLayout()
        self.widgets['NS_txt'] = mc.text( l=' nameSpace', h= 20, align= 'left')
        self.widgets['NS_list'] = mc.textScrollList( allowMultiSelection= True, append= self.datas.keys(), showIndexedItem= 1, h= 150, w= 220, font= 'fixedWidthFont', annotation='Select nameSpace.', sc= partial( self.scrollList_update, 'DS_list') )
        self.widgets['NS_button_row'] = mc.rowLayout( numberOfColumns=3, rowAttach= [ (1, 'top', 0), (2, 'top', 0), (3, 'top', 0) ])
        self.widgets['NS_bt_select_clear'] = mc.button(l='clear', h= 20, w= 55, c= partial( self.scrollList_manage_selection, 'NS_list', 'clear' ))
        self.widgets['NS_bt_select_invert'] = mc.button(l='invert', h= 20, w= 55, c= partial( self.scrollList_manage_selection, 'NS_list', 'invert' ))
        self.widgets['NS_bt_select_all'] = mc.button(l='select all', h= 20, w= 105, c= partial( self.scrollList_manage_selection, 'NS_list', 'all' ))

        mc.setParent( self.widgets['SELECT_row'])
        self.widgets['DS_col'] = mc.columnLayout( adj= True)
        self.widgets['NS_txt'] = mc.text( l=' dynamic System', h= 20, align= 'left')
        self.widgets['DS_list'] = mc.textScrollList( allowMultiSelection= True, append= [], showIndexedItem= 1, h= 150, w= 220, font= 'fixedWidthFont', annotation='Select Dynamic System', dcc= self.select_global_ctrl )
        self.widgets['DS_button_row'] = mc.rowLayout( numberOfColumns=3, rowAttach= [ (1, 'top', 0), (2, 'top', 0), (3, 'top', 0) ], adj= 3)
        self.widgets['DS_bt_select_clear'] = mc.button(l='clear', h= 20, w= 55, c= partial( self.scrollList_manage_selection, 'DS_list', 'clear' ))
        self.widgets['DS_bt_select_invert'] = mc.button(l='invert', h= 20, w= 55, c= partial( self.scrollList_manage_selection, 'DS_list', 'invert' ))
        self.widgets['DS_bt_select_all'] = mc.button(l='select all', h= 20, c= partial( self.scrollList_manage_selection, 'DS_list', 'all' ))

        mc.setParent( self.widgets['win_col'])
        self.widgets['ACTION_sep'] = mc.separator( style='none', height=5 )

        # --- ACTION
        self.widgets['ACTION_frame'] = mc.frameLayout(l='Execute on selected', width= 450, bs= 'etchedIn', cll=False )
        self.widgets['ACTION_col'] = mc.columnLayout( adj= True )
        self.widgets['ACTION_row'] = mc.rowLayout( numberOfColumns=2, rowAttach= [ (1, 'top', 0), (2, 'top', 0) ], adj= 2 )
        self.widgets['ACTION_bt_disble'] = mc.button(l='select Global Ctrl', h= 30, w= 220, c= self.select_global_ctrl )
        self.widgets['ACTION_bt_disble'] = mc.button(l='set start frame at current', h= 30, w= 220, c= self.set_start_frame_at_current )

        mc.setParent( self.widgets['ACTION_col'])
        self.widgets['NS_txt'] = mc.text( l=' Turn ON / OFF Dynamic', h= 15, align= 'left')
        self.widgets['ACTION_row'] = mc.rowLayout( numberOfColumns=2, rowAttach= [ (1, 'top', 0), (2, 'top', 0) ], adj= 2 )
        self.widgets['ACTION_bt_enable'] = mc.button(l='OFF', h= 30, w= 220, c= partial( self.enable_disable_dynamic_system, 'OFF' ))
        self.widgets['ACTION_bt_disble'] = mc.button(l='ON', h= 30, w= 220, c= partial( self.enable_disable_dynamic_system, 'ON' ))

        mc.setParent( self.widgets['ACTION_col'])
        self.widgets['NS_txt'] = mc.text( l=' Bake / Unbake Dynamic', h= 15, align= 'left')
        self.widgets['ACTION_row'] = mc.rowLayout( numberOfColumns=2, rowAttach= [ (1, 'top', 0), (2, 'top', 0) ], adj= 2)
        self.widgets['ACTION_bt_unbake'] = mc.button(l='unbake', h= 30, w= 220, c= partial( self.bake_dynamic, 'unbake' ), annotation= 'Remove keys on Dynamic Joints.')
        self.widgets['ACTION_bt_bake'] = mc.button(l='bake', h= 30, w= 220, c= partial( self.bake_dynamic, 'bake' ), annotation= 'Bake Dynamic Joints in the Scene time range.')

        mc.setParent( self.widgets['ACTION_col'])
        self.widgets['NS_txt'] = mc.frameLayout( l='Extra', width= 450, bs= 'etchedIn', cll=True, cl=True )
        self.widgets['ACTION_row'] = mc.rowLayout( numberOfColumns=2, rowAttach= [ (1, 'top', 0), (2, 'top', 0) ], adj= 2)
        self.widgets['ACTION_bt_select_system'] = mc.button(l='select dyn System', h= 30, w= 220, c= self.select_dynamic_system )
        
        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def update_datas_UI( self, *args ):
        '''
        Update the datas dictionnary with info from current scene and update UI
        '''
        self.datas.clear()
        self.datas = self.get_dynamic_system_datas()

        self.scrollList_update( in_scrollList= 'NS_list' )        
        self.scrollList_update( in_scrollList= 'DS_list' )
        
    #----------------------------------------------------------------------
    def scrollList_manage_selection( self, in_scrollList, in_mode, *args ):
        '''
        Manage the selected items in the in_scrollList.
        - clear : No items displayed will be select
        - invert : Previous selected will be no select and Previous no selected will be select
        - all : All items displayed will be select
        
        :param in_scrollList: Define the scrollList name.
        :type in_scrollList: string

        :param in_mode: Define the mode to execute. Values : 'clear' 'invert' 'all'
        :type in_mode: string
        '''
        # --- CLEAR selection
        if in_mode == 'clear':
            mc.textScrollList( self.widgets[ in_scrollList ], deselectAll= True, edit= True )

        # --- INVERT selection
        if in_mode == 'invert':
            l_item = mc.textScrollList( self.widgets[ in_scrollList ], allItems= True, q= True )
            l_selected = mc.textScrollList( self.widgets[ in_scrollList ], selectItem= True, q= True ) or list()

            for s_item in l_item:
                if s_item in l_selected:
                    mc.textScrollList( self.widgets[ in_scrollList ], deselectItem= s_item, edit= True )
                else:
                    mc.textScrollList( self.widgets[ in_scrollList ], selectItem= s_item, edit= True )
    
        # --- select ALL
        if in_mode == 'all':
            l_item = mc.textScrollList( self.widgets[ in_scrollList ], allItems= True, q= True )
            mc.textScrollList( self.widgets[ in_scrollList ], selectItem= l_item, edit= True )

        if in_scrollList != 'DS_list':
            self.scrollList_update('DS_list')

    #----------------------------------------------------------------------
    def scrollList_update( self, in_scrollList, *args ):
        '''
        Update the display list of the UI scrollList. Refresh items list and selected or not.
        
        :param in_scrollList: Define the scrollList name. Values : 'NS_list' 'DS_list'
        :type in_scrollList: string
        '''
        # --- Update nameSpace list
        if in_scrollList == 'NS_list':
            # Get selected in NS_list
            l_nameSpace_selected = mc.textScrollList( self.widgets['NS_list'], q=True , selectItem=True ) or list()
            
            # Clean DS_scrollList
            mc.textScrollList( self.widgets['NS_list'], removeAll= True, edit= True)

            # --- Selected nameSpace like previous if possible            
            mc.textScrollList( self.widgets['NS_list'], append= self.datas.keys(), edit= True)
            for s_item in self.datas.keys():
                if s_item in l_nameSpace_selected:
                    mc.textScrollList( self.widgets['NS_list'], selectItem= s_item, edit= True )

        # --- Update dynamic System list
        if in_scrollList == 'DS_list':
            # Get selected in NS_list
            l_dynSystem_selected = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True ) or list()
            
            # Clean DS_scrollList
            mc.textScrollList( self.widgets['DS_list'], removeAll= True, edit= True)
            
            # Get selected in NS_list
            l_NS_list = mc.textScrollList( self.widgets['NS_list'], q=True , selectItem=True ) or list()
            
            l_DS_to_display = []
            i = 1
            for s_nameSpace in self.datas.keys():
                # Check if nameSpace is selected in UI
                if s_nameSpace in l_NS_list:
                    # for each nameSapace selected get each dynSystem and this state
                    for s_DS_name in self.datas[ s_nameSpace ].keys():
                        if self.datas[s_nameSpace][s_DS_name] == 0:
                            l_DS_to_display.append( 'OFF| '+ s_DS_name )
                        elif self.datas[s_nameSpace][s_DS_name] == 1:
                            l_DS_to_display.append( ' ON| '+ s_DS_name )
                        elif self.datas[s_nameSpace][s_DS_name] == 2:
                            l_DS_to_display.append( ' BK| '+ s_DS_name )
                        # increase iterator
                        i = i + 1

            # --- Show in scrollList the result
            mc.textScrollList( self.widgets['DS_list'], append= l_DS_to_display, edit= True )
            
            # --- Selected dynSystem like previous if possible
            if l_dynSystem_selected:
                # Rebuild previous selected list without ON| / OFF| prefix
                for i in range(len( l_dynSystem_selected )):
                    l_dynSystem_selected[i] = l_dynSystem_selected[i].split('| ')[1]
                # Check and select as previous
                for s_item in l_DS_to_display:
                    if s_item.split('| ')[1] in l_dynSystem_selected:
                        mc.textScrollList( self.widgets['DS_list'], selectItem= s_item, edit= True )

    #----------------------------------------------------------------------
    def select_global_ctrl( self, *args ):
        '''
        Select the corresponding Global_Ctrl of the selected dynamic System
        '''
        # Get selected dynamic System
        l_dynSystem_selected = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True )
        
        if l_dynSystem_selected:
            l_to_select = list()
            for s_dynSystem_selected in l_dynSystem_selected:
                # Get the name of the corresponding Global_Ctrl
                l_to_select.append( connection.get_MessageConnection_Input( s_dynSystem_selected.split('| ')[1], 'globalCtrl' ) )
            
            # --- Select Global_Ctrl of the selected Dyn System
            mc.select( l_to_select )

    #----------------------------------------------------------------------
    def select_dynamic_system( self, *args ):
        '''
        Select the dynamic System of the selected
        '''
        # Get selected dynamic System
        l_dynSystem_selected = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True )
        
        if l_dynSystem_selected:
            l_to_select = list()
            for s_dynSystem_selected in l_dynSystem_selected:
                # Get the exact name of dyn System
                l_to_select.append( s_dynSystem_selected.split('| ')[1] )
            
            # --- Select dynamic System
            mc.select( l_to_select )

    #----------------------------------------------------------------------
    def enable_disable_dynamic_system( self, in_mode, *args ):
        '''
        Turn ON / OFF the selected dynamic System
        
        :param in_mode: Define the state you want turn the dynamic System. Values : 'ON' 'OFF'
        :type in_mode: string
        '''         
        # Get selected dynamic System
        l_dynSystem_selected = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True )

        if l_dynSystem_selected:
            # Define the state value
            if in_mode == 'ON':
                i_state= 1
            elif in_mode == 'OFF':
                i_state= 0
            
            # --- Turn dynamic System ON / OFF
            log= ''
            for s_dynSystem_selected in l_dynSystem_selected:
                state_bake= mc.getAttr( connection.get_MessageConnection_Input( s_dynSystem_selected.split('| ')[1], 'globalCtrl') + '.dynamicJoints_bake' )
                if state_bake:
                    log += '\n'+ s_dynSystem_selected.split('| ')[1]
                else:
                    mc.setAttr( connection.get_MessageConnection_Input( s_dynSystem_selected.split('| ')[1], 'globalCtrl') + '.on_off', i_state )

            # --- Print log
            if log:
                message = '\n<hl>Unbake</hl> dynamic before turn <hl>' + in_mode +'</hl>'+ log
                general.viewPrint( message, mode= 2 )
            
            # --- Update UI
            self.update_datas_UI()

    #----------------------------------------------------------------------
    def set_start_frame_at_current( self, *args):
        '''
        Set the start frame of selected dynamic System to ocurrent frame
        '''
        # Get selected dynamic System
        l_dynSystem_selected = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True )
        
        if l_dynSystem_selected:
            # Get current time
            i_time = mc.currentTime( q=True )
                    
            # --- Set start frame to current frame
            for s_dynSystem_selected in l_dynSystem_selected:
                s_attr_start_frame = connection.get_MessageConnection_Input( s_dynSystem_selected.split('| ')[1], 'globalCtrl') + '.startFrame'
                mc.setAttr( s_attr_start_frame, i_time )
                
            message = 'Start Frame set to <hl>' + str(i_time) +'</hl>'
            general.viewPrint( message, mode= 1 )

    #----------------------------------------------------------------------
    def bake_dynamic( self, in_mode, externalRun= False, *args ):
        '''
        Bake/Unbake the dynamic Joints of the selected dynamic System.
        in_mode = 'bake' Bake the dynamic Joints
        in_mode = 'unbake' Remove keys on dynamic Joints
        
        :param in_mode: Define the mode 'bake' or 'unbake'
        :type in_mode: string
        
        :param externalRun: If True the command works without UI
        :type externalRun: boolean
        '''
        # --- Define VARIABLES
        if externalRun:
            l_objects = mc.ls( sl= True ) or list()
            s_Attr = 'dyn_jointCtrl'
        else:
            l_objects = mc.textScrollList( self.widgets['DS_list'], q=True , selectItem=True ) or list()
            for i in range( len( l_objects )):
                l_objects[i] = l_objects[i].split('| ')[1]
            s_Attr = 'globalCtrl'

        # --- Get the Global_Ctrl of each in_Obj_list
        l_global_name = []
        for s_item in l_objects:
            s_global_name = connection.get_MessageConnection_Input( inObj= s_item, inAttr= s_Attr )
            if s_global_name:
                state_enable = mc.getAttr( s_global_name+ '.on_off' )
                state_bake = mc.getAttr( s_global_name+ '.dynamicJoints_bake' )
                # Add to list
                # 1. already bake and we want unbake
                # 2. not already bake AND dyn enable AND we want bake
                if (state_bake and in_mode == 'unbake') or ( not state_bake and in_mode == 'bake' and state_enable ):
                    l_global_name.append( s_global_name )
        
        # Remove duplicate to have a unique items list
        l_global_name = list(set( l_global_name ))

        # --- Get the dyn Joints
        l_dynJoints = []
        for s_item in l_global_name:
            l_Joints = connection.get_MessageConnection_Ouput( inObj= s_item, inAttr= 'dyn_jointDyn' )
            if l_Joints:
                l_dynJoints.extend( l_Joints )

        if len( l_dynJoints )== 0:
            return
        
        # --- Bake / Unbake
        if in_mode == 'bake':
            animation.bake_Objects( in_Obj_list= l_dynJoints )
            attr_bake= True
            attr_on_off= 0
        elif in_mode == 'unbake':
            animation.unbake_Objects( in_Obj_list= l_dynJoints )
            attr_bake= False
            attr_on_off= 1

        # Update Attributs            
        for s_item in l_global_name:
            # ON OFF Attr
            mc.setAttr( s_item+ '.on_off', attr_on_off )
            # Bake Attr
            mc.setAttr( s_item+ '.dynamicJoints_bake', attr_bake )
            # IK_Blend
            l_IKHandle = connection.get_MessageConnection_Ouput( inObj=  s_item, inAttr= 'dynSys_IKHandle' )
            for s_IKHandle in l_IKHandle:
                mc.setAttr( s_IKHandle+ '.ikBlend', attr_on_off )
                
        print '--> ' + in_mode + ' done'

        # --- Update UI
        if not externalRun:
            self.update_datas_UI()

    #----------------------------------------------------------------------
    def get_dynamic_system_datas( self, *args):
        '''
        Return a dictionnary who list the hair System build with the Dyn System tool of the current scene
        Filtered by nameSpace with the dynSys state as value
        
        :rtype : dictionnary
        
        return dictionnary example::
            
            { 
            'noNameSpaceDynSytem': 
                { 
                    'noNameSpaceDynSytem': 2
                },
            'nameSpace': 
                { 
                    'nameSpace:Dynamics_System1': 1,
                    'nameSpace:Dynamics_System2': 1
                }
            }
        '''
        d_return = dict()

        # --- Get all dyn sys
        l_dynamic_system = mc.ls( type= 'hairSystem' )

        for s_dynamic_system in l_dynamic_system:
            # --- Get only valid Dyn System
            if mc.objExists( s_dynamic_system + '.dynSystem' ) and mc.objExists( s_dynamic_system + '.globalCtrl' ):
                # --- Get the state of the Dyn enable/disable
                b_state = mc.getAttr( connection.get_MessageConnection_Input( s_dynamic_system, 'globalCtrl') + '.on_off' )
                b_bake = mc.getAttr( connection.get_MessageConnection_Input( s_dynamic_system, 'globalCtrl') + '.dynamicJoints_bake' )

                # Define state
                if not b_bake:
                    i_state = b_state
                else:
                    i_state = 2

                # --- Filter by nameSpace
                l_splitName = s_dynamic_system.split(':')

                if len( l_splitName ) == 2:
                    # nameSpace
                    s_nameSpace = l_splitName[0]
                else:
                    # no nameSpace
                    s_nameSpace = s_dynamic_system

                # --- Insert datas in return dictionnary
                if not s_nameSpace in d_return.keys():
                    d_return[ s_nameSpace ] = {}
                d_return[ s_nameSpace ][ s_dynamic_system ] = i_state

        return d_return
