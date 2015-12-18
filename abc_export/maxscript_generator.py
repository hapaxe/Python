__author__ = 'v.moriceau'

import os
import sys
import json
import datetime
import traceback
import alembic
from general_purpose_libraries import FileSystem
import tube_libraries

class MaxscriptGenerator(object):

    def __init__(self, filepath=""):
        self.filepath = filepath
        self._script = ""

    def add_maxscript(self, maxscript):
        # Add to Script Maxscript
        self._script += str(maxscript)

    def reset(self):
        # Reset Script Content
        self._script = ""

    def save(self):
        # Create a local context around script
        self._script = "%s\n)" % self._script
        # If filename given
        if self.filepath:
            # Create File
            with open(self.filepath, 'w+') as file_object:
                # Write Content
                file_object.write(self._script)

    def generate_script(self, filepath_in, force_import=False, include_auto_save_wip=False):
        # Report
        export_report = {'not_published':[], 'missing_alembic_file':[], 'no_shading':[]}
        # Prepare Assets
        export_metadatas = FileSystem.load_from_json(filepath_in)
        # If Success
        if export_metadatas:
            # Get Scene datas
            shot_infos = export_metadatas['shot_infos']
            # Occurence Count
            occurence_count = 0
            # Get project id
            project_id = shot_infos['project_id']
            # Get Exported Assets
            exported_assets = export_metadatas['exported_assets']
            # Init Asset Dicts
            assets_dicts = []
            # Each Asset
            for asset_name, asset_dict in exported_assets.items():
                # Hotfix on Ambiances
                if asset_name in ['niSC001', 'niSt002'] : asset_name = 'niSt001'
                # If asset has occurence(s)
                if len(asset_dict.keys()):
                    # If Camera
                    if asset_dict['1']['asset_type'] == 'CM':
                        # Fake asset for CM type
                        assets_dicts.append({'shading':{'type_name':'CM'},
                                            'alembic_filepath':asset_dict['1']['abc_filepath'],
                                            'source_node_type':'camera'})
                    else:
                        # Find Asset Dict in Tube
                        tube_asset_dict = tube_libraries.get_asset_infos(
                                                        asset_name.replace('_LOCATOR', '').replace('_PARAMETER', ''),
                                                        project_id)
                        # Each Occurrence
                        for occurence_number, export_infos in asset_dict.items():
                            # Add Fields
                            tube_asset_dict['asset_name'] = asset_name
                            tube_asset_dict['alembic_filepath'] = export_infos['abc_filepath']
                            tube_asset_dict['source_node_type'] = export_infos['source_node_type']
                            # Append copy Dict to import
                            assets_dicts.append(dict(tube_asset_dict))
                            # Increment
                            occurence_count += 1
            # Init Scene
            self.init_scene(shot_infos['frame_rate'], shot_infos['frame_in'], shot_infos['frame_out'], occurence_count)
            # Each Asset
            for asset_dict in assets_dicts:
                # If asset has occurence(s)
                if len(asset_dict.keys()):
                    # If Locator
                    if '_LOCATOR' in asset_dict['alembic_filepath']:
                        # Get Infos form filepath
                        asset_type, asset_name, locator, occurence_number = os.path.basename(asset_dict['alembic_filepath']).split('.')[0].split('_')
                        # Simply Import Alembic File
                        self._merge_locator(asset_dict['alembic_filepath'], asset_name, int(occurence_number))
                    # If Parameter
                    elif '_PARAMETER' in asset_dict['alembic_filepath']:
                        # Get Infos form filepath
                        asset_type, asset_name, parameter, occurence_number = os.path.basename(asset_dict['alembic_filepath']).split('.')[0].split('_')
                        # Simply Import Alembic File
                        self._merge_parameter(asset_dict['alembic_filepath'], asset_name, int(occurence_number))
                    # If Not Locator
                    else:
                        # Get Asset Type
                        try:
                            asset_type = asset_dict.values()[0]['type_name']
                        except TypeError, e:
                            print "\nMaxscript Generator : Error !!"
                            print "Maxscript Generator : '%s'\n%s" % (e.args[0], traceback.format_exc())
                            print json.dumps(asset_dict, indent=2)
                            print "- - - - - - - - - - - - - - - - - -"
                            continue
                        # If Task 'Shading' Exists
                        if 'shading' not in asset_dict.keys():
                            # Asset Name
                            asset_name = asset_dict.values()[0]['asset_name']
                            # Verbose
                            print " - %s : No 'shading' task !" % asset_name
                            # Add to report
                            export_report['no_shading'].append(asset_name)
                            # Skip loop
                            continue
                        # Get Task Dict
                        task_dict = asset_dict['shading']
                        # Get Alembic File
                        abc_filepath = FileSystem.normpath(asset_dict['alembic_filepath'])
                        # If PR, CH, BG, AM, FX
                        if asset_type  in ['PR', 'CH', 'BG', 'AM', 'FX']:
                            # Get Asset Name
                            asset_name = asset_dict['asset_name']
                            # Prepare Max Filepath
                            max_filepath = None
                            # If Published
                            if task_dict['scene_check'] in ['publish', 'wip_pub']:
                                # Get Published Scene
                                max_filepath = task_dict['publish_p']
                            # If Not Published
                            else:
                                # Verbose
                                print "\t! %s is not published !" % asset_name
                                # Add to report
                                export_report['not_published'].append(asset_name)
                                # If force
                                if force_import:
                                    # Get Last WIP Scene
                                    max_filepath = task_dict['scene_path']
                            # If Max File
                            if max_filepath :
                                # If Alembic filepath
                                if abc_filepath:
                                    # Get Alembic Top
                                    root_name = self._get_alembic_top(abc_filepath)
                                    # Verbose
                                    print root_name
                                    print "\t<- %s" % max_filepath
                                    print "\t<- %s" % abc_filepath
                                    print "\t<- [%s]" % asset_dict['source_node_type']
                                    # Reparent to
                                    reparent_to = '%s_ROOT' % asset_type
                                    # assemblyReference -> BG / AM
                                    if asset_dict['source_node_type'] == 'assemblyReference':
                                        # Always reparent to BG_ROOT
                                        reparent_to = 'BG_ROOT'
                                        # Merge Accordingly
                                        self._merge_position(max_filepath, abc_filepath, root_name, reparent_to)
                                    # If Position
                                    else:
                                        # Merge Accordingly
                                        self._merge_deformation(max_filepath, abc_filepath, root_name, reparent_to)
                                # If no abc
                                else:
                                    # Verbose
                                    print "Fichier .abc n'existe pas !"
                                    # Add to report
                                    export_report['missing_alembic_file'].append(abc_filepath)
                        # if CM
                        elif asset_type == 'CM':
                            # Verbose
                            print "Camera"
                            print "\t<- %s" % abc_filepath
                            # Merge Camera
                            self._merge_camera(abc_filepath)
                        # Separator
                        print ""
            # If Should save
            if include_auto_save_wip:
                # Save
                self.add_maxscript("\n-- Finalize and Save WIP")
                self.add_maxscript('\nclean_importer_.finalize '
                                   'proj_name:"{0}" '
                                   'proj_description:"{1}" '
                                   'season_number:{2} '
                                   'episode_number:{3} '
                                   'seq_number:{4} '
                                   'shot_number:{5} '
                                   'task_name:"{6}"'.format(shot_infos['proj_name'],
                                                            shot_infos['proj_description'],
                                                            shot_infos['season_number'],
                                                            shot_infos['episode_number'],
                                                            shot_infos['sequence_number'],
                                                            shot_infos['shot_number'],
                                                            'clean'))
            # No need to save
            else:
                # Finalize
                self.add_maxscript("\n-- Finalize")
                self.add_maxscript("\nclean_importer_.finalize()\n")
            # Set filename
            self.filepath = "%s\\generate_clean.ms" % os.path.dirname(filepath_in)
            # Save
            self.save()
            # Export Json
            FileSystem.save_to_json(export_report, os.path.dirname(filepath_in) + '\\maxscript_report.json')

    def init_scene(self, frame_rate, frame_in, frame_out, occurence_count):
        # Init Scene
        self.add_maxscript("""-- GENERATED BY MAXSCRIPT GENERATOR
-- STELLA / BAD PIGGIES CLEAN EXPORTER
-- {3}
(
-- New Clean Importer
clean_importer_ = clean_importer()
-- Init Scene
clean_importer_.init_scene {0} {1} {2} operation_count:{4}
""".format(frame_rate, frame_in, frame_out,
           datetime.datetime.now().strftime('%a %d %b %Y - %H:%M:%S'), occurence_count))

    def _merge_locator(self, abc_filepath, asset_name, occurence_number):
        # Prepare MaxScript
        maxscript = """
-- Locator
clean_importer_.merge_locator @"{0}" asset_name:"{1}" occurence_number:{2}
""".format(os.path.normpath(abc_filepath), asset_name, occurence_number)
        # Add to Script
        self.add_maxscript(maxscript)

    def _merge_parameter(self, abc_filepath, asset_name, occurence_number):
        # Prepare MaxScript
        maxscript = """
-- Parameter
clean_importer_.merge_parameter @"{0}" asset_name:"{1}" occurence_number:{2}
""".format(os.path.normpath(abc_filepath), asset_name, occurence_number)
        # Add to Script
        self.add_maxscript(maxscript)

    def _merge_camera(self, abc_filepath):
        # Prepare MaxScript
        maxscript = """
-- Camera
clean_importer_.merge_camera @"{0}"
""".format(os.path.normpath(abc_filepath))
        # Add to Script
        self.add_maxscript(maxscript)

    def _merge_position(self, filepath, abc_filepath, root_name, reparent_to):
        # Generate Maxscript
        maxscript = """
-- {0}
clean_importer_.merge_position @"{1}" @"{2}" "{3}" "{4}"
""".format(os.path.basename(abc_filepath), os.path.normpath(filepath),
           os.path.normpath(abc_filepath), root_name, reparent_to)
        # Add to Script
        self.add_maxscript(maxscript)

    def _merge_deformation(self, filepath, abc_filepath, root_name, reparent_to):
        # Generate Maxscript
        maxscript = """
-- {0}
clean_importer_.merge_deformation @"{1}" @"{2}" "{3}"
""".format(os.path.basename(abc_filepath), os.path.normpath(filepath), os.path.normpath(abc_filepath), reparent_to)
        # Add to Script
        self.add_maxscript(maxscript)

    def _get_alembic_top(self, abc_filepath):
        # Open Archive
        iarch = alembic.Abc.IArchive(str(abc_filepath))
        # Get Top
        top = iarch.getTop()
        # Return First Node Name
        return top.children[0].getName()


if __name__ == '__main__':
    # If Argument count ok
    if len(sys.argv) == 3:
        # Verbose
        print "Generating Maxscript ..."
        # New Generator
        maxscript_generator = MaxscriptGenerator()
        # Generate
        maxscript_generator.generate_script(filepath_in=sys.argv[1], include_auto_save_wip=bool(sys.argv[2]))