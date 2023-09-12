from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt




class Main(QDialog):
    def __init__(self, object_1, object_2):
        super().__init__()
        loadUi('../../UI/MainPage.ui', self)
        self.btn_event()
        self.window_option()
        self.object_1 = object_1
        self.object_2 = object_2

    def window_option(self):
        """프로그램 초기 설정 이벤트 함수"""
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.stackedWidget.setCurrentIndex(0)

    def btn_event(self):
        """버튼 클릭 이벤트 함수"""
        self.exit_btn.clicked.connect(self.close_event)
        self.exit_btn2.clicked.connect(self.close_event)
        self.join_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.back_btn.clicked.connect(self.join_page_back_situation)
        self.hide_btn.clicked.connect(self.hide_btn_situation)
        self.login_btn.clicked.connect(self.go_main_page)

    # ========================================== 타이틀 클릭 이벤트 ======================================== #
    def close_event(self):
        """닫기 버튼 클릭 했을 때 일어나는 이벤트 함수"""
        self.object_1.hide()
        self.object_2.hide()
        self.close()

    def hide_btn_situation(self):
        """윈도우 타이틀 창 숨기기 버튼 클릭시 발생 이벤트 함수"""
        self.hide()

    # ========================================== 로그인 / 회원가입 ========================================= #
    def join_page_back_situation(self):
        """회원가입 페이지에서 뒤로가기 버튼 클릭 시 이벤트 함수"""
        self.join_id.clear()
        self.join_pw.clear()
        self.check_pw.clear()
        self.join_name.clear()
        self.stackedWidget.setCurrentIndex(0)

    def go_main_page(self):
        """로그인 버튼 클릭 시 메인 페이지로 이동하는 함수"""
        self.stackedWidget.setCurrentIndex(2)
