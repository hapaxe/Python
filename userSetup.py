print '--- userSetup.py : Stella_Serie ---'

import maya.cmds as mc
#import maya.mel
import functions.file_info as file_info

# --- Set joint AutoOrient OFF
mc.optionVar(sv=['Move', 'manipMoveContext -e -orientJointEnabled 0 Move'])
print ' . Set joint AutoOrient OFF'

# --- Load Plugin
plugins_toLoad= list()
# - Maya
plugins_toLoad.extend( ['AbcExport', 'AbcImport', 'rotateHelper', 'matrixNodes', 'objExport', 'sceneAssembly', 'gpuCache' ] )
# - Cube
plugins_toLoad.extend( ['cubeMenu_maya', 'extraMenu'] )
# - ThirdPart
plugins_toLoad.extend( ['ngSkinTools', 'radialBlendShape', 'MayaExocortexAlembic'] )

mc.evalDeferred( 'file_info.load_plugin( plugins= plugins_toLoad )' )

