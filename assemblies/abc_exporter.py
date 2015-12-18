__author__ = 'v.moriceau'

import os
import maya.cmds as cmds

class AlembicExporter(object):
    def __init__(self, jobs={}, framerange=[101,254], attributes=[], debug=False):
        # Init Super class
        object.__init__(self)
        # Add Attributes
        self.jobs = jobs
        self.framerange = framerange
        self.attributes = attributes
        self.debug = debug

    def add_job(self, abc_filepath, nodes):
        # Check if file not already registered
        if abc_filepath in self.jobs.keys():
            # Verbose
            print "Alembic Exporter : '%s' already registered, adding new nodes to job" % os.path.basename(abc_filepath)
            # Append Nodes
            self.jobs[abc_filepath].append(nodes)
            # Success
            return True
        # Verbose
        print "Alembic Exporter : '%s' added job" % os.path.basename(abc_filepath)
        # Add to jobs
        self.jobs[abc_filepath] = nodes
        # Success
        return True

    def _make_jobstrings(self):
        jobstrings = []
        # Each job
        for abc_filepath, nodes in self.jobs.items():
            # Check nodes number
            if nodes:
                # Nodes
                command_nodes = " ".join(['-root %s' % node for node in nodes])
                # Attributes
                command_attributes = " ".join(['-attr %s' % attribute for attribute in self.attributes])
                # Genereate Job String
                job_string = "-framerange {0} {1} {4} -stripNameSpaces -uvWrite -worldSpace -writeVisibility {2} \
                -file {3}".format(self.framerange[0],
                                  self.framerange[1],
                                  command_nodes,
                                  abc_filepath,
                                  command_attributes)
                # If Debug
                if self.debug:
                    # Try
                    try:
                        # Export One at a time
                        cmds.AbcExport(j=job_string)
                    # Runtime Error
                    except RuntimeError, e:
                        # Verbose
                        print "Alembic Exporter : Impossible to Export !"
                        print nodes
                        print '\n'.join(e.args)
                # Append
                jobstrings.append(job_string)
        # Return
        return jobstrings

    def export(self):
        # Verbose
        print 'Alembic Exporter : Exporting...'
        # Get Jobstring
        jobstrings = self._make_jobstrings()
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
                print '\n'.join(e.args)

def make_abc(nodes, abc_filepath, attributes=[], frame_in=101, frame_out=149):
    """Retro Compatibility"""
    # New Exporter
    abc_exporter = AlembicExporter(jobs={abc_filepath: nodes}, framerange=[frame_in, frame_out],
                                                    attributes=attributes)
    # Export
    abc_exporter.export()