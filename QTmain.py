from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtWidgets import QComboBox, QApplication
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
import sys
import requests


def get_geo(place, postal_code_bullin):
    apikey = '40d1649f-0493-4b70-98ba-98533de7710b'
    geocoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={apikey}&geocode={place}&format=json'
    response = requests.get(geocoder_request)
    if response:
        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_postalcode = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"] \
                if postal_code_bullin else '000000'
            ll = [float(toponym_coodrinates.split(' ')[0]), float(toponym_coodrinates.split(' ')[1])]
            full_info = toponym_address, toponym_postalcode, toponym_coodrinates
            return ll
        except Exception as ex:
            print('!!error!!!', geocoder_request, ex)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(773, 581)
        self.w, self.h = self.size().width(), self.size().height()
        self.centralwidget = QWidget(MainWindow)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.t1 = QWidget()
        self.map = QLabel(self.t1)
        self.map.setText("ppppppppppppppppppppp")
        self.lb = QPushButton(self.t1)
        self.db = QPushButton(self.t1)
        self.rb = QPushButton(self.t1)
        self.ub = QPushButton(self.t1)
        self.mb = QPushButton(self.t1)
        self.pb = QPushButton(self.t1)
        self.tabWidget.addTab(self.t1, "")
        self.t2 = QWidget()
        self.sl = QLineEdit(self.t2)
        self.sb = QPushButton(self.t2)
        self.xb = QPushButton(self.t2)
        self.vari = QComboBox(self.t2)
        self.gb = QPushButton(self.t2)
        self.tabWidget.addTab(self.t2, "")
        self.pixmap = QPixmap()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setAccessibleName(_translate("MainWindow", "home"))
        self.lb.setText(_translate("MainWindow", "<"))
        self.db.setText(_translate("MainWindow", "V"))
        self.rb.setText(_translate("MainWindow", ">"))
        self.ub.setText(_translate("MainWindow", "^"))
        self.mb.setText(_translate("MainWindow", "M"))
        self.pb.setText(_translate("MainWindow", "P"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.t1), _translate("MainWindow", "MAP"))
        self.t2.setAccessibleName(_translate("MainWindow", "search"))
        self.sb.setText(_translate("MainWindow", "Search"))
        self.xb.setText(_translate("MainWindow", "X"))
        self.gb.setText(_translate("MainWindow", "GO"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.t2), _translate("MainWindow", "search"))

    def resizeEvent(self, event):
        """настройка зависимости размеров элементов от размеров окна"""
        w1, h1 = self.size().width(), self.size().height()
        w, h = w1 / self.w, h1 / self.h
        self.tabWidget.setGeometry(*map(int, (0 * w, 0 * h, 773 * w, 581 * h)))
        self.map.setGeometry(*map(int, (0 * w, 0 * h, 773 * w, 551 * h)))
        self.lb.setGeometry(*map(int, (0 * w, 220 * h, 31 * w, 61 * h)))
        self.db.setGeometry(*map(int, (350 * w, 525 * h, 61 * w, 31 * h)))
        self.rb.setGeometry(*map(int, (736 * w, 220 * h, 31 * w, 61 * h)))
        self.ub.setGeometry(*map(int, (340 * w, 0 * h, 61 * w, 31 * h)))
        self.mb.setGeometry(*map(int, (727 * w, 0 * h, 41 * w, 41 * h)))
        self.pb.setGeometry(*map(int, (687 * w, 0 * h, 41 * w, 41 * h)))
        self.sl.setGeometry(*map(int, (0 * w, 10 * h, 620 * w, 41 * h)))
        self.sb.setGeometry(*map(int, (624 * w, 9 * h, 101 * w, 43 * h)))
        self.xb.setGeometry(*map(int, (726 * w, 9 * h, 41 * w, 43 * h)))
        self.vari.setGeometry(*map(int, (0 * w, 80 * h, 684 * w, 61 * h)))
        self.gb.setGeometry(*map(int, (686 * w, 79 * h, 81 * w, 63 * h)))
        self.map.setPixmap(self.pixmap.scaled(*map(int, (0 * w, 0 * h, 773 * w, 551 * h))))


class MyWidget(QMainWindow, MainWindow):
    last = ''
    ll = [32.530887, 55.703118]
    scale, mapZoom = 2.0, 15
    landArray = ['map', 'sat', 'skl', 'trf']
    pmArray = list()
    lCount = 0
    past = ''
    kToMoveMap = 0.002
    adressArray = list()

    def __init__(self):
        super().__init__()
        self.binds = {Qt.Key_S: lambda: self.moove_co(0, -1), Qt.Key_W: lambda: self.moove_co(0, 1),
                      Qt.Key_A: lambda: self.moove_co(-1, 0), Qt.Key_D: lambda: self.moove_co(1, 0),
                      Qt.Key_Equal: lambda: self.zoom_m(1), Qt.Key_Minus: lambda: self.zoom_m(-1),
                      Qt.Key_M: self.switch_mode, Qt.Key_H: self.hide, Qt.Key_P: self.point_point}
        self.setupUi(self)
        """self.tabWidget.setCurrentWidget(self.tab_2)"""
        self.lb.clicked.connect(self.binds[Qt.Key_A])
        self.rb.clicked.connect(self.binds[Qt.Key_D])
        self.ub.clicked.connect(self.binds[Qt.Key_W])
        self.db.clicked.connect(self.binds[Qt.Key_S])
        self.mb.clicked.connect(self.binds[Qt.Key_M])
        self.pb.clicked.connect(self.binds[Qt.Key_P])
        self.xb.clicked.connect(self.clear_re)
        self.gb.clicked.connect(self.show_searched)
        self.sb.clicked.connect(self.search)
        self.sl.editingFinished.connect(self.search)
        self.initUI()

    def initUI(self):
        pass

    def hide(self):
        if not self.lb.isHidden():
            self.lb.hide()
            self.rb.hide()
            self.ub.hide()
            self.db.hide()
            self.mb.hide()
            self.pb.hide()
        else:
            self.lb.show()
            self.rb.show()
            self.ub.show()
            self.db.show()
            self.mb.show()
            self.pb.show()

    def moove_co(self, dx, dy):
        self.ll[0] += dx * self.mapZoom * self.kToMoveMap
        self.ll[1] += dy * self.mapZoom * self.kToMoveMap
        self.update_image()

    def switch_mode(self):
        self.lCount = 0 if self.lCount == 3 else self.lCount + 1
        self.update_image()

    def zoom_m(self, d):
        if self.mapZoom + d in range(1, 23):
            self.mapZoom += d
            self.update_image()

    def keyPressEvent(self, event):
        key = event.key()
        if key in self.binds.keys():
            self.binds[key]()

    def create_base_point(self, anypm, long, lat):
        if self.pmArray:
            self.pmArray.append('~' + str(long) + ',' + str(lat))
        else:
            self.pmArray.append('&' + anypm + '=' + str(long) + ',' + str(lat))
        # print(self.pmArray, self.pmArray[-1])

    def point_point(self):
        if len(self.pmArray) >= 99:
            return False
        self.create_base_point('pt', self.ll[0], self.ll[1])
        self.update_image()

    def search(self):
        text = self.sl.text()
        # searching
        self.vari.clear()
        rez = [text]
        if text not in self.adressArray:
            self.adressArray.append(text)
            # collecting rezults
        self.vari.addItems(self.adressArray)

    def show_searched(self):
        text = self.vari.currentText()
        # изменение координат в self.ll
        self.ll = get_geo(text, False)
        self.create_base_point('pt', self.ll[0], self.ll[1])
        self.tabWidget.setCurrentIndex(0)
        self.update_image()

    def clear_re(self):
        self.vari.clear()
        self.sl.clear()
        self.pmArray.pop(-1) if self.pmArray else print('point list is empty')
        self.update_image()

    def update_image(self):
        land, zoom, longLat, pmArray = self.landArray[self.lCount], self.mapZoom, self.ll, self.pmArray
        if land == 'saat':
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}' \
                          f'&z={zoom}&spn=0.002,0.002&l={land}'
        else:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={float(longLat[0])},{float(longLat[1])}' \
                          f'&z={zoom}&pn=0.002,0.002&l={land}' + ','.join(pmArray)
        try:
            response = requests.get(map_request, timeout=10)
        except Exception as ex:
            response = False
            re = f"Ошибка выполнения запроса: {map_request}\nHttp статус: {ex})"
            self.map.setText(re)
        if response:
            self.pixmap.loadFromData(response.content)
            self.map.setPixmap(self.pixmap.scaled(int(773 * self.size().width() / self.w),
                                                  int(551 * self.size().height() / self.h)))
            self.map.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
