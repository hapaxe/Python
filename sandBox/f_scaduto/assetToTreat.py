__author__ = 'f.scaduto'


import maya.cmds as cmds
from tube_libraries import Tube
import libs.common as common

# =====================================
def assets_from_tube():
    '''
    Get all assets names from tube
    :return:
    '''
    # Connect to tube
    with Tube() as tube:
        # Request
        assets = tube.cursor.select('SELECT asset_name FROM Asset WHERE asset_id_proj = 413', None)
    # Return a dict with all asset_name
    return assets


def assets_list():
    '''
    Add assets to a list
    :return:
    '''
    # Create a list of all assets
    assets_tube = []

    for each in assets_discts_tube:
        assets_tube.append(str(each['asset_name']))

    return assets_tube


def list_assets_sets():
    '''
    Add only assets with task set and different from the start version in a list
    :return:
    '''
    # Create a list of assets with task set and different from the start version
    assets_cube_to_treat = []

    for each in all_assets:
        # Get cube tasks for the asset
        tasks_dicts = common.assets_last_wips(each)

        if not 'set' in tasks_dicts:
            pass
        else:
            if tasks_dicts['set']['scene_version'] != 'v001':
                assets_cube_to_treat.append(each)
            else:
                pass

    return assets_cube_to_treat


def write_asset_to_treat_txt(assets):
    '''
    Write assets list into a text file
    :param assets:
    :return:
    '''
    f = open( "P:\\Stella_Serie\\scripts\\S02\\data\\assets_to_treat.txt", "w" )
    f.write( str(assets) )
    f.close()

def assets_list_from_txt():
    '''
    Open assest from a text file
    :return:
    '''
    file_open = open( "P:\\Stella_Serie\\scripts\\S02\\data\\assets_to_treat.txt", "r" )
    file_log = file.readlines( file_open )[0]
    file.close( file_open )
    # Add list to a variable
    props_list = eval(file_log)
    return props_list


# ============================================
# Run one time to actualise the list to treat

# Get all assets from tube
assets_discts_tube = assets_from_tube()
all_assets = assets_list()
# Get only assets with task set
assets_to_treat = list_assets_sets()

print "we have %s assets to treat !" %len(assets_to_treat)

# Write in text file
write_asset_to_treat_txt(assets = assets_to_treat)
print "\nAssets list writed in P:\\Stella_Serie\\scripts\\S02\\data\\assets_to_treat.txt ."