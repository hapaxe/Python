__author__ = 'v.moriceau'

import os
import subprocess
import datetime
import time
from general_purpose_libraries import FileSystem
from maya import cmds
import common
import alembic_exporter
from processors import cleaning
from processors import job_maker
from processors import job_maker_camera
from processors import job_maker_reference
from processors import job_maker_parameter
from processors import job_maker_locator
from processors import job_maker_assembly

DEBUG = False

map(reload, [common, alembic_exporter, cleaning, job_maker,
             job_maker_camera, job_maker_reference, job_maker_parameter, job_maker_locator, job_maker_assembly])

def make_abc(nodes, abc_filepath, attributes=[], frame_in=101, frame_out=149, world_space=True):
    """Retro Compatibility"""
    # New Exporter
    abc_exporter = alembic_exporter.AlembicExporter(framerange=[frame_in, frame_out], attributes=attributes)
    # Add Job
    abc_exporter.add_job(abc_filepath, nodes, world_space=world_space)
    # Export
    abc_exporter.export_standard()


class SceneExporter(object):
    def __init__(self):
        # Init Superclass
        object.__init__(self)
        # Init Member
        self.assemblies_to_restore = []

    def export_scene(self, selected_only=False, relative_root='/datas/abc', popup_explorer=True,
                     include_auto_save_wip=False):
        # Wait Cursor
        cmds.waitCursor(state=True)
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        # Verbose File infos
        print "SceneExporter : File is %s (last modified on %s)" % (__file__, time.ctime(os.path.getmtime(__file__)))
        # Get Shot Infos
        shot_infos = common.get_shot_infos()
        # If info found
        if not shot_infos:
            # Verbose
            print "Current Scene is not a shot"
            # Wait Cursor
            cmds.waitCursor(state=False)
            # Exit
            return
        # Alter task_root for local test
        #shot_infos['task_root'] = "D:/stella_prepaBG_s022/"
        #shot_infos['task_root'] = "D:/BadPiggies_rocket_p001/"
        # Compile Export Folder
        export_folder = os.path.normpath('%s/%s' % (shot_infos["task_root"], relative_root))
        # If Fps is zero
        if shot_infos['frame_rate'] == 0.0:
            # Verbose
            print "Framerate returned 0.0, will use 24.0"
            # Use 24 by default
            shot_infos['frame_rate'] = 24.0
        # Make Dirs
        if not os.path.exists(export_folder + '/temp'):
            os.makedirs(export_folder + '/temp')
        # Reset JobMaker
        job_maker.JobMaker.reset_exporter_assets()
        # Job Makers
        maker_assembly = job_maker_assembly.JobMakerAssembly(export_rootpath=export_folder + '/temp')
        maker_reference = job_maker_reference.JobMakerReference(export_rootpath=export_folder + '/temp')
        maker_parameter = job_maker_parameter.JobMakerParameter(export_rootpath=export_folder + '/temp')
        maker_locator = job_maker_locator.JobMakerLocator(export_rootpath=export_folder + '/temp')
        maker_camera = job_maker_camera.JobMakerCamera(export_rootpath=export_folder + '/temp')
        # Clean Containers
        cleaning.clean_containers()
        # Find Camera
        camera_name = maker_camera._list_sources(selected_only)
        # If found
        if camera_name:
            # Frustum Cull
            culled_nodes = cleaning.frustum_cull(camera_name[0])
        # Else
        else:
            culled_nodes = []
        # New Exporter
        alembic_exporter_standard = alembic_exporter.AlembicExporter(jobs=dict(), framerange=[shot_infos['frame_in'],
                                                                                             shot_infos['frame_out']],
                                                                     attributes=list(), debug=DEBUG)
        # Make Jobs
        maker_assembly.make_jobs(alembic_exporter_standard)
        maker_reference.make_jobs(alembic_exporter_standard)
        maker_camera.make_jobs(alembic_exporter_standard)
        # If Stella
        if shot_infos['project_id'] == 413:
            # Search for Locators
            maker_locator.make_jobs(alembic_exporter_standard)
            # Search for parameters
            maker_parameter.make_jobs(alembic_exporter_standard)
        # Add to Reports
        exported_assets = job_maker.JobMaker.exported_assets
        # Export
        alembic_exporter_standard.export_standard()
        # Verbose
        print "New Scene"
        # New Scene
        cmds.file(newFile=True, force=True)
        cmds.playbackOptions(animationStartTime=shot_infos['frame_in'], animationEndTime=shot_infos['frame_out'],
                             framesPerSecond=shot_infos['frame_rate'])
        # New Exporter
        alembic_exporter_crate = alembic_exporter.AlembicExporter(jobs=dict(), framerange=[shot_infos['frame_in'],
                                                                                           shot_infos['frame_out']],
                                                                     attributes=list(), debug=DEBUG)
        # Verbose
        print "Reconstructing from exported Alembics ..."
        # Each Exported Asset
        for asset_name, exported_occurences in exported_assets.items():
            # Each Exported Occurence
            for occurence_number, occurence_dict in exported_occurences.items():
                # Set Filename of the new abc
                abc_filepath = "%s/%s_%s_%03d.abc" % (export_folder, occurence_dict['asset_type'],
                                                      asset_name, occurence_number)
                # If source node is Assembly Reference i.e only a transform
                if occurence_dict['source_node_type'] in ['assemblyReference', 'locatorSet']:
                    # Copy previously exported Alembic
                    FileSystem.copy_file(occurence_dict['abc_filepath'], abc_filepath)
                    # Update Metadatas
                    exported_assets[asset_name][occurence_number]['abc_filepath'] = abc_filepath
                # If source node is not Assembly Reference
                else:
                    # Compile Parent Locator Name
                    parent_locator_name = "%s_%03d" % (asset_name, occurence_number)
                    # Import corresponding ABC
                    alembic_exporter_crate.import_standard(occurence_dict['abc_filepath'], parent_locator_name)
                    # Update Metadatas
                    exported_assets[asset_name][occurence_number]['abc_filepath'] = abc_filepath
                    # Get Nodes to export
                    nodes_to_export = cmds.listRelatives(parent_locator_name, type='transform', fullPath=True)
                    # Add Job
                    alembic_exporter_crate.add_job(abc_filepath, nodes_to_export, occurence_dict['world_space'])
        # Export
        alembic_exporter_crate.export_crate()
        # Verbose
        print "New Scene"
        # New Scene
        #cmds.file(newFile=True, force=True)
        # If not 'selected only'
        if not selected_only:
            # Compile Json Datas
            metadatas_json = {'shot_infos': shot_infos,
                              'exported_assets': exported_assets,
                              'culled_nodes':len(culled_nodes),
                              'job_maker_errors':maker_assembly.report['error']
                                                 + maker_reference.report['error']
                                                 + maker_camera.report['error'],
                              'job_maker_warnings':maker_assembly.report['warn']
                                                 + maker_reference.report['warn']
                                                 + maker_camera.report['warn']}
            # Export Json
            FileSystem.save_to_json(metadatas_json, export_folder + '/%s_metadatas.json' % timestamp)
            # Prepare Popen Command
            popen_command = 'python %s\\python\\abc_export\\maxscript_generator.py %s %s' % \
                                                (os.path.expandvars('$CUBE_PROJECT_SCRIPTS'),
                                                export_folder.replace('/', '\\') + '\\%s_metadatas.json' % timestamp,
                                                include_auto_save_wip)
            # Verbose
            print popen_command
            # Generate Maxscript in a separate process, Impossible to make correct imports inside Maya :(
            maxscript_process = subprocess.Popen(popen_command, shell=True,
                                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Get Pipe
            process_out, process_err = maxscript_process.communicate()
            # Verbose
            print process_out
            print "Errors : %s" % process_err
        print 'Done !'
        # Popen an Explorer inside the datas folder
        if popup_explorer:
            subprocess.Popen(r'explorer "%s"' % export_folder.replace('/', '\\'))
            # Verbose
            print "Opening : %s" % export_folder.replace('/', '\\')
        # Wait Cursor
        cmds.waitCursor(state=False)
