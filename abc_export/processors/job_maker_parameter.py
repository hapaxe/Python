__author__ = 'v.moriceau'

import os
from maya import cmds
import common
import job_maker
import cleaning

map(reload,[common, job_maker])

class JobMakerParameter(job_maker.JobMaker):

    def _list_sources(self, selected_only):
        # Get References
        reference_nodes = cmds.ls('*:GEOMETRY_SET*', long=True, type='objectSet', selection=selected_only)
        # If Project is BadPiggies Serie2
        if common.get_shot_infos()['project_id'] == 500:
            # Get Also Reference's References
            reference_nodes += cmds.ls('*:*:GEOMETRY_SET*', long=True, type='objectSet', selection=selected_only)
        # Return
        return reference_nodes

    def _get_asset_name(self, source_node):
        # Get Cube Name
        return "%s_PARAMETER" % common.get_cube_tag(source_node, 'cube_name')

    def _make_occurrence_dict(self, source_node, occurrence_infos):
        # If objectSet
        if cmds.objectType(source_node) == 'objectSet':
            # Verboe
            print " - %s" % source_node.split('|')[-1]
            # Root Locator Name
            root_locator_name = "%s_%s_%03d" % (occurrence_infos['asset_type'],
                                                occurrence_infos['asset_name'],
                                                occurrence_infos['occurrence_number'])
            # Init Members
            root_locator_created = False
            exported_nodes = []
            attributes_to_bake = []
            # Get Set Member's Transforms
            set_member_shapes = common.get_set_shapes(source_node)
            # Each Shape
            for set_member_shape in set_member_shapes:
                # Get Attributes
                attribute_names = [attribute_name for attribute_name in cmds.listAttr(set_member_shape)
                                   if attribute_name.startswith('SP_')]
                # If any
                if attribute_names:
                    # If no root locator
                    if not root_locator_created:
                        # Root Locator
                        cmds.spaceLocator(name=root_locator_name)
                        # Valid
                        root_locator_created = True
                    # Member Shape Short name
                    shape_name_short = set_member_shape.split('|')[-1].split(':')[1].replace('Shape', '')
                    # Each Attr
                    for attribute_name in attribute_names:
                        # Add to baked if not exists
                        if attribute_name not in attributes_to_bake: attributes_to_bake.append(attribute_name)
                        # New Locator Name
                        locator_name = "%s:%s" % (shape_name_short, attribute_name)
                        # Verbose
                        print "\t-> %s" % locator_name
                        # New Locator
                        cmds.spaceLocator(name=locator_name)
                        cmds.parent('|' + locator_name, root_locator_name)
                        # Connect Attributes
                        cmds.connectAttr("%s.%s" % (set_member_shape, attribute_name),
                                         "|%s|%s.translateX" % (root_locator_name, locator_name))
                        # Add Locator to Exported Nodes
                        exported_nodes.append('|%s|%s' % (root_locator_name, locator_name))
            # If any locator Created
            if exported_nodes:
                # Bake TranslateX
                cleaning._bake_geo_attr(exported_nodes, 'translateX')
                # Occurence dict
                occurrence_dict = dict(nodes=exported_nodes, world_space=False, flatten_hierarchy=False,
                                       bake_focal_length=False, bake_visibility=False)
                occurrence_dict.update(occurrence_infos)
                # Rename Asset
                occurrence_infos['asset_name'] += "#"
                # Set Source Node Type
                occurrence_dict['source_node_type'] = 'locatorSet'
                # Return
                return occurrence_dict
