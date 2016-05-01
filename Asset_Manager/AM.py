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

        # Populating menus
        project_list = self.create_subdir_list(self.project_path)
        self.update_combobox(self.project_comboBox, project_list)
        self.update_tabs_comboBox()

        # Connecting ui selections
        self.project_comboBox.currentIndexChanged.connect(self.update_tabs_comboBox)
        self.asset_anim_tabWidget.currentChanged.connect(self.update_tabs_comboBox)
        self.asset_type_comboBox.currentIndexChanged.connect(self.update_asset_combobox)
        self.asset_comboBox.currentIndexChanged.connect(self.update_task_comboBox)
        self.shot_comboBox.currentIndexChanged.connect(self.update_task_comboBox)
        self.task_comboBox.currentIndexChanged.connect(self.update_files_list)

        # Connecting buttons
        self.open_pushButton.clicked.connect(self.open_file)

    # ------------------------------------------------------------------------------------------------------------------
    def get_am_ui_datas(self):
        """
        Get datas from UI
        :return: list of all the UI datas (list)
        """
        # Projet
        project = self.project_comboBox.currentText()
        # Asset/Anim
        asset_anim_index = self.asset_anim_tabWidget.currentIndex()
        asset_anim = self.asset_anim_tabWidget.tabText(asset_anim_index)
        # Asset type
        asset_type = self.asset_type_comboBox.currentText()
        # Episode
        episode = self.episode_comboBox.currentText()
        # Asset
        asset = self.asset_comboBox.currentText()
        # Shot
        shot = self.shot_comboBox.currentText()
        # Task
        task = self.task_comboBox.currentText()
        # File
        file_name = self.files_listWidget.selectedItems()
        if file_name != []:
            file_name = file_name[0].text()
        else:
            file_name = 'None'

        return [project, asset_anim, asset_type, episode, asset, shot, task, file_name]

    # ------------------------------------------------------------------------------------------------------------------
    def create_subdir_list(self, path):
        """
        create list of the subdirectories in the given directory
        :param path: directory to list subdirectories in
        :return: list of the subdirectories
        """
        subdir_list = [sub_path for sub_path in os.listdir(path) if os.path.isdir(path+'/'+sub_path)]

        # unlisting mayaSwatches, keyboard and edits
        subdir_list = [directory for directory in subdir_list
                       if directory != '.mayaSwatches' and directory != 'Keyboard' and directory != 'edits']

        # returning list
        return subdir_list

    # ------------------------------------------------------------------------------------------------------------------
    def build_files_list(self, path):
        # List everything in the folder
        os.chdir(path)
        # Filter files
        files = filter(os.path.isfile, os.listdir(path))
        # Filter maya files
        maya_files = [file for file in files
                      if '.ma' in file or '.mb' in file or '.fbx' in file]

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
    def build_path(self, return_type=4):
        # Get datas from ui
        datas = self.get_am_ui_datas()

        if datas[1] == 'Assets':
            if return_type == 0:
                return_path = '%s/%s/scenes/ASSETS/' % (self.project_path, datas[0])
                return return_path
            elif return_type == 1:
                return_path = '%s/%s/scenes/ASSETS/%s' % (self.project_path, datas[0], datas[2])
                return return_path
            elif return_type == 2:
                return_path = '%s/%s/scenes/ASSETS/%s/%s' % (self.project_path, datas[0], datas[2], datas[4])
                return return_path
            elif return_type == 3:
                return_path = '%s/%s/scenes/ASSETS/%s/%s/%s' % (self.project_path, datas[0], datas[2], datas[4], datas[6])
                return return_path
            else:
                return_path = '%s/%s/scenes/ASSETS/%s/%s/%s/%s' % (self.project_path, datas[0], datas[2], datas[4], datas[6], datas[7])
                return return_path
        else:
            if return_type == 0:
                return_path = '%s/%s/scenes/ANIMATION/' % (self.project_path, datas[0])
                return return_path
            elif return_type == 1:
                return_path = '%s/%s/scenes/ANIMATION/%s' % (self.project_path, datas[0], datas[3])
                return return_path
            elif return_type == 2:
                return_path = '%s/%s/scenes/ANIMATION/%s/%s' % (self.project_path, datas[0], datas[3], datas[5])
                return return_path
            elif return_type == 3:
                return_path = '%s/%s/scenes/ANIMATION/%s/%s/%s' % (self.project_path, datas[0], datas[3], datas[5], datas[6])
                return return_path
            else:
                return_path = '%s/%s/scenes/ANIMATION/%s/%s/%s/%s' % (self.project_path, datas[0], datas[3], datas[5], datas[6], datas[7])
                return return_path



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
            text_index = combobox.findText(selected_text)
            combobox.setCurrentIndex(text_index)
        else:
            combobox.setCurrentIndex(0)

        for i, item in enumerate(items):
            combobox.setItemData(i, item, Qt.ToolTipRole)

        # --- Unblocking signals from ui
        combobox.blockSignals(False)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def update_tabs_comboBox(self):
        # Get datas from ui
        datas = self.get_am_ui_datas()

        if datas[1] == 'Assets':
            self.update_type_combobox()
        else:
            self.update_episode_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_type_combobox(self):
        type_path = self.build_path(0)

        types_list = self.create_subdir_list(type_path)

        # Update comboBox
        self.update_combobox(self.asset_type_comboBox, types_list)

        self.update_asset_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_asset_combobox(self):
        asset_path = self.build_path(1)

        assets_list = self.create_subdir_list(asset_path)

        # Update comboBox
        self.update_combobox(self.asset_comboBox, assets_list)

        self.update_task_comboBox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_episode_combobox(self):
        episode_path = self.build_path(0)

        episodes_list = self.create_subdir_list(episode_path)

        # Update comboBox
        self.update_combobox(self.episode_comboBox, episodes_list)

        self.update_shot_combobox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_shot_combobox(self):
        shot_path = self.build_path(1)

        # Create shots list
        shots_list = self.create_subdir_list(shot_path)

        # Update comboBox
        self.update_combobox(self.shot_comboBox, shots_list)

        # Init update task comboBox
        self.update_task_comboBox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_task_comboBox(self):
        task_path = self.build_path(2)

        # Create task list
        task_list = self.create_subdir_list(task_path)

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
        task_path = self.build_path(3)

        # Get the previous selection
        selected_file = self.files_listWidget.selectedItems()
        if len(selected_file) != 0:
            print 'Previous selected file is ', selected_file[0].text()
        else:
            print "No previous selected file"

        maya_files = self.build_files_list(task_path)

        # Clear and recreate the list
        self.files_listWidget.clear()
        self.files_listWidget.addItems(maya_files)

        # If currently selected text in new item list, select it
        if len(selected_file) != 0 and selected_file[0].text() in maya_files:
            # Get item matching the previously selected name
            item_to_select = self.files_listWidget.findItems(selected_file[0].text(), Qt.MatchExactly)[0]
            # Get its index
            idx = self.files_listWidget.indexFromItem(item_to_select)
            # Select it
            self.files_listWidget.item(idx.row()).setSelected(True)
        else:
            # Else, select item at index 0
            self.files_listWidget.item(0).setSelected(True)

    # ------------------------------------------------------------------------------------------------------------------
    def open_file(self):
        file_path = self.build_path()
        # Open
        mc.file(file_path, o=True, f=True)
        # Verbose
        print file_path.split('/')[-1], ' has been open'

    # ------------------------------------------------------------------------------------------------------------------
    def save_file(self):
        # Get current open file
        open_file = mc.file(q=True, exn=True)

        # Build file path
        file_path = self.build_path()

        # If open file match selected file
        if open_file == file_path:
            # Save
            mc.file(file_path, s=True, f=True)
            # Verbose
            print file_path.split('/')[-1], ' has been saved'
        # If not, pass (for now)
        else:
            pass
