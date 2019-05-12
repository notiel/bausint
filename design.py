# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(729, 355)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.LblDescr = QtWidgets.QLabel(self.centralwidget)
        self.LblDescr.setObjectName("LblDescr")
        self.gridLayout.addWidget(self.LblDescr, 1, 0, 1, 6)
        self.LblList = QtWidgets.QLabel(self.centralwidget)
        self.LblList.setObjectName("LblList")
        self.gridLayout.addWidget(self.LblList, 2, 0, 1, 1)
        self.BtnRescan = QtWidgets.QPushButton(self.centralwidget)
        self.BtnRescan.setObjectName("BtnRescan")
        self.gridLayout.addWidget(self.BtnRescan, 2, 3, 1, 2)
        self.BtnChangState = QtWidgets.QPushButton(self.centralwidget)
        self.BtnChangState.setObjectName("BtnChangState")
        self.gridLayout.addWidget(self.BtnChangState, 2, 5, 1, 1)
        self.CBDevices = QtWidgets.QComboBox(self.centralwidget)
        self.CBDevices.setObjectName("CBDevices")
        self.gridLayout.addWidget(self.CBDevices, 2, 1, 1, 1)
        self.BtnChangeDevice = QtWidgets.QPushButton(self.centralwidget)
        self.BtnChangeDevice.setEnabled(False)
        self.BtnChangeDevice.setObjectName("BtnChangeDevice")
        self.gridLayout.addWidget(self.BtnChangeDevice, 2, 2, 1, 1)
        self.GBAuto = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.GBAuto.setFont(font)
        self.GBAuto.setObjectName("GBAuto")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.GBAuto)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.BtnStop = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnStop.setFont(font)
        self.BtnStop.setObjectName("BtnStop")
        self.gridLayout_3.addWidget(self.BtnStop, 3, 0, 1, 1)
        self.BtnSetFreqFile = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetFreqFile.setFont(font)
        self.BtnSetFreqFile.setObjectName("BtnSetFreqFile")
        self.gridLayout_3.addWidget(self.BtnSetFreqFile, 1, 0, 1, 1)
        self.BtnSetTime = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetTime.setFont(font)
        self.BtnSetTime.setObjectName("BtnSetTime")
        self.gridLayout_3.addWidget(self.BtnSetTime, 0, 0, 1, 1)
        self.BtnDeleteFreqfile = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnDeleteFreqfile.setFont(font)
        self.BtnDeleteFreqfile.setObjectName("BtnDeleteFreqfile")
        self.gridLayout_3.addWidget(self.BtnDeleteFreqfile, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.GBAuto, 3, 3, 1, 3)
        self.GBHand = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.GBHand.setFont(font)
        self.GBHand.setObjectName("GBHand")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GBHand)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BtnSetCalTable = QtWidgets.QPushButton(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetCalTable.setFont(font)
        self.BtnSetCalTable.setObjectName("BtnSetCalTable")
        self.gridLayout_2.addWidget(self.BtnSetCalTable, 0, 0, 1, 2)
        self.BtnDeleteCalTable = QtWidgets.QPushButton(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnDeleteCalTable.setFont(font)
        self.BtnDeleteCalTable.setObjectName("BtnDeleteCalTable")
        self.gridLayout_2.addWidget(self.BtnDeleteCalTable, 0, 2, 1, 1)
        self.SpinDACValue = QtWidgets.QSpinBox(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SpinDACValue.setFont(font)
        self.SpinDACValue.setObjectName("SpinDACValue")
        self.gridLayout_2.addWidget(self.SpinDACValue, 1, 2, 1, 1)
        self.SpinRough = QtWidgets.QSpinBox(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SpinRough.setFont(font)
        self.SpinRough.setObjectName("SpinRough")
        self.gridLayout_2.addWidget(self.SpinRough, 2, 2, 1, 1)
        self.SpinFine = QtWidgets.QSpinBox(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SpinFine.setFont(font)
        self.SpinFine.setObjectName("SpinFine")
        self.gridLayout_2.addWidget(self.SpinFine, 3, 2, 1, 1)
        self.BtnSetDACValue = QtWidgets.QPushButton(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetDACValue.setFont(font)
        self.BtnSetDACValue.setObjectName("BtnSetDACValue")
        self.gridLayout_2.addWidget(self.BtnSetDACValue, 1, 0, 1, 2)
        self.BtnSetRough = QtWidgets.QPushButton(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetRough.setFont(font)
        self.BtnSetRough.setObjectName("BtnSetRough")
        self.gridLayout_2.addWidget(self.BtnSetRough, 2, 0, 1, 2)
        self.BtnSetFine = QtWidgets.QPushButton(self.GBHand)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.BtnSetFine.setFont(font)
        self.BtnSetFine.setObjectName("BtnSetFine")
        self.gridLayout_2.addWidget(self.BtnSetFine, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.GBHand, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 729, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Синтезатор частот"))
        self.LblDescr.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Выбрано устройство 1. Устройство работает в режиме ручного управления. </span></p></body></html>"))
        self.LblList.setText(_translate("MainWindow", "Список устройств:"))
        self.BtnRescan.setText(_translate("MainWindow", "Повторный поиск"))
        self.BtnChangState.setText(_translate("MainWindow", "Сменить режим"))
        self.BtnChangeDevice.setText(_translate("MainWindow", "Сменить устройство"))
        self.GBAuto.setTitle(_translate("MainWindow", "Автоматический режим"))
        self.BtnStop.setText(_translate("MainWindow", "Остановить эксперимент"))
        self.BtnSetFreqFile.setText(_translate("MainWindow", "Задать файл эксперимента"))
        self.BtnSetTime.setText(_translate("MainWindow", "Задать точное время"))
        self.BtnDeleteFreqfile.setText(_translate("MainWindow", "Удалить файл эксперимента"))
        self.GBHand.setTitle(_translate("MainWindow", "Ручное управление"))
        self.BtnSetCalTable.setText(_translate("MainWindow", "Задать калибровочную таблицу"))
        self.BtnDeleteCalTable.setText(_translate("MainWindow", "Удалить"))
        self.BtnSetDACValue.setText(_translate("MainWindow", "Задать напряжение ЦАП"))
        self.BtnSetRough.setText(_translate("MainWindow", "Задать частоту грубо"))
        self.BtnSetFine.setText(_translate("MainWindow", "Задать частоту точно"))

