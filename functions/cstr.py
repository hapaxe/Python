#----------------------------------------------------------------------
# functions cstr
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc

#----------------------------------------------------------------------
def constraint( source, target, mode= ['translate', 'rotate', 'scale']):
    '''
    Create cstr inbetween two given objects

    :param source: the Source object name
    :type source: string

    :param target: the Target object name
    :type target: string

    :param mode: Define the cstr Mode ['translate', 'rotate', 'scale'] by default cstr All transform
    :type mode: list

    :return: none
    '''

    # - Do parent Cstr
    if 'translate' in mode or 'rotate' in mode:
        # - Parent Cstr Filter
        cstr_name= '_parent'
        if 'translate' in mode and 'rotate' in mode:
            skipTranslate= 'none'
            skipRotate= 'none'
            cstr_name+= '_TR'
        elif 'translate' in mode:
            skipTranslate= 'none'
            skipRotate= ('x','y','z')
            cstr_name+= '_T'
        elif 'rotate' in mode:
            skipTranslate= ('x','y','z')
            skipRotate= 'none'
            cstr_name+= '_R'
        cstr_name+= '_cstr'

        mc.parentConstraint( source, target, name= target + cstr_name, skipTranslate= skipTranslate, skipRotate= skipRotate, maintainOffset= True )

    # - Do scale Cstr
    if 'scale' in mode:
        cstr_name = '_scale_cstr'
        mc.scaleConstraint( source, target, name= target + cstr_name, maintainOffset= True )