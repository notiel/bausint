import design
import sys
import os
from dataclasses import *
from PyQt5 import QtWidgets, QtCore
from Usbhost import UsbHost
from typing import Dict
import csv
import datetime
from loguru import logger

import registers

wrong_answers = ['Bad data', "Unknown command", "No device port", 'Port error']
answer_translate = {'Bad data': "Неверные данные", "Unknown command": 'Неизвестная команда',
                    "No device port": "Устройство не подключено", "Port error": "Ошибка порта"}
answer_codes = {'Ok': 'Ack 0', 'Unknown command': 'Ack 6', 'Bad data': 'Ack 7'}

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


states_dict = {"L1": [1575.42, 296.979], 'L2': [1227.60, 314.37], 'L5': [1176.45, 316.9275]}


@dataclass
class State:
    state: int = 0
    device_id: int = -1
    comport: str = ""
    ser = None
    syncro = False
    message = "Частотный преобразователь не подключен"
    range: str = ""


class Synthetizer(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = State()
        self.devices: Dict[int, str] = dict()
        self.calibr_table: Dict[int, float] = dict()
        self.UsbHost = UsbHost()

        # self.set_hand_active()
        self.statusbar.showMessage("Частотный преобразователь не подключен")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.command_dict = {self.BtnSetFine: "SetDac", self.BtnSetRough: "SetFreqRough",
                             self.BtnSetDACValue: "SetDac",
                             self.BtnStop: "Stop", self.BtnL1: 'SyntL1', self.BtnL2: 'SyntL2', self.BtnL5: 'SyntL5',
                             self.BtnAttenuate: "SetAtt", self.BtnStart: "Start"}

        self.error_dict = {self.BtnSetFine: "Не удалось задать сдвиг точно",
                           self.BtnSetRough: "Не удалось задать сдвиг грубо",
                           self.BtnSetDACValue: "Не удалось задать значение ЦАП",
                           self.BtnStop: "Не удалось остановить эксперимент",
                           self.BtnStart: "Не удалось начать эксперимент",
                           self.BtnL1: 'Не удалось задать частотный диапазон',
                           self.BtnL2: 'Не удалось задать частотный диапазон',
                           self.BtnL5: 'Не удалось задать частотный диапазон',
                           self.BtnAttenuate: "Не удалось задать ослабленние выходного сигнала"}
        self.result_dict = {self.BtnSetFine: "Точная частота задана", self.BtnSetRough: "Частота задана грубо",
                            self.BtnSetDACValue: "Задано значение ЦАП",
                            self.BtnStop: "Эксперимент остановлен", self.BtnL1: 'Выбран диапазон L1',
                            self.BtnL2: 'Выбран диапазон L2', self.BtnL5: 'Выбран диапазон L5',
                            self.BtnAttenuate: "Задано ослабление выходного сигнала"}

        self.spins = {self.BtnAttenuate: self.SpinAttenuate, self.BtnSetRough: self.SpinRough,
                      self.BtnSetFine: self.SpinFine, self.BtnSetDACValue: self.SpinDACValue}

        self.val_labels = {self.BtnAttenuate: self.LblAttVal, self.BtnSetRough: self.LblMoveVal,
                           self.BtnSetDACValue: self.LblDacVal, self.BtnSetFine: None}

        self.val_dimensions = {self.BtnAttenuate: " дБ", self.BtnSetRough: " Гц",
                               self.BtnSetDACValue: "", self.BtnSetFine: None}

        self.controls = [self.BtnConnect, self.BtnSyncro, self.BtnL1, self.BtnL2, self.BtnL5,
                         self.BtnAttenuate, self.SpinAttenuate, self.GBState, self.GBReg,
                         self.GBHand, self.BtnSetDACValue, self.SpinDACValue, self.BtnSetRough, self.SpinRough,
                         self.BtnSetFine, self.SpinFine, self.GBAuto, self.BtnSetFreqFile, self.BtnStart, self.BtnStop]

        self.btns = {self.BtnL1: self.LblL1, self.BtnL2: self.LblL2, self.BtnL5: self.LblL5}

        self.BtnRescan.clicked.connect(self.scan_ports)
        self.BtnConnect.clicked.connect(self.change_device)
        self.BtnSyncro.clicked.connect(self.set_current_time)
        self.BtnL1.clicked.connect(self.send_reg_command)
        self.BtnL2.clicked.connect(self.send_reg_command)
        self.BtnL5.clicked.connect(self.send_reg_command)
        self.BtnSetRough.clicked.connect(self.send_reg_command)

        self.BtnSetDACValue.clicked.connect(self.send_command_with_parameter)
        self.BtnAttenuate.clicked.connect(self.send_command_with_parameter)
        self.BtnSetFine.clicked.connect(self.send_command_with_parameter)

        self.BtnSetCalTable.clicked.connect(self.read_calibr_table)

        # self.BtnDeleteCalTable.clicked.connect(self.send_command)
        # self.BtnSetFreqFile.clicked.connect(self.set_freq_table)
        # self.BtnStop.clicked.connect(self.send_command)

        self.scan_ports()
        if os.path.exists("Calibration_DAC.csv"):
            self.set_calibr_table("Calibration_DAC.csv")

    def scan_ports(self):
        self.set_controls_state(False)
        if self.state.ser:
            UsbHost.close_port(self.state.ser)
        self.state = State()
        self.statusbar.showMessage("Идет сканирование портов")
        self.state.message = "Идет сканирование портов"
        self.statusbar.showMessage(self.state.message)
        self.BtnConnect.setEnabled(False)
        self.CBDevices.clear()
        self.devices = UsbHost.get_all_device_ports_with_id()
        self.CBDevices.addItems([str(x) for x in self.devices.keys()])
        if self.devices.keys():
            self.BtnConnect.setEnabled(True)
            self.create_message()
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
        self.LblFreqVal.setText("-")
        self.LblStateVal.setText("Ручной")
        self.LblMoveVal.setText("0 Гц")
        self.LblResVal.setText("Неизвестно")
        self.LblAttVal.setText("Неизвестно")
        self.SpinRough.setValue(0)
        self.SpinFine.setValue(0)
        self.SpinDACValue.setValue(0)
        self.SpinAttenuate.setValue(30)
        self.TxtLog.clear()
        if not self.calibr_table:
            self.SpinFine.setEnabled(False)
            self.BtnSetFine.setEnabled(False)
        for btn in self.btns.keys():
            btn.setStyleSheet("")
            self.btns[btn].setStyleSheet("font: 16px")

    def send_reg_command(self):
        """
        sends command to change state to l1, l2, l5
        :return:
        """
        button = self.sender()
        if button in self.btns.keys():
            state: str = button.text()
            move = None
        else:
            state = self.state.range
            move = (self.SpinRough.value() // 500) * 500
        param = registers.get_reg_str(state, move)
        answer: str = self.UsbHost.send_command(self.state.ser, "SetAdf14", str(self.state.device_id),
                                                param)
        if answer == 'Ok':
            self.statusbar.showMessage(self.result_dict[button])
            # при установлении диапазона, он записывается в интерфейсе везде
            if button in self.btn.keys():
                self.state.range = button.text()
                self.LblFreqVal.setText(button.text())
                self.LblResVal.setText(str(states_dict[button.text()][0] +
                                           self.SpinFine.value() + self.SpinRough.value()))
                # все кнопки серые, кроме кнопки режима
                for btn in self.btns.keys():
                    btn.setStyleSheet("")
                    self.btns[btn].setStyleSheet("font: 16px")
                button.setStyleSheet("background-color : rgb(70, 210, 00)")
                self.btns[button].setStyleSheet("color: red; font:  bold 16px")
        else:
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])

        # add commands to log
        param = registers.get_reg_str(state, move).replace(" ", '\n')
        param.replace(" ", "\n")
        self.create_log_message(button.text(), answer, param)

        # set sw command
        if answer == 'Ok' and button in self.btn.keys():
            params = '0 1' if button == self.BtnL1 else "1 0"
            self.set_sw(params)

    def send_command(self):
        """
        sends command and shows status depending on sender
        :return:
        """
        button = self.sender()
        answer: str = self.UsbHost.send_command(self.state.ser, self.command_dict[button], str(self.state.device_id))
        if answer == 'Ok':
            self.statusbar.showMessage(self.result_dict[button])
        else:
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])
        self.create_log_message(self.command_dict[button], answer, "")

    def send_command_with_parameter(self):
        """
        sends command with parameter and shows status depending on sender
        :return:
        """
        button = self.sender()
        param = self.spins[button].value() if button != self.BtnSetFine else\
            get_dac_value(self.SpinFine.value(), self.calibr_table, self.state.range)

        answer: str = self.UsbHost.send_command(self.state.ser, self.command_dict[button],
                                                str(self.state.device_id), param)
        if answer != 'Ok':
            error_message(self.error_dict[button])
            self.statusbar.showMessage(answer_translate[answer])
        else:
            self.statusbar.showMessage(self.result_dict[button])
            try:
                # добавляем размерность
                if self.val_labels[button]:
                    self.val_labels[button].setText(str(self.spins[button].value()) + self.val_dimensions[button])
                # устанавливаем зависимость цап и сдвига
                self.set_fine_and_dac(button)
                # пересчитываем значение сдвига
                self.LblMoveVal.setText(str(self.SpinFine.value() + self.SpinRough.value())
                                        + self.val_dimensions[self.BtnSetRough])
                # пересчитываем результирующую частоту
                if self.state.range:
                    self.LblResVal.setText("%.4f MГц" % (states_dict[self.state.range][0] +
                                           float(self.LblMoveVal.text().split()[0])/1000000))
            except KeyError:
                pass
        self.create_log_message(self.command_dict[button], answer,  str(param))

    def set_fine_and_dac(self, button):
        """
        updates fine shift fields if dac changed and vice versa
        :param button: button pressed
        :return:
        """
        if button == self.BtnSetDACValue and self.calibr_table:
            dac = round(self.SpinDACValue.value() / 10) * 10
            freq = self.calibr_table[dac]
            k = states_dict[self.state.range][1]
            self.SpinFine.setValue(freq * k)
        if button == self.BtnSetFine and self.calibr_table:
            dac = get_dac_value(self.SpinFine.value(), self.calibr_table, self.state.range)
            self.SpinDACValue.setValue(dac)
            self.LblDacVal.setText(str(dac))

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
            self.create_message()
            self.set_controls_state(True)
            self.BtnL1.click()
            self.BtnAttenuate.click()
            self.SpinDACValue.setValue(35000)
            self.BtnSetDACValue.click()
            self.set_sw("0 1")

    def set_sw(self, params: str):
        answer: str = self.UsbHost.send_command(self.state.ser, "SetSW", str(self.state.device_id), params)
        if answer == 'Ok':
            self.statusbar.showMessage("Команда SetSw сработала")
        else:
            error_message("Команда SetSw не сработала")
            self.statusbar.showMessage("Команда SetSw не сработала")
        self.create_log_message("SetSw", answer, params)

    def set_calibr_table(self, filename: str):
        """
        using given csv sets calibration table
        :return:
        """
        try:
            with open(filename, encoding='utf-8') as f:
                data = list(csv.reader(f, delimiter=';'))
                states_dict['L1'][1], states_dict['L2'][1], states_dict['L5'][1] = \
                    float(data[0][0].replace(',', '.')), float(data[0][1].replace(',', '.')), \
                    float(data[0][2].replace(',', '.'))
                for row in data[1:]:
                    self.calibr_table[int(row[0])] = float(row[1].replace(',', '.'))
                self.SpinDACValue.setMinimum(min(self.calibr_table.keys()))
                self.SpinDACValue.setMaximum(max(self.calibr_table.keys()))
        except Exception as e:
            print(e)
            self.SpinDACValue.setMaximum(65535)
            self.SpinDACValue.setMinimum(0)
            self.calibr_table = dict()
        self.create_message()

    def read_calibr_table(self):
        """
        reads and creates calibration table row by row
        :return:
        """
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '.')[0]
        if filename and filename.lower().endswith('.csv'):
            self.set_calibr_table(filename)
            if self.state.ser:
                self.SpinFine.setEnabled(True)
                self.BtnSetFine.setEnabled(True)
        else:
            error_message("Файл не выбран или в формате .csv")

    def create_message(self):
        """
        creates status message
        :return:
        """
        if self.state.ser and self.state.device_id != -1 and self.state.comport:
            self.state.message = "Подключен частотный преобразователь %i через %s порт." \
                                 % (self.state.device_id, self.state.comport)
            if self.state.syncro:
                self.state.message += " Время синхронизировано."
            else:
                self.state.message += " Время не синхронизировано."
        else:
            self.state.message = "Частотный преобразователь не подключен."
        if self.calibr_table:
            self.state.message += " Калибровочная таблица загружена"
        else:
            self.state.message += " Калибровочная таблица не загружена"
        self.statusbar.showMessage(self.state.message)

    def create_log_message(self, command: str, answer: str, params: str):
        """
        adds message to log
        :return:
        """
        answer_log = answer_codes[answer] if answer in answer_codes.keys() else answer
        caption = self.TxtLog.toPlainText()
        self.TxtLog.setText(caption + ">> " + command + " " + str(self.state.device_id) + ' ' + params + '\n'
                            + '<<' + answer_log + '\n')

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
            self.state.syncro = True
            self.create_message()

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
    # def set_freq_table(self):
    #    """
    #    sends calibration table row by row
    #    :return:
    #    """
    #    filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '.')[0]
    #    if filename and filename.lower().endswith('.csv'):
    #        with open(filename) as f:
    #            data = csv.reader(f, encoding='uft-8', delimiter=',')
    #            start_time = data[0]
    #            answer = UsbHost.send_command(self.state.ser, "SetStartTime", str(self.state.device_id), *start_time)
    #            if answer in wrong_answers:
    #                error_message("Не удалось отправить файл эксперимента")
    #                self.statusbar.showMessage(answer_translate[answer])
    #            else:
    #                for row in data[1:]:
    #                    answer = UsbHost.send_command(self.state.ser, "SetCalibrTableRow", str(self.state.device_id),
    #                                                  *row)
    #                    if answer in wrong_answers:
    #                        error_message("Не удалось отправить строку, удаляем файл эксперимента")
    #                        self.BtnDeleteFreqfile.click()
    #                        self.statusbar.showMessage(answer_translate[answer])
    #                        return
    #                self.statusbar.showMessage("Калибровочная таблица отправлена")
    #    else:
    #        error_message("Файл не выбран или в формате .csv")
    #        self.statusbar.clearMessage()

    # refactor
    # def set_hand_state(self, state: bool):
    #    """
    #    sets state status to all objects of hand mode
    #    :param state: state of objects
    #    :return:
    #    """
    #    self.BtnSetCalTable.setEnabled(state)
    #    self.BtnDeleteCalTable.setEnabled(state)
    #    self.BtnSetDACValue.setEnabled(state)
    #    self.BtnSetFine.setEnabled(state)
    #    self.BtnSetRough.setEnabled(state)
    #    self.SpinDACValue.setEnabled(state)
    #    self.SpinFine.setEnabled(state)
    #    self.SpinRough.setEnabled(state)

    # refactor
    # def set_auto_state(self, state: bool):
    #    """
    #    sets state status to all objects of auto mode
    #    :param state: state of objects
    #    :return:
    #    """
    #    self.BtnSetFreqFile.setEnabled(state)
    #    self.BtnStop.setEnabled(state)
    #    self.BtnStart.setEnabled(state)

    # refactor
    # def set_hand_active(self):
    #    """
    #    sets hand mode to ui
    #    :return:
    #    """
    #    self.set_auto_state(False)
    #    self.set_hand_state(True)

    # refactor
    # def set_auto_active(self):
    #    """
    #    sets auto mode to ui
    #    :return:
    #    """
    #    self.set_hand_state(False)
    #    self.set_auto_state(True)

    # answer = UsbHost.send_command(self.state.ser, "SetCalibrTableRow",
    #                              str(self.state.device_id), row[0], row[1])
    # if answer in wrong_answers:
    #    error_message("Не удалось отправить строку, удаляем калибровочную таблицу")
    #    self.BtnDeleteCalTable.click()
    #    self.statusbar.showMessage(answer_translate[answer])
    #    return
    # self.statusbar.showMessage("Калибровочная таблица отправлена")


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


def get_dac_value(fine_shift: int, table: Dict[int, float], state: str):
    """
    get dac value using calibration table
    :param state: l1, l2 or l3
    :param fine_shift: fine freq shift
    :param table: table with calibration value of dac
    :return: nearest dac value
    """
    if state not in ["L1", "L2", "L5"]:
        return 0
    shift_k = fine_shift/states_dict[state][1]
    if shift_k <= table[min(table.keys())]:
        return table[min(table.keys())]
    if shift_k >= table[max(table.keys())]:
        return table[max(table.keys())]
    temp = [(abs(x[1] - shift_k), x[0]) for x in table.items()]
    temp.sort(key=lambda x: x[0])
    return temp[0][1]


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Synthetizer()  # Создаём объект класса
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
