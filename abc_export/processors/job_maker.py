__author__ = 'v.moriceau'

import os
from collections import OrderedDict
from maya import cmds
import common


class JobMaker(object):

    exported_assets = OrderedDict()

    @staticmethod
    def reset_exporter_assets():
        # Reset Static Member
        JobMaker.exported_assets = OrderedDict()

    def __init__(self, export_rootpath):
        # Init Superclass
        object.__init__(self)
        # Set Members
        self.export_rootpath = export_rootpath
        self._init_report()

    def _init_report(self):
        # Initializes Report Dict
        self.report = dict(info=[], warn=[], error=[])

    def info(self, message):
        # Add to member
        self.report['info'].append(message)
        # Verbose
        print "[info] %s : %s" % (self.__class__.__name__, message)

    def warn(self, message):
        # Add to member
        self.report['warn'].append(message)
        # Verbose
        print "[warn] %s : %s" % (self.__class__.__name__, message)

    def error(self, message):
        # Add to member
        self.report['error'].append(message)
        # Verbose
        print "[erro] %s : %s" % (self.__class__.__name__, message)

    def _make_abc_filepath(self, occurrence_infos):
        # Compile abc filepath
        abc_filepath = os.path.normpath(os.path.join(self.export_rootpath,
                                    '%s_%s_%03d.abc' % (
                                        occurrence_infos["asset_type"],
                                        occurrence_infos["asset_name"],
                                        occurrence_infos["occurrence_number"]
                                    ))
        ).replace('\\', '/')
        # Return
        return abc_filepath

    def nodes(self):
        # Nodes
        nodes = []
        # If Any Asset
        if JobMaker.exported_assets.values():
            # Each Exported Asset
            for asset_dict in JobMaker.exported_assets.values():
                # Each Occurence
                for occurrence_dict in asset_dict.values():
                    # If any
                    if occurrence_dict:
                        # Append
                        nodes += occurrence_dict['nodes']
        # Return
        return nodes

    def _get_asset_name(self, source_node):
        # Get Cube Name
        return common.get_cube_tag(source_node, 'cube_name')

    def get_occurrence_dict(self, source_node):
        # Get Asset Name
        cube_name = self._get_asset_name(source_node)
        # If found
        if cube_name:
            # Get Asset Type
            cube_type = common.get_cube_tag(source_node, 'cube_type')
            # Get Occurrence Number
            if cube_name in JobMaker.exported_assets.keys():
                # Increment Occurence number
                occurence_number = len(JobMaker.exported_assets[cube_name].keys()) + 1
            else:
                # Init dict entry
                JobMaker.exported_assets[cube_name] = {}
                # Init Occurence counter
                occurence_number = 1
            # Set Occurence Infos
            occurrence_infos = {'asset_name': cube_name,
                                'asset_type': cube_type,
                                'source_node': source_node,
                                'occurrence_number': occurence_number,
                                'source_node_type': cmds.objectType(source_node)}
            # Add Alembic Filepath to Dict
            occurrence_infos['abc_filepath'] = self._make_abc_filepath(occurrence_infos)
            # Process Infos into Occurrence dict
            occurrence_dict = self._make_occurrence_dict(source_node, occurrence_infos)
            # If Anything
            if occurrence_dict:
                # Store Occurence Dict
                JobMaker.exported_assets[cube_name][occurence_number] = occurrence_dict
            # Return Occurence Dict
            return occurrence_dict
        # If Tag not found
        self.warn("Tag not found for node '%s'" % source_node)

    def _list_sources(self, selected_only):
        """Should Return a list of the nodes that are sources for assets (assembly reference, selection set, ...)"""
        # Raise
        raise NotImplementedError

    def _make_occurrence_dict(self, source_node, occurence_infos):
        """Should get all nodes associated with given source node name
        Return a copy of occurence_infos plus 'exported_nodes': [] and 'world_space': bool"""
        # Raise
        raise NotImplementedError

    def make_jobs(self, alembic_exporter, selected_only=False):
        # Reset Report
        self._init_report()
        # List All Sources
        source_nodes = self._list_sources(selected_only=selected_only)
        # Verbose
        for source_node in source_nodes:
            self.info("'%s' added to sources" % source_node)
        # Each Source Node
        for source_node in source_nodes:
            # Get Occurences Dict
            occurrence_dict = self.get_occurrence_dict(source_node)
            # If success
            if occurrence_dict:
                # Add job to Exporter
                alembic_exporter.add_job(abc_filepath=occurrence_dict['abc_filepath'],
                                         nodes=occurrence_dict['nodes'],
                                         world_space=occurrence_dict['world_space'],
                                         bake_visibilty=occurrence_dict['bake_visibility'],
                                         bake_focal_length=occurrence_dict['bake_focal_length'],
                                         flatten_hierarchy=occurrence_dict['flatten_hierarchy'])
        # Return Rapport
        return self.report
