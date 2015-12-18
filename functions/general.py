#----------------------------------------------------------------------
# functions general
# Author : felixlechA.com | f.rault
# Date   : Janury 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc

#----------------------------------------------------------------------
def viewPrint( msg, mode=0, pos='topLeft', fade=True ):
    '''
    Display inViewMeassage with a prefixe

    mode
    0 = normale
    1 = info
    2 = warning
    3 = error

    :param msg: The message
    :type msg: string

    :param mode: Define the mode who add prefix
    :type mode: integer

    :param pos: Define the position in viewport to display the message. Show 'inViewMessage' maya documentation to other values
    :type pos: string

    :param fade: Fade or not the message
    :type fade: boolean

    :return: none
    '''
    if mode == 0:
        mc.inViewMessage( msg=msg, pos=pos, fade=fade )
    elif mode == 1:
        mc.inViewMessage( msg='<span style=\"color:#82C99A;\">Info : </span>' + msg, pos=pos, fade=fade )
    elif mode == 2:
        mc.inViewMessage( msg='<span style=\"color:#F4FA58;\">Warning : </span>' + msg, pos=pos, fade=fade )
    elif mode == 3:
        mc.inViewMessage( msg='<span style=\"color:#F05A5A;\">Error : </span>' + msg, pos=pos, fade=fade )

#----------------------------------------------------------------------
def manageSet( mode, use_mode= 'command' ):
    '''
    Manage Set, Select object to manage and select last the set

    :param mode: Define the mode 'REMOVE' or 'ADD'
    :type mode: string
    '''
    # Get Selection and filter
    cSel = mc.ls(sl= True)

    # - Check Selection
    if cSel:
        if len(cSel) < 2:
            if use_mode == 'shelf':
                viewPrint( 'Select objects and last a Set', mode= 1 )
            else:
                print 'Select objects and last a Set'
            return
    else:
        if use_mode == 'shelf':
            viewPrint( 'Select objects and last a Set', mode= 1 )
        else:
            print 'Select objects and last a Set'
        return

    # - Get Set
    set= cSel[-1]

    # - Test if set is a set
    if not mc.nodeType( set ) == 'objectSet':
        if use_mode == 'shelf':
            viewPrint( 'Last selected is not a Set', mode= 2 )
        else:
            print 'Last selected is not a Set'
        return

    # - Get Item to Add or Remove
    items= cSel[0:-1]

    if mode == 'REMOVE':
        # Remove object from a set
        mc.sets( items, rm= set )
    elif mode == 'ADD':
        # Add to Set
        mc.sets( items, fe= set )
