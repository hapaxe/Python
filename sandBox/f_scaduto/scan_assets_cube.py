__author__ = 'f.scaduto'


# Recap assets
#=============================
import maya.cmds as cmds
import common
from tube_libraries import Tube


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

#=============================

list_no_maps = []
list_no_looks = []
list_no_shading = []
#=============================
def va_chercher_json(in_asset):
    '''
    '''
    # Lit le .json
    assets_dicts = load_from_json(ROOT_PATH + '/scans/scan_413.json')
    for each in in_asset:
        asset_dict = assets_dicts[each]

        if asset_dict['Maps'] == "Pas de Dossier":
            list_no_maps.append(str("Anima_name : "+each+ "    , cube_name : "+asset_dict['Cube Name']))

        if asset_dict['Look'] == "Pas de Dossier":
            list_no_looks.append(str("Anima_name : "+each+ "    , cube_name : "+asset_dict['Cube Name']))



def le_shading_est_il_fait(in_asset):
    for each in in_asset:
        print each
        try:
            # Va chercher dans tube les tasks de l'asset
            tasks_dicts = common.assets_last_wips(each)
            # Recupere le Dict de l'asset Tube set
            if not tasks_dicts['shading']:
                pass
            else:
                tube_dict_shad = tasks_dicts['shading']

                if not tube_dict_shad['type_name'] == 'PR':
                    pass
                else:
                    if tube_dict_shad['scene_version'] == 'v001':
                        list_no_shading.append(str('cube_name : '+each))
        except:
            pass


#=============================
# recupere la liste de tout les assets tubes
assets_tube = assets_from_tube()

assets_list = []

for each in assets_tube:
    assets_list.append(each['asset_name'])
# va_chercher_json(in_asset = assets_list)
#le_shading_est_il_fait(in_asset = assets_list)

print "nombre d'assets sans shading max : %s" % len(list_no_shading)