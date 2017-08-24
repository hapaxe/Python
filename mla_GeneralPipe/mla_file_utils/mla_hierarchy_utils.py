import mla_GeneralPipe.mla_file_utils.mla_path_utils as pu
import mla_GeneralPipe.mla_file_utils.mla_file_library as fl
import mla_GeneralPipe.mla_file_utils.mla_file_utils as fu
import mla_MultiPipe.mla_file_utils.mla_Multi_import_utils as import_utils
import logging
import os
from collections import OrderedDict

reload(pu)
reload(fl)
reload(fu)
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


# TODO
def create_hierarchy_template(depth=6,
                              increment_depth_save=6,
                              increment_digits=3,
                              increment_template_file_name='[depth4]_[depth5]_[depth6]_[increment].ext',
                              publish_depth_save=6,
                              publish_template_file_name='[depth4]_[depth5]_[depth6]_PUBLISH.ext'):
    """
    Create hierarchy template and store it into json file.
    :param depth: number of levels in the hierarchy
    :type depth: int

    :param increment_depth_save: depth level to which save the incremented files
    :type increment_depth_save: int

    :param increment_digits: number of digits in the increment number
    :type increment_digits: int

    :param increment_template_file_name: define template name for incremented
    files
    :type increment_template_file_name: str

    :param publish_depth_save: depth level to which save the published files
    :type publish_depth_save: int

    :param publish_template_file_name: define template name for published files
    :type publish_template_file_name: str
    """
    location = '\\'.join(__file__.split('\\')[0:-1])
    template_hierarchy_path = os.path.join(location, 'template_hierarchy.json')

    hierarchy_templates, number = get_template_file()

    # Creating template hierarchy dict
    hierarchy = dict()
    hierarchy['depth'] = depth
    hierarchy['increment_depth_save'] = increment_depth_save
    hierarchy['increment_digits'] = increment_digits
    hierarchy['increment_template_file_name'] = increment_template_file_name
    hierarchy['publish_depth_save'] = publish_depth_save
    hierarchy['publish_template_file_name'] = publish_template_file_name
    for i in range(depth + 1):
        hierarchy['depth%s' % i] = list()

    # Add template hierarchy to template hierarchy file
    hierarchy_templates['template_hierarchy_%s' % number] = hierarchy
    print hierarchy_templates
    fu.FileSystem.save_to_json(hierarchy_templates, template_hierarchy_path)


def get_template_file():
    """
    Get template file from provided path.

    :return: template hierarchy dict
    :rtype: OrderedDict
    """
    location = '\\'.join(__file__.split('\\')[0:-1])

    template_hierarchy_path = os.path.join(location, 'template_hierarchy.json')

    # Get template hierarchies if the file already exists
    if os.path.isfile(template_hierarchy_path):
        logging.info('template hierarchy file exists')
        hierarchy_templates = fu.FileSystem.load_from_json(template_hierarchy_path)
        hierarchy_number = 0
        for hierarchy in hierarchy_templates:
            hierarchy_number += 1
    else:
        hierarchy_templates = OrderedDict()
        hierarchy_number = 1
        logging.info('template hierarchy file does not exist')

    return hierarchy_templates, hierarchy_number


def customize_hierarchy_template(depth=None, depth_template_type=None,
                                 folder_name=None, master_folder=None,
                                 hierarchy_template=None):
    """
    Customize
    :param depth: depth level to add the
    :type depth: int

    :param depth_template_type: type to give to the depth level, accepted types
    are : fixed, variable, fixed by folder, variable by folder
    :type depth_template_type: str

    :param folder_name: name to give to the folder if 'fixed'
    or 'fixed by folder'
    :type folder_name: str

    :param master_folder: folder from which the new level set up will be
    dependent (must be one level higher in hierarchy)
    :type master_folder: str

    :param hierarchy_template: hierarchy template to edit
    :type hierarchy_template: str

    :return:
    """
    # Get hierarchy templates from file
    hierarchy_templates = get_template_file()

    template = hierarchy_templates[hierarchy_template]

    if type == 'fixed':
        depth_template = list()

    elif type == 'variable':
        depth_template = list()

    elif type == 'fixed by folder':
        depth_template = dict()

    elif type == 'variable by folder':
        depth_template = dict()

    else:
        pass
