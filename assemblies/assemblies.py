__author__ = 'f.scaduto'

# =====================================
# Imports
import maya.cmds as cmds
import maya.cmds as mc
import maya.mel as mel
import sys, os.path
from pprint import pprint
from tube_libraries import Tube

#sys.path.append(r"\\netapp\shared_workflow\Workflow\C_pipe\API\tube")
#sys.path.append(r"\\netapp\shared_workflow\Workflow\C_pipe\API\scene_manager")
from MayaSceneManagerGeneric import MayaSceneManagerDialog
import general_purpose_libraries
import math
import stella_processor
import common
import functions.clean as clean
reload(clean)
import abc_exporter as abc
reload(abc)

reload(stella_processor)
sp = stella_processor.StellaProcessor()

# load scene assembly plugin
if not cmds.pluginInfo( 'sceneAssembly', q=True, l=True):
    cmds.loadPlugin( 'sceneAssembly' )

# load AbcExport plugin
if not cmds.pluginInfo( 'AbcExport', q=True, l=True):
    cmds.loadPlugin( 'AbcExport' )

# load AbcImport plugin
if not cmds.pluginInfo( 'AbcImport', q=True, l=True):
    cmds.loadPlugin( 'AbcImport' )

# load gpuCache plugin
if not cmds.pluginInfo( 'gpuCache', q=True, l=True):
    cmds.loadPlugin( 'gpuCache' )

# =====================================
def scan_bg_and_create_unique_props_list():
    '''
    Scan a background, list all assamblies ref,
    sort them in uniques name, sort them from another list of already existing assets,
    en write list un txt file (commented)
    :return:
    '''
    # List all transforms of the scene
    scene_list = cmds.ls(type="transform")
    # Create empty list
    assemblies = []

    # List all assemblies of the scene
    for each in scene_list:
        if cmds.objExists(each+".definition") == True:
            definition_path = cmds.getAttr(each+'.definition')
            split_definition_path = definition_path.split('/')
            props_anima_name = str(split_definition_path[-1:][0])
            props_name = props_anima_name.replace("_AD.ma","")
            assemblies.append(props_name)
            '''
            print "> " + each
            print props_anima_name
            print ""
            '''
    # Create empty list
    props_list = []
    # For each assembly, add them to props_list
    for each in assemblies:
        #props_list.append(each[:-1])
        props_list.append(each)

    # Create empty list who contain props with unique names
    unique_props_list = []
    # For each elements in the list, if they are not in the new list, we add them.
    for i in props_list:
        if not i in unique_props_list:
            unique_props_list.append(i)

    # Print unique_props_list
    print str( len(props_list)) + ' props_list found'
    print str( len(unique_props_list)) + ' unique_props_list found'

    # --------------------------------
    # Compare Two lists to check if props are not already ok

    # Open the file text props_list_already_ok
    file_open = open( "P:\\Stella_Serie\\scripts\\S02\\data\\props_list_already_ok.txt", "r" )
    file_log = file.readlines( file_open )[0]
    file.close( file_open )
    # Ajoute la liste dans une variable
    props_list_already_ok = eval(file_log)

    new_unique_props_list = []
    new_props_list_already_ok = []

    # For each elements in the list, if they are not in the new list, we add them.
    for i in unique_props_list:
        if not i in props_list_already_ok:
            new_unique_props_list.append(i)
        else:
            new_props_list_already_ok.append(i)
    # Print unique_props_list
    print str( len(new_unique_props_list)) + ' new_unique_props_list found'
    print str( len(new_props_list_already_ok)) + ' new_props_list_already_ok found'

    '''
    # Ecrit la liste dans un fichier txt

    f = open( "P:\\Stella_Serie\\scripts\\S02\\data\\props_list_tmp.txt", "w" )
    f.write( str(new_unique_props_list) )
    f.close()
    '''

def read_asset_to_generate():
    '''
    Open a list of all assets to generate, use only after the scan_bg_and_create_unique_props_list.
    :return:
    '''
    file_open = open("P:\\Stella_Serie\\scripts\\S02\\data\\props_list_tmp.txt", "r")
    file_log = file.readlines(file_open)[0]
    file.close(file_open)

    anima_names = eval(file_log)
    return anima_names

def get_cube_name(asset_name):
    '''
    Get cube Name, Convert an Anima_name to a cube name if not already a cube name
    :param asset_name:
    :return:
    '''
    if common.assets_last_wips(asset_name):
        cube_name = asset_name
    else:
        cube_name = common.name_convert(anima_name=asset_name)

    return cube_name

def add_tasks_in_tube(in_asset):
    '''
    Ajoute les tasks assemblyDef, modeling, set, setupLOD0 et setupLOD2 aux assets a partir de leurs noms anima
    :param in_asset:
    :return:
    '''
    # Connection to Tube
    with Tube() as tube:
        # Asset Builder
        asset_builder = tube.asset_builder()
        # Parameters
        asset_builder.proj_id = 413
        asset_builder.tasks_ids = [219, 6, 218, 231, 234]  # assemblyDef, modeling, set, setupLOD0, setupLOD2
        asset_builder.users_tasks = [-1, -1, -1, -1, -1]  # Personne
        # Each asset to generate
        for asset_name in in_asset:
            # Get cube name
            cube_name = get_cube_name(asset_name=asset_name)
            # Create tasks and files
            result = asset_builder.add_tasks_asset(asset_name=cube_name)
            # Verbose
        print result, cube_name, asset_name

def save(tube_dict, save_type):
    '''
    Save Wip / Publish
    :param tube_dict:
    :param save_type:
    :return:
    '''
    # Get the scene id
    cmds.fileInfo('SceneId', tube_dict)

    # Create new instance on tube manager
    d = MayaSceneManagerDialog()

    # Save wip to te file open
    if save_type == 'publish':
        # Verbose
        print "SAVE PUBLISH"
        # Save wip first
        d.saveWip()
        # And Save publish
        d.publish()
        # Succes
        return True
    elif save_type == 'wip':
        # Verbose
        print "SAVE WIP"
        # Save wip first
        d.saveWip()
        # Succes
        return True
    # Failure
    print "NOTHING SAVED"
    return False

def zero_out(var):
    '''
    Create offset group zeroOut
    :param var:
    :return:
    '''
    zero_out = cmds.group(em=True, name=var[:-5] + '_zeroOut')
    constraint = cmds.parentConstraint(var, zero_out)
    cmds.delete(constraint)
    cmds.parent(var, zero_out)
    return zero_out

def create_rig_element(in_name, in_type, in_parent=None, in_radius=1, in_color=None):
    '''
    Create controls, set radius, colors, create groups and parent them.
    :param in_name:
    :param in_type:
    :param in_parent:
    :param in_radius:
    :param in_color:
    :return:
    '''
    # --- Create object
    # Grp group
    if in_type == 'grp':
        element = cmds.group(em=True, name=in_name)
        # Parent
        if in_parent:
            cmds.parent(element, in_parent)
    # Ctrl curve
    elif in_type == 'ctrl':
        element = cmds.circle(name=in_name, normal=(0, 1, 0), sections=8, radius=in_radius)[0]
        if in_color:
            cmds.setAttr(element + "Shape.overrideEnabled", 1)
            cmds.setAttr(element + "Shape.overrideColor", in_color)

        element_grp = cmds.group(em=True, name=element[:-5] + '_zeroOut')
        cmds.parent(element, element_grp)
        # Parent
        if in_parent:
            cmds.parent(element_grp, in_parent)
    else:
        print 'no type corresponding found'
        return

    return element

def geometry_set():
    '''
    Build a Geometry Set
    :return:
    '''
    # Scan all transforms descendents of GEO group
    geometry = cmds.listRelatives("GEO", allDescendents=True, type="transform", fullPath=True)

    content = cmds.ls(geometry, dag=True, type="transform")

    # List empty who contain geometries
    geo_set_to_add = []
    # For each transforms in geometry
    for stuff in content:
        # If they ave shape in child, add them to a list
        if cmds.listRelatives(stuff, children=True, shapes=True, fullPath=True):
            geo_set_to_add.append(stuff)

    # Create selection set
    cmds.sets(geo_set_to_add, n="GEOMETRY_SET")

def rig_set():
    '''
    Build a rig set
    :return:
    '''
    # List all nurbsCurves in the RIG group
    controls_shapes = cmds.listRelatives("RIG", allDescendents=True, type="nurbsCurve", fullPath=True)

    # Get the parent shapes
    controls = cmds.listRelatives(controls_shapes, parent=True, fullPath=True)

    # Create selection set
    cmds.sets(controls, n="RIG_SET")

def add_cube_tag_no_ns(node_to_tag, type_name, asset_name, task_name, scene_version):
    '''
    Add cube tag attributs, for modeling, setups, assembly def
    :param node_to_tag:
    :param type_name:
    :param asset_name:
    :param task_name:
    :param scene_version:
    :return:
    '''
    # cube type
    cmds.addAttr(node_to_tag, longName="cube_type", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_type", type_name, type="string")
    # cube name
    cmds.addAttr(node_to_tag, longName="cube_name", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_name", asset_name, type="string")
    # cube_task
    cmds.addAttr(node_to_tag, longName="cube_task", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_task", task_name, type="string")
    # cube version
    cmds.addAttr(node_to_tag, longName="cube_version", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_version", scene_version, type="string")

def add_cube_tag_manual():
    '''
    Add cube tag attributs, but without informations
    :param node_to_tag:
    :return:
    '''
    node_to_tag = cmds.ls(sl=True)
    # cube type
    cmds.addAttr(node_to_tag, longName="cube_type", dataType="string")
    # cube name
    cmds.addAttr(node_to_tag, longName="cube_name", dataType="string")
    # cube_task
    cmds.addAttr(node_to_tag, longName="cube_task", dataType="string")
    # cube version
    cmds.addAttr(node_to_tag, longName="cube_version", dataType="string")

def add_cube_tag_ref(node_to_tag, type_name, asset_name, task_name, scene_version):
    '''
    Add cube tag attributs, for assembly ref
    :param node_to_tag:
    :param type_name:
    :param asset_name:
    :param task_name:
    :param scene_version:
    :return:
    '''
    # cube type
    cmds.addAttr(node_to_tag, longName="cube_type", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_type", type_name, type="string")
    # cube name
    cmds.addAttr(node_to_tag, longName="cube_name", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_name", asset_name, type="string")
    # cube_ns only for assemblies references
    cmds.addAttr(node_to_tag, longName = "cube_ns", dataType = "string")
    # cube_task
    cmds.addAttr(node_to_tag, longName="cube_task", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_task", task_name, type="string")
    # cube version
    cmds.addAttr(node_to_tag, longName="cube_version", dataType="string")
    cmds.setAttr(node_to_tag + ".cube_version", scene_version, type="string")

def lock_hide_attr(node_to_lock_hide):
    '''
    Lock and hide all transforms attributs and visibility
    :param node_to_lock_hide:
    :return:
    '''
    # Create attributs list
    attributs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']
    # For each attributs in list, lock and hide them
    for attribut in attributs:
        cmds.setAttr(node_to_lock_hide+attribut, lock=True, keyable=False)

def clean_scene():
    '''
    From functions.clean we clean the scene
    :return:
    '''
    # --- CLEAN Scene
    # - Remove unused animation Curve
    clean.unused_animCurve_remove()

    # - Remove unknow noReferenced nodes
    clean.unknowNodes_remove()

    # - Remove unused hyperView
    clean.unused_hyperView_remove()

    # - Remove useless_scriptNode
    clean.useless_scriptNode_remove()

    # - Remove fosterParent
    clean.fosterParent_remove()

def create_modeling(in_asset, save_type):
    '''
    import le modeling_LOD1 d'anima, puis fait un wip
    :param in_asset:
    :return:
    '''
    for each in in_asset:
        # Get cube name
        cube_name = get_cube_name(asset_name=each)

        # Get on Tube the asset tasks
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get the dictionary of modeling
        tube_dict_mod = tasks_dicts['modeling']


        # Open the modeling scene
        print tube_dict_mod['scene_path']
        try:
            cmds.file(tube_dict_mod['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass

        # Get the path of geometry
        anima_abc_lod1 = common.geo_by_cube_name(cube_name)
        anima_geometry_lod1 = anima_abc_lod1.replace(".abc", ".mb")

        # Import geometry
        cmds.file(anima_geometry_lod1, i=True, mergeNamespacesOnClash=True)

        # --------------------
        #------ Add tags
        # Name of the object to tag
        node = each

        # List all transforms whith the same name of the asset
        name = cmds.ls(node, type="transform")

        # Reverse in the good order
        name.reverse()

        # Create list empty
        unique_name = []

        # If in the list, an element have not child with shapes, we add it in a list
        for each in name:
            if not cmds.listRelatives(each, children=True, shapes=True):
                unique_name.append(each)

        # Convert to string
        str_unique_name = str(unique_name)

        # Split
        split_str = str_unique_name.split("'")

        # Get the unique name with "|"
        unique_node = split_str[1]

        # If anima tags exists we delete them
        if cmds.objExists(node + ".assetInfoAssetData") == True:
            cmds.deleteAttr(node + ".assetInfoAssetData")

        # Add cube tag attributs
        add_cube_tag_no_ns(node_to_tag = unique_node,
                           type_name = tube_dict_mod['type_name'],
                           asset_name = tube_dict_mod['asset_name'],
                           task_name = tube_dict_mod['task_name'],
                           scene_version = tube_dict_mod['scene_version'])

        # Clean scene
        clean_scene()

        try:
            # Set the scene ID and Save Wip
            save(tube_dict_mod['scene_id'], save_type)
        except:
            pass

        print("    >\n")
        print("    > %s est OK !\n" ) % each
        print("    >\n")

def copy_abc_modeling(in_asset, assets_underscores, assets_descriptions):
    '''
    Copy abc from anima and the publish modeling into modeling datas
    :param in_asset:
    :return:
    '''
    for each in in_asset:
        # Get Cube Name
        cube_name = get_cube_name(asset_name=each)
        # If Name in JSON
        if cube_name:
            # Get on Tube the asset tasks
            tasks_dicts = common.assets_last_wips(cube_name)

            # Get the path of GeometryLOD1
            anima_abc_lod1 = common.geo_by_cube_name(cube_name)

            # Create path of other abc
            anima_abc_lod0_gpu = anima_abc_lod1.replace("LOD1.abc", "LOD0_gpucache.abc")
            anima_abc_lod1_gpu = anima_abc_lod1.replace("LOD1.abc", "LOD1_gpucache.abc")
            anima_abc_lod2_gpu = anima_abc_lod1.replace("LOD1.abc", "LOD2_gpucache.abc")

            # Create path of bbox
            anima_abc_bbox = anima_abc_lod1.replace("LOD1.abc", "BBOX_gpucache.abc")

            # Get the dictionary of modeling
            tube_dict_mod = tasks_dicts['modeling']

            # Create the full name of the asset with his description
            full_cube_asset_name = tube_dict_mod['asset_name'] + "_" + tube_dict_mod['asset_description']

            # Create path of publish modeling
            cube_modeling_ma = tube_dict_mod['publish_p'].replace("/", "\\")

            # Create paths of folders for destinations
            mod_abc_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu" % (assets_descriptions,
                                                                                                  full_cube_asset_name)
            mod_abc_cpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\cpu" % (assets_descriptions,
                                                                                                  full_cube_asset_name)
            mod_ma = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\ma" % (assets_descriptions,
                                                                                       full_cube_asset_name)

            # Create list
            directorys = []
            dir_list = directorys.extend([mod_abc_gpu, mod_abc_cpu, mod_ma])

            # If folders does not exists, we create them
            for each in directorys:
                if not os.path.exists(each):
                    # Create folders
                    os.makedirs(each)

            # Create paths of destinations
            dest_modeling_ma = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\ma\\%s_modeling_LOD1.ma" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])
            dest_abc_lod1_cpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\cpu\\%s_LOD1.abc" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])
            dest_abc_bbox_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu\\%s_BBOX.abc" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])
            dest_abc_lod0_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu\\%s_LOD0.abc" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])
            dest_abc_lod1_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu\\%s_LOD1.abc" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])
            dest_abc_lod2_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu\\%s_LOD2.abc" % (
                assets_descriptions, full_cube_asset_name, assets_underscores + tube_dict_mod['asset_name'])


            # Copy files in the good place
            general_purpose_libraries.FileSystem.copy_file(cube_modeling_ma, dest_modeling_ma)
            general_purpose_libraries.FileSystem.copy_file(anima_abc_lod1, dest_abc_lod1_cpu)
            general_purpose_libraries.FileSystem.copy_file(anima_abc_bbox, dest_abc_bbox_gpu)
            general_purpose_libraries.FileSystem.copy_file(anima_abc_lod0_gpu, dest_abc_lod0_gpu)
            general_purpose_libraries.FileSystem.copy_file(anima_abc_lod1_gpu, dest_abc_lod1_gpu)
            general_purpose_libraries.FileSystem.copy_file(anima_abc_lod2_gpu, dest_abc_lod2_gpu)

            print "  > " + full_cube_asset_name
            print "  > les abc de l'asset ont bien ete copies !\n"

        # If not in JSON
        else:
            # Verbose
            print "%s not found in .json !" % each

def create_setuplod0(in_asset, assets_underscores, assets_descriptions, save_type):
    '''
    Create setupLOD0:
    We get tube dicts, we get full name and path of the setupLOD0 from tube,
    Open the scene, import geometry, create rig, selections sets, tags
    and wip or publish
    :param in_asset:
    :return:
    '''
    for each in in_asset:
        # Get cube name
        cube_name = get_cube_name(asset_name=each)

        # Get on Tube the asset tasks
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get dictionary of setupLOD0
        tube_dict_setuplod0 = tasks_dicts['setupLOD0']

        # Get dictionary of modeling
        tube_dict_mod = tasks_dicts['modeling']

        # Get path publish
        path_mod_publish = tube_dict_mod['publish_p']

        # Open the cube setup scene
        try:
            # Open the scene
            cmds.file(tube_dict_setuplod0['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass

        # Create the full name of the asset with his description
        full_cube_asset_name = tube_dict_setuplod0['asset_name'] + "_" + tube_dict_setuplod0['asset_description']

        try:
            # Import modeling
            cmds.file(path_mod_publish, i=True, mergeNamespacesOnClash=True)
        except:
            pass

        #--------------------
        #------ Add shaders / textures
        try:
            sp.apply_shaders(tube_dict_setuplod0['asset_name'])
        except:
            pass

        #--------------------
        #------ PREPARATION
        node = each

        # List all transforms whith the same name of the asset
        name = cmds.ls(node, type="transform")

        # Reverse in the good order
        name.reverse()

        # Create empty list
        unique_name = []

        # If in the list, an element have not child with shapes, we add it in a list
        for each in name:
            if not cmds.listRelatives(each, children=True, shapes=True):
                unique_name.append(each)

        # Convert to string
        str_unique_name = str(unique_name)

        # Split
        split_str = str_unique_name.split("'")

        # Get the unique name with "|"
        unique_node = split_str[1]

        #--------------------
        #------ BUILD A RIG
        # Get the bounding box
        bbox = cmds.exactWorldBoundingBox(unique_node, ignoreInvisible=True)

        # calculate ctrl size
        bbox_size = [0, 0]
        bbox_size[0] = bbox[3] - bbox[0]
        bbox_size[1] = bbox[5] - bbox[2]

        bbox_size.sort()

        walk_size = bbox_size[1] * 0.8
        master_size = bbox_size[1] * 0.95


        #calculate bbox center
        bbox_center = [0, 0, 0]
        bbox_center[0] = (bbox[0] + bbox[3]) / 2
        bbox_center[1] = (bbox[1] + bbox[4]) / 2
        bbox_center[2] = (bbox[2] + bbox[5]) / 2


        #calculate distance of bbox center to world center
        hypot = math.hypot(bbox_center[0], bbox_center[1])
        distance = math.hypot(hypot, bbox_center[2])

        # Create rig
        root_grp = create_rig_element(in_name=unique_node + "_RIG", in_type='grp')
        geo_grp = create_rig_element(in_name="GEO", in_type='grp', in_parent=root_grp)
        rig_grp = create_rig_element(in_name="RIG", in_type='grp', in_parent=root_grp)
        to_attach_grp = create_rig_element(in_name="TO_ATTACH", in_type='grp', in_parent=rig_grp)
        master_ctrl = create_rig_element(in_name="master_ctrl", in_type='ctrl', in_parent=to_attach_grp,
                                         in_radius=master_size, in_color=13)
        walk_ctrl = create_rig_element(in_name="walk_ctrl", in_type='ctrl', in_parent=master_ctrl,
                                       in_radius=walk_size, in_color=6)

        helper_ctrl = 'helper_ctrl'

        #if distance of bbox center to world center is more than 80% of bbox radius :
        if distance > bbox_size[1] * 0.8:
            cmds.circle(name=helper_ctrl, normal=(0, 1, 0), sections=8, radius=bbox_size[1] * 0.65)[0]
            cmds.xform(helper_ctrl, t=[bbox_center[0], bbox[1], bbox_center[2]])
            of = zero_out(helper_ctrl)
            cmds.parent(of, walk_ctrl)

        # Set le geo group en drawing override : reference
        cmds.setAttr("GEO.overrideEnabled", 1)
        cmds.setAttr("GEO.overrideDisplayType", 2)

        # Parent anima_name to geo grp
        cmds.parent(unique_node, geo_grp)

        # Clean controls history
        cmds.delete(master_ctrl, ch=True)
        cmds.delete(walk_ctrl, ch=True)

        if cmds.objExists(helper_ctrl):
            cmds.parentConstraint(helper_ctrl, geo_grp, mo=True)
            cmds.scaleConstraint(helper_ctrl, geo_grp, mo=True)

            # Clean controls history
            cmds.delete(helper_ctrl, ch=True)
        else:
            # Constrain geo grp to walk ctrl
            cmds.parentConstraint(walk_ctrl, geo_grp, mo=True)
            cmds.scaleConstraint(walk_ctrl, geo_grp, mo=True)

        # Build a geometry set
        geometry_set()

        # Build a rig set
        rig_set()

        # Add tags
        # name of the object to tag
        node = unique_node+"_RIG"

        # Add cube tag attributs
        add_cube_tag_no_ns(node_to_tag = node,
                           type_name = tube_dict_setuplod0['type_name'],
                           asset_name = tube_dict_setuplod0['asset_name'],
                           task_name = tube_dict_setuplod0['task_name'],
                           scene_version = tube_dict_setuplod0['scene_version'])

        # Delete attribut from modeling if exist
        if cmds.objExists(each + ".cube_ns") == True:
            cmds.deleteAttr(each + ".cube_ns")

        # Clean scene
        clean_scene()

        try :
            # Set the scene ID and Save Wip
            save(tube_dict_setuplod0['scene_id'], save_type)
        except:
            print each + " not saved."

def create_setuplod2(in_asset, save_type):
    '''
    Create setupLOD2:
    Check in jason dict if a rig exist, if yes ,
    We get tube dicts, we get full name and path of the setupLOD0 from tube,
    Open the scene, import geometry, create rig, selections sets, tags
    and wip or publish
    :param in_asset:
    :return:
    '''

    for each in in_asset:
        # If not a cube name:
        if not common.assets_last_wips(each):
            # Get the cube name
            cube_name = get_cube_name(asset_name = each)

            # Get on tube the assets tasks
            tasks_dicts = common.assets_last_wips(cube_name)

            # Get on tube the modeling task dict
            tube_dict_setuplod2 = tasks_dicts['setupLOD2']


            # If there is a rig in jason dict
            if common.key_by_cube_name(tube_dict_setuplod2['asset_name'], 'Rig') == "Pas de Dossier":
                # If not
                print ("    >>>-----------------------------------------------------------------------------")
                print ("    >>> Le rig de l'asset '%s' n'existe pas ! " % each)
                print ("    >>>-----------------------------------------------------------------------------")
                pass

            else:
                try:
                    # Open setup cube scene
                    try:
                        # Open scene
                        cmds.file(tube_dict_setuplod2['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
                    except:
                        print "L'asset n'existe pas dans tube.."
                        pass

                    # Get rig path
                    anima_rig_path = common.key_by_cube_name(tube_dict_setuplod2['asset_name'], 'Rig')

                    # Import rig
                    cmds.file(anima_rig_path, i=True, mergeNamespacesOnClash=True)

                    #--------------------
                    #------ Add SHADERS / TEXTURES
                    try:
                        sp.apply_shaders(tube_dict_setuplod2['asset_name'])
                    except:
                        pass

                    #--------------------
                    #------ CONFORM ROOT GROUP
                    # Create correct name
                    root_grp_normalised = each + "_RIG"



                    # If name is not correct
                    if not cmds.objExists(root_grp_normalised):
                        # Get the root group
                        root_grp = cmds.ls(dag=True, type="transform")[4]

                        # Rename root group
                        cmds.rename(root_grp, root_grp_normalised)
                    # If name is correct
                    else:
                        pass

                    # If master control exist
                    if cmds.objExists("master_ctrl") == False:
                        # If master control have not the good name, we ave to do it manualy
                        print ("    >>>-----------------------------------------------------------------------------")
                        print ("    >>> Le master control de l'asset '%s' n'est pas normalise ! " % each)
                        print ("    >>>-----------------------------------------------------------------------------")
                        pass

                    else:
                        #--------------------
                        #------ CONFORM TO ATTACH GROUP
                        # If the to attach group exist we pass, else we create it
                        if cmds.objExists("TO_ATTACH"):
                            pass
                        else:
                            to_attach = cmds.group(name="TO_ATTACH", em=True)
                            cmds.parent(to_attach, "RIG")

                        #--------------------
                        #------ CONFORM MASTER_CTRL
                        # Create offset group for master control
                        offset = zero_out('master_ctrl')

                        # Parent to rig group
                        cmds.parent(offset, 'TO_ATTACH')

                        #--------------------
                        #------ CONFORM WALK_CTRL
                        # Create walk control and his offset
                        # BoundinBox for evaluate the radius of walk control
                        bbox = cmds.exactWorldBoundingBox(each, ignoreInvisible=True)

                        # Calculate the radius of control
                        bbox_size = [0, 0]
                        bbox_size[0] = bbox[3] - bbox[0]
                        bbox_size[1] = bbox[5] - bbox[2]

                        bbox_size.sort()

                        walk_size = bbox_size[1] * 0.8

                        # Create the walk control
                        walk_ctrl = cmds.circle(name="walk_ctrl", normal=(0, 1, 0), sections=8, radius=walk_size)[0]

                        # Set the color of walk control
                        cmds.setAttr(walk_ctrl + "Shape.overrideEnabled", 1)
                        cmds.setAttr(walk_ctrl + "Shape.overrideColor", 6)

                        # Create the zero_out
                        walk_zero_out = zero_out(walk_ctrl)

                        # Parent walk_zero_out to master_ctrl
                        cmds.parent(walk_zero_out, 'master_ctrl')

                        #--------------------
                        #------ REBUILD CONSTRAINTS TO MATCH TO WALK_CTRL
                        # Scan child elements of master control
                        enfants_master_ctrl = cmds.listRelatives("master_ctrl", children=True, type="transform")[:-1]

                        # If there is child under master control, parent them to walk control
                        if enfants_master_ctrl != '':
                            for enfant in enfants_master_ctrl:
                                cmds.parent(enfant, walk_ctrl)

                        # List elemnts with attributs master_ctrl_parent_constraint
                        list_constrains = cmds.ls("*.master_ctrl_parentConstraint1_1W0")

                        # Get the constraints names
                        new_list = []
                        for const in list_constrains:
                            split = const.split('.')[0]
                            new_list.append(split)

                        # Create two list to sort constraints used by Anima
                        # (they have always the same name "parent_constrain")
                        parent_list = []
                        scale_list = []
                        for nl in new_list:
                            # If they are scale constraint, add to list
                            if "scaleConstraint1" in nl:
                                scale_list.append(nl)

                            # If they are parent constraint, add to list
                            if "parentConstraint1" in nl:
                                parent_list.append(nl)

                        # If they are parent constraints in the list
                        if parent_list != '':
                            # For each elements in the list
                            for pl in parent_list:
                                # Get and query the parent
                                contraint_parent = cmds.listRelatives(pl, parent=True, fullPath=True)
                                # Delete constraint
                                cmds.delete(pl)
                                # Create constraint
                                cmds.parentConstraint('walk_ctrl', contraint_parent, maintainOffset=True)

                        # If they are scales constraints in the list
                        if scale_list != '':
                            # For each element in the list
                            for sl in scale_list:
                                # Get and query parent
                                scale_parent = cmds.listRelatives(sl, parent=True, fullPath=True)
                                # Delete constraint
                                cmds.delete(sl)
                                # Create constraint
                                cmds.scaleConstraint('walk_ctrl', scale_parent, maintainOffset=True)

                        # List elements with attribut master_ctrlW0
                        bad_rename_anima_list_constrains = cmds.ls("*.master_ctrlW0")

                        # Get constraints names
                        bad_rename_anima_new_list = []
                        for b_const in bad_rename_anima_list_constrains:
                            bad_rename_split = b_const.split('.')[0]
                            bad_rename_anima_new_list.append(bad_rename_split)

                        # Create two another lists
                        bad_rename_anima_parent_list = []
                        bad_rename_anima_scale_list = []
                        for b_rename in bad_rename_anima_new_list:
                            # If they are scales constraints in the list
                            if "scaleConstraint1" in b_rename:
                                bad_rename_anima_scale_list.append(b_rename)

                            # If they are parent constraints in the list
                            if "parentConstraint1" in b_rename:
                                bad_rename_anima_parent_list.append(b_rename)

                        # If they are parents constraints in list
                        if bad_rename_anima_parent_list != '':
                            # For each elements in the list
                            for b_rename_a_p in bad_rename_anima_parent_list:
                                # Get and query parent
                                contraint_parent = cmds.listRelatives(b_rename_a_p, parent=True, fullPath=True)
                                # Delete constraint
                                cmds.delete(b_rename_a_p)
                                # Create constraint
                                cmds.parentConstraint('walk_ctrl', contraint_parent, maintainOffset=True)

                        # If they are scale constrantin in the list
                        if bad_rename_anima_scale_list != '':
                            # For each elements in the list
                            for b_rename_a_s in bad_rename_anima_scale_list:
                                # Get and query parent
                                scale_parent = cmds.listRelatives(b_rename_a_s, parent=True, fullPath=True)
                                # Delete constraint
                                cmds.delete(b_rename_a_s)
                                # Create constraint
                                cmds.scaleConstraint('walk_ctrl', scale_parent, maintainOffset=True)

                        # Build a geometry set
                        geometry_set()

                        # Build a rig set
                        rig_set()

                        #--------------------
                        #------ Add tags
                        # Object to tag
                        node = each + "_RIG"

                        # Add cube tag attributs
                        add_cube_tag_no_ns(node_to_tag = node,
                                           type_name = tube_dict_setuplod2['type_name'],
                                           asset_name = tube_dict_setuplod2['asset_name'],
                                           task_name = tube_dict_setuplod2['task_name'],
                                           scene_version = tube_dict_setuplod2['scene_version'])

                        #--------------------
                        #------ Clean tags attributs form Anima
                        # Delete tag info asset data
                        if cmds.objExists("*.assetInfoAsset") == True:
                            cmds.deleteAttr("*.assetInfoAsset")
                        # Delete tag assetInfoAssetContainer
                        if cmds.objExists("*.assetInfoAssetContainer") == True:
                            cmds.deleteAttr("*.assetInfoAssetContainer")
                        # Delete tag assetInfoAssetData
                        if cmds.objExists("*.assetInfoAssetData") == True:
                            cmds.deleteAttr("*.assetInfoAssetData")
                        # Delete tag defaultCharProfileVersion
                        if cmds.objExists("*.defaultCharProfileVersion") == True:
                            cmds.setAttr("*.defaultCharProfileVersion", lock=False)
                            cmds.deleteAttr("*.defaultCharProfileVersion")

                        # Clean scene
                        clean_scene()

                        # Set the scene ID and Save Wip
                        save(tube_dict_setuplod2['scene_id'], save_type)


                        # Print
                        print ("    >>>-----------------------------------------------------------------------------")
                        print ("    >>> Le rig de l'asset '%s' a ete correctement normalise et enregistre ! " % each)
                        print ("    >>>-----------------------------------------------------------------------------")

                except:
                    print "    >>>"
                    print "    >>> " + tube_dict_setuplod2['asset_description']
                    print "    >>>"
                    pass
        else:
            # Get cube name
            cube_name = get_cube_name(asset_name=each)

            # Get on Tube the asset tasks
            tasks_dicts = common.assets_last_wips(cube_name)

            # Get dictionary of setupLOD0
            tube_dict_setuplod0 = tasks_dicts['setupLOD0']

            # Get path publish
            path_setuplod0 = tube_dict_setuplod0['publish_p']

            # Get dictionary of setupLOD2
            tube_dict_setuplod2 = tasks_dicts['setupLOD2']

            # Open the cube setup scene
            try:
                # Open the scene
                cmds.file(tube_dict_setuplod2['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
            except:
                pass

            try:
                # Import setupLOD0
                cmds.file(path_setuplod0, i=True, mergeNamespacesOnClash=True)
            except:
                pass

            # Set attr of cube task
            cmds.setAttr(each + "_RIG" + ".cube_task", "setupLOD2", type="string")

            # Clean scene
            clean_scene()

            # Set the scene ID and Save Wip
            save(tube_dict_setuplod2['scene_id'], save_type)

            # Print
            print ("    >>>-----------------------------------------------------------------------------")
            print ("    >>> Le setupLOD0 de l'asset '%s' a ete correctement enregistre en setupLOD2! " % each)
            print ("    >>>-----------------------------------------------------------------------------")

def create_assembly_def(in_asset, assets_underscores, assets_descriptions, save_type):
    '''
    Create assembly Def:
    Open assembly def scene from cube,
    Create abc path, and rig path,
    Create assembly, and add representations,
    Then save wip or publish
    :param in_asset:
    :return:
    '''
    for each in in_asset:
        # Get cube name
        cube_name = get_cube_name(asset_name = each)

        # Get on tube the assets tasks
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get from cube the task dict for assemblyDef
        tube_dict_ad = tasks_dicts['assemblyDef']

        # Open scene
        try:
            cmds.file(tube_dict_ad['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass

        #--------------------
        #------ Create abc path
        # Create full name with description
        full_cube_asset_name = tube_dict_ad['asset_name'] + "_" + tube_dict_ad['asset_description']

        # Create path of folders
        doc_abc_gpu = "$CUBE_PROJECT_DATAS/asset/%s/%s/modeling/datas/abc/gpu/" % (assets_descriptions,
                                                                                   full_cube_asset_name)
        doc_setup_LOD0 = "$CUBE_PROJECT_DATAS/asset/%s/%s/setupLOD0/" % (assets_descriptions, full_cube_asset_name)
        doc_setup_LOD2 = "$CUBE_PROJECT_DATAS/asset/%s/%s/setupLOD2/" % (assets_descriptions, full_cube_asset_name)

        # Rebuild full path of representations
        representation_abc_bbox_gpucache = doc_abc_gpu + assets_underscores + tube_dict_ad['asset_name'] + "_BBOX.abc"
        representation_abc_lod0_gpucache = doc_abc_gpu + assets_underscores + tube_dict_ad['asset_name'] + "_LOD0.abc"
        representation_abc_lod1_gpucache = doc_abc_gpu + assets_underscores + tube_dict_ad['asset_name'] + "_LOD1.abc"
        representation_abc_lod2_gpucache = doc_abc_gpu + assets_underscores + tube_dict_ad['asset_name'] + "_LOD2.abc"
        representation_setup_LOD0 = doc_setup_LOD0 + assets_underscores + tube_dict_ad['asset_name'] + "_setupLOD0_" +\
                                    tube_dict_ad['asset_description'] + ".ma"
        representation_setup_LOD2 = doc_setup_LOD2 + assets_underscores + tube_dict_ad['asset_name'] + "_setupLOD2_" +\
                                    tube_dict_ad['asset_description'] + ".ma"


        #--------------------
        #------ Create assembly def
        # Create name for assembly def
        assembly_def = "AD_" + each

        if cmds.objExists(assembly_def) == True:
            cmds.delete(assembly_def)

        # Create empty assembly with the name of the asset
        cmds.createNode('assemblyDefinition', n=assembly_def)

        if assets_descriptions == "PR_props":
            # Create 6 representations
            cmds.setAttr(".rep", s=6)

            # Create BBOX representation
            # Name
            cmds.setAttr(".rep[0].rna", "BBOX_gpuCache", type="string")
            # Label
            cmds.setAttr(".rep[0].rla", "BBOX", type="string")
            # Type
            cmds.setAttr(".rep[0].rty", "Cache", type="string")
            # Data
            cmds.setAttr(".rep[0].rda", representation_abc_bbox_gpucache, type="string")

            # Create LOD0 representation
            # Name
            cmds.setAttr(".rep[1].rna", "LOD0_gpuCache", type="string")
            # Label
            cmds.setAttr(".rep[1].rla", "LOD0", type="string")
            # Type
            cmds.setAttr(".rep[1].rty", "Cache", type="string")
            # Data
            cmds.setAttr(".rep[1].rda", representation_abc_lod0_gpucache, type="string")

            # Create LOD1 representation
            # Name
            cmds.setAttr(".rep[2].rna", "LOD1_gpuCache", type="string")
            # Label
            cmds.setAttr(".rep[2].rla", "LOD1", type="string")
            # Type
            cmds.setAttr(".rep[2].rty", "Cache", type="string")
            # Data
            cmds.setAttr(".rep[2].rda", representation_abc_lod1_gpucache, type="string")

            # Create LOD2 representation
            # Name
            cmds.setAttr(".rep[3].rna", "LOD2_gpuCache", type="string")
            # Label
            cmds.setAttr(".rep[3].rla", "LOD2", type="string")
            # Type
            cmds.setAttr(".rep[3].rty", "Cache", type="string")
            # Data
            cmds.setAttr(".rep[3].rda", representation_abc_lod2_gpucache, type="string")

            # Create setupLOD0 representation
            # Name
            cmds.setAttr(".rep[4].rna", "setupLOD0", type="string")
            # Label
            cmds.setAttr(".rep[4].rla", "setupLOD0", type="string")
            # Type
            cmds.setAttr(".rep[4].rty", "Scene", type="string")
            # Data
            cmds.setAttr(".rep[4].rda", representation_setup_LOD0, type="string")

            # IF the setupLOD2 have a publish, we create representation
            # Path of publish setupLOD2
            path_pub_setupLOD2 = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\setupLOD2\\%s_setupLOD2_%s.ma" % \
                                 (assets_descriptions, full_cube_asset_name,
                                  assets_underscores + tube_dict_ad['asset_name'], tube_dict_ad['asset_description'])

            if os.path.exists(path_pub_setupLOD2):
                # Create setupLOD2 representation
                # Name
                cmds.setAttr(".rep[5].rna", "setupLOD2", type="string")
                # Label
                cmds.setAttr(".rep[5].rla", "setupLOD2", type="string")
                # Type
                cmds.setAttr(".rep[5].rty", "Scene", type="string")
                # Data
                cmds.setAttr(".rep[5].rda", representation_setup_LOD2, type="string")

        if not assets_descriptions == "PR_props":
            # Create 6 representations
            cmds.setAttr(".rep", s=2)

            # Create setupLOD0 representation
            # Name
            cmds.setAttr(".rep[0].rna", "setupLOD0", type="string")
            # Label
            cmds.setAttr(".rep[0].rla", "setupLOD0", type="string")
            # Type
            cmds.setAttr(".rep[0].rty", "Scene", type="string")
            # Data
            cmds.setAttr(".rep[0].rda", representation_setup_LOD0, type="string")

            # IF the setupLOD2 have a publish, we create representation
            # Path of publish setupLOD2
            path_pub_setupLOD2 = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\setupLOD2\\%s_setupLOD2_%s.ma" % \
                                 (assets_descriptions, full_cube_asset_name,
                                  assets_underscores + tube_dict_ad['asset_name'], tube_dict_ad['asset_description'])

            if os.path.exists(path_pub_setupLOD2):
                # Create setupLOD2 representation
                # Name
                cmds.setAttr(".rep[1].rna", "setupLOD2", type="string")
                # Label
                cmds.setAttr(".rep[1].rla", "setupLOD2", type="string")
                # Type
                cmds.setAttr(".rep[1].rty", "Scene", type="string")
                # Data
                cmds.setAttr(".rep[1].rda", representation_setup_LOD2, type="string")

        #--------------------
        #------ Add tags
        # name of object to tag
        node = assembly_def

        # Add cube tag attributs
        add_cube_tag_no_ns(node_to_tag = node,
                           type_name = tube_dict_ad['type_name'],
                           asset_name = tube_dict_ad['asset_name'],
                           task_name = tube_dict_ad['task_name'],
                           scene_version = tube_dict_ad['scene_version'])

        # Clean scene
        clean_scene()

        try:
            # Set the scene ID and Save Wip
            save(tube_dict_ad['scene_id'], save_type)

        except:
            pass

def create_assembly_ref(in_asset, assets_underscores, save_type):
    '''
    Create assembly Ref ( Set ):
    Open set scene, if assemblyref already exist, we delete it,
    we create assembly ref, with tags, and save wip or publish
    :param in_asset:
    :return:
    '''
    for each in in_asset:
        # Get cube name
        cube_name = get_cube_name(asset_name = each)

        # Get on tube, the asset tasks
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get set dict and assemblyDef dict
        tube_dict_set = tasks_dicts['set']
        tube_dict_ad = tasks_dicts['assemblyDef']

        # --------------------
        #------ OPEN ASSEMBLYDEF CUBE
        #
        try:
            cmds.file(tube_dict_set['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass

        #--------------------
        #------ CLEAN SCENE
        #
        # Scan transforms in the scene
        transforms = cmds.ls(type="transform")

        # If an assembly already exist, we delete it
        for each in transforms:
            if cmds.objExists(each + ".assemblyEdits") == True:
                cmds.delete(each)
            else:
                pass


        #--------------------
        #------ Create l'assembly
        #
        # Create empty assembly ref
        create_assembly = cmds.assembly(name=assets_underscores + tube_dict_ad['asset_name'] + "_MODEL_001",
                                        type="assemblyReference")

        # Add env cube in path
        # publish path
        path_publish = tube_dict_ad['publish_p']

        # replace path
        env_pub = path_publish.replace("P:/Stella_Serie/projet/", "$CUBE_PROJECT_DATAS/")

        # add path in assembly ref
        cmds.setAttr(create_assembly + ".definition", env_pub, type="string")

        # Modify namespace
        cmds.setAttr(create_assembly + ".repNamespace", tube_dict_ad['asset_name'] + "_001", type="string")

        #--------------------
        #------ Add tags
        # name of object to tag
        node = create_assembly

        add_cube_tag_ref(node_to_tag = node,
                         type_name = tube_dict_set['type_name'],
                         asset_name = tube_dict_set['asset_name'],
                         task_name = tube_dict_set['task_name'],
                         scene_version = tube_dict_set['scene_version'])

        # If its a character
        if assets_underscores == "CH_":
            # Lock and hide all attributs and visibility
            lock_hide_attr(node_to_lock_hide=node)
        else:
            pass

        # Clean scene
        clean_scene()

        try:

            # Set the scene ID and Save Wip
            save(tube_dict_set['scene_id'], save_type)

        except:
            pass

def open_cube_setuplod0(in_asset):
    '''
    Open a scene of setupLOD0
    :param in_asset:
    :return:
    '''
    # Get cube name
    cube_name = get_cube_name(asset_name = in_asset)

    # Get tasks dict
    tasks_dicts = common.assets_last_wips(cube_name)

    # Get setupLOD0 dict
    tube_dict_setuplod0 = tasks_dicts['setupLOD0']

    # Open cube setuplod0 scene
    try:
        # Open scene
        cmds.file(tube_dict_setuplod0['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
    except:
        pass

def replace_assemblies_data():
    '''
    Replace assemblies datas, and add tag
    :return:
    '''

    # List all transforms from the scene
    scene_list = cmds.ls(type="transform")
    # Create empty lists
    assemblies = []
    assemblies_ref = []

    # List all assemblies
    for each in scene_list:
        if cmds.objExists(each + ".definition") == True:
            definition_path = cmds.getAttr(each + '.definition')
            split_definition_path = definition_path.split('/')
            props_anima_name = str(split_definition_path[-1:][0])
            props_name = props_anima_name.replace("_AD.ma", "")
            assemblies.append(props_name)
            assemblies_ref.append(each)

    print assemblies_ref

    # For each assemblies, add them to the props_list
    for each in assemblies_ref:

        print each
        removed_digit = common.remove_last_digits(each)
        cube_name = common.name_convert(anima_name=removed_digit)

        # Get tasks dicts
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get assemblyDef dict
        tube_dict_ad = tasks_dicts['assemblyDef']

        # Get set dict
        tube_dict_set = tasks_dicts['set']

        # Add env cube path
        # publish path
        path_publish = tube_dict_ad['publish_p']

        # replace env cube var
        env_pub = os.path.normpath(os.path.normpath(path_publish).replace(os.path.expandvars("$CUBE_PROJECT_DATAS"),
                                                                          "$CUBE_PROJECT_DATAS")).replace('\\', '/')

        # Change path in assembly
        cmds.setAttr(each + ".definition", env_pub, type="string")

        # --------------------
        #------ Clean anima tags attributs
        # delete tag info asset data
        if cmds.objExists(each + ".assetInfoAsset") == True:
            cmds.deleteAttr(each + ".assetInfoAsset")
        # delete tag assetInfoAssetContainer
        if cmds.objExists(each + ".assetInfoAssetContainer") == True:
            cmds.deleteAttr(each + ".assetInfoAssetContainer")
        # delete tag assetInfoAssetData
        if cmds.objExists(each + ".assetInfoAssetData") == True:
            cmds.deleteAttr(each + ".assetInfoAssetData")
        # delete tag defaultCharProfileVersion
        if cmds.objExists(each + ".defaultCharProfileVersion") == True:
            cmds.setAttr(each + ".defaultCharProfileVersion", lock=False)
            cmds.deleteAttr(each + ".defaultCharProfileVersion")
        # delete tag  assetImprint
        if cmds.objExists(each + ".assetInfoAssetImprint") == True:
            cmds.deleteAttr(each + ".assetInfoAssetImprint")

        add_cube_tag_ref(node_to_tag = each,
                         type_name = tube_dict_set['type_name'],
                         asset_name = tube_dict_set['asset_name'],
                         task_name = tube_dict_set['task_name'],
                         scene_version = tube_dict_set['scene_version'])

        print each + " OK !"

def create_rig():
    '''
    Create a rig like a setupLOD0, and add attributs without informations
    :param in_asset:
    :return:
    '''
    # --------------------
    #------ BUILD A RIG
    in_asset = cmds.ls(sl=True)
    # boundinbox
    bbox = cmds.exactWorldBoundingBox(in_asset, ignoreInvisible=True)

    # calculate ctrl size
    bbox_size = [0, 0]
    bbox_size[0] = bbox[3] - bbox[0]
    bbox_size[1] = bbox[5] - bbox[2]

    bbox_size.sort()

    walk_size = bbox_size[1] * 0.8
    master_size = bbox_size[1] * 0.95


    #calculate bbox center
    bbox_center = [0, 0, 0]
    bbox_center[0] = (bbox[0] + bbox[3]) / 2
    bbox_center[1] = (bbox[1] + bbox[4]) / 2
    bbox_center[2] = (bbox[2] + bbox[5]) / 2


    #calculate distance of bbox center to world center
    hypot = math.hypot(bbox_center[0], bbox_center[1])
    distance = math.hypot(hypot, bbox_center[2])

    # Create rig
    root_grp = create_rig_element(in_name=in_asset[0] + "_RIG", in_type='grp')
    geo_grp = create_rig_element(in_name="GEO", in_type='grp', in_parent=root_grp)
    rig_grp = create_rig_element(in_name="RIG", in_type='grp', in_parent=root_grp)
    to_attach_grp = create_rig_element(in_name="TO_ATTACH", in_type='grp', in_parent=rig_grp)
    master_ctrl = create_rig_element(in_name="master_ctrl", in_type='ctrl', in_parent=to_attach_grp,
                                     in_radius=master_size, in_color=13)
    walk_ctrl = create_rig_element(in_name="walk_ctrl", in_type='ctrl', in_parent=master_ctrl, in_radius=walk_size,
                                   in_color=6)

    helper_ctrl = 'helper_ctrl'

    #if distance of bbox center to world center is more than 80% of bbox radius :
    if distance > bbox_size[1] * 0.8:
        cmds.circle(name=helper_ctrl, normal=(0, 1, 0), sections=8, radius=bbox_size[1] * 0.65)[0]
        cmds.xform(helper_ctrl, t=[bbox_center[0], bbox[1], bbox_center[2]])
        of = zero_out(helper_ctrl)
        cmds.parent(of, walk_ctrl)

    # Set geo group in drawing override : reference
    cmds.setAttr("GEO.overrideEnabled", 1)
    cmds.setAttr("GEO.overrideDisplayType", 2)

    # Parent anima_name to geo grp
    cmds.parent(in_asset, geo_grp)

    # clean history controls
    cmds.delete(master_ctrl, ch=True)
    cmds.delete(walk_ctrl, ch=True)

    if cmds.objExists(helper_ctrl):
        cmds.parentConstraint(helper_ctrl, geo_grp, mo=True)
        cmds.scaleConstraint(helper_ctrl, geo_grp, mo=True)

        # clean history controls
        cmds.delete(helper_ctrl, ch=True)
    else:
        # Constraint geo grp to walk ctrl
        cmds.parentConstraint(walk_ctrl, geo_grp, mo=True)
        cmds.scaleConstraint(walk_ctrl, geo_grp, mo=True)

    try:
        # Build geometry set
        geometry_set()
    except:
        pass

    # Build rig set
    rig_set()

    #--------------------
    #------ Add tags
    # object name to tag
    node = in_asset + "_RIG"

    # Add tags without informations
    # cube type
    cmds.addAttr(node, longName="cube_type", dataType="string")
    # cube name
    cmds.addAttr(node, longName="cube_name", dataType="string")
    # cube_task
    cmds.addAttr(node, longName="cube_task", dataType="string")
    # cube version
    cmds.addAttr(node, longName="cube_version", dataType="string")

    # Clean scene
    clean_scene()

def create_lods_abc(assets_underscores, assets_descriptions):
    '''
    Create lod representation for assembly, from selected group in maya
    :param assets_underscores:
    :param assets_descriptions:
    :return:
    '''
    selected_group = cmds.ls(sl=True)
    cube_name = selected_group[0]
    # If Name in JSON
    if cube_name:
        # Get tasks dicts
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get modeling dict
        tube_dict_mod = tasks_dicts['modeling']

        # Create full name with description
        full_cube_asset_name = tube_dict_mod['asset_name'] + "_" + tube_dict_mod['asset_description']

        # Create publish modeling path
        cube_modeling_ma = tube_dict_mod['publish_p'].replace("/","\\")

        # Create destination folders path
        mod_abc_gpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu" % (assets_descriptions,
                                                                                              full_cube_asset_name)
        mod_abc_cpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\cpu" % (assets_descriptions,
                                                                                              full_cube_asset_name)
        mod_ma = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\ma" % (assets_descriptions,
                                                                                   full_cube_asset_name)
        shad_abc_cpu = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\shading\\datas\\abc" % (assets_descriptions,
                                                                                   full_cube_asset_name)

        # Create list
        directorys = []
        dir_list = directorys.extend([mod_abc_gpu, mod_abc_cpu, mod_ma, shad_abc_cpu])

        # inf folder does not exists, we create it
        for each in directorys:
            if not os.path.exists(each):
                # Create folder
                os.makedirs(each)

        # Create path for abc
        path_abc_shad = "P:/Stella_Serie/projet/asset/%s/%s/shading/datas/abc/%s_MODEL_001.abc" % (
            assets_descriptions, full_cube_asset_name, cube_name)
        path_abc_mod = "P:/Stella_Serie/projet/asset/%s/%s/modeling/datas/abc/cpu/%s%s_LOD1.abc" % (
            assets_descriptions, full_cube_asset_name, assets_underscores, cube_name)

        print "ABC created in modeling : "+path_abc_mod


        # Create ABC
        abc.make_abc([cube_name], path_abc_shad)
        print "ABC created in shading : "+path_abc_shad
        abc.make_abc([cube_name], path_abc_mod)


        # =============================
        # Generate BBOX

        # Get exact positions of each bbox point position
        x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(selected_group, calculateExactly=True)

        # Create BBOX
        bbox_geo = cmds.polyCube(name = "%s%s_BBOX" % (assets_underscores, selected_group[0]))[0]

        # Move each vertex
        cmds.move(x1, '%s.f[5]' % bbox_geo, x=True)
        cmds.move(y1, '%s.f[3]' % bbox_geo, y=True)
        cmds.move(z1, '%s.f[2]' % bbox_geo, z=True)
        cmds.move(x2, '%s.f[4]' % bbox_geo, x=True)
        cmds.move(y2, '%s.f[1]' % bbox_geo, y=True)
        cmds.move(z2, '%s.f[0]' % bbox_geo, z=True)

        # =============================
        # Generate LOD0 LOD1 LOD2

        # Create names representations
        bbox = assets_underscores + selected_group[0] + "_BBOX"
        lod0 = assets_underscores + selected_group[0] + "_LOD0"
        lod1 = assets_underscores + selected_group[0] + "_LOD1"
        lod2 = assets_underscores + selected_group[0] + "_LOD2"

        # Create a list for loop
        lods = (lod0, lod1, lod2)

        to_dup = [mesh for mesh in cmds.listRelatives(cube_name, shapes=False, ad=True) if cmds.listRelatives(mesh, shapes=True)]

        for each in lods:
            lod_dup = []
            for mesh in to_dup:
                dup = cmds.duplicate(mesh, n=mesh + '_dup')
                lod_dup.append(dup[0])
                #reduce
                if each == lod0:
                    cmds.polyReduce(dup, percentage=60, keepBorder=True)
                    cmds.delete(dup, constructionHistory=True)
                #smooth
                elif each == lod2:
                    cmds.polySmooth(dup, divisions=1)
                    cmds.delete(dup, constructionHistory=True)
                else:
                    pass
            cmds.group(lod_dup, n=each)
            cmds.parent(each, w=True)

        # for the modeling
        dest_modeling_ma = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\ma\\%s_modeling_LOD1.ma" % (
            assets_descriptions, full_cube_asset_name, assets_underscores+tube_dict_mod['asset_name'])


        # Copy files in good place
        # For modeling
        general_purpose_libraries.FileSystem.copy_file(cube_modeling_ma, dest_modeling_ma)
        # =============================
        # EXPORTS GPU caches

        # Create path to gpu
        gpu_path = mod_abc_gpu
        # Create gpuCaches
        cmds.gpuCache(bbox, startTime = 1, endTime = 1, optimize = True, optimizationThreshold = 40000,
                      writeMaterials = True, directory = gpu_path, fileName = bbox)
        cmds.gpuCache(lod0, startTime = 1, endTime = 1, optimize = True, optimizationThreshold = 40000,
                      writeMaterials = True, directory = gpu_path, fileName = lod0)
        cmds.gpuCache(lod1, startTime = 1, endTime = 1, optimize = True, optimizationThreshold = 40000,
                      writeMaterials = True, directory = gpu_path, fileName = lod1)
        cmds.gpuCache(lod2, startTime = 1, endTime = 1, optimize = True, optimizationThreshold = 40000,
                      writeMaterials = True, directory = gpu_path, fileName = lod2)

        print "  > "+full_cube_asset_name
        print "  > les abc de l'asset ont bien ete copies !\n"


    # If not in JSON
    else:
        # Verbose
        print "%s not found in .json !" % each


def replace_selected_assemblies_data(cube_name):
    '''
    Replace selected assemblies data by another data
    '''
    # Get the selection
    selected_assemblies = cmds.ls(sl=True, type="transform")

    # Get cube name
    get_name = get_cube_name(asset_name = cube_name[0])

    # Get on tube, the asset tasks
    tasks_dicts = common.assets_last_wips(get_name)

    # Get assemblyDef dict
    tube_dict_ad = tasks_dicts['assemblyDef']

    # Get publish path
    path_publish = tube_dict_ad['publish_p']

    # replace path
    env_pub = path_publish.replace("P:/Stella_Serie/projet/", "$CUBE_PROJECT_DATAS/")

    #env_pub = "D:\\Stella_serie\\projet\\asset\\PR_props\\bean001_beanbag\\assembly_def\\assembly_def_lod2.ma"

    # For each assemblies
    for each in selected_assemblies:
        # Change assembly path
        cmds.setAttr(each+".definition", env_pub, type="string")

        # Change assembly cube name Tag
        cmds.setAttr(each+".cube_name", cube_name[0], type="string")

        print each+" have been replaced ! :)"

def replace_selected_by_assemblies(assembly_to_deploy):
    '''
    Replace selected object by assemblies, without delete source
    '''
    # Get selected items
    selected_items = cmds.ls(sl=True, type="transform")

    # Check if set exist
    if not cmds.objExists("replaced_elements_set"):
        # Create empty set
        replaced_elements_set = cmds.sets(n="replaced_elements_SET")

    # For each item in selected items
    for item in selected_items:
        item_translate = cmds.xform(item,q=True,t=True, ws=True)
        item_rotation = cmds.xform(item,q=True,ro=True, ws=True)
        item_scale = cmds.xform(item,q=True,s=True, ws=True)

        assembly_replacement = cmds.duplicate(assembly_to_deploy[0])

        cmds.xform(assembly_replacement, t=item_translate, ro=item_rotation, s=item_scale)

        # Add assembly to converted_elements_SET
        cmds.sets(item, forceElement="replaced_elements_SET", edit=True)

        print item+" is now in place ! :P"

def create_gpuCache_node(gpuCache_name, gpuCache_path):
    # Create a new gpuCache
    new_gpuCache = cmds.createNode('gpuCache',n=gpuCache_name+'Shape#')
    cmds.setAttr(new_gpuCache+'.cacheFileName', gpuCache_path,
        type="string",e=1)
    cmds.setAttr(new_gpuCache+'.cacheGeomPath',"|",
        type="string",e=1)

    # Get the parent node transform
    parent_node_transform = cmds.listRelatives(new_gpuCache, parent=True)

    # Rename the new gpuCache
    new_gpuCache_name = cmds.rename(parent_node_transform, gpuCache_name)

    return new_gpuCache_name

def get_transforms_import_and_snap(node, node_path, node_element_grp, rep):
    # Get transforms
    assembly_translate = cmds.xform(node, q=True, t=True, ws=True)
    assembly_rotation = cmds.xform(node ,q=True, ro=True, ws=True)
    assembly_scale = cmds.xform(node, q=True, s=True, ws=True)

    if rep == "geometry":
        # define TMP nameSpace
        TMP_nameSpace= "replacement_TMP"

        # Import
        cmds.file(node_path, i=True, mergeNamespacesOnClash=True, namespace = TMP_nameSpace)

        # Create a temporary list
        get_parent = cmds.listRelatives( TMP_nameSpace+ ':*', parent = True, shapes=False, allDescendents=False, fullPath=True)

        # Create a temporary list
        parent_node = []

        # Get parent node
        for each in get_parent:
            split_each = each.split("|")
            if not split_each[1] in parent_node:
                parent_node.append(split_each[1])

        # Parent item imported to converted elements group
        if parent_node:
            for item in parent_node:
                cmds.parent( '|'+ item, 'TMP_ROOT')

        # Sets transforms on the geometry imported
        cmds.xform(parent_node, t=assembly_translate, ro=assembly_rotation, s=assembly_scale)

        # Clean namespace
        if cmds.namespace( exists='replacement_TMP'):
            cmds.namespace(moveNamespace=('replacement_TMP', ":"), force=True)
            cmds.namespace(removeNamespace='replacement_TMP', force=True)

    if rep == "gpuCache":
        # Create node
        gpuCache_node = create_gpuCache_node(gpuCache_name=node, gpuCache_path=node_path)

        # Parent item imported to converted elements group
        cmds.parent(gpuCache_node, node_element_grp)

        # Sets transforms on the geometry imported
        cmds.xform(gpuCache_node, t=assembly_translate, ro=assembly_rotation, s=assembly_scale)

def convert_assembly_to(representation):
    '''
    Get the selection, get the path, import and match world space transformations
    '''
    # Get selected items
    item_list = cmds.ls(sl=True, type="transform")

    # Create empty list
    assemblies_ref = []

    # Get selected assemblies list
    for each in item_list:
        if cmds.objExists(each + ".definition") == True:
            assemblies_ref.append(each)

    # Check if group exist
    if not cmds.objExists("converted_elements_GRP"):
        # Create empty group
        converted_elements_grp = cmds.group(em=True, name="converted_elements_GRP")
        # Clear selection to dont add group to set
        cmds.select(clear=True)

    # Check if set exist
    if not cmds.objExists("converted_elements_SET"):
        # Create empty set
        converted_elements_set = cmds.sets(n="converted_elements_SET" )

    # Get the real name of asset in assembly
    for each in assemblies_ref:
        definition_path = cmds.getAttr(each + '.definition')
        split_definition_path = definition_path.split('/')
        props_anima_name = str(split_definition_path[-1:][0])
        split_name = props_anima_name.split("_")
        props_name = split_name[1]

        # Get cube name
        cube_name = get_cube_name(asset_name = props_name)

        # Get on tube, the asset tasks
        tasks_dicts = common.assets_last_wips(cube_name)

        # Get geometry dict
        tube_dict_geo = tasks_dicts['modeling']

        # Set variables
        assets_descriptions = tube_dict_geo['type_name']+"_"+tube_dict_geo['type_description']
        assets_underscores = tube_dict_geo['type_name']


        if representation == "gpuCache":
            # Create the full name of the asset with his description
            full_cube_asset_name = tube_dict_geo['asset_name'] + "_" + tube_dict_geo['asset_description']

            gpucache_lod1_path = "P:\\Stella_Serie\\projet\\asset\\%s\\%s\\modeling\\datas\\abc\\gpu\\%s_LOD1.abc" % (
                    assets_descriptions, full_cube_asset_name, assets_underscores +"_"+ tube_dict_geo['asset_name'])

            # Get transforms, import gpucache, match transforms, add each in set and imported element in grp
            get_transforms_import_and_snap(node=each, node_path=gpucache_lod1_path, node_element_grp="converted_elements_GRP", rep="gpuCache")

        if representation == "geometry":
            # Get publish path
            geometry_pub_path = tube_dict_geo['publish_p']

            # Get transforms, import geometry, match transforms, add each in set and imported element in grp
            get_transforms_import_and_snap(node=each, node_path=geometry_pub_path, node_element_grp="converted_elements_GRP", rep="geometry")

        # Add assembly to converted_elements_SET
        cmds.sets(each, forceElement="converted_elements_SET", edit=True)

    print "All selected assemblies have been converted !"

def actualise_assemblies_tags():
    # Create scene list
    scene_list = mc.ls(type="transform")

    # For each in scene list
    for each in scene_list:
        # if assemblies
        if cmds.objExists(each+".definition") == True:
            # Get definition path
            definition_path = cmds.getAttr(each+'.definition')
            # Split
            split_definition_path = definition_path.split('/')
            # Get last part
            scene_name_cube= str(split_definition_path[-1:][0])
            # Split
            split_cube_name = scene_name_cube.split('_')
            #Get cube name
            cube_name = split_cube_name[1]

            # Change assembly cube name Tag
            cmds.setAttr(each+".cube_name", cube_name, type="string")

def switchLOD0FromBbox():
    '''
    If assemblies representations are in BBOX, the script auto switch assemblies to LOD0
    '''
    # List all scene transforms
    scene_list = mc.ls(type="transform")

    # For each in scene list
    for each in scene_list:
        # If each is an assembly
        if mc.objExists(each+".definition") == True:
            # Query active representation
            activeRepresentation = mc.assembly(each, query=True, active=True)
            # If active representation is BBOX
            if activeRepresentation == 'BBOX_gpuCache':
                # Set assembly representation to LOD0
                mc.assembly(each, edit=True, active="LOD0_gpuCache")

    print ">>   Switch LOD0 from Bbox Done."

def switchToRepresentationNone():
    '''
    Based on selection, if assemblies selected , we switch to representation none,
    else, we search the assembies and we switch to none
    '''
    # Var for new tagg
    attribute_name = "lock_representation"
    attribute_string = "True"
    # Get Selection
    selected_object = mc.ls(sl=True)

    # Check if selected object are assemblies
    for each in selected_object:
        # If assemblies
        if mc.objExists(each+".definition") == True:
            # Set assembly representation to LOD0
            mc.assembly(each, edit=True, active="")
            # Add tagg
            cmds.addAttr(each, longName=attribute_name, dataType="string")
            cmds.setAttr(each + "."+attribute_name, attribute_string, type="string")
            print "\n>>    "+each+" is now in representation None."
        # If not assemblies
        else:
            # Get namespace
            split_name = each.split(":")
            # List all assembly of the scene
            assemblies = mc.ls(type="assembly")
            # For each in assemblies
            for each in assemblies:
                # Query namespace of assembly
                namespaceAssembly = mc.assembly(each, query=True, repNamespace=True)
                # If namespace of actual assembly = to split_name
                if namespaceAssembly == split_name[0]:
                    # Set assembly representation to LOD0
                    mc.assembly(each, edit=True, active="")
                    # Add tagg
                    cmds.addAttr(each, longName=attribute_name, dataType="string")
                    cmds.setAttr(each + "."+attribute_name, attribute_string, type="string")
                    print "\n>>    "+each+" is now in representation None."