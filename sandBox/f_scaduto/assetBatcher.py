import maya.cmds as cmds
import libs.common as common
#import sys
#sys.path.append(r"\\netapp\shared_workflow\Workflow\C_pipe\API\scene_manager")
from MayaSceneManagerGeneric import MayaSceneManagerDialog


def save_publish(tube_dict):
    
    # Get the scene id
    cmds.fileInfo( 'SceneId', tube_dict )
    
    # Create a new instance in tube manager
    d = MayaSceneManagerDialog()
    
    # Save wip first
    d.saveWip()
    
    # And Save publish
    d.publish()


def assets_list_from_txt():
    file_open = open( "P:\\Stella_Serie\\scripts\\S02\\data\\assets_to_treat.txt", "r" )
    file_log = file.readlines( file_open )[0]
    file.close( file_open )
    # Add list to a variable
    props_list = eval(file_log)
    return props_list


def open_setuplod0(in_assets):
    
    asset_setuplod0_without_rig_set = []
    
    for each in in_assets:
        # Get all dicts of the asset
        tasks_dicts = common.assets_last_wips(each)
        
        # Get task setupLOD0 of the asset
        tube_dict_setuplod0 = tasks_dicts['setupLOD0']
        
        try: # For the datas lost, if not try, the script stop.. 
            cmds.file(tube_dict_setuplod0['scene_path'], o=True, f=True, prompt=False, ignoreVersion=True)
        except:
            pass
            
        # Test publish
        #save_publish(tube_dict = tube_dict_setuplod0['scene_id'])
        
        if not cmds.objExists('RIG_SET'):
            asset_setuplod0_without_rig_set.append(each)
        
            f = open( "D:\\stella_S02\\asset_setuplod0_without_rig_set.txt", "w" )
            f.write( str(asset_setuplod0_without_rig_set) )
            f.close()


assets_to_check = assets_list_from_txt()
#assets_to_check = ['truG001', 'dahl001', 'gale001', 'palm003', 'floC001']

# Open scene
open_setuplod0(in_assets=assets_to_check)