import design
import sys
from dataclasses import *
from PyQt5 import QtWidgets, QtCore
from Usbhost import UsbHost
from typing import Dict
import csv
import datetime
from loguru import logger

wrong_answers = ['Bad data', "Unknown command", "No device port", 'Port error']
answer_translate = {'Bad data': "Неверные данные", "Unknown command": 'Неизвестная команда',
                    "No device port": "Устройство не подключено", "Port error": "Ошибка порта"}

logger.start("logfile.log", rotation="1 week", format="{time} {level} {message}", level="DEBUG", enqueue=True)


def initiate_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)
    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


@dataclass
class State:
    state: int = 0
    device_id: int = -1
    comport: str = ""
    ser = None
    message = "Частотный преобразователь не подключен"


class Synthetizer(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = State()
        self.devices: Dict[int, str] = dict()
        self.UsbHost = UsbHost()

        # self.set_hand_active()
        self.statusbar.showMessage("Частотный преобразователь не подключен")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.command_dict = {self.BtnSetFine: "SetFreqFine", self.BtnDeleteCalTable: "SetCalibrTable",
                             self.BtnSetRough: "SetFreqRough", self.BtnSetDACValue: "SetDac",
                             self.BtnStop: "Stop", self.BtnL1: 'SyntL1', self.BtnL2: 'SyntL2', self.BtnL5: 'SyntL5',
                             self.BtnAttenuate: "SetAtt", self.BtnStart: "Start"}
        self.error_dict = {self.BtnSetFine: "Не удалось задать сдвиг точно",
                           self.BtnDeleteCalTable: "Не удалось удалить калибровочную таблицу",
                           self.BtnSetRough: "Не удалось задать сдвиг грубо",
                           self.BtnSetDACValue: "Не удалось задать значение ЦАП",
                           self.BtnStop: "Не удалось остановить эксперимент",
                           self.BtnStop: "Не удалось начать эксперимент",
                           self.BtnL1: 'Не удалось задать частотный диапазон',
                           self.BtnL2: 'Не удалось задать частотный диапазон',
                           self.BtnL5: 'Не удалось задать частотный диапазон',
                           self.BtnAttenuate: "Не удалось задать ослабленние выходного сигнала"}
        self.result_dict = {self.BtnSetFine: "Точная частота задана", self.BtnDeleteCalTable: "Таблица удалена",
                            self.BtnSetRough: "Частота задана грубо", self.BtnSetDACValue: "Задано значение ЦАП",
                            self.BtnStop: "Эксперимент остановлен", self.BtnL1: 'Выбран диапазон L1',
                            self.BtnL2: 'Выбран диапазон L2', self.BtnL5: 'Выбран диапазон L5',
                            self.BtnAttenuate: "Задано ослабление выходного сигнала"}

        self.spins = {self.BtnAttenuate: self.SpinAttenuate, self.BtnSetRough: self.SpinRough,
                      self.BtnSetFine: self.SpinFine, self.BtnSetDACValue: self.SpinDACValue}

        self.val_labels = {self.BtnAttenuate: self.LblAttVal, self.BtnSetRough: self.LblMoveVal,
                           self.BtnSetDACValue: self.LblDacVal, self.BtnSetFine: None}

        self.val_dimensions = {self.BtnAttenuate: " дБ", self.BtnSetRough: " Гц",
                           self.BtnSetDACValue: " Гц", self.BtnSetFine: None}

        self.controls = [self.BtnConnect, self.BtnSyncro, self.BtnL1, self.BtnL2, self.BtnL5, self.BtnSetCalTable,
                         self.BtnDeleteCalTable, self.BtnAttenuate, self.SpinAttenuate, self.GBState, self.GBReg,
                         self.GBHand, self.BtnSetDACValue, self.SpinDACValue, self.BtnSetRough, self.SpinRough,
                         self.BtnSetFine, self.SpinFine, self.GBAuto, self.BtnSetFreqFile, self.BtnStart, self.BtnStop]

        self.BtnRescan.clicked.connect(self.scan_and_select)
        self.BtnConnect.clicked.connect(self.change_device)
        self.BtnSyncro.clicked.connect(self.set_current_time)
        self.BtnL1.clicked.connect(self.send_command)
        self.BtnL2.clicked.connect(self.send_command)
        self.BtnL5.clicked.connect(self.send_command)
        self.BtnSetDACValue.clicked.connect(self.send_command_with_parameter)
        self.BtnSetRough.clicked.connect(self.send_command_with_parameter)
        self.BtnAttenuate.clicked.connect(self.send_command_with_parameter)

        self.BtnSetFine.clicked.connect(self.send_command)
        self.BtnSetCalTable.clicked.connect(self.set_cal_table)
        self.BtnDeleteCalTable.clicked.connect(self.send_command)
        self.BtnSetFreqFile.clicked.connect(self.set_freq_table)
        self.BtnStop.clicked.connect(self.send_command)

        self.scan_and_select()

    def scan_and_select(self):
        self.set_controls_state(False)
        if self.state.ser:
            UsbHost.close_port(self.state.ser)
        self.state.message = "Частотный преобразователь не подключен"
        self.statusbar.showMessage(self.state.message)
        self.BtnConnect.setEnabled(False)
        self.CBDevices.clear()
        self.devices = UsbHost.get_all_device_ports_with_id()
        self.CBDevices.addItems([str(x) for x in self.devices.keys()])
        if self.devices.keys():
            self.BtnConnect.setEnabled(True)
            self.statusbar.clearMessage()
        else:
            self.statusbar.showMessage("Устройства не найдены")

    def timerEvent(self):
        """
        changes timers
        :return:
        """
        if self.GBState.isEnabled():
            now = datetime.datetime.now()
            self.LblTimeVal.setText("%02.i:%02.i:%02.i" % (now.hour, now.minute, now.second))
        self.statusbar.showMessage(self.state.message)

    def set_controls_state(self, state: bool):
        """
        activates or desactivates all controls
        :param state: state of activaation
        :return:
        """
        for control in self.controls:
            control.setEnabled(state)
        self.LblDacVal.setText("Неизвестно")
        self.LblFreqVal.setText("L1")
        self.LblStateVal.setText("Ручной")
        self.LblMoveVal.setText("Гц")
        self.LblResVal.setText("МГц")
        self.LblAttVal.setText("дБ")

    def send_command(self):
        """
        sends command and shows status depending on sender
        :return:
        """
        button = self.sender()
        answer: str = self.UsbHost.send_command(self.state.ser, self.command_dict[button], str(self.state.device_id))
        if answer in wrong_answers:
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.showMessage(self.result_dict[button])
            if button in [self.BtnL1, self.BtnL2, self.BtnL5]:
                self.LblFreqVal.setText(button.text())

    def send_command_with_parameter(self):
        """
        sends command with parameter and shows status depending on sender
        :return:
        """
        button = self.sender()
        spin = self.spins[button]
        answer: str = self.UsbHost.send_command(self.state.ser, self.command_dict[button],
                                                str(self.state.device_id), spin.value())
        if answer in wrong_answers:
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.showMessage(self.result_dict[button])
        if self.val_labels[button]:
            self.val_labels[button].setText(str(spin.value()) + self.val_dimensions[button])

    def change_device(self):
        """
        changes current device to selected
        :return:
.        """
        if self.state.ser:
            UsbHost.close_port(self.state.ser)
        device = self.CBDevices.currentText()
        if device:
            comport = self.devices[int(device)]
            self.state.ser = UsbHost.open_port(comport)
            if not self.state.ser:
                self.statusbar.showMessage("Выбранный порт более недоступен. Произведите повторный поиск")
                return
            answer: str = self.UsbHost.send_command(self.state.ser, "ping", device)
            if answer in wrong_answers:
                error_message("Выбранный девайс не отвечает")
                self.statusbar.showMessage("Выбранный порт более недоступен. Произведите повторный поиск")
                return
            self.state.device_id = int(device)
            self.state.comport = comport
            self.state.message = "Подключен частотный преобразователь %i через %s порт. Время не синхронизировано" \
                                 % (int(device), comport)
            self.statusbar.showMessage(self.state.message)
            self.set_controls_state(True)
            self.BtnAttenuate.click()

    # refactor
    def change_state(self):
        """
        changes state of selected device
        :return:
        """
        new_state = 0 if self.state.state == 1 else 1
        answer = UsbHost.send_query(self.state.ser, "SetState", str(self.state.device_id), new_state)
        if answer in wrong_answers:
            error_message("Не удалось сменить состояние")
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.clearMessage()
            self.state.state = new_state
            if new_state == 1:
                self.set_auto_active()
            if new_state == 0:
                self.set_hand_active()

    # refactor
    def set_cal_table(self):
        """
        sends calibration table row by row
        :return:
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '.')[0]
        if filename and filename.lower().endswith('.csv'):
            with open(filename) as f:
                data = csv.reader(f, encoding='uft-8', delimiter=',')
                for row in data:
                    answer = UsbHost.send_command(self.state.ser, "SetCalibrTableRow",
                                                  str(self.state.device_id), row[0], row[1])
                    if answer in wrong_answers:
                        error_message("Не удалось отправить строку, удаляем калибровочную таблицу")
                        self.BtnDeleteCalTable.click()
                        self.statusbar.showMessage(answer_translate[answer])
                        return
                self.statusbar.showMessage("Калибровочная таблица отправлена")
        else:
            error_message("Файл не выбран или в формате .csv")
            self.statusbar.clearMessage()

    # refactor
    def set_current_time(self):
        """
        sends current timr to selected device
        :return:
        """
        now = datetime.datetime.now()
        answer = self.UsbHost.send_command(self.state.ser, "SetCurrentTime", str(self.state.device_id),
                                           now.year, now.month, now.day,
                                           now.hour, now.minute, now.second, int(now.microsecond / 1000))
        if answer in wrong_answers:
            error_message("Не удалось задать время")
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.state.message = self.state.message.split('.')[-1] + ". Время синхронизировано"
            self.statusbar.showMessage(self.state.message)

    # refactor
    def set_freq_table(self):
        """
        sends calibration table row by row
        :return:
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '.')[0]
        if filename and filename.lower().endswith('.csv'):
            with open(filename) as f:
                data = csv.reader(f, encoding='uft-8', delimiter=',')
                start_time = data[0]
                answer = UsbHost.send_command(self.state.ser, "SetStartTime", str(self.state.device_id), *start_time)
                if answer in wrong_answers:
                    error_message("Не удалось отправить файл эксперимента")
                    self.statusbar.showMessage(answer_translate[answer])
                else:
                    for row in data[1:]:
                        answer = UsbHost.send_command(self.state.ser, "SetCalibrTableRow", str(self.state.device_id),
                                                      *row)
                        if answer in wrong_answers:
                            error_message("Не удалось отправить строку, удаляем файл эксперимента")
                            self.BtnDeleteFreqfile.click()
                            self.statusbar.showMessage(answer_translate[answer])
                            return
                    self.statusbar.showMessage("Калибровочная таблица отправлена")
        else:
            error_message("Файл не выбран или в формате .csv")
            self.statusbar.clearMessage()

    # refactor
    def set_hand_state(self, state: bool):
        """
        sets state status to all objects of hand mode
        :param state: state of objects
        :return:
        """
        self.BtnSetCalTable.setEnabled(state)
        self.BtnDeleteCalTable.setEnabled(state)
        self.BtnSetDACValue.setEnabled(state)
        self.BtnSetFine.setEnabled(state)
        self.BtnSetRough.setEnabled(state)
        self.SpinDACValue.setEnabled(state)
        self.SpinFine.setEnabled(state)
        self.SpinRough.setEnabled(state)

    # refactor
    def set_auto_state(self, state: bool):
        """
        sets state status to all objects of auto mode
        :param state: state of objects
        :return:
        """
        self.BtnSetFreqFile.setEnabled(state)
        self.BtnStop.setEnabled(state)
        self.BtnStart.setEnabled(state)

    # refactor
    def set_hand_active(self):
        """
        sets hand mode to ui
        :return:
        """
        self.set_auto_state(False)
        self.set_hand_state(True)

    # refactor
    def set_auto_active(self):
        """
        sets auto mode to ui
        :return:
        """
        self.set_hand_state(False)
        self.set_auto_state(True)


def error_message(text):
    """
    shows error window with text
    :param text: error text
    :return:
    """
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Ошибка!')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Synthetizer()  # Создаём объект класса
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
