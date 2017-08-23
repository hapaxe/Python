 # Create .json file storing the MAYA_PROJECT_PATH and MAX_PROJECT_PATH as well as the depth and folder hierarchy for both MAYA and MAX :
# Save number of digits for increments and file name template in the file too

hierarchy_template_1 = {'DEPTH': 6,
                        'increment_depth_save': 6,
                        'increment digits': 4,
                        'increment_template_file_name': '[depth4]_[depth5]_[depth6]_v[increment_digits].ext',
                        'publish_depth_save': 4,
                        'publish_template_file_name': '[depth4]_[depth5]_[depth6]_PUBLISH.ext',
                        'depth0': [PROJECT_PATH_1, PROJECT_PATH_2],
                        'depth1': [**PROJECTS],
                        'depth2': ['scenes', 'sounds', 'sourceimage'],
                        'depth3': ['ASSETS', 'ANIMATION'],
                        'depth4': {'ASSETS': ['CH', 'PR', 'VEH'],
                                   'ANIMATION': {**episodes}},
                        'depth5': {'ASSETS': {**assets},
                                   'ANIMATION': {**shots}},
                        'depth6': {'ASSETS': ['MODEL', 'RIG', 'TEXTURE'],
                                   'ANIMATION': ['LAYOUT', 'ANIM']}}

hierarchy_template_2 = {'DEPTH': 2,
                        'increment_depth_save': 2,
                        'increment digits': 3,
                        'increment_template_file_name': '[depth1]_[depth2]_v[increment_digits].ext',
                        'publish_depth_save': 2,
                        'publish_template_file_name': '[depth1]_[depth2].ext',
                        'depth0': PROJECT_PATH_1,
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
