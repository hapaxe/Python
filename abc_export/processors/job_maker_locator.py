__author__ = 'v.moriceau'

import os
from maya import cmds
import common
import job_maker

reload(job_maker)

class JobMakerLocator(job_maker.JobMaker):

    def _list_sources(self, selected_only):
        # Get References
        locator_nodes = cmds.ls('*:LOCATOR_NORMAL_SET*', long=True, type='objectSet')
        # Return
        return locator_nodes

    def _get_asset_name(self, source_node):
        # Get Cube Name
        return "%s_LOCATOR" % common.get_cube_tag(source_node, 'cube_name')

    def _make_occurrence_dict(self, source_node, occurrence_infos):
        # If objectSet
        if cmds.objectType(source_node) == 'objectSet':
            # Get Set Member's Transforms
            exported_nodes = common.get_set_transforms(source_node)
            # Occurence dict
            occurrence_dict = dict(nodes=exported_nodes, world_space=False, flatten_hierarchy=True,
                                   bake_focal_length=False, bake_visibility=False)
            occurrence_dict.update(occurrence_infos)
            # Set Source Node Type
            occurrence_dict['source_node_type'] = 'locatorSet'
            # Return
            return occurrence_dict
