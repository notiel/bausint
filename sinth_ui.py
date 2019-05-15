import design
from loguru import logger
import sys
from dataclasses import *
from PyQt5 import QtWidgets
import Usbhost
from typing import List
import csv
import datetime

wrong_answers = ['Bad data', "Unknown command", "No device port", 'Port error']
answer_translate = {'Bad data': "Неверные данные", "Unknown command": 'Неизвестная команда',
                    "No device port": "Устройство не подключено", "Port error": "Ошибка порта"}


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
    device: str = ""


class Synthetizer(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = State()
        self.port = None

        self.set_hand_active()
        self.scan_and_select()

        self.command_dict = {self.BtnSetFine: "SetFreqFine", self.BtnDeleteCalTable: "SetCalibrTable",
                             self.BtnSetRough: "SetFreqRough", self.BtnSetDACValue: "SetDACValue",
                             self.BtnStop: "Stop", self.BtnDeleteFreqfile: "ClearFreqTable"}
        self.error_dict = {self.BtnSetFine: "Не удалось задать точную частоту",
                           self.BtnDeleteCalTable: "Не удалось задать калибровочную таблицу",
                           self.BtnSetRough: "Не удалось задать частоту грубо",
                           self.BtnSetDACValue: "Не удалось задать значение ЦАП",
                           self.BtnStop: "Не удалось остановить эксперимент",
                           self.BtnDeleteFreqfile: "Не удалось удалить файл эксперимента"}
        self.result_dict = {self.BtnSetFine: "Точная частота задана", self.BtnDeleteCalTable: "Таблица удалена",
                            self.BtnSetRough: "Частота задана грубо", self.BtnSetDACValue: "Задано значение ЦАП",
                            self.BtnStop: "Эксперимент остановлен", self.BtnDeleteFreqfile: "Файл эксперимента удален"}

        self.BtnRescan.clicked.connect(self.scan_and_select)
        self.BtnChangeDevice.clicked.connect(self.change_device)
        self.BtnChangState.clicked.connect(self.change_state)
        self.BtnSetCalTable.clicked.connect(self.set_cal_table)
        self.BtnDeleteCalTable.clicked.connect(self.send_command)
        self.BtnSetDACValue.clicked.connect(self.send_command)
        self.BtnSetRough.clicked.connect(self.send_command)
        self.BtnSetFine.clicked.connect(self.send_command)
        self.BtnSetTime.clicked.connect(self.set_current_time)
        self.BtnSetFreqFile.clicked.connect(self.set_freq_table)
        self.BtnDeleteFreqfile.clicked.connect(self.send_command)
        self.BtnStop.clicked.connect(self.send_command)

    def scan_and_select(self):
        self.BtnChangeDevice.setEnabled(False)
        self.CBDevices.clear()
        self.port = Usbhost.open_port(Usbhost.get_device_port())
        answer: str = Usbhost.send_query(self.port, "GetAddr")
        if answer in wrong_answers:
            # error_message(answer)
            self.statusbar.showMessage(answer_translate[answer])
        else:
            devices: List[str] = answer.split()
            self.CBDevices.addItems(devices)
            if devices:
                self.BtnChangeDevice.setEnabled(True)
                self.statusbar.clearMessage()
            else:
                self.statusbar.showMessage("Устройства не найдены")

    def change_device(self):
        """
        changes current device to selected
        :return:
        """
        device = self.CBDevices.currentText()
        answer = Usbhost.send_query(self.port, "GetState", device)
        if answer in wrong_answers:
            error_message("Не удалось сменить устройство")
            self.statusbar.showMessage(answer_translate[answer])
        elif answer not in ("0", "1"):
            error_message("Ошибка статуса устройства")
        else:
            self.state.device = device
            self.statusbar.clearMessage()
            self.set_descr_label(self.state.device, int(answer))

    def change_state(self):
        """
        changes state of selected device
        :return:
        """
        new_state = 0 if self.state.state == 1 else 1
        answer = Usbhost.send_query(self.port, "SetState", self.state.device, new_state)
        if answer in wrong_answers:
            error_message("Не удалось сменить состояние")
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.clearMessage()
            self.state.state = new_state
            self.set_descr_label(self.state.device, self.state.state)
            if new_state == 1:
                self.set_auto_active()
            if new_state == 0:
                self.set_hand_active()

    def send_command(self):
        """
        sends command and shows status depending on sender
        :return:
        """
        button = self.sender()
        answer: str = Usbhost.send_command(self.port, self.command_dict[button], self.state.device)
        if answer in wrong_answers:
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.showMessage(self.result_dict[button])

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
                    answer = Usbhost.send_command(self.port, "SetCalibrTableRow", self.state.device, row[0], row[1])
                    if answer in wrong_answers:
                        error_message("Не удалось отправить строку, удаляем калибровочную таблицу")
                        self.BtnDeleteCalTable.click()
                        self.statusbar.showMessage(answer_translate[answer])
                        return
                self.statusbar.showMessage("Калибровочная таблица отправлена")
        else:
            error_message("Файл не выбран или в формате .csv")
            self.statusbar.clearMessage()

    def set_current_time(self):
        """
        sends current timr to selected device
        :return:
        """
        now = datetime.datetime.now()
        answer = Usbhost.send_command(self.port, "SetCurrentTime", self.state.device, now.year, now.month, now.day,
                                      now.hour, now.minute, now.second, int(now.microsecond / 1000))
        if answer in wrong_answers:
            error_message("Не удалось задать время")
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.showMessage("Время задано")

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
                answer = Usbhost.send_command(self.port, "SetStartTime", self.state.device, *start_time)
                if answer in wrong_answers:
                    error_message("Не удалось отправить файл эксперимента")
                    self.statusbar.showMessage(answer_translate[answer])
                else:
                    for row in data[1:]:
                        answer = Usbhost.send_command(self.port, "SetCalibrTableRow", self.state.device, *row)
                        if answer in wrong_answers:
                            error_message("Не удалось отправить строку, удаляем файл эксперимента")
                            self.BtnDeleteFreqfile.click()
                            self.statusbar.showMessage(answer_translate[answer])
                            return
                    self.statusbar.showMessage("Калибровочная таблица отправлена")
        else:
            error_message("Файл не выбран или в формате .csv")
            self.statusbar.clearMessage()

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

    def set_auto_state(self, state: bool):
        """
        sets state status to all objects of auto mode
        :param state: state of objects
        :return:
        """
        self.BtnSetTime.setEnabled(state)
        self.BtnSetFreqFile.setEnabled(state)
        self.BtnDeleteFreqfile.setEnabled(state)
        self.BtnStop.setEnabled(state)

    def set_hand_active(self):
        """
        sets hand mode to ui
        :return:
        """
        self.set_auto_state(False)
        self.set_hand_state(True)

    def set_auto_active(self):
        """
        sets auto mode to ui
        :return:
        """
        self.set_hand_state(False)
        self.set_auto_state(True)

    def set_descr_label(self, addr: str, state: int):
        """
        forms description label
        :param addr: device address
        :param state: 0 for hand and 1 for auto
        :return:
        """
        states = {0: 'ручном', 1: "автоматическом"}
        self.LblDescr.setText("Выбрано устройство %s. Устройство работает в %s режиме." % (addr, states[state]))
        self.LblDescr.setStyleSheet("font-size: 12pt")


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
