__author__ = 'v.moriceau'

from maya import cmds
import common
import job_maker
import sys

reload(job_maker)

class JobMakerAssembly(job_maker.JobMaker):

    def _list_sources(self, selected_only):
        # Get Assemblies
        return [transform for transform in cmds.ls(type='transform', long=True, selection=selected_only) if
            cmds.nodeType(transform) == 'assemblyReference' and 'BG_' not in transform.split('|')[-1]]

    def _make_occurrence_dict(self, source_node, occurrence_infos):
        # Get Representation Label
        source_node_representation_label = cmds.assembly(source_node, query=True, activeLabel=True)
        # Case Definition
        case_selector = {'BBOX': self._make_occurrence_dict_base,
                         'LOD0': self._make_occurrence_dict_base,
                         'LOD1': self._make_occurrence_dict_base,
                         'LOD2': self._make_occurrence_dict_base,
                         'setupLOD0': self._make_occurrence_dict_setupLOD0,
                         'setupLOD1': self._make_occurrence_dict_setupLOD2,
                         'setupLOD2': self._make_occurrence_dict_setupLOD2}
        # If Case possible
        if source_node_representation_label in case_selector.keys():
            # Get Nodes
            exported_nodes = case_selector[source_node_representation_label](source_node)
            # If Success
            if exported_nodes:
                # Occurence dict
                occurrence_dict = dict(nodes=exported_nodes, world_space=True, flatten_hierarchy=True,
                                       bake_focal_length=False, bake_visibility=True)
                occurrence_dict.update(occurrence_infos)
                # Return
                return occurrence_dict

    def _make_occurrence_dict_base(self, source_node):
        # Export Alembic file of only assembly
        return [source_node]

    def _make_occurrence_dict_setupLOD0(self, source_node):
        # If CH
        if source_node.startswith('CH_'):
            # Get Cog
            cog_node = common.cog_from_assembly(source_node)
            # Return Cog
            return [cog_node]
        # If AM
        elif source_node.startswith('AM_'):
            # Export on place
            return [source_node]
        # If not CH nor AM
        else:
            # Get GEO Controller
            geo_node = common.geo_from_assembly(source_node)
            # If Found
            if geo_node:
                # Return GEO
                return [geo_node]

    def _make_occurrence_dict_setupLOD2(self, source_node):
        # Message
        message = '\'%s\' is an Assembly while it should be a Reference !' % source_node
        # Verbose
        self.warn(message)