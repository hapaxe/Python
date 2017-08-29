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

# Set project path and file types depending on application
if application == 'Maya':
    PROJECT_PATH = MAYA_PROJECT_PATH
    types = ['.ma', '.mb', '.fbx', '.obj']
elif application == 'Max':
    PROJECT_PATH = MAX_PROJECT_PATH
    types = ['.max', '.fbx', '.obj']
else:
    PROJECT_PATH = None
    types = []

# Define the path of the hierarchy_template file
location = '\\'.join(__file__.split('\\')[0:-1])
hierarchy_template_path = os.path.join(location, 'hierarchy_templates.json')


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
def set_hierarchy_template(hierarchy_template_name='',
                           depth=6,
                           increment_depth_save=6,
                           increment_digits=3,
                           increment_template_file_name=
                           '[depth4]_[depth5]_[depth6]_[increment].ext',
                           publish_depth_save=6,
                           publish_template_file_name=
                           '[depth4]_[depth5]_[depth6]_PUBLISH.ext',
                           edit=False):
    """
    Create hierarchy template and store it into json file.
    :param hierarchy_template_name: name to give to the current hierarchy
    template
    :type hierarchy_template_name: str

    :param depth: number of levels in the hierarchy
    :type depth: int

    :param increment_depth_save: depth level to which save the incremented files
    :type increment_depth_save: int

    :param increment_digits: number of digits in the increment number
    :type increment_digits: int

    :param increment_template_file_name: define template name for incremented
    files. Accepted string parts are [*depth_level*], [increment] and words.
    Each part must be separated by an underscore.
    Example :'[depth4]_[depth5]_[depth6]_[increment].ext',
    '[depth4]_[depth5]_[depth6]_PUBLISH.ext'
    :type increment_template_file_name: str

    :param publish_depth_save: depth level to which save the published files
    :type publish_depth_save: int

    :param publish_template_file_name: define template name for published files
    :type publish_template_file_name: str
    
    :param edit: define if the file must be edited (True) or created (False)
    :type edit: bool
    """
    # Check if a hierarchy template name is specified, if not, return
    if not hierarchy_template_name:
        logging.error('No hierarchy template name specified')
        return
        
    # Get hierarchy templates
    hierarchy_templates = get_template_file()

    # Get specified hierarchy template if in edit mode and if it exists
    if edit:
        if hierarchy_templates[hierarchy_template_name]:
            hierarchy = hierarchy_templates[hierarchy_template_name]
        else:
            logging.warning('Specified hierarchy template does not exist and'
                            'therefore cannot be edited. It will be created'
                            'instead')
            hierarchy = dict()
    else:
        # Creating template hierarchy dict
        hierarchy = dict()
    
    # Set or modify hierarchy information (depending on the mode)
    if hierarchy_template_name:
        hierarchy['hierarchy_template_name'] = hierarchy_template_name
    if depth:
        hierarchy['depth'] = depth
    if increment_depth_save:
        hierarchy['increment_depth_save'] = increment_depth_save
    if increment_digits:
        hierarchy['increment_digits'] = increment_digits
    if increment_template_file_name:
        hierarchy['increment_template_file_name'] = increment_template_file_name
    if publish_depth_save:
        hierarchy['publish_depth_save'] = publish_depth_save
    if publish_template_file_name:
        hierarchy['publish_template_file_name'] = publish_template_file_name
    
    if depth or not edit:
        for i in range(depth + 1):
            hierarchy['depth%s' % i] = list()

    # Add template hierarchy to template hierarchy file
    hierarchy_templates[hierarchy_template_name] = hierarchy
    logging.debug(hierarchy_templates)

    # Save
    fu.FileSystem.save_to_json(hierarchy_templates, hierarchy_template_path)


def get_template_file():
    """
    Get template file from provided path.

    :return: template hierarchy dict
    :rtype: OrderedDict
    """
    # Get template hierarchies if the file already exists
    if os.path.isfile(hierarchy_template_path):
        logging.info('template hierarchy file exists')
        hierarchy_templates = fu.FileSystem.load_from_json(hierarchy_template_path)
    # Create an empty OrderedDict if the file doesn't exist
    else:
        logging.info('template hierarchy file does not exist')
        hierarchy_templates = OrderedDict()

    return hierarchy_templates


def customize_hierarchy_template(depth=None, depth_template_type=None,
                                 folder_name=None, master_folder=None,
                                 hierarchy_template=None):
    """
    Customize
    :param depth: depth level to add the
    :type depth: int

    :param depth_template_type: type to give to the depth level, accepted types
    are : fixed, dynamic, fixed by folder, dynamic by folder
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

    # Get hierarchy template to update
    current_template = hierarchy_templates[hierarchy_template]

    # Set up current hierarchy depth level depending on specified depth type
    # If type is fixed, add the folder name
    if depth_template_type == 'fixed':
        current_template['depth%s' % depth].append(folder_name)

    # If type is dynamic, set the depth as list of one str
    elif depth_template_type == 'dynamic':
        current_template['depth%s' % depth] = ['**dynamic']

    # If type is fixed by folder
    elif depth_template_type == 'fixed by folder':
        # If there is already a dict stored for this depth level, add the folder
        # name to the list
        if type(current_template['depth%s' % depth]) == dict:
            depth_template = current_template['depth%s' % depth]
            if len(depth_template[master_folder]) > 0:
                depth_template[master_folder].append(folder_name)
        # If there is no dict stored for this depth level, create a dict with a
        # list containing the folder name at the right index
        else:
            depth_template = dict()
            depth_template[master_folder] = [folder_name]
        # Replace old level value by the newly edited dict
        current_template['depth%s' % depth] = depth_template

    # If the type is dynamic by folder, set the depth for the master folder as a
    # list of one str
    elif depth_template_type == 'dynamic by folder':
        if type(current_template['depth%s' % depth]) == dict:
            depth_template = current_template['depth%s' % depth]
            depth_template[master_folder] = ['**dynamic']
        else:
            depth_template = dict()
            depth_template[master_folder] = ['**dynamic']
        # Replace old level value by the newly edited dict
        current_template['depth%s' % depth] = depth_template

    # Else, pass
    else:
        pass

    # Save
    fu.FileSystem.save_to_json(hierarchy_templates, hierarchy_template_path)
