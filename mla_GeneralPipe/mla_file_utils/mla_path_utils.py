import os
import mla_file_library as fl
reload(fl)
MAYA_PROJECT_PATH = 'D:/BOULOT/TRAVAUX_PERSO/MAYA PROJECTS'


def build_path(project, scenes_sound='', asset_anim='', asset_type='', asset='',
               task='', filename='', return_type='project'):
    """
    Build path from given data.
    
    :param project: project to create path with
    :type project: str

    :param scenes_sound: type of scene or file to look for
    :type scenes_sound: str

    :param asset_anim: type of asset or animation to look for
    :type asset_anim: str
    
    :param asset_type: type to look for
    :type asset_type: str
    
    :param asset: asset to look for
    :type asset: str
    
    :param task: task to look for
    :type task: str
    
    :param filename: file to look for
    :type filename: str
    
    :param return_type: defines what type of path we want to output
    :type return_type: str
    
    :return: path to selected task/file
    :rtype: str
    """
    # Build project path
    if return_type == 'project':
        return_path = '%s/%s' % (MAYA_PROJECT_PATH, project)

    elif return_type == 'directory':
        return_path = '%s/%s/%s/%s/%s/%s/%s' % (MAYA_PROJECT_PATH,
                                                project, scenes_sound,
                                                asset_anim, asset_type, asset,
                                                task)

    # Build file path
    elif return_type == 'file':
        return_path = '%s/%s/%s/%s/%s/%s/%s/%s' % (MAYA_PROJECT_PATH,
                                                   project, scenes_sound,
                                                   asset_anim, asset_type,
                                                   asset, task, filename)

    # Build wip path
    elif return_type == 'wip':
        if filename == 'No file in this directory' or filename == '':
            wip_file = '%s_%s_%s_00.ma' % (asset_type, asset, task)
        else:
            # Split file name
            wip_file = filename.split('.')[0]
            print wip_file
            wip_file = wip_file.split('_')
            print wip_file
            # Increment version number
            wip_file[3] = build_increment(wip_file[3])
            print wip_file[3]
            # Join publish file name
            wip_file = '_'.join(wip_file)
            print wip_file
        # Build path
        return_path = '%s/%s/%s/%s/%s/%s/%s/%s' % (MAYA_PROJECT_PATH,
                                                   project, scenes_sound,
                                                   asset_anim, asset_type,
                                                   asset, task, wip_file)

    # Build publish path
    else:
        # Split file name
        publish_file = filename.split('_')
        # Remove increment and extension
        publish_file = publish_file[:3]
        print publish_file
        # Append PUBLISH plus extension
        publish_file.append('PUBLISH.ma')
        print publish_file
        # Join publish file name
        publish_file = '_'.join(publish_file)
        print publish_file
        # Build path
        return_path = '%s/%s/%s/%s/%s/%s/%s' % (MAYA_PROJECT_PATH,
                                                project, scenes_sound,
                                                asset_anim, asset_type, asset,
                                                publish_file)

    # print return_path
    return return_path


def build_increment(number):
    """
    Increment the given number and return it as a 2 decimal string (ie : 01, 02, etc.)
    :param number: number you want to increment
    :return: incremented number (string)
    """
    # Set it as an integer
    increment = int(number)
    # Increment
    increment += 1
    # List it
    increment = list(str(increment))

    # Add number to get 2 numbers
    if len(increment) < 2:
        increment.insert(0, '0')

    # Join it as a string
    increment = ''.join(increment)

    return increment


def list_hierarchy():
    """
    Create the list of the whole hierarchy.
    :return: the hierarchy (dict)
    """
    # Creating empty dictionary for the hierarchy
    print 'Listing hierarchy'
    hierarchy = dict()

    # Create projects list
    projects = create_subdir_list(MAYA_PROJECT_PATH)

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
            asset_anim_list = create_subdir_list('%s/%s/%s/'
                                                 % (MAYA_PROJECT_PATH,
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
                asset_types_list = create_subdir_list('%s/%s/%s/%s/'
                                                      % (MAYA_PROJECT_PATH,
                                                         project, scenes_sounds,
                                                         asset_anim))

                # Loop for every type
                for asset_type in asset_types_list:
                    # For every type, create a dictionary
                    type_dict = dict()

                    # Create assets/shots list
                    assets = create_subdir_list('%s/%s/%s/%s/%s/'
                                                % (MAYA_PROJECT_PATH,
                                                   project, scenes_sounds,
                                                   asset_anim, asset_type))

                    # Loop for every asset
                    for asset in assets:
                        # For every asset create a dictionary
                        asset_dict = dict()

                        # Create tasks list
                        tasks = create_subdir_list('%s/%s/%s/%s/%s/%s/'
                                                   % (MAYA_PROJECT_PATH,
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


def create_subdir_list(given_path):
    """
    create list of the subdirectories in the given directory
    
    :param given_path: directory to list subdirectories in
    :type given_path: str
    
    :return: list of the subdirectories
    :rtype: list
    """
    # print 'Listing sub directories in %s' % given_path
    # List all the directories at the given path
    subdir_list = [sub_path for sub_path in os.listdir(given_path)
                   if os.path.isdir(given_path+'/'+sub_path)]

    # Removing mayaSwatches, keyboard and edits
    subdir_list = [directory for directory in subdir_list
                   if directory != '.mayaSwatches'
                   and directory != 'Keyboard'
                   and directory != 'edits']

    # Returning list
    return subdir_list


def build_files_list(given_path):
    """
    Create a list of all the files in the given directory
    
    :param given_path: path to the directory you want to list the files in
    :type given_path: str
    
    :return: all the files in that directory
    :rtype: list
    """
    # Set current directory to the given path
    os.chdir(given_path)
    # Filter files
    files = [dir_file for dir_file in os.listdir(given_path)
             if os.path.isfile(os.path.join(given_path, dir_file))]
    # Filter maya files
    maya_files = [maya_file for maya_file in files
                  if '.ma' in maya_file
                  or '.mb' in maya_file
                  or '.fbx' in maya_file]
    # If no maya files
    if not maya_files:
        # list is used as verbose
        maya_files = ['No file in this directory']
    # If there are maya files
    else:
        # Sort them
        maya_files.sort(key=lambda x: os.path.getmtime(x))
        # Get most recent in first
        maya_files.reverse()

    return maya_files


