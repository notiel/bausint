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
        MainWindow.resize(948, 604)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.BtnConnect = QtWidgets.QPushButton(self.centralwidget)
        self.BtnConnect.setEnabled(False)
        self.BtnConnect.setObjectName("BtnConnect")
        self.gridLayout.addWidget(self.BtnConnect, 1, 2, 1, 1)
        self.CBDevices = QtWidgets.QComboBox(self.centralwidget)
        self.CBDevices.setObjectName("CBDevices")
        self.gridLayout.addWidget(self.CBDevices, 1, 1, 1, 1)
        self.LblList = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.LblList.setFont(font)
        self.LblList.setObjectName("LblList")
        self.gridLayout.addWidget(self.LblList, 1, 0, 1, 1)
        self.BtnRescan = QtWidgets.QPushButton(self.centralwidget)
        self.BtnRescan.setObjectName("BtnRescan")
        self.gridLayout.addWidget(self.BtnRescan, 1, 3, 1, 2)
        self.BtnSyncro = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSyncro.setEnabled(False)
        self.BtnSyncro.setObjectName("BtnSyncro")
        self.gridLayout.addWidget(self.BtnSyncro, 1, 5, 1, 1)
        self.GBState = QtWidgets.QGroupBox(self.centralwidget)
        self.GBState.setEnabled(False)
        self.GBState.setObjectName("GBState")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.GBState)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.LblTime = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblTime.setFont(font)
        self.LblTime.setObjectName("LblTime")
        self.gridLayout_5.addWidget(self.LblTime, 1, 0, 1, 1)
        self.LblState = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblState.setFont(font)
        self.LblState.setObjectName("LblState")
        self.gridLayout_5.addWidget(self.LblState, 0, 0, 1, 1)
        self.LblMove = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblMove.setFont(font)
        self.LblMove.setObjectName("LblMove")
        self.gridLayout_5.addWidget(self.LblMove, 3, 0, 1, 1)
        self.LblFreq = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblFreq.setFont(font)
        self.LblFreq.setObjectName("LblFreq")
        self.gridLayout_5.addWidget(self.LblFreq, 2, 0, 1, 1)
        self.LblRes = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblRes.setFont(font)
        self.LblRes.setObjectName("LblRes")
        self.gridLayout_5.addWidget(self.LblRes, 4, 0, 1, 1)
        self.LblAtt = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblAtt.setFont(font)
        self.LblAtt.setObjectName("LblAtt")
        self.gridLayout_5.addWidget(self.LblAtt, 5, 0, 1, 1)
        self.LblStateVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblStateVal.setFont(font)
        self.LblStateVal.setObjectName("LblStateVal")
        self.gridLayout_5.addWidget(self.LblStateVal, 0, 1, 1, 1)
        self.LblTimeVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblTimeVal.setFont(font)
        self.LblTimeVal.setObjectName("LblTimeVal")
        self.gridLayout_5.addWidget(self.LblTimeVal, 1, 1, 1, 1)
        self.LblFreqVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblFreqVal.setFont(font)
        self.LblFreqVal.setObjectName("LblFreqVal")
        self.gridLayout_5.addWidget(self.LblFreqVal, 2, 1, 1, 1)
        self.LblMoveVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblMoveVal.setFont(font)
        self.LblMoveVal.setObjectName("LblMoveVal")
        self.gridLayout_5.addWidget(self.LblMoveVal, 3, 1, 1, 1)
        self.LblResVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblResVal.setFont(font)
        self.LblResVal.setObjectName("LblResVal")
        self.gridLayout_5.addWidget(self.LblResVal, 4, 1, 1, 1)
        self.LblAttVal = QtWidgets.QLabel(self.GBState)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblAttVal.setFont(font)
        self.LblAttVal.setObjectName("LblAttVal")
        self.gridLayout_5.addWidget(self.LblAttVal, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.GBState, 3, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.BtnSetCalTable = QtWidgets.QPushButton(self.groupBox)
        self.BtnSetCalTable.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnSetCalTable.setFont(font)
        self.BtnSetCalTable.setObjectName("BtnSetCalTable")
        self.gridLayout_4.addWidget(self.BtnSetCalTable, 0, 2, 1, 3)
        self.BtnAttenuate = QtWidgets.QPushButton(self.groupBox)
        self.BtnAttenuate.setEnabled(False)
        self.BtnAttenuate.setObjectName("BtnAttenuate")
        self.gridLayout_4.addWidget(self.BtnAttenuate, 2, 2, 1, 1)
        self.SpinAttenuate = QtWidgets.QSpinBox(self.groupBox)
        self.SpinAttenuate.setEnabled(False)
        self.SpinAttenuate.setMaximum(30)
        self.SpinAttenuate.setProperty("value", 30)
        self.SpinAttenuate.setObjectName("SpinAttenuate")
        self.gridLayout_4.addWidget(self.SpinAttenuate, 2, 3, 1, 1)
        self.LblAttenuate = QtWidgets.QLabel(self.groupBox)
        self.LblAttenuate.setObjectName("LblAttenuate")
        self.gridLayout_4.addWidget(self.LblAttenuate, 2, 4, 1, 1)
        self.BtnL1 = QtWidgets.QPushButton(self.groupBox)
        self.BtnL1.setEnabled(False)
        self.BtnL1.setObjectName("BtnL1")
        self.gridLayout_4.addWidget(self.BtnL1, 0, 0, 1, 1)
        self.LlL3 = QtWidgets.QLabel(self.groupBox)
        self.LlL3.setObjectName("LlL3")
        self.gridLayout_4.addWidget(self.LlL3, 2, 1, 1, 1)
        self.LbLL1 = QtWidgets.QLabel(self.groupBox)
        self.LbLL1.setObjectName("LbLL1")
        self.gridLayout_4.addWidget(self.LbLL1, 0, 1, 1, 1)
        self.BtnL2 = QtWidgets.QPushButton(self.groupBox)
        self.BtnL2.setEnabled(False)
        self.BtnL2.setObjectName("BtnL2")
        self.gridLayout_4.addWidget(self.BtnL2, 1, 0, 1, 1)
        self.BtnL5 = QtWidgets.QPushButton(self.groupBox)
        self.BtnL5.setEnabled(False)
        self.BtnL5.setObjectName("BtnL5")
        self.gridLayout_4.addWidget(self.BtnL5, 2, 0, 1, 1)
        self.LblL2 = QtWidgets.QLabel(self.groupBox)
        self.LblL2.setObjectName("LblL2")
        self.gridLayout_4.addWidget(self.LblL2, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 6)
        self.GBAuto = QtWidgets.QGroupBox(self.centralwidget)
        self.GBAuto.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.GBAuto.setFont(font)
        self.GBAuto.setObjectName("GBAuto")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.GBAuto)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.BtnSetFreqFile = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnSetFreqFile.setFont(font)
        self.BtnSetFreqFile.setObjectName("BtnSetFreqFile")
        self.gridLayout_3.addWidget(self.BtnSetFreqFile, 0, 0, 1, 1)
        self.BtnStop = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnStop.setFont(font)
        self.BtnStop.setStyleSheet("color: red")
        self.BtnStop.setObjectName("BtnStop")
        self.gridLayout_3.addWidget(self.BtnStop, 2, 0, 1, 1)
        self.BtnStart = QtWidgets.QPushButton(self.GBAuto)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnStart.setFont(font)
        self.BtnStart.setStyleSheet("color: green")
        self.BtnStart.setObjectName("BtnStart")
        self.gridLayout_3.addWidget(self.BtnStart, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.GBAuto, 4, 3, 1, 3)
        self.GBReg = QtWidgets.QGroupBox(self.centralwidget)
        self.GBReg.setEnabled(False)
        self.GBReg.setObjectName("GBReg")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.GBReg)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.LblDac = QtWidgets.QLabel(self.GBReg)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblDac.setFont(font)
        self.LblDac.setObjectName("LblDac")
        self.gridLayout_6.addWidget(self.LblDac, 0, 0, 1, 1)
        self.LblDacVal = QtWidgets.QLabel(self.GBReg)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LblDacVal.setFont(font)
        self.LblDacVal.setObjectName("LblDacVal")
        self.gridLayout_6.addWidget(self.LblDacVal, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.GBReg, 3, 3, 1, 3)
        self.GBHand = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.GBHand.setFont(font)
        self.GBHand.setObjectName("GBHand")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GBHand)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BtnSetRough = QtWidgets.QPushButton(self.GBHand)
        self.BtnSetRough.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnSetRough.setFont(font)
        self.BtnSetRough.setObjectName("BtnSetRough")
        self.gridLayout_2.addWidget(self.BtnSetRough, 0, 0, 1, 1)
        self.LblHz = QtWidgets.QLabel(self.GBHand)
        self.LblHz.setEnabled(False)
        self.LblHz.setText("")
        self.LblHz.setObjectName("LblHz")
        self.gridLayout_2.addWidget(self.LblHz, 0, 3, 1, 1)
        self.SpinRough = QtWidgets.QSpinBox(self.GBHand)
        self.SpinRough.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SpinRough.setFont(font)
        self.SpinRough.setMinimum(-150000)
        self.SpinRough.setMaximum(150000)
        self.SpinRough.setSingleStep(500)
        self.SpinRough.setObjectName("SpinRough")
        self.gridLayout_2.addWidget(self.SpinRough, 0, 1, 1, 1)
        self.BtnSetDACValue = QtWidgets.QPushButton(self.GBHand)
        self.BtnSetDACValue.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnSetDACValue.setFont(font)
        self.BtnSetDACValue.setObjectName("BtnSetDACValue")
        self.gridLayout_2.addWidget(self.BtnSetDACValue, 3, 0, 1, 1)
        self.SpinDACValue = QtWidgets.QSpinBox(self.GBHand)
        self.SpinDACValue.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SpinDACValue.setFont(font)
        self.SpinDACValue.setMaximum(65535)
        self.SpinDACValue.setObjectName("SpinDACValue")
        self.gridLayout_2.addWidget(self.SpinDACValue, 3, 1, 1, 1)
        self.BtnSetFine = QtWidgets.QPushButton(self.GBHand)
        self.BtnSetFine.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnSetFine.setFont(font)
        self.BtnSetFine.setObjectName("BtnSetFine")
        self.gridLayout_2.addWidget(self.BtnSetFine, 2, 0, 1, 1)
        self.LblKHz = QtWidgets.QLabel(self.GBHand)
        self.LblKHz.setEnabled(False)
        self.LblKHz.setObjectName("LblKHz")
        self.gridLayout_2.addWidget(self.LblKHz, 0, 2, 1, 1)
        self.LblMoveHz = QtWidgets.QLabel(self.GBHand)
        self.LblMoveHz.setEnabled(False)
        self.LblMoveHz.setObjectName("LblMoveHz")
        self.gridLayout_2.addWidget(self.LblMoveHz, 2, 2, 1, 1)
        self.SpinFine = QtWidgets.QSpinBox(self.GBHand)
        self.SpinFine.setEnabled(False)
        self.SpinFine.setMinimum(-3500)
        self.SpinFine.setMaximum(3500)
        self.SpinFine.setObjectName("SpinFine")
        self.gridLayout_2.addWidget(self.SpinFine, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.GBHand, 4, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 948, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Частотный преобразователь - Converter75"))
        self.BtnConnect.setText(_translate("MainWindow", "Подключить"))
        self.LblList.setText(_translate("MainWindow", "Список устройств:"))
        self.BtnRescan.setText(_translate("MainWindow", "Повторный поиск"))
        self.BtnSyncro.setText(_translate("MainWindow", "Синхронизировать"))
        self.GBState.setTitle(_translate("MainWindow", "Текущее состояние"))
        self.LblTime.setText(_translate("MainWindow", "Время:"))
        self.LblState.setText(_translate("MainWindow", "Режим:"))
        self.LblMove.setText(_translate("MainWindow", "Сдвиг по частоте: "))
        self.LblFreq.setText(_translate("MainWindow", "Диапазон частот: "))
        self.LblRes.setText(_translate("MainWindow", "Выходная частота:"))
        self.LblAtt.setText(_translate("MainWindow", "Ослабление:"))
        self.LblStateVal.setText(_translate("MainWindow", "Ручной"))
        self.LblTimeVal.setText(_translate("MainWindow", "00:00:00"))
        self.LblFreqVal.setText(_translate("MainWindow", "-"))
        self.LblMoveVal.setText(_translate("MainWindow", "0 Гц"))
        self.LblResVal.setText(_translate("MainWindow", "Неизвестно"))
        self.LblAttVal.setText(_translate("MainWindow", "Неизвестно"))
        self.groupBox.setTitle(_translate("MainWindow", "Выбор частотного диапазона"))
        self.BtnSetCalTable.setText(_translate("MainWindow", "Задать калибровочную таблицу"))
        self.BtnAttenuate.setText(_translate("MainWindow", "Ослабить выходной сигнал"))
        self.LblAttenuate.setText(_translate("MainWindow", "дБ"))
        self.BtnL1.setText(_translate("MainWindow", "L1"))
        self.LlL3.setText(_translate("MainWindow", "1176,45 МГц"))
        self.LbLL1.setText(_translate("MainWindow", "1575,42 МГц"))
        self.BtnL2.setText(_translate("MainWindow", "L2"))
        self.BtnL5.setText(_translate("MainWindow", "L5"))
        self.LblL2.setText(_translate("MainWindow", "1227,60 МГц"))
        self.GBAuto.setTitle(_translate("MainWindow", "Автоматический режим"))
        self.BtnSetFreqFile.setText(_translate("MainWindow", "Задать файл эксперимента"))
        self.BtnStop.setText(_translate("MainWindow", "Остановить эксперимент"))
        self.BtnStart.setText(_translate("MainWindow", "Начать эксперимент"))
        self.GBReg.setTitle(_translate("MainWindow", "Значения регистров"))
        self.LblDac.setText(_translate("MainWindow", "Значение ЦАП:"))
        self.LblDacVal.setText(_translate("MainWindow", "Неизвестно"))
        self.GBHand.setTitle(_translate("MainWindow", "Ручное управление"))
        self.BtnSetRough.setText(_translate("MainWindow", "Задать сдвиг грубо"))
        self.BtnSetDACValue.setText(_translate("MainWindow", "Задать значение ЦАП"))
        self.BtnSetFine.setText(_translate("MainWindow", "Задать сдвиг точно"))
        self.LblKHz.setText(_translate("MainWindow", "Гц"))
        self.LblMoveHz.setText(_translate("MainWindow", "Гц"))

