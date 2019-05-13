import design
from loguru import logger
import sys
from dataclasses import *
from PyQt5 import QtWidgets
import Usbhost
from typing import List

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

        self.BtnRescan.clicked.connect(self.scan_and_select)
        self.BtnChangeDevice.clicked.connect(self.change_device)
        self.BtnChangState.clicked.connect(self.change_state)
        self.BtnDeleteCalTable.clicked.connect(self.clear_cal_table)
        self.BtnSetDACValue.clicked.connect(self.set_dac_valur)

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

    def clear_cal_table(self):
        """
        clears table device
        :return:
        """
        answer: str = Usbhost.send_command(self.port, "ClearCalibrTable", self.state.device)
        if answer in wrong_answers:
            error_message("Не удалось удалить таблицу калибровки")
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.clearMessage()

    def set_dac_valur(self):
        """
        sends dac value to device
        :return:
        """
        # to do граничные значения
        dac_value: int = self.SpinDACValue.value()
        answer = Usbhost.send_command(self.port, "SetDACValue", self.state.device, dac_value)
        if answer in wrong_answers:
            error_message("Не удалось задать значение ЦАП")
            self.statusbar.showMessage(answer_translate[answer])
        else:
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
