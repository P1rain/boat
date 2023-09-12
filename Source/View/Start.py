import sys

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from Source.View.Main import Main


class Start(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/StartPage.ui', self)
        self.btn_event()
        self.window_option()
        self.font_option()

    def window_option(self):
        """프로그램 초기 설정 이벤트 함수"""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.logo_btn.hide()
        self.logo_lbl.hide()

    def font_option(self):
        """폰트 설정 이벤트 함수"""
        fontDB = QFontDatabase()
        fontDB.addApplicationFont("../../Font/GMARKETSANSTTFBOLD.ttf")
        fontDB.addApplicationFont("../../Font/GmarketSansTTFMedium.ttf")
        fontDB.addApplicationFont("../../Font/KIMJUNGCHULSCRIPT-REGULAR.ttf")
        fontDB.addApplicationFont("../../Font/TMONEYROUNDWINDEXTRABOLD.ttf")
        fontDB.addApplicationFont("../../Font/THE_Nakseo.ttf")

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.window_btn.clicked.connect(lambda: self.close())
        self.icon_btn.clicked.connect(self.go_login_page)
        self.logo_btn.clicked.connect(self.main_page_show)

    def go_login_page(self):
        """로그인 페이지 함수로 이동하는 함수"""
        self.logo_btn.show()
        self.logo_lbl.show()
        self.main = Main(self.logo_btn, self.logo_lbl)
        self.main.exec_()

    def main_page_show(self):
        """윈도우 창 하단 해듀윌 버튼 클릭 시 메인 페이지 show 함수"""
        self.main.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Start()
    myWindow.show()
    app.exec_()
