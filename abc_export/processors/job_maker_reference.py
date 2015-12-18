__author__ = 'v.moriceau'

from maya import cmds
import common
import job_maker

reload(job_maker)

class JobMakerReference(job_maker.JobMaker):

    def _list_sources(self, selected_only):
        # Get References
        reference_nodes = cmds.ls('*:GEOMETRY_SET*', long=True, type='objectSet', selection=selected_only)
        # If Project is BadPiggies Serie2
        if common.get_shot_infos()['project_id'] == 500:
            # Get Also Reference's References
            reference_nodes += cmds.ls('*:*:GEOMETRY_SET*', long=True, type='objectSet', selection=selected_only)
        # Return
        return reference_nodes

    def _make_occurrence_dict(self, source_node, occurrence_infos):
        # If objectSet
        if cmds.objectType(source_node) == 'objectSet':
            # Get Set Member's Transforms
            exported_nodes = common.get_set_transforms(source_node)
            # Occurence dict
            occurrence_dict = dict(nodes=exported_nodes, world_space=True, flatten_hierarchy=True,
                                   bake_focal_length=False, bake_visibility=True)
            occurrence_dict.update(occurrence_infos)
            # Return
            return occurrence_dict
