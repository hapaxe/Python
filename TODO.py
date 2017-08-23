 # Create .json file storing the MAYA_PROJECT_PATH and MAX_PROJECT_PATH as well as the depth and folder hierarchy for both MAYA and MAX :
# Save number of digits for increments and file name template in the file too 

PROJECT_PATH_1 = 'D:\Project\NeoPlum\Art\Characters'
PROJECT_PATH_2 = 'D:\Project\NeoPlum\Art\Levels\Hotel\Art'

increment_digits = 4

# Either standard template file name, or folder dependent
MAYA_standard_template_file_name = '[depth4]_[depth5]_[depth6]_v[increment_digits].ext'
MAYA_folder_dependent_template_file_name = {'ASSETS': '[depth4]_[depth5]_[depth6]_v[increment_digits].ext',
                                            'ANIMATION': '[depth5]_[depth6]_v[increment_digits].ext'}
MAYA_publish_depth_save = 4
MAYA_standard_publish_template_file_name = '[depth4]_[depth5]_[depth6]_PUBLISH.ext'
MAYA_folder_dependent_publish_template_file_name = {'ASSETS': '[depth4]_[depth5].ext',
                                                    'ANIMATION': '[depth5]_[depth6].ext'}

hierarchy_template_1_depth = 6
hierarchy_template_1 = {'depth0': [PROJECT_PATH_1, PROJECT_PATH_2],
                        'depth1': [**PROJECTS],
                        'depth2': ['scenes', 'sounds', 'sourceimage'],
                        'depth3': ['ASSETS', 'ANIMATION'],
                        'depth4': {'ASSETS': ['CH', 'PR', 'VEH'],
                                   'ANIMATION': {**episodes}},
                        'depth5': {'ASSETS': {**assets},
                                   'ANIMATION': {**shots}},
                        'depth6': {'ASSETS': ['MODEL', 'RIG', 'TEXTURE'],
                                   'ANIMATION': ['LAYOUT', 'ANIM']}}

hierarchy_template_2_depth = 2
hierarchy_template_2 = {'depth0': PROJECT_PATH_2,
                        'depth1': [**ASSETS],
                        'depth2': ['Animation', 'Rig', 'Model']}

# 4 ways to create folders : fixed, variable, variable by folder, fixed by
# folder
# 

# Create .json file storing project relative folders :

# EXAMPLE HIERARCHY TEMPLATE 1 --------------------
# Stored at depth1
PROJECTS = ['project1', 'project2', 'project3', 'project4']

# Stored at depth4
episodes = ['episode1', 'episode2', 'episode3']

# Stored at depth 5
assets = {'CH': ['Anna', 'Ziggs'],
          'PR': ['Chair', 'Table', 'Bowl', 'Spoon'],
          'VEH': ['Bike', 'Car']}
shots = {'episode1': ['shot1', 'shot2'],
         'episode2': ['shot1', 'shot2', 'shot3'],
         'episode3': ['shot1']}

# EXAMPLE HIERARCHY TEMPLATE 2 --------------------
# Stored at depth1
ASSETS = ['Asset1', 'Asset2', 'Asset3']
         
# Create .json file storing user preferences : number of last paths stored as well as last paths stored