 # Create .json file storing the MAYA_PROJECT_PATH and MAX_PROJECT_PATH as well as the depth and folder hierarchy for both MAYA and MAX :
# Save number of digits for increments and file name template in the file too


{hierarchy_template_1 = {'DEPTH': 6,
                         'increment_depth_save': 6,
                         'increment digits': 4,
                         'increment_template_file_name': '[depth4]_[depth5]_[depth6]_v[increment_digits].ext',
                         'publish_depth_save': 5,
                         'publish_template_file_name': '[depth4]_[depth5]_[depth6]_PUBLISH.ext',
                         'depth0': [PROJECT_PATH_1, PROJECT_PATH_2],
                         'depth1': [**PROJECTS],
                         'depth2': ['scenes', 'sounds', 'sourceimage'],
                         'depth3': ['ASSETS', 'ANIMATION'],
                         'depth4': {'ASSETS': ['CH', 'PR', 'VEH'],
                                    'ANIMATION': [**episodes]},
                         'depth5': {'CH': [**assets], 
                                    'PR': [**assets],
                                    'VEH': [**assets],
                                    **episodes: [**shots]},
                         'depth6': {'ASSETS': ['MODEL', 'RIG', 'TEXTURE'],
                                    'ANIMATION': ['LAYOUT', 'ANIM']}},
 hierarchy_template_2 = {'DEPTH': 2,
                         'increment_depth_save': 2,
                         'increment digits': 3,
                         'increment_template_file_name': '[depth1]_[depth2]_v[increment_digits].ext',
                         'publish_depth_save': 2,
                         'publish_template_file_name': '[depth1]_[depth2].ext',
                         'depth0': PROJECT_PATH_1,
                         'depth1': [**ASSETS],
                         'depth2': ['Animation', 'Rig', 'Model']}
}


# Each DEPTH level can be absolute : (list) ['ASSETS', 'ANIMATION']
# Or relative (to another depth level) : (dict) {'ASSETS': ['MODEL', 'RIG', 'TEXTURE'],
#                                                'ANIMATION': ['LAYOUT', 'ANIM']}}
# In addition, each depth level can be fixed : (str) ['ASSETS', 'ANIMATION']
# Or variable : (var) [**ASSETS] ==> ASSETS = ['Asset1', 'Asset2', 'Asset3']
# They can also be imbricated : {**assets} ==> assets = {'CH': ['Anna', 'Ziggs'],
#                                                        'PR': ['Chair', 'Table', 'Bowl', 'Spoon'],
#                                                        'VEH': ['Bike', 'Car']}

# variable based depth level are going to be based on folder exploration?

# Create .json file storing user preferences : number of last paths stored as well as last paths stored
