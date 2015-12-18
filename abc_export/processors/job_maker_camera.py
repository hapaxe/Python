__author__ = 'v.moriceau'

from maya import cmds
import common
import job_maker

reload(job_maker)

class JobMakerCamera(job_maker.JobMaker):

    def _list_sources(self, selected_only):
        # Get Cameras
        cameras = cmds.ls(long=True, type='camera', selection=selected_only)
        camera_transform = []
        # Each Camera
        for camera in cameras:
            # Try to get Tag
            if common.get_cube_tag(camera, 'cube_name'):
                # Get Transform
                camera_transform = cmds.listRelatives(camera, type='transform', parent=True)
        # If no Camera found
        if not camera_transform:
            # Inform Report
            self.warn("No Tagged Camera Found")
        # Return
        return camera_transform

    def _make_occurrence_dict(self, source_node, occurrence_infos):
        # Occurence dict
        occurrence_dict = dict(nodes=[source_node], world_space=True, flatten_hierarchy=True,
                               bake_focal_length=True, bake_visibility=False)
        occurrence_dict.update(occurrence_infos)
        # Return
        return occurrence_dict
