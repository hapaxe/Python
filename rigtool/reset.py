#----------------------------------------------------------------------
# rigtool reset
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Decription : Reset Attributs functions
#----------------------------------------------------------------------
import maya.cmds as mc
from functions.general import viewPrint

#----------------------------------------------------------------------
def set_Attributes( obj_list= None ):
    '''
    Set reset Attributes on attributes keyable and displayed in channelBox
    reset Attributes created are name like base attribute '_reset' and have a reset category

    Transform Attributes :
    Create a reset attribute and store current value only if current isn't 0 for Translate and Rotate and isn't 1 for Scaling

    Extra Attribute :
    Create a reset attribute for each and store the current value

    :param obj_list: List of object to set reset Attribute, Get current selection if not define
    :type obj_list: list

    :return: None
    '''
    # --- List objects
    if not obj_list:
        obj_list = mc.ls(sl= True)

    for item in obj_list:
        # --- Get All reset Attributes
        attributes_all = mc.listAttr( item ) or list()
        # --- Get Keyable Attributes from channelBox
        attributes_chBox = mc.listAttr( item, k=True ) or list()
        attributes_display = mc.listAttr( item, cb= True ) or list()

        # --- Clean joint Radius parameter
        if mc.objectType( item ) == 'joint' and 'radius' in attributes_display:
            mc.setAttr( item +'.radius', channelBox= False )

        # --- Hide visibility attribute from channelBox
        if 'visibility' in attributes_chBox:
            mc.setAttr( item +'.visibility', keyable= False, channelBox= False )

        # --- Remove All previous Reset Value
        for attr in attributes_all:
            if '_reset' in attr and not attr in attributes_chBox:
                mc.setAttr( item + '.' + attr, lock=False )
                mc.deleteAttr( item + '.' + attr )

        # --- Create Reset Attributes
        for attr in attributes_chBox:
            # - Pass if attribut is locked
            if mc.getAttr( item + '.' + attr, lock=True ) or attr == 'visibility':
                continue

            value = mc.getAttr( item +'.'+ attr )

            # --- Pass next if Attribute is a Transform and this value isn't custom
            if (attr in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ'] and value == 0) or (attr in ['scaleX', 'scaleY', 'scaleZ'] and value == 1):
                continue

            # --- Create, Set and lock Attribute
            mc.addAttr( item, ln= attr +'_reset', at='float', dv= value, k= False, category= 'reset')
            mc.setAttr( item + '.' + attr +'_reset', lock=True )

    if obj_list:
        logMsg =  'Reset Attributes done on <hl>'+ str(len(obj_list)) + '</hl> objects'
    else:
        logMsg =  '<hl>no</hl> given objects to reset Attributes\n> select some Objects to run'
    viewPrint( msg= logMsg, mode=1 )

#----------------------------------------------------------------------
def all_Attributes():
    '''
    Reset All keyable Attributes of selected objects based on reset values

    :return: None
    '''
    #--- Get current selection
    cSel = mc.ls(sl= True)

    for item in cSel:
        #--- Get All Attributes
        attributes_reset = mc.listAttr( item, category= 'reset' ) or list()
        #--- Get Keyable Attributes can be Reset
        attributes_chBox = mc.listAttr( item, k=True ) or list()

        #--- Reset Attributes
        for attr in attributes_chBox:
            # - Pass if attribut is locked
            if mc.getAttr( item + '.' + attr, lock=True ):
                continue

            if attr + '_reset' in attributes_reset:
                reset_value = mc.getAttr( item +'.'+ attr + '_reset' )
                mc.setAttr( item +'.'+ attr, reset_value )
            elif attr in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']:
                mc.setAttr( item +'.'+ attr, 0 )
            elif attr in ['scaleX', 'scaleY', 'scaleZ']:
                mc.setAttr( item +'.'+ attr, 1 )

#----------------------------------------------------------------------
def active_Transform():
    '''
    Reset All keyable Attributes of selected objects based on reset values

    If a Transform mode is active Reset only this current Transform

    :return: None
    '''
    #--- Get current selection
    cSel = mc.ls(sl= True)

    #--- Get current transform mode
    currentCtx = mc.currentCtx()

    for item in cSel:
        #--- Get All Attributes
        attributes_reset = mc.listAttr( item, category= 'reset' ) or list()
        #--- Get Keyable Attributes can be Reset
        attributes_chBox = mc.listAttr( item, k=True )

        #--- Filter Attributes to Reset
        toReset= list()
        if currentCtx == 'moveSuperContext':
            for attr in ['translateX', 'translateY', 'translateZ']:
                if attr in attributes_chBox:
                    toReset.append( attr )
        elif currentCtx == 'RotateSuperContext':
            for attr in ['rotateX', 'rotateY', 'rotateZ']:
                if attr in attributes_chBox:
                    toReset.append( attr )
        elif currentCtx == 'scaleSuperContext':
            for attr in ['scaleX', 'scaleY', 'scaleZ']:
                if attr in attributes_chBox:
                    toReset.append( attr )
        else:
            toReset.extend( attributes_chBox )

        #--- Reset Attributes
        for attr in toReset:
            if attr + '_reset' in attributes_reset:
                reset_value = mc.getAttr( item +'.'+ attr + '_reset' )
                mc.setAttr( item +'.'+ attr, reset_value )
            elif attr in ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']:
                mc.setAttr( item +'.'+ attr, 0 )
            elif attr in ['scaleX', 'scaleY', 'scaleZ']:
                mc.setAttr( item +'.'+ attr, 1 )
