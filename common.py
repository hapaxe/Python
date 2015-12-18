__author__ = 'v.moriceau'

import sys
import os
import glob
from PySide.QtGui import QMainWindow
try:
    import OpenImageIO as oiio
    from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo
    OIIO_IMPORTED = True
except:
    OIIO_IMPORTED = False

try:
    import maya.mel as mel
    import maya.cmds as cmds
    import maya.OpenMayaUI as omui
    import pymel.core as pm
    from shiboken import wrapInstance
    from MayaSceneManagerGeneric import MayaSceneManagerDialog
    MAYA_IMPORTED = True
except:
    MAYA_IMPORTED = False

from general_purpose_libraries import file_system
from general_purpose_libraries import cube_logging
import tube_libraries
from config import *

def _maya_not_loaded(*args, **kwargs):
    '''Raises error'''
    raise NotImplementedError('Maya Modules could not be imported ! Maybe you are outside Maya ?')

def _oiio_not_loaded(*args, **kwargs):
    '''Raises error'''
    raise NotImplementedError('OpenImageIO could not be imported ! Maybe you are inside Maya ?')

def assets_last_wips(asset_name, project_id=PROJECT_ID):
    '''DEPRECATED !!'''
    # Return
    return tube_libraries.get_asset_infos(asset_name, project_id)

def key_by_cube_name(cube_name, key_name):
    # Open JSON
    anima_assets = file_system.FileSystem.load_from_json(ASSETS_ANIMA_JSON_FILEPATH)
    # Each Asset
    for anima_name, asset_dict in anima_assets.items():
        # If dict cube name match
        if asset_dict['Cube Name'] == cube_name:
            # If key_name exists
            if key_name in asset_dict.keys():
                # Return
                return asset_dict[key_name]

def geo_by_cube_name(cube_name):
    # Return
    return key_by_cube_name(cube_name, 'Geometry')

def look_by_cube_name(anima_assets, cube_name):
    # Return
    return key_by_cube_name(cube_name, 'Look')

def name_by_anima_name(anima_assets, anima_name):
    # TODO supprimer cette methode
    # Key present
    if anima_name in anima_assets.keys():
        # Return
        return anima_assets[anima_name]['Cube Name']

def name_convert(cube_name='', anima_name=''):
    '''Fetches Corresponding name from/to Anima from/to Cube'''
    # If Anima Name given
    if anima_name != '' and cube_name == '':
        # Load .json
        anima_assets = file_system.FileSystem.load_from_json(ASSETS_ANIMA_JSON_FILEPATH)
        # If loaded
        if anima_assets:
            # If Key present
            if anima_name in anima_assets.keys():
                # Return
                return anima_assets[anima_name]['Cube Name']
    # If Cube Name given
    elif anima_name == '' and cube_name != '':
        # Load .json
        anima_assets = file_system.FileSystem.load_from_json(ASSETS_ANIMA_JSON_FILEPATH)
        # If loaded
        if anima_assets:
            # Each Asset
            for anima_name, anima_dict in anima_assets.items():
                # If Cube Name
                if anima_dict['Cube Name'] == cube_name:
                    # Return
                    return anima_name
    # If none or both
    else:
        # Attribute Error
        raise AttributeError('You should give one and only one param !')

def remove_last_digits(string):
    '''Suppress digits at the end of a string'''
    # Assume last char is castable to int
    is_int = True
    # As long as last char is castable
    while is_int:
        # Try to cast
        try:
            int(string[-1])
            # Remove last char
            string = string[:-1]
            # Go on looping
            is_int = True
        # Cast Failed
        except:
            # Stop Looping
            is_int = False
    # Return
    return string

if OIIO_IMPORTED:
    def scale_and_convert(source_filepath, target_filepath, fast=False, width=256, height=256, depth=oiio.INT8):
        # Verbose
        cube_logging.CubeLogging.info('Resize : %s' % source_filepath)
        cube_logging.CubeLogging.info('      -> %s' % target_filepath)
        cube_logging.CubeLogging.info('       @ %sx%s' % (width, height))
        # Open Tif
        source_buf = ImageBuf(str(source_filepath))
        # Create buffer 256x256x3x8
        target_buf = ImageBuf(ImageSpec(width, height, 3, depth))
        # If fast
        if fast:
            # Resample (faster)
            ImageBufAlgo.resample(target_buf, source_buf)
        else:
            # Resize (slower, better)
            ImageBufAlgo.resize(target_buf, source_buf)
        # Write File
        target_buf.write(str(target_filepath))
# Module not loaded
else: scale_and_convert = _oiio_not_loaded

if MAYA_IMPORTED:
    def maya_main_window_widget():
        '''Returns Maya Main Window Widget'''
        # Get Pointer
        ptr = omui.MQtUtil.mainWindow()
        # Return wrapped instance
        return wrapInstance(long(ptr), QMainWindow)
# Module not loaded
else: maya_main_window_widget = _maya_not_loaded

if MAYA_IMPORTED:
    def get_shot_infos():
        # Get Current Scene filepath
        current_scene_filepath = cmds.file(query=True, sceneName=True)
        # If its a shot
        if '/shot/' in current_scene_filepath:
            # Split
            splitted_scene_filepath = current_scene_filepath.split('/')
            # If Has 11 elements
            if len(splitted_scene_filepath) == 11:
                # Project Infos
                project_name, project_description = splitted_scene_filepath[1].split('_')
                # Connect to tube
                with tube_libraries.Tube() as tube:
                    # Project Manager
                    project_manager = tube.project_manager(-1)
                    # Get Porject ID
                    project_id = project_manager.get_project_id_by_name(project_name, project_description)
                # If Project id Found
                if project_id:
                    # Season / Episode Infos
                    episode_code = splitted_scene_filepath[4].split('_')[0][1:]
                    season_number = int(episode_code[:2])
                    episode_number = int(episode_code[2:])
                    # Sequence Infos
                    sequence_number = int(splitted_scene_filepath[6][1:])
                    # Shot Infos
                    shot_number = int(splitted_scene_filepath[7][1:])
                    # Task Infos
                    task_name = splitted_scene_filepath[8]
                    # Task Root
                    task_root = current_scene_filepath.split('/wip/')[0]
                    # Get Framerange and Framerate
                    frame_in = cmds.playbackOptions(query=True, animationStartTime=True)
                    frame_out = cmds.playbackOptions(query=True, animationEndTime=True)
                    frame_rate = cmds.playbackOptions(query=True, framesPerSecond=True)
                    # Build dict
                    return dict(project_id=project_id, proj_name=project_name, proj_description=project_description,
                                season_number=season_number, episode_number=episode_number,
                                sequence_number=sequence_number, shot_number=shot_number, task_name=task_name,
                                task_root=task_root, frame_in=frame_in, frame_out=frame_out, frame_rate=frame_rate)
# Module not loaded
else: get_shot_infos = _maya_not_loaded

if MAYA_IMPORTED:
    def walk_from_assembly(assembly_node):
        '''Returns Walk Controller for a given Assembly Transform'''
        # Get Descendants
        group_grp_rig = [child_node for child_node in cmds.listRelatives(assembly_node, children=True) if child_node.endswith('_RIG')]
        # If Any
        if group_grp_rig:
            group_grp_rig = group_grp_rig[0]
            # Get Descendants
            group_rig = [child_node for child_node in cmds.listRelatives(group_grp_rig, children=True) if child_node.endswith('RIG')][0]
            # If Any
            if group_rig:
                # Get Walk
                walk_node = [child_node for child_node in cmds.listRelatives(group_rig, allDescendents=True) if child_node.endswith('walk_ctrl')][0]
                # Get Helper
                helper_nodes = [child_node for child_node in cmds.listRelatives(walk_node, allDescendents=True) if child_node.endswith('helper_ctrl')]
                # If Any
                if helper_nodes:
                    # Return First (supposed only)
                    return helper_nodes[0]
                # Else
                return walk_node
# Module not loaded
else: walk_from_assembly = _maya_not_loaded

if MAYA_IMPORTED:
    def geo_from_assembly(assembly_node):
        '''Returns Walk Controller for a given Assembly Transform'''
        # Get Descendants
        group_grp_rig = [child_node for child_node in cmds.listRelatives(assembly_node, children=True) if child_node.endswith('_RIG')]
        # If Any
        if group_grp_rig:
            group_grp_rig = group_grp_rig[0]
            # Get Descendants
            group_rig = [child_node for child_node in cmds.listRelatives(group_grp_rig, children=True, fullPath=True) if child_node.endswith('GEO')]
            # If Any
            if group_rig:
                # Return GEO
                return group_rig[0]
# Module not loaded
else: geo_from_assembly = _maya_not_loaded

if MAYA_IMPORTED:
    def cog_from_assembly(assembly_node):
        '''Returns Cog Controller for a given Assembly Transform'''
        # Get Descendants
        cog_contrl = [child_node for child_node in cmds.listRelatives(assembly_node, allDescendents=True) if child_node.endswith('cog_ctrl')]
        print cog_contrl
        # If Any
        if cog_contrl:
            # Return
            return cog_contrl[0]
# Module not loaded
else: cog_from_assembly = _maya_not_loaded

if MAYA_IMPORTED:
    def save_wip(scene_id):
        # Try
        try:
            # Obligatoire pour pouvoir ensuite faire un wip
            cmds.fileInfo('SceneId', scene_id)
            # cree une nouvelle instance sur le tube manager
            d = MayaSceneManagerDialog()
            # fait un save wip sur la scene ouverte
            d.saveWip()
        # Except
        except: pass
# Module not loaded
else: save_wip = _maya_not_loaded

if MAYA_IMPORTED:
    def set_attribute(node, attribute_name, attrbute_value=None, data_type="string"):
        # Check If not Exists
        if not cmds.listAttr(node, st=attribute_name):
            # Create Attribute
            cmds.addAttr(node, longName=attribute_name, dataType=data_type)
        # If attribute value given
        if attrbute_value:
            # Set Value
            cmds.setAttr(node + "." + attribute_name, attrbute_value, type=data_type)
# Module not loaded
else: set_attribute = _maya_not_loaded

if MAYA_IMPORTED:
    def get_attribute(node, attribute_name):
        # Check If Exists
        if cmds.listAttr(node, st=attribute_name):
            # Get Attribute
            return cmds.getAttr(node + "." + attribute_name)
# Module not loaded
else: get_attribute = _maya_not_loaded

if MAYA_IMPORTED:
    def del_attribute(node, attribute_name):
        # Check If Exists
        if cmds.listAttr(node, st=attribute_name):
            # Delete Attribute
            cmds.deleteAttr(node, attribute=attribute_name)
# Module not loaded
else: del_attribute = _maya_not_loaded

if MAYA_IMPORTED:
    def assembly_set_representation():
        # Get All AssemblyReferences
        assembly_nodes = [transform for transform in cmds.ls(type='transform') if cmds.nodeType(transform) == 'assemblyReference']
        # Each Assembly Reference
        for assembly_node in assembly_nodes:
            # List Representations
            assembly_representations = [cmds.assembly(assembly_node, query=True, repLabel=representation_name) for representation_name in cmds.assembly(assembly_node, query=True, listRepresentations=True)]
            # Get Representation Label
            representation_label = cmds.assembly(assembly_node, query=True, activeLabel=True)
            # If setupLOD0
            if representation_label == 'setupLOD0':
                # Get Walk
                walk_node = walk_from_assembly(assembly_node)
                # Record Transforms
                assembly_matrix = cmds.xform(assembly_node, query=True, matrix=True, worldSpace=True)
                walk_matrix = cmds.xform(walk_node, query=True, matrix=True, worldSpace=True)
                # If BBOX available
                if 'BBOX' in assembly_representations:
                    # Set Represenation to BBOX
                    cmds.assembly(assembly_node, edit=True, activeLabel='BBOX')
                    # Set Transform
                    cmds.xform(assembly_node, matrix=walk_matrix, worldSpace=True)
            # If setupLOD2
            elif representation_label == 'setupLOD2':
                pass
            # All Other
            else:
                pass
# Module not loaded
else: assembly_set_representation = _maya_not_loaded

if MAYA_IMPORTED:
    class ProgressBar(object):
        '''Class use the Progressbar of Maya'''
        def __init__(self, message, max_value=1000, hide_nodes=True):
            # Set Attributes
            self.message = message
            self.max_value = max(max_value, 1)
            self.hide_nodes = hide_nodes
            self.hidden_nodes = []

        def __enter__(self):
            # Generate a progressbar
            self.main_progressbar = mel.eval('$tmp = $gMainProgressBar')
            # Start
            cmds.progressBar( self.main_progressbar,
                                edit=True,
                                beginProgress=True,
                                isInterruptable=False,
                                status=self.message,
                                maxValue=self.max_value)
            # If hide
            if self.hide_nodes:
                # Get Hidden Nodes
                self.hidden_nodes = cmds.ls(iv=True, typ='transform')
                # Hide All Nodes
                cmds.hide(all=True)
            # Return
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # End
            self._end()

        def is_cancelled(self):
            # Return if cancelled
            return cmds.progressBar(self.main_progressbar, query=True, isCancelled=True)

        def increment(self, step=1):
            # Sets the step value of the progressbar
            cmds.progressBar(self.main_progressbar, edit=True, step=step)
            # If hide
            if self.hide_nodes:
                # Hide All Nodes
                cmds.hide(all=True)

        def set_message(self, message):
            # Set Member
            self.message = message
            # Set Progress bar
            cmds.progressBar(self.main_progressbar, edit=True, status=self.message)

        def _end(self):
            # If hide
            if self.hide_nodes:
                # Unhide All
                cmds.showHidden(allObjects=True)
                # Rehide Hidden
                cmds.hide(self.hidden_nodes)
            # Terminates Progress
            cmds.progressBar(self.main_progressbar, edit=True, endProgress=True)
# Module not loaded
else: ProgressBar = _maya_not_loaded

if MAYA_IMPORTED:
    def get_cube_tag(node_name, attribute_name):
        # Verbose
        #print 'get_cube_tag("%s")' % node_name
        # Try Directly
        cube_name = get_attribute(node_name, attribute_name)
        # If not gotten
        if not cube_name:
            # Get Object Type
            node_type = cmds.objectType(node_name)
            # If Geometry Set
            if node_type == 'objectSet':
                # Get Contained Transforms
                transforms = cmds.listRelatives(node_name, c=True, f=True, noIntermediate= True) or list()
                # Each transform
                for transform in transforms:
                    # Recurse
                    tag = get_cube_tag(transform, attribute_name)
                    # If found
                    if tag:
                        # Return
                        return tag
            # If Transform / Mesh / Shape
            elif node_type in ['transform', 'mesh', 'shape', 'camera', 'locator']:
                # If not shape
                if node_type == 'locator':
                    # Get Shape
                    shape = cmds.listRelatives(node_name, parent=True, f=True, type='transform')
                # If Locator
                elif node_type != 'shape':
                    # Get Shape
                    shape = cmds.listRelatives(node_name, children=True, f=True, type='shape')
                else:
                    # Use
                    shape = node_name
                # If Any
                if shape:
                    # Try Directly (recusion here would cause infinite recurse)
                    tag = get_attribute(shape[0], attribute_name)
                    # If found
                    if tag:
                        # Return
                        return tag
                # Go up
                node_up = cmds.listRelatives(node_name, p=True, f=True, typ='transform')
                # If up
                if node_up:
                    # Recurse
                    tag = get_cube_tag(node_up[0], attribute_name)
                    # If found
                    if tag:
                        # Return
                        return tag
        # If gotten
        return cube_name
# Module not loaded
else: get_cube_tag = _maya_not_loaded

def list_bg_props():
    # Get Filename
    current_scene_filename = cmds.file(query=True, sceneName=True)
    # Get Task Root
    shot_task_root = current_scene_filename.split('/wip/')[0]
    # Compile Json Filename
    json_filename = os.path.normpath(os.path.join(shot_task_root, 'datas/props_list.json'))
    # List Assemblies
    assemblies = [transform for transform in cmds.ls(type='transform', long=True) if cmds.nodeType(transform) == 'assemblyReference']
    # Prepare Json
    json_dict = {'scene_assets':[]}
    # Each Assemblie
    for assembly in assemblies:
        # Get Cube Name
        cube_name = get_cube_tag(assembly, 'cube_name')
        # If Not already present
        if cube_name not in [asset_dict['asset_name'] for asset_dict in json_dict['scene_assets']]:
            # Append
            json_dict['scene_assets'].append({'asset_name':cube_name})
    # Save to Json
    file_system.FileSystem.save_to_json(json_dict, json_filename)

if MAYA_IMPORTED:
    def get_set_transforms(set_name):
        # Init transforms
        set_transforms = []
        # If objectSet
        if cmds.objectType(set_name) == 'objectSet':
            # Get Shapes
            shapes = cmds.listRelatives(set_name, c=True, f=True, typ='shape')
            # If Found
            if shapes:
                # Each Shape
                for shape in shapes:
                    # Get transform
                    transform = cmds.listRelatives(shape, p=True, f=True, typ="transform")
                    # If found
                    if transform:
                        # Append
                        set_transforms.append(transform[0])
            # If no shapes
            else:
                # Get Transforms
                transforms = cmds.listRelatives(set_name, c=True, f=True, typ='transform')
                # If transforms
                if transforms:
                    # Add to return
                    set_transforms += transforms
        # Return
        return set_transforms
# Module not loaded
else: get_set_transforms = _maya_not_loaded

if MAYA_IMPORTED:
    def get_set_shapes(set_name):
        # Init transforms
        set_shapes = []
        # If objectSet
        if cmds.objectType(set_name) == 'objectSet':
            # Get Shapes
            shapes = cmds.listRelatives(set_name, children=True, fullPath=True, type='shape')
            # If Found
            if shapes:
                # Add to return
                set_shapes += shapes
            # If no shapes
            else:
                # Get Transforms
                transforms = cmds.listRelatives(set_name, children=True, fullPath=True, type='transform') or list()
                # Each Shape
                for transform in transforms:
                    # Get transform
                    shape = cmds.listRelatives(transform, children=True, fullPath=True, type='shape')
                    # If found
                    if shape:
                        # Append
                        set_shapes.append(shape[0])
        # Return
        return set_shapes
# Module not loaded
else: get_set_shapes = _maya_not_loaded
