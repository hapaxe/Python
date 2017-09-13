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
                           hierarchy_path='',
                           depth=6,
                           increment_depth_save=6,
                           increment_digits=3,
                           increment_template_file_name=
                           '{depth4}_{depth5}_{depth6}_v{increment}.ext',
                           publish_depth_save=6,
                           publish_template_file_name=
                           '{depth4}_{depth5}_{depth6}_PUBLISH.ext',
                           edit=False):
    """
    Create hierarchy template and store it into json file.
    :param hierarchy_template_name: name to give to the current hierarchy
    template
    :type hierarchy_template_name: str

    :param hierarchy_path: path to the top folder of the hierarchy
    :type hierarchy_path: str

    :param depth: number of levels in the hierarchy
    :type depth: int

    :param increment_depth_save: depth level to which save the incremented files
    :type increment_depth_save: int

    :param increment_digits: number of digits in the increment number
    :type increment_digits: int

    :param increment_template_file_name: define template name for incremented
    files. Accepted string parts are {*depth_level*}, {increment} and words.
    Each part must be separated by an underscore. You can specify a range of
    character inside of a depth level.
    Example :'{depth4}_{depth5}_{depth6}_{increment}.ext',
    '{depth4[0:2]}_{depth5}_{depth6}_PUBLISH.ext'
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
    if hierarchy_path:
        hierarchy['hierarchy_path'] = hierarchy_path
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
    if not edit:
        hierarchy['hierarchy_file_types'] = list()

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


def customize_hierarchy_template(depth=None, template_type=None,
                                 folder_name=None, master_folder=None,
                                 hierarchy_template=None, file_type=None):
    """
    Customize
    :param depth: depth level to add the
    :type depth: int

    :param template_type: type to give to the depth level, accepted types
    are : fixed, dynamic, fixed by folder, dynamic by folder
    :type template_type: str

    :param folder_name: name to give to the folder if 'fixed'
    or 'fixed by folder'
    :type folder_name: str

    :param master_folder: folder from which the new level set up will be
    dependent (must be one level higher in hierarchy)
    :type master_folder: str

    :param hierarchy_template: hierarchy template to edit
    :type hierarchy_template: str
    
    :param file_type: type of file to add to the 'hierarchy_file_types' entry
    :type file_type: str
    """
    # Get hierarchy templates from file
    hierarchy_templates = get_template_file()

    # Get hierarchy template to update
    current_template = hierarchy_templates[hierarchy_template]

    if not file_type:
        # Set up current hierarchy depth level depending on specified depth type
        # If type is fixed, add the folder name
        if template_type == 'fixed':
            current_template['depth%s' % depth].append(folder_name)

        # If type is dynamic, set the depth as list of one str
        elif template_type == 'dynamic':
            current_template['depth%s' % depth] = ['**dynamic']

        # If type is fixed by folder
        elif template_type == 'fixed by folder':
            # If there is already a dict stored for this depth level, add the
            # folder name to the list
            if type(current_template['depth%s' % depth]) == dict:
                depth_template = current_template['depth%s' % depth]
                if len(depth_template[master_folder]) > 0:
                    depth_template[master_folder].append(folder_name)
            # If there is no dict stored for this depth level, create a dict
            # with a list containing the folder name at the right index
            else:
                depth_template = dict()
                depth_template[master_folder] = [folder_name]
            # Replace old level value by the newly edited dict
            current_template['depth%s' % depth] = depth_template

        # If the type is dynamic by folder, set the depth for the master folder
        # as a list of one str
        elif template_type == 'dynamic by folder':
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
    else:
        # Set up current hierarchy file types depending on specified file types
        # If type is fixed, add the folder name
        if template_type == 'fixed':
            current_template['hierarchy_file_types'].append(folder_name)

        # If type is dynamic, set the depth as list of one str
        elif template_type == 'dynamic':
            logging.warning('hierarchy_file_types cannot be dynamic')

        # If type is fixed by folder
        elif template_type == 'fixed by folder':
            # If there is already a dict stored for this depth level, add the
            # file type to the list
            if type(current_template['hierarchy_file_types']) == dict:
                types_template = current_template['hierarchy_file_types']
                if len(types_template[master_folder]) > 0:
                    types_template[master_folder].append(file_type)
            # If there is no dict stored for this depth level, create a dict
            # with a list containing the folder name at the right index
            else:
                types_template = dict()
                types_template[master_folder] = [folder_name]
            # Replace old level value by the newly edited dict
            current_template['hierarchy_file_types'] = types_template

        # If the type is dynamic by folder, set the depth for the master folder
        # as a list of one str
        elif template_type == 'dynamic by folder':
            logging.warning('hierarchy_file_types cannot be dynamic')

        # Else, pass
        else:
            pass

    # Save
    fu.FileSystem.save_to_json(hierarchy_templates, hierarchy_template_path)


def build_hierarchy_path(hierarchy_template_name='', folder_list=[],
                         add_filename=False):
    """
    Build a path from given hierarchy and folder list.
    :param hierarchy_template_name: name of the hierarchy template to browse in
    :type hierarchy_template_name: str

    :param folder_list: list of folders to build the current path
    :type folder_list: list

    :param add_filename: name of the file to add at the end of the path
    :type add_filename: str

    :return:
    """
    # Get hierarchy templates from file
    hierarchy_templates = get_template_file()
    hierarchy_template = hierarchy_templates[hierarchy_template_name]
    hierarchy_path = hierarchy_template['hierarchy_path']

    # Build path from root path and specified folders
    return_path = hierarchy_path
    for folder in folder_list:
        return_path = os.path.join(return_path, folder)
    if add_filename:
        return_path = build_file_name(hierarchy_template_name=
                                      hierarchy_template_name,
                                      folder_path=return_path,
                                      return_path=True)

    return return_path


# TODO
def list_hierarchy_from_template(hierarchy_template_name=''):
    """
    List all the content of the selected hierarchy.
    :param hierarchy_template_name: name of the hierarchy template to browse in
    :type hierarchy_template_name: str

    :return: folders and files contained in the selected hierarchy
    :rtype: dict
    """
    hierarchy_templates = get_template_file()
    hierarchy_template = hierarchy_templates[hierarchy_template_name]
    folder_path = hierarchy_template['hierarchy_path']
    depth = 1

    hierarchy_content = list_hierarchy_content(folder_path, hierarchy_template,
                                               depth)

    return hierarchy_content


# TODO
def list_hierarchy_content(folder_path='', hierarchy_template=dict,
                           current_depth=int):
    """
    Recursively list the content of a folder.
    :param folder_path: path to the folder whom you want to list the content
    :type folder_path: str

    :param hierarchy_template: hierarchy template of the hierarchy to explore
    :type hierarchy_template: dict

    :param current_depth: depth level to list
    :type current_depth: int


    :return: content of the folder
    :type
    """

    file_types = hierarchy_template['file_types']

    if current_depth == hierarchy_template['depth']:
        if type(file_types) == list:
            hierarchy_content = fl.FileLibrary(folder_path, file_types=file_types)
        elif type(file_types) == dict:
            hierarchy_content = None
            for folder in file_types.keys():
                if folder in folder_path:
                    hierarchy_content = fl.FileLibrary(folder_path,
                                                       file_types=file_types[folder])
        else:
            hierarchy_content = None
    else:
        hierarchy_content = dict()
        depth_content = pu.create_subdir_list(folder_path)
        for folder in depth_content:
            current_depth += 1
            next_path = os.path.join(folder_path, folder)
            folder_content = list_hierarchy_content(next_path,
                                                    hierarchy_template,
                                                    current_depth)
            hierarchy_content[folder] = folder_content

    return hierarchy_content


def build_file_name(hierarchy_template_name='', folder_path='', filetype='',
                    return_path=False):
    """
    Build file name from specified hierarchy template and folder path.
    :param hierarchy_template_name: name of the hierarchy template to browse in
    :type hierarchy_template_name: str

    :param folder_path: path to the folder where the file is going to be saved
    :type folder_path: str

    :param filetype: type of the file whom you want to create the name.
    type accepted are: increment, publish, image_increment, image_publish
    :type filetype: str

    :param return_path: specify if we want to include the path in the return
    value
    :type return_path: bool

    :return:
    """
    hierarchy_templates = get_template_file()
    hierarchy_template = hierarchy_templates[hierarchy_template_name]

    # Define extension types depending on the application running
    if application == 'Maya':
        scene_ext = '.ma'
    elif application == 'Max':
        scene_ext = '.max'
    else:
        scene_ext = None
    image_ext = 'jpg'

    # Define file_template_name and file extension
    if filetype == 'increment':
        file_ext = scene_ext
        file_template_name = hierarchy_template['increment_template_file_name']
    elif filetype == 'publish':
        file_ext = scene_ext
        file_template_name = hierarchy_template['publish_template_file_name']
    elif filetype == 'image_increment':
        file_ext = image_ext
        file_template_name = hierarchy_template['increment_template_file_name']
    elif filetype == 'image_publish':
        file_ext = image_ext
        file_template_name = hierarchy_template['publish_template_file_name']

    # Get the different parts of the name

    filename = ''
    # (\{[A-Za-z0-9]*\})

    if return_path:
        filename = os.path.join(folder_path, filename)

    return filename
