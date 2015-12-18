__author__ = 'v.moriceau'

import os
from general_purpose_libraries import CubeLogging, FileSystem
from tube_libraries import Tube
from config import *
from common import *
try:
    from maya import cmds
    MAYA_IMPORTED = True
except:
    MAYA_IMPORTED = False

class StellaProcessor(object):
    '''
    Class allowing processing of Stella's Files and Maya Scenes
    '''
    def __init__(self,
                 json_anima_assets_filepath=ASSETS_ANIMA_JSON_FILEPATH,
                 json_textures_rename_filepath=TEXTURES_MATCHES_JSON_FILEPATH,
                 root_database_anima=DATABASE_ANIMA_ROOT,
                 root_image_repository=TEXTURES_REPOSITORY_ROOT,
                 project_id=PROJECT_ID):
        # Init Superclass
        object.__init__(self)
        # Init Logging
        CubeLogging.init('StellaProcessor')
        # Verbose New Session
        CubeLogging.info('=====================')
        CubeLogging.info('     New Session')
        CubeLogging.info('=====================')
        # Init Attributes
        self.set_project_id(project_id)
        self.set_json_anima_assets_filepath(json_anima_assets_filepath)
        self.set_json_textures_rename_filepath(json_textures_rename_filepath)
        self.set_root_database_anima(root_database_anima)
        self.set_root_images_repository(root_image_repository)
    # ---------------------------------------
    def set_project_id(self, project_id):
        '''Sets Attribute'''
        # Cast
        project_id = int(project_id)
        # If strict positive
        if project_id > 0:
            # Set Attribute
            self.project_id = project_id
            # Success
            return True
        # Failure
        raise AttributeError('project_id=%s' % project_id)
    # ---------------------------------------
    def set_json_anima_assets_filepath(self, json_anima_assets_filepath):
        '''Sets Attribute'''
        # Cast types and env vars
        json_anima_assets_filepath = FileSystem.normpath(json_anima_assets_filepath)
        # If Succes
        if json_anima_assets_filepath:
            # Set Attribute
            self.json_anima_assets_filepath = json_anima_assets_filepath
            # Success
            return True
        # Failure
        raise AttributeError('json_anima_assets_filepath=%s' % json_anima_assets_filepath)
    # ---------------------------------------
    def set_json_textures_rename_filepath(self, json_textures_rename_filepath):
        '''Sets Attribute'''
        # Cast types and env vars
        json_textures_rename_filepath = FileSystem.normpath(json_textures_rename_filepath)
        # If Succes
        if json_textures_rename_filepath:
            # Set Attribute
            self.json_textures_rename_filepath = json_textures_rename_filepath
            # Success
            return True
        # Failure
        raise AttributeError('json_textures_rename_filepath=%s' % json_textures_rename_filepath)
    # ---------------------------------------
    def set_root_database_anima(self, root_database_anima):
        '''Sets Attribute'''
        # Cast types and env vars
        root_database_anima = FileSystem.normpath(root_database_anima)
        # If Succes
        if root_database_anima:
            # Set Attribute
            self.root_database_anima = root_database_anima
            # Success
            return True
        # Failure
        raise AttributeError('root_database_anima=%s' % root_database_anima)
    # ---------------------------------------
    def set_root_images_repository(self, root_image_repository):
        '''Sets Attribute'''
        # Cast types and env vars
        root_image_repository = FileSystem.normpath(root_image_repository)
        # If Succes
        if root_image_repository:
            # Set Attribute
            self.root_image_repository = root_image_repository
            # Success
            return True
        # Failure
        raise AttributeError('root_image_repository=%s' % root_image_repository)
    # ---------------------------------------
    def look_conform(self, cube_name='', anima_name=''):
        '''Conforms a given .look file, according to given Cube Asset Name'''
        # Verbose
        CubeLogging.info("==> look_conform(cube_name='%s', anima_name='%s')" % (cube_name, anima_name))
        # Open anima .json
        anima_assets = FileSystem.load_from_json(self.json_anima_assets_filepath)
        # If Anima name
        if anima_name and not cube_name:
            # Find Cube Name
            asset_name = name_by_anima_name(anima_assets, anima_name)
        # If Cube Name
        elif not anima_name and cube_name:
            # Cube name
            asset_name = cube_name
        # Else
        else:
            # Error
            raise ValueError('Give only one name ! cube_name=%s OR anima_name=%s' % (cube_name, anima_name))
        # Connect to Tube
        with Tube() as tube:
            # Asset Manager
            asset_manager = tube.asset_manager(self.project_id)
            # Fetch Scenes
            asset_scenes = asset_manager.get_asset_last_scenes(asset_name=asset_name)
        # If Anything found
        if asset_scenes:
            # Open matching .json
            textures_matching_dict = FileSystem.load_from_json(self.json_textures_rename_filepath)
            # Find .look
            source_look_filepath = look_by_cube_name(anima_assets, asset_name)
            # Asset Type Name
            asset_type_name = asset_scenes[0]['type_name']
            # Asset Root
            asset_root = asset_scenes[0]['scene_path'].split(asset_scenes[0]['task_name'])[0]
            # Get Textures path
            asset_textures_path = "%stextures" % asset_root
            # Get Shading Path
            asset_shading_path =  "%sshading" % asset_root
            # .look filename
            target_look_filepath = "%s/datas/look/%s_%s.look" % (asset_shading_path, asset_type_name, asset_name)
            # If .look already present in Shading
            if os.path.isfile(target_look_filepath):
                # Verbose
                CubeLogging.warn('%s Already Exists !' % target_look_filepath)
            # If .look not already generated
            #else:
            if True:
                # If Pathes exists
                if os.path.isdir(asset_textures_path) and os.path.isdir(asset_shading_path):
                    # Open Source .look
                    look_header, look_nodes, look_shaders = FileSystem.load_from_json(source_look_filepath)
                    # New Shaders
                    new_shaders = []
                    # Each Shader
                    for shader_dict in look_shaders:
                        # New Shader
                        new_shader = {}
                        # Each Items
                        for shader_key, shader_value in shader_dict.items():
                            # If Value is dict
                            if isinstance(shader_value, dict):
                                # If Key 'diffuseColorMap'
                                if 'diffuseColorMap' in shader_value.keys():
                                    # Fetch Texture pathes
                                    texture_anima_filepath = os.path.normpath(shader_value['diffuseColorMap'].replace('$ANIMA_PROJECT_ROOT', self.root_database_anima)).replace('{assetDataType}', '.tif')
                                    texture_filename = os.path.basename(texture_anima_filepath)
                                    texture_cube_tiff_filepath = os.path.normpath('%s/%s' % (asset_textures_path, texture_filename))
                                    # Each mathcing items
                                    for source_filepath, target_filepath in textures_matching_dict.items():
                                        # If Filename Matches
                                        if os.path.basename(source_filepath) == texture_filename:
                                            # Modify source filepath
                                            texture_anima_filepath = os.path.normpath('%s/%s' % (self.root_image_repository, target_filepath))
                                            # Modify target filepath
                                            texture_cube_tiff_filepath = os.path.normpath('%s/%s' % (asset_textures_path, target_filepath))
                                    # Prepare .jpeg target map
                                    texture_cube_jpeg_filepath = texture_cube_tiff_filepath.replace('.tif', '.jpg')
                                    # If .tif target not present
                                    if not os.path.isfile(texture_cube_tiff_filepath):
                                        # Copy source tif
                                        texture_success = FileSystem.copy_file(texture_anima_filepath, texture_cube_tiff_filepath)
                                        # If error
                                        if not texture_success:
                                            # Modify path to be used in .look
                                            texture_cube_tiff_filepath = None
                                    # If .jpg target not present
                                    if not os.path.isfile(texture_cube_jpeg_filepath):
                                        # Resize and convert to .jpg
                                        scale_and_convert(texture_cube_tiff_filepath, texture_cube_jpeg_filepath)
                                    # Update dict
                                    if texture_cube_tiff_filepath:  shader_value['diffuseColorMap'] = texture_cube_tiff_filepath.replace(os.path.expandvars('$CUBE_PROJECT_DATAS'), '$CUBE_PROJECT_DATAS')
                                    else:                           shader_value['diffuseColorMap'] = None
                            # Append to New Shader
                            new_shader[shader_key] = shader_value
                        # Append to new Shaders
                        new_shaders.append(new_shader)
                    # Save as new JSON
                    FileSystem.save_to_json([look_header, look_nodes, new_shaders], target_look_filepath)
                # If Pathes don't exists
                else:
                    # Verbose
                    CubeLogging.warn('%s Might not exist !' % asset_textures_path)
                    CubeLogging.warn('%s Might not exist !' % asset_shading_path)
        # Nothing found
        else:
            # Verbose
            CubeLogging.warn("asset_name='%s' not found in Tube for project_id=%s !" % (asset_name, self.project_id))
    # ---------------------------------------
    if MAYA_IMPORTED:
        def apply_shaders(self, asset_name):
            CubeLogging.info('==> apply_shaders()')
            # Connect to Tube
            with Tube() as tube:
                # Asset Manager
                asset_manager = tube.asset_manager(self.project_id)
                # Fetch Scenes
                asset_scenes = asset_manager.get_asset_last_scenes(asset_name=asset_name)
            # If Anything found
            if asset_scenes:
                # Init Filepath
                look_filepath = None
                # Each Task
                for task_dict in asset_scenes:
                    # If Shading
                    if task_dict['task_name'] == 'shading':
                        # Get Path
                        look_filepath = "%sdatas/look/%s_%s.look" % (task_dict['scene_path'].split('wip')[0], task_dict['type_name'], asset_name)
                # Open JSON file
                look_data = FileSystem.load_from_json(look_filepath)
                # If look data
                if look_data:
                    # Shaders
                    shading_groups = {}
                    shader_index = 0
                    # Each Shader
                    for shader_dict in look_data[2]:
                        # Get Shader Infos
                        shader_infos = shader_dict['material_override']
                        # If diffuseColorMap
                        if 'diffuseColorMap' in shader_infos.keys():
                            # Get map entry
                            look_map_path = shader_infos['diffuseColorMap']
                            # If Map Entry
                            if look_map_path:
                                # Verbose
                                CubeLogging.info('Creating New Shader with Texture %s' % look_map_path)
                                # New Shader
                                new_shader = cmds.shadingNode(shader_dict['shader'].split('/')[1], asShader=True, name='sh_%s_0' % asset_name)
                                # Get Texture Filepath
                                texture_filepath = look_map_path.replace('.tif', '.jpg')
                                # New Texture Map
                                new_texturemap = cmds.shadingNode('file', asTexture=True, name='tx_%s_0' % asset_name)
                                cmds.setAttr(new_texturemap+'.fileTextureName', texture_filepath, type='string')
                                # Connect Map to Shader
                                cmds.connectAttr(new_texturemap+'.outColor', new_shader+'.color', force=True)
                                # New Shading Group
                                new_shading_group = cmds.sets(renderable=True,empty=1,noSurfaceShader=True)
                                # Connect Shader to Shading Group
                                cmds.defaultNavigation(source=new_shader,destination=new_shading_group,connectToExisting=1)
                                # Append to shading_groups
                                shading_groups[shader_index] = new_shading_group
                                # Increment
                                shader_index += 1
                    # Each Object
                    for object_name, shader_id in look_data[1].items():
                        # Get Shape
                        object_shape = cmds.ls('*|' + object_name.replace('/', '|'))
                        # If Exists
                        if object_shape:
                            # Get Actual Shape
                            object_shape = object_shape[0]
                            # If Shader Exists
                            if shader_id in shading_groups.keys():
                                # Verbose
                                CubeLogging.info('Deleting Current Shader of %s' % object_shape)
                                # Get Old Shading Group and Shader
                                object_shading_group = cmds.listConnections(object_shape, t='shadingEngine')
                                object_lambert = cmds.listConnections(object_shading_group, t='lambert')
                                # Delete Shader if Found
                                if object_lambert: cmds.delete(object_lambert)
                                # Delete Shading Group if Found
                                if object_shading_group: cmds.delete(object_shading_group)
                                # Verbose
                                CubeLogging.info('Applying New Shader id=%s to %s' % (shader_id, object_shape))
                                # Connect to New Shading Group
                                cmds.sets(object_shape,forceElement=shading_groups[shader_id],e=1)
                            # Else
                            else:
                                # Verbose
                                CubeLogging.info('No New Shader was generated for %s' % object_shape)
            else:
                # Verbose
                CubeLogging.warn('No Info found in Tube for %s !' % asset_name)
    else:
        def apply_shaders(self, *args, **kwargs):
            # Raise
            raise NotImplementedError('Maya Cmds could not be imported ! Maybe you are outside Maya ?')
    # ---------------------------------------
    if MAYA_IMPORTED:
        def apply_envvar_to_shaders(self, envvar_name='$CUBE_PROJECT_DATAS'):
            # List All Materials
            materials = cmds.ls(materials=True)
            # Each Material
            for material in materials:
                # Get Color Node
                color_node = cmds.listConnections(material + '.color')
                # If Something
                if color_node:
                    # Get value
                    filepath = cmds.getAttr(color_node[0] + '.fileTextureName')
                    # If value
                    if filepath:
                        # Conform
                        filepath = os.path.normpath(filepath)
                        filepath = filepath.replace(os.path.expandvars(envvar_name), envvar_name)
                        # Update Map
                        cmds.setAttr(color_node[0] + '.fileTextureName', filepath, type='string')
    else:
        def apply_envvar_to_shaders(self, *args, **kwargs):
            # Raise
            raise NotImplementedError('Maya Cmds could not be imported ! Maybe you are outside Maya ?')
# ---------------------------------------

la_liste = [u'stellasHouse', u'beanBag_A', u'bigPillow_A', u'booksStack_A', u'booksStack_B', u'candle_A', u'canoe_A', u'chair_A', u'chair_B', u'chest_A', u'cornerTable_A', u'floorMat_A', u'floorMat_B', u'floorMat_C', u'floorMat_D', u'floorMat_E', u'floorMat_F', u'fruitBowl_A', u'funkyPotPlant_A', u'headphones_A', u'jewelleryBox_A', u'ladder_A', u'mirror_A', u'paints_A', u'paints_B', u'paraSail_A', u'piggieToy_A', u'pillow_A', u'pillow_B', u'pillow_C', u'potPlant_A', u'potPlant_B', u'potPlant_C', u'potPlant_D', u'radio_A', u'recordPlayer_A', u'reelTable_A', u'rolledPaper_A', u'skateBoard_A', u'stool_A', u'straw_A', u'stump_A', u'surfBoard_A', u'surfBoard_B', u'teddyBear_A', u'tvShelf_A', u'vase_A', u'violetPillow_A', u'violetPillow_B', u'weatherVane_A', u'whitePillow_A', u'wineGlass_B', u'workStand_A']
la_liste = ['beadCurtain_stellasHouseA', 'bed_stellasHouseA', 'bootPlant_stellasHouseA', 'door_stellasHouseA', 'drape_stellasHouseA', 'drape_stellasHouseB', 'frontCurtain_stellasHouseA', 'frontWall_stellasHouseA', 'hammoc_stellasHouseA', 'hangingOrnament_stellasHouseA', 'hangingOrnametnt_stellasHouseB', 'leftWall_stellasHouseA', 'photos_stellasHouseA', 'platform_stellasHouseA', 'ramp_stellasHouseA', 'rightWall_stellasHouseA', 'roof_stellasHouseA', 'sideTable_stellasHouseA', 'smallLeaves_stellasHouseA', 'tree_stellasHouseA']
la_liste = ['axe_A', 'ballWeed_A', 'bigFlower_A', 'bulbPlant_A', 'chainsaw_A', 'fatPalm_A', 'flatBoulder_B', 'grassClump_tallA', 'grassClump_tallB', 'grassClump_tallC', 'groundPatch_A', 'ground_pathToVolcanoA', 'hoopRoot_A', 'hoopRoot_C', 'hugeCliff_A', 'mossPatch_flatA', 'mossPatch_flatB', 'mossPatch_flatC', 'mushroomDome_A', 'mushroomDome_B', 'mushroomDome_C', 'palmBush_A', 'palmBush_B', 'palmBush_C', 'palmForestUneven_A', 'palmTreeShort_B', 'palmTreeShort_C', 'palmTreeShort_D', 'palmTree_A', 'palmTree_B', 'palmTree_D', 'palmTree_fallenA', 'palmTree_fallenB', 'palm_stumpA', 'palm_stumpB', 'palm_stumpC', 'pillarBoulder_C', 'pillarBoulder_smallA', 'pillarBoulder_smallB', 'rock_littleC', 'rock_mediumA', 'rock_mediumB', 'rock_mediumC', 'rock_smoothA', 'rock_smoothB', 'rock_smoothC', 'rock_smoothD', 'rockyOutCrop_B', 'rockyPillar_tallA', 'root_mediumC', 'roundedGrassClump_A', 'roundedGrassClump_B', 'roundedGrassClump_D', 'slime_A', 'slime_C', 'slime_D', 'slime_E', 'spikePlant_mediumB', 'spikePlant_mediumC', 'spikePlant_smallA', 'stalkFlower_A', 'stalkFlower_B', 'stalkFlower_C', 'stone_A', 'tinyGrassFlowers_A', 'tinyGrassFlowers_B', 'tinyGrassFlowers_C', 'tinyGrassFlowers_E', 'treeStump_A', 'treeStump_B', 'treeStump_C', 'treeTrunk_A', 'treeTrunk_B', 'treeTrunk_D', 'treeTrunk_E', 'twistedPalm_A', 'twistedPalm_B', 'woodyCactus_A', 'woodyCactus_B', 'woodyCactus_C']
la_liste = ['roundPillow_A', 'bentPalmTree_A', 'bigTreeIsland_A', 'boulder_A', 'boulder_B', 'flatTopMushroom_A', 'flatTopMushroom_B', 'flatTopMushroom_C', 'flatTopMushroom_D', 'flatTopMushroom_E', 'hangingVineHoop_A', 'hangingVineHoop_B', 'hangingVineHoop_C', 'hangingVineHoop_mediumA', 'hangingVine_A', 'hangingVine_B', 'hangingVine_mediumA', 'leaves_bigTreeA', 'mainIsland_LS', 'mushroomSideGaint_A', 'mushroomSideGaint_B', 'mushroomSideGaint_C', 'mushroomSideGaint_D', 'mushroomSideGaint_E', 'mushroomSide_A', 'mushroomSide_B', 'mushroomSide_C', 'mushroomTallSkinny_A', 'ocean_A', 'palmTreeShort_A', 'palmTreeTall_A', 'palmTreeTall_B', 'palmTreeTall_C', 'rock_bigA', 'rock_littleA', 'rock_littleB', 'rockyIsland_A', 'rockyIsland_B', 'root_theBigTreeA', 'root_theBigTreeB', 'tinyRoot_A', 'trunk_bigTreeA', 'vine_multiA', 'volcano_LS', 'wetRock_A', 'wetRock_B', 'wetRock_C', 'wetRock_D', 'wetRock_E', 'cocoNutPaint_A', 'willowsBrush_A', 'canvas_A', 'campFire_A', 'apple_A', 'cherry_A', 'grapes_A', 'pie_A', 'roundPillow_A', 'pie_smashedA', 'pillow_D', 'birthdayCake_smallA', 'muffin_A', 'pineapple_A', 'potPlant_F', 'pillow_detailedA', 'barrel_A', 'barrel_B', 'bucket_A', 'bigMallet_A', 'jackHammer_A', 'plank_E', 'paintBrush_A', 'bell_A', 'plank_texbP', 'drawMessy_A', 'umbrella_A', 'stool_B']
la_liste = ['drawsMessy_A']
la_liste = ['benchWooden_A', 'bookcase_A', 'booksStack_C', 'booksStack_D', 'booksStack_E', 'bouy_hangingA', 'cabin_headQuartersA', 'chairSixties_A', 'chest_B', 'chest_C', 'crystalBall_A', 'curtain_headQuartersA', 'deckChair_A', 'deckChair_B', 'drawingBoard_A', 'drawingBoard_B', 'drawingBoard_C', 'flagPole_A', 'floorMatDroopy_A', 'footballl_A', 'fountain_headQuartersA', 'gong_headQuartersA', 'hangingVineHoopSmall_A', 'hangingVineHoopSmall_B', 'hangingVineSmall_A', 'harp_A', 'hqFloorMat_A', 'hqFloorMat_B', 'hqFloorMat_C', 'hqFloorMat_D', 'hqFloorMat_E', 'ladder_B', 'lifeRing_A', 'lightHanging_A', 'lowerFrame_headQuartersA', 'lowerPlanks_headQuartersA', 'midFrame_headQuartersA', 'midFrame_headQuartersB', 'midPlanks_headQuartersA', 'midPlanks_headQuartersB', 'mushroomTallSkinny_B', 'mushroomTallSkinny_C', 'planksPile_A', 'pullie_headQuartersA', 'rampFrame_headQuartersA', 'rope_coilA', 'slide_headQuartersA', 'slingShot_A', 'sofaRounded_A', 'suitCase_A', 'topFrame_headQuartersA', 'topPlanks_headQuartersA', 'treeStumpSeat_A', 'vineCrazy_A', 'vineFat_A', 'wallHook_A', 'stool_C']
la_liste = ['bigTreeFoliage_clumpA', 'bigTreeFoliage_clumpB', 'bigTreeFoliage_clumpC', 'bigTreeFoliage_clumpD', 'bigTreeFoliage_clumpE', 'bigTreeFoliage_ballA', 'bigTreeFoliage_smallClumpA', 'bigTreeFoliage_smallClumpB', 'bigTreeFoliage_flatA', 'bigTreeFoliage_ringA', 'foliage_dahliasHouseA', 'foliage_lucasHouseA', 'foliage_lucasHouseB']
la_liste = ['cornerBeams_A', 'drinkingBarrel_A', 'extension_galesCastleTopA', 'extension_galesCastleTopB', 'extension_galesCastleTopC', 'plank_A', 'plank_B', 'plank_C', 'tower_galesCastleTopA', 'woodenBox_B', 'balconyRail_galesCastleA', 'beam_woodD', 'corridorExt_galesCastleA', 'doorFrame_galesCastleA', 'extension_galesCastleA', 'extension_galesCastleB', 'extension_galesCastleC', 'frontSteps_throneRoomA', 'galesTelescope_A', 'leftBalconyDoor_galesCastleA', 'leftDoor_galesCastleA', 'nail_A', 'nail_B', 'oilDrum_A', 'oilDrum_B', 'oldTyre_A', 'pedestal_throneRoomA', 'plank_texaA', 'plank_texaB', 'plank_texaD', 'plank_texaE', 'plank_texaF', 'plank_texaG', 'plank_texaH', 'plank_texaI', 'plank_texaJ', 'plank_texaK', 'plank_texaM', 'plank_texaN', 'plank_texaO', 'plank_texaP', 'plank_texaQ', 'plank_texaR', 'plank_texbA', 'plank_texbB', 'plank_texbD', 'plank_texbE', 'plank_texbF', 'plank_texbG', 'plank_texbI', 'plank_texbJ', 'plank_texbK', 'plank_texbM', 'plank_texbN', 'plank_texbO', 'plank_texbQ', 'plank_texbR', 'rightBalconyDoor_galesCastleA', 'rightDoor_galesCastleA', 'roundBeam_longA', 'roundBeam_shortB', 'sofa_C', 'squareBeam_shortA', 'squareBeam_shortB', 'stoneBrick_A', 'stoneBrick_B', 'stoneBrick_C', 'storeageBail_A', 'throneRoom_galesCastleA', 'tower_galesCastleA', 'tower_galesCastleB', 'tower_galesCastleC', 'woodenCrate_A', 'woodenSheet_A', 'volcanicRock_ExtE', 'volcanicRock_extA', 'volcanicRock_extB', 'volcanicRock_extC', 'volcanicRock_extD', 'volcanoColumn_A', 'volcanoColumn_B', 'volcanoColumn_C', 'volcanoColumn_D']
la_liste = ['volcanoColumn_E', 'volcanoWall_A', 'volcanoWall_B', 'volcanoWall_drilledC', 'volcano_theVolcanoA']
la_liste = ['blanket_stellasHouseA']
la_liste = ['toySpade_A', 'rubberDuck_A', 'galesPortrait_A', 'drawsMessy_A', 'handCart_A', 'wrench_A', 'mirror_D', 'portrait_galesHouseA']
la_liste = ['bridgeRope_theVolcanoA', 'bridgeRope_theVolcanoB', 'hangingRoot_A', 'hangingRoot_B', 'lava_theVolcanoA', 'mushroomDome_D', 'post_shortA', 'post_shortB', 'slime_B', 'stone_C', 'backWall_throneRoomA', 'banner_throneRoomA', 'beam_woodA', 'beam_woodB', 'bookOfGoldenEgg', 'bookStand_A', 'candleHolder_wallA', 'carpetRamp_throneRoomA', 'drape_throneRoomA', 'floorMat_largeA', 'floor_throneRoomA', 'flyNet_throneRoomA', 'frontWall_throneRoomA', 'galeStatue_throneRoomA', 'leftWallDestoryed_throneRoomA', 'leftWall_throneRoomA', 'lift_throneRoomA', 'log_carvedA', 'log_carvedB', 'log_carvedC', 'log_carvedD', 'log_carvedE', 'log_carvedF', 'metalPlate_A', 'plankCut_A', 'plankCut_B', 'plank_texaL', 'plank_texbH', 'railTrack_A', 'rightWall_throneRoomA', 'roundBeam_longB', 'roundBeam_shortA', 'roundBoulder_smallA', 'saw_A', 'slicedLog_A', 'slicedLog_B', 'stage_throneRoomA', 'stepLadder_A', 'stoneBrick_D', 'stone_B', 'windowFrame_throneRoomA', 'woodShavings_A']
la_liste = ['galesCastleTop_LS', 'galesCastle_LS', 'giantCliff_A', 'giantCliff_B', 'ground_mixedForestA', 'largeTree_A', 'largeTree_B', 'lowShrub_A', 'lowShrub_B', 'mainIsland_beachClearingA', 'palmBushPatch_groundA', 'palmForestBig_A', 'palmForestHill_B', 'palmForestLittle_A', 'palmTree_C', 'pillarBoulder_B', 'rockFace_A', 'rockFace_waterFallA', 'rockFace_waterFallB', 'rockyIsland_C', 'rockyIsland_D', 'rockyPillar_E', 'theBigTree_LS', 'treeTop_A']
la_liste = ['groundDitch_volcanoBaseExtA', 'lava_volcanoBaseExtA', 'volcanoLedge_A', 'volcanoLedge_B', 'volcanoLedge_C', 'volcanoWall_C', 'lava_volcanoEntranceA', 'volcanoWall_tunnelD']
la_liste = ['bentPalmTree_B', 'floweringVine_A', 'ground_beachAndWoodsA', 'helixTree_toplessA', 'helixTree_toplessB', 'hoopRoot_B', 'rockyOutCrop_A', 'rockyOutCrop_C', 'rockyPillar_tallB', 'root_leafyA', 'root_leafyB', 'root_leafyC', 'root_leafyD', 'spikePlant_mediumA', 'spikePlant_smallB', 'topHeavyTree_B']
la_liste = ['backCurtains_galesHouseA', 'bed_galesHouseA', 'bigPillow_B', 'blanket_galesHouseA', 'branchWithVines_A', 'branch_A', 'branch_B', 'discoBall_A', 'doorFrame_galesHouseA', 'doors_galesHouseA', 'entrancePlate_galesHouseA', 'flatPillow_A', 'frontCurtains_galesHousetA', 'leaves_galesHouseA', 'leftCurtains_galesHouseA', 'leftStructure_galesHouseA', 'lift_galesHouseA', 'metalFloor_galesHouseA', 'mirror_B', 'mirror_C', 'patchPillow_A', 'platform_galesHouseA', 'platform_galesHouseB', 'portrait_galesHouseA', 'potPlant_E', 'redCarpet_galesHouseA', 'rightCurtains_galesHouseA', 'rightStructure_galesHouseA', 'roofRope_galesHouseA', 'roof_galesHouseA', 'vineCrazySmall_A']
la_liste = ['balloons_A', 'balloons_B', 'bellTree_A', 'bellTree_B', 'bellTree_C', 'blueStalk_A', 'bowlLeaf_B', 'bowlLeaf_C', 'danceFloor_A', 'discoBall_B', 'discoLight_A', 'djBooth_A', 'galesBanner_A', 'galesBanner_B', 'ground_beachPartyA', 'headQuarters_LS', 'palmForestFlat_A', 'palmTreeCurved_A', 'ribbonBanner_beachPartyA', 'roundBoulder_smallB', 'stellasHouse_LS', 'throneTruck_A', 'tinyFlowersClump_B', 'tinyStone_A']
la_liste = ['palmForestFlat_A']
la_liste = ['floweringVine_B', 'ground_pathForkA', 'hangingVineHoop_mediumB', 'mossPatch_flatD', 'mossPatch_hangingC', 'mossPatch_hangingD', 'multiTrunkTree_A', 'rockFace_B', 'rockPools_A', 'rockyPillar_A', 'rockyPillar_B', 'rockyPillar_C', 'rockyPillar_D', 'root_mediumA', 'root_mediumB', 'roundMossyBoulder_B', 'stringTrunkTree_A', 'stringTrunkTree_B', 'stringTrunkTree_C', 'stringTrunkTree_largeA', 'tinyFlowersClump_A', 'toadStool_A', 'toadStool_C']
la_liste = ['abacus_A', 'barrelRoomBack_dahliasHouseA', 'barrelRoomFront_dahliasHouseA', 'barrelRoomLeft_dahliasHouseA', 'barrelRoomRight_dahliasHouseA', 'bookStand_B', 'book_openA', 'canister_A', 'chemistryBottle_A', 'chemistryBottle_B', 'chemistryBottle_C', 'chemistryPipe_A', 'chemistryPipet_A', 'chemistrySet_A', 'chemistrySet_B', 'cog_A', 'craneHook_A', 'dahliasTelescope_A', 'drawingBoard_D', 'featherPen_A', 'funkyFlower_A', 'halfBeam_texaA', 'hammer_A', 'haningNote_dahliasHouseA', 'ironNail_A', 'jar_A', 'landingPad_dahliasHouseA', 'leafSamples_dahliasHouseA', 'lowerPlaform_dahliasHouseA', 'magnetControlUnit_A', 'mainDoor_dahliasHouseA', 'map_dahliasHouseA', 'mortar_A', 'mug_A', 'paper_A', 'pen_A', 'pipe_dahliasHouseA', 'plank_D', 'planterBox_A', 'radio_B', 'rollUpScreen_A', 'ruler_A', 'sketches_dahliasHouse_A', 'sledCable_dahliasHouseA', 'thermometer_A', 'treeTrunk_dahliasHouseA', 'triangle_A', 'upperPlatform_dahliasHouseA', 'vegePlant_A', 'vinePlant_A', 'winch_dahliasHouseA', 'windMill_dahliasHouseA', 'woodenBox_A', 'workBench_A']
la_liste = ['painting_girlsA', 'easel_A']
la_liste = ['backLeaves_parkouringAreaA', 'branch_gaint_B', 'branch_medium_A', 'branch_medium_B', 'forkedBranch_gaintA', 'frontLeaves_parkouringAreaA', 'hangingVineHoopSmall_C', 'hangingVineSmall_C', 'spiralBranch_A', 'spiralBranch_B', 'toadStool_B']
la_liste = ['backWall_corridorA', 'banner_corridorA', 'beam_crookedA', 'beam_woodC', 'colorPalette_A', 'floorBack_corridorA', 'hallMat_A', 'hangingFabric_corridorA', 'hangingFabric_corridorB', 'leftWall_corridorA', 'lifterControl_corridorA', 'logBeam_A', 'mirror_D', 'painting_goldFrameA', 'painting_goldFrameB', 'plank_texaC', 'plank_texbC', 'rightWall_corridorA', 'roofBack_corridorA', 'shaftBack_corridorA', 'shaftDoorFrame_corridorA', 'shaftFront_corridorA', 'stoneBrick_roundA', 'stoneBrick_roundB', 'stoneBrick_roundC', 'stoneBrick_roundD']
la_liste = ['brush_A', 'mirror_C', 'sedan_A', 'magnifyingGlass_A', 'elevator_A', 'drumSet_A', 'tambourine_A', 'microphone_A', 'tuba_A', 'drumsticks_A', 'galesCrown_A']
la_liste = ['drumsSet_A']
la_liste = ['smallCliff_A']
la_liste = ['backBag_A', 'bellTree_A', 'bellTree_B', 'drumsSet_C', 'campFire_A', 'giantTree_A', 'giantTree_B', 'fallenLog_A', 'glowMushroom_A', 'glowMushroom_B', 'glowMushroom_C', 'glowMushroom_D']
la_liste = ['rootyTree_A', 'rootyTree_C', 'rootyTree_B', 'palmTree_cutA']
la_liste = ['goldenEgg_A']
la_liste = ['colorPalette_B']
la_liste = ['toyHead_A']
la_liste = ['paintBrush_bigA']
la_liste = ['skunksie']
la_liste = ['powderBrush_A']
la_liste = ['galesThrone_throneRoomA']
la_liste = ['ancientPlinth_A', 'ground_generalGardenA', 'kissingPlant_A', 'kissingPlant_B', 'kissingPlant_C', 'kissingPlant_D', 'miniRoots_B', 'piggieStatue_smallA', 'snappingFlower_A', 'snappingFlower_B', 'spikyRoot_A', 'spikyRoot_B', 'spikyRoot_C', 'splitTrunkTree_A', 'splitTrunkTree_B', 'splitTrunkTree_C', 'steppingStone_A', 'steppingStone_B', 'steppingStone_C', 'steppingStone_D', 'steppingStone_E', 'tinyGrassFlowers_D', 'topHeavyTree_A']
la_liste = ['trumpet_A', 'bowlingBall_A', 'gongStick_A']
la_liste = ['ground_viewToWaterFallA', 'hangingVineSmall_B', 'hoopRoot_D', 'mossPatch_hangingA', 'mossPatch_hangingB', 'river_viewToWaterFallA']
la_liste = ['brickEdge_A', 'brickPath_A', 'eggLanding_eggChamberCollapsedA', 'ground_eggChamberA', 'lava_eggChamberA', 'lava_eggChamberB', 'lava_eggChamberC', 'lava_eggChamberD', 'lava_eggChamberE', 'leftWall_eggChamberA', 'piggieStatue_roundedA', 'piggieStatue_roundedB', 'pillarStone_H', 'pillarStone_I', 'pillarStone_J', 'pillarStone_K', 'pillarStone_headA', 'plinthInner_eggChamberCollapsedA', 'plinthOuter_eggChamberCollapsedA', 'pyramidBase_eggChamberCollapsedA', 'pyramidBase_eggChamberCollapsedB', 'pyramidBase_eggChamberCollapsedC', 'pyramidMidBack_eggChamberCollapsedB', 'pyramidMidBottom_eggChamberCollapsedA', 'pyramidMidCrack_eggChamberCollapsedB', 'pyramidMidMid_eggChamberCollapsedA', 'pyramidMidPlatformBack_eggChamberCollapsedB', 'pyramidMidPlatform_eggChamberCollapsedB', 'pyramidMidStairsMid_eggChamberCollapsedC', 'pyramidMidStairsTop_eggChamberCollapsedC', 'pyramidMidTop_eggChamberCollapsedA', 'pyramidMid_eggChamberCollapsedD', 'pyramidTop_eggChamberCollapsedA', 'pyramidTop_eggChamberCollapsedB', 'pyramidTop_eggChamberCollapsedC', 'pyramidTop_eggChamberCollapsedD', 'rightWallTunnel_eggChamberA', 'rightWall_eggChamberA', 'stelactite_E', 'stelactite_F', 'stelactite_G', 'stelactite_H', 'stelactite_I', 'stoneBrick_M', 'stoneBrick_N']
la_liste = ['bowlLeaf_A', 'ground_mudPoolA', 'hoopRoot_E', 'mud_mudPoolA', 'roundMossyBoulder_A', 'roundMossyBoulder_C']
la_liste = ['artwork_paintingRoomA', 'artwork_paintingRoomB', 'artwork_paintingRoomC', 'backWall_paintingRoomA', 'canvas_rolledA', 'canvas_rolledB', 'curtain_paintingRoomA', 'curtain_paintingRoomB', 'door_woodenA', 'easel_B', 'easel_C', 'floorMat_largeB', 'floorMat_largeC', 'floorMat_largeD', 'floor_paintingRoomA', 'frontWall_paintingRoomA', 'galesPortrait_paintingRoomA', 'galesPortrait_paintingRoomB', 'giantPainting_paintingRoomA', 'hallMat_B', 'leftWall_paintingRoomA', 'paintBrush_giantA', 'paintSplash_bigA', 'paintTube_A', 'paintingA', 'paintingB', 'paintingC', 'paintingD', 'paintingE', 'pedestal_paintingRoomA', 'rightWall_paintingRoomA', 'roof_paintingRoomA', 'smallBucket_A', 'stove_A', 'teaPot_A', 'window_paintingRoomA', 'window_paintingRoomB', 'window_paintingRoomC']
la_liste = ['carnivoreWaterLily_B', 'creepingVine_A', 'creepingVine_B', 'creepingVine_C', 'creepingVine_D', 'creepingVine_E', 'creepingVine_F', 'ground_eggPondA', 'ground_eggPondB', 'hangingVineHoop_mediumD', 'lake_eggPondA', 'purpleVine_A', 'purpleVine_B', 'purpleVine_C', 'purpleVine_multiA', 'purpleVine_multiB', 'smallWaterFall_A', 'stoneArchway_A', 'stoneArchway_B', 'stonePlinth_eggPondA', 'tunnelTree_A', 'tunnelTree_B', 'tunnelTree_C', 'waterLily_A', 'waterLily_B']


if __name__ == '__main__':
    # Init Processor
    stella_processor = StellaProcessor()
    # Each Given Asset
    for anima_name in la_liste:
        try:
            # Conform .look
            stella_processor.look_conform(anima_name=anima_name)
        except Exception, e:
            # Verbose
            print e.args