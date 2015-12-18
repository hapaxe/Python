import maya.cmds as cmds
import maya.mel as mel
import sys, time, traceback
sys.path.append(r"\\netapp\shared_workflow\Workflow\maya2012_workgroup\scripts\python")
import mayaExporter

def preview_tool():
    # Locals
    camRef = 'CAM_aRN'
    # Ask User
    result = cmds.confirmDialog( title='Confirmation', message='Make Preview?', button=['Yes','No'], defaultButton='Yes', cancelButton='Yes', dismissString='No' )
    # If Yes
    if result=='Yes':
        # If camRef present in scene
        if cmds.ls(camRef):
            # Store Camera lock state
            stored_cam_islocked = cmds.getAttr(camRef + '.locked')
            # Unlock CAM_aRN and kill popUp error (prompt flag)
            cmds.file(unloadReference=camRef)
            cmds.setAttr(camRef+'.locked',0)
            cmds.file(loadReference=camRef, prompt=False)
            # Save Current Layout
            temp_layout = cmds.panelConfiguration(l='tempLayout', sc=0)
            mel.eval('updatePanelLayoutFromCurrent "tempLayout"')
            # Set Layout 'Single Perspective View'
            mel.eval('setNamedPanelLayout "Single Perspective View"')
            # Get Panel 0
            model_panel = cmds.getPanel(vis=1)[0]
            # Give Focus
            cmds.setFocus(model_panel)
            # Set Camera On Panel
            mel.eval('lookThroughModelPanel("CAM_a:finalShape", "%s")' %model_panel)
            # Set ViewPort 2.0
            mel.eval("ActivateViewport20();")
            # Message Box to avoid crash
            cmds.confirmDialog(title='Continue', message='Continue', button=['Yes'], defaultButton='Yes')
            #mel.eval('setRendererInModelPanel("vp2Renderer", "%s")' %model_panel) BUG !!
            # Set Use All Light
            cmds.modelEditor(model_panel,edit=1,dl="all")
            # Set Shadows On
            cmds.modelEditor(model_panel,shadows=True,e=1)
            # Set ambiantOclusion active on ViewPort 2.0
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable",1)
            # Set Antialisaing
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
            # Make Preview (no batch)
            mayaExporter.makePreview3()
            # Restore Lock State on camRef
            cmds.file(unloadReference=camRef)
            cmds.setAttr(camRef+'.locked',stored_cam_islocked)
            cmds.file(loadReference=camRef, prompt=False)
            # Restore Standard Viewport
            mel.eval("setRendererInModelPanel base_OpenGL_Renderer %s;" %model_panel)
            # Disable on ViewPort 2.0
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable",0)
            # Disable Antialisaing
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable",0)
            # Restore Layout
            mel.eval('setNamedPanelLayout "tempLayout"')
            # Get Layout to Delete
            temp_layout = cmds.getPanel(cwl='tempLayout')
            # Delete it
            cmds.deleteUI(temp_layout, pc=1)
        # camRef Not Present
        else:
            # Prompt User
            cmds.confirmDialog(title='Alert', message='You dont have the camera : %s' %camRef, button=['Ok'], defaultButton='Ok')