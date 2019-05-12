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


class Synthetizer(design.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super.__init__()
        self.setupUi(self)
        self.state = State(state=0)


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Synthetizer()  # Создаём объект класса
    window.show()# Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()