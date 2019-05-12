import design
from loguru import logger
import sys
from dataclasses import *
from PyQt5 import QtWidgets

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


class Synthetizer(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = State(state=0)

        self.set_hand_active()

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
        self.LblDescr.setText("Выбрано устройство %s. Устройство работает в %s режиме" % (addr, states[state]))

@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Synthetizer()  # Создаём объект класса
    window.show()# Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()