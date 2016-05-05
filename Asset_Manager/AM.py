from pprint import pprint


import os
import glob
import maya.cmds as mc
from PySide.QtCore import *
from PySide.QtGui import *
import AM_ui as AM_ui

reload(AM_ui)


class AMClass(QMainWindow, AM_ui.Ui_Asset_Manager_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Declaring projects directory path
        self.project_path = 'D:/BOULOT/TRAVAUX_PERSO/MAYA PROJECTS'
        self.hierarchy = self.list_hierarchy()

        # Populating menus
        project_list = [project for project in self.hierarchy.keys()]
        project_list.sort()
        self.update_combobox(self.project_comboBox, project_list)
        self.update_asset_anim_comboBox()

        # Connecting ui selections
        self.project_comboBox.currentIndexChanged.connect(self.update_asset_anim_comboBox)
        self.asset_anim_comboBox.currentIndexChanged.connect(self.update_type_episode_combobox)
        self.asset_type_episode_comboBox.currentIndexChanged.connect(self.update_asset_shot_combobox)
        self.asset_shot_comboBox.currentIndexChanged.connect(self.update_task_combobox)
        self.task_comboBox.currentIndexChanged.connect(self.update_files_list)

        # Connecting buttons
        self.open_pushButton.clicked.connect(self.open_file)
        self.open_publish_pushButton.clicked.connect(self.open_publish)
        self.save_pushButton.clicked.connect(self.save_file)
        self.wip_pushButton.clicked.connect(self.save_wip_file)
        self.publish_pushButton.clicked.connect(self.save_publish_file)

        self.select_current_open()

    # ------------------------------------------------------------------------------------------------------------------
    def list_hierarchy(self):
        hierarchy = dict()

        projects = self.create_subdir_list(self.project_path)

        for project in projects:
            project_dict = dict()

            project_subdir = self.create_subdir_list('%s/%s/scenes/' % (self.project_path, project))

            for directory in project_subdir:
                dir_dict = dict()

                types = self.create_subdir_list('%s/%s/scenes/%s/' % (self.project_path, project, directory))

                for type_dir in types:
                    type_dict = dict()

                    assets = self.create_subdir_list('%s/%s/scenes/%s/%s/' % (self.project_path, project,
                                                                              directory, type_dir))

                    for asset in assets:
                        asset_dict = dict()

                        tasks = self.create_subdir_list('%s/%s/scenes/%s/%s/%s/' % (self.project_path,
                                                                                    project, directory,
                                                                                    type_dir, asset))

                        for task in tasks:
                            task_dict = dict()
                            task_dict['task'] = task

                            task_files = self.build_files_list('%s/%s/scenes/%s/%s/%s/%s/' % (self.project_path,
                                                                                              project, directory,
                                                                                              type_dir, asset,
                                                                                              task))
                            asset_dict[task] = task_files

                        type_dict[asset] = asset_dict

                    dir_dict[type_dir] = type_dict

                    project_dict[directory] = dir_dict

            hierarchy[project] = project_dict

        return hierarchy

    # ------------------------------------------------------------------------------------------------------------------
    def create_subdir_list(self, given_path):
        """
        create list of the subdirectories in the given directory
        :param path: directory to list subdirectories in
        :return: list of the subdirectories
        """
        # List all the directories at the given path
        subdir_list = [sub_path for sub_path in os.listdir(given_path) if os.path.isdir(given_path+'/'+sub_path)]

        # Unlisting mayaSwatches, keyboard and edits
        subdir_list = [directory for directory in subdir_list
                       if directory != '.mayaSwatches' and directory != 'Keyboard' and directory != 'edits']

        # Returning list
        return subdir_list

    # ------------------------------------------------------------------------------------------------------------------
    def build_files_list(self, given_path):
        os.chdir(given_path)
        # Filter files
        files = [dir_file for dir_file in os.listdir(given_path) if os.path.isfile(os.path.join(given_path, dir_file))]
        # Filter maya files
        maya_files = [maya_file for maya_file in files
                      if '.ma' in maya_file or '.mb' in maya_file or '.fbx' in maya_file]
        # If no maya files
        if maya_files == []:
            # list is used as verbose
            maya_files = ['No file in this directory']
        # If there are maya files
        else:
            # Sort them
            maya_files.sort(key=lambda x: os.path.getmtime(x))
            # Get most recent in first
            maya_files.reverse()

        return maya_files

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def get_am_ui_datas(self):
        """
        Get datas from UI
        :return: list of all the UI datas (list)
        """
        # Projet
        project = self.project_comboBox.currentText()
        # Asset/Anim
        asset_anim = self.asset_anim_comboBox.currentText()
        # Asset type
        asset_type_episode = self.asset_type_episode_comboBox.currentText()
        # Asset
        asset_shot = self.asset_shot_comboBox.currentText()
        # Task
        task = self.task_comboBox.currentText()
        # File
        file_name = self.files_listWidget.selectedItems()
        if file_name != []:
            file_name = file_name[0].text()
        else:
            file_name = 'None'

        return [project, asset_anim, asset_type_episode, asset_shot, task, file_name]
    # ------------------------------------------------------------------------------------------------------------------
    def build_path(self, return_type='project'):
        # Get datas from ui
        datas = self.get_am_ui_datas()

        if return_type == 'project':
            return_path = '%s/%s' % (self.project_path, datas[0])
        elif return_type == 'file':
            return_path = '%s/%s/scenes/%s/%s/%s/%s/%s' % (self.project_path,
                                                           datas[0], datas[1], datas[2], datas[3], datas[4], datas[5])
        elif return_type == 'wip':
            if datas[5] == 'No file in this directory':
                wip_file = '%s_%s_%s_00.ma' % (datas[2], datas[3], datas[4])
            else:
                # Split file name
                wip_file = datas[5].split('.')[0]
                print wip_file
                wip_file = wip_file.split('_')
                print wip_file
                # Increment version number
                wip_file[3] = self.build_increment(wip_file[3])
                print wip_file[3]
                # Join publish file name
                wip_file = ('_').join(wip_file)
                print wip_file
            # Build path
            return_path = '%s/%s/scenes/%s/%s/%s/%s/%s' % (self.project_path,
                                                        datas[0], datas[1], datas[2], datas[3], datas[4], wip_file)
            print return_path
        else:
            # Split file name
            publish_file = datas[5].split('_')
            # Remove increment and extension
            publish_file = publish_file[:3]
            print publish_file
            # Append PUBLISH plus extension
            publish_file.append('PUBLISH.ma')
            print publish_file
            # Join publish file name
            publish_file = ('_').join(publish_file)
            print publish_file
            # Build path
            return_path = '%s/%s/scenes/%s/%s/%s/%s' % (self.project_path,
                                                        datas[0], datas[1], datas[2], datas[3], publish_file)

        return return_path

    # ------------------------------------------------------------------------------------------------------------------
    def build_increment(self, number):
        """

        :param number: number you want to increment
        :return: incremented number (string)
        """
        increment = int(number)
        increment += 1
        increment = list(str(increment))

        if len(increment) < 2:
            increment.insert(0, '0')

        increment = ('').join(increment)

        return increment

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def update_combobox(self, combobox, items, block='True'):
        """
        Update the given combobox
        :param combobox: combobox to update,  ie: self.bs_node_menu
        :param items: list of items to add to the given combobox
        """

        # --- Blocking signals from ui
        if block:
            combobox.blockSignals(True)
        else:
            pass

        # --- Init items if empty
        if items == []:
            items = ['None']

        # --- Get currently selected text
        selected_text = combobox.currentText()

        # --- Clear combobox
        combobox.clear()
        # --- Add items
        combobox.addItems(items)

        # --- If current selected item in new item list, select it
        if selected_text in items:
            self.select_combobox_index_from_text(combobox, selected_text)
        else:
            combobox.setCurrentIndex(0)

        for i, item in enumerate(items):
            combobox.setItemData(i, item, Qt.ToolTipRole)

        # --- Unblocking signals from ui
        combobox.blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def update_ui(self):
        self.hierarchy = self.list_hierarchy()

        project_list = [project for project in self.hierarchy.keys()]
        project_list.sort()
        self.update_combobox(self.project_comboBox, project_list)
        self.update_asset_anim_comboBox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_asset_anim_comboBox(self):
        # Get datas from ui
        datas = self.get_am_ui_datas()
        # Set project directory
        self.set_current_project_directory()
        # Build list
        asset_anim_list = [directory for directory in self.hierarchy[datas[0]]]

        # Update comboBox
        self.update_combobox(self.asset_anim_comboBox, asset_anim_list)

        # Init update type/episode combobox
        self.update_type_episode_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_type_episode_combobox(self):
        # Get datas from ui
        datas = self.get_am_ui_datas()
        # Build list
        types_list = [asset_type for asset_type in self.hierarchy[datas[0]][datas[1]]]

        # Change labels according to selection
        if datas[1] == 'ANIMATION':
            self.asset_type_episode_label.setText('Episode')
            self.asset_shot_label.setText('Shot')
        else:
            self.asset_type_episode_label.setText('Type')
            self.asset_shot_label.setText('Asset')

        # Update comboBox
        self.update_combobox(self.asset_type_episode_comboBox, types_list)

        # Init update asset/shot combobox
        self.update_asset_shot_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_asset_shot_combobox(self):
        # Get datas from ui
        datas = self.get_am_ui_datas()
        # Build list
        assets_list = [asset for asset in self.hierarchy[datas[0]][datas[1]][datas[2]]]

        # Update comboBox
        self.update_combobox(self.asset_shot_comboBox, assets_list)

        # Init update task combobox
        self.update_task_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_task_combobox(self):
        # Get datas from ui
        datas = self.get_am_ui_datas()
        # Build list
        task_list = [asset for asset in self.hierarchy[datas[0]][datas[1]][datas[2]][datas[3]]]

        # Update comboBox
        self.update_combobox(self.task_comboBox, task_list)

        # Init update files list
        self.update_files_list()

    # ------------------------------------------------------------------------------------------------------------------
    def update_files_list(self):
        """
        Update the targets qlistwidget
        :param selected_bs_targets : currently selected target in bs_node_menu combobox
        """
        # Get datas from ui
        datas = self.get_am_ui_datas()

        maya_files = [maya_file for maya_file in self.hierarchy[datas[0]][datas[1]][datas[2]][datas[3]][datas[4]]]

        # Clear and recreate the list
        self.files_listWidget.clear()
        self.files_listWidget.addItems(maya_files)

        # Select item at index 0
        self.files_listWidget.item(0).setSelected(True)

    # ------------------------------------------------------------------------------------------------------------------
    def set_current_project_directory(self):
        # Build path
        project_path = self.build_path('project')
        # Set current directory
        mc.workspace(dir=project_path)

    # ------------------------------------------------------------------------------------------------------------------
    def select_combobox_index_from_text(self, combobox, text):
        # Get index from the text
        text_index = combobox.findText(text)
        # Select text from index
        combobox.setCurrentIndex(text_index)

    # ------------------------------------------------------------------------------------------------------------------
    def select_current_open(self):
        # Get current open file
        open_file = mc.file(q=True, exn=True)

        # Check if path contains '/scenes/'
        if '/scenes/' not in open_file:
            pass
        # If yes, split it and defines the different part
        else:
            path_split = open_file.split('/scenes/')[1].split('/')
            project = open_file.split('/scenes/')[0].split('/')[-1]
            asset_anim = path_split[0]
            asset_type_episode = path_split[1]
            asset_shot = path_split[2]
            task = path_split[3]
            file_name = path_split[-1]
            # Try to select project, asset/anim, and so on
            if project in self.hierarchy:
                self.select_combobox_index_from_text(self.project_comboBox, project)
                if asset_anim in self.hierarchy[project]:
                    self.select_combobox_index_from_text(self.asset_anim_comboBox, asset_anim)
                    if asset_type_episode in self.hierarchy[project][asset_anim]:
                        self.select_combobox_index_from_text(self.asset_type_episode_comboBox, asset_type_episode)
                        if asset_shot in self.hierarchy[project][asset_anim][asset_type_episode]:
                            self.select_combobox_index_from_text(self.asset_shot_comboBox, asset_shot)
                            if task in self.hierarchy[project][asset_anim][asset_type_episode][asset_shot]:
                                self.select_combobox_index_from_text(self.task_comboBox, task)
                                if file_name in self.hierarchy[project][asset_anim][asset_type_episode][asset_shot][task]:
                                    item = self.files_listWidget.findItems(file_name, Qt.MatchExactly)[0]
                                    index = self.files_listWidget.indexFromItem(item)
                                    self.files_listWidget.item(index.row()).setSelected(True)
            # If can't find it, verbose
                                else:
                                    print file_name, 'not found'
                            else:
                                print task, ' not found'
                        else:
                            print asset_shot, ' not found'
                    else:
                        print asset_type_episode, ' not found'
                else:
                    print asset_anim, ' not found'
            else:
                print project, ' not found'

    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------BUTTONS-------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def open_file(self):
        file_path = self.build_path('file')
        # Open
        mc.file(file_path, o=True, f=True)
        # Verbose
        print file_path.split('/')[-1], ' has been open'

    # ------------------------------------------------------------------------------------------------------------------
    def open_publish(self):
        # Build path
        file_path = self.build_path('publish')
        # Open
        if os.path.isfile(file_path):
            print file_path
            mc.file(file_path, o=True, f=True)
            # Verbose
            print file_path.split('/')[-1], ' has been open'
        else:
            print 'No publish associated to selected file'

    # ------------------------------------------------------------------------------------------------------------------
    def save_file(self):
        # Get current open file
        open_file = mc.file(q=True, exn=True)

        # Build file path
        file_path = self.build_path('file')

        # If open file match selected file
        if open_file == file_path:
            # Save
            mc.file(s=True, f=True)
            # Verbose
            print file_path.split('/')[-1], ' has been saved'
        # If not, pass (for now)
        else:
            print 'Open file does not match selection. Essaie pas de me la faire a l\'envers!' \
                  'Petit salaud! File faire un wip avant.'

    # ------------------------------------------------------------------------------------------------------------------
    def save_wip_file(self):
        # Build file path
        wip_file_path = self.build_path('wip')

        # Save
        mc.file(rename=wip_file_path)
        mc.file(s=True, f=True)
        # Verbose
        print wip_file_path.split('/')[-1], ' has been saved'

        self.update_ui()

    # ------------------------------------------------------------------------------------------------------------------
    def save_publish_file(self):
        # Get current open file
        open_file_path = mc.file(q=True, exn=True)

        open_file_path_tmp = open_file_path.split('/')
        open_file_path_tmp[-1] = open_file_path_tmp[-1].split('_')[0:3]
        open_file = ('_').join(open_file_path_tmp[-1])


        # Build file path
        file_path = self.build_path('publish')
        print file_path
        publish_file = file_path.split('/')[-1]
        print publish_file

        # If open file match selected file
        if open_file in file_path:
            # Save
            mc.file(rename=file_path)
            mc.file(s=True, f=True)
            mc.file(rename=open_file_path)
            # Verbose
            print file_path.split('/')[-1], ' has been published'
        # If not, pass (for now)
        else:
            print 'Open file does not match selection. Essaie pas de me la faire a l\'envers!' \
                  'Petit salaud! File faire un wip avant.'
