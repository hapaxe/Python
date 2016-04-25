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

        # declaring projects directory path
        self.project_path = 'D:/BOULOT/TRAVAUX_PERSO/MAYA PROJECTS'
        # declaring asset/anim list
        self.asset_anim_list = ['ASSETS', 'ANIMATION']

        # populating menus
        project_list = self.create_subdir_list(self.project_path)
        self.update_combobox(self.project_comboBox, project_list)
        self.update_combobox(self.asset_animation_comboBox, self.asset_anim_list)
        self.update_scene_comboBox()
        self.update_task_comboBox()
        self.update_files_list()

        # connecting buttons
        self.project_comboBox.currentIndexChanged.connect(self.update_scene_comboBox)
        self.asset_animation_comboBox.currentIndexChanged.connect(self.update_scene_comboBox)
        self.scene_comboBox.currentIndexChanged.connect(self.update_task_comboBox)
        self.task_comboBox.currentIndexChanged.connect(self.update_files_list)

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
    def update_combobox(self, combobox, items):
        """
        Update the given combobox
        :param combobox: combobox to update,  ie: self.bs_node_menu
        :param items: list of items to add to the given combobox
        """
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

    # ------------------------------------------------------------------------------------------------------------------
    def update_scene_comboBox(self):
        asset_anim = self.asset_animation_comboBox.currentText()

        if asset_anim == 'ASSETS':
            self.asset_shot_label.setText('Asset')
        else:
            self.asset_shot_label.setText('Shot')

        asset_anim_path = '%s/%s/scenes/%s/' % (self.project_path, self.project_comboBox.currentText(), asset_anim)

        assets_shots_list = self.create_subdir_list(asset_anim_path)

        self.update_combobox(self.scene_comboBox, assets_shots_list)

        self.update_task_comboBox()

    # ------------------------------------------------------------------------------------------------------------------
    def update_task_comboBox(self):
        asset_path = '%s/%s/scenes/%s/%s/' % (self.project_path,
                                              self.project_comboBox.currentText(),
                                              self.asset_animation_comboBox.currentText(),
                                              self.scene_comboBox.currentText())

        asset_task_list = self.create_subdir_list(asset_path)

        self.update_combobox(self.task_comboBox, asset_task_list)

        self.update_files_list()

    # ------------------------------------------------------------------------------------------------------------------
    def update_files_list(self):
        """
        Update the targets qlistwidget
        :param selected_bs_targets : currently selected target in bs_node_menu combobox
        """

        path = '%s/%s/scenes/%s/%s/%s' % (self.project_path,
                                          self.project_comboBox.currentText(),
                                          self.asset_animation_comboBox.currentText(),
                                          self.scene_comboBox.currentText(),
                                          self.task_comboBox.currentText())
        # Get the previous selection
        selected_files = self.files_listWidget.selectedItems()
        selected_files_list = list()
        for item in selected_files:
            selected_files_list.append(item.text())

        # list the files in the folder
        os.chdir(path)
        files = filter(os.path.isfile, os.listdir(path))
        maya_files = [file for file in files
                      if '.ma' in file
                      or '.mb' in file
                      or '.fbx' in file]

        # sort them
        maya_files.sort(key=lambda x: os.path.getmtime(x))
        maya_files.reverse()

        # clear and recreate the list
        self.files_listWidget.clear()
        self.files_listWidget.addItems(maya_files)

        # --- If currently selected text in new item list, select it
        for text in selected_files_list:
            if text in maya_files:
                items = self.files_listWidget.findItems(text, Qt.MatchExactly)
                for item in items:
                    idx = self.files_listWidget.indexFromItem(item)
                    # index = self.bs_targets_list.row(item)
                    self.files_listWidget.item(idx.row()).setSelected(True)
