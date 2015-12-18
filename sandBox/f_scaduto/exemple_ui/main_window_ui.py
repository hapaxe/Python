# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\f.scaduto\Desktop\ui\test_toto_untitled_trop_frais_ta_vu.ui'
#
# Created: Thu May 21 13:40:41 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(483, 416)
        DockWidget.setMinimumSize(QtCore.QSize(150, 173))
        DockWidget.setMaximumSize(QtCore.QSize(483, 416))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(self.dockWidgetContents)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget(self.groupBox)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QtGui.QApplication.translate("DockWidget", "DockWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DockWidget", "-- Titre --", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("DockWidget", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("DockWidget", "radi", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("DockWidget", "rado", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("DockWidget", "RUN", None, QtGui.QApplication.UnicodeUTF8))

