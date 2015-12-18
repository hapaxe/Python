__author__ = 'v.moriceau'

import os
import sys
import maya.cmds as cmds
from processors import cleaning

reload(cleaning)

class AlembicExporter(object):
    def __init__(self, jobs={}, framerange=[], attributes=[], debug=False):
        # Init Super class
        object.__init__(self)
        # Add Attributes
        self.jobs = jobs
        self.framerange = framerange
        self.attributes = attributes
        self.debug = debug
        # Verbose
        print "Alembic Exporter : New Exporter [ frames %s - %s ]" % (framerange[0], framerange[1])

    def add_job(self, abc_filepath, nodes, world_space=True, bake_visibilty=True,
                bake_focal_length=True, flatten_hierarchy=True):
        # Check if file not already registered
        if abc_filepath in self.jobs.keys():
            # Verbose
            print "Alembic Exporter : '%s' already registered, adding new nodes to job" % os.path.basename(abc_filepath)
            # Append Nodes
            self.jobs[abc_filepath]['nodes'] += nodes
            # Success
            return True
        # Verbose
        print "Alembic Exporter : '%s' added job" % os.path.basename(abc_filepath)
        # Add to jobs
        self.jobs[abc_filepath] = {'nodes':nodes,
                                   'world_space':world_space,
                                   'bake_visibility':bake_visibilty,
                                   'bake_focal_length':bake_focal_length,
                                   'flatten_hierarchy':flatten_hierarchy}
        # Success
        return True

    def get_nodes_by_flag(self, flag, value):
        # Prepare Return
        collected_nodes = []
        # Each Job
        for job in self.jobs.values():
            # Test Flag
            if job[flag] == value:
                # If nodes
                if job['nodes']:
                    # Append
                    collected_nodes += job['nodes']
        # Return
        return collected_nodes

    def bake_visibility(self):
        # Collect Nodes
        nodes = self.get_nodes_by_flag('bake_visibility', True)
        # Bake Visiblilty
        cleaning.bake_visibility(nodes)

    def bake_focal_length(self):
        # Collect Nodes
        nodes = self.get_nodes_by_flag('bake_focal_length', True)
        # Bake Visiblilty
        cleaning.bake_focal_length(nodes)

    def _make_jobstrings_maya_standard(self):
        # Prepare Jobstrings
        jobstrings = []
        # Each job
        for abc_filepath, job_dict in self.jobs.items():
            # Get Nodes
            nodes = job_dict['nodes']
            world_space = job_dict['world_space']
            flatten_hierarchy = job_dict['flatten_hierarchy']
            # Check nodes number
            if nodes:
                # Nodes
                command_nodes = " ".join(['-root %s' % node for node in nodes])
                # Attributes
                command_attributes = " ".join(['-attr %s' % attribute for attribute in self.attributes])
                # Genereate Job String
                job_string = "-framerange {0} {1} {4} {6} -uvWrite {5} -writeVisibility {2} \
                -file {3}".format(self.framerange[0],
                                  self.framerange[1],
                                  command_nodes,
                                  abc_filepath,
                                  command_attributes,
                                  ['', '-worldSpace'][world_space],
                                  ['', '-stripNameSpaces'][flatten_hierarchy])
                # If Debug
                if self.debug:
                    # Try
                    try:
                        # Export One at a time
                        cmds.AbcExport(j=job_string)
                    # Runtime Error
                    except RuntimeError, e:
                        # Verbose
                        print "Alembic Exporter Debug : Impossible to Export !"
                        print nodes
                        print "Alembic Exporter Debug : Error Message is"
                        print '\n'.join(e.args)
                        print "========================================="
                # Append
                jobstrings.append(job_string)
        # Return
        return jobstrings

    def _make_jobstrings_maya_crate(self):
        # Prepare Jobstrings
        jobstrings = []
        # Each job
        for abc_filepath, job_dict in self.jobs.items():
            # Get Nodes
            nodes = job_dict['nodes']
            world_space = job_dict['world_space']
            flatten_hierarchy = job_dict['flatten_hierarchy']
            # Check nodes number
            if nodes:
                # Nodes
                command_nodes = ",".join(nodes)
                # Attributes
                job_string = "filename=%s;" % abc_filepath
                job_string += "objects=%s;" % command_nodes
                job_string += "in=%s;" % self.framerange[0]
                job_string += "out=%s;" % self.framerange[1]
                job_string += "normals=1;"
                job_string += "dynamictopology=1;"
                job_string += "uvs=1;"
                job_string += "facesets=0;"
                job_string += "globalspace=%s;" % world_space
                job_string += "withouthierarchy=%s;" % int(flatten_hierarchy)
                job_string += "ogawa=1;"
                # If Debug
                if self.debug:
                    # Try
                    try:
                        # Export One at a time
                        cmds.ExocortexAlembic_export(j=[job_string])
                    # Runtime Error
                    except RuntimeError, e:
                        # Verbose
                        print "Alembic Exporter Crate Debug : Impossible to Export !"
                        print nodes
                        print "Alembic Exporter Crate Debug : Error Message is"
                        print '\n'.join(e.args)
                        print "========================================="
                # Append
                jobstrings.append(job_string)
        # Return
        return jobstrings

    def export_crate(self):
        # If any jobs
        if len(self.jobs):
            # Bake Attributes
            self.bake_visibility()
            self.bake_focal_length()
            # Verbose
            print 'Alembic Exporter : Exporting...'
            # Get Jobstring
            jobstrings = self._make_jobstrings_maya_crate()
            # If not debug
            if not self.debug:
                # Try
                try:
                    # Export all at once
                    cmds.ExocortexAlembic_export(j=jobstrings)
                # Runtime Error
                except RuntimeError, e:
                    # Verbose
                    print "Alembic Exporter Crate : Impossible to Export !"
                    print "Alembic Exporter Crate : Error Message is"
                    print '\n'.join(e.args)
                    print "========================================="
        # If no jobs
        else:
            # Verbose
            print "Alembic Exporter : No jobs defined"

    def export_standard(self):
        # If any jobs
        if len(self.jobs):
            # Bake Attributes
            self.bake_visibility()
            self.bake_focal_length()
            # Verbose
            print 'Alembic Exporter : Exporting...'
            # Get Jobstring
            jobstrings = self._make_jobstrings_maya_standard()
            # If not debug
            if not self.debug:
                # Try
                try:
                    # Export all at once
                    cmds.AbcExport(j=jobstrings)
                # Runtime Error
                except RuntimeError, e:
                    # Verbose
                    print "Alembic Exporter : Impossible to Export !"
                    print "Alembic Exporter : Error Message is"
                    print '\n'.join(e.args)
                    print "========================================="
        # If no jobs
        else:
            # Verbose
            print "Alembic Exporter : No jobs defined"

    def import_standard(self, abc_filepath, parent_name):
        # Verbose
        print 'Alembic Exporter : Import %s' % os.path.basename(abc_filepath)
        # New Locator
        cmds.spaceLocator(name=parent_name)
        # Gather all Nodes
        nodes_before = cmds.ls()
        # Import
        cmds.AbcImport(abc_filepath, fitTimeRange=True, reparent=parent_name)
        # Get Imported Nodes
        imported_nodes = list(set(cmds.ls()) - set(nodes_before))
        # Return
        return imported_nodes