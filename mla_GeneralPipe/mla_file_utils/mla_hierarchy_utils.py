import mla_GeneralPipe.mla_file_utils.mla_path_utils as pu
import mla_GeneralPipe.mla_file_utils.mla_file_library as fl
import mla_MultiPipe.mla_file_utils.mla_Multi_import_utils as import_utils
import logging

reload(pu)
reload(fl)
reload(import_utils)
MAYA_PROJECT_PATH = 'D:/BOULOT/TRAVAUX_PERSO/MAYA PROJECTS'
MAX_PROJECT_PATH = 'D:/BOULOT/TRAVAUX_PERSO/3DSMAX PROJECTS'
application = import_utils.get_application()

if application == 'Maya':
    PROJECT_PATH = MAYA_PROJECT_PATH
    types = ['.ma', '.mb', '.fbx', '.obj']
elif application == 'Max':
    PROJECT_PATH = MAX_PROJECT_PATH
    types = ['.max', '.fbx', '.obj']
else:
    PROJECT_PATH = None
    types = []


def list_hierarchy():
    """
    Create the list of the whole hierarchy.
    :return: the hierarchy (dict)
    """

    if not PROJECT_PATH:
        print 'No project path found'
        return

    # Creating empty dictionary for the hierarchy
    print 'Listing hierarchy'
    hierarchy = dict()

    # Create projects list
    projects = pu.create_subdir_list(PROJECT_PATH)

    file_types = list()

    # Loop in projects
    for project in projects:
        # For every project, create a dictionary
        project_dict = dict()

        # Creates the list of sub directory in the scenes folder
        scenes_sounds_list = ['scenes', 'sound', 'sourceimages']

        # Loop in every sub directory
        for scenes_sounds in scenes_sounds_list:
            scenes_sound_dir_dict = dict()

            # Create the list of types
            asset_anim_list = pu.create_subdir_list('%s/%s/%s/'
                                                    % (PROJECT_PATH,
                                                       project, scenes_sounds))

            if scenes_sounds == 'scenes':
                file_types = ['.ma', '.mb', '.fbx', '.obj']
            elif scenes_sounds == 'sounds':
                file_types = ['.mpeg', '.mp4', '.mp3', '.wma']
            elif scenes_sounds == 'sourceimages':
                file_types = ['.jpg', '.jpeg', '.jpe', '.psd', '.psb',
                              '.tif', '.tiff', '.png', '.pns', '.bmp', '.rle',
                              '.dib', '.raw', '.pxr', '.pbm', '.pgm', '.ppm',
                              '.pnm', '.pfm', '.pam', '.tga', '.vda', '.icb',
                              '.vst']

            for asset_anim in asset_anim_list:
                # For every sub directory, create a dictionary
                asset_types_dict = dict()

                # Create the list of types
                asset_types_list = pu.create_subdir_list('%s/%s/%s/%s/'
                                                         % (PROJECT_PATH,
                                                            project,
                                                            scenes_sounds,
                                                            asset_anim))

                # Loop for every type
                for asset_type in asset_types_list:
                    # For every type, create a dictionary
                    type_dict = dict()

                    # Create assets/shots list
                    assets = pu.create_subdir_list('%s/%s/%s/%s/%s/'
                                                   % (PROJECT_PATH,
                                                      project, scenes_sounds,
                                                      asset_anim, asset_type))

                    # Loop for every asset
                    for asset in assets:
                        # For every asset create a dictionary
                        asset_dict = dict()

                        # Create tasks list
                        tasks = pu.create_subdir_list('%s/%s/%s/%s/%s/%s/'
                                                      % (PROJECT_PATH,
                                                         project, scenes_sounds,
                                                         asset_anim, asset_type,
                                                         asset))

                        # Loop for every task
                        for task in tasks:
                            # Create list of the files in every task directory
                            task_files = fl.FileLibrary(project, scenes_sounds,
                                                        asset_anim, asset_type,
                                                        asset, task, file_types)

        # Store all the collected datas into dictionaries
                            asset_dict[task] = task_files

                        type_dict[asset] = asset_dict

                    asset_types_dict[asset_type] = type_dict

                scenes_sound_dir_dict[asset_anim] = asset_types_dict

            project_dict[scenes_sounds] = scenes_sound_dir_dict

        hierarchy[project] = project_dict

    return hierarchy