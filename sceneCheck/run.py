#----------------------------------------------------------------------
# sceneCheck run
# Author : felixlechA.com | f.rault
# Date   : February 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
import sceneCheck
reload(sceneCheck)
import functions.clean as clean
reload(clean)
from functions.general import viewPrint

def convert_scene_Layout_to_Aniamtion( force_state, set_firstKey= True):
    '''
    Convert current layout scene to Aniamtion scene
    Analyse Assembly and change animate one to Reference
    Keep animation
    Keep Assembly for BG noAnimate elements

    :param force_state: Define the state to force the ref load
    :type force_state: string

    :param set_firstKey: Set a first animation key on all CH and PR ctrls
    :type set_firstKey: boolean

    :return: None
    '''
    print '-----'
    print 'Conversion Scene Layout to Animation :'

    # - Set cursor disable
    mc.waitCursor( state=True )

    # --- Get scene Assembly info
    infoDict = sceneCheck.get_AssemblyInfo()

    # --- Get Assembly to Switch as ref
    toSwitch = sceneCheck.get_AssemblyToSwitchAsRef( infoDict, force_state= force_state )

    # --- Duplicate animCurve
    sceneCheck.duplicate_animCurve( toSwitch )

    # --- Switch Assembly to Ref - Force setupLOD2 if exist
    ctrlsRef = sceneCheck.switch_assembly_to_ref( toSwitch )

    # --- Reconnect animation
    sceneCheck.reconnect_animCurve( ctrlsRef )

    # --- Set Fisrt key on all Ctrls
    if set_firstKey:
        sceneCheck.set_firstKey( ctrlsRef )

    # --- CLEAN Scene
    sceneCheck.extraClean()

    # - Remove unused animation Curve
    clean.unused_animCurve_remove()

    # - Remove unknow noReferenced nodes
    clean.unknowNodes_remove()

    # - Remove unused hyperView
    clean.unused_hyperView_remove()

    # - Remove useless scriptNode
    clean.useless_scriptNode_remove()

    # - Remove fosterParent
    clean.fosterParent_remove()

    # - Set cursor enable
    mc.waitCursor( state=False )

    # - Display in View message
    viewPrint( msg= 'Scene converted. \n<hl>Ready to Animation</hl>',mode= 1 )

    print '-----'


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class convert_Layout_to_Aniamtion():
    def __init__( self ):
        '''
        init Class
        '''
        self.widgets = {} # Dictionnary who store the tool's UI

    #----------------------------------------------------------------------
    def UI( self, *args ):
        '''
        The convert scene Layout to Aniamtion UI
        '''
        # --- Check existing Windows
        if mc.window('convert_toAnimScene_Window', exists=True ):
            mc.deleteUI( 'convert_toAnimScene_Window', window=True )

        # --- Create window
        self.widgets['win'] = mc.window('convert_toAnimScene_Window', title='Convert Scene Layout to Animation', w= 200, sizeable= False )

        self.widgets['win_col'] = mc.columnLayout( adj= True )
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, bgc=[0.433, 0.286, 0.0], l='Convert Layout > Animation', cll= False )

        self.widgets['force_state'] = mc.checkBox( label='Force setupLOD2', v= False )
        self.widgets['set_firstKey'] = mc.checkBox( label='Set the first animation key', v= False )

        self.widgets['win_bt_launch'] = mc.button(l='Convert', height= 30, c= self.launch )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):

        force_state = mc.checkBox( self.widgets['force_state'], q=True, v=True )
        set_firstKey = mc.checkBox( self.widgets['set_firstKey'], q=True, v=True )

        if force_state:
            force_state= 'setupLOD2'
        else:
            force_state= None

        convert_scene_Layout_to_Aniamtion( force_state= force_state, set_firstKey= set_firstKey )
