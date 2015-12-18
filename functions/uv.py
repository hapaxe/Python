#----------------------------------------------------------------------
# functions uv
# Author : felixlechA.com | f.rault
# Date   : Janury 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Transfer_UV():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'transfert_UV_Window'
        self.tool_title= 'transfert UV settings'
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

        self.widgets['menu_sampleSpace'] = mc.optionMenu( label=' Define sample Space' )
        for sample_space in [ 'World', 'Local', 'Component', 'Topology' ]:
            mc.menuItem( self.widgets['menu_sampleSpace'], label = sample_space )
        # Select 'Component-based' by default
        mc.optionMenu( self.widgets['menu_sampleSpace'], edit= True, select= 3  )

        self.widgets['win_bt_launch'] = mc.button(l='Launch Copy UV', height= 30, c= self.launch )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def launch( self, *args ):

        menu_sampleSpace = mc.optionMenu( self.widgets['menu_sampleSpace'], q=True, value=True )

        if menu_sampleSpace == 'World':
            sampleSpace= 0
        elif menu_sampleSpace == 'Local':
            sampleSpace= 1
        elif menu_sampleSpace == 'Component':
            sampleSpace= 4
        elif menu_sampleSpace == 'Topology':
            sampleSpace= 5

        transfer_uv( source= '', target= '', sampleSpace= sampleSpace, sourceUvSpace= 'map1', targetUvSpace= 'map1' )

#----------------------------------------------------------------------
def transfer_uv( source= '', target= '', sampleSpace= 4, sourceUvSpace= 'map1', targetUvSpace= 'map1' ):
    '''
    Transfer UV from one Geo to a Other rigged or not, without add history ;)

    :param source: the object source UV name
    :type source: string

    :param target: the object target name
    :type target: string

    :param sourceUvSpace: Define the source's UvSpace to used default 'map1'
    :type sourceUvSpace: string

    :param targetUvSpace: Define the target's UvSpace to used default 'map1'
    :type targetUvSpace: string

    :return: none
    '''
    if not source and not target:
        sel= mc.ls( selection=True ) or []

        if len(sel) == 0:
            viewPrint( msg= 'Select a source and a target Geometry to launch the Transfert UV', mode= 2 )
            return
        else:
            source= sel[0]
            target= sel[1]

    # --- Get the Orig shapes of target
    shapes= mc.listRelatives( target, s= True )

    # --- Set the mode to No intermediate by default
    intermediate= False

    # --- If multiple shapes search intermediate Origine shapes
    if len(shapes) > 1:
        if mc.getAttr( shapes[1] +'.intermediateObject' ) and 'Orig' in shapes[1]:
            # Turn intermediate mode Active
            intermediate= True
            # Overwrite target by this intermediate shape
            target= shapes[1]

            # Turn the Intermediate Object to False
            mc.setAttr( target +'.intermediateObject', False)

    # --- Transfer UV
    mc.transferAttributes( source, target,
        transferPositions= False, transferNormals= False,
        transferUVs= 2, transferColors= 2, sampleSpace= sampleSpace,
        sourceUvSpace= sourceUvSpace, targetUvSpace= targetUvSpace,
        searchMethod= 3, flipUVs= False, colorBorders= True )

    # --- Delete Construction History on target
    mc.delete( target, constructionHistory=True)

    # --- Toggle the Intermediate Object to True
    if intermediate:
        mc.setAttr( target +'.intermediateObject', True )

    viewPrint( msg= 'UV successfully transferred to target mesh', mode= 0 )
