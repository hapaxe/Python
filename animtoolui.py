__author__ = 'f.scaduto'

import maya.cmds as cmds
import animtool as animtool

def main():
    '''
    Create window
    :return:
    '''
    if cmds.window("animToolWin", ex=True):
        cmds.deleteUI("animToolWin", window=True)

    cmds.window("animToolWin", wh=(200, 100), t="Anim Tool Stella", s=False)

    cmds.columnLayout(adj=True)
    ''' # Cam buttons not needed
    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')

    cmds.separator(style='none', height=8)

    cmds.text(l="Lock / Unlock Cam")

    cmds.separator(style='none', height=8)

    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')

    cmds.rowColumnLayout(numberOfColumns=2,
                         columnWidth=[(1, 107), (2, 107)])

    cmds.button(l="Lock", command="animtoolui.animtool.lockCam()")
    cmds.button(l="Unlock", command="animtoolui.animtool.unlockCam()")

    cmds.setParent('..')

    cmds.separator(style='none', height=8)
    '''

    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')
    cmds.separator(style='none', height=5)

    cmds.text(l="Copy and Paste World position")

    cmds.separator(style='none', height=8)

    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')

    cmds.separator(style='none', height=8)

    cmds.rowColumnLayout(numberOfColumns=4,
                         columnWidth=[(1, 45), (2, 70), (3, 1), (4, 60)])

    cmds.separator(style='none', height=5)
    cmds.checkBox('cbTrans', label="Translate")
    cmds.separator(style='none', height=5)
    cmds.checkBox('cbRot', label="Rotate")

    cmds.setParent('..')

    cmds.separator(style='none', height=8)

    cmds.rowColumnLayout(numberOfColumns=4,
                         columnWidth=[(1, 21), (2, 70), (3, 32), (4, 70)])
    cmds.separator(style='none', height=5)
    cmds.text(al="center", l="Select Source")
    cmds.separator(style='none', height=5)
    cmds.text(al="center", l="Select Target")

    cmds.setParent('..')

    cmds.separator(style='none', height=4)

    cmds.rowColumnLayout(numberOfColumns=2,
                         columnWidth=[(1, 107), (2, 107)])

    cmds.button(command=lambda *args: animtool.copyWS(), l="Copy")
    cmds.button(command=lambda *args: animtool.pasteWS(), l="Paste")

    cmds.setParent('..')

    cmds.separator(style='none', height=10)
    cmds.separator(w=190, height=5, style='in')

    cmds.rowColumnLayout(numberOfColumns=4,
                         columnWidth=[(1, 18), (2, 65), (3, 65), (4, 65)])

    cmds.separator(style='none', height=5)
    cmds.text(al="center", l="X", vis=True)
    cmds.text(al="center", l="Y", vis=True)
    cmds.text(al="center", l="Z", vis=True)

    cmds.text(al="center", l="T", vis=True)
    cmds.floatField('wsXPos', vis=True, editable=False)
    cmds.floatField('wsYPos', vis=True, editable=False)
    cmds.floatField('wsZPos', vis=True, editable=False)
    cmds.text(al="center", l="R", vis=True)
    cmds.floatField('wsXRot', vis=True, editable=False)
    cmds.floatField('wsYRot', vis=True, editable=False)
    cmds.floatField('wsZRot', vis=True, editable=False)

    cmds.setParent('..')
    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')
    cmds.separator(style='none', height=5)

    cmds.text(l="Reset attribut")

    cmds.separator(style='none', height=8)

    cmds.separator(w=190, height=5, style='in')
    cmds.separator(w=190, height=5, style='in')

    cmds.button(l="Reset", command="animtoolui.animtool.reset()")

    cmds.separator(style='none', height=8)

    cmds.showWindow("animToolWin")
