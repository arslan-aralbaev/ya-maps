import sys
from PyQt5.QtWidgets import QStatusBar, QMainWindow, QApplication, QComboBox
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QDialog
from PyQt5.QtCore import QMetaObject, QCoreApplication


class MainWindow(object):
    def setupUi(self, window):
        """создание объектов формы"""
        window.setObjectName("MainWindow")
        window.resize(570, 120)
        self.w, self.h = self.size().width(), self.size().height()
        self.centralwidget = QWidget(window)
        self.s_line = QLineEdit(self.centralwidget)
        self.search = QPushButton(self.centralwidget)
        self.list_1 = QComboBox(self.centralwidget)
        """const"""
        window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(window)
        window.setStatusBar(self.statusbar)
        self.retranslateUi(window)
        QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "search"))
        self.s_line.setToolTip(_translate("MainWindow", "set your search"))
        self.search.setText(_translate("MainWindow", "Go! 🔎"))

    def resizeEvent(self, event):
        w1, h1 = self.size().width(), self.size().height()
        w, h = w1 / self.w, h1 / self.h
        self.centralwidget.setGeometry(*map(int, (0 * w, 0 * h, 570 * w, 50 * h)))
        self.s_line.setGeometry(*map(int, (10 * w, 10 * h, 470 * w, 40 * h)))
        self.search.setGeometry(*map(int, (480 * w, 9 * h, 80 * w, 42 * h)))
        self.list_1.setGeometry(*map(int, (10 * w, 60 * h, 550 * w, 40 * h)))


class Form(QMainWindow, MainWindow):
    def __init__(self, get_search: object, return_rez: object):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.s_line.editingFinished.connect(self.search_fu)
        self.in_fu, self.out_fu = get_search, return_rez
        self.search.clicked.connect(self.search_fu)

    def initUI(self):
        pass

    def search_fu(self):
        if self.list_1.count() > 0:
            self.out_fu(self.list_1.currentText())
            self.emitAndClose
        else:
            self.in_fu(self.s_line.text())

    def add_place(self, text: str):
        self.list_1.addItem(text)



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main_th(get_search: object, return_rez: object):
    """app = QApplication(sys.argv)
    main = Form(get_search, return_rez)
    main.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
    """
    sys.excepthook = except_hook
    Dialog = QDialog(Form(get_search, return_rez))