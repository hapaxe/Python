#----------------------------------------------------------------------
# previz3d LO_ShotSetup
# Author : Julien Wieser
# reWrite : felixlechA.com | f.rault
# Date   : April 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm

import rigtool.defs as rigtool_defs
import functions.selection as selection

from tube_libraries import Tube
from MayaSceneManagerGeneric import MayaSceneManagerDialog

import os.path
from PySide.QtCore import *
from PySide.QtGui import *

#----------------------------------------------------------------------
def get_scene_manager():
    '''
    Get the Scene Manager

    :return: The first scene manager found
    :rtype: object instance
    '''
    # Get All widget
    for widget in QApplication.allWidgets():
        # Get First MayaSceneManagerDialog instance
        if isinstance(widget, MayaSceneManagerDialog):
            return widget

#----------------------------------------------------------------------
def get_shot_datas( sm ):
    '''
    Get datas from scene manger

    :param sm: Scene Manager instance
    :type sm: object instance

    :return:
    '''
    # Project name
    proj_text = sm.ui.project_comboBox.currentText()
    # Episode Full
    ep_text_full = sm.ui.episode_comboBox.currentText()
    # Episode
    ep_text = ep_text_full.split("_")[0]
    # Sequence
    seq_text = sm.ui.seq_comboBox.currentText()
    # Shot
    shot_text = sm.ui.plan_comboBox.currentText()

    if not proj_text== '' and not ep_text_full== 'ALL' and not seq_text== '' and not shot_text== '':
        return [ proj_text, ep_text_full, ep_text, seq_text, shot_text ]
    else:
        return None

#----------------------------------------------------------------------
def shot_setup():
    '''
    Setup Shot based on current SceneManger infos

    :return: none
    '''
    print '-----\nShot Setup :'
    # - Get scene Manager
    sm = get_scene_manager()

    # - Get Shot Datas
    shot_datas= get_shot_datas( sm )

    if shot_datas:
        name_ep= shot_datas[1]
        num_ep= shot_datas[2]
        num_seq= shot_datas[3]
        num_plan= shot_datas[4]
    else:
        print '---\nMissing infos to build Shot.\nCheck your SceneManager\n---\n '
        return


    # --- Set TIMELINE
    # - Get Shot Start/End frames
    with Tube() as tube:
        currentShot = tube.cursor.select('SELECT shot_startframe, shot_endFrame FROM Shot WHERE Shot.shot_id_proj= '+ str( sm.episode_id ) +' AND shot_id = '+ str( sm.shot_id ), None)
    timelineIN = currentShot[0]['shot_startframe']
    timelineOUT = currentShot[0]['shot_endFrame']
    mc.playbackOptions( animationStartTime= timelineIN, animationEndTime= timelineOUT, minTime= timelineIN, maxTime= timelineOUT )
    print '+ Timeline Set'


    # --- Check ROOT Grp
    log= 'Root Group :\n'
    grpDict= dict()

    # - ROOT FOLDER
    root_name= num_ep +'_'+ num_seq +'_'+ num_plan
    if mc.objExists('|e0*'):
        root = mc.ls('|e0*')[0]
        root= mc.rename( root, root_name )
        log+= '. Root grp already exist and is renamed\n'
    else:
        root= rigtool_defs.create_group( name= root_name )
        log+= '+ Root grp Created\n'

    grpDict['ROOT']= root

    for grp in ['BG_ROOT', 'CH_ROOT', 'PR_ROOT', 'CM_ROOT', 'AM_ROOT', 'LT_ROOT', 'MT_ROOT', 'GD_ROOT']:
        if not mc.objExists( '|' + root +'|'+ grp ):
            rigtool_defs.create_group( name= grp, parent= root )
            log+= '+ '+ grp +' Created'
        else:
            log+= '. '+ grp +' already exist'
        grpDict[grp]= grp
    print log


    # --- Import Sound
    # - Remove previous
    pm.runtime.DeleteAllSounds()

    # - Import current shot Sound
    SOUND_MAIN_PATH = os.path.expandvars( '$CUBE_PROJECT_DATAS\\episode\\'+ name_ep +'\\audio\\pPP' )
    SOUND_EXT = '.wav'
    Sound_Path = SOUND_MAIN_PATH +'\\'+ num_ep +'_'+ num_seq +'_'+ num_plan + SOUND_EXT
    audio_shot = pm.sound( offset=101, file= Sound_Path, name = 'audio_' + num_ep +'_'+ num_seq +'_'+ num_plan + SOUND_EXT )

    # - Show Sound in Timeline
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    pm.timeControl( aPlayBackSliderPython, e=True, sound=audio_shot, displaySound=True )
    print '+ Sound imported'


    # --- Animatic
    # - Get mov path
    VIDEO_MAIN_PATH = os.path.expandvars( '$CUBE_PROJECT_IMAGES\\episode\\'+ name_ep +'\\editing\\animatic2D\\pPP\\' )
    VIDEO_EXT = '.mov'
    Video_Path = VIDEO_MAIN_PATH + num_ep +'_'+ num_seq +'_'+ num_plan +'_animatic2D'+ VIDEO_EXT

    # - Remove previous Animatic Camera
    toDelete = mc.listRelatives( grpDict['GD_ROOT'], allDescendents= True, type= 'camera' ) or list()
    for item in toDelete:
        mc.delete( selection.get_parent( item ) )

    # - Create new Animatic Camera
    CAM_Animatic = mc.camera( name= 'cam_animatique_'+ num_ep +'_'+ num_plan +'_', aspectRatio=1.77, displayFilmGate=True )
    mc.setAttr( CAM_Animatic[1] +'.visibility', 0 )
    mc.parent( CAM_Animatic[0], grpDict['GD_ROOT'] )
    # - Create imagePlane
    IMGP = pm.imagePlane(camera = CAM_Animatic[1], showInAllViews=False )


    #SET DE L'IMAGE PLANE
    pm.setAttr(IMGP[1].name()+".type",2)
    IMGP[1].fileName( Video_Path )
    pm.setAttr(IMGP[1].name()+".fit",1)
    pm.setAttr(IMGP[1].name()+".useFrameExtension",1)
    pm.setAttr(IMGP[1].name()+".frameOffset",-100)
    pm.setAttr(IMGP[1].name()+".frameIn",101)
    pm.setAttr(IMGP[1].name()+".frameOut",1000)
    pm.setAttr(CAM_Animatic[1] +".displayFilmGate", 1)
    pm.setAttr(CAM_Animatic[1] +".displayGateMask", 1)
    pm.setAttr(CAM_Animatic[1] +".overscan", 1.4)
    pm.setAttr(CAM_Animatic[1] +".displaySafeTitle", 1)
    pm.setAttr(CAM_Animatic[1] +".displaySafeAction", 1)
    pm.setAttr(CAM_Animatic[1] +".displayGateMaskColor", [0,0,0])
    print '+ Animatic 2D loaded'


    # --- Set Viewport 2.0 AO default Value
    mc.setAttr( 'hardwareRenderingGlobals.ssaoAmount', 0.3)
    mc.setAttr( 'hardwareRenderingGlobals.ssaoRadius', 8 )
    mc.setAttr( 'hardwareRenderingGlobals.ssaoFilterRadius', 8 )
    mc.setAttr( 'hardwareRenderingGlobals.ssaoSamples', 16 )
    print '+ Viewport 2.0 default AO value Set'


    # --- Pimp Viewport
    mel.eval( 'setNamedPanelLayout("Four View")' )
    sidePanel = mc.getPanel( withLabel= 'Side View' )
    pm.modelPanel( sidePanel, edit= True, camera= CAM_Animatic[1] )
    topPanel = mc.getPanel( withLabel= 'Top View' )
    perspPanel = mc.getPanel( withLabel= 'Persp View' )
    pm.modelPanel( perspPanel, edit= True, replacePanel= topPanel )
    mc.modelEditor( sidePanel, edit= True, allObjects= 0, imagePlane= True, grid= False )
    print '+ Viewport pimp as Layout work flow'

    print '-----'