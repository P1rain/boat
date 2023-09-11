import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class Start(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../../UI/StartPage.ui', self)
        self.btn_event()
        self.window_option()

    def window_option(self):
        """프로그램 초기 설정 이벤트 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.window_btn.clicked.connect(lambda: self.close())
        self.icon_btn.clicked.connect(self.go_to_main)

    def go_to_main(self):
        """메인 페이지 함수로 이동하는 함수"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Start()
    myWindow.show()
    app.exec_()