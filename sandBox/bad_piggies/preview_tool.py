__author__ = 'f.scaduto'

import maya.cmds as mc
import maya.mel as mel
import time
import mayaExporter

def badpiggies_make_preview(cameraScene):
    # Locals
    cam = cameraScene
    # Ask User
    result = mc.confirmDialog( title='Confirmation', message='Make Preview?', button=['Yes','No'], defaultButton='Yes', cancelButton='Yes', dismissString='No' )
    # If Yes
    if result=='Yes':
        # If camRef present in scene
        if mc.ls(cam):
            # Kill window if already exist
            if mc.window('MakePreviewWin', exists=1):
                mc.deleteUI('MakePreviewWin')
            # Create window
            mc.window('MakePreviewWin', t="MakePreview Window 2.0", wh=(960, 540))
            # Kill windowPref if exist
            if mc.windowPref('MakePreviewWin', exists=1):
                mc.windowPref('MakePreviewWin', remove=1)
            # Create paneLayout
            mc.paneLayout()
            # Show Window
            mc.showWindow('MakePreviewWin')
            # Create new model panel with cam set view in
            activePanel = str(mc.modelPanel(l="makePreview_panel", camera=cam))
            # Set displayAppearance to smoothShaded
            mc.modelEditor(activePanel,edit=1,displayAppearance='smoothShaded',activeOnly=False)
            # Set displayTexture
            mc.modelEditor(activePanel,e=1,displayTextures=True)
            # If nurbsCurves Active
            if mc.modelEditor(activePanel, q=1, nurbsCurves=1) == 1:
                mc.modelEditor(activePanel, e=1, nurbsCurves=0)
            # Give Focus
            mc.setFocus(activePanel)
            # Set ViewPort 2.0
            mel.eval("ActivateViewport20();")
            # Set Use All Light
            #mc.modelEditor(activePanel,edit=1,dl="all")
            # Set Shadows On
            #mc.modelEditor(activePanel,shadows=True,e=1)
            # Set ambiantOclusion active on ViewPort 2.0
            mc.setAttr("hardwareRenderingGlobals.ssaoEnable",1)
            # Screen space ambient occlusion setings
            mc.setAttr("hardwareRenderingGlobals.ssaoAmount",1.3)
            mc.setAttr("hardwareRenderingGlobals.ssaoRadius",45)
            mc.setAttr("hardwareRenderingGlobals.ssaoFilterRadius",16)
            mc.setAttr("hardwareRenderingGlobals.ssaoSamples",32)
            # Set Antialisaing
            mc.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
            # Message Box to avoid crash
            cntinue = mc.confirmDialog(title='Continue', message='Continue? :)', button=['Yes','No'], defaultButton='Yes', dismissString='No')
            # If cntinue
            if cntinue == 'Yes':
                # Message Box to desactivate ambianteOclu or not
                ambOcl = mc.confirmDialog(title='Ambiant Occlusion', message='Keep ambiant Occlusion Actual settings?', button=['Keep settings Active','Apply minimal settings','Desactivate Ambiant Occlusion'], defaultButton='Keep settings Active', dismissString='Desactivate Ambiant Occlusion')
                # If keep active
                if ambOcl == 'Keep settings Active':
                    pass
                if ambOcl == 'Apply minimal settings':
                    # Reduce screen space ambient occlusion setings
                    mc.setAttr("hardwareRenderingGlobals.ssaoAmount",0.2)
                    mc.setAttr("hardwareRenderingGlobals.ssaoRadius",30)
                if ambOcl == 'Desactivate Ambiant Occlusion':
                    # Desactivate ambiant Oclusion
                    mc.setAttr("hardwareRenderingGlobals.ssaoEnable",0)
                # Time sleep to avoid crash
                time.sleep( 2 )
                # Make Preview (no batch)
                mayaExporter.makePreview3()
            else:
                print "makePreview aborted !"

            # Kill UI mother fucker
            mc.deleteUI(activePanel, panel=True)
            mc.deleteUI('MakePreviewWin')

        # camRef Not Present
        else:
            # Prompt User
            mc.confirmDialog(title='Alert', message='You dont have the camera : %s' %cam, button=['Ok'], defaultButton='Ok')