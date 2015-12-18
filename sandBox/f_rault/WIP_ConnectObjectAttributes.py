#----------------------------------------------------------------------
# connect Object Attributes
# Author : felixlechA.com
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ConnectObjectAttributes():
    '''
    Tool to connect Object Attributes
    '''
    
    def __init__( self ):
        '''
        init Class
        '''
        self.widgets = {} # Dictionnary who store the tool's UI
        self.datas = self.get_selection_datas()

    def UI():
        '''
        Create the UI
        '''
        if mc.window('connectObjectAttributesWindow', exists=True ):
            mc.deleteUI( 'connectObjectAttributesWindow', window=True )
        
        # Get the existing Hair System
        lHairSys = ['New_Hair_System']
        lHairSys.extend( mc.ls( type= 'hairSystem' ) )
        
        # ---
        # Create window
        widgets['win'] = mc.window('createDynamicChaineWindow', title='Create Dynamic Chain', w=300, h=450)
        
        # Top Frame
    
        widgets['topFrame'] = mc.frameLayout(l='init Parameters', w=300)
        widgets['topColumn'] = mc.columnLayout()
    
        # Object selection area
        widgets['jntName'] = mc.textFieldButtonGrp(l="1. Get fisrt Joint ", cal= [ (1, 'left'), (2, 'center'), (3, 'right') ], cw3=[120, 150, 40], ed=False, bl='<', annotation='Get the first joint of the chain you want to convert to Dynamic.', bc= partial( Pick_Object, 'joint', 'jntName' ) )
    
        # Define Dyn Chain Name
        widgets['baseName'] = mc.textFieldGrp(l='2. Define Chain name : ', cl2= [ 'left', 'right' ], cw2= [ 120, 170], text='', annotation='')
        
        # go Back to Window
        mc.setParent(widgets['win'])
        
        # scroll Frame
        widgets['scrollFrame'] = mc.frameLayout(l='Hair System', w=300)
        widgets['scrollColumn'] = mc.columnLayout()
        widgets['textDynList'] = mc.text( l='3. Select Hair System' )
        widgets['dynList'] = mc.textScrollList( allowMultiSelection= False, append= lHairSys, selectItem= 'New_Hair_System', showIndexedItem= 1, w= 300, h= 150, annotation='Select the hair system to use.', sc=Update_dynName )
        
        # go Back to Window
        mc.setParent(widgets['win'])
        
        # Dyn System Name Frame
        widgets['dynNameFrame'] = mc.frameLayout(l='Dynamic System Frame', lv=False, w=300)
        widgets['dynNameColumn'] = mc.columnLayout()
            
        # Define Dyn Name
        widgets['dynName'] = mc.textFieldGrp(l='4. System dynamic name : ', cl2= [ 'left', 'right' ], cw2= [ 120, 170], text='', annotation='The hair system name')
        widgets['ctrlGlobal'] = mc.textFieldButtonGrp(l="5. Get Global Ctrl ", cal= [ (1, 'left'), (2, 'center'), (3, 'right') ], cw3=[120, 150, 40], ed=False, bl='<', annotation='Get the curve who became the global Control of the dynamic system.', bc= partial( Pick_Object, 'transform', 'ctrlGlobal' ) )
        
        # go Back to Window
        mc.setParent(widgets['win'])
        widgets['buttonFrame'] = mc.frameLayout(l='Button Frame', lv=False, w=300)
        widgets['buttonColumn'] = mc.rowLayout( numberOfColumns=2 )
        widgets['refreshButton'] = mc.button(l='Refresh UI', w=75, h=40, c= ui_refresh )
        widgets['createButton'] = mc.button(l='Create Dynamic Chain', w=215, h=40, c= Create_DynamicSystem )
    
        widgets['previousHairSys'] = 'New_Hair_System'
        widgets['validHairSys'] = True
        
        # Show window
        mc.showWindow(widgets['win'])