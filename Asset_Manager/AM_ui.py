# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\development\Ui\Asset_Manager\Asset_Manager.ui'
#
# Created: Mon Apr 25 18:29:35 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Asset_Manager_MainWindow(object):
    def setupUi(self, Asset_Manager_MainWindow):
        Asset_Manager_MainWindow.setObjectName("Asset_Manager_MainWindow")
        Asset_Manager_MainWindow.setWindowModality(QtCore.Qt.NonModal)
        Asset_Manager_MainWindow.resize(280, 492)
        Asset_Manager_MainWindow.setMinimumSize(QtCore.QSize(280, 0))
        Asset_Manager_MainWindow.setMaximumSize(QtCore.QSize(360, 1000))
        Asset_Manager_MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Asset_Manager_MainWindow.setAcceptDrops(False)
        Asset_Manager_MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        Asset_Manager_MainWindow.setDocumentMode(False)
        Asset_Manager_MainWindow.setDockNestingEnabled(True)
        Asset_Manager_MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        Asset_Manager_MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(Asset_Manager_MainWindow)
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setAcceptDrops(False)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(260, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(342, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.files_listWidget = QtGui.QListWidget(self.groupBox)
        self.files_listWidget.setMinimumSize(QtCore.QSize(0, 150))
        self.files_listWidget.setObjectName("files_listWidget")
        self.gridLayout.addWidget(self.files_listWidget, 1, 0, 1, 3)
        self.save_pushButton = QtGui.QPushButton(self.groupBox)
        self.save_pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.save_pushButton.setObjectName("save_pushButton")
        self.gridLayout.addWidget(self.save_pushButton, 2, 0, 1, 1)
        self.wip_pushButton = QtGui.QPushButton(self.groupBox)
        self.wip_pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.wip_pushButton.setObjectName("wip_pushButton")
        self.gridLayout.addWidget(self.wip_pushButton, 2, 1, 1, 1)
        self.publish_pushButton = QtGui.QPushButton(self.groupBox)
        self.publish_pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.publish_pushButton.setObjectName("publish_pushButton")
        self.gridLayout.addWidget(self.publish_pushButton, 2, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(115, 35))
        self.label.setMaximumSize(QtCore.QSize(155, 16777215))
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(115, 35))
        self.label_2.setMaximumSize(QtCore.QSize(155, 16777215))
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.asset_shot_label = QtGui.QLabel(self.groupBox)
        self.asset_shot_label.setMinimumSize(QtCore.QSize(115, 35))
        self.asset_shot_label.setMaximumSize(QtCore.QSize(155, 16777215))
        self.asset_shot_label.setObjectName("asset_shot_label")
        self.verticalLayout_3.addWidget(self.asset_shot_label)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMinimumSize(QtCore.QSize(115, 35))
        self.label_3.setMaximumSize(QtCore.QSize(155, 16777215))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.open_pushButton = QtGui.QPushButton(self.groupBox)
        self.open_pushButton.setMinimumSize(QtCore.QSize(115, 35))
        self.open_pushButton.setMaximumSize(QtCore.QSize(155, 16777215))
        self.open_pushButton.setObjectName("open_pushButton")
        self.verticalLayout_3.addWidget(self.open_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.project_comboBox = QtGui.QComboBox(self.groupBox)
        self.project_comboBox.setMinimumSize(QtCore.QSize(115, 35))
        self.project_comboBox.setMaximumSize(QtCore.QSize(155, 16777215))
        self.project_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.project_comboBox.setFrame(True)
        self.project_comboBox.setObjectName("project_comboBox")
        self.verticalLayout_2.addWidget(self.project_comboBox)
        self.asset_animation_comboBox = QtGui.QComboBox(self.groupBox)
        self.asset_animation_comboBox.setMinimumSize(QtCore.QSize(115, 35))
        self.asset_animation_comboBox.setMaximumSize(QtCore.QSize(155, 16777215))
        self.asset_animation_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.asset_animation_comboBox.setFrame(True)
        self.asset_animation_comboBox.setObjectName("asset_animation_comboBox")
        self.verticalLayout_2.addWidget(self.asset_animation_comboBox)
        self.scene_comboBox = QtGui.QComboBox(self.groupBox)
        self.scene_comboBox.setMinimumSize(QtCore.QSize(115, 35))
        self.scene_comboBox.setMaximumSize(QtCore.QSize(155, 16777215))
        self.scene_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.scene_comboBox.setFrame(True)
        self.scene_comboBox.setObjectName("scene_comboBox")
        self.verticalLayout_2.addWidget(self.scene_comboBox)
        self.task_comboBox = QtGui.QComboBox(self.groupBox)
        self.task_comboBox.setMinimumSize(QtCore.QSize(115, 35))
        self.task_comboBox.setMaximumSize(QtCore.QSize(155, 16777215))
        self.task_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.task_comboBox.setFrame(True)
        self.task_comboBox.setObjectName("task_comboBox")
        self.verticalLayout_2.addWidget(self.task_comboBox)
        self.open_publish_pushButton = QtGui.QPushButton(self.groupBox)
        self.open_publish_pushButton.setMinimumSize(QtCore.QSize(115, 35))
        self.open_publish_pushButton.setMaximumSize(QtCore.QSize(155, 16777215))
        self.open_publish_pushButton.setObjectName("open_publish_pushButton")
        self.verticalLayout_2.addWidget(self.open_publish_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 3)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        Asset_Manager_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Asset_Manager_MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        Asset_Manager_MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(Asset_Manager_MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 280, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFiles = QtGui.QMenu(self.menuBar)
        self.menuFiles.setObjectName("menuFiles")
        Asset_Manager_MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(Asset_Manager_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Asset_Manager_MainWindow)

    def retranslateUi(self, Asset_Manager_MainWindow):
        Asset_Manager_MainWindow.setWindowTitle(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Asset Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Asset Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.save_pushButton.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.wip_pushButton.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "WIP", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_pushButton.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Publish", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Asset/Animation", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_shot_label.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.open_pushButton.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.open_publish_pushButton.setText(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Open Publish", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFiles.setTitle(QtGui.QApplication.translate("Asset_Manager_MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
