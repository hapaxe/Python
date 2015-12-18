__author__ = 'f.scaduto'

import maya.cmds as mc
import common
import tube_libraries
import sceneCheck.hotFix as hotFix

def create_globalScale(control):
    '''
    Create an attribute global_scale on a controler, create a multiplyDivide node,
    make connections, and lock and hide scales attributes from controler
    :param control:
        'master_ctrl' for characters
    '''
    # Create attribute on master control
    controler = control

    mc.addAttr(controler, ln="global_scale", min=0.001, dv=1, at='double')
    mc.setAttr(controler+'.global_scale', edit=True, channelBox=True)
    mc.setAttr(controler+'.global_scale', edit=True, keyable=True)

    # Create multiply divide node
    global_scale_mult = mc.createNode('multiplyDivide', n=controler+'_globalScale_mult')

    # Connect Global scale to mult
    mc.connectAttr(controler+'.global_scale', global_scale_mult+'.input1X')

    # Connect mult to controler
    mc.connectAttr(global_scale_mult+'.outputX', controler+'.scaleX')
    mc.connectAttr(global_scale_mult+'.outputX', controler+'.scaleY')
    mc.connectAttr(global_scale_mult+'.outputX', controler+'.scaleZ')

    # Lock and hide scales attr of controler
    mc.setAttr(controler+'.sx', lock=True, keyable=False, channelBox=False)
    mc.setAttr(controler+'.sy', lock=True, keyable=False, channelBox=False)
    mc.setAttr(controler+'.sz', lock=True, keyable=False, channelBox=False)

def save_publish(tube_dict):
    '''
    Save publish
    '''
    # Get the scene id
    mc.fileInfo( 'SceneId', tube_dict )

    # Create a new instance in tube manager
    d = common.MayaSceneManagerDialog()

    # Save wip first
    d.saveWip()

    # And Save publish
    d.publish()

def save_wip(tube_dict):
    '''
    Save publish
    '''
    # Get the scene id
    mc.fileInfo( 'SceneId', tube_dict )

    # Create a new instance in tube manager
    d = common.MayaSceneManagerDialog()

    # Save wip first
    d.saveWip()

def assets_last_wips(asset_name, project_id):
    '''DEPRECATED !!'''
    # Return
    return tube_libraries.get_asset_infos(asset_name, project_id)

def get_info_from_tube(in_asset, project_id, task_representation):
    '''
    Get info from tube, stored in dictionary

    :param in_assets:
        insert a list of cube name ex: ['abcd001']
    :param task:
        'modeling'
        'setupLOD0'
        'setupLOD2'
        'assemblyDef'
        'set'
    :return:
        tube_dict_task
    '''
    # Get all dicts of the asset
    tasks_dicts = assets_last_wips(in_asset, project_id)

    # Get the "task" of the asset
    tube_dict_task = tasks_dicts[task_representation]

    return tube_dict_task

def check_tag_anima():
    '''
    Clean tags attributs form Anima if exist
    '''
    # Delete tag info asset data
    if mc.objExists("*.assetInfoAsset") == True:
        mc.deleteAttr("*.assetInfoAsset")
    # Delete tag assetInfoAssetContainer
    if mc.objExists("*.assetInfoAssetContainer") == True:
        mc.deleteAttr("*.assetInfoAssetContainer")
    # Delete tag assetInfoAssetData
    if mc.objExists("*.assetInfoAssetData") == True:
        mc.deleteAttr("*.assetInfoAssetData")
    # Delete tag defaultCharProfileVersion
    if mc.objExists("*.defaultCharProfileVersion") == True:
        mc.setAttr("*.defaultCharProfileVersion", lock=False)
        mc.deleteAttr("*.defaultCharProfileVersion")
    # Delete tag character
    if mc.objExists("*.character") == True:
        mc.deleteAttr("*.character")

def check_selections_sets():
    '''
    Check if Geometry Set and Rig set exists, if not, create them.
    '''
    if not mc.objExists("GEOMETRY_SET"):
        if mc.objExists("GEO"):
            # Scan all transforms descendents of GEO group
            geometry = mc.listRelatives("GEO", allDescendents=True, type="transform", fullPath=True)

            content = mc.ls(geometry, dag=True, type="transform")

            # List empty who contain geometries
            geo_set_to_add = []
            # For each transforms in geometry
            for stuff in content:
                # If they ave shape in child, add them to a list
                if mc.listRelatives(stuff, children=True, shapes=True, fullPath=True):
                    geo_set_to_add.append(stuff)

            # Create selection set
            mc.sets(geo_set_to_add, n="GEOMETRY_SET")

    if not mc.objExists("RIG_SET"):
        if mc.objExists("RIG"):
            # List all nurbsCurves in the RIG group
            controls_shapes = mc.listRelatives("RIG", allDescendents=True, type="nurbsCurve", fullPath=True)

            # Get the parent shapes
            controls = mc.listRelatives(controls_shapes, parent=True, fullPath=True)

            # Create selection set
            mc.sets(controls, n="RIG_SET")

def check_if_tag_exist(node_to_tag):
    '''
    Check if tags exists, if not, create them.
    '''
    if not mc.objExists(node_to_tag+'.cube_type'):
        # cube type
        mc.addAttr(node_to_tag, longName="cube_type", dataType="string")

    if not mc.objExists(node_to_tag+'.cube_name'):
        # cube name
        mc.addAttr(node_to_tag, longName="cube_name", dataType="string")

    if not mc.objExists(node_to_tag+'.cube_task'):
        # cube_task
        mc.addAttr(node_to_tag, longName="cube_task", dataType="string")

    if not mc.objExists(node_to_tag+'.cube_version'):
        # cube version
        mc.addAttr(node_to_tag, longName="cube_version", dataType="string")

def delete_old_tag(parentNode):
    '''
    Delete tags if exists
    :return:
    '''
    if mc.objExists(parentNode):
        nodeToClean = mc.listRelatives(parentNode, children=True)
        
        for child in nodeToClean :
            if mc.objExists(child+'.cube_type'):
                mc.deleteAttr(child+'.cube_type')
            if mc.objExists(child+'.cube_name'):
                mc.deleteAttr(child+'.cube_name')
            if mc.objExists(child+'.cube_task'):
                mc.deleteAttr(child+'.cube_task')
            if mc.objExists(child+'.cube_version'):
                mc.deleteAttr(child+'.cube_version')

def lock_unlock_attr_tag(node_to_tag, state):
    '''
    lock or unlock tag attr.

    :param node_to_tag:
        for characters 'rigGrp'
    :param state:
        True
        False
    '''
    # cube type
    mc.setAttr(node_to_tag+'.cube_type', lock=state)
    # cube name
    mc.setAttr(node_to_tag+'.cube_name', lock=state)
    # cube_task
    mc.setAttr(node_to_tag+'.cube_task', lock=state)
    # cube version
    mc.setAttr(node_to_tag+'.cube_version', lock=state)

def set_tag_attr(tube_dict_task, node_to_tag):
    '''
    Get info for tags in tube, and set attributes
    '''
    # Get info for tags in tube
    type_name = tube_dict_task['type_name']
    asset_name = tube_dict_task['asset_name']
    task_name = tube_dict_task['task_name']

    # cube type
    mc.setAttr(node_to_tag + ".cube_type", type_name, type="string")
    # cube name
    mc.setAttr(node_to_tag + ".cube_name", asset_name, type="string")
    # cube_task
    mc.setAttr(node_to_tag + ".cube_task", task_name, type="string")

def set_tag_attr_local(node_to_tag):
    '''
    Get info in local, and set attributes
    :param node_to_tag:
    :return:
    '''
    # Get scene path
    scene_path = mc.file(query=True, sceneName=True)
    # Split path
    split_path = scene_path.split('/')
    # Get type name
    type_name = split_path[4][:2]
    # Get asset name
    split_asset_name = split_path[5].split('_')
    asset_name = split_asset_name[0]
    # Get task name
    task_name = split_path[6]

    # cube type
    mc.setAttr(node_to_tag + ".cube_type", type_name, type="string")
    # cube name
    mc.setAttr(node_to_tag + ".cube_name", asset_name, type="string")
    # cube_task
    mc.setAttr(node_to_tag + ".cube_task", task_name, type="string")

def clean_and_update_tag_attr(in_assets, task):
    '''
    Create log, for each assets, get info from tube, open scene, clean anima tags if exists, check if cube tag exist,
    if not, create it, loch unlock tags, force strings in tag attributes to match with files,
    check if selections sets exists, if not, create them.

    param in_assets:
        insert a list of cube name ex: ['abcd001']
    :param task:
        'modeling'
        'setupLOD0'
        'setupLOD2'
        'assemblyDef'
        'set'
    :return:
        log
    '''
    # Create a log
    log = []

    for each in in_assets:
        # Get info from tube
        tube_dict_task = get_info_from_tube(in_asset=each, project_id='413', task_representation=task)
        # Open Scene
        if tube_dict_task['publish_p']:
            try: # For the datas lost, if not try, the script stop..
                mc.file(tube_dict_task['publish_p'], o=True, f=True, prompt=False, ignoreVersion=True)
            except:
                pass
            # Set node to tag
            node = 'rigGrp'
            # Check if tag Anima exists, if yes, delete it
            check_tag_anima()
            # Check if tag exist, if not, create them
            check_if_tag_exist(node_to_tag=node)
            # Unlock tags
            lock_unlock_attr_tag(node_to_tag=node, state=False)
            # Update tag attributes
            set_tag_attr(tube_dict_task=tube_dict_task, node_to_tag=node)
            # Lock tags
            lock_unlock_attr_tag(node_to_tag=node, state=True)

            # Delete old unused tags
            delete_old_tag(parentNode='GEO')

            # Check if selections sets exists, if not, create them
            check_selections_sets()
            
            # Fix joint scale compensation
            #hotFix.fix_joint_scale_compensation()
            
            # Save publish
            save_publish(tube_dict=tube_dict_task['scene_id'])

            # Append result to log var
            log.append(str(each+' : '+task+' is Ok.'))
        else:
            log.append(str(each+' : '+task+' is not Ok.'))

    print log
    return log

def open_scene(in_asset, project_id, task, scene_state):
    '''
    Get the path of the scene on Tube, and open the scene

    :param in_asset:
        insert a cube name ex: 'abcd001'
    :param task:
        'modeling'
        'setupLOD0'
        'setupLOD2'
        'assemblyDef'
        'set'
    :param scene_state: 'wip' / 'publish'
    :return: tube_dict_task
    '''
    # Get info from tube
    tube_dict_task = get_info_from_tube(in_asset=in_asset, project_id=project_id, task_representation=task)

    if scene_state == 'wip':
        # Check if a wip exist
        if tube_dict_task['scene_path']:
            try: # For the datas lost, if not try, the script stop..
                mc.file(tube_dict_task['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
            except:
                pass
        else:
            print '>>   The scene %s of %s in %s does not exist' %(task, in_asset, 'wip')

    if scene_state == 'publish':
        # Check if a publish exist
        if tube_dict_task['publish_p']:
            try: # For the datas lost, if not try, the script stop..
                mc.file(tube_dict_task['publish_p'], o=True, f=True, prompt=False, ignoreVersion=True)
            except:
                pass
        else:
            print '>>   The scene %s of %s in %s does not exist' %(task, in_asset, 'publish')
            if tube_dict_task['scene_path']:
                try: # For the datas lost, if not try, the script stop..
                    mc.file(tube_dict_task['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
                except:
                    pass
            else:
                print '>>   The scene %s of %s in %s does not exist' %(task, in_asset, 'wip')
    return tube_dict_task

def batch_scenes(in_assets, project_id, tasks, scene_state, in_cmds, save_state):
    '''
    Batch scenes with custom defs, and save
    :param in_assets: Give a list of asset
    :param task: Give a list of tasks
    :param scene_state: 'wip' / 'publish'
    :param cmds: Give a list of defs to launch
    :param save_state: 'wip' / 'publish'
    :return:
    '''
    # Import in local for in_cmds lists
    import maya.cmds as cmds
    import maya.cmds as mc

    # For each assets
    for asset in in_assets:
        # In each tasks
        for task in tasks:
            # Open scene and store tube dict task for save step
            tube_dict_task = open_scene(in_asset=asset, project_id=project_id,
                                                       task=task, scene_state=scene_state)

            for cmd in in_cmds:
                # Execute command in string
                exec(cmd) in locals()

            if save_state == 'wip':
                #sceneCheck_def.save_wip(tube_dict=tube_dict_task['scene_id'])
                print("Go home! Save wip is not activated yet.")

            if save_state == 'publish':
                #sceneCheck_def.save_publish(tube_dict=tube_dict_task['scene_id'])
                print("Go home! Save publish is not activated yet.")

def debug():
    '''
    # TODO delete this proc
    Debug proc to test ui.
    :return:
    '''
    print">>    It's fine, you win."


