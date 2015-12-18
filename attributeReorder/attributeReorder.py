#----------------------------------------------------------------------
# Attribute Reorder
# Author : felixlechA.com
# Date   : April 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
from functools import partial
import os

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AttributeReorder():
    def __init__( self ):
        '''
        init Class
        '''
        # define the path of the UI file
        self.filePath_ui= os.path.split( os.path.realpath(__file__))[0] + '/attributeReorder.ui'
        self.form_name= 'AttributeReorderWindows'
        self.layout_name= 'ChannelsLayersPaneLayout'
        
    def UI( self, *args ):
        '''
        Build UI

        :return: none
        '''  
        # Clean Previous Layout
        if mc.formLayout( self.form_name, exists=True ):
            self.delete_UI( layout_name= self.form_name )
    
        # Edit the channelBox Layout
        if mc.paneLayout( self.layout_name, configuration= True, query= True) == 'horizontal2':
            mc.paneLayout( self.layout_name, edit= True, configuration=  'horizontal3' )
            mc.paneLayout( self.layout_name, edit= True, setPane= ['LayerEditorForm', 3] )
    
        # Build the Layout
        mc.formLayout( self.form_name, numberOfDivisions= 100, p= self.layout_name )
        b1= mc.button( l= 'Refresh', w= 100, h= 18, c= self.refresh )
        b2= mc.button( l= 'Reorder', w= 100, h= 18, c= self.reorder )
        b3= mc.button( l= 'X', w= 20, h= 18, c= partial( self.delete_UI, self.form_name ))
    
        # Get the ui form file .ui
        Scroll= mc.loadUI( uiFile= self.filePath_ui )
    
        # Reparent the scrollList to the channelBox Layout
        mc.showWindow( Scroll )
        mc.window( Scroll, edit= True, vis= 0, wh= [10, 10], tlc= [0, 0] )
        mc.textScrollList( 'ScrollListAttrReor', edit= True, p= self.form_name )
        mc.deleteUI( Scroll, wnd= True )
    
        # Set the Layout form
        mc.formLayout( self.form_name, edit= True, attachForm= [ (b1, 'top', 5), (b1, 'left', 5), (b2, 'top', 5), (b3, 'right', 5), (b3, 'top', 5), ('ScrollListAttrReor', 'left', 5), ('ScrollListAttrReor', 'right', 5), ('ScrollListAttrReor', 'bottom', 5) ], attachControl= [ (b2, 'left', 5, b1), (b2, 'right', 5, b3), ('ScrollListAttrReor', 'top', 5, b1) ] )
    
        # Populate textScrollList Attributes
        self.refresh()


    def refresh( self, *args ):
        '''
        refresh the Attributes list

        :return: none
        '''
        # remove All in the textScrollList
        mc.textScrollList( 'ScrollListAttrReor', edit= True, removeAll= True )
    
        # get Object display in channelBox    
        channelBox_objects= mc.channelBox( 'mainChannelBox', mainObjectList= True, query= True)
    
        if channelBox_objects:
            attributes= mc.listAttr( channelBox_objects[0], userDefined= True )
    
            if attributes:
                for attribute in attributes:
                    mc.textScrollList( 'ScrollListAttrReor', edit= True, append= attribute )
    
    
    def delete_UI( self, layout_name, *args ):
        '''
        delete the Tool UI from channelBox

        :param layout_name: name of the Layout toi delete
        :type layout_name: basestring

        :return: none
        '''
        mc.deleteUI( layout_name, lay= True )
        mc.paneLayout( 'ChannelsLayersPaneLayout', edit= True, setPane= ['LayerEditorForm', 2] )
        mc.paneLayout( 'ChannelsLayersPaneLayout', edit= True, configuration=  'horizontal2' )
    
    
    def reorder( self, *args ):
        '''
        reBuild Attributes order

        :return: none
        '''
        channelBox_objects= mc.channelBox( 'mainChannelBox', mainObjectList= True, query= True)
        attributes= mc.textScrollList( 'ScrollListAttrReor', q= True, allItems= True )
        
        if not channelBox_objects or not attributes:
            return
        
        for object in channelBox_objects:
            for attribute in attributes:
                if mc.objExists( object +"."+ attribute ):
                    if mc.getAttr( object +"."+ attribute, lock= True ):
                        mc.setAttr( object +"."+ attribute, lock= False )
                        try:
                            mc.deleteAttr( object +"."+ attribute )
                        except:
                            print e
                        mc.undo()
                        mc.setAttr( object +"."+ attribute, lock= True )
                    else:
                        try:
                            mc.deleteAttr( object +"."+ attribute )
                        except:
                            print e
                        mc.undo()
        
        mc.refreshEditorTemplates()
