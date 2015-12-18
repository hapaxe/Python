__author__ = 'f.scaduto'

import maya.cmds as mc
import common
import sceneCheck.hotFix as hotFix
reload( hotFix )

def save_publish(tube_dict):
    '''
    save publish
    :param tube_dict:
    :return:
    '''
    # Get the scene id
    mc.fileInfo( 'SceneId', tube_dict )

    # Create a new instance in tube manager
    d = common.MayaSceneManagerDialog()

    # Save wip first
    d.saveWip()

    # And Save publish
    d.publish()


def open_scene(in_assets, task):
    '''
    Get the path of the scene on Tube, and open the scene

    :param in_assets:
        insert a list of cube names ex: ['abcd001']
    :param task:
        'modeling'
        'setupLOD0'
        'setupLOD2'
        'assemblyDef'
        'set'

    :return:
    '''
    for each in in_assets:
        # Get all dicts of the asset
        tasks_dicts = common.assets_last_wips(each)

        # Get the "task" of the asset
        tube_dict_task = tasks_dicts[task]

        try: # For the datas lost, if not try, the script stop..
            mc.file(tube_dict_task['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass

        # <><><><><><><><><><><><><><>
        # <><> Insert script here <><>
        # <><><><><><><><><><><><><><>
        hotFix.update_dynamic_system()

        # Test publish
        save_publish(tube_dict = tube_dict_task['scene_id'])

#-----------------------------------------------------------------------------
# Insert a list of cube name
#assets_cube = ['dahl001', 'gale001', 'luca001', 'pigy001', 'pigy006', 'popy001', 'stela001', 'wilo001']
assets_cube = ['dahl001', 'gale001', 'luca001', 'pigy001', 'pigy006', 'popy001', 'wilo001']

# Open scene
open_scene(in_assets=assets_cube, task='setupLOD2')

