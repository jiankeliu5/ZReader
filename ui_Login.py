# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created: Sun Jul 17 23:54:14 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName(_fromUtf8("Login"))
        Login.resize(331, 216)
        self.verticalLayout = QtGui.QVBoxLayout(Login)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Login)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.emailLineEdit = QtGui.QLineEdit(Login)
        self.emailLineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.emailLineEdit.setObjectName(_fromUtf8("emailLineEdit"))
        self.gridLayout.addWidget(self.emailLineEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Login)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwdLineEdit = QtGui.QLineEdit(Login)
        self.passwdLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwdLineEdit.setObjectName(_fromUtf8("passwdLineEdit"))
        self.gridLayout.addWidget(self.passwdLineEdit, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.checkBox = QtGui.QCheckBox(Login)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exitButton = QtGui.QPushButton(Login)
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.horizontalLayout.addWidget(self.exitButton)
        self.loginButton = QtGui.QPushButton(Login)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.horizontalLayout.addWidget(self.loginButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label.setBuddy(self.emailLineEdit)
        self.label_2.setBuddy(self.passwdLineEdit)

        self.retranslateUi(Login)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Login.close)
        QtCore.QObject.connect(self.passwdLineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.loginButton.click)
        QtCore.QObject.connect(self.emailLineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.loginButton.click)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtGui.QApplication.translate("Login", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Login", "Email:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Login", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Login", "Save Email and Passwd", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("Login", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.loginButton.setText(QtGui.QApplication.translate("Login", "&Login", None, QtGui.QApplication.UnicodeUTF8))

