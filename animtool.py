__author__ = 'f.scaduto'

import maya.cmds as cmds
import sys

def copyWS():
    '''
    Copy WorldSpace position and query it in floatField
    :return:
    '''
    copyTrans = cmds.checkBox('cbTrans', q=1, v=1)
    copyRot = cmds.checkBox('cbRot', q=1, v=1)
    objToCopy = cmds.ls(sl=1)
    if objToCopy[0] == "":
        cmds.error("Select the Source")

    wsPos = cmds.xform(objToCopy[0], q=1, ws=1, t=1)
    wsRot = cmds.xform(objToCopy[0], q=1, ro=1, ws=1)
    # Query Translations in floatField
    if copyTrans == 1:
        cmds.floatField('wsXPos', e=1, v=wsPos[0])
        cmds.floatField('wsYPos', e=1, v=wsPos[1])
        cmds.floatField('wsZPos', e=1, v=wsPos[2])

    # Query Rotations in floatField
    if copyRot == 1:
        cmds.floatField('wsXRot', e=1, v=wsRot[0])
        cmds.floatField('wsYRot', e=1, v=wsRot[1])
        cmds.floatField('wsZRot', e=1, v=wsRot[2])

    if copyRot == 0 and copyTrans == 0:
        cmds.error("Select a channel to Copy")


def pasteWS():
    '''
    Paste WorldSpace position from floatField queryed
    :return:
    '''
    copyTrans = cmds.checkBox('cbTrans', q=1, v=1)
    copyRot = cmds.checkBox('cbRot', q=1, v=1)
    objToPaste = cmds.ls(sl=1)
    if objToPaste[0] == "":
        cmds.error("Select the Target")

    # Paste Translations from floatField
    if copyTrans == 1:
        xPos = float(cmds.floatField('wsXPos', q=1, v=1))
        yPos = float(cmds.floatField('wsYPos', q=1, v=1))
        zPos = float(cmds.floatField('wsZPos', q=1, v=1))
        cmds.xform(objToPaste[0], ws=1, t=(xPos, yPos, zPos))

    # Paste Rotations from floatField
    if copyRot == 1:
        xRot = float(cmds.floatField('wsXRot', q=1, v=1))
        yRot = float(cmds.floatField('wsYRot', q=1, v=1))
        zRot = float(cmds.floatField('wsZRot', q=1, v=1))
        cmds.xform(objToPaste[0], ro=(xRot, yRot, zRot), ws=1)

    if copyRot == 0 and copyTrans == 0:
        cmds.error("Select a channel to Paste")


def lockCam():
    '''
    Unload CamRef, Lock file and Reload CamRef
    :return:
    '''
    camRef = 'CAM_aRN'
    # Lock CAM_aRN and kill popUp error (prompt flag)
    cmds.file(unloadReference=camRef)
    cmds.setAttr(camRef + '.locked', 1)
    cmds.file(loadReference=camRef, prompt=False)
    sys.stderr.write("%s is succefully Locked ! \n" % camRef)


def unlockCam():
    '''
    Unload CamRef, Unlock file and Reload CamRef
    :return:
    '''
    camRef = 'CAM_aRN'
    # Unlock CAM_aRN and kill popUp error (prompt flag)
    cmds.file(unloadReference=camRef)
    cmds.setAttr(camRef + '.locked', 0)
    cmds.file(loadReference=camRef, prompt=False)
    sys.stderr.write("%s is succefully Unlocked ! \n" % camRef)


def reset():
    '''
    Reset transform attribute
    :return:
    '''
    # Set default value attribute transform on selection
    attrDefaultValue = {'sx': 1, 'sy': 1, 'sz': 1, 'rx': 0, 'ry': 0, 'rz': 0, 'tx': 0, 'ty': 0, 'tz': 0}

    sel = cmds.ls(sl=1)
    for obj in sel:
        for attr in attrDefaultValue:
            try:
                cmds.setAttr('%s.%s' % (obj, attr), attrDefaultValue[attr])
            except:
                pass
